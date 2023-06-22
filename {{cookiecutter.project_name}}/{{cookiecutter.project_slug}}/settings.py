from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn
from pydantic.tools import parse_obj_as


class Settings(BaseSettings):
    # Typing pydantic fields complains with mypy. Use parse_obj_as to get around this
    # type warning while still validating input with pydantic.
    # https://github.com/pydantic/pydantic/issues/3143
    pg_dsn: PostgresDsn = parse_obj_as(
        PostgresDsn, "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    cors_origins: list[AnyHttpUrl] = [parse_obj_as(AnyHttpUrl, "http://localhost:8080")]


# Workaround for typing issue related to _env_file.
# https://github.com/pydantic/pydantic/issues/3072#issuecomment-1496386277
settings = Settings(_env_file=".env")  # type: ignore[call-arg]
