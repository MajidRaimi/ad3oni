from typing import Any

from arq import ArqRedis

from src.features.prayers.mappers import to_prayer
from src.features.prayers.schema import (
    Prayer,
    PrayerSort,
    PrayerSubmission,
    SubmittedPrayer,
)
from src.shared.errors.exceptions import NotFoundError, ValidationError
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.pocketbase.filters import combine, quote
from src.shared.queue.pool import enqueue_process_prayer
from src.shared.schema.pagination import Page, to_page

_CONFIRMED = 'status = "confirmed"'
_PRAYER_EXPAND = "category.group,type"


class PrayerService:
    def __init__(self, pocketbase: PocketBaseClient, queue: ArqRedis) -> None:
        self._pocketbase = pocketbase
        self._queue = queue

    async def list_prayers(
        self,
        *,
        category: str | None = None,
        type_: str | None = None,
        group: str | None = None,
        q: str | None = None,
        page: int = 1,
        per_page: int = 20,
        sort: PrayerSort = "-created",
    ) -> Page[Prayer]:
        filter_ = combine(
            _CONFIRMED,
            f"category.slug = {quote(category)}" if category else None,
            f"type.slug = {quote(type_)}" if type_ else None,
            f"category.group.slug = {quote(group)}" if group else None,
            f"text ~ {quote(q)}" if q else None,
        )
        data = await self._pocketbase.list_records(
            "prayers",
            {
                "filter": filter_,
                "expand": _PRAYER_EXPAND,
                "page": page,
                "perPage": per_page,
                "sort": sort,
            },
        )
        items = [to_prayer(record) for record in data.get("items", [])]
        return to_page(data, items)

    async def get_prayer(self, prayer_id: str) -> Prayer:
        record = await self._pocketbase.get_first(
            "prayers",
            combine(_CONFIRMED, f"id = {quote(prayer_id)}"),
            expand=_PRAYER_EXPAND,
        )
        if record is None:
            raise NotFoundError(f"Prayer '{prayer_id}' not found")
        return to_prayer(record)

    async def random_prayer(
        self, *, category: str | None = None, type_: str | None = None
    ) -> Prayer:
        filter_ = combine(
            _CONFIRMED,
            f"category.slug = {quote(category)}" if category else None,
            f"type.slug = {quote(type_)}" if type_ else None,
        )
        data = await self._pocketbase.list_records(
            "prayers",
            {
                "filter": filter_,
                "expand": _PRAYER_EXPAND,
                "perPage": 1,
                "sort": "@random",
                "skipTotal": True,
            },
        )
        items = data.get("items", [])
        if not items:
            raise NotFoundError("No prayers available")
        return to_prayer(items[0])

    async def submit_prayer(self, submission: PrayerSubmission) -> SubmittedPrayer:
        payload: dict[str, Any] = {
            "text": submission.text,
            "status": "pending",
        }

        if submission.category is not None:
            category = await self._resolve_slug("categories", submission.category)
            if category is None:
                raise ValidationError(f"Unknown category '{submission.category}'")
            payload["category"] = category["id"]

        if submission.type is not None:
            prayer_type = await self._resolve_slug("types", submission.type)
            if prayer_type is None:
                raise ValidationError(f"Unknown type '{submission.type}'")
            payload["type"] = prayer_type["id"]

        created = await self._pocketbase.create_record("prayers", payload)
        await enqueue_process_prayer(self._queue, created["id"])
        return SubmittedPrayer(
            id=created["id"],
            status=created["status"],
            created=created["created"],
        )

    async def _resolve_slug(
        self, collection: str, slug: str
    ) -> dict[str, Any] | None:
        return await self._pocketbase.get_first(collection, f"slug = {quote(slug)}")
