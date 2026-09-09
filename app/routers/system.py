"""System endpoints: landing page, health, metrics and API discovery."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, Response

from .. import __version__
from ..config import Settings
from ..data.examples import EXAMPLE_INDEX, EXAMPLES
from ..data.libraries import LIBRARIES
from ..deps import get_client, settings_dep
from ..encoding import encode
from ..metrics import BACKEND_UP, metrics_response
from ..models import ApiInfo, BackendHealth, HealthResponse

router = APIRouter()

#: Examples rendered live on the landing page.
_FEATURED = ["sequence-basic", "aws-architecture", "kubernetes-architecture", "c4-container"]


@router.get("/", include_in_schema=False)
async def landing(request: Request, settings: Settings = Depends(settings_dep)) -> HTMLResponse:
    client = get_client(request)
    templates = request.app.state.templates
    editor_path = "/" + settings.editor_path.strip("/")
    featured = [
        {"ex": EXAMPLE_INDEX[i], "encoded": encode(EXAMPLE_INDEX[i].source)}
        for i in _FEATURED
        if i in EXAMPLE_INDEX
    ]
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "version": __version__,
            "plantuml_version": client.version,
            "editor_path": editor_path,
            "examples": EXAMPLES,
            "libraries": LIBRARIES,
            "featured": featured,
        },
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health check",
    description="Reports overall service health plus the PlantUML backend status and "
    "version. Always returns HTTP 200 so simple probes can read the JSON body.",
)
async def health(request: Request) -> HealthResponse:
    client = get_client(request)
    up = await client.ping()
    BACKEND_UP.set(1 if up else 0)
    version = client.version
    if up and version is None:
        version = await client.fetch_version()
    return HealthResponse(
        status="healthy" if up else "degraded",
        api_version=__version__,
        plantuml=BackendHealth(status="healthy" if up else "unhealthy", version=version),
    )


@router.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return metrics_response()


@router.get(
    "/api/v1",
    response_model=ApiInfo,
    tags=["System"],
    summary="API discovery",
    description="Service metadata and links to the API's main entry points.",
)
async def api_info(request: Request) -> ApiInfo:
    client = get_client(request)
    return ApiInfo(
        service="PlantUML API Server",
        api_version=__version__,
        plantuml_version=client.version,
        openapi="/openapi.json",
        docs="/docs",
        editor="/editor",
        health="/health",
        metrics="/metrics",
        libraries="/api/v1/libraries",
        themes="/api/v1/themes",
        examples="/api/v1/examples",
    )
