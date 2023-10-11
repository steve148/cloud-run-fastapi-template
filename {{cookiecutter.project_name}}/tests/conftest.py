import asyncio
import os
from asyncio import AbstractEventLoop
from collections.abc import AsyncIterator, Iterator

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from {{cookiecutter.project_slug}}.api.deps import geo_company_authenticate, get_async_db
from {{cookiecutter.project_slug}}.db.base_class import Base
from {{cookiecutter.project_slug}}.main import app


@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest) -> Iterator[AbstractEventLoop]:
    """Create instance of event loop for all tests.

    For db_engine and db_session fixtures to be session scoped, the event loop needs to
    match that scope. This fixture overwrites the default function scoped event loop
    that is provided by the pytest-asyncio plugin.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_engine() -> AsyncEngine:
    """Create a engine for connecting to the test database.

    You likely don't need to use this fixture directly. Instead, use the db fixture.
    """
    return create_async_engine(
        os.environ.get(
            "TESTING_PG_ASYNC_DSN",
            "postgresql+asyncpg://postgres:postgres@localhost:45432/postgres",
        )
    )


@pytest.fixture(scope="session")
async def db_session(db_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """Create required tables and an async session for querying the test database.

    You likely don't need to use this fixture directly. Instead, use the db fixture.
    """
    async with db_engine.begin() as conn:
        schemas = {table.schema for _, table in Base.metadata.tables.items()}
        for schema in schemas:
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(bind=db_engine) as session:
        yield session


@pytest.fixture
async def db(db_session: AsyncSession) -> AsyncIterator[AsyncSession]:
    """Create a transactional test database session.

    This is likely the fixture you need when setting up data in the database. Rolling
    back the transaction should be much faster than clearing the database before / after
    each test case.

    https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """
    async with db_session.begin():
        yield db_session
        await db_session.rollback()


@pytest.fixture
async def client(db: AsyncSession) -> AsyncIterator[AsyncClient]:
    # 2023-08-10 - Don't worry about validating auth token during testing.
    app.dependency_overrides[geo_company_authenticate] = lambda: True
    app.dependency_overrides[get_async_db] = lambda: db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
