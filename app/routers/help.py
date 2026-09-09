"""Help / documentation pages, rendered from Markdown with the site's look & feel."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse

from .. import __version__
from ..config import Settings
from ..deps import settings_dep
from ..help import nav_by_category, render_page

router = APIRouter()


def _editor_path(settings: Settings) -> str:
    return "/" + settings.editor_path.strip("/")


@router.get("/help", include_in_schema=False)
async def help_index(request: Request, settings: Settings = Depends(settings_dep)) -> HTMLResponse:
    editor_path = _editor_path(settings)
    page = render_page("index", editor_path) or {
        "title": "Documentation",
        "category": "Overview",
        "content": "<p>Select a topic from the navigation.</p>",
        "toc": "",
        "diagram_count": 0,
    }
    return request.app.state.templates.TemplateResponse(
        request,
        "help.html",
        {"nav": nav_by_category(), "page": page, "active": "index", "version": __version__},
    )


@router.get("/help/{slug}", include_in_schema=False)
async def help_page(
    slug: str, request: Request, settings: Settings = Depends(settings_dep)
) -> HTMLResponse:
    page = render_page(slug, _editor_path(settings))
    if page is None:
        raise HTTPException(status_code=404, detail=f"No help page '{slug}'")
    return request.app.state.templates.TemplateResponse(
        request,
        "help.html",
        {"nav": nav_by_category(), "page": page, "active": slug, "version": __version__},
    )
