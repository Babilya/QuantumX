from __future__ import annotations

import logging
import os
from typing import Any
import sentry_sdk
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response


REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'HTTP request latency', ['endpoint'])


def setup_logging() -> None:
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    root = logging.getLogger()
    if not root.handlers:
        root.addHandler(handler)
    root.setLevel(logging.INFO)


def setup_sentry() -> None:
    dsn = os.getenv('SENTRY_DSN')
    if dsn:
        sentry_sdk.init(dsn=dsn, traces_sample_rate=0.1)


async def metrics_middleware(request: Request, call_next):
    endpoint = request.url.path
    with REQUEST_LATENCY.labels(endpoint=endpoint).time():
        response: Response = await call_next(request)
    try:
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=str(response.status_code)).inc()
    except Exception:
        pass
    return response


def metrics_response() -> Response:
    data = generate_latest()  # type: ignore[arg-type]
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

