from typing import Any

from src.features.discord.schema import Schedule, to_schedule
from src.shared.errors.exceptions import ValidationError
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.pocketbase.filters import combine, quote

_COLLECTION = "schedules"
_PAGE_SIZE = 200


class DiscordScheduleService:
    def __init__(self, pocketbase: PocketBaseClient, limit: int = 15) -> None:
        self._pocketbase = pocketbase
        self._limit = limit

    async def list_for_guild(self, guild_id: str) -> list[Schedule]:
        data = await self._pocketbase.list_records(
            _COLLECTION,
            {
                "filter": f"guild_id = {quote(guild_id)}",
                "sort": "created",
                "perPage": _PAGE_SIZE,
            },
        )
        return [to_schedule(record) for record in data.get("items", [])]

    async def list_enabled(self) -> list[Schedule]:
        schedules: list[Schedule] = []
        page = 1
        while True:
            data = await self._pocketbase.list_records(
                _COLLECTION,
                {"filter": "enabled = true", "page": page, "perPage": _PAGE_SIZE},
            )
            items = data.get("items", [])
            schedules.extend(to_schedule(record) for record in items)
            if len(items) < _PAGE_SIZE:
                return schedules
            page += 1

    async def create(
        self,
        *,
        guild_id: str,
        channel_id: str,
        cron: str,
        timezone: str,
        content_type: str,
        category: str | None,
        label: str | None,
        created_by: str,
    ) -> Schedule:
        existing = await self.list_for_guild(guild_id)
        if len(existing) >= self._limit:
            raise ValidationError(
                f"This server already has the maximum of {self._limit} schedules."
            )
        payload: dict[str, Any] = {
            "guild_id": guild_id,
            "channel_id": channel_id,
            "cron": cron,
            "timezone": timezone,
            "content_type": content_type,
            "category": category or "",
            "label": label or "",
            "enabled": True,
            "created_by": created_by,
        }
        record = await self._pocketbase.create_record(_COLLECTION, payload)
        return to_schedule(record)

    async def remove(self, guild_id: str, schedule_id: str) -> bool:
        record = await self._pocketbase.get_first(
            _COLLECTION,
            combine(f"id = {quote(schedule_id)}", f"guild_id = {quote(guild_id)}"),
        )
        if record is None:
            return False
        await self._pocketbase.delete_record(_COLLECTION, schedule_id)
        return True

    async def mark_run(self, schedule_id: str, stamp: str) -> None:
        await self._pocketbase.update_record(
            _COLLECTION, schedule_id, {"last_run_at": stamp}
        )

    async def disable(self, schedule_id: str) -> None:
        await self._pocketbase.update_record(
            _COLLECTION, schedule_id, {"enabled": False}
        )
