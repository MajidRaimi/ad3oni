from pydantic import BaseModel


class SampleSchema(BaseModel):
    name: str
    score: float
    note: str | None


class NestedSchema(BaseModel):
    title: str
    sample: SampleSchema
