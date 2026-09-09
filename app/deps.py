"""FastAPI dependencies."""

from __future__ import annotations

from fastapi import Request

from .config import Settings, get_settings
from .plantuml_client import PlantUMLClient


def get_client(request: Request) -> PlantUMLClient:
    return request.app.state.plantuml


def settings_dep() -> Settings:
    return get_settings()
