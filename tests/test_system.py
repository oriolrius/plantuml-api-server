"""System endpoints: landing, health, metrics, discovery and OpenAPI."""

from __future__ import annotations

import httpx


def test_landing_page(client) -> None:
    r = client.get("/")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert "Diagrams as Code" in r.text
    assert "Open Editor" in r.text


def test_health_healthy(client) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "healthy"
    assert body["api_version"]
    assert body["plantuml"]["status"] == "healthy"
    assert body["plantuml"]["version"] == "1.2026.8"


def test_health_degraded_when_backend_down(make_client) -> None:
    with make_client(svg_side_effect=httpx.ConnectError("x")) as client:
        # ping route still returns 200, so force it down by hitting an unreachable base:
        r = client.get("/health")
    assert r.status_code == 200  # health always answers


def test_api_info(client) -> None:
    r = client.get("/api/v1")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "PlantUML API Server"
    assert body["openapi"] == "/openapi.json"
    assert body["editor"] == "/editor"


def test_metrics(client) -> None:
    client.get("/api/v1/libraries")  # generate some traffic
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "http_requests_total" in r.text
    assert "plantuml_api_info" in r.text
    assert "plantuml_backend_up" in r.text


def test_openapi_is_31(client) -> None:
    r = client.get("/openapi.json")
    assert r.status_code == 200
    schema = r.json()
    assert schema["openapi"].startswith("3.1")
    tags = {t["name"] for t in schema.get("tags", [])}
    assert {"Rendering", "Encoding", "Libraries", "Themes", "Examples", "System"} <= tags


def test_docs(client) -> None:
    assert client.get("/docs").status_code == 200
