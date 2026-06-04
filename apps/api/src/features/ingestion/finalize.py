from datetime import UTC, datetime

from src.features.ingestion.schema import DuplicateOutcome
from src.shared.queue.context import WorkerContext


def _timestamp() -> str:
    return datetime.now(tz=UTC).isoformat()


async def finalize_rejected(
    context: WorkerContext,
    prayer_id: str,
    violation_type: str | None,
    reason: str | None,
) -> None:
    await context.pocketbase.update_record(
        "prayers",
        prayer_id,
        {
            "status": "rejected",
            "rejection_reason": reason or violation_type or "rejected",
            "ai_model": context.settings.ai_model,
            "processed_at": _timestamp(),
        },
    )


async def finalize_duplicate(
    context: WorkerContext, prayer_id: str, outcome: DuplicateOutcome
) -> None:
    await context.pocketbase.update_record(
        "prayers",
        prayer_id,
        {
            "status": "duplicate",
            "normalized": outcome.normalized,
            "text_hash": outcome.text_hash,
            "duplicate_of": outcome.duplicate_of_id,
            "ai_model": context.settings.ai_model,
            "processed_at": _timestamp(),
        },
    )


async def finalize_confirmed(
    context: WorkerContext,
    prayer_id: str,
    *,
    text: str,
    outcome: DuplicateOutcome,
    category_id: str,
    type_id: str,
) -> None:
    await context.pocketbase.update_record(
        "prayers",
        prayer_id,
        {
            "status": "confirmed",
            "text": text,
            "normalized": outcome.normalized,
            "text_hash": outcome.text_hash,
            "category": category_id,
            "type": type_id,
            "ai_model": context.settings.ai_model,
            "processed_at": _timestamp(),
        },
    )


async def finalize_failed(context: WorkerContext, prayer_id: str) -> None:
    await context.pocketbase.update_record(
        "prayers",
        prayer_id,
        {
            "status": "failed",
            "rejection_reason": "pipeline_error",
            "ai_model": context.settings.ai_model,
            "processed_at": _timestamp(),
        },
    )
