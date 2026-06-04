from dataclasses import dataclass

from pydantic import BaseModel


class ComplianceResult(BaseModel):
    compliant: bool
    violation_type: str | None
    reason: str | None


class SpellingResult(BaseModel):
    corrected_text: str


class DedupJudgeResult(BaseModel):
    is_duplicate: bool
    duplicate_index: int | None


class DiacritizationResult(BaseModel):
    diacritized_text: str
    confidence: float


class CategorizationResult(BaseModel):
    group_name: str
    category_name: str
    type_name: str


@dataclass(slots=True)
class DuplicateOutcome:
    normalized: str
    text_hash: str
    duplicate_of_id: str | None


@dataclass(slots=True)
class CategorizationOutcome:
    category_id: str
    type_id: str


@dataclass(slots=True)
class Candidate:
    id: str
    text: str
