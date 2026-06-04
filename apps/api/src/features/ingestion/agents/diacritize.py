from src.features.ingestion.prompts import (
    DIACRITIZATION_VERIFY_SYSTEM,
    diacritization_system,
    diacritization_user,
    diacritization_verify_user,
)
from src.features.ingestion.schema import DiacritizationResult
from src.shared.ai.structured import complete_json
from src.shared.arabic.normalize import harakat_preserves_wording
from src.shared.logging.setup import get_logger
from src.shared.queue.context import WorkerContext

logger = get_logger("api.ingestion")


async def _add_harakat(context: WorkerContext, corrected: str) -> str:
    result = await complete_json(
        context.ai,
        context.settings.ai_model,
        diacritization_system(context.settings.diacritization_mode),
        diacritization_user(corrected),
        DiacritizationResult,
        reasoning_effort=context.settings.diacritization_effort,
    )
    return result.diacritized_text.strip()


async def _verify_harakat(
    context: WorkerContext, corrected: str, diacritized: str
) -> str:
    result = await complete_json(
        context.ai,
        context.settings.ai_model,
        DIACRITIZATION_VERIFY_SYSTEM,
        diacritization_verify_user(corrected, diacritized),
        DiacritizationResult,
        reasoning_effort=context.settings.diacritization_effort,
    )
    candidate = result.diacritized_text.strip()
    if candidate and harakat_preserves_wording(corrected, candidate):
        return candidate
    return diacritized


async def diacritize(context: WorkerContext, corrected: str) -> str:
    for _ in range(context.settings.diacritization_max_attempts):
        candidate = await _add_harakat(context, corrected)
        if candidate and harakat_preserves_wording(corrected, candidate):
            if context.settings.diacritization_verify_enabled:
                return await _verify_harakat(context, corrected, candidate)
            return candidate
    logger.info("diacritization_fallback_plain")
    return corrected
