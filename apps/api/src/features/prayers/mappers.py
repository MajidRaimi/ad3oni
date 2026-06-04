from typing import Any

from src.features.prayers.schema import Prayer
from src.features.taxonomy.mappers import to_category, to_prayer_type


def to_prayer(record: dict[str, Any]) -> Prayer:
    expand = record.get("expand", {})
    category_record = expand.get("category")
    type_record = expand.get("type")
    return Prayer(
        id=record["id"],
        text=record["text"],
        text_diacritized=record.get("text_diacritized"),
        status=record["status"],
        category=to_category(category_record) if category_record else None,
        type=to_prayer_type(type_record) if type_record else None,
        created=record["created"],
        updated=record["updated"],
    )
