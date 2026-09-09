---
name: plantuml-api
description: Create and render PlantUML diagrams as code — UML (sequence, class, activity, state, component, deployment…) and architecture diagrams (AWS, Azure, Kubernetes, C4, GCP, OSA/security, and more) — through the PlantUML API server. Use when the user wants to draw/render a diagram, produce a PNG/SVG/TXT/PDF from PlantUML source, get a shareable diagram URL, decode a PlantUML URL, or needs reference on PlantUML syntax and architecture icon libraries.
---

# PlantUML API

Render and design PlantUML diagrams via a running **PlantUML API server** (default
`https://plantuml.joor.net`). You write normal PlantUML source; the API renders it to
images and gives you shareable URLs. There is **no new DSL** — plain PlantUML always works.

## Configuration

Base URL is `https://plantuml.joor.net` by default. Override with the `PLANTUML_API_BASE`
environment variable if you run your own instance:

```bash
export PLANTUML_API_BASE="https://plantuml.joor.net"
```

## How to render a diagram

Write PlantUML to a file, then render it. Prefer the bundled helper:

```bash
# scripts/plantuml_api.py — render to SVG/PNG/TXT/PDF
python3 scripts/plantuml_api.py render diagram.puml --format svg --out diagram.svg
python3 scripts/plantuml_api.py render diagram.puml --format png --out diagram.png
```

Or with plain `curl` (JSON body; response is the native media type — not base64):

```bash
curl -fsS -X POST "$PLANTUML_API_BASE/api/v1/render" \
  -H 'content-type: application/json' \
  -d '{"source":"@startuml\nAlice -> Bob: Hello\n@enduml","format":"svg"}' \
  -o diagram.svg
```

Supported formats: `svg`, `png`, `txt`, `utxt`, `pdf`, `eps`. Optional request fields:
`theme` (a PlantUML theme name), `libraries` (known library ids to auto-`!include`), and
`index` (for a source with multiple `@startuml` blocks). You can always just include
libraries/themes in the source yourself.

## Shareable URLs (encode)

```bash
python3 scripts/plantuml_api.py encode diagram.puml
# → { "encoded": "...", "editor_url": ".../editor/uml/...", "png_url": ..., "svg_url": ... }
```

Anyone who opens `editor_url` gets the exact diagram back — the source is inside the URL
(nothing is stored server-side). `decode` reverses it:

```bash
python3 scripts/plantuml_api.py decode "<encoded-token>"
```

## Discover libraries, themes, examples

```bash
python3 scripts/plantuml_api.py libraries          # AWS, Azure, Kubernetes, C4, GCP, OSA…
python3 scripts/plantuml_api.py themes             # cerulean, superhero, sketchy, …
python3 scripts/plantuml_api.py examples           # curated, ready-to-render gallery
python3 scripts/plantuml_api.py example c4-container   # one example's source + URLs
```

## Writing good PlantUML

- For **plain UML**, just write `@startuml … @enduml`. See `references/cheatsheet.md` for
  quick syntax of every diagram type.
- For **architecture diagrams** (AWS/Azure/Kubernetes/C4/GCP/OSA/Material/…), use the
  bundled stdlib includes. The exact, verified include paths and macros are in
  `references/architecture-libraries.md` — read it before writing architecture diagrams,
  because include paths are easy to get subtly wrong (e.g. Kubernetes is `<k8s/...>`, GCP
  macros are snake_case, Azure SQL macro is `AzureSqlDatabase`).
- Keep it INTERNET-safe: use bundled `!include <...>` (angle brackets); avoid remote
  `!includeurl` to arbitrary hosts.

## Full reference

The complete, example-rich documentation (every diagram type, the language, preprocessing,
themes, architecture libraries, a cookbook) is served by the same host at
`GET $PLANTUML_API_BASE/help` — with a live-rendered preview under every example. Fetch a
page's Markdown source or the rendered HTML when you need depth beyond the cheatsheets here.

## Verify a diagram renders

Before handing source to the user, confirm it renders (HTTP 200, no error):

```bash
python3 scripts/plantuml_api.py check diagram.puml   # prints OK / the PlantUML error
```
