from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from src.shared.ai.client import create_ai_client
from src.shared.config.settings import get_settings
from src.shared.lifespan.state import AppState
from src.shared.logging.setup import get_logger
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.queue.pool import create_arq_pool

logger = get_logger("api.lifespan")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()

    async with httpx.AsyncClient(timeout=30.0) as http:
        pocketbase = PocketBaseClient(
            settings.pocketbase_url,
            http,
            settings.pocketbase_admin_email,
            settings.pocketbase_admin_password,
        )
        await pocketbase.authenticate()
        ai = create_ai_client(settings)
        queue = await create_arq_pool(settings)

        app.state.app_state = AppState(
            settings=settings,
            pocketbase=pocketbase,
            ai=ai,
            queue=queue,
            http=http,
        )
        logger.info("startup_complete environment=%s", settings.environment)

        try:
            yield
        finally:
            await queue.aclose()
            logger.info("shutdown_complete")


def get_app_state(app: FastAPI) -> AppState:
    state: AppState = app.state.app_state
    return state
