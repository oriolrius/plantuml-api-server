"""Application configuration, loaded from environment variables.

All settings are plain environment variables (no prefix) so the deployment stack
can wire them straight into the container. Sensible defaults let the app boot for
local development against ``localhost``.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # --- Upstream PlantUML Server ------------------------------------------------
    # Internal base URL of the official PlantUML Server, INCLUDING its context path.
    # When the PlantUML Server runs with BASE_URL=editor it serves every endpoint
    # under /editor, so this must end with /editor to match.
    plantuml_url: str = Field(
        default="http://localhost:8080/plantuml",
        description="Internal base URL of the PlantUML Server (including context path).",
    )

    # --- Public identity ---------------------------------------------------------
    # Public origin the service is reachable at; used to build shareable URLs.
    public_base_url: str = Field(default="http://localhost:8080")
    # Public path prefix under which the PlantUML editor is exposed by the gateway.
    editor_path: str = Field(default="/editor")

    # --- Rendering behaviour -----------------------------------------------------
    connect_timeout: float = Field(default=5.0, description="PlantUML connect timeout (s).")
    request_timeout: float = Field(default=30.0, description="PlantUML render timeout (s).")
    max_source_bytes: int = Field(
        default=100_000, description="Reject diagram sources larger than this (bytes)."
    )

    # --- Observability -----------------------------------------------------------
    log_level: str = Field(default="INFO")
    log_json: bool = Field(default=True, description="Emit structured JSON logs.")

    @property
    def plantuml_url_clean(self) -> str:
        return self.plantuml_url.rstrip("/")

    @property
    def public_base_url_clean(self) -> str:
        return self.public_base_url.rstrip("/")

    @property
    def editor_base(self) -> str:
        """Public base URL of the PlantUML editor endpoints, e.g. https://host/editor."""
        return f"{self.public_base_url_clean}/{self.editor_path.strip('/')}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
