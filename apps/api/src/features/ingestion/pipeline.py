from src.features.ingestion.agents.categorize import categorize
from src.features.ingestion.agents.compliance import review_compliance
from src.features.ingestion.agents.dedup import find_duplicate
from src.features.ingestion.agents.diacritize import diacritize
from src.features.ingestion.agents.spelling import correct_spelling
from src.features.ingestion.claim import claim_prayer
from src.features.ingestion.finalize import (
    finalize_confirmed,
    finalize_duplicate,
    finalize_rejected,
)
from src.shared.logging.setup import get_logger
from src.shared.queue.context import WorkerContext

logger = get_logger("api.ingestion")


async def run_pipeline(context: WorkerContext, prayer_id: str) -> None:
    claimed = await claim_prayer(context, prayer_id)
    if claimed is None:
        logger.info("prayer_skipped id=%s reason=not_claimable", prayer_id)
        return

    original_text = claimed.get("text_original") or claimed.get("text") or ""

    compliance = await review_compliance(context, original_text)
    if not compliance.compliant:
        await finalize_rejected(context, prayer_id, compliance.violation_type, compliance.reason)
        logger.info("prayer_rejected id=%s violation=%s", prayer_id, compliance.violation_type)
        return

    spelling = await correct_spelling(context, original_text)
    corrected = spelling.corrected_text.strip() or original_text

    duplicate = await find_duplicate(context, corrected)
    if duplicate.duplicate_of_id is not None:
        await finalize_duplicate(context, prayer_id, duplicate)
        logger.info("prayer_duplicate id=%s of=%s", prayer_id, duplicate.duplicate_of_id)
        return

    diacritization = await diacritize(context, corrected)
    category = await categorize(context, corrected)

    await finalize_confirmed(
        context,
        prayer_id,
        text=corrected,
        diacritized=diacritization.diacritized_text,
        confidence=diacritization.confidence,
        outcome=duplicate,
        category_id=category.category_id,
        type_id=category.type_id,
    )
    logger.info("prayer_confirmed id=%s", prayer_id)
