from src.features.ingestion.prompts import DIACRITIZATION_SYSTEM, diacritization_user
from src.features.ingestion.schema import DiacritizationResult
from src.shared.ai.structured import complete_json
from src.shared.queue.context import WorkerContext


async def diacritize(context: WorkerContext, text: str) -> DiacritizationResult:
    return await complete_json(
        context.ai,
        context.settings.ai_model,
        DIACRITIZATION_SYSTEM,
        diacritization_user(text),
        DiacritizationResult,
        reasoning_effort=context.settings.diacritization_effort,
    )
