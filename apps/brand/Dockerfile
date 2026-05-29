ARG BUN_VERSION=1.3.14
ARG NODE_VERSION=22-slim

FROM oven/bun:${BUN_VERSION}-slim AS builder

WORKDIR /repo

COPY package.json bun.lock turbo.json ./
COPY apps/brand/package.json ./apps/brand/
COPY apps/web/package.json ./apps/web/

RUN bun install --no-progress

COPY apps/brand ./apps/brand

WORKDIR /repo/apps/brand
ENV NITRO_PRESET=node-server
RUN bun run build

FROM node:${NODE_VERSION} AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

RUN groupadd --system app && useradd --system --gid app --no-create-home app

COPY --from=builder --chown=app:app /repo/apps/brand/.output ./

USER app

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:3000/').then((r) => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"

CMD ["node", "server/index.mjs"]
