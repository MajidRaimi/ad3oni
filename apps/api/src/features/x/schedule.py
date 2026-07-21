import json
import random
from collections.abc import Awaitable
from datetime import datetime
from typing import cast
from zoneinfo import ZoneInfo

from arq import ArqRedis

from src.features.daily.keys import MECCA_TIMEZONE
from src.features.x.keys import (
    GRACE_MINUTES,
    POST_WINDOWS,
    SLOT_TTL_SECONDS,
    X_LAST_POST,
    plan_key,
    posted_prayers_key,
    slot_posted_key,
)
from src.features.x.service import pick_postable_prayer, publish_prayer
from src.shared.logging.setup import get_logger
from src.shared.queue.context import WorkerContext

logger = get_logger("api.x.schedule")


def _decode(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode()
    return str(value)


def make_plan() -> list[str]:
    times: list[str] = []
    for start, end in POST_WINDOWS:
        minute = random.randint(0, (end - start) * 60 - 1)
        total = start * 60 + minute
        times.append(f"{total // 60:02d}:{total % 60:02d}")
    return times


def is_due(now_minutes: int, target: str) -> bool:
    target_minutes = int(target[:2]) * 60 + int(target[3:])
    return target_minutes <= now_minutes <= target_minutes + GRACE_MINUTES


async def _plan_for(redis: ArqRedis, day: str) -> list[str]:
    stored = _decode(await redis.get(plan_key(day)))
    if stored:
        loaded: list[str] = json.loads(stored)
        return loaded
    plan = make_plan()
    await redis.set(plan_key(day), json.dumps(plan), ex=SLOT_TTL_SECONDS)
    logger.info("x_plan_created day=%s times=%s", day, plan)
    return plan


async def dispatch_posts(context: WorkerContext, redis: ArqRedis) -> None:
    if not context.settings.x_enabled:
        return

    now = datetime.now(ZoneInfo(MECCA_TIMEZONE))
    day = now.date().isoformat()
    plan = await _plan_for(redis, day)
    now_minutes = now.hour * 60 + now.minute

    for slot, target in enumerate(plan):
        if not is_due(now_minutes, target):
            continue
        if await redis.get(slot_posted_key(day, slot)) is not None:
            continue

        picked = await pick_postable_prayer(context, redis, day)
        if picked is None:
            logger.warning("x_no_postable_prayer day=%s slot=%s", day, slot)
            continue

        prayer, text = picked
        if not await publish_prayer(context, redis, prayer, text):
            continue

        await redis.set(slot_posted_key(day, slot), prayer.id, ex=SLOT_TTL_SECONDS)
        await cast(
            "Awaitable[int]", redis.sadd(posted_prayers_key(day), prayer.id)
        )
        await cast(
            "Awaitable[bool]",
            redis.expire(posted_prayers_key(day), SLOT_TTL_SECONDS),
        )
        await redis.set(X_LAST_POST, f"{day}:{slot}:{prayer.id}")
        logger.info(
            "x_posted day=%s slot=%s time=%s prayer=%s", day, slot, target, prayer.id
        )
