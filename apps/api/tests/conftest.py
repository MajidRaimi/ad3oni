from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from src.shared.dependencies import get_pocketbase, get_queue
from src.shared.ratelimit.limiter import limiter

GROUP: dict[str, Any] = {"id": "g1", "name": "المشاعر", "slug": "emotion"}
CATEGORY: dict[str, Any] = {
    "id": "c1",
    "name": "القلق والهمّ",
    "slug": "anxiety",
    "expand": {"group": GROUP},
}
PRAYER_TYPE: dict[str, Any] = {"id": "t1", "name": "نبوي", "slug": "prophetic"}
PRAYER: dict[str, Any] = {
    "id": "p1",
    "text": "اللهم اغفر لي وارحمني",
    "status": "confirmed",
    "created": "2026-05-30 00:00:00.000Z",
    "updated": "2026-05-30 00:00:00.000Z",
    "expand": {"category": CATEGORY, "type": PRAYER_TYPE},
}


class FakePocketBase:
    def __init__(self) -> None:
        self.created: list[dict[str, Any]] = []

    async def list_records(
        self, collection: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        table: dict[str, list[dict[str, Any]]] = {
            "groups": [GROUP],
            "categories": [CATEGORY],
            "types": [PRAYER_TYPE],
            "prayers": [PRAYER],
        }
        items = table.get(collection, [])
        return {
            "items": items,
            "page": 1,
            "perPage": 20,
            "totalItems": len(items),
            "totalPages": 1,
        }

    async def get_first(
        self, collection: str, filter_: str, *, expand: str | None = None
    ) -> dict[str, Any] | None:
        records: dict[str, dict[str, Any]] = {
            "groups": GROUP,
            "categories": CATEGORY,
            "types": PRAYER_TYPE,
            "prayers": PRAYER,
        }
        record = records.get(collection)
        if record is None:
            return None
        if "missing" in filter_:
            return None
        return record

    async def create_record(
        self, collection: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        self.created.append(payload)
        return {
            "id": "new1",
            "status": payload["status"],
            "created": "2026-05-30 00:00:00.000Z",
        }


class FakeQueue:
    def __init__(self) -> None:
        self.jobs: list[tuple[str, tuple[Any, ...]]] = []

    async def enqueue_job(self, name: str, *args: Any) -> None:
        self.jobs.append((name, args))


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app()
    fake = FakePocketBase()
    queue = FakeQueue()
    app.dependency_overrides[get_pocketbase] = lambda: fake
    app.dependency_overrides[get_queue] = lambda: queue
    limiter.enabled = False
    test_client = TestClient(app)
    test_client.fake = fake  # type: ignore[attr-defined]
    test_client.queue = queue  # type: ignore[attr-defined]
    yield test_client
    app.dependency_overrides.clear()
    limiter.enabled = True
