FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --group x

COPY src ./src
COPY scripts ./scripts

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --group x

FROM python:3.14-slim-bookworm AS runtime

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends procps \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --system app && useradd --system --gid app --no-create-home app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src
COPY --from=builder --chown=app:app /app/scripts /app/scripts

USER app

HEALTHCHECK --interval=60s --timeout=10s --start-period=20s --retries=3 \
    CMD test "$PROCESS" = "once" || pgrep -f "arq src.x_worker" > /dev/null || exit 1

CMD ["sh", "-c", "if [ \"$PROCESS\" = \"once\" ]; then exec python -m scripts.post_daily_to_x; else exec arq src.x_worker.WorkerSettings; fi"]
