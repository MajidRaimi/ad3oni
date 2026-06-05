from typing import Literal

from pydantic import BaseModel

TypeSlug = Literal["quranic", "prophetic", "athar", "custom"]
Verdict = Literal["auto_publish", "human_review"]


class SeedEntry(BaseModel):
    text: str
    type_slug: TypeSlug
    category_slug: str
    source: str
    quran_ref: tuple[int, int] | None = None
    dua_substring: str | None = None
    review_note: str | None = None


class VerifiedEntry(BaseModel):
    text: str
    type_slug: str
    category_slug: str
    source: str
    normalized: str
    text_hash: str
    verdict: Verdict
    quran_verified: bool
    notes: str | None = None
