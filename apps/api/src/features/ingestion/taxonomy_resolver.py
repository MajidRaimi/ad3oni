from typing import Any

from src.shared.arabic.normalize import normalize_arabic
from src.shared.arabic.slugify import slugify_arabic
from src.shared.pocketbase.filters import quote
from src.shared.queue.context import WorkerContext


async def _find_existing(
    context: WorkerContext, collection: str, slug: str, name_normalized: str
) -> dict[str, Any] | None:
    by_slug = await context.pocketbase.get_first(collection, f"slug = {quote(slug)}")
    if by_slug is not None:
        return by_slug
    if not name_normalized:
        return None
    return await context.pocketbase.get_first(
        collection, f"name_normalized = {quote(name_normalized)}"
    )


async def resolve_or_create_group(context: WorkerContext, name: str) -> dict[str, Any]:
    slug = slugify_arabic(name)
    name_normalized = normalize_arabic(name)
    existing = await _find_existing(context, "groups", slug, name_normalized)
    if existing is not None:
        return existing
    return await context.pocketbase.create_record(
        "groups",
        {"name": name, "slug": slug, "name_normalized": name_normalized},
    )


async def resolve_or_create_category(
    context: WorkerContext, name: str, group_id: str
) -> dict[str, Any]:
    slug = slugify_arabic(name)
    name_normalized = normalize_arabic(name)
    existing = await _find_existing(context, "categories", slug, name_normalized)
    if existing is not None:
        return existing
    return await context.pocketbase.create_record(
        "categories",
        {
            "name": name,
            "slug": slug,
            "name_normalized": name_normalized,
            "group": group_id,
        },
    )


async def resolve_or_create_type(context: WorkerContext, name: str) -> dict[str, Any]:
    slug = slugify_arabic(name)
    name_normalized = normalize_arabic(name)
    existing = await _find_existing(context, "types", slug, name_normalized)
    if existing is not None:
        return existing
    return await context.pocketbase.create_record(
        "types",
        {"name": name, "slug": slug, "name_normalized": name_normalized},
    )
