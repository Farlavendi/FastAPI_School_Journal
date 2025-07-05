FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTE=1

ENV UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./uv.lock ./.python-version ./alembic.ini ./Makefile /app/

ENV PATH="/app/.venv/bin:$PATH"

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY ./src /app/src

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

CMD ["python", "-m", "src.main"]