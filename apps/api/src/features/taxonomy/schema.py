from src.shared.schema.base import CamelModel


class Group(CamelModel):
    id: str
    name: str
    slug: str


class Category(CamelModel):
    id: str
    name: str
    slug: str
    group: Group | None = None


class PrayerType(CamelModel):
    id: str
    name: str
    slug: str
