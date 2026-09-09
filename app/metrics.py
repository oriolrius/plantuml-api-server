"""Prometheus metrics and the HTTP metrics middleware.

Only low-cardinality labels are used: HTTP method, the *matched route template*
(never the raw path), response status, and render format. Diagram source, encoded
tokens, client IPs and arbitrary URLs are NEVER used as labels.
"""

from __future__ import annotations

import time

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, Info, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests.",
    ["method", "route", "status"],
)
HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "route"],
)
RENDER_REQUESTS = Counter(
    "plantuml_render_requests_total",
    "Total diagram render requests.",
    ["format", "status"],
)
RENDER_DURATION = Histogram(
    "plantuml_render_duration_seconds",
    "Diagram render duration in seconds.",
    ["format"],
)
RENDER_ERRORS = Counter(
    "plantuml_render_errors_total",
    "Total diagram render errors.",
    ["format", "reason"],
)
BACKEND_UP = Gauge(
    "plantuml_backend_up",
    "1 if the PlantUML backend is reachable, else 0.",
)
BACKEND_REQUEST_DURATION = Histogram(
    "plantuml_backend_request_duration_seconds",
    "Duration of requests made to the PlantUML backend.",
)
API_INFO = Info(
    "plantuml_api",
    "Build/version information for the PlantUML API server.",
)


def normalized_route(request: Request) -> str:
    """The matched route template (low cardinality), or 'unmatched'."""
    route = request.scope.get("route")
    path = getattr(route, "path", None)
    if path:
        return str(path)
    return "unmatched"


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        route = normalized_route(request)
        # Don't record the /metrics scrape itself as request traffic noise.
        if route != "/metrics":
            HTTP_REQUESTS.labels(request.method, route, str(response.status_code)).inc()
            HTTP_REQUEST_DURATION.labels(request.method, route).observe(elapsed)
        return response


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
