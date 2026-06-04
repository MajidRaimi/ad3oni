from typing import Any

from src.features.ingestion.prompts import DEDUP_SYSTEM, dedup_user
from src.features.ingestion.schema import Candidate, DedupJudgeResult, DuplicateOutcome
from src.shared.ai.structured import complete_json
from src.shared.arabic.hashing import text_hash
from src.shared.arabic.normalize import normalize_arabic
from src.shared.pocketbase.filters import combine, quote
from src.shared.queue.context import WorkerContext

_MIN_KEYWORD_LENGTH = 3
_MAX_KEYWORDS = 3
_MAX_CANDIDATES = 8


def _keywords(normalized: str) -> list[str]:
    words = [word for word in normalized.split(" ") if len(word) >= _MIN_KEYWORD_LENGTH]
    return sorted(set(words), key=len, reverse=True)[:_MAX_KEYWORDS]


async def _find_exact(context: WorkerContext, digest: str) -> dict[str, Any] | None:
    return await context.pocketbase.get_first(
        "prayers",
        combine(f"text_hash = {quote(digest)}", 'status = "confirmed"'),
    )


async def _fetch_candidates(context: WorkerContext, normalized: str) -> list[Candidate]:
    keywords = _keywords(normalized)
    if not keywords:
        return []
    clause = " || ".join(f"normalized ~ {quote(word)}" for word in keywords)
    filter_ = combine('status = "confirmed"', f"({clause})")
    data = await context.pocketbase.list_records(
        "prayers",
        {
            "filter": filter_,
            "perPage": _MAX_CANDIDATES,
            "sort": "-created",
            "skipTotal": True,
        },
    )
    return [Candidate(id=item["id"], text=item.get("text", "")) for item in data.get("items", [])]


async def find_duplicate(context: WorkerContext, corrected_text: str) -> DuplicateOutcome:
    normalized = normalize_arabic(corrected_text)
    digest = text_hash(normalized)

    exact = await _find_exact(context, digest)
    if exact is not None:
        return DuplicateOutcome(normalized, digest, exact["id"])

    candidates = await _fetch_candidates(context, normalized)
    if not candidates:
        return DuplicateOutcome(normalized, digest, None)

    result = await complete_json(
        context.ai,
        context.settings.ai_model,
        DEDUP_SYSTEM,
        dedup_user(corrected_text, [candidate.text for candidate in candidates]),
        DedupJudgeResult,
        reasoning_effort=context.settings.dedup_effort,
    )

    index = result.duplicate_index
    if result.is_duplicate and index is not None and 0 <= index < len(candidates):
        return DuplicateOutcome(normalized, digest, candidates[index].id)
    return DuplicateOutcome(normalized, digest, None)
