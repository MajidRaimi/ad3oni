from typing import Any

from src.features.prayers.schema import Prayer
from src.features.taxonomy.schema import Category

BRAND_COLOR = 0x6D5ACD
SITE_URL = "https://ad3oni.com"


def prayer_embed(prayer: Prayer) -> dict[str, Any]:
    footer_parts = [
        part
        for part in (
            prayer.source,
            prayer.category.name if prayer.category else None,
            prayer.type.name if prayer.type else None,
        )
        if part
    ]
    embed: dict[str, Any] = {
        "description": prayer.text,
        "color": BRAND_COLOR,
        "url": SITE_URL,
    }
    if prayer.category:
        embed["title"] = prayer.category.name
    if footer_parts:
        embed["footer"] = {"text": " · ".join(footer_parts)}
    return embed


def amin_components(count: int) -> list[dict[str, Any]]:
    label = "آمين" if count <= 0 else f"آمين · {count}"
    return [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": 1,
                    "label": label,
                    "emoji": {"name": "🤲"},
                    "custom_id": "amin",
                }
            ],
        }
    ]


def help_embed() -> dict[str, Any]:
    return {
        "title": "أدعوني · ad3oni",
        "description": (
            "منصّة أدعية موثّقة. استخدم الأوامر التالية:\n\n"
            "• `/daily` — دعاء اليوم\n"
            "• `/random` — دعاء عشوائي (يمكن تحديد التصنيف)\n"
            "• `/search` — البحث في الأدعية\n"
            "• `/categories` — تصفّح التصنيفات\n"
            "• `/submit` — إرسال دعاء جديد للمراجعة\n"
            "• `/setup-daily` — نشر دعاء اليوم تلقائيًا في قناة\n"
            "• `/schedule` — جدولة نشر الأدعية بوقت محدد أو بصيغة cron"
        ),
        "color": BRAND_COLOR,
        "url": SITE_URL,
    }


def info_embed(message: str) -> dict[str, Any]:
    return {"description": message, "color": BRAND_COLOR}


def categories_embed(categories: list[Category]) -> dict[str, Any]:
    groups: dict[str, list[str]] = {}
    for category in categories:
        group_name = category.group.name if category.group else "أخرى"
        groups.setdefault(group_name, []).append(category.name)
    sections = [
        f"**{group_name}**\n{'، '.join(names)}"
        for group_name, names in groups.items()
    ]
    return {
        "title": "التصنيفات",
        "description": "\n\n".join(sections),
        "color": BRAND_COLOR,
    }
