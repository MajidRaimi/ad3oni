from src.features.ingestion.prompts import SPELLING_SYSTEM, spelling_user
from src.features.ingestion.schema import SpellingResult
from src.shared.ai.structured import complete_json
from src.shared.queue.context import WorkerContext


async def correct_spelling(context: WorkerContext, text: str) -> SpellingResult:
    return await complete_json(
        context.ai,
        context.settings.ai_model,
        SPELLING_SYSTEM,
        spelling_user(text),
        SpellingResult,
        reasoning_effort=context.settings.spelling_effort,
    )
