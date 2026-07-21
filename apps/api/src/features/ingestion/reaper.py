from datetime import UTC, datetime
from typing import Any

from arq import ArqRedis

from src.features.ingestion.finalize import finalize_failed
from src.shared.logging.setup import get_logger
from src.shared.queue.context import WorkerContext
from src.shared.queue.pool import enqueue_process_prayer

logger = get_logger("api.ingestion.reaper")

STALE_MINUTES = 5
GIVE_UP_MINUTES = 6 * 60
_PAGE_SIZE = 200
_STUCK_FILTER = '(status = "pending" || status = "processing")'


def _parse_timestamp(value: str) -> datetime | None:
    text = value.strip().replace(" ", "T")
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


async def _collect_stuck(context: WorkerContext) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    page = 1
    while True:
        data = await context.pocketbase.list_records(
            "prayers",
            {
                "filter": _STUCK_FILTER,
                "page": page,
                "perPage": _PAGE_SIZE,
                "skipTotal": True,
                "sort": "created",
                "fields": "id,status,created,updated",
            },
        )
        items = data.get("items", [])
        records.extend(items)
        if len(items) < _PAGE_SIZE:
            return records
        page += 1


async def reap_stuck_prayers(context: WorkerContext, redis: ArqRedis) -> None:
    now = datetime.now(tz=UTC)
    stuck = await _collect_stuck(context)

    requeued = 0
    failed = 0
    for record in stuck:
        stamp = _parse_timestamp(record.get("updated") or record.get("created") or "")
        if stamp is None:
            continue
        age_minutes = (now - stamp).total_seconds() / 60
        if age_minutes < STALE_MINUTES:
            continue

        prayer_id = record["id"]
        if age_minutes >= GIVE_UP_MINUTES:
            await finalize_failed(context, prayer_id)
            logger.warning(
                "prayer_reaped_failed id=%s age_min=%.0f", prayer_id, age_minutes
            )
            failed += 1
            continue

        await enqueue_process_prayer(redis, prayer_id)
        logger.info(
            "prayer_reaped_requeued id=%s status=%s age_min=%.0f",
            prayer_id,
            record.get("status"),
            age_minutes,
        )
        requeued += 1

    if requeued or failed:
        logger.info("reaper_done requeued=%d failed=%d", requeued, failed)
