from typing import Any
from zoneinfo import ZoneInfo

import httpx
from arq import ArqRedis, cron

from src.features.daily.keys import MECCA_TIMEZONE
from src.features.x.schedule import dispatch_posts
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

logger = get_logger("api.x.worker")
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
    logger.info(
        "x_worker_startup enabled=%s dry_run=%s",
        settings.x_enabled,
        settings.x_dry_run,
    )


async def shutdown(ctx: dict[Any, Any]) -> None:
    context = get_worker_context(ctx)
    await context.http.aclose()
    logger.info("x_worker_shutdown")


async def dispatch(ctx: dict[Any, Any]) -> None:
    context = get_worker_context(ctx)
    redis: ArqRedis = ctx["redis"]
    try:
        await dispatch_posts(context, redis)
    except Exception:
        logger.exception("x_dispatch_crashed")


class WorkerSettings:
    queue_name = "ad3oni:x:queue"
    functions: list[Any] = []
    cron_jobs = [cron(dispatch, minute=set(range(60)), second=15, run_at_startup=False)]
    timezone = ZoneInfo(MECCA_TIMEZONE)
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = redis_settings_from(_settings)
    max_jobs = 1
    job_timeout = 300
