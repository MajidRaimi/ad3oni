from typing import Any, Generic, TypeVar

from src.shared.schema.base import CamelModel

T = TypeVar("T")


class Page(CamelModel, Generic[T]):
    items: list[T]
    page: int
    per_page: int
    total_items: int
    total_pages: int


def to_page(data: dict[str, Any], items: list[T]) -> Page[T]:
    return Page(
        items=items,
        page=data.get("page", 1),
        per_page=data.get("perPage", len(items)),
        total_items=data.get("totalItems", len(items)),
        total_pages=data.get("totalPages", 1),
    )
