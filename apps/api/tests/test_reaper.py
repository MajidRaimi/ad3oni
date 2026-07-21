from datetime import UTC, datetime, timedelta
from typing import Any, cast

import pytest
from arq import ArqRedis
from src.features.ingestion.reaper import (
    GIVE_UP_MINUTES,
    STALE_MINUTES,
    _parse_timestamp,
    reap_stuck_prayers,
)
from src.shared.config.settings import Settings
from src.shared.queue.context import WorkerContext


def _iso(minutes_ago: float) -> str:
    stamp = datetime.now(tz=UTC) - timedelta(minutes=minutes_ago)
    return stamp.strftime("%Y-%m-%d %H:%M:%S.000Z")


class FakePocketBase:
    def __init__(self, records: list[dict[str, Any]]) -> None:
        self._records = records
        self.updated: list[tuple[str, dict[str, Any]]] = []

    async def list_records(
        self, collection: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return {"items": self._records}

    async def update_record(
        self, collection: str, record_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        self.updated.append((record_id, payload))
        return {"id": record_id, **payload}


class FakeRedis:
    def __init__(self) -> None:
        self.jobs: list[tuple[str, tuple[Any, ...]]] = []

    async def enqueue_job(self, name: str, *args: Any) -> None:
        self.jobs.append((name, args))


def _context(pocketbase: FakePocketBase) -> WorkerContext:
    return WorkerContext(
        settings=Settings(ai_model="test-model"),
        pocketbase=cast(Any, pocketbase),
        ai=cast(Any, None),
        http=cast(Any, None),
    )


def _record(prayer_id: str, status: str, age_minutes: float) -> dict[str, Any]:
    return {
        "id": prayer_id,
        "status": status,
        "created": _iso(age_minutes),
        "updated": _iso(age_minutes),
    }


def test_parse_timestamp_handles_pocketbase_format() -> None:
    parsed = _parse_timestamp("2026-07-21 12:05:33.142Z")
    assert parsed is not None
    assert parsed.tzinfo is not None
    assert parsed.year == 2026 and parsed.hour == 12


def test_parse_timestamp_rejects_garbage() -> None:
    assert _parse_timestamp("not a date") is None
    assert _parse_timestamp("") is None


@pytest.mark.asyncio
async def test_fresh_prayer_is_left_alone() -> None:
    pb = FakePocketBase([_record("p1", "processing", STALE_MINUTES - 1)])
    redis = FakeRedis()
    await reap_stuck_prayers(_context(pb), cast(ArqRedis, redis))
    assert redis.jobs == []
    assert pb.updated == []


@pytest.mark.asyncio
async def test_stuck_processing_prayer_is_requeued() -> None:
    pb = FakePocketBase([_record("p1", "processing", STALE_MINUTES + 1)])
    redis = FakeRedis()
    await reap_stuck_prayers(_context(pb), cast(ArqRedis, redis))
    assert redis.jobs == [("process_prayer", ("p1",))]
    assert pb.updated == []


@pytest.mark.asyncio
async def test_stuck_pending_prayer_is_requeued() -> None:
    pb = FakePocketBase([_record("p1", "pending", STALE_MINUTES + 2)])
    redis = FakeRedis()
    await reap_stuck_prayers(_context(pb), cast(ArqRedis, redis))
    assert redis.jobs == [("process_prayer", ("p1",))]


@pytest.mark.asyncio
async def test_ancient_prayer_is_failed_not_requeued() -> None:
    pb = FakePocketBase([_record("p1", "processing", GIVE_UP_MINUTES + 1)])
    redis = FakeRedis()
    await reap_stuck_prayers(_context(pb), cast(ArqRedis, redis))
    assert redis.jobs == []
    assert pb.updated and pb.updated[0][0] == "p1"
    assert pb.updated[0][1]["status"] == "failed"


@pytest.mark.asyncio
async def test_mixed_batch_routes_each_prayer_correctly() -> None:
    pb = FakePocketBase(
        [
            _record("fresh", "processing", STALE_MINUTES - 1),
            _record("stuck", "processing", STALE_MINUTES + 5),
            _record("ancient", "pending", GIVE_UP_MINUTES + 10),
        ]
    )
    redis = FakeRedis()
    await reap_stuck_prayers(_context(pb), cast(ArqRedis, redis))
    assert redis.jobs == [("process_prayer", ("stuck",))]
    assert [r[0] for r in pb.updated] == ["ancient"]
