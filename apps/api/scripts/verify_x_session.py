import asyncio
from pathlib import Path

from src.features.x.poster import SessionExpiredError, resolve_handle
from src.features.x.session import parse_cookies
from src.shared.config.settings import get_settings

_INPUT = Path(__file__).resolve().parent.parent / "x-session.json"


async def main() -> None:
    if not _INPUT.exists():
        print(f"no session file at {_INPUT}")
        print("run: uv run python -m scripts.build_x_session")
        raise SystemExit(1)

    cookies = parse_cookies(_INPUT.read_text(encoding="utf-8"))
    if cookies is None:
        print("session file is not a JSON object with auth_token and ct0")
        raise SystemExit(1)

    expected = get_settings().x_handle.lstrip("@")
    try:
        handle = await resolve_handle(cookies)
    except SessionExpiredError as error:
        print(f"session is NOT valid: {error}")
        raise SystemExit(1) from error

    if handle.lower() != expected.lower():
        print(f"WRONG ACCOUNT: session is @{handle}, expected @{expected}")
        print("Switch accounts in your browser, then copy the cookies again.")
        raise SystemExit(1)

    print(f"session is VALID and belongs to @{handle}")


if __name__ == "__main__":
    asyncio.run(main())
