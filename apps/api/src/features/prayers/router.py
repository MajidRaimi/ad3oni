from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, Response, status

from src.features.prayers.schema import (
    Prayer,
    PrayerSort,
    PrayerSubmission,
    SubmittedPrayer,
)
from src.features.prayers.service import PrayerService
from src.shared.dependencies import PocketBaseDep, QueueDep
from src.shared.ratelimit.limiter import limiter, submit_rate_limit
from src.shared.schema.pagination import Page

router = APIRouter(prefix="/prayers", tags=["prayers"])


def get_prayer_service(pocketbase: PocketBaseDep, queue: QueueDep) -> PrayerService:
    return PrayerService(pocketbase, queue)


PrayerServiceDep = Annotated[PrayerService, Depends(get_prayer_service)]


@router.get("", response_model=Page[Prayer])
async def list_prayers(
    service: PrayerServiceDep,
    category: Annotated[str | None, Query()] = None,
    type_: Annotated[str | None, Query(alias="type")] = None,
    group: Annotated[str | None, Query()] = None,
    q: Annotated[str | None, Query()] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(alias="perPage", ge=1, le=100)] = 20,
    sort: Annotated[PrayerSort, Query()] = "-created",
) -> Page[Prayer]:
    return await service.list_prayers(
        category=category,
        type_=type_,
        group=group,
        q=q,
        page=page,
        per_page=per_page,
        sort=sort,
    )


@router.get("/random", response_model=Prayer)
async def random_prayer(
    service: PrayerServiceDep,
    category: Annotated[str | None, Query()] = None,
    type_: Annotated[str | None, Query(alias="type")] = None,
) -> Prayer:
    return await service.random_prayer(category=category, type_=type_)


@router.get("/{prayer_id}", response_model=Prayer)
async def get_prayer(service: PrayerServiceDep, prayer_id: str) -> Prayer:
    return await service.get_prayer(prayer_id)


@router.post("", response_model=SubmittedPrayer, status_code=status.HTTP_201_CREATED)
@limiter.limit(submit_rate_limit)
async def submit_prayer(
    request: Request,
    response: Response,
    service: PrayerServiceDep,
    submission: PrayerSubmission,
) -> SubmittedPrayer:
    return await service.submit_prayer(submission)
