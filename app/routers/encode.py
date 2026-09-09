"""PlantUML text-encoding endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from ..config import Settings
from ..deps import settings_dep
from ..encoding import decode as decode_text
from ..encoding import encode as encode_text
from ..models import DecodeRequest, DecodeResponse, EncodeRequest, EncodeResponse, ErrorResponse

router = APIRouter(tags=["Encoding"])


@router.post(
    "/encode",
    response_model=EncodeResponse,
    summary="Encode PlantUML source",
    description="Encode PlantUML source into the URL-safe token used by the PlantUML "
    "Server, and return ready-to-use editor / PNG / SVG / TXT URLs.",
)
async def encode(req: EncodeRequest, settings: Settings = Depends(settings_dep)) -> EncodeResponse:
    token = encode_text(req.source)
    base = settings.editor_base
    return EncodeResponse(
        encoded=token,
        editor_url=f"{base}/uml/{token}",
        png_url=f"{base}/png/{token}",
        svg_url=f"{base}/svg/{token}",
        txt_url=f"{base}/txt/{token}",
    )


@router.post(
    "/decode",
    response_model=DecodeResponse,
    summary="Decode a PlantUML token",
    description="Decode a PlantUML URL token (deflate, `~1` or `~h` hex forms) back "
    "into diagram source.",
    responses={422: {"model": ErrorResponse, "description": "Malformed token."}},
)
async def decode(req: DecodeRequest) -> DecodeResponse:
    try:
        return DecodeResponse(source=decode_text(req.encoded))
    except Exception as exc:  # noqa: BLE001 — any decode failure is a client error
        raise HTTPException(status_code=422, detail=f"Could not decode token: {exc}") from exc
