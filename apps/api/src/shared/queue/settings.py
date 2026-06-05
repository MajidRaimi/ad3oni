from typing import Any
from zoneinfo import ZoneInfo

import httpx
from arq import ArqRedis, cron

from src.features.daily.keys import MECCA_TIMEZONE
from src.features.daily.selection import assign_daily_prayer
from src.features.discord.scheduler import run_due_schedules
from src.features.ingestion.finalize import finalize_failed
from src.features.ingestion.pipeline import run_pipeline
from src.shared.ai.client import create_ai_client
from src.shared.config.settings import get_settings
from src.shared.logging.setup import configure_logging, get_logger
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.queue.context import (
    WorkerContext,
    get_worker_context,
    set_worker_context,
)
from src.shared.queue.pool import redis_settings_from

logger = get_logger("api.worker")
_settings = get_settings()


async def startup(ctx: dict[Any, Any]) -> None:
    configure_logging(_settings.log_level)
    settings = get_settings()
    http = httpx.AsyncClient(timeout=30.0)
    pocketbase = PocketBaseClient(
        settings.pocketbase_url,
        http,
        settings.pocketbase_admin_email,
        settings.pocketbase_admin_password,
    )
    await pocketbase.authenticate()
    ai = create_ai_client(settings)
    set_worker_context(ctx, WorkerContext(settings, pocketbase, ai, http))
    logger.info("worker_startup_complete environment=%s", settings.environment)


async def shutdown(ctx: dict[Any, Any]) -> None:
    context = get_worker_context(ctx)
    await context.http.aclose()
    logger.info("worker_shutdown_complete")


async def process_prayer(ctx: dict[Any, Any], prayer_id: str) -> None:
    context = get_worker_context(ctx)
    try:
        await run_pipeline(context, prayer_id)
    except Exception:
        job_try = int(ctx.get("job_try", 1))
        if job_try >= _settings.job_max_tries:
            await finalize_failed(context, prayer_id)
            logger.exception("prayer_pipeline_failed id=%s", prayer_id)
            return
        raise


async def assign_daily(ctx: dict[Any, Any]) -> None:
    context = get_worker_context(ctx)
    redis: ArqRedis = ctx["redis"]
    try:
        prayer_id = await assign_daily_prayer(context.pocketbase, redis)
        logger.info("daily_prayer_assigned id=%s", prayer_id)
    except Exception:
        logger.exception("daily_prayer_assignment_failed")


async def dispatch_schedules(ctx: dict[Any, Any]) -> None:
    context = get_worker_context(ctx)
    redis: ArqRedis = ctx["redis"]
    try:
        await run_due_schedules(context, redis)
    except Exception:
        logger.exception("discord_schedule_dispatch_failed")


class WorkerSettings:
    functions = [process_prayer]
    cron_jobs = [
        cron(assign_daily, hour=0, minute=0, run_at_startup=False),
        cron(dispatch_schedules, minute=set(range(60)), second=0),
    ]
    timezone = ZoneInfo(MECCA_TIMEZONE)
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = redis_settings_from(_settings)
    max_jobs = _settings.worker_max_jobs
    max_tries = _settings.job_max_tries
    job_timeout = _settings.job_timeout
