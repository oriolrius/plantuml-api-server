# syntax=docker/dockerfile:1
# ---- deps -------------------------------------------------------------------
FROM python:3.12-slim AS deps
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /usr/local/bin/uv
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
# Install only third-party dependencies (not the project itself) for better caching.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# ---- runtime ----------------------------------------------------------------
FROM python:3.12-slim AS runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"
WORKDIR /app

# Always ship the newest CA bundle from the distro (eMudhra CA compromise, 2026-10):
# a stale base layer would otherwise keep trusting distrusted roots.
RUN apt-get update \
    && apt-get install -y --no-install-recommends --only-upgrade ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Non-root runtime user.
RUN useradd --system --uid 10001 --home-dir /app --no-create-home appuser

COPY --from=deps /app/.venv /app/.venv
COPY app ./app
COPY static ./static
COPY templates ./templates
COPY help ./help

USER 10001
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=4).status==200 else 1)"

# Single worker: metrics are per-process; scale with replicas behind the gateway.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
