from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from arq import ArqRedis
from croniter import croniter

from src.features.daily.service import DailyService
from src.features.discord.embeds import prayer_embed
from src.features.discord.rest import DiscordRest
from src.features.discord.schema import Schedule
from src.features.discord.service import DiscordScheduleService
from src.features.prayers.schema import Prayer
from src.features.prayers.service import PrayerService
from src.shared.errors.exceptions import NotFoundError
from src.shared.logging.setup import get_logger
from src.shared.queue.context import WorkerContext

logger = get_logger("api.discord.scheduler")


def _minute_now(timezone: str) -> datetime | None:
    try:
        zone = ZoneInfo(timezone)
    except (ZoneInfoNotFoundError, ValueError):
        return None
    return datetime.now(zone).replace(second=0, microsecond=0)


def _is_due(schedule: Schedule, now: datetime) -> bool:
    if not croniter.is_valid(schedule.cron):
        return False
    if not croniter.match(schedule.cron, now):
        return False
    return schedule.last_run_at != now.isoformat()


async def _resolve_prayer(
    schedule: Schedule, daily: DailyService, prayers: PrayerService
) -> Prayer | None:
    try:
        if schedule.content_type == "daily":
            return await daily.get_daily()
        if schedule.content_type == "category" and schedule.category:
            return await prayers.random_prayer(category=schedule.category)
        return await prayers.random_prayer()
    except NotFoundError:
        return None


async def run_due_schedules(context: WorkerContext, redis: ArqRedis) -> None:
    if not context.settings.discord_bot_token:
        return

    service = DiscordScheduleService(context.pocketbase)
    schedules = await service.list_enabled()
    if not schedules:
        return

    daily = DailyService(context.pocketbase, redis)
    prayers = PrayerService(context.pocketbase, redis)
    rest = DiscordRest(context.http, context.settings.discord_bot_token)

    for schedule in schedules:
        now = _minute_now(schedule.timezone)
        if now is None or not _is_due(schedule, now):
            continue

        prayer = await _resolve_prayer(schedule, daily, prayers)
        if prayer is None:
            continue

        response = await rest.post_message(
            schedule.channel_id, prayer_embed(prayer)
        )
        if response.status_code in (403, 404):
            await service.disable(schedule.id)
            logger.warning(
                "discord_schedule_disabled id=%s status=%s",
                schedule.id,
                response.status_code,
            )
            continue
        if response.status_code >= 400:
            logger.warning(
                "discord_schedule_post_failed id=%s status=%s",
                schedule.id,
                response.status_code,
            )
            continue

        await service.mark_run(schedule.id, now.isoformat())
