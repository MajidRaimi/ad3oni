from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

import httpx
from arq import ArqRedis
from croniter import croniter
from openai import AsyncOpenAI

from src.features.daily.service import DailyService
from src.features.discord.describe import (
    content_label_ar,
    describe_cron_ar,
    isolate,
    rtl_block,
    timezone_label_ar,
)
from src.features.discord.embeds import (
    help_embed,
    info_embed,
    prayer_embed,
)
from src.features.discord.keys import (
    ACTION_ROW,
    APPLICATION_COMMAND,
    APPLICATION_COMMAND_AUTOCOMPLETE,
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT,
    CHANNEL_MESSAGE_WITH_SOURCE,
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
    DEFERRED_UPDATE_MESSAGE,
    EPHEMERAL_FLAG,
    MANAGE_GUILD,
    MESSAGE_COMPONENT,
    PONG,
    SCHEDULE_REMOVE_SELECT,
    STRING_SELECT,
    UPDATE_MESSAGE,
    submit_cooldown_key,
)
from src.features.discord.parse import DEFAULT_TIMEZONE, parse_schedule
from src.features.discord.rest import DiscordRest
from src.features.discord.schema import Schedule
from src.features.discord.service import DiscordScheduleService
from src.features.prayers.schema import PrayerSubmission
from src.features.prayers.service import PrayerService
from src.features.taxonomy.service import TaxonomyService
from src.shared.config.settings import Settings
from src.shared.errors.exceptions import NotFoundError, ValidationError
from src.shared.pocketbase.client import PocketBaseClient

_DAILY_CRON = "0 8 * * *"
_SUBMIT_COOLDOWN_SECONDS = 30
_SEARCH_LIMIT = 3


@dataclass(slots=True)
class DiscordDeps:
    settings: Settings
    pocketbase: PocketBaseClient
    queue: ArqRedis
    ai: AsyncOpenAI
    http: httpx.AsyncClient


@dataclass(slots=True)
class InteractionResult:
    response: dict[str, Any]
    background: Callable[[], Awaitable[None]] | None = None


def _message(
    embeds: list[dict[str, Any]], *, ephemeral: bool = False
) -> dict[str, Any]:
    data: dict[str, Any] = {"embeds": embeds}
    if ephemeral:
        data["flags"] = EPHEMERAL_FLAG
    return {"type": CHANNEL_MESSAGE_WITH_SOURCE, "data": data}


def _ephemeral(message: str) -> dict[str, Any]:
    return _message([info_embed(message)], ephemeral=True)


def _options(options: list[dict[str, Any]]) -> dict[str, Any]:
    return {option["name"]: option.get("value") for option in options}


def _user_id(payload: dict[str, Any]) -> str:
    member = payload.get("member") or {}
    user = member.get("user") or payload.get("user") or {}
    return str(user.get("id", ""))


def _has_manage_guild(payload: dict[str, Any]) -> bool:
    member = payload.get("member")
    if not member:
        return False
    try:
        permissions = int(member.get("permissions", "0"))
    except (TypeError, ValueError):
        return False
    return bool(permissions & MANAGE_GUILD)


def _focused_option(data: dict[str, Any]) -> dict[str, Any] | None:
    def walk(options: list[dict[str, Any]]) -> dict[str, Any] | None:
        for option in options:
            if option.get("focused"):
                return option
            nested = option.get("options")
            if nested and (found := walk(nested)):
                return found
        return None

    return walk(data.get("options", []))


async def _category_names(
    deps: DiscordDeps, schedules: list[Schedule]
) -> dict[str, str]:
    if not any(s.content_type == "category" and s.category for s in schedules):
        return {}
    categories = await TaxonomyService(deps.pocketbase).list_categories()
    return {category.slug: category.name for category in categories}


def _schedule_summary(schedule: Schedule, category_names: dict[str, str]) -> str:
    when = describe_cron_ar(schedule.cron) or f"وفق الجدولة `{schedule.cron}`"
    category_display = category_names.get(
        schedule.category or "", schedule.category or ""
    )
    content = content_label_ar(schedule.content_type, category_display)
    channel = isolate(f"<#{schedule.channel_id}>")
    message = rtl_block(
        f"{content} {when} {timezone_label_ar(schedule.timezone)} في {channel}"
    )
    return f"- `{schedule.id}` - {message}"


