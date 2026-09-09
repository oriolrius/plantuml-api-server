---
title: Claude Code Skill
order: 26
category: Using the API
---
# Claude Code Skill

This project ships a **Claude Code / Agent Skill** that teaches an AI coding agent to create and
render diagrams through this API — using the very documentation you are reading as its reference.
It lives in the repository under [`skill/plantuml-api/`](https://github.com/oriolrius/plantuml-api-server/tree/main/skill/plantuml-api).

## What the skill gives an agent

- A tiny, dependency-free client (`scripts/plantuml_api.py`) to **render**, **check**, **encode**,
  **decode**, and list **libraries / themes / examples**.
- Two curated references so the agent writes *correct* PlantUML the first time:
  - `references/cheatsheet.md` — quick syntax for every diagram type.
  - `references/architecture-libraries.md` — the exact, verified `!include` paths and macros for
    AWS, Azure, Kubernetes, C4, GCP, OSA, Material, Office, Logos, Devicons and ArchiMate.
- A pointer to this live site (`/help`) for full depth.

## Install

Copy the skill folder into a skills directory your agent loads (for Claude Code, e.g.
`~/.claude/skills/plantuml-api/`), then point it at your instance:

```bash
export PLANTUML_API_BASE="https://plantuml.joor.net"   # or your own host
```

## Use it

```bash
# render source to an image
python3 scripts/plantuml_api.py render diagram.puml --format svg --out diagram.svg

# validate a diagram renders before using it
python3 scripts/plantuml_api.py check diagram.puml

# get a shareable editor/PNG/SVG URL
python3 scripts/plantuml_api.py encode diagram.puml

# discover what's available
python3 scripts/plantuml_api.py libraries
python3 scripts/plantuml_api.py themes
python3 scripts/plantuml_api.py examples
python3 scripts/plantuml_api.py example c4-container
```

The same operations are plain HTTP, so any agent or script can use them without the helper — see
[Getting Started](/help/getting-started) and the [REST API Reference](/help/api-reference).

## Why a skill?

Diagrams-as-code shines when the diagram lives beside the code and is regenerated automatically.
An agent equipped with this skill can turn a request like *"draw the deployment architecture"*
into correct PlantUML, validate it against the API, and drop the rendered SVG into your docs — all
without you memorizing include paths. See [Diagrams as Code](/help/diagrams-as-code).
