import asyncio
from pathlib import Path

from playwright.async_api import async_playwright
from src.features.x.keys import ACCOUNT_SWITCHER, HOME_URL
from src.features.x.session import parse_state
from src.shared.config.settings import get_settings

_INPUT = Path(__file__).resolve().parent.parent / "x-session.json"


async def main() -> None:
    if not _INPUT.exists():
        print(f"no session file at {_INPUT}")
        print("run: uv run python -m scripts.build_x_session")
        raise SystemExit(1)

    state = parse_state(_INPUT.read_text(encoding="utf-8"))
    if state is None:
        print("session file is not valid JSON with a cookies list")
        raise SystemExit(1)

    names = sorted(c.get("name", "") for c in state["cookies"])
    print(f"cookies: {', '.join(names)}")

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(
            storage_state=state,  # type: ignore[arg-type]
            locale="ar",
            timezone_id="Asia/Riyadh",
        )
        page = await context.new_page()
        await page.goto(HOME_URL, wait_until="domcontentloaded")
        try:
            await page.wait_for_selector(ACCOUNT_SWITCHER, timeout=20_000)
            label = await page.locator(ACCOUNT_SWITCHER).inner_text()
            handle = next(
                (part for part in label.split() if part.startswith("@")), "(unknown)"
            )
            expected = f"@{get_settings().x_handle}"
            print(f"session is VALID and belongs to {handle}")
            ok = handle == expected
            if not ok:
                print(f"WRONG ACCOUNT: expected {expected}, got {handle}")
                print("Switch accounts in your browser, then copy the cookies again.")
        except Exception:
            print("session is NOT valid, x.com did not render a logged-in timeline")
            ok = False
        finally:
            await browser.close()

    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    asyncio.run(main())
