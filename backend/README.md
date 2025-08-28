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
# Using Docker (recommended - port 8000)
docker-compose -f ../docker-compose.dev.yml up --build

# Using Poetry (for debugging - port 8001)
poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
```

### Run Tests

Tests are **not** run automatically. Run them manually when needed:

```bash
# Run all tests
docker-compose -f docker-compose.dev.yml run --rm backend poetry run pytest -vv

# Run specific test categories
docker-compose -f docker-compose.dev.yml run --rm backend poetry run pytest tests/unit/ -vv
docker-compose -f docker-compose.dev.yml run --rm backend poetry run pytest tests/int/ -vv

# Run specific test file
docker-compose -f docker-compose.dev.yml run --rm backend poetry run pytest tests/unit/test_coverage_service.py -v
```

## API Documentation

Once the service is running, you can access the interactive API documentation:

- **Docker**: `http://localhost:8000/docs` (Swagger UI) | `http://localhost:8000/redoc` (ReDoc)
- **Poetry**: `http://localhost:8001/docs` (Swagger UI) | `http://localhost:8001/redoc` (ReDoc)

## Documentation

- [Development Guide](docs/development.md) - Detailed development setup, dependencies, code quality
- [Testing Guide](docs/testing.md) - Testing setup and best practices
