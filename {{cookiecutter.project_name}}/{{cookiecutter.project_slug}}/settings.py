import os
from enum import StrEnum, auto
from typing import Literal

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Environment(StrEnum):
    """Context the application is running in."""

    DEV = auto()
    PROD = auto()


class Settings(BaseSettings):
    """Settings for the application.

    Fields are expected to be set in the environment or in a .env file.
    https://docs.pydantic.dev/latest/usage/pydantic_settings
    """

    env: Environment
    pg_async_dsn: str
    cors_origins: list[AnyHttpUrl | Literal["*"]]


def setup_settings() -> Settings:
    """Return the settings for the application.

    Note that environment variables take precedence over dotenv files. This is useful in
    production where configuration is passed in as environment variables and no dotenv
    file exists on the file system.
    """
    if os.environ.get("ENV") == "prod":
        return Settings(env="prod", _env_file=".env.prod")
    else:
        return Settings(env="dev", _env_file=".env.dev")


settings = setup_settings()
