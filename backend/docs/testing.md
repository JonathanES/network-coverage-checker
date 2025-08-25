# Testing Guide

## Running Tests

### Using Docker Compose

```bash
# Run tests
docker-compose -f docker-compose.dev.yml run --rm backend-test
```

## Local Testing (Alternative to Docker)

```bash
cd backend

# Run tests
poetry run pytest -v

# Run tests with coverage
poetry run coverage run -m pytest -v
poetry run coverage report
```

## Test Structure

Tests are located in the `backend/tests/` directory and follow pytest conventions.

## Writing Tests

- Test files should be named `test_*.py`
- Test functions should be named `test_*`
- Use fixtures for common test setup
- Keep tests focused and independent
