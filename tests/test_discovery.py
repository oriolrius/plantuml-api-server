"""Libraries, themes and examples discovery endpoints."""

from __future__ import annotations


def test_libraries_list(client) -> None:
    r = client.get("/api/v1/libraries")
    assert r.status_code == 200
    ids = {lib["id"] for lib in r.json()}
    assert {"awslib", "azure", "kubernetes", "c4", "gcp", "osa"} <= ids


def test_library_detail_and_404(client) -> None:
    assert client.get("/api/v1/libraries/awslib").status_code == 200
    assert client.get("/api/v1/libraries/does-not-exist").status_code == 404


def test_library_examples(client) -> None:
    r = client.get("/api/v1/libraries/awslib/examples")
    assert r.status_code == 200
    assert any(ex["id"] == "aws-architecture" for ex in r.json())


def test_library_icons(client) -> None:
    r = client.get("/api/v1/libraries/c4/icons")
    assert r.status_code == 200
    assert "categories" in r.json()


def test_themes(client) -> None:
    r = client.get("/api/v1/themes")
    assert r.status_code == 200
    names = {t["id"] for t in r.json()}
    assert "cerulean" in names
    assert client.get("/api/v1/themes/cerulean").status_code == 200
    assert client.get("/api/v1/themes/nope").status_code == 404


def test_examples(client) -> None:
    r = client.get("/api/v1/examples")
    assert r.status_code == 200
    assert len(r.json()) >= 10


def test_example_detail(client) -> None:
    r = client.get("/api/v1/examples/aws-architecture")
    assert r.status_code == 200
    body = r.json()
    assert body["encoded"]
    assert body["svg_url"].endswith(body["encoded"])
    assert body["api_request"]["method"] == "POST"
    assert client.get("/api/v1/examples/nope").status_code == 404
