import json
from typing import Any

from arq import ArqRedis

from src.features.x.keys import X_SESSION
from src.shared.logging.setup import get_logger

logger = get_logger("api.x.session")


def _decode(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bytes):
        return value.decode()
    return str(value)


def parse_state(raw: str) -> dict[str, Any] | None:
    try:
        state: dict[str, Any] = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None
    if not isinstance(state.get("cookies"), list):
        return None
    return state


async def load_session(redis: ArqRedis, bootstrap: str) -> dict[str, Any] | None:
    stored = _decode(await redis.get(X_SESSION))
    if stored:
        state = parse_state(stored)
        if state is not None:
            return state
        logger.warning("x_session_in_redis_unparseable falling_back_to_env")

    if not bootstrap:
        return None

    state = parse_state(bootstrap)
    if state is None:
        logger.error("x_session_env_unparseable")
        return None

    await save_session(redis, state)
    logger.info("x_session_bootstrapped_from_env")
    return state


async def save_session(redis: ArqRedis, state: dict[str, Any]) -> None:
    await redis.set(X_SESSION, json.dumps(state))
