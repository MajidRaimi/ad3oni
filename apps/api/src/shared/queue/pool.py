from arq import ArqRedis, create_pool
from arq.connections import RedisSettings

from src.shared.config.settings import Settings

PROCESS_PRAYER_TASK = "process_prayer"


def redis_settings_from(settings: Settings) -> RedisSettings:
    return RedisSettings.from_dsn(settings.redis_url)


async def create_arq_pool(settings: Settings) -> ArqRedis:
    return await create_pool(redis_settings_from(settings))


async def enqueue_process_prayer(pool: ArqRedis, prayer_id: str) -> None:
    await pool.enqueue_job(PROCESS_PRAYER_TASK, prayer_id)
