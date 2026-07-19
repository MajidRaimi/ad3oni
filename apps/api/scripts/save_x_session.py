import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright
from src.features.x.keys import ACCOUNT_SWITCHER, HOME_URL

_OUTPUT = Path(__file__).resolve().parent.parent / "x-session.json"
_LOGIN_TIMEOUT_MS = 5 * 60 * 1000

_INSTRUCTIONS = """
A browser window will open on x.com.

  1. Log in there yourself, exactly as you normally would.
  2. Complete any 2FA or captcha challenge.
  3. Wait until your home timeline is visible.

This script never sees or stores your password. It waits for a valid session
and then saves only the resulting cookies.

Do not commit the output file. Push it to Infisical as X_SESSION_STATE instead.
"""


async def main() -> None:
    print(_INSTRUCTIONS)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(
            locale="ar",
            timezone_id="Asia/Riyadh",
            viewport={"width": 1280, "height": 900},
        )
        page = await context.new_page()
        await page.goto(HOME_URL)

        print("waiting for a logged-in session (up to 5 minutes)...")
        try:
            await page.wait_for_selector(ACCOUNT_SWITCHER, timeout=_LOGIN_TIMEOUT_MS)
        except Exception:
            print("timed out before a session appeared; nothing was saved")
            await browser.close()
            raise SystemExit(1) from None

        state = await context.storage_state()
        await browser.close()

    _OUTPUT.write_text(json.dumps(state), encoding="utf-8")
    cookies = state.get("cookies", [])
    print(f"\nsaved {len(cookies)} cookies to {_OUTPUT}")
    print("\nNext:")
    print(f"  1. Set X_SESSION_STATE to the contents of {_OUTPUT.name}")
    print("  2. Sync it to Infisical, then delete the local file")
    print(f"  3. rm {_OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())
