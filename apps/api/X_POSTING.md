# Posting the daily du'a to X

This posts through a real browser session rather than the X API.

**Read this first.** Automated posting through the web UI is against X's automation
rules. The realistic failure mode is suspension of `@ad3oni_`. This is the trade
that was accepted: the official API costs about $0.45/month at one link-free post
per day, and cannot get the account suspended.

The feature is inert until `X_ENABLED=true`, so merging it changes nothing.

## One-time setup

### 1. Capture a session

**Never log in through automation.** Playwright's bundled Chromium is trivially
fingerprinted by X, and logging in through it will get the account temporarily
restricted. That happened once already. Take the cookies from the browser you
are already signed into instead.

Make sure the browser is switched to the account you want to post from. If you
are signed into several, the active one is what gets captured.

1. Open https://x.com in your normal browser as `@ad3oni_`.
2. DevTools -> Application -> Storage -> Cookies -> `https://x.com`
3. Copy `auth_token` and `ct0`.

```bash
cd apps/api
uv sync --group playwright
uv run playwright install chromium
X_AUTH_TOKEN=... X_CT0=... uv run python -m scripts.build_x_session
uv run python -m scripts.verify_x_session
```

`build_x_session` touches nothing on the network. `verify_x_session` loads the
timeline once and reports which handle the session belongs to, so a personal
account cannot be wired up by mistake.

### 2. Store the session

`x-session.json` is gitignored and must stay that way. Put its contents in
`X_SESSION_STATE`, sync to Infisical, then delete the local file.

```bash
# push to Infisical via the sync-env skill, then:
rm apps/api/x-session.json
```

### 3. Configure

| Variable | Purpose |
|---|---|
| `X_ENABLED` | Master switch. Leave `false` until you have tested. |
| `X_SESSION_STATE` | The captured cookies. Bootstraps Redis on first run. |
| `X_HANDLE` | Used for read-back verification. Default `ad3oni_`. |
| `X_HEADLESS` | `true` in production. |
| `X_DRY_RUN` | Logs the post text and exits without posting. |
| `DISCORD_ALERT_CHANNEL_ID` | Where failures are reported. Strongly recommended. |

### 4. Dry run

```bash
X_ENABLED=true X_DRY_RUN=true uv run python -m scripts.post_daily_to_x
```

Confirms prayer selection and formatting without touching X.

## Deploying

Build from `Dockerfile.playwright`, which is separate so the api and worker
images stay slim. The container runs `scripts/post_daily_to_x.py` once and exits,
so schedule it as a Coolify Scheduled Task rather than a long-running service.

Suggested schedule: `0 8 * * *` (08:00 Mecca time), matching the Discord default.

## How it behaves

- **Session lives in Redis** at `ad3oni:x:session`, refreshed after every
  successful post. X rotates cookies, so writing the refreshed state back is what
  keeps the session alive. `X_SESSION_STATE` is only a bootstrap.
- **Posts are deduplicated** per Mecca day at `ad3oni:x:posted:<date>`, so a retry
  or double-fire cannot post twice.
- **Every post is verified**, first by waiting for the confirmation toast, then by
  reading the profile timeline back and matching the text. An unverified post is
  reported as a failure rather than silently assumed to have worked.
- **Du'as longer than 280 characters are skipped**, not truncated, and an alert is
  sent. About 2 of 83 current prayers are affected. Note X counts each haraka as a
  character, so vocalised text is much longer than it looks.
- **The bot never logs in.** If the session expires it raises, alerts, and stops.
  Re-run step 1.

## When it breaks

It will. Cookies expire, and X changes its UI without notice. Failures alert to
Discord if `DISCORD_ALERT_CHANNEL_ID` is set. If posts stop, check that channel
first, then re-capture the session.

The selectors most likely to break are in `src/features/x/keys.py`.
