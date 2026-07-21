# Posting the daily du'a to X

This posts through [twikit](https://github.com/d60/twikit), which drives X's
internal API using a logged-in session's cookies. No developer key, no cost, no
browser.

**Read this first.** This is unofficial access, the same category that got the
account temporarily restricted once already. The realistic failure mode is
suspension of `@ad3oni_`. The trade was accepted deliberately: the official API
costs about $0.45/month at one link-free post per day and cannot get the account
suspended. twikit is also unmaintained since early 2025, so it may break if X
changes its internal API.

The feature is inert until `X_ENABLED=true`, so merging it changes nothing.

## One-time setup

### 1. Capture a session

**Never log in through automation.** Take the cookies from the browser you are
already signed into. Make sure it is switched to the account you want to post
from; if you are signed into several, the active one is what you capture.

1. Open https://x.com in your normal browser as `@ad3oni_`.
2. DevTools -> Application -> Storage -> Cookies -> `https://x.com`
3. Copy `auth_token` and `ct0`.

```bash
cd apps/api
uv sync --group x
X_AUTH_TOKEN=... X_CT0=... uv run python -m scripts.build_x_session
uv run python -m scripts.verify_x_session
```

`build_x_session` makes no network calls. `verify_x_session` asks X whose session
this is and fails loudly if it is not `@ad3oni_`, so a personal account cannot be
wired up by mistake.

### 2. Store the session

`x-session.json` is `{"auth_token":"...","ct0":"..."}`, gitignored, and must stay
that way. Put its contents in `X_SESSION_STATE`, sync to Infisical, delete the
local file.

```bash
# push to Infisical via the sync-env skill, then:
rm apps/api/x-session.json
```

### 3. Configure

| Variable | Purpose |
|---|---|
| `X_ENABLED` | Master switch. Leave `false` until you have tested. |
| `X_SESSION_STATE` | The captured cookies. Bootstraps Redis on first run. |
| `X_HANDLE` | The account to post from and verify against. Default `ad3oni_`. |
| `X_DRY_RUN` | Logs the post text and exits without posting. |
| `DISCORD_ALERT_CHANNEL_ID` | Where failures are reported. Strongly recommended. |

### 4. Dry run

```bash
X_ENABLED=true X_DRY_RUN=true uv run python -m scripts.post_daily_to_x
```

Confirms prayer selection and formatting without touching X.

## Deploying

Built from `Dockerfile.x` (a slim, browserless image, ~330MB). Runs as the
`ad3oni-x-worker` Coolify app, an arq worker on its own queue `ad3oni:x:queue`
with an 08:00 Mecca cron. `PROCESS=once` runs a single post and exits, for dry
runs and manual triggers.

## How it behaves

- **Session lives in Redis** at `ad3oni:x:session`, refreshed after every post.
  X rotates `ct0`, so writing the refreshed cookies back is what keeps the session
  alive. `X_SESSION_STATE` is only a bootstrap.
- **Posts are deduplicated** per Mecca day at `ad3oni:x:posted:<date>`, so a retry
  or double-fire cannot post twice. A `DuplicateTweet` from X is treated as a
  success (X rejects identical posts).
- **Every post is verified** by the tweet id X returns from `create_tweet`. No id
  means the post is reported as a failure, not assumed to have worked.
- **Wrong-account guard**: before posting, the session's handle is checked against
  `X_HANDLE`. A personal-account session is refused, not posted to.
- **Du'as longer than 280 characters are skipped**, not truncated, and an alert is
  sent. About 2 of 83 current prayers are affected. X counts each haraka as a
  character, so vocalised text is much longer than it looks.
- **The bot never logs in.** If the session expires or the account is locked it
  raises, alerts, and stops. Re-run step 1.

## When it breaks

It will. Cookies expire, and X changes its internal API without notice (twikit is
unmaintained). Failures alert to Discord if `DISCORD_ALERT_CHANNEL_ID` is set. If
posts stop, check that channel first, then re-capture the session. If twikit
itself breaks against a changed X API, the fallback is the official API, which
reuses everything here except `src/features/x/poster.py`.
