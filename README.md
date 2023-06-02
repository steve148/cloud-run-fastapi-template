# cloud-run-fastapi-template

My take on building a template for running FastAPI on Google Cloud Run.

## Local development

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
pack build --builder=gcr.io/buildpacks/builder sample-python
docker run -it -ePORT=8080 -p8080:8080 sample-python
```

## Linting

```bash
mypy .
black .
ruff check --fix .
```

## Features

- FastAPI server
- Poetry for package management
- No docker image, use buildpacks instead
- Linting with ruff
- Type checking with mypy
- Formatting with black
- Testing with pytest

## Future

- Load testing with locust
- Deploy to Clod Run
- SQL database with SQLAlchemy
- SQL migrations with Alembic
- CI with CloudBuild
- CD with CloudBuild
- Replace buildpack with Dockerfile and Skaffold for local development
- Pre commit hooks for all CI checks
- CORS middleware
- Settings via environment variables and .env file
- More convention for organizing app code
