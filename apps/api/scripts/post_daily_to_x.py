import asyncio

import httpx
from src.features.x.service import post_one_now
from src.shared.ai.client import create_ai_client
from src.shared.config.settings import get_settings
from src.shared.logging.setup import configure_logging, get_logger
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.queue.context import WorkerContext
from src.shared.queue.pool import create_arq_pool

logger = get_logger("api.x.cli")


async def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)

    redis = await create_arq_pool(settings)
    async with httpx.AsyncClient(timeout=30.0) as http:
        pocketbase = PocketBaseClient(
            settings.pocketbase_url,
            http,
            settings.pocketbase_admin_email,
            settings.pocketbase_admin_password,
        )
        await pocketbase.authenticate()
        context = WorkerContext(settings, pocketbase, create_ai_client(settings), http)
        try:
            posted = await post_one_now(context, redis)
        finally:
            await redis.aclose()

    raise SystemExit(0 if posted else 1)


if __name__ == "__main__":
    asyncio.run(main())
