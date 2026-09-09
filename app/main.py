"""FastAPI application factory for the PlantUML API Server."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import __version__
from .config import get_settings
from .logging import configure_logging, get_logger
from .metrics import API_INFO, BACKEND_UP, MetricsMiddleware
from .models import ErrorResponse
from .paths import resource_dir
from .plantuml_client import PlantUMLClient, PlantUMLError
from .routers import encode, examples, help, libraries, render, system, themes

log = get_logger()


DESCRIPTION = """
**Diagrams as Code — UML, Cloud Architecture, Kubernetes, C4 and more.**

A modern REST API and developer portal around the official **PlantUML Server**. It does
not reinvent PlantUML — it exposes it elegantly: render diagrams to PNG/SVG/TXT/PDF,
encode/decode PlantUML URLs, and discover the architecture icon libraries (AWS, Azure,
Kubernetes, C4, GCP, OSA, Material and more), themes and curated examples.

You can always submit **plain PlantUML source** — the `theme` and `libraries` options are
conveniences, never a replacement for PlantUML syntax.

* Interactive **editor**: [`/editor`](/editor)
* This documentation: [`/docs`](/docs) · OpenAPI schema: [`/openapi.json`](/openapi.json)
* Health: [`/health`](/health) · Prometheus metrics: [`/metrics`](/metrics)
""".strip()

TAGS_METADATA = [
    {"name": "Rendering", "description": "Render PlantUML source to images and text."},
    {"name": "Encoding", "description": "Encode/decode PlantUML URL tokens."},
    {"name": "Libraries", "description": "Discover architecture & icon libraries."},
    {"name": "Themes", "description": "Discover PlantUML themes."},
    {"name": "Examples", "description": "Curated, ready-to-render example gallery."},
    {"name": "System", "description": "Health, metrics and API discovery."},
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level, settings.log_json)
    client = PlantUMLClient(
        settings.plantuml_url_clean, settings.connect_timeout, settings.request_timeout
    )
    app.state.plantuml = client
    try:
        up = await client.ping()
        BACKEND_UP.set(1 if up else 0)
        if up:
            await client.fetch_version()
    except Exception as exc:  # noqa: BLE001 — never block boot on backend problems
        BACKEND_UP.set(0)
        log.warning("backend probe failed at startup", extra={"extra": {"err": str(exc)}})
    API_INFO.info({"api_version": __version__, "plantuml_version": client.version or "unknown"})
    log.info(
        "started",
        extra={"extra": {"api_version": __version__, "plantuml_version": client.version}},
    )
    yield
    await client.aclose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="PlantUML API Server",
        version=__version__,
        description=DESCRIPTION,
        openapi_tags=TAGS_METADATA,
        license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(MetricsMiddleware)
    app.state.templates = Jinja2Templates(directory=str(resource_dir("templates")))

    static_dir = resource_dir("static")
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # System routes (root: /, /health, /metrics, /api/v1)
    app.include_router(system.router)
    app.include_router(help.router)
    # Versioned API
    for r in (render.router, encode.router, libraries.router, themes.router, examples.router):
        app.include_router(r, prefix="/api/v1")

    @app.exception_handler(StarletteHTTPException)
    async def _http_exc(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        try:
            title = HTTPStatus(exc.status_code).phrase
        except ValueError:
            title = "Error"
        body = ErrorResponse(title=title, status=exc.status_code, detail=str(exc.detail))
        return JSONResponse(status_code=exc.status_code, content=body.model_dump())

    @app.exception_handler(PlantUMLError)
    async def _puml_exc(request: Request, exc: PlantUMLError) -> JSONResponse:
        body = ErrorResponse(title="PlantUML backend error", status=exc.status, detail=str(exc))
        return JSONResponse(status_code=exc.status, content=body.model_dump())

    return app


app = create_app()
