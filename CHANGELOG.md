# Changelog

All notable changes to this project are documented here. This project adheres to
[Semantic Versioning](https://semver.org/) and uses
[Conventional Commits](https://www.conventionalcommits.org/) via
[Commitizen](https://commitizen-tools.github.io/commitizen/).

## v1.1.3 (2026-09-09)

### Fix

- document URL-embedding in the guide; point skill to the marketplace

## v1.1.2 (2026-09-09)

### Fix

- content pane fills 99% of the canvas beside the open menu; add skill references

## v1.1.1 (2026-09-09)

### Fix

- widen the guide/help layout to 95% of the viewport

## v1.1.0 (2026-09-09)

### Feat

- rendered help docs site and Claude Code skill

## v1.0.0

### Feat

- Initial release: FastAPI facade around the official PlantUML Server.
- `POST /api/v1/render` (PNG/SVG/TXT/UTXT/PDF/EPS) with optional theme/library injection.
- `POST /api/v1/encode` and `POST /api/v1/decode` (PlantUML text-encoding).
- Discovery endpoints: `/api/v1/libraries`, `/api/v1/themes`, `/api/v1/examples`.
- Curated example gallery covering UML, AWS, Azure, Kubernetes, C4, GCP, OSA and themes.
- Modern responsive landing page (Pico CSS), OpenAPI 3.1 docs at `/docs`.
- Prometheus metrics at `/metrics` and health at `/health` (reports PlantUML version).
- Multi-arch Docker image published to GHCR via GitHub Actions.
