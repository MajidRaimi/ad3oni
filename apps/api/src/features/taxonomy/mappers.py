from typing import Any

from src.features.taxonomy.schema import Category, Group, PrayerType


def to_group(record: dict[str, Any]) -> Group:
    return Group(id=record["id"], name=record["name"], slug=record["slug"])


def to_category(record: dict[str, Any]) -> Category:
    group_record = record.get("expand", {}).get("group")
    return Category(
        id=record["id"],
        name=record["name"],
        slug=record["slug"],
        group=to_group(group_record) if group_record else None,
    )


def to_prayer_type(record: dict[str, Any]) -> PrayerType:
    return PrayerType(id=record["id"], name=record["name"], slug=record["slug"])
