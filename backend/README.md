# Backend Service

FastAPI service for the network coverage checker.

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- **Language**: Python 3.11
- **Package Manager**: [Poetry](https://python-poetry.org/) - Dependency management and packaging
- **Testing**: [pytest](https://pytest.org/) - Testing framework
- **Code Formatting**: [Black](https://black.readthedocs.io/) - Code formatter
- **Containerization**: Docker

## Quick Start

### Setup

```bash
# Install dependencies and pre-commit hooks
poetry install
poetry run pre-commit install
```

### Run the Service

```bash
# Using Docker (recommended)
docker-compose -f ../docker-compose.dev.yml up --build

# Using Poetry (alternative - port 8001)
poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
```

### Run Tests

```bash
# Using Docker
docker-compose -f ../docker-compose.dev.yml run --rm backend-test

# Using Poetry
poetry run pytest -v
```

## API Documentation

Once the service is running, you can access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Documentation

- [Development Guide](docs/development.md) - Detailed development setup, dependencies, code quality
- [Testing Guide](docs/testing.md) - Testing setup and best practices