def _confirm_created(
    schedules: list[Schedule], category_names: dict[str, str]
) -> str:
    lines = "\n".join(
        _schedule_summary(schedule, category_names) for schedule in schedules
    )
    return f"تمت إضافة الجدولة:\n{lines}"


async def handle_interaction(
    payload: dict[str, Any], deps: DiscordDeps
) -> InteractionResult:
    interaction_type = payload.get("type")
    if interaction_type == APPLICATION_COMMAND:
        return await _handle_command(payload, deps)
    if interaction_type == MESSAGE_COMPONENT:
        return await _handle_component(payload, deps)
    if interaction_type == APPLICATION_COMMAND_AUTOCOMPLETE:
        return await _handle_autocomplete(payload, deps)
    return InteractionResult({"type": PONG})


async def _handle_command(
    payload: dict[str, Any], deps: DiscordDeps
) -> InteractionResult:
    data = payload["data"]
    name = data["name"]
    options = _options(data.get("options", []))

    if name == "daily":
        return await _handle_daily(deps)
    if name == "random":
        return await _handle_random(deps, options)
    if name == "search":
        return await _handle_search(deps, options)
    if name == "submit":
        return await _handle_submit(payload, deps, options)
    if name == "help":
        return InteractionResult(_message([help_embed()], ephemeral=True))
    if name == "setup-daily":
        return await _handle_setup_daily(payload, deps, options)
    if name == "schedule":
        return await _handle_schedule(payload, deps, data)
    return InteractionResult(_ephemeral("أمر غير معروف."))


async def _handle_daily(deps: DiscordDeps) -> InteractionResult:
    service = DailyService(deps.pocketbase, deps.queue)
    try:
        prayer = await service.get_daily()
    except NotFoundError:
        return InteractionResult(_ephemeral("لا توجد أدعية متاحة بعد."))
    return InteractionResult(_message([prayer_embed(prayer)]))


async def _handle_random(
    deps: DiscordDeps, options: dict[str, Any]
) -> InteractionResult:
    service = PrayerService(deps.pocketbase, deps.queue)
    try:
        prayer = await service.random_prayer(
            category=options.get("category"), type_=options.get("type")
        )
    except NotFoundError:
        return InteractionResult(_ephemeral("لا توجد أدعية مطابقة."))
    return InteractionResult(_message([prayer_embed(prayer)]))


async def _handle_search(
    deps: DiscordDeps, options: dict[str, Any]
) -> InteractionResult:
    service = PrayerService(deps.pocketbase, deps.queue)
    page = await service.list_prayers(
        q=options.get("query"),
        category=options.get("category"),
        per_page=_SEARCH_LIMIT,
    )
    if not page.items:
        return InteractionResult(_ephemeral("لا توجد نتائج."))
    embeds = [prayer_embed(prayer) for prayer in page.items]
    return InteractionResult(_message(embeds))


async def _handle_submit(
    payload: dict[str, Any], deps: DiscordDeps, options: dict[str, Any]
) -> InteractionResult:
    text = str(options.get("text", "")).strip()
    if len(text) < 3:
        return InteractionResult(_ephemeral("الدعاء قصير جدًا."))

    user_id = _user_id(payload)
    cooldown_key = submit_cooldown_key(user_id)
    if await deps.queue.get(cooldown_key) is not None:
        return InteractionResult(_ephemeral("انتظر قليلًا قبل إرسال دعاء آخر."))

    service = PrayerService(deps.pocketbase, deps.queue)
    try:
        await service.submit_prayer(PrayerSubmission(text=text))
    except ValidationError as error:
        return InteractionResult(_ephemeral(error.message))

    await deps.queue.set(cooldown_key, "1", ex=_SUBMIT_COOLDOWN_SECONDS)
    return InteractionResult(
        _ephemeral("تم استلام دعائك، وسيُراجَع ويُضاف قريبًا إن شاء الله.")
    )


