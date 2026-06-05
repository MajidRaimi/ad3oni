from typing import Any

from src.features.prayers.schema import Prayer

BRAND_COLOR = 0x6D5ACD
SITE_URL = "https://ad3oni.com"


def prayer_embed(prayer: Prayer) -> dict[str, Any]:
    return {"description": f"**﴿ {prayer.text} ﴾**", "color": BRAND_COLOR}


def help_embed() -> dict[str, Any]:
    return {
        "title": "أدعوني · ad3oni",
        "description": (
            "منصّة أدعية موثّقة. استخدم الأوامر التالية:\n\n"
            "• `/daily` — دعاء اليوم\n"
            "• `/random` — دعاء عشوائي (يمكن تحديد التصنيف)\n"
            "• `/search` — البحث في الأدعية\n"
            "• `/submit` — إرسال دعاء جديد للمراجعة\n"
            "• `/setup-daily` — نشر دعاء اليوم تلقائيًا في قناة\n"
            "• `/schedule` — جدولة نشر الأدعية بوقت محدد أو بصيغة cron"
        ),
        "color": BRAND_COLOR,
        "url": SITE_URL,
    }


def info_embed(message: str) -> dict[str, Any]:
    return {"description": message, "color": BRAND_COLOR}
