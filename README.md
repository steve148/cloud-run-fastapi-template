# cloud-run-fastapi-template

My take on building a template for running FastAPI on Google Cloud Run.

## Local development

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
pack build --builder=gcr.io/buildpacks/builder sample-python
docker run -it -ePORT=8080 -p8080:8080 sample-python
```

## Features

- FastAPI server
- Poetry for package management
- No docker image, use buildpacks instead

## Future

- Linting with mypy and ruff
- Formatting with black
- Testing with pytest
- Load testing with locust
