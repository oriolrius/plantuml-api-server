"""Test fixtures.

The PlantUML backend is mocked with ``respx`` so tests need no live server. Each
client runs the app's real lifespan (which probes the backend and reads its version)
against the mocked routes.
"""

from __future__ import annotations

import contextlib
import os

# Settings are read when the app module is imported, so configure the environment first.
os.environ.setdefault("PLANTUML_URL", "http://plantuml.test/plantuml")
os.environ.setdefault("PUBLIC_BASE_URL", "http://testserver")
os.environ.setdefault("EDITOR_PATH", "/editor")
os.environ.setdefault("LOG_JSON", "false")

import httpx  # noqa: E402
import pytest  # noqa: E402
import respx  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

SVG = b'<svg xmlns="http://www.w3.org/2000/svg"><text>ok</text></svg>'
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 40
VERSION_TXT = b"      PlantUML 1.2026.8 Git Commit abc Build Time 2026-09-05"


@contextlib.contextmanager
def _make(svg_side_effect=None, svg_error: str | None = None):
    with respx.mock(assert_all_called=False) as mock:
        mock.get(url__regex=r".*/plantuml/?$").mock(return_value=httpx.Response(200))
        mock.get(url__regex=r".*/txt/.*").mock(
            return_value=httpx.Response(
                200, content=VERSION_TXT, headers={"content-type": "text/plain"}
            )
        )
        svg_route = mock.get(url__regex=r".*/svg/.*")
        if svg_side_effect is not None:
            svg_route.mock(side_effect=svg_side_effect)
        elif svg_error is not None:
            svg_route.mock(
                return_value=httpx.Response(
                    200,
                    content=SVG,
                    headers={
                        "X-PlantUML-Diagram-Error": svg_error,
                        "X-PlantUML-Diagram-Error-Line": "2",
                    },
                )
            )
        else:
            svg_route.mock(
                return_value=httpx.Response(
                    200, content=SVG, headers={"content-type": "image/svg+xml"}
                )
            )
        mock.get(url__regex=r".*/png/.*").mock(
            return_value=httpx.Response(200, content=PNG, headers={"content-type": "image/png"})
        )
        from app.main import app

        with TestClient(app) as test_client:
            yield test_client


@pytest.fixture
def client():
    with _make() as c:
        yield c


@pytest.fixture
def make_client():
    """Factory yielding a client with customised backend behaviour."""
    return _make
