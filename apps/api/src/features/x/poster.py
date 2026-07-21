import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, cast

from patchright.async_api import (
    BrowserContext,
    Page,
    async_playwright,
)
from patchright.async_api import (
    TimeoutError as PlaywrightTimeout,
)

from src.features.x.keys import (
    _USER_DATA_DIR,
    COMPOSE_URL,
    EDITOR,
    HOME_URL,
    PROFILE_LINK,
    PROFILE_URL,
    SUBMIT,
    TWEET_TEXT,
)
from src.features.x.session import Cookies, to_browser_cookies
from src.shared.logging.setup import get_logger

logger = get_logger("api.x.poster")

_VERIFY_SLICE = 30


class SessionExpiredError(RuntimeError):
    pass


class WrongAccountError(RuntimeError):
    pass


class PostVerificationError(RuntimeError):
    pass


@dataclass(slots=True)
class PostResult:
    verified: bool
    cookies: Cookies


@asynccontextmanager
async def _context(
    cookies: Cookies, *, headless: bool, channel: str, timeout_ms: int
) -> AsyncIterator[BrowserContext]:
    async with async_playwright() as playwright:
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=_USER_DATA_DIR,
            channel=channel or None,
            headless=headless,
            no_viewport=True,
        )
        context.set_default_timeout(timeout_ms)
        context.set_default_navigation_timeout(timeout_ms)
        await context.add_cookies(cast("Any", to_browser_cookies(cookies)))
        try:
            yield context
        finally:
            await context.close()


async def _new_page(context: BrowserContext, headless: bool) -> Page:
    page = await context.new_page()
    if not headless:
        return page
    agent: str = await page.evaluate("() => navigator.userAgent")
    if "HeadlessChrome" not in agent:
        return page
    cdp = await context.new_cdp_session(page)
    await cdp.send(
        "Network.setUserAgentOverride",
        {"userAgent": agent.replace("HeadlessChrome", "Chrome")},
    )
    return page


async def _current_cookies(context: BrowserContext) -> Cookies:
    wanted = {"auth_token", "ct0"}
    return {
        c["name"]: c["value"]
        for c in await context.cookies("https://x.com")
        if c["name"] in wanted
    }


async def _current_handle(page: Page) -> str:
    await page.goto(HOME_URL, wait_until="domcontentloaded")
    try:
        await page.wait_for_selector(PROFILE_LINK)
    except PlaywrightTimeout as exc:
        raise SessionExpiredError(
            "X did not render a logged-in timeline; the session is invalid or "
            "the account is restricted."
        ) from exc
    href = await page.locator(PROFILE_LINK).get_attribute("href")
    return (href or "").strip("/").lstrip("@")


async def _assert_logged_in(page: Page, handle: str) -> None:
    actual = await _current_handle(page)
    if actual.lower() != handle.lstrip("@").lower():
        raise WrongAccountError(
            f"session belongs to @{actual or 'unknown'}, expected @{handle}"
        )


async def _compose(page: Page, text: str) -> None:
    await page.goto(COMPOSE_URL, wait_until="domcontentloaded")
    editor = page.locator(EDITOR).first
    await editor.wait_for(state="visible")
    await editor.click()
    await page.keyboard.insert_text(text)

    submit = page.locator(SUBMIT).first
    await submit.wait_for(state="visible")
    if await submit.is_disabled():
        raise PostVerificationError("compose button stayed disabled; text rejected")

    modifier = "Meta" if sys.platform == "darwin" else "Control"
    await page.keyboard.press(f"{modifier}+Enter")

    # The composer clears/detaches once X accepts the post; wait for that signal
    # rather than a fixed sleep so verification does not race the send.
    try:
        await editor.wait_for(state="detached", timeout=20_000)
    except PlaywrightTimeout:
        await page.wait_for_timeout(4000)


async def _confirm_on_profile(page: Page, handle: str, text: str) -> bool:
    await page.goto(
        PROFILE_URL.format(handle=handle.lstrip("@")), wait_until="domcontentloaded"
    )
    try:
        await page.wait_for_selector(TWEET_TEXT)
    except PlaywrightTimeout:
        return False
    needle = text[:_VERIFY_SLICE].strip()
    count = min(await page.locator(TWEET_TEXT).count(), 5)
    for index in range(count):
        if needle in await page.locator(TWEET_TEXT).nth(index).inner_text():
            return True
    return False


async def resolve_handle(cookies: Cookies, *, headless: bool, channel: str) -> str:
    async with _context(
        cookies, headless=headless, channel=channel, timeout_ms=45_000
    ) as context:
        page = await _new_page(context, headless)
        return await _current_handle(page)


async def publish(
    text: str,
    *,
    cookies: Cookies,
    handle: str,
    headless: bool,
    channel: str,
    timeout_ms: int,
) -> PostResult:
    async with _context(
        cookies, headless=headless, channel=channel, timeout_ms=timeout_ms
    ) as context:
        page = await _new_page(context, headless)
        await _assert_logged_in(page, handle)
        await _compose(page, text)
        verified = await _confirm_on_profile(page, handle, text)
        cookies_out = await _current_cookies(context)
        return PostResult(verified=verified, cookies=cookies_out or cookies)
