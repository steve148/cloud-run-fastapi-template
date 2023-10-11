"""Utilities for configuring logging for local development or on Google Cloud Run.

References
----------
Google Cloud Logging Python Client
https://github.com/googleapis/python-logging/tree/main

Examples
--------
Below are some examples of calling the logger and what you can expect the GCP log record to be. Each
    example includes the function call and the relevant fields on the resulting GCP log record.

Text payload log record.
>>> logger.info("a text payload")

`{"textPayload": "a text payload"}`

Text payload log record via dictionary.
>>> logger.info({"message": "another text payload"})

`{"textPayload": "another text payload"}`

JSON payload log record.
>>> logger.info({"message": "a json payload", "foo": "bar"})

`{"jsonPayload": {"foo": "bar", "message": "a json payload"}}`

JSON payload log record via extra fields.
>>> logger.info("a json payload via extra fields", extra={"json_fields": {"foo": "bar"}})

`{"jsonPayload": {"foo": "bar", "message": "a json payload via extra fields"}}`
"""

import logging
import os
import re
import sys
from contextvars import ContextVar
from logging import LogRecord
from typing import Any

from fastapi.exceptions import ResponseValidationError
from google.cloud.logging import Client
from google.cloud.logging_v2.handlers import CloudLoggingFilter, setup_logging
from google.cloud.logging_v2.handlers.handlers import EXCLUDED_LOGGER_DEFAULTS
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

cloud_trace_context = ContextVar("cloud_trace_context", default="")
http_request_context: ContextVar[dict[str, Any]] = ContextVar(
    "http_request_context", default={}
)


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure logging for FastAPI depending on environment."""
    if os.environ.get("K_REVISION"):
        configure_logging_cloud_run()
    else:
        configure_logging_local()


def configure_logging_cloud_run() -> None:
    """Set up logging when running app on Cloud Run.

    Function accomplishes the following:
        * Use structured logs handler to parse multi line messages as a single record in GCP.
        * Add a filter to inject trace and http request info into the logs.

    Warnings
    --------
    This function should only be called when running on Cloud Run. If run outside of GCP, logs will
    still be collected and sent to GCP.

    Notes
    -----
    Ideally we'd use the basic setup for google python cloud logging. However, the basic setup only
    handles injecting trace and http request information into the logs for django and flask apps.
    Based on the issue linked below it seems unlikely they'll add support for either. If that
    changes, we should switch to using the basic setup.

    References
    ----------
    GCP documentation showing basic set up of logging
        https://cloud.google.com/logging/docs/setup/python
    Python logging issue for supporting Starlette trace injection
        https://github.com/googleapis/python-logging/issues/505
    """
    client = Client()  # type: ignore[no-untyped-call]

    handler = client.get_default_handler()  # type: ignore[no-untyped-call]
    handler.filters = []
    handler.addFilter(GoogleCloudLogFilter(project=client.project))  # type: ignore[no-untyped-call]

    setup_logging(  # type: ignore[no-untyped-call]
        handler,
        log_level=logging.INFO,
        excluded_loggers=EXCLUDED_LOGGER_DEFAULTS,
    )


def configure_logging_local() -> None:
    """Configure logging when running app locally."""
    logging.basicConfig(level=logging.INFO)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware required to customize logging to GCP."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Store GCP trace ID in context for logging."""
        if "x-cloud-trace-context" in request.headers:
            cloud_trace_context.set(request.headers["x-cloud-trace-context"])

        http_request: dict[str, Any] = {
            "requestMethod": request.method,
            "requestUrl": request.url.path,
            "requestSize": sys.getsizeof(request),
            "protocol": request.url.scheme,
        }

        if request.client:
            http_request["remoteIp"] = request.client.host

        if "referrer" in request.headers:
            http_request["referrer"] = request.headers.get("referrer")

        if "user-agent" in request.headers:
            http_request["userAgent"] = request.headers.get("user-agent")

        http_request_context.set(http_request)

        return await call_next(request)


class GoogleCloudLogFilter(CloudLoggingFilter):
    """Logging filter for integration with Google Cloud Logging."""

    def filter(self, record: LogRecord) -> bool:
        """Attach extra information to logs sent to GCP."""
        http_request = http_request_context.get()
        trace = cloud_trace_context.get()

        if trace:
            split_header = trace.split("/", 1)

            record.trace = f"projects/{self.project}/traces/{split_header[0]}"

            header_suffix = split_header[1]
            record.span_id = re.findall(r"^\w+", header_suffix)[0]

        if http_request:
            record.http_request = http_request

        super().filter(record)  # type: ignore [no-untyped-call]
        return True


class ResponseValidationErrorLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for custom logging of ResponseValidationError exceptions."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Log ResponseValidationErrors using the app logger.

        Prevent bubbling these errors to Uvicorn in production to avoid multi-line logs in
        CloudLogging, etc.
        """
        try:
            return await call_next(request)
        except ResponseValidationError as exc:
            logger.exception(exc)
            return Response(
                "Internal Server Error", status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
