FROM python:3.14.5-slim
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY app ./app
COPY auth ./auth
COPY alembic.ini .
COPY migrations ./migrations
RUN mkdir -p files
CMD alembic upgrade head && uvicorn app.web_api:app --host 0.0.0.0 --port 8000
