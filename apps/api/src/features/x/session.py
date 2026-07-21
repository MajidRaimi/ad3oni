import json
from typing import Any

from arq import ArqRedis

from src.features.x.keys import X_SESSION
from src.shared.logging.setup import get_logger

logger = get_logger("api.x.session")

Cookies = dict[str, str]

_REQUIRED = ("auth_token", "ct0")


def _decode(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode()
    return str(value)


def parse_cookies(raw: str) -> Cookies | None:
    try:
        data: Any = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None
    if not isinstance(data, dict):
        return None
    if any(not data.get(name) for name in _REQUIRED):
        return None
    return {str(k): str(v) for k, v in data.items() if v is not None}


async def load_session(redis: ArqRedis, bootstrap: str) -> Cookies | None:
    stored = _decode(await redis.get(X_SESSION))
    if stored:
        cookies = parse_cookies(stored)
        if cookies is not None:
            return cookies
        logger.warning("x_session_in_redis_unparseable falling_back_to_env")

    if not bootstrap:
        return None

    cookies = parse_cookies(bootstrap)
    if cookies is None:
        logger.error("x_session_env_unparseable")
        return None

    await save_session(redis, cookies)
    logger.info("x_session_bootstrapped_from_env")
    return cookies


async def save_session(redis: ArqRedis, cookies: Cookies) -> None:
    await redis.set(X_SESSION, json.dumps(cookies))
