# Backend Development Guide

## Code of Conduct

While developing, please apply the boy scout rule: leave the campground better than you found it. When issuing pull requests, be respectful of your reviewers' time.

## Code Quality Setup

### Style Guide

This project follows [PEP 8](https://pep8.org/), the official Python style guide, with automatic formatting handled by [Black](https://black.readthedocs.io/). Black's opinionated formatting removes style debates and ensures consistency.

**Key principles:**

- Follow PEP 8 conventions for naming, imports, and general code structure
- Use meaningful variable and function names
- Write docstrings for functions, classes, and modules
- Keep functions focused and reasonably sized
- Use type hints where helpful for code clarity

### Formatting Guidelines

To ensure consistency in the code style, we are using a pre-commit hook that runs Black (a formatter). Please install the pre-commit package and run `pre-commit install` (when you clone the repo) to install the hook. Formatting will run automatically on commits. If your file change is not formatted, it will fail to commit; simply re-add to staging area. It's recommended to run the formatter as a normal part of your workflow.

## Managing Dependencies

```bash
cd backend

# Add a new dependency
poetry add package-name

# Add a development dependency
poetry add --group dev package-name

# Remove a dependency
poetry remove package-name

# Update dependencies
poetry update

# After adding/removing dependencies, rebuild Docker image otherwise your new packages won't be available in the container!
docker-compose -f docker-compose.dev.yml build
```

## Docker Cleanup

Over time, Docker can take quite a bit of disk space as it loves to keep old containers, images, and volumes around. This can sometimes cause weird caching issues. Here's how to keep your Docker environment tidy:

```bash
# Stop containers (the polite way to say goodbye)
docker-compose -f docker-compose.dev.yml down

# Clean up (remove containers, volumes, images - the deep clean)
docker-compose -f docker-compose.dev.yml down -v --rmi all

# System cleanup (when your disk is crying for space)
docker system prune -a
```

## Local Development (Alternative to Docker)

```bash
cd backend

# Install dependencies
poetry install

# Run the service with hot reload (different port to avoid conflicts)
poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
```

The service will be available at `http://localhost:8001`
