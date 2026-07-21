from dataclasses import dataclass

from twikit import Client
from twikit.errors import (
    AccountLocked,
    AccountSuspended,
    DuplicateTweet,
    Unauthorized,
)

from src.shared.logging.setup import get_logger

logger = get_logger("api.x.poster")

_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)

Cookies = dict[str, str]


class SessionExpiredError(RuntimeError):
    pass


class WrongAccountError(RuntimeError):
    pass


@dataclass(slots=True)
class PostResult:
    verified: bool
    tweet_id: str | None
    cookies: Cookies
    duplicate: bool = False


def _client() -> Client:
    return Client("en-US", user_agent=_USER_AGENT)


async def resolve_handle(cookies: Cookies) -> str:
    client = _client()
    client.set_cookies(dict(cookies))
    try:
        me = await client.user()
    except (Unauthorized, AccountLocked, AccountSuspended) as exc:
        raise SessionExpiredError(
            f"X session is not usable ({type(exc).__name__})."
        ) from exc
    return (me.screen_name or "").lstrip("@")


async def publish(text: str, *, cookies: Cookies, handle: str) -> PostResult:
    client = _client()
    client.set_cookies(dict(cookies))

    try:
        me = await client.user()
    except (Unauthorized, AccountLocked, AccountSuspended) as exc:
        raise SessionExpiredError(
            f"X session is not usable ({type(exc).__name__}). "
            "Re-capture with scripts/build_x_session.py."
        ) from exc

    actual = (me.screen_name or "").lstrip("@").lower()
    expected = handle.lstrip("@").lower()
    if actual != expected:
        raise WrongAccountError(f"session belongs to @{actual}, expected @{expected}")

    try:
        tweet = await client.create_tweet(text=text)
    except DuplicateTweet:
        logger.info("x_duplicate_tweet already_posted")
        return PostResult(
            verified=True, tweet_id=None, cookies=client.get_cookies(), duplicate=True
        )
    except (Unauthorized, AccountLocked, AccountSuspended) as exc:
        raise SessionExpiredError(f"X rejected the post ({type(exc).__name__}).") from exc

    tweet_id = getattr(tweet, "id", None)
    return PostResult(
        verified=bool(tweet_id),
        tweet_id=tweet_id,
        cookies=client.get_cookies(),
    )
