import json
from datetime import datetime
from typing import Any, cast
from zoneinfo import ZoneInfo

import httpx
import pytest
from fastapi.testclient import TestClient
from nacl.signing import SigningKey
from openai import AsyncOpenAI
from src.features.discord import parse as parse_module
from src.features.discord.describe import (
    content_label_ar,
    describe_cron_ar,
    timezone_label_ar,
)
from src.features.discord.parse import NLSchedule, parse_schedule
from src.features.discord.scheduler import _is_due, run_due_schedules
from src.features.discord.schema import Schedule
from src.features.discord.verify import verify_signature
from src.main import create_app
from src.shared.config.settings import Settings
from src.shared.lifespan.state import AppState
from src.shared.pocketbase.client import PocketBaseClient
from src.shared.queue.context import WorkerContext

GROUP: dict[str, Any] = {"id": "g1", "name": "المشاعر", "slug": "emotion"}
CATEGORY: dict[str, Any] = {
    "id": "c1",
    "name": "القلق والهمّ",
    "slug": "anxiety",
    "expand": {"group": GROUP},
}
PRAYER_TYPE: dict[str, Any] = {"id": "t1", "name": "نبوي", "slug": "prophetic"}
PRAYER: dict[str, Any] = {
    "id": "p1",
    "text": "اللَّهُمَّ اغْفِرْ لِي وَارْحَمْنِي",
    "status": "confirmed",
    "source": "صحيح مسلم",
    "created": "2026-05-30 00:00:00.000Z",
    "updated": "2026-05-30 00:00:00.000Z",
    "expand": {"category": CATEGORY, "type": PRAYER_TYPE},
}


