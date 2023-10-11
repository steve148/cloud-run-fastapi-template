"""Common dependencies which can be injected into an endpoint.

Currently only contains async db session, but might later be used for connecting shared
    functionality into endpoints (eg. authentication, common query params, etc.)
"""

from collections.abc import AsyncIterator
from typing import Annotated
from urllib.parse import urljoin

import aiohttp
from fastapi import Depends, HTTPException, Request
from fastapi.openapi.models import APIKey
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from collections.abc import Generator

from sqlalchemy.orm import Session

from {{cookiecutter.project_slug}}.db.session import AsyncSessionLocal
from {{cookiecutter.project_slug}}.settings import settings


async def get_async_db() -> AsyncIterator[AsyncSession]:
    """Get a SQLAlchemy async session for each request."""
    try:
        db = AsyncSessionLocal()
        yield db
    finally:
        await db.close()


AsyncDB = Annotated[AsyncSession, Depends(get_async_db)]


class GeoCompanyTokenAuth(HTTPBase):
    """Implementation of Authorization header validation that checks access for a geo_company_id."""

    def __init__(
        self,
    ) -> None:
        self.model = APIKey(**{"in": "header", "name": "Authorization"})
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        """Verify token is valid for given geo company id.

        Assumes geo company id can be found in the path params for all endpoints. Based on
        permissions.py and services/account.py files in perpetua-pybackend-common.
        https://github.com/perpetua1/perpetua-pybackend-common/blob/master/perpetua_pybackend_common/permissions.py
        https://github.com/perpetua1/perpetua-pybackend-common/blob/master/perpetua_pybackend_common/services/account.py
        """
        geo_company_id = request.path_params.get("geo_company_id")
        if not geo_company_id:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="No geo_company_id provided."
            )

        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")

        async with aiohttp.ClientSession() as session:
            url = urljoin(
                settings.account_service_host.unicode_string(),
                f"/account/v2/geo_companies/{geo_company_id}/check_auth_token/",
            )
            async with session.get(url=url, headers={"Authorization": authorization}) as resp:
                if resp.status != HTTP_200_OK:
                    raise HTTPException(status_code=resp.status)

        scheme, credentials = get_authorization_scheme_param(authorization)
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


geo_company_authenticate = GeoCompanyTokenAuth()