async def _handle_setup_daily(
    payload: dict[str, Any], deps: DiscordDeps, options: dict[str, Any]
) -> InteractionResult:
    if not _has_manage_guild(payload):
        return InteractionResult(_ephemeral("تحتاج صلاحية إدارة الخادم."))
    guild_id = str(payload.get("guild_id", ""))
    channel_id = str(options.get("channel", ""))
    service = DiscordScheduleService(
        deps.pocketbase, deps.settings.discord_schedule_limit
    )
    try:
        created = await service.create(
            guild_id=guild_id,
            channel_id=channel_id,
            cron=_DAILY_CRON,
            timezone=DEFAULT_TIMEZONE,
            content_type="daily",
            category=None,
            label="daily prayer",
            created_by=_user_id(payload),
        )
    except ValidationError as error:
        return InteractionResult(_ephemeral(error.message))
    channel = isolate(f"<#{channel_id}>")
    return InteractionResult(
        _ephemeral(
            f"سيُنشر دعاء اليوم في {channel} يوميًا الساعة الثامنة صباحًا "
            f"(توقيت مكة).\n{isolate(f'`{created.id}`')}"
        )
    )


async def _handle_schedule(
    payload: dict[str, Any], deps: DiscordDeps, data: dict[str, Any]
) -> InteractionResult:
    if not _has_manage_guild(payload):
        return InteractionResult(_ephemeral("تحتاج صلاحية إدارة الخادم."))
    sub = data["options"][0]
    sub_name = sub["name"]
    options = _options(sub.get("options", []))
    if sub_name == "add":
        return await _handle_schedule_add(payload, deps, options)
    if sub_name == "list":
        return await _handle_schedule_list(payload, deps)
    if sub_name == "remove":
        return await _handle_schedule_remove(payload, deps)
    return InteractionResult(_ephemeral("أمر غير معروف."))


async def _handle_schedule_add(
    payload: dict[str, Any], deps: DiscordDeps, options: dict[str, Any]
) -> InteractionResult:
    guild_id = str(payload.get("guild_id", ""))
    channel_id = str(options.get("channel", ""))
    content_type = str(options.get("content") or "random")
    category = options.get("category")
    timezone = str(options.get("timezone") or DEFAULT_TIMEZONE)
    cron = options.get("cron")
    when = options.get("when")
    created_by = _user_id(payload)
    service = DiscordScheduleService(
        deps.pocketbase, deps.settings.discord_schedule_limit
    )

    if content_type == "category" and not category:
        return InteractionResult(_ephemeral("اختر تصنيفًا عند اختيار 'from a category'."))

    if cron:
        if not croniter.is_valid(str(cron)):
            return InteractionResult(_ephemeral(f"تعبير cron غير صحيح: `{cron}`"))
        try:
            created = await service.create(
                guild_id=guild_id,
                channel_id=channel_id,
                cron=str(cron),
                timezone=timezone,
                content_type=content_type,
                category=category,
                label=None,
                created_by=created_by,
            )
        except ValidationError as error:
            return InteractionResult(_ephemeral(error.message))
        names = await _category_names(deps, [created])
        return InteractionResult(_ephemeral(_confirm_created([created], names)))

    if when:
        return InteractionResult(
            {
                "type": DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {"flags": EPHEMERAL_FLAG},
            },
            background=_schedule_add_background(
                payload, deps, service, str(when), guild_id, channel_id, created_by
            ),
        )

    return InteractionResult(_ephemeral("زوّدني بتعبير cron أو وصف الوقت (when)."))


def _schedule_add_background(
    payload: dict[str, Any],
    deps: DiscordDeps,
    service: DiscordScheduleService,
    when: str,
    guild_id: str,
    channel_id: str,
    created_by: str,
) -> Callable[[], Awaitable[None]]:
    async def run() -> None:
        rest = DiscordRest(deps.http, deps.settings.discord_bot_token)
        app_id = deps.settings.discord_app_id
        token = payload["token"]
        parsed = await parse_schedule(deps.ai, deps.settings.ai_model, when)
        if parsed is None:
            await rest.edit_original(
                app_id,
                token,
                info_embed("لم أفهم الوقت المطلوب. جرّب: every day at 3pm and 6pm"),
            )
            return
        created: list[Schedule] = []
        try:
            for expr in parsed.crons:
                created.append(
                    await service.create(
                        guild_id=guild_id,
                        channel_id=channel_id,
                        cron=expr,
                        timezone=parsed.timezone,
                        content_type=parsed.content_type,
                        category=parsed.category,
                        label=parsed.label,
                        created_by=created_by,
                    )
                )
        except ValidationError as error:
            await rest.edit_original(app_id, token, info_embed(error.message))
            return
        names = await _category_names(deps, created)
        await rest.edit_original(
            app_id, token, info_embed(_confirm_created(created, names))
        )

    return run


