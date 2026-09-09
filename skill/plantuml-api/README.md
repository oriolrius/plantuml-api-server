# plantuml-api skill

A Claude Code (Agent Skills) skill that teaches an agent to create and render PlantUML
diagrams — UML and cloud/architecture — through the [PlantUML API server](../../README.md).

## What it does
- Renders PlantUML source to SVG/PNG/TXT/PDF via the API (`scripts/plantuml_api.py`).
- Encodes/decodes shareable PlantUML URLs.
- Discovers libraries, themes and curated examples.
- Ships verified references so the agent writes correct diagrams:
  - `references/cheatsheet.md` — quick syntax for every diagram type.
  - `references/architecture-libraries.md` — exact, validated `!include` paths & macros for
    AWS, Azure, Kubernetes, C4, GCP, OSA, Material, Office, Logos, Devicons, ArchiMate.

## Configure
Set the API base URL (defaults to `https://plantuml.joor.net`):
```bash
export PLANTUML_API_BASE="https://your-plantuml-host"
```

## Install
Copy the `plantuml-api/` folder into your skills directory (e.g. `~/.claude/skills/` or a
plugin), or point your skill tooling at it. The full live docs are always at
`$PLANTUML_API_BASE/help`.
