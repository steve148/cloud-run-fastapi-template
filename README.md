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
- Buildpacks for building container images
- Commands with just
- Linting with ruff
- Type checking with mypy
- Formatting with black
- Testing with pytest
- Pre commit hooks for CI checks
- SQL database with SQLAlchemy
- SQL migrations with Alembic
- Settings with pydantic via .env file

## Future

- Load testing with locust
- CI with CloudBuild
- CD with CloudBuild
- CORS middleware
- More convention for organizing app code
