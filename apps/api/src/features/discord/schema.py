from typing import Any

from pydantic import BaseModel


class Schedule(BaseModel):
    id: str
    guild_id: str
    channel_id: str
    cron: str
    timezone: str
    content_type: str
    category: str | None = None
    label: str | None = None
    enabled: bool = True
    last_run_at: str | None = None


def to_schedule(record: dict[str, Any]) -> Schedule:
    return Schedule(
        id=record["id"],
        guild_id=record.get("guild_id", ""),
        channel_id=record.get("channel_id", ""),
        cron=record.get("cron", ""),
        timezone=record.get("timezone") or "Asia/Riyadh",
        content_type=record.get("content_type", "random"),
        category=record.get("category") or None,
        label=record.get("label") or None,
        enabled=bool(record.get("enabled", False)),
        last_run_at=record.get("last_run_at") or None,
    )
