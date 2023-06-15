from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from template_app.api.v1 import router as api_v1_router
from template_app.settings import settings

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/v1")
