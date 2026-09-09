"""Theme discovery endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..data.themes import THEME_INDEX, THEMES
from ..models import Theme

router = APIRouter(tags=["Themes"])


@router.get(
    "/themes",
    response_model=list[Theme],
    summary="List PlantUML themes",
    description="Discover the PlantUML themes supported by this service. Apply one with "
    "`!theme <name>` in your source, or via the `theme` field of /api/v1/render.",
)
async def list_themes() -> list[Theme]:
    return THEMES


@router.get(
    "/themes/{theme_id}",
    response_model=Theme,
    summary="Get a single theme",
    responses={404: {"description": "Unknown theme."}},
)
async def get_theme(theme_id: str) -> Theme:
    theme = THEME_INDEX.get(theme_id)
    if theme is None:
        raise HTTPException(status_code=404, detail=f"Unknown theme '{theme_id}'")
    return theme
