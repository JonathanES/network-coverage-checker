# Network Coverage Checker

A full-stack application for checking network coverage with a FastAPI backend and Angular frontend.

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (recommended for quick setup)
- [Node.js](https://nodejs.org/) (for frontend development)
- [Poetry](https://python-poetry.org/docs/#installation) (for backend development)

### Clone the Repository

```bash
git clone https://github.com/JonathanES/network-coverage-checker.git
cd network-coverage-checker
```

## Project Structure

- **Backend**: FastAPI service - see [backend/README.md](backend/README.md)
- **Frontend**: Angular application with Material UI

## Quick Start

### Backend Only (Docker)

```bash
docker-compose -f docker-compose.dev.yml up --build
```

Backend API: `http://localhost:8000` (Swagger docs: `http://localhost:8000/docs`)

### Run Both Frontend and Backend

1. **Start the backend with Docker**:
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

2. **Start the frontend** (in another terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```

- Backend API: `http://localhost:8000` (Swagger docs: `http://localhost:8000/docs`)
- Frontend: `http://localhost:4200`

## Development Setup

### Backend Only

```bash
cd backend
poetry install
poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Only

```bash
cd frontend
npm install
npm start
```

The frontend will be available at `http://localhost:4200` and will proxy API requests to the backend.

### Full Development Setup

1. **Start the backend** (in one terminal):
   ```bash
   cd backend
   poetry install
   poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend** (in another terminal):
   ```bash
   cd frontend
   npm install
   npm start
   ```

## API Documentation

Interactive API documentation is available at `http://localhost:8000/docs` when the backend is running.
