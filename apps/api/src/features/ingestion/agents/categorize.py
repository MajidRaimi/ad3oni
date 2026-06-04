from src.features.ingestion.prompts import CATEGORIZATION_SYSTEM, categorization_user
from src.features.ingestion.schema import CategorizationOutcome, CategorizationResult
from src.features.ingestion.taxonomy_resolver import (
    resolve_or_create_category,
    resolve_or_create_group,
    resolve_or_create_type,
)
from src.shared.ai.structured import complete_json
from src.shared.queue.context import WorkerContext

_TAXONOMY_PAGE_SIZE = 200
_FALLBACK_GROUP = "أدعية عامة"
_FALLBACK_CATEGORY = "أدعية متنوعة"
_FALLBACK_TYPE = "مخصص"


async def _names(context: WorkerContext, collection: str) -> list[str]:
    data = await context.pocketbase.list_records(
        collection, {"sort": "name", "perPage": _TAXONOMY_PAGE_SIZE}
    )
    return [item["name"] for item in data.get("items", [])]


async def categorize(context: WorkerContext, text: str) -> CategorizationOutcome:
    groups = await _names(context, "groups")
    categories = await _names(context, "categories")
    types = await _names(context, "types")

    result = await complete_json(
        context.ai,
        context.settings.ai_model,
        CATEGORIZATION_SYSTEM,
        categorization_user(text, groups, categories, types),
        CategorizationResult,
        reasoning_effort=context.settings.categorization_effort,
    )

    group_name = result.group_name.strip() or _FALLBACK_GROUP
    category_name = result.category_name.strip() or _FALLBACK_CATEGORY
    type_name = result.type_name.strip() or _FALLBACK_TYPE

    group = await resolve_or_create_group(context, group_name)
    category = await resolve_or_create_category(context, category_name, group["id"])
    prayer_type = await resolve_or_create_type(context, type_name)
    return CategorizationOutcome(category_id=category["id"], type_id=prayer_type["id"])
