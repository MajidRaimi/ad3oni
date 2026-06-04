from typing import Annotated, Literal

from pydantic import StringConstraints

from src.features.taxonomy.schema import Category, PrayerType
from src.shared.schema.base import CamelModel

PrayerSort = Literal["-created", "created", "-updated", "updated"]

PrayerText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=3, max_length=1000)
]
TaxonomySlug = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]


class Prayer(CamelModel):
    id: str
    text: str
    status: str
    category: Category | None = None
    type: PrayerType | None = None
    created: str
    updated: str


class PrayerSubmission(CamelModel):
    text: PrayerText
    category: TaxonomySlug | None = None
    type: TaxonomySlug | None = None


class SubmittedPrayer(CamelModel):
    id: str
    status: str
    created: str
