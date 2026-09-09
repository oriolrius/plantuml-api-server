"""Diagram rendering endpoints."""

from __future__ import annotations

import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from ..config import Settings
from ..data.libraries import INCLUDE_LINES
from ..deps import get_client, settings_dep
from ..metrics import RENDER_DURATION, RENDER_ERRORS, RENDER_REQUESTS
from ..models import FORMAT_MEDIA, ErrorResponse, RenderRequest
from ..plantuml_client import PlantUMLClient, PlantUMLError

router = APIRouter(tags=["Rendering"])


def build_source(req: RenderRequest) -> str:
    """Apply optional theme/library conveniences without hiding raw PlantUML.

    Injected lines are placed immediately after the first ``@start…`` directive so
    the user's own source is preserved verbatim.
    """
    inject: list[str] = []
    if req.libraries:
        for lib in req.libraries:
            inject.extend(INCLUDE_LINES.get(lib, []))
    if req.theme:
        inject.append(f"!theme {req.theme}")
    if not inject:
        return req.source

    lines = req.source.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith("@start"):
            return "\n".join(lines[: i + 1] + inject + lines[i + 1 :])
    return "\n".join(inject + lines)


@router.post(
    "/render",
    summary="Render a PlantUML diagram",
    description="Render PlantUML source to the requested format (PNG, SVG, TXT, PDF, …). "
    "Returns the native media type — binary responses are streamed, not base64-encoded. "
    "Submit normal PlantUML source; `theme` and `libraries` are optional conveniences.",
    responses={
        200: {
            "content": {
                "image/png": {},
                "image/svg+xml": {},
                "text/plain": {},
                "application/pdf": {},
            },
            "description": "The rendered diagram in the requested media type.",
        },
        422: {"model": ErrorResponse, "description": "Invalid PlantUML source."},
        503: {"model": ErrorResponse, "description": "PlantUML backend unavailable."},
        504: {"model": ErrorResponse, "description": "PlantUML render timed out."},
    },
)
async def render(
    req: RenderRequest,
    client: PlantUMLClient = Depends(get_client),
    settings: Settings = Depends(settings_dep),
) -> Response:
    if len(req.source.encode("utf-8")) > settings.max_source_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Diagram source exceeds the {settings.max_source_bytes} byte limit.",
        )
    fmt_token, media = FORMAT_MEDIA[req.format]
    source = build_source(req)
    start = time.perf_counter()
    try:
        content, _ctype = await client.render(source, fmt_token, req.index)
    except PlantUMLError as exc:
        RENDER_REQUESTS.labels(req.format.value, "error").inc()
        RENDER_ERRORS.labels(req.format.value, type(exc).__name__).inc()
        raise HTTPException(status_code=exc.status, detail=str(exc)) from exc
    RENDER_REQUESTS.labels(req.format.value, "success").inc()
    RENDER_DURATION.labels(req.format.value).observe(time.perf_counter() - start)
    return Response(content=content, media_type=media)
