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

## Background

> Context is everything. - Someone

The template is a self reflection of what is important in building a python web app on Google Cloud. What I write here should help explain the choices made within this repository.

First, I picked FastAPI for the framework of this project for a few reasons. Selfishly I picked it because it was something I wanted to learn more about. Playing with a new tool takes me back to that wonderful moment that I coded my first computer program. Objectively, I prefer tools which are good at fewer things and are easy to combine with other tools. Writing an endpoint with FastAPI feels more intuitive than the equal in vanilla Django or DRF.

Second, I set a goal for this template to work within the realm of Google Cloud. This template may be useful for a broader audience, but that's not the intent. I wanted a new project on GCP using this template to start with low maintenance overhead (eg. Procfile instead of Dockerfile). At the same time, if a project needed to pivot it shouldn't be too difficult to change the infrastructure (eg. deploy knative service to your own k8s cluster).

Finally, I wanted to make the development experience as smooth as possible. Development experience is a broad term, so I'll expand on how I interpret it. For one, it should be easy for someone new to join the project. All the common commands exist in the justfile with documentation. Next, when coding I don't want to think about minor details like import order or unnecessary f strings. Linters like ruff and mypy should be quick enough that I get feedback without getting in the way. These linters should also run at different stages of development. The template has the linters run on each commit, but in the future it should run on each merge and deploy. Finally, I wanted a dependency manager for explicitly listed required dependencies. I chose poetry over pipenv due to my lackluster experience with pipenv over the years.

## Future

- Load testing with locust
- CI with CloudBuild
- CD with CloudBuild
