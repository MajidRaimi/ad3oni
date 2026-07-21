from collections.abc import Awaitable
from datetime import datetime
from typing import cast
from zoneinfo import ZoneInfo

from arq import ArqRedis

from src.features.daily.keys import MECCA_TIMEZONE
from src.features.discord.embeds import info_embed
from src.features.discord.rest import DiscordRest
from src.features.prayers.schema import Prayer
from src.features.prayers.service import PrayerService
from src.features.x.keys import (
    MAX_POST_LENGTH,
    PICK_TRIES,
    posted_prayers_key,
)
from src.features.x.poster import (
    PostVerificationError,
    SessionExpiredError,
    WrongAccountError,
    publish,
)
from src.features.x.session import load_session, save_session
from src.shared.errors.exceptions import NotFoundError
from src.shared.logging.setup import get_logger
from src.shared.queue.context import WorkerContext

logger = get_logger("api.x.service")


def compose_post(prayer: Prayer) -> str | None:
    text = prayer.text.strip()
    if len(text) > MAX_POST_LENGTH:
        return None
    if prayer.source:
        with_source = f"{text}\n\n{prayer.source.strip()}"
        if len(with_source) <= MAX_POST_LENGTH:
            return with_source
    return text


def today() -> str:
    return datetime.now(ZoneInfo(MECCA_TIMEZONE)).date().isoformat()


async def alert(context: WorkerContext, message: str) -> None:
    channel = context.settings.discord_alert_channel_id
    token = context.settings.discord_bot_token
    if not channel or not token:
        return
    rest = DiscordRest(context.http, token)
    await rest.post_message(channel, info_embed(f"‏X: {message}"))


async def _posted_today(redis: ArqRedis, day: str) -> set[str]:
    members = await cast(
        "Awaitable[set[bytes]]", redis.smembers(posted_prayers_key(day))
    )
    return {m.decode() if isinstance(m, bytes) else str(m) for m in members}


async def pick_postable_prayer(
    context: WorkerContext, redis: ArqRedis, day: str
) -> tuple[Prayer, str] | None:
    already = await _posted_today(redis, day)
    service = PrayerService(context.pocketbase, redis)
    for _ in range(PICK_TRIES):
        try:
            prayer = await service.random_prayer()
        except NotFoundError:
            return None
        if prayer.id in already:
            continue
        text = compose_post(prayer)
        if text is None:
            continue
        return prayer, text
    return None


async def publish_prayer(
    context: WorkerContext, redis: ArqRedis, prayer: Prayer, text: str
) -> bool:
    """Return True if the post was committed to X (mark the slot), False to retry."""
    settings = context.settings

    if settings.x_dry_run:
        logger.info("x_dry_run prayer=%s text=%r", prayer.id, text)
        return True

    cookies = await load_session(redis, settings.x_session_state)
    if cookies is None:
        logger.error("x_no_session")
        await alert(context, "لا توجد جلسة محفوظة. شغّل scripts/build_x_session.py")
        return False

    try:
        result = await publish(
            text,
            cookies=cookies,
            handle=settings.x_handle,
            headless=settings.x_headless,
            channel=settings.x_channel,
            timeout_ms=settings.x_nav_timeout_ms,
        )
    except SessionExpiredError as error:
        logger.error("x_session_expired")
        await alert(context, f"انتهت صلاحية الجلسة: {error}")
        return False
    except WrongAccountError as error:
        logger.error("x_wrong_account %s", error)
        await alert(context, f"الجلسة لحساب خاطئ: {error}")
        return False
    except PostVerificationError:
        logger.info("x_submit_rejected prayer=%s", prayer.id)
        return False
    except Exception as error:
        logger.exception("x_post_failed")
        await alert(context, f"فشل النشر: {type(error).__name__}: {error}")
        return False

    await save_session(redis, result.cookies)
    if not result.verified:
        logger.warning("x_post_unverified prayer=%s", prayer.id)
        await alert(context, "أُرسل المنشور لكن تعذّر التأكد من ظهوره. راجع الحساب.")
    return True


async def post_one_now(context: WorkerContext, redis: ArqRedis) -> bool:
    """Post a single random prayer immediately, ignoring the schedule. For
    manual testing via scripts/post_daily_to_x.py."""
    if not context.settings.x_enabled:
        logger.info("x_disabled skipping")
        return False
    day = today()
    picked = await pick_postable_prayer(context, redis, day)
    if picked is None:
        logger.warning("x_no_postable_prayer")
        return False
    prayer, text = picked
    committed = await publish_prayer(context, redis, prayer, text)
    if committed:
        await cast(
            "Awaitable[int]", redis.sadd(posted_prayers_key(day), prayer.id)
        )
        logger.info("x_posted_manual prayer=%s", prayer.id)
    return committed
