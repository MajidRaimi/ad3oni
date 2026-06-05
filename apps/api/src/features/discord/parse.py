from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from croniter import croniter
from openai import AsyncOpenAI
from pydantic import BaseModel

from src.shared.ai.structured import complete_json
from src.shared.errors.exceptions import UpstreamError

DEFAULT_TIMEZONE = "Asia/Riyadh"

ContentType = Literal["daily", "random", "category"]

_PARSE_SYSTEM = (
    "You convert a natural-language recurring schedule into standard 5-field cron "
    "expressions (minute hour day-of-month month day-of-week). Rules:\n"
    "- Return one cron expression per distinct firing time.\n"
    "- 'every day at 3pm and 6pm' -> [\"0 15 * * *\", \"0 18 * * *\"].\n"
    "- Interpret times in the provided default timezone unless the text names another; "
    "set 'timezone' to a valid IANA name.\n"
    "- content_type is 'daily' (the prayer of the day), 'random', or 'category'. "
    "Default to 'random'. Only set 'category' when content_type is 'category'.\n"
    "- 'label' is a short human description of the schedule.\n"
    "- If the text is not a schedule, return an empty crons list."
)


def _parse_user(text: str, default_timezone: str) -> str:
    return f"Default timezone: {default_timezone}\nSchedule: {text}"


class NLSchedule(BaseModel):
    crons: list[str]
    timezone: str
    content_type: ContentType
    category: str | None
    label: str


def _valid_timezone(name: str) -> bool:
    try:
        ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        return False
    return True


async def parse_schedule(
    ai: AsyncOpenAI,
    model: str,
    text: str,
    default_timezone: str = DEFAULT_TIMEZONE,
) -> NLSchedule | None:
    try:
        result = await complete_json(
            ai,
            model,
            _PARSE_SYSTEM,
            _parse_user(text, default_timezone),
            NLSchedule,
            reasoning_effort="low",
        )
    except UpstreamError:
        return None

    valid_crons = [expr for expr in result.crons if croniter.is_valid(expr)]
    if not valid_crons:
        return None

    result.crons = valid_crons
    if not _valid_timezone(result.timezone):
        result.timezone = default_timezone
    if result.content_type != "category":
        result.category = None
    return result
