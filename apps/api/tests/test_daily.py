import asyncio
import re
from collections.abc import Iterator
from typing import Any, cast

import pytest
from arq import ArqRedis
from fastapi.testclient import TestClient
from src.features.daily.keys import DAILY_CURRENT, DAILY_HISTORY
from src.features.daily.selection import assign_daily_prayer, select_daily_prayer_id
from src.main import create_app
from src.shared.dependencies import get_pocketbase, get_redis
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.ratelimit.limiter import limiter

BytesSet = set[bytes]

GROUP: dict[str, Any] = {"id": "g1", "name": "المشاعر", "slug": "emotion"}
CATEGORY: dict[str, Any] = {
    "id": "c1",
    "name": "القلق والهمّ",
    "slug": "anxiety",
    "expand": {"group": GROUP},
}
PRAYER_TYPE: dict[str, Any] = {"id": "t1", "name": "نبوي", "slug": "prophetic"}

_ID_PATTERN = re.compile(r'id = "([^"]+)"')


def _confirmed(prayer_id: str) -> dict[str, Any]:
    return {
        "id": prayer_id,
        "text": "اللَّهُمَّ اغْفِرْ لِي وَارْحَمْنِي",
        "status": "confirmed",
        "created": "2026-05-30 00:00:00.000Z",
        "updated": "2026-05-30 00:00:00.000Z",
        "expand": {"category": CATEGORY, "type": PRAYER_TYPE},
    }


class FakePocketBase:
    def __init__(
        self,
        confirmed_ids: list[str],
        duplicate_of: list[str] | None = None,
    ) -> None:
        self.confirmed = [_confirmed(prayer_id) for prayer_id in confirmed_ids]
        self.duplicates = [
            {"id": f"d{index}", "status": "duplicate", "duplicate_of": target}
            for index, target in enumerate(duplicate_of or [])
        ]

    async def list_records(
        self, collection: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        filter_ = (params or {}).get("filter", "")
        if 'status = "duplicate"' in filter_:
            items = self.duplicates
        elif 'status = "confirmed"' in filter_:
            items = self.confirmed
        else:
            items = []
        return {
            "items": items,
            "page": 1,
            "perPage": 500,
            "totalItems": len(items),
            "totalPages": 1,
        }

    async def get_first(
        self, collection: str, filter_: str, *, expand: str | None = None
    ) -> dict[str, Any] | None:
        match = _ID_PATTERN.search(filter_)
        if match is None:
            return None
        prayer_id = match.group(1)
        return next(
            (record for record in self.confirmed if record["id"] == prayer_id), None
        )


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.sets: dict[str, set[str]] = {}

    async def get(self, key: str) -> bytes | None:
        value = self.values.get(key)
        return value.encode() if value is not None else None

    async def set(self, key: str, value: str) -> None:
        self.values[key] = value

    async def sadd(self, key: str, *members: str) -> None:
        self.sets.setdefault(key, set()).update(members)

    async def smembers(self, key: str) -> BytesSet:
        return {member.encode() for member in self.sets.get(key, set())}

    async def delete(self, *keys: str) -> int:
        removed = 0
        for key in keys:
            removed += self.values.pop(key, None) is not None
            removed += self.sets.pop(key, None) is not None
        return removed


def _select(pocketbase: FakePocketBase, redis: FakeRedis) -> str | None:
    return asyncio.run(
        select_daily_prayer_id(
            cast(PocketBaseClient, pocketbase), cast(ArqRedis, redis)
        )
    )


def _assign(pocketbase: FakePocketBase, redis: FakeRedis) -> str | None:
    return asyncio.run(
        assign_daily_prayer(cast(PocketBaseClient, pocketbase), cast(ArqRedis, redis))
    )


def _make_client(pocketbase: FakePocketBase, redis: FakeRedis) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_pocketbase] = lambda: pocketbase
    app.dependency_overrides[get_redis] = lambda: redis
    limiter.enabled = False
    return TestClient(app)


@pytest.fixture
def cleanup() -> Iterator[None]:
    yield
    limiter.enabled = True


def test_daily_cold_start_assigns_and_returns_prayer(cleanup: None) -> None:
    pocketbase = FakePocketBase(["p1"])
    redis = FakeRedis()
    with _make_client(pocketbase, redis) as client:
        response = client.get("/v1/daily")
    assert response.status_code == 200
    assert response.json()["id"] == "p1"
    assert redis.values[DAILY_CURRENT] == "p1"
    assert redis.sets[DAILY_HISTORY] == {"p1"}


def test_daily_is_stable_across_calls(cleanup: None) -> None:
    pocketbase = FakePocketBase(["p1", "p2"], duplicate_of=["p1", "p1", "p1"])
    redis = FakeRedis()
    redis.values[DAILY_CURRENT] = "p2"
    with _make_client(pocketbase, redis) as client:
        first = client.get("/v1/daily")
        second = client.get("/v1/daily")
    assert first.json()["id"] == "p2"
    assert second.json()["id"] == "p2"


def test_no_prayers_returns_404(cleanup: None) -> None:
    with _make_client(FakePocketBase([]), FakeRedis()) as client:
        response = client.get("/v1/daily")
    assert response.status_code == 404


def test_duplicate_weighting_picks_most_duplicated() -> None:
    pocketbase = FakePocketBase(
        ["p1", "p2", "p3"], duplicate_of=["p2", "p2", "p2", "p1"]
    )
    redis = FakeRedis()
    for _ in range(20):
        assert _select(pocketbase, redis) == "p2"


def test_selection_skips_history() -> None:
    pocketbase = FakePocketBase(["p1", "p2", "p3"])
    redis = FakeRedis()
    redis.sets[DAILY_HISTORY] = {"p1"}
    for _ in range(20):
        assert _select(pocketbase, redis) in {"p2", "p3"}


def test_auto_recycle_excludes_current() -> None:
    pocketbase = FakePocketBase(["p1", "p2"])
    redis = FakeRedis()
    redis.sets[DAILY_HISTORY] = {"p1", "p2"}
    redis.values[DAILY_CURRENT] = "p1"
    assert _select(pocketbase, redis) == "p2"
    assert DAILY_HISTORY not in redis.sets


def test_assign_writes_current_and_history() -> None:
    pocketbase = FakePocketBase(["p1"])
    redis = FakeRedis()
    prayer_id = _assign(pocketbase, redis)
    assert prayer_id == "p1"
    assert redis.values[DAILY_CURRENT] == "p1"
    assert redis.sets[DAILY_HISTORY] == {"p1"}
