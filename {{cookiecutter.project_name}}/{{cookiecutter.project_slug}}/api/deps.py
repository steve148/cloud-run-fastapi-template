from collections.abc import Generator

from sqlalchemy.orm import Session

from {{cookiecutter.project_slug}}.db import SessionLocal


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
