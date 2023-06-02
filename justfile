# List all available commands.
default:
    just --list

# Initialize the project.
init: init-setup install

# Install all required tools.
init-setup:
    pyenv install --skip-existing < .python-version
    pyenv local
    pip install --upgrade pip
    pip install poetry

# Install python dependencies.
install:
    poetry install

# Run the application locally.
run-local:
    poetry run uvicorn template_app.main:app --port 8080 --reload

# Run the application within local docker container.
run-local-docker:
    poetry export -f requirements.txt --output requirements.txt --without-hashes
    pack build --builder=gcr.io/buildpacks/builder template-app
    docker run -it -ePORT=8080 -p8080:8080 template-app

# Push new version of service to Cloud run.
deploy:
    gcloud run deploy --source . --allow-unauthenticated

# Run all checks against code.
check: format lint type-check

# Format code with black.
format:
    poetry run black .

# Lint and fix code with ruff.
lint:
    poetry run ruff check --fix .

# Type check with mypy.
type-check:
    poetry run mypy .

# Run all tests.
test:
    poetry run pytest
