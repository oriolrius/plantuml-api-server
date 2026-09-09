"""Pydantic models and the API's typed request/response contracts."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class RenderFormat(StrEnum):
    """Output formats the API exposes (a subset the PlantUML Server supports)."""

    png = "png"
    svg = "svg"
    txt = "txt"
    pdf = "pdf"
    eps = "eps"


#: Format -> (server path token, response media type).
FORMAT_MEDIA: dict[RenderFormat, tuple[str, str]] = {
    RenderFormat.png: ("png", "image/png"),
    RenderFormat.svg: ("svg", "image/svg+xml"),
    RenderFormat.txt: ("txt", "text/plain; charset=utf-8"),
    RenderFormat.pdf: ("pdf", "application/pdf"),
    RenderFormat.eps: ("eps", "application/postscript"),
}


class RenderRequest(BaseModel):
    source: str = Field(
        ...,
        min_length=1,
        description="PlantUML source. Submit normal PlantUML — `@startuml … @enduml`.",
    )
    format: RenderFormat = Field(default=RenderFormat.svg, description="Desired output format.")
    theme: str | None = Field(
        default=None,
        description="Optional PlantUML theme name, injected as `!theme <name>`.",
    )
    libraries: list[str] | None = Field(
        default=None,
        description="Optional known library ids (see /api/v1/libraries) whose `!include` "
        "lines are injected for convenience. You can always include them yourself instead.",
    )
    index: int | None = Field(
        default=None,
        ge=0,
        description="Diagram index for a source containing multiple `@startuml` blocks.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "source": "@startuml\nAlice -> Bob: Hello\nBob --> Alice: Hi!\n@enduml",
                    "format": "svg",
                },
                {
                    "source": "@startuml\nComponent [Web] as web\n@enduml",
                    "format": "png",
                    "theme": "cerulean",
                    "libraries": ["awslib"],
                },
            ]
        }
    }


class EncodeRequest(BaseModel):
    source: str = Field(..., min_length=1, description="PlantUML source to encode.")

    model_config = {
        "json_schema_extra": {"examples": [{"source": "@startuml\nAlice -> Bob\n@enduml"}]}
    }


class EncodeResponse(BaseModel):
    encoded: str = Field(..., description="PlantUML URL-safe encoded token.")
    editor_url: str
    png_url: str
    svg_url: str
    txt_url: str


class DecodeRequest(BaseModel):
    encoded: str = Field(..., min_length=1, description="PlantUML encoded token to decode.")

    model_config = {
        "json_schema_extra": {"examples": [{"encoded": "SyfFKj2rKt3CoKnELR1Io4ZDoSa70000"}]}
    }


class DecodeResponse(BaseModel):
    source: str


class BackendHealth(BaseModel):
    status: str = Field(..., description="`healthy` | `unhealthy`.")
    version: str | None = Field(default=None, description="Running PlantUML version.")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall service status: `healthy` | `degraded`.")
    api_version: str
    plantuml: BackendHealth


class ApiInfo(BaseModel):
    service: str
    api_version: str
    plantuml_version: str | None
    openapi: str
    docs: str
    editor: str
    health: str
    metrics: str
    libraries: str
    themes: str
    examples: str


class LibraryCategory(BaseModel):
    id: str
    name: str


class Library(BaseModel):
    id: str
    name: str
    builtin: bool = Field(..., description="Whether the library ships with PlantUML stdlib.")
    description: str
    include: str = Field(..., description="The `!include` line(s) that load the library.")
    docs_url: str | None = None
    categories: list[str] = Field(default_factory=list)


class Theme(BaseModel):
    id: str
    name: str
    preview_source: str = Field(
        ..., description="A tiny PlantUML source that demonstrates the theme."
    )


class Example(BaseModel):
    id: str
    title: str
    description: str
    category: str
    libraries: list[str] = Field(default_factory=list)
    source: str


class ExampleSummary(BaseModel):
    id: str
    title: str
    description: str
    category: str
    libraries: list[str] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """RFC 7807-style problem detail."""

    type: str = "about:blank"
    title: str
    status: int
    detail: str | None = None
