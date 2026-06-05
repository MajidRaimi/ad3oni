import asyncio
from collections.abc import Awaitable
from typing import cast

from src.features.daily.keys import DAILY_CURRENT, DAILY_DATE, DAILY_HISTORY
from src.shared.config.settings import get_settings
from src.shared.queue.pool import create_arq_pool


async def main() -> None:
    settings = get_settings()
    redis = await create_arq_pool(settings)
    try:
        removed = await cast(
            "Awaitable[int]", redis.delete(DAILY_CURRENT, DAILY_HISTORY, DAILY_DATE)
        )
        print(f"cleared {removed} daily key(s): current, history, date")
    finally:
        await redis.aclose()


if __name__ == "__main__":
    asyncio.run(main())
