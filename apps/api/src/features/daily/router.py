from typing import Annotated

from fastapi import APIRouter, Depends

from src.features.daily.service import DailyService
from src.features.prayers.schema import Prayer
from src.shared.dependencies import PocketBaseDep, RedisDep

router = APIRouter(prefix="/daily", tags=["daily"])


def get_daily_service(pocketbase: PocketBaseDep, redis: RedisDep) -> DailyService:
    return DailyService(pocketbase, redis)


DailyServiceDep = Annotated[DailyService, Depends(get_daily_service)]


@router.get("", response_model=Prayer)
async def daily_prayer(service: DailyServiceDep) -> Prayer:
    return await service.get_daily()
