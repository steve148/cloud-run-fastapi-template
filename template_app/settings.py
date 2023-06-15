from pydantic import BaseSettings, PostgresDsn

dev_pg_dsn = "postgresql://postgres:postgres@localhost:5432/postgres"


class Settings(BaseSettings):
    # Typing PostgresDsn is not supported, see issue below.
    # https://github.com/pydantic/pydantic/issues/1490
    pg_dsn: PostgresDsn = PostgresDsn(
        "postgresql://postgres:postgres@localhost:5432/postgres"
    )


# Workaround for typing issue related to _env_file.
# https://github.com/pydantic/pydantic/issues/3072#issuecomment-1496386277
settings = Settings(_env_file=".env")  # type: ignore[call-arg]
