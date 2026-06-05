from fastapi import FastAPI

from src.features.daily.router import router as daily_router
from src.features.discord.router import router as discord_router
from src.features.health.router import router as health_router
from src.features.prayers.router import router as prayers_router
from src.features.taxonomy.router import router as taxonomy_router
from src.shared.config.settings import get_settings
from src.shared.errors.handlers import register_error_handlers
from src.shared.lifespan.lifespan import lifespan
from src.shared.logging.setup import configure_logging
from src.shared.middleware.cors import register_cors
from src.shared.ratelimit.limiter import register_rate_limiting

API_PREFIX = "/v1"


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(title="Ad3oni API", lifespan=lifespan)

    register_cors(app, settings)
    register_rate_limiting(app)
    register_error_handlers(app)

    app.include_router(health_router)
    app.include_router(taxonomy_router, prefix=API_PREFIX)
    app.include_router(prayers_router, prefix=API_PREFIX)
    app.include_router(daily_router, prefix=API_PREFIX)
    app.include_router(discord_router, prefix=API_PREFIX)

    return app


app = create_app()
