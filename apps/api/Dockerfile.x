FROM mcr.microsoft.com/playwright/python:v1.61.0-noble AS runtime

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev --group x

# Patchright's patched Chromium. Branded Google Chrome does not ship for Linux
# arm64, and the server is arm64, so channel="chrome" is unavailable; this
# patched Chromium is the arm64 option and still fixes the webdriver/CDP leaks.
RUN patchright install chromium

COPY src ./src
COPY scripts ./scripts

HEALTHCHECK --interval=60s --timeout=10s --start-period=20s --retries=3 \
    CMD test "$PROCESS" = "once" || pgrep -f "arq src.x_worker" > /dev/null || exit 1

# Runs headless, which needs no display, so no xvfb wrapper. xvfb-run also
# swallowed the worker's logs, hiding whether the cron was firing. If X_HEADLESS
# is ever set false, wrap the command in `xvfb-run -a` to supply a display.
CMD ["sh", "-c", "if [ \"$PROCESS\" = \"once\" ]; then exec python -m scripts.post_daily_to_x; else exec arq src.x_worker.WorkerSettings; fi"]
