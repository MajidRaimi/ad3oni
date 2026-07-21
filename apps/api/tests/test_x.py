import json
from typing import Any, cast

import pytest
from arq import ArqRedis
from src.features.prayers.schema import Prayer
from src.features.x.keys import MAX_POST_LENGTH, X_SESSION
from src.features.x.service import compose_post
from src.features.x.session import (
    load_session,
    parse_cookies,
    save_session,
    to_browser_cookies,
)

_COOKIES = {"auth_token": "tok", "ct0": "csrf"}


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


def test_to_browser_cookies_shapes_both_for_x_domain() -> None:
    browser = to_browser_cookies(_COOKIES)
    by_name = {c["name"]: c for c in browser}
    assert set(by_name) == {"auth_token", "ct0"}
    assert all(c["domain"] == ".x.com" and c["secure"] for c in browser)
    assert by_name["auth_token"]["httpOnly"] is True
    assert by_name["ct0"]["httpOnly"] is False


def test_parse_cookies_requires_both_tokens() -> None:
    assert parse_cookies("not json") is None
    assert parse_cookies('{"auth_token": "x"}') is None
    assert parse_cookies('{"ct0": "x"}') is None
    assert parse_cookies('{"auth_token": "a", "ct0": ""}') is None
    assert parse_cookies(json.dumps(_COOKIES)) == _COOKIES


@pytest.mark.asyncio
async def test_session_bootstraps_from_env_then_persists() -> None:
    redis = FakeRedis()
    cookies = await load_session(cast(ArqRedis, redis), json.dumps(_COOKIES))
    assert cookies == _COOKIES
    assert X_SESSION in redis.values


@pytest.mark.asyncio
async def test_session_prefers_redis_over_env() -> None:
    redis = FakeRedis()
    redis.values[X_SESSION] = json.dumps({"auth_token": "fresh", "ct0": "fresh"})
    cookies = await load_session(cast(ArqRedis, redis), json.dumps(_COOKIES))
    assert cookies is not None
    assert cookies["auth_token"] == "fresh"


@pytest.mark.asyncio
async def test_session_falls_back_to_env_when_redis_corrupt() -> None:
    redis = FakeRedis()
    redis.values[X_SESSION] = "corrupted"
    cookies = await load_session(cast(ArqRedis, redis), json.dumps(_COOKIES))
    assert cookies == _COOKIES


@pytest.mark.asyncio
async def test_no_session_anywhere_returns_none() -> None:
    assert await load_session(cast(ArqRedis, FakeRedis()), "") is None


@pytest.mark.asyncio
async def test_save_session_roundtrips() -> None:
    redis = FakeRedis()
    state: dict[str, Any] = {"auth_token": "a", "ct0": "b", "extra": "c"}
    await save_session(cast(ArqRedis, redis), state)
    loaded = await load_session(cast(ArqRedis, redis), "")
    assert loaded == state
