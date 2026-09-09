"""Async client for the official PlantUML Server.

The API never re-implements PlantUML rendering; it delegates to the real server.
This client encodes source, drives the native `/png|/svg|/txt|…` endpoints, maps
transport failures onto typed exceptions, and best-effort discovers the running
PlantUML version.
"""

from __future__ import annotations

import re
import time

import httpx

from .encoding import encode
from .logging import get_logger
from .metrics import BACKEND_REQUEST_DURATION

log = get_logger()


class PlantUMLError(Exception):
    """Base class for backend failures."""

    status: int = 502


class PlantUMLUnavailable(PlantUMLError):
    status = 503


class PlantUMLTimeout(PlantUMLError):
    status = 504


class PlantUMLRenderError(PlantUMLError):
    """The backend rejected the diagram (syntax error or unsupported format)."""

    def __init__(self, detail: str, line: int | None = None, status: int = 422):
        super().__init__(detail)
        self.detail = detail
        self.line = line
        self.status = status


class PlantUMLClient:
    def __init__(self, base_url: str, connect_timeout: float, request_timeout: float):
        self.base_url = base_url.rstrip("/")
        self._timeout = httpx.Timeout(request_timeout, connect=connect_timeout)
        self._client = httpx.AsyncClient(timeout=self._timeout, follow_redirects=True)
        self.version: str | None = None

    async def aclose(self) -> None:
        await self._client.aclose()

    def _url(self, fmt_token: str, encoded: str, index: int | None = None) -> str:
        if index is not None:
            return f"{self.base_url}/{fmt_token}/{index}/{encoded}"
        return f"{self.base_url}/{fmt_token}/{encoded}"

    async def render(
        self, source: str, fmt_token: str, index: int | None = None
    ) -> tuple[bytes, str]:
        """Render ``source`` to bytes. Returns (content, content_type)."""
        encoded = encode(source)
        url = self._url(fmt_token, encoded, index)
        start = time.perf_counter()
        try:
            resp = await self._client.get(url)
        except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
            raise PlantUMLUnavailable("PlantUML backend is unreachable") from exc
        except httpx.ReadTimeout as exc:
            raise PlantUMLTimeout("PlantUML render timed out") from exc
        finally:
            BACKEND_REQUEST_DURATION.observe(time.perf_counter() - start)

        # PlantUML signals diagram/syntax errors via response headers even on 200.
        err = resp.headers.get("X-PlantUML-Diagram-Error")
        if err:
            line_hdr = resp.headers.get("X-PlantUML-Diagram-Error-Line")
            line = int(line_hdr) if line_hdr and line_hdr.isdigit() else None
            raise PlantUMLRenderError(err, line=line)
        if resp.status_code >= 400:
            raise PlantUMLRenderError(
                f"PlantUML backend returned HTTP {resp.status_code}",
                status=502 if resp.status_code >= 500 else 422,
            )
        content_type = resp.headers.get("content-type", "application/octet-stream")
        return resp.content, content_type

    async def ping(self) -> bool:
        try:
            resp = await self._client.get(self.base_url + "/", timeout=httpx.Timeout(5.0))
            return resp.status_code < 500
        except httpx.HTTPError:
            return False

    async def fetch_version(self) -> str | None:
        """Discover the PlantUML version via the built-in ``version`` diagram."""
        try:
            content, _ = await self.render("@startuml\nversion\n@enduml", "txt")
        except PlantUMLError as exc:
            log.warning("could not fetch PlantUML version", extra={"extra": {"err": str(exc)}})
            return None
        text = content.decode("utf-8", errors="replace")
        m = re.search(r"PlantUML\s+v?([0-9][0-9A-Za-z.\-]+)", text) or re.search(
            r"[Vv]ersion[:\s]+v?([0-9][0-9A-Za-z.\-]+)", text
        )
        self.version = m.group(1) if m else None
        return self.version
