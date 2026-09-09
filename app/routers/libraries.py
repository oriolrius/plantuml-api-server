"""Library discovery endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..data.examples import EXAMPLES
from ..data.libraries import LIBRARIES, LIBRARY_INDEX
from ..models import Example, Library

router = APIRouter(tags=["Libraries"])


@router.get(
    "/libraries",
    response_model=list[Library],
    summary="List architecture / icon libraries",
    description="Discover the PlantUML standard-library icon and architecture libraries "
    "supported by this service (AWS, Azure, Kubernetes, C4, OSA, Material, GCP, …).",
)
async def list_libraries() -> list[Library]:
    return LIBRARIES


@router.get(
    "/libraries/{library}",
    response_model=Library,
    summary="Get a single library",
    responses={404: {"description": "Unknown library."}},
)
async def get_library(library: str) -> Library:
    lib = LIBRARY_INDEX.get(library)
    if lib is None:
        raise HTTPException(status_code=404, detail=f"Unknown library '{library}'")
    return lib


@router.get(
    "/libraries/{library}/examples",
    response_model=list[Example],
    summary="Examples that use a library",
    responses={404: {"description": "Unknown library."}},
)
async def library_examples(library: str) -> list[Example]:
    if library not in LIBRARY_INDEX:
        raise HTTPException(status_code=404, detail=f"Unknown library '{library}'")
    return [ex for ex in EXAMPLES if library in ex.libraries]


@router.get(
    "/libraries/{library}/icons",
    summary="Discover a library's icon categories",
    description="Returns the icon categories exposed by a library. Full per-icon sprite "
    "enumeration is best explored in the editor's autocomplete; the categories here give "
    "the top-level groupings.",
    responses={404: {"description": "Unknown library."}},
)
async def library_icons(library: str) -> dict:
    lib = LIBRARY_INDEX.get(library)
    if lib is None:
        raise HTTPException(status_code=404, detail=f"Unknown library '{library}'")
    return {
        "library": lib.id,
        "name": lib.name,
        "include": lib.include,
        "categories": lib.categories,
        "docs_url": lib.docs_url,
        "note": "Use the categories with the library include path, e.g. "
        f"`!include <{lib.id}/<Category>/<Icon>>`. Explore full icon names in the editor.",
    }
