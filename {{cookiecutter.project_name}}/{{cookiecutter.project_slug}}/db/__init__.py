from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from {{cookiecutter.project_slug}}.settings import settings

app = FastAPI()


engine = create_engine(settings.pg_dsn, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
