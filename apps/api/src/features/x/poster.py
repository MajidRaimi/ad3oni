from dataclasses import dataclass
from typing import Any, cast

from playwright.async_api import Page, async_playwright
from playwright.async_api import TimeoutError as PlaywrightTimeout

from src.features.x.keys import (
    ACCOUNT_SWITCHER,
    COMPOSE_URL,
    EDITOR,
    HOME_URL,
    PROFILE_URL,
    SUBMIT,
    TOAST,
    TWEET_TEXT,
)
from src.shared.logging.setup import get_logger

logger = get_logger("api.x.poster")

_LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-dev-shm-usage",
]
_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
_VERIFY_SLICE = 40


class SessionExpiredError(RuntimeError):
    pass


class PostVerificationError(RuntimeError):
    pass


@dataclass(slots=True)
class PostResult:
    verified: bool
    storage_state: dict[str, Any]


async def _assert_logged_in(page: Page, timeout_ms: int) -> None:
    try:
        await page.wait_for_selector(ACCOUNT_SWITCHER, timeout=timeout_ms)
    except PlaywrightTimeout as exc:
        raise SessionExpiredError(
            "X session is no longer valid. Re-run scripts/save_x_session.py."
        ) from exc


async def _compose(page: Page, text: str, timeout_ms: int) -> None:
    await page.goto(COMPOSE_URL, wait_until="domcontentloaded")
    editor = page.locator(EDITOR)
    await editor.wait_for(state="visible", timeout=timeout_ms)
    await editor.click()
    await page.keyboard.type(text, delay=12)

    submit = page.locator(SUBMIT)
    await submit.wait_for(state="visible", timeout=timeout_ms)
    if await submit.is_disabled():
        raise PostVerificationError("Compose button stayed disabled; text may be too long.")
    await submit.click()


async def _confirm_via_toast(page: Page, timeout_ms: int) -> bool:
    try:
        await page.wait_for_selector(TOAST, timeout=timeout_ms)
    except PlaywrightTimeout:
        return False
    return True


async def _confirm_via_profile(page: Page, handle: str, text: str, timeout_ms: int) -> bool:
    await page.goto(PROFILE_URL.format(handle=handle), wait_until="domcontentloaded")
    try:
        await page.wait_for_selector(TWEET_TEXT, timeout=timeout_ms)
    except PlaywrightTimeout:
        return False
    recent = await page.locator(TWEET_TEXT).first.inner_text()
    needle = text[:_VERIFY_SLICE].strip()
    return needle in recent


async def publish(
    text: str,
    *,
    storage_state: dict[str, Any],
    handle: str,
    headless: bool,
    timeout_ms: int,
) -> PostResult:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=headless, args=_LAUNCH_ARGS)
        try:
            context = await browser.new_context(
                storage_state=storage_state,  # type: ignore[arg-type]
                locale="ar",
                timezone_id="Asia/Riyadh",
                user_agent=_USER_AGENT,
                viewport={"width": 1280, "height": 900},
            )
            page = await context.new_page()

            await page.goto(HOME_URL, wait_until="domcontentloaded")
            await _assert_logged_in(page, timeout_ms)

            await _compose(page, text, timeout_ms)

            verified = await _confirm_via_toast(page, timeout_ms // 3)
            if not verified:
                logger.info("x_toast_missing falling_back_to_profile_readback")
                verified = await _confirm_via_profile(page, handle, text, timeout_ms)

            refreshed = cast("dict[str, Any]", await context.storage_state())
            await context.close()
            return PostResult(verified=verified, storage_state=refreshed)
        finally:
            await browser.close()