class FakePocketBase:
    def __init__(self) -> None:
        self.schedules: list[dict[str, Any]] = []
        self.created: list[dict[str, Any]] = []
        self.updated: list[tuple[str, dict[str, Any]]] = []
        self.deleted: list[str] = []
        self._counter = 0

    async def list_records(
        self, collection: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if collection == "categories":
            items = [CATEGORY]
        elif collection == "prayers":
            items = [PRAYER]
        elif collection == "schedules":
            items = self.schedules
        else:
            items = []
        return {
            "items": items,
            "page": 1,
            "perPage": 20,
            "totalItems": len(items),
            "totalPages": 1,
        }

    async def get_first(
        self, collection: str, filter_: str, *, expand: str | None = None
    ) -> dict[str, Any] | None:
        if collection == "prayers":
            return PRAYER
        if collection == "schedules":
            return self.schedules[0] if self.schedules else None
        if collection in {"categories", "types", "groups"}:
            return CATEGORY
        return None

    async def create_record(
        self, collection: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        self._counter += 1
        record = {
            **payload,
            "id": f"rec{self._counter}",
            "created": "2026-05-30 00:00:00.000Z",
            "updated": "2026-05-30 00:00:00.000Z",
        }
        if collection == "schedules":
            self.schedules.append(record)
        self.created.append(record)
        return record

    async def update_record(
        self, collection: str, record_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        self.updated.append((record_id, payload))
        return {"id": record_id, **payload}

    async def delete_record(self, collection: str, record_id: str) -> None:
        self.deleted.append(record_id)


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.counters: dict[str, int] = {}

    async def get(self, key: str) -> bytes | None:
        value = self.values.get(key)
        return value.encode() if value is not None else None

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        self.values[key] = value

    async def incr(self, key: str) -> int:
        self.counters[key] = self.counters.get(key, 0) + 1
        return self.counters[key]


class FakeResponse:
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class FakeHttp:
    def __init__(self, status_code: int = 200) -> None:
        self.status_code = status_code
        self.posts: list[str] = []

    async def post(
        self, url: str, headers: dict[str, str], json: dict[str, Any]
    ) -> FakeResponse:
        self.posts.append(url)
        return FakeResponse(self.status_code)


def _settings(public_key: str) -> Settings:
    return Settings(
        discord_public_key=public_key,
        discord_app_id="app1",
        discord_bot_token="bot-token",
    )


def _client(public_key: str, pocketbase: FakePocketBase, redis: FakeRedis) -> TestClient:
    app = create_app()
    app.state.app_state = AppState(
        settings=_settings(public_key),
        pocketbase=cast(PocketBaseClient, pocketbase),
        ai=cast(AsyncOpenAI, None),
        queue=cast(Any, redis),
        http=cast(Any, FakeHttp()),
    )
    return TestClient(app)


def _post(
    client: TestClient, signing_key: SigningKey, payload: dict[str, Any]
) -> httpx.Response:
    body = json.dumps(payload).encode()
    timestamp = "1700000000"
    signature = signing_key.sign(timestamp.encode() + body).signature.hex()
    return client.post(
        "/v1/discord/interactions",
        content=body,
        headers={
            "X-Signature-Ed25519": signature,
            "X-Signature-Timestamp": timestamp,
            "Content-Type": "application/json",
        },
    )


def _command(
    name: str,
    options: list[dict[str, Any]] | None = None,
    *,
    permissions: str = "0",
) -> dict[str, Any]:
    return {
        "type": 2,
        "token": "interaction-token",
        "guild_id": "guild1",
        "member": {"permissions": permissions, "user": {"id": "user1"}},
        "data": {"name": name, "options": options or []},
    }


@pytest.fixture
def keypair() -> SigningKey:
    return SigningKey.generate()


def test_verify_accepts_valid_signature(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    body = b'{"type":1}'
    timestamp = "123"
    signature = keypair.sign(timestamp.encode() + body).signature.hex()
    assert verify_signature(public_key, signature, timestamp, body) is True


def test_verify_rejects_tampered_body(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    timestamp = "123"
    signature = keypair.sign(timestamp.encode() + b'{"type":1}').signature.hex()
    assert verify_signature(public_key, signature, timestamp, b'{"type":2}') is False


def test_ping_returns_pong(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    client = _client(public_key, FakePocketBase(), FakeRedis())
    response = _post(client, keypair, {"type": 1})
    assert response.status_code == 200
    assert response.json() == {"type": 1}


def test_bad_signature_is_rejected(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    client = _client(public_key, FakePocketBase(), FakeRedis())
    response = client.post(
        "/v1/discord/interactions",
        content=b'{"type":1}',
        headers={
            "X-Signature-Ed25519": "00" * 64,
            "X-Signature-Timestamp": "1",
        },
    )
    assert response.status_code == 401


def test_random_command_returns_minimal_prayer_embed(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    client = _client(public_key, FakePocketBase(), FakeRedis())
    response = _post(client, keypair, _command("random"))
    body = response.json()
    assert body["type"] == 4
    embed = body["data"]["embeds"][0]
    assert embed["description"] == f"**﴿ {PRAYER['text']} ﴾**"
    assert "title" not in embed
    assert "footer" not in embed
    assert "components" not in body["data"]


def test_describe_cron_ar() -> None:
    assert describe_cron_ar("0 8 * * *") == "كل يوم الساعة ٨ صباحًا"
    assert describe_cron_ar("18 19 * * *") == "كل يوم الساعة ٧:١٨ مساءً"
    assert describe_cron_ar("0 12 * * *") == "كل يوم ظهرًا"
    assert describe_cron_ar("0 0 * * *") == "كل يوم منتصف الليل"
    assert describe_cron_ar("30 6 * * 5") == "كل جمعة الساعة ٦:٣٠ صباحًا"
    assert describe_cron_ar("*/15 * * * *") is None


def test_schedule_summary_isolates_bidi() -> None:
    from src.features.discord import handlers
    from src.features.discord.schema import Schedule

    schedule = Schedule(
        id="abc123",
        guild_id="g",
        channel_id="555",
        cron="0 8 * * *",
        timezone="Asia/Riyadh",
        content_type="daily",
    )
    rli, fsi, pdi = chr(0x2067), chr(0x2068), chr(0x2069)
    summary = handlers._schedule_summary(schedule, {})
    assert summary.startswith(f"- `abc123` - {rli}")
    assert f"{fsi}<#555>{pdi}" in summary
    assert summary.endswith(pdi)


def test_timezone_and_content_labels() -> None:
    assert timezone_label_ar("Asia/Riyadh") == "بتوقيت مكة"
    assert timezone_label_ar("Africa/Cairo") == "بتوقيت القاهرة"
    assert content_label_ar("daily", None) == "دعاء اليوم"
    assert content_label_ar("random", None) == "دعاء عشوائي"
    assert content_label_ar("category", "الرزق") == "دعاء من تصنيف الرزق"


def test_component_interaction_is_acknowledged(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    client = _client(public_key, FakePocketBase(), FakeRedis())
    payload = {
        "type": 3,
        "token": "t",
        "data": {"custom_id": "amin"},
        "message": {"id": "m1"},
    }
    body = _post(client, keypair, payload).json()
    assert body["type"] == 6


def test_autocomplete_returns_categories(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    client = _client(public_key, FakePocketBase(), FakeRedis())
    payload = {
        "type": 4,
        "token": "t",
        "data": {
            "name": "random",
            "options": [{"name": "category", "value": "", "focused": True}],
        },
    }
    body = _post(client, keypair, payload).json()
    assert body["type"] == 8
    assert body["data"]["choices"][0]["value"] == "anxiety"


def test_schedule_add_requires_permission(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    client = _client(public_key, FakePocketBase(), FakeRedis())
    options = [{"name": "add", "options": [{"name": "channel", "value": "chan1"}]}]
    body = _post(client, keypair, _command("schedule", options)).json()
    assert body["data"]["flags"] == (1 << 6)
    assert "صلاحية" in body["data"]["embeds"][0]["description"]


def test_schedule_add_with_cron_creates(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    pocketbase = FakePocketBase()
    client = _client(public_key, pocketbase, FakeRedis())
    options = [
        {
            "name": "add",
            "options": [
                {"name": "channel", "value": "chan1"},
                {"name": "cron", "value": "0 15 * * *"},
            ],
        }
    ]
    body = _post(
        client, keypair, _command("schedule", options, permissions="32")
    ).json()
    assert body["type"] == 4
    assert len(pocketbase.schedules) == 1
    assert pocketbase.schedules[0]["cron"] == "0 15 * * *"


def test_schedule_add_with_invalid_cron_is_rejected(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    pocketbase = FakePocketBase()
    client = _client(public_key, pocketbase, FakeRedis())
    options = [
        {
            "name": "add",
            "options": [
                {"name": "channel", "value": "chan1"},
                {"name": "cron", "value": "not-a-cron"},
            ],
        }
    ]
    body = _post(
        client, keypair, _command("schedule", options, permissions="32")
    ).json()
    assert pocketbase.schedules == []
    assert "cron" in body["data"]["embeds"][0]["description"]


def _seed_schedule(pocketbase: FakePocketBase) -> None:
    pocketbase.schedules.append(
        {
            "id": "sch1",
            "guild_id": "guild1",
            "channel_id": "c1",
            "cron": "0 8 * * *",
            "timezone": "Asia/Riyadh",
            "content_type": "daily",
            "category": "",
            "label": "",
            "enabled": True,
            "last_run_at": "",
        }
    )


def test_schedule_remove_shows_select(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    pocketbase = FakePocketBase()
    _seed_schedule(pocketbase)
    client = _client(public_key, pocketbase, FakeRedis())
    options = [{"name": "remove"}]
    body = _post(
        client, keypair, _command("schedule", options, permissions="32")
    ).json()
    assert body["type"] == 4
    select = body["data"]["components"][0]["components"][0]
    assert select["type"] == 3
    assert select["custom_id"] == "schedule_remove"
    assert select["options"][0]["value"] == "sch1"


def test_schedule_remove_select_deletes(keypair: SigningKey) -> None:
    public_key = keypair.verify_key.encode().hex()
    pocketbase = FakePocketBase()
    _seed_schedule(pocketbase)
    client = _client(public_key, pocketbase, FakeRedis())
    payload = {
        "type": 3,
        "token": "t",
        "guild_id": "guild1",
        "member": {"permissions": "32", "user": {"id": "u"}},
        "data": {"custom_id": "schedule_remove", "values": ["sch1"]},
    }
    body = _post(client, keypair, payload).json()
    assert body["type"] == 7
    assert "sch1" in pocketbase.deleted


@pytest.mark.asyncio
async def test_parse_schedule_filters_invalid_cron(monkeypatch: Any) -> None:
    async def fake_complete_json(*args: Any, **kwargs: Any) -> NLSchedule:
        return NLSchedule(
            crons=["0 15 * * *", "garbage"],
            timezone="Asia/Riyadh",
            content_type="random",
            category=None,
            label="afternoon",
        )

    monkeypatch.setattr(parse_module, "complete_json", fake_complete_json)
    result = await parse_schedule(
        cast(AsyncOpenAI, None), "model", "every day at 3pm"
    )
    assert result is not None
    assert result.crons == ["0 15 * * *"]


def test_is_due_matches_and_dedupes() -> None:
    now = datetime(2026, 6, 5, 15, 0, tzinfo=ZoneInfo("Asia/Riyadh"))
    schedule = Schedule(
        id="s1",
        guild_id="g1",
        channel_id="c1",
        cron="0 15 * * *",
        timezone="Asia/Riyadh",
        content_type="random",
    )
    assert _is_due(schedule, now) is True
    schedule.last_run_at = now.isoformat()
    assert _is_due(schedule, now) is False


@pytest.mark.asyncio
async def test_run_due_schedules_posts_and_marks() -> None:
    pocketbase = FakePocketBase()
    pocketbase.schedules.append(
        {
            "id": "s1",
            "guild_id": "g1",
            "channel_id": "c1",
            "cron": "* * * * *",
            "timezone": "Asia/Riyadh",
            "content_type": "random",
            "category": "",
            "label": "",
            "enabled": True,
            "last_run_at": "",
        }
    )
    http = FakeHttp(status_code=200)
    context = WorkerContext(
        settings=_settings("deadbeef"),
        pocketbase=cast(PocketBaseClient, pocketbase),
        ai=cast(AsyncOpenAI, None),
        http=cast(Any, http),
    )
    await run_due_schedules(context, cast(Any, FakeRedis()))
    assert len(http.posts) == 1
    assert pocketbase.updated and pocketbase.updated[0][0] == "s1"
