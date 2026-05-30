from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.features.taxonomy.schema import Category, Group, PrayerType
from src.features.taxonomy.service import TaxonomyService
from src.shared.dependencies import PocketBaseDep

router = APIRouter(tags=["taxonomy"])


def get_taxonomy_service(pocketbase: PocketBaseDep) -> TaxonomyService:
    return TaxonomyService(pocketbase)


TaxonomyServiceDep = Annotated[TaxonomyService, Depends(get_taxonomy_service)]


@router.get("/groups", response_model=list[Group])
async def list_groups(service: TaxonomyServiceDep) -> list[Group]:
    return await service.list_groups()


@router.get("/groups/{slug}", response_model=Group)
async def get_group(service: TaxonomyServiceDep, slug: str) -> Group:
    return await service.get_group(slug)


@router.get("/categories", response_model=list[Category])
async def list_categories(
    service: TaxonomyServiceDep,
    group: Annotated[str | None, Query()] = None,
) -> list[Category]:
    return await service.list_categories(group)


@router.get("/categories/{slug}", response_model=Category)
async def get_category(service: TaxonomyServiceDep, slug: str) -> Category:
    return await service.get_category(slug)


@router.get("/types", response_model=list[PrayerType])
async def list_types(service: TaxonomyServiceDep) -> list[PrayerType]:
    return await service.list_types()
