"""Curated example endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..config import Settings
from ..data.examples import EXAMPLE_INDEX, EXAMPLES
from ..deps import settings_dep
from ..encoding import encode as encode_text
from ..models import Example, ExampleSummary

router = APIRouter(tags=["Examples"])


class ExampleDetail(Example):
    """An example plus ready-to-use render/editor URLs and a sample API request."""

    encoded: str
    svg_url: str
    png_url: str
    editor_url: str
    api_request: dict


@router.get(
    "/examples",
    response_model=list[ExampleSummary],
    summary="List curated examples",
    description="A curated gallery covering UML, AWS, Azure, Kubernetes, C4, GCP, "
    "network/security, icon libraries, themes and PlantUML's non-UML diagram types.",
)
async def list_examples() -> list[ExampleSummary]:
    return [
        ExampleSummary(**ex.model_dump(include=set(ExampleSummary.model_fields))) for ex in EXAMPLES
    ]


@router.get(
    "/examples/{example_id}",
    response_model=ExampleDetail,
    summary="Get one example with render URLs",
    responses={404: {"description": "Unknown example."}},
)
async def get_example(example_id: str, settings: Settings = Depends(settings_dep)) -> ExampleDetail:
    ex = EXAMPLE_INDEX.get(example_id)
    if ex is None:
        raise HTTPException(status_code=404, detail=f"Unknown example '{example_id}'")
    token = encode_text(ex.source)
    base = settings.editor_base
    return ExampleDetail(
        **ex.model_dump(),
        encoded=token,
        svg_url=f"{base}/svg/{token}",
        png_url=f"{base}/png/{token}",
        editor_url=f"{base}/uml/{token}",
        api_request={
            "method": "POST",
            "url": f"{settings.public_base_url_clean}/api/v1/render",
            "body": {"source": ex.source, "format": "svg"},
        },
    )
