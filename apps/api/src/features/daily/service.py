from typing import Any

from arq import ArqRedis

from src.features.daily.selection import (
    assign_daily_prayer,
    current_daily_prayer_id,
)
from src.features.prayers.mappers import to_prayer
from src.features.prayers.schema import Prayer
from src.shared.errors.exceptions import NotFoundError
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.pocketbase.filters import combine, quote

_CONFIRMED = 'status = "confirmed"'
_PRAYER_EXPAND = "category.group,type"


class DailyService:
    def __init__(self, pocketbase: PocketBaseClient, redis: ArqRedis) -> None:
        self._pocketbase = pocketbase
        self._redis = redis

    async def get_daily(self) -> Prayer:
        prayer_id = await current_daily_prayer_id(self._redis)
        if prayer_id is None:
            prayer_id = await assign_daily_prayer(self._pocketbase, self._redis)

        record = await self._fetch(prayer_id)
        if record is None:
            prayer_id = await assign_daily_prayer(self._pocketbase, self._redis)
            record = await self._fetch(prayer_id)

        if record is None:
            raise NotFoundError("No prayers available")
        return to_prayer(record)

    async def _fetch(self, prayer_id: str | None) -> dict[str, Any] | None:
        if prayer_id is None:
            return None
        return await self._pocketbase.get_first(
            "prayers",
            combine(_CONFIRMED, f"id = {quote(prayer_id)}"),
            expand=_PRAYER_EXPAND,
        )
