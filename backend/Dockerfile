# Base stage with common dependencies
FROM python:3.11-slim as base

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

# Production stage
FROM base as production

RUN poetry install --only=main

COPY src/ ./src/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["poetry", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Development stage (includes tests and dev dependencies)
FROM base as development

RUN poetry install

COPY src/ ./src/
COPY tests/ ./tests/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
