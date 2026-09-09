"""Curated list of PlantUML themes.

PlantUML ships many built-in themes usable via ``!theme <name>``. This is the
well-known stable set; each entry carries a tiny preview source. The list can be
cross-checked against the running backend with ``plantuml -listthemes``.
"""

from __future__ import annotations

from ..models import Theme

_THEME_NAMES: list[str] = [
    "amiga",
    "aws-orange",
    "black-knight",
    "bluegray",
    "cerulean",
    "cerulean-outline",
    "crt-amber",
    "crt-green",
    "cyborg",
    "cyborg-outline",
    "hacker",
    "lightgray",
    "mars",
    "materia",
    "materia-outline",
    "metal",
    "minty",
    "mono",
    "plain",
    "reddress-darkblue",
    "reddress-darkgreen",
    "reddress-darkorange",
    "reddress-darkred",
    "reddress-lightblue",
    "reddress-lightgreen",
    "reddress-lightorange",
    "reddress-lightred",
    "sandstone",
    "silver",
    "sketchy",
    "sketchy-outline",
    "spacelab",
    "spacelab-white",
    "sunlust",
    "superhero",
    "superhero-outline",
    "toy",
    "united",
    "vibrant",
]


def _preview(name: str) -> str:
    return f"@startuml\n!theme {name}\nAlice -> Bob: Hello\nBob --> Alice: Hi!\n@enduml"


THEMES: list[Theme] = [
    Theme(id=name, name=name, preview_source=_preview(name)) for name in _THEME_NAMES
]

THEME_INDEX: dict[str, Theme] = {t.id: t for t in THEMES}
