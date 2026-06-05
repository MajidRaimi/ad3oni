import random
from collections import Counter
from collections.abc import Awaitable
from datetime import datetime
from typing import Any, cast
from zoneinfo import ZoneInfo

from arq import ArqRedis

from src.features.daily.keys import (
    DAILY_CURRENT,
    DAILY_DATE,
    DAILY_HISTORY,
    MECCA_TIMEZONE,
)
from src.shared.pocketbase.client import PocketBaseClient

_PAGE_SIZE = 500


def _decode(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode()
    return str(value)


async def _collect_records(
    pocketbase: PocketBaseClient, filter_: str
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    page = 1
    while True:
        data = await pocketbase.list_records(
            "prayers",
            {
                "filter": filter_,
                "page": page,
                "perPage": _PAGE_SIZE,
                "skipTotal": True,
                "fields": "id,duplicate_of",
            },
        )
        items = data.get("items", [])
        records.extend(items)
        if len(items) < _PAGE_SIZE:
            return records
        page += 1


async def _duplicate_counts(pocketbase: PocketBaseClient) -> Counter[str]:
    duplicates = await _collect_records(pocketbase, 'status = "duplicate"')
    return Counter(
        record["duplicate_of"]
        for record in duplicates
        if record.get("duplicate_of")
    )


async def _history(redis: ArqRedis) -> set[str]:
    members = await cast("Awaitable[set[bytes]]", redis.smembers(DAILY_HISTORY))
    return {decoded for member in members if (decoded := _decode(member))}


def _pick_from_tier(eligible: list[str], counts: Counter[str]) -> str:
    peak = max(counts.get(prayer_id, 0) for prayer_id in eligible)
    tier = [prayer_id for prayer_id in eligible if counts.get(prayer_id, 0) == peak]
    return random.choice(tier)


async def select_daily_prayer_id(
    pocketbase: PocketBaseClient, redis: ArqRedis
) -> str | None:
    confirmed = [
        record["id"]
        for record in await _collect_records(pocketbase, 'status = "confirmed"')
    ]
    if not confirmed:
        return None

    counts = await _duplicate_counts(pocketbase)
    history = await _history(redis)

    eligible = [prayer_id for prayer_id in confirmed if prayer_id not in history]
    if not eligible:
        await cast("Awaitable[int]", redis.delete(DAILY_HISTORY))
        current = _decode(await redis.get(DAILY_CURRENT))
        eligible = [prayer_id for prayer_id in confirmed if prayer_id != current]
        if not eligible:
            eligible = confirmed

    return _pick_from_tier(eligible, counts)


async def assign_daily_prayer(
    pocketbase: PocketBaseClient, redis: ArqRedis
) -> str | None:
    prayer_id = await select_daily_prayer_id(pocketbase, redis)
    if prayer_id is None:
        return None

    today = datetime.now(ZoneInfo(MECCA_TIMEZONE)).date().isoformat()
    await redis.set(DAILY_CURRENT, prayer_id)
    await cast("Awaitable[int]", redis.sadd(DAILY_HISTORY, prayer_id))
    await redis.set(DAILY_DATE, today)
    return prayer_id


async def current_daily_prayer_id(redis: ArqRedis) -> str | None:
    return _decode(await redis.get(DAILY_CURRENT))
