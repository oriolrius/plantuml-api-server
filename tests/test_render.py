"""Rendering endpoint tests (backend mocked)."""

from __future__ import annotations

import httpx

SEQ = "@startuml\nAlice -> Bob: Hello\n@enduml"


def test_render_svg(client) -> None:
    r = client.post("/api/v1/render", json={"source": SEQ, "format": "svg"})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("image/svg+xml")
    assert r.content.startswith(b"<svg")


def test_render_png(client) -> None:
    r = client.post("/api/v1/render", json={"source": SEQ, "format": "png"})
    assert r.status_code == 200
    assert r.headers["content-type"] == "image/png"
    assert r.content.startswith(b"\x89PNG")


def test_render_with_theme_and_library(client) -> None:
    r = client.post(
        "/api/v1/render",
        json={"source": SEQ, "format": "svg", "theme": "cerulean", "libraries": ["awslib"]},
    )
    assert r.status_code == 200


def test_render_invalid_source(make_client) -> None:
    with make_client(svg_error="Syntax Error?") as client:
        r = client.post("/api/v1/render", json={"source": "@startuml\nnope(", "format": "svg"})
    assert r.status_code == 422
    assert "Syntax Error" in r.json()["detail"]


def test_render_backend_unavailable(make_client) -> None:
    with make_client(svg_side_effect=httpx.ConnectError("refused")) as client:
        r = client.post("/api/v1/render", json={"source": SEQ, "format": "svg"})
    assert r.status_code == 503


def test_render_timeout(make_client) -> None:
    with make_client(svg_side_effect=httpx.ReadTimeout("slow")) as client:
        r = client.post("/api/v1/render", json={"source": SEQ, "format": "svg"})
    assert r.status_code == 504


def test_render_too_large(client) -> None:
    r = client.post("/api/v1/render", json={"source": "x" * 100_001, "format": "svg"})
    assert r.status_code == 413


def test_render_requires_source(client) -> None:
    r = client.post("/api/v1/render", json={"format": "svg"})
    assert r.status_code == 422
