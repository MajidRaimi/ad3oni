from src.features.taxonomy.mappers import to_category, to_group, to_prayer_type
from src.features.taxonomy.schema import Category, Group, PrayerType
from src.shared.errors.exceptions import NotFoundError
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.pocketbase.filters import quote

_TAXONOMY_PAGE_SIZE = 200


class TaxonomyService:
    def __init__(self, pocketbase: PocketBaseClient) -> None:
        self._pocketbase = pocketbase

    async def list_groups(self) -> list[Group]:
        data = await self._pocketbase.list_records(
            "groups", {"sort": "name", "perPage": _TAXONOMY_PAGE_SIZE}
        )
        return [to_group(record) for record in data.get("items", [])]

    async def get_group(self, slug: str) -> Group:
        record = await self._pocketbase.get_first("groups", f"slug = {quote(slug)}")
        if record is None:
            raise NotFoundError(f"Group '{slug}' not found")
        return to_group(record)

    async def list_categories(self, group: str | None = None) -> list[Category]:
        filter_ = f"group.slug = {quote(group)}" if group else ""
        params = {
            "sort": "name",
            "perPage": _TAXONOMY_PAGE_SIZE,
            "expand": "group",
        }
        if filter_:
            params["filter"] = filter_
        data = await self._pocketbase.list_records("categories", params)
        return [to_category(record) for record in data.get("items", [])]

    async def get_category(self, slug: str) -> Category:
        record = await self._pocketbase.get_first(
            "categories", f"slug = {quote(slug)}", expand="group"
        )
        if record is None:
            raise NotFoundError(f"Category '{slug}' not found")
        return to_category(record)

    async def list_types(self) -> list[PrayerType]:
        data = await self._pocketbase.list_records(
            "types", {"sort": "name", "perPage": _TAXONOMY_PAGE_SIZE}
        )
        return [to_prayer_type(record) for record in data.get("items", [])]
