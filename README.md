# PlantUML API Server

**Diagrams as Code — UML, Cloud Architecture, Kubernetes, C4 and more.**

A modern [FastAPI](https://fastapi.tiangolo.com/) REST API and developer portal built
around the official **[PlantUML Server](https://github.com/plantuml/plantuml-server)**.
It does not reinvent PlantUML — it exposes it elegantly: render diagrams to
PNG/SVG/TXT/PDF, encode/decode PlantUML URLs, and discover the architecture icon
libraries (AWS, Azure, Kubernetes, C4, GCP, OSA, Material and more), themes and a curated
example gallery. Ships with a polished landing page, OpenAPI 3.1 docs and Prometheus
metrics.

> You can always submit **plain PlantUML source**. The `theme` and `libraries` options are
> conveniences — never a replacement for PlantUML syntax. No new DSL, no lock-in.

## Features

- 🚀 **REST API** — `POST /api/v1/render` returns native `image/png`, `image/svg+xml`,
  `text/plain` or `application/pdf` (binary is streamed, never base64 unless you ask).
- 🔗 **PlantUML URL encoding** — `POST /api/v1/encode` / `decode` with ready-to-use editor
  and image URLs.
- 🧭 **Discovery** — `/api/v1/libraries`, `/api/v1/themes`, `/api/v1/examples`.
- ☁️ **Architecture as code** — first-class AWS (`awslib`), Azure, Kubernetes (`k8s`), C4,
  GCP, OSA (network/security), Material, Office, Logos, Devicons/Font-Awesome, ArchiMate.
- 🖼️ **Full editor** — the official PlantUML editor is served under `/editor`.
- 📊 **Prometheus** — `/metrics` with low-cardinality HTTP / render / backend metrics.
- 📚 **OpenAPI 3.1** — Swagger UI at `/docs`, schema at `/openapi.json`.
- 🎨 **Modern landing page** — responsive, light/dark, [Pico CSS](https://picocss.com/),
  no Node/React build chain.

## Quick start

```bash
# You need a PlantUML Server too (INTERNET security profile recommended).
docker network create puml
docker run -d --name plantuml --network puml \
  -e PLANTUML_SECURITY_PROFILE=INTERNET -e BASE_URL=editor \
  plantuml/plantuml-server:jetty-v1.2026.8

docker run -d --name plantuml-api --network puml -p 8080:8080 \
  -e PLANTUML_URL=http://plantuml:8080/editor \
  -e PUBLIC_BASE_URL=http://localhost:8080 \
  ghcr.io/oriolrius/plantuml-api-server:1

# open http://localhost:8080
```

A complete production stack (gateway + API + PlantUML Server) is a separate concern; this
repository ships only the API image.

## API reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Landing page |
| `GET` | `/editor/*` | Official PlantUML editor & native endpoints |
| `POST` | `/api/v1/render` | Render source → PNG/SVG/TXT/PDF |
| `POST` | `/api/v1/encode` | Encode source → token + URLs |
| `POST` | `/api/v1/decode` | Decode a token → source |
| `GET` | `/api/v1/libraries` | List icon/architecture libraries |
| `GET` | `/api/v1/libraries/{id}` | Library detail |
| `GET` | `/api/v1/libraries/{id}/examples` | Examples using a library |
| `GET` | `/api/v1/libraries/{id}/icons` | Library icon categories |
| `GET` | `/api/v1/themes` | List themes |
| `GET` | `/api/v1/examples` | Curated example gallery |
| `GET` | `/api/v1/examples/{id}` | Example + render URLs |
| `GET` | `/api/v1` | API discovery/metadata |
| `GET` | `/health` | Health + PlantUML version |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/docs`, `/openapi.json` | Swagger UI / OpenAPI 3.1 |

### curl examples

```bash
# Render a sequence diagram to SVG
curl -s -X POST http://localhost:8080/api/v1/render \
  -H 'content-type: application/json' \
  -d '{"source":"@startuml\nAlice -> Bob: Hello\n@enduml","format":"svg"}' \
  -o hello.svg

# Render an AWS architecture to PNG
curl -s -X POST http://localhost:8080/api/v1/render \
  -H 'content-type: application/json' \
  -d '{"source":"@startuml\n!include <awslib/AWSCommon>\n!include <awslib/Compute/EC2>\nEC2(web,\"Web\",\"t3.micro\")\n@enduml","format":"png"}' \
  -o aws.png

# Encode a diagram and get shareable URLs
curl -s -X POST http://localhost:8080/api/v1/encode \
  -H 'content-type: application/json' \
  -d '{"source":"@startuml\nAlice -> Bob\n@enduml"}' | jq

# Convenience: theme + library injection (still plain PlantUML underneath)
curl -s -X POST http://localhost:8080/api/v1/render \
  -H 'content-type: application/json' \
  -d '{"source":"@startuml\nAlice->Bob\n@enduml","format":"svg","theme":"cerulean"}' \
  -o themed.svg
```

## Architecture libraries

All of the following are bundled with the pinned PlantUML version and work under
`SECURITY_PROFILE=INTERNET` (no remote fetch). Discover them via `GET /api/v1/libraries`.

| Library | Include | Example macro |
|---|---|---|
| AWS (`awslib`) | `!include <awslib/AWSCommon>` + `<awslib/Compute/EC2>` | `EC2(id,"Web","t3")` |
| Azure | `!include <azure/AzureCommon>` + `<azure/Compute/AzureVirtualMachine>` | `AzureVirtualMachine(...)` |
| Kubernetes (`k8s`) | `!include <k8s/Common>` + `<k8s/OSS/KubernetesPod>` | `KubernetesPod(...)` |
| C4 | `!include <C4/C4_Container>` | `Container(...)`, `Rel(...)` |
| GCP | `!include <gcp/GCPCommon>` + `<gcp/Compute/Compute_Engine>` | `Compute_Engine(...)` |
| OSA (security) | `!include <aws/common>` + `<osa/firewall/firewall>` | `FIREWALL(...)` |
| Material | `!include <material2.1.19/common>` + `<material2.1.19/folder>` | `<$folder>` |
| Office | `!include <tupadr3/common>` + `<office/Servers/database_server>` | `OFF_DATABASE_SERVER(...)` |
| Logos | `!include <logos/kafka>` | `<$kafka>` |
| Devicons / FA5 | `!include <tupadr3/common>` + `<tupadr3/devicons/mysql>` | `DEV_MYSQL(...)` |
| ArchiMate | `!include <archimate/Archimate>` | `Business_Actor(...)` |

## Output formats

`png`, `svg`, `txt`, `pdf`, `eps` — subject to what the running PlantUML build
supports. The response carries the native media type.

## Prometheus metrics

`GET /metrics` exposes, among others:

```
http_requests_total{method,route,status}
http_request_duration_seconds{method,route}
plantuml_render_requests_total{format,status}
plantuml_render_duration_seconds{format}
plantuml_render_errors_total{format,reason}
plantuml_backend_up
plantuml_backend_request_duration_seconds
plantuml_api_info{api_version,plantuml_version}
```

Labels are strictly low-cardinality — diagram source, encoded tokens, client IPs and
arbitrary URLs are **never** used as labels.

## Configuration (environment variables)

| Variable | Default | Description |
|---|---|---|
| `PLANTUML_URL` | `http://localhost:8080/plantuml` | Internal PlantUML Server base URL **including context path** (e.g. `.../editor`). |
| `PUBLIC_BASE_URL` | `http://localhost:8080` | Public origin, used to build shareable URLs. |
| `EDITOR_PATH` | `/editor` | Public path prefix where the editor is exposed. |
| `CONNECT_TIMEOUT` | `5.0` | PlantUML connect timeout (s). |
| `REQUEST_TIMEOUT` | `30.0` | PlantUML render timeout (s). |
| `MAX_SOURCE_BYTES` | `100000` | Reject sources larger than this. |
| `LOG_LEVEL` | `INFO` | Log level. |
| `LOG_JSON` | `true` | Emit structured JSON logs. |

## Development

```bash
uv sync --extra dev
uv run uvicorn app.main:app --reload --port 8080
# with a local PlantUML backend:
#   PLANTUML_URL=http://localhost:18080 uv run uvicorn app.main:app --reload
```

Lint / type-check / test:

```bash
uv run ruff check app tests
uv run mypy app
uv run pytest
```

## Testing

`pytest` mocks the PlantUML backend with `respx`, so no live server is required. Tests
cover rendering (PNG/SVG), invalid source, backend-unavailable, timeout, encode/decode,
libraries/themes/examples, health, metrics and the OpenAPI 3.1 declaration.

## Releases

This project uses [Commitizen](https://commitizen-tools.github.io/commitizen/) with
[Conventional Commits](https://www.conventionalcommits.org/) and SemVer.

```bash
cz bump          # bump version + update CHANGELOG from commit history
git push
git push --tags
```

Pushing a `vX.Y.Z` tag triggers GitHub Actions to publish multi-arch images to GHCR.

## Container images

Published to `ghcr.io/oriolrius/plantuml-api-server`:

```
ghcr.io/oriolrius/plantuml-api-server:1.3.2   # exact
ghcr.io/oriolrius/plantuml-api-server:1.3     # minor
ghcr.io/oriolrius/plantuml-api-server:1       # major
ghcr.io/oriolrius/plantuml-api-server:latest  # latest release
```

Consume a specific SemVer tag in production — not `latest`.

## License

MIT.