async def _handle_schedule_list(
    payload: dict[str, Any], deps: DiscordDeps
) -> InteractionResult:
    guild_id = str(payload.get("guild_id", ""))
    service = DiscordScheduleService(deps.pocketbase)
    schedules = await service.list_for_guild(guild_id)
    if not schedules:
        return InteractionResult(_ephemeral("لا توجد جدولات في هذا الخادم."))
    names = await _category_names(deps, schedules)
    body = "\n".join(_schedule_summary(schedule, names) for schedule in schedules)
    return InteractionResult(_message([info_embed(body)], ephemeral=True))


def _remove_option(
    schedule: Schedule, category_names: dict[str, str]
) -> dict[str, Any]:
    category_display = category_names.get(
        schedule.category or "", schedule.category or ""
    )
    content = content_label_ar(schedule.content_type, category_display)
    when = describe_cron_ar(schedule.cron) or schedule.cron
    return {
        "label": f"{content} · {when}"[:100],
        "description": timezone_label_ar(schedule.timezone)[:100],
        "value": schedule.id,
    }


async def _handle_schedule_remove(
    payload: dict[str, Any], deps: DiscordDeps
) -> InteractionResult:
    guild_id = str(payload.get("guild_id", ""))
    service = DiscordScheduleService(deps.pocketbase)
    schedules = await service.list_for_guild(guild_id)
    if not schedules:
        return InteractionResult(_ephemeral("لا توجد جدولات في هذا الخادم."))
    names = await _category_names(deps, schedules)
    select = {
        "type": ACTION_ROW,
        "components": [
            {
                "type": STRING_SELECT,
                "custom_id": SCHEDULE_REMOVE_SELECT,
                "placeholder": "اختر الجدولة التي تريد حذفها",
                "options": [_remove_option(s, names) for s in schedules[:25]],
            }
        ],
    }
    return InteractionResult(
        {
            "type": CHANNEL_MESSAGE_WITH_SOURCE,
            "data": {
                "content": "اختر الجدولة التي تريد حذفها:",
                "components": [select],
                "flags": EPHEMERAL_FLAG,
            },
        }
    )


async def _handle_component(
    payload: dict[str, Any], deps: DiscordDeps
) -> InteractionResult:
    if payload["data"].get("custom_id") == SCHEDULE_REMOVE_SELECT:
        return await _handle_remove_select(payload, deps)
    return InteractionResult({"type": DEFERRED_UPDATE_MESSAGE})


async def _handle_remove_select(
    payload: dict[str, Any], deps: DiscordDeps
) -> InteractionResult:
    if not _has_manage_guild(payload):
        return InteractionResult(
            {
                "type": UPDATE_MESSAGE,
                "data": {"content": "تحتاج صلاحية إدارة الخادم.", "components": []},
            }
        )
    guild_id = str(payload.get("guild_id", ""))
    values = payload["data"].get("values", [])
    schedule_id = str(values[0]) if values else ""
    service = DiscordScheduleService(deps.pocketbase)
    removed = await service.remove(guild_id, schedule_id)
    text = "تم حذف الجدولة." if removed else "لم أجد الجدولة."
    return InteractionResult(
        {"type": UPDATE_MESSAGE, "data": {"content": text, "components": []}}
    )


async def _handle_autocomplete(
    payload: dict[str, Any], deps: DiscordDeps
) -> InteractionResult:
    focused = _focused_option(payload["data"]) or {}
    typed = str(focused.get("value") or "").strip()
    service = TaxonomyService(deps.pocketbase)
    categories = await service.list_categories()
    matches = [
        category
        for category in categories
        if not typed
        or typed in category.name
        or typed.lower() in category.slug.lower()
    ][:25]
    choices = [{"name": category.name, "value": category.slug} for category in matches]
    return InteractionResult(
        {
            "type": APPLICATION_COMMAND_AUTOCOMPLETE_RESULT,
            "data": {"choices": choices},
        }
    )
