"""Help / documentation rendering tests."""

from __future__ import annotations

import pytest

from app.encoding import encode
from app.help import _parse_front_matter, _puml_figure, list_pages


def test_front_matter_parsing() -> None:
    meta, body = _parse_front_matter(
        "---\ntitle: Sequence\norder: 100\ncategory: Diagram Types\n---\n# Hi\n"
    )
    assert meta["title"] == "Sequence"
    assert meta["order"] == "100"
    assert body.startswith("# Hi")


def test_puml_figure_has_live_preview() -> None:
    src = "@startuml\nA -> B\n@enduml"
    fig = _puml_figure(src, "/editor")
    assert 'figure class="puml"' in fig
    assert f"/editor/svg/{encode(src)}" in fig
    assert f"/editor/uml/{encode(src)}" in fig


def test_help_index(client) -> None:
    r = client.get("/help")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    assert "help-sidebar" in r.text


def test_help_unknown_page_404(client) -> None:
    assert client.get("/help/no-such-page-xyz").status_code == 404


def test_help_real_page_renders(client) -> None:
    pages = [p for p in list_pages() if p.slug != "index"]
    if not pages:
        pytest.skip("no help pages generated yet")
    r = client.get(f"/help/{pages[0].slug}")
    assert r.status_code == 200
    assert "help-content" in r.text
