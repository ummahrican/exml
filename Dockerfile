# syntax=docker/dockerfile:1

##
## Build stage: resolve and install dependencies into /app/.venv
##
FROM python:3.12-slim AS builder

# Pinned so builds are reproducible ("latest" silently changes under you)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /bin/uv

ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Only the lockfile inputs, so this layer is cached until dependencies change
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache --no-install-project

##
## Runtime stage: application + the prebuilt venv, no uv, no build caches
##
FROM python:3.12-slim

# The venv keeps absolute paths, so it must land on the same path it was built at
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

WORKDIR /app

# Application code last: source edits don't invalidate the dependency layer
COPY . .

# Runtime write targets (app.py: UPLOAD_FOLDER / OUTPUT_FOLDER), owned by the app user
RUN useradd --create-home --uid 10001 app \
    && mkdir -p /app/uploads /app/output_xmls \
    && chown -R app:app /app/uploads /app/output_xmls

USER app

EXPOSE 5000

# Override the port at run time with -e FLASK_RUN_PORT=...
CMD ["flask", "run"]
