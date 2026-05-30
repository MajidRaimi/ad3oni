from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from src.features.health.schema import HealthStatus
from src.shared.config.settings import get_settings

router = APIRouter(tags=["health"])


@router.get("/ping", response_class=PlainTextResponse)
async def ping() -> str:
    return "pong"


@router.get("/health")
async def health() -> HealthStatus:
    settings = get_settings()
    return HealthStatus(status="ok", environment=settings.environment)
