"""Entrypoint for the FastAPI application."""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from {{cookiecutter.project_slug}}.api.deps import geo_company_authenticate
from {{cookiecutter.project_slug}}.api.v1 import router as api_v1_router
from {{cookiecutter.project_slug}}.logging import (
    LoggingMiddleware,
    ResponseValidationErrorLoggingMiddleware,
    configure_logging,
)
from {{cookiecutter.project_slug}}.settings import settings

logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
configure_logging()
app.add_middleware(LoggingMiddleware)
app.add_middleware(ResponseValidationErrorLoggingMiddleware)

# index router
index_router = APIRouter()


@index_router.get("/", include_in_schema=False)
async def index() -> PlainTextResponse:
    """Splash page text."""
    return PlainTextResponse("is your sheep genuine?")

app.include_router(index_router)

# API router
api_router = APIRouter(
    prefix="/geo_companies/{geo_company_id}", dependencies=[Depends(geo_company_authenticate)]
)
api_router.include_router(api_v1_router, prefix="/v1")

app.include_router(api_router)
