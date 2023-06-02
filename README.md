# cloud-run-fastapi-template

My take on building a template for running FastAPI on Google Cloud Run.

## Getting started

```bash
just init
```

## Commands

```bash
just --list
```

## Features

- FastAPI server
- Poetry for package management
- No docker image, use buildpacks instead
- Commands with just
- Linting with ruff
- Type checking with mypy
- Formatting with black
- Testing with pytest

## Future

- Load testing with locust
- Deploy to Cloud Run
- SQL database with SQLAlchemy
- SQL migrations with Alembic
- CI with CloudBuild
- CD with CloudBuild
- Replace buildpack with Dockerfile and Skaffold for local development
- Pre commit hooks for all CI checks
- CORS middleware
- Settings via environment variables and .env file
- More convention for organizing app code
