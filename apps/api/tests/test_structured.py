from typing import Any

from src.shared.ai.structured import _strict_schema_for, _to_strict_schema

from tests.support_models import NestedSchema, SampleSchema


def test_strict_schema_forces_additional_properties_false() -> None:
    schema = _strict_schema_for(SampleSchema)
    assert schema["additionalProperties"] is False


def test_strict_schema_marks_all_properties_required() -> None:
    schema = _strict_schema_for(SampleSchema)
    assert set(schema["required"]) == {"name", "score", "note"}


def test_strict_schema_applies_to_nested_defs() -> None:
    schema = _strict_schema_for(NestedSchema)
    inner = schema["$defs"]["SampleSchema"]
    assert inner["additionalProperties"] is False
    assert set(inner["required"]) == {"name", "score", "note"}


def test_to_strict_schema_handles_plain_dict() -> None:
    node: dict[str, Any] = {"type": "object", "properties": {"a": {"type": "string"}}}
    _to_strict_schema(node)
    assert node["additionalProperties"] is False
    assert node["required"] == ["a"]
