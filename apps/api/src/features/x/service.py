from datetime import datetime
from zoneinfo import ZoneInfo

from arq import ArqRedis

from src.features.daily.keys import MECCA_TIMEZONE
from src.features.daily.service import DailyService
from src.features.discord.embeds import info_embed
from src.features.discord.rest import DiscordRest
from src.features.prayers.schema import Prayer
from src.features.x.keys import MAX_POST_LENGTH, X_LAST_POST, posted_key
from src.features.x.poster import SessionExpiredError, WrongAccountError, publish
from src.features.x.session import load_session, save_session
from src.shared.errors.exceptions import NotFoundError
from src.shared.logging.setup import get_logger
from src.shared.queue.context import WorkerContext

logger = get_logger("api.x.service")

_POSTED_TTL_SECONDS = 60 * 60 * 48


def compose_post(prayer: Prayer) -> str | None:
    text = prayer.text.strip()
    if len(text) > MAX_POST_LENGTH:
        return None
    if prayer.source:
        with_source = f"{text}\n\n{prayer.source.strip()}"
        if len(with_source) <= MAX_POST_LENGTH:
            return with_source
    return text


def _today() -> str:
    return datetime.now(ZoneInfo(MECCA_TIMEZONE)).date().isoformat()


async def _alert(context: WorkerContext, message: str) -> None:
    channel = context.settings.discord_alert_channel_id
    token = context.settings.discord_bot_token
    if not channel or not token:
        return
    rest = DiscordRest(context.http, token)
    await rest.post_message(channel, info_embed(f"‏X: {message}"))


async def post_daily_to_x(context: WorkerContext, redis: ArqRedis) -> bool:
    settings = context.settings
    if not settings.x_enabled:
        logger.info("x_disabled skipping")
        return False

    day = _today()
    if await redis.get(posted_key(day)) is not None:
        logger.info("x_already_posted day=%s", day)
        return False

    try:
        prayer = await DailyService(context.pocketbase, redis).get_daily()
    except NotFoundError:
        logger.warning("x_no_prayer_available")
        return False

    text = compose_post(prayer)
    if text is None:
        logger.warning("x_prayer_too_long id=%s len=%d", prayer.id, len(prayer.text))
        await _alert(
            context,
            f"دعاء اليوم أطول من {MAX_POST_LENGTH} حرفًا، فلم يُنشر. المعرّف: {prayer.id}",
        )
        return False

    if settings.x_dry_run:
        logger.info("x_dry_run text=%r", text)
        return False

    cookies = await load_session(redis, settings.x_session_state)
    if cookies is None:
        logger.error("x_no_session")
        await _alert(context, "لا توجد جلسة محفوظة. شغّل scripts/build_x_session.py")
        return False

    try:
        result = await publish(text, cookies=cookies, handle=settings.x_handle)
    except SessionExpiredError as error:
        logger.error("x_session_expired")
        await _alert(context, f"انتهت صلاحية الجلسة: {error}")
        return False
    except WrongAccountError as error:
        logger.error("x_wrong_account %s", error)
        await _alert(context, f"الجلسة لحساب خاطئ: {error}")
        return False
    except Exception as error:
        logger.exception("x_post_failed")
        await _alert(context, f"فشل النشر: {type(error).__name__}: {error}")
        return False

    await save_session(redis, result.cookies)

    if not result.verified:
        logger.error("x_post_unverified id=%s", prayer.id)
        await _alert(context, "أُرسل المنشور لكن تعذّر التأكد من ظهوره. راجع الحساب.")
        return False

    await redis.set(posted_key(day), prayer.id, ex=_POSTED_TTL_SECONDS)
    await redis.set(X_LAST_POST, f"{day}:{prayer.id}")
    logger.info("x_posted day=%s prayer=%s", day, prayer.id)
    return True
