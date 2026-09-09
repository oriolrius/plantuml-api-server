"""Render the Markdown help docs (``help/*.md``) to HTML.

Each ```plantuml fenced block is turned into a live, on-page rendered preview (an
``<img>`` pointing at the editor's SVG endpoint) plus links to open it in the editor.
Front-matter (``title`` / ``order`` / ``category`` between ``---`` fences) drives the
navigation.
"""

from __future__ import annotations

import html as _html
import re
from dataclasses import dataclass
from functools import lru_cache

import markdown

from .encoding import encode
from .paths import resource_dir

HELP_DIR = resource_dir("help")

_FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
_PUML_RE = re.compile(r"```plantuml\n(.*?)\n```", re.DOTALL)
_SLUG_RE = re.compile(r"[a-z0-9][a-z0-9\-]*")


@dataclass(frozen=True)
class HelpPage:
    slug: str
    title: str
    order: int
    category: str


def _parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    meta: dict[str, str] = {}
    m = _FM_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
        text = text[m.end() :]
    return meta, text


@lru_cache(maxsize=1)
def list_pages() -> tuple[HelpPage, ...]:
    """All help pages, ordered. Cached (docs are static in the image)."""
    pages: list[HelpPage] = []
    if HELP_DIR.exists():
        for path in HELP_DIR.glob("*.md"):
            meta, _ = _parse_front_matter(path.read_text(encoding="utf-8"))
            try:
                order = int(meta.get("order", "999"))
            except ValueError:
                order = 999
            pages.append(
                HelpPage(
                    slug=path.stem,
                    title=meta.get("title", path.stem.replace("-", " ").title()),
                    order=order,
                    category=meta.get("category", "Docs"),
                )
            )
    pages.sort(key=lambda p: (p.order, p.title))
    return tuple(pages)


def nav_by_category() -> list[tuple[str, list[HelpPage]]]:
    """Pages grouped by category, both categories and pages in order."""
    groups: dict[str, list[HelpPage]] = {}
    for page in list_pages():
        groups.setdefault(page.category, []).append(page)
    # category order = min order within the category
    return sorted(groups.items(), key=lambda kv: min(p.order for p in kv[1]))


def _new_md() -> markdown.Markdown:
    return markdown.Markdown(
        extensions=["fenced_code", "tables", "toc", "attr_list", "sane_lists", "admonition"],
        output_format="html",
    )


def _puml_figure(src: str, editor_path: str) -> str:
    enc = encode(src)
    esc = _html.escape(src)
    uml = f"{editor_path}/uml/{enc}"
    png = f"{editor_path}/png/{enc}"
    svg = f"{editor_path}/svg/{enc}"
    links = (
        f'<a href="{uml}" target="_blank" rel="noopener">Open in editor ↗</a>'
        f' · <a href="{png}" target="_blank" rel="noopener">PNG</a>'
        f' · <a href="{svg}" target="_blank" rel="noopener">SVG</a>'
    )
    return (
        '<figure class="puml">'
        f'<pre class="puml-src"><code>{esc}</code></pre>'
        f'<div class="puml-render"><img loading="lazy" src="{svg}" alt="Rendered diagram"></div>'
        f"<figcaption>{links}</figcaption>"
        "</figure>"
    )


def render_page(slug: str, editor_path: str) -> dict | None:
    """Render one help page to HTML. Returns None for unknown/invalid slugs."""
    if not _SLUG_RE.fullmatch(slug):
        return None
    path = HELP_DIR / f"{slug}.md"
    if not path.is_file():
        return None

    meta, body = _parse_front_matter(path.read_text(encoding="utf-8"))

    blocks: list[str] = []

    def _stash(m: re.Match[str]) -> str:
        blocks.append(m.group(1))
        return f"\n\nXPUMLBLOCK{len(blocks) - 1}X\n\n"

    body = _PUML_RE.sub(_stash, body)
    md = _new_md()
    content = md.convert(body)
    for i, src in enumerate(blocks):
        fig = _puml_figure(src, editor_path)
        token = f"XPUMLBLOCK{i}X"
        content = content.replace(f"<p>{token}</p>", fig).replace(token, fig)

    return {
        "title": meta.get("title", slug),
        "category": meta.get("category", "Docs"),
        "content": content,
        "toc": getattr(md, "toc", ""),
        "diagram_count": len(blocks),
    }
