"""Resource-directory resolution that works in both the installed (app/<name>) and
source (repo/<name>) layouts."""

from __future__ import annotations

from pathlib import Path

_PKG = Path(__file__).resolve().parent


def resource_dir(name: str) -> Path:
    installed = _PKG / name
    return installed if installed.exists() else _PKG.parent / name
