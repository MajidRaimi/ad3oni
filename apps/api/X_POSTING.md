# Posting the daily du'a to X

This drives a real browser ([patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright),
an undetected Playwright fork) with a logged-in session's cookies. No developer
key, no API cost.

**Why a browser and not a library.** twikit (X's internal API) broke the moment X
changed a script file and is unmaintained. A real browser posts through the same
UI a human uses, so X cannot break it without breaking their own website. That is
the most sustainable of the free routes.

**The risk, stated plainly.** This is still automation against X, and the account
was temporarily restricted once before (by an automated *login*, since removed).
The realistic worst case is suspension. Mitigations: we never log in (cookies
only), post once a day (human frequency), and patchright plus a user-agent fix
hide the automation markers. But the risk is not zero.

The feature is inert until `X_ENABLED=true`.

## One-time setup

### 1. Capture a session

Never log in through automation. Copy the cookies from the browser you are
already signed into, on the account you want to post from.

1. Open https://x.com in your normal browser as `@ad3oni_`.
2. DevTools -> Application -> Storage -> Cookies -> `https://x.com`
3. Copy `auth_token` and `ct0`.

```bash
cd apps/api
uv sync --group x
patchright install chromium
X_AUTH_TOKEN=... X_CT0=... uv run python -m scripts.build_x_session
uv run python -m scripts.verify_x_session
```

`build_x_session` makes no network calls. `verify_x_session` opens the browser
read-only, asks X whose session this is, and fails loudly if it is not
`@ad3oni_` (so a personal account cannot be wired up by mistake). It posts
nothing.

### 2. Store the session

`x-session.json` is `{"auth_token":"...","ct0":"..."}`, gitignored. Put its
contents in `X_SESSION_STATE`, sync to Infisical, delete the local file.

### 3. Configure

| Variable | Purpose |
|---|---|
| `X_ENABLED` | Master switch. Leave `false` until tested. |
| `X_SESSION_STATE` | The captured cookies. Bootstraps Redis on first run. |
| `X_HANDLE` | The account to post from and verify against. Default `ad3oni_`. |
| `X_HEADLESS` | `true` in production. Headed needs a real display. |
| `X_DRY_RUN` | Logs the post text and exits without opening a browser. |
| `DISCORD_ALERT_CHANNEL_ID` | Where failures are reported. Strongly recommended. |

## Stealth notes

- Real browser via **patchright**, which patches `navigator.webdriver`, CDP
  leaks, and the automation command flags before the page loads.
- Headless Chromium leaks `HeadlessChrome` in the user-agent; the poster detects
  the real UA and strips the `Headless` token so it matches genuine Chrome of the
  same version (client hints stay consistent).
- Branded Google Chrome (`channel="chrome"`, whose real TLS fingerprint is
  strongest) does not ship for Linux arm64, and the server is arm64, so we use
  patchright's patched Chromium instead.
- Persistent browser profile at `/tmp/ad3oni-x-profile` for a consistent
  fingerprint across runs.

## How it behaves

- **Cookies live in Redis** at `ad3oni:x:session`, refreshed after each post
  (X rotates `ct0`). `X_SESSION_STATE` is only a bootstrap.
- **Deduplicated** per Mecca day at `ad3oni:x:posted:<date>`.
- **Verified by reading the profile timeline back** and matching the text. An
  unverified post is reported as a failure, not assumed.
- **Wrong-account guard** refuses to post if the session is not `X_HANDLE`.
- **Du'as over 280 characters are skipped**, not truncated. About 2 of 83
  current prayers are affected (X counts each haraka).
- **Never logs in.** If the session expires or the account is locked it raises,
  alerts to Discord, and stops. Re-capture the session.

## Deploying

Built from `Dockerfile.x` on the Playwright base image (has Chromium deps and
Xvfb), running as the `ad3oni-x-worker` Coolify app: an arq worker on its own
queue `ad3oni:x:queue` with an 08:00 Mecca cron. `PROCESS=once` runs a single
post and exits, for dry runs and manual triggers.

## When it breaks

The fragile surface is the compose UI selectors in `src/features/x/keys.py`
(`tweetTextarea_0`, `tweetButton`), which change less often than X's internal
API but still change. Failures alert to Discord. If posts stop, check that
channel, then re-capture the session.
