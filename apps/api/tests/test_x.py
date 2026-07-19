import json
from typing import Any, cast

import pytest
from arq import ArqRedis
from src.features.prayers.schema import Prayer
from src.features.x.keys import MAX_POST_LENGTH, X_SESSION
from src.features.x.service import compose_post
from src.features.x.session import load_session, parse_state, save_session


def _prayer(text: str, source: str | None = None) -> Prayer:
    return Prayer(
        id="p1",
        text=text,
        status="confirmed",
        source=source,
        created="2026-07-19 00:00:00.000Z",
        updated="2026-07-19 00:00:00.000Z",
    )


class FakeRedis:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}

    async def get(self, key: str) -> bytes | None:
        value = self.values.get(key)
        return value.encode() if value is not None else None

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        self.values[key] = value


def test_compose_appends_source_when_it_fits() -> None:
    post = compose_post(_prayer("اللهم اغفر لي", "صحيح مسلم"))
    assert post == "اللهم اغفر لي\n\nصحيح مسلم"


def test_compose_drops_source_when_it_would_overflow() -> None:
    text = "ا" * (MAX_POST_LENGTH - 3)
    post = compose_post(_prayer(text, "صحيح البخاري"))
    assert post == text
    assert len(post or "") <= MAX_POST_LENGTH


def test_compose_returns_none_when_prayer_itself_is_too_long() -> None:
    assert compose_post(_prayer("ا" * (MAX_POST_LENGTH + 1))) is None


def test_compose_accepts_prayer_at_exactly_the_limit() -> None:
    text = "ا" * MAX_POST_LENGTH
    assert compose_post(_prayer(text)) == text


def test_parse_state_rejects_garbage() -> None:
    assert parse_state("not json") is None
    assert parse_state('{"no":"cookies"}') is None
    assert parse_state('{"cookies": []}') == {"cookies": []}


@pytest.mark.asyncio
async def test_session_bootstraps_from_env_then_persists() -> None:
    redis = FakeRedis()
    bootstrap = json.dumps({"cookies": [{"name": "auth_token"}]})

    state = await load_session(cast(ArqRedis, redis), bootstrap)

    assert state is not None
    assert state["cookies"][0]["name"] == "auth_token"
    assert X_SESSION in redis.values


@pytest.mark.asyncio
async def test_session_prefers_redis_over_env() -> None:
    redis = FakeRedis()
    redis.values[X_SESSION] = json.dumps({"cookies": [{"name": "fresh"}]})
    stale = json.dumps({"cookies": [{"name": "stale"}]})

    state = await load_session(cast(ArqRedis, redis), stale)

    assert state is not None
    assert state["cookies"][0]["name"] == "fresh"


@pytest.mark.asyncio
async def test_session_falls_back_to_env_when_redis_corrupt() -> None:
    redis = FakeRedis()
    redis.values[X_SESSION] = "corrupted"
    bootstrap = json.dumps({"cookies": [{"name": "auth_token"}]})

    state = await load_session(cast(ArqRedis, redis), bootstrap)

    assert state is not None
    assert state["cookies"][0]["name"] == "auth_token"


@pytest.mark.asyncio
async def test_no_session_anywhere_returns_none() -> None:
    assert await load_session(cast(ArqRedis, FakeRedis()), "") is None


@pytest.mark.asyncio
async def test_save_session_roundtrips() -> None:
    redis = FakeRedis()
    state: dict[str, Any] = {"cookies": [{"name": "ct0", "value": "abc"}]}

    await save_session(cast(ArqRedis, redis), state)
    loaded = await load_session(cast(ArqRedis, redis), "")

    assert loaded == state
