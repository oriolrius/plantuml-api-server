---
title: Claude Code Skill
order: 26
category: Using the API
---
# Claude Code Skill

This project has a companion **Claude Code / Agent Skill**, `plantuml-api`, that teaches an AI
coding agent to create and render diagrams through this API — using this very documentation as
its reference. The agent turns a request like *"draw the deployment architecture"* into correct
PlantUML, validates it against the API, and can embed the rendered SVG straight into your docs.

## Install

The skill is published to a Claude Code plugin marketplace. Install it (project scope):

```bash
/plugin install skill-plantuml-api@litellm --scope project
```

Then point it at your instance (defaults to `https://plantuml.joor.net`):

```bash
export PLANTUML_API_BASE="https://plantuml.joor.net"   # or your own host
```

> Running your own marketplace? The skill is a standard single-skill repo (`SKILL.md` at the
> root, plus `scripts/` and `references/`) that publishes on a `v*` tag. Point your marketplace
> at it, or vendor the folder into any skills directory your agent loads
> (e.g. `~/.claude/skills/plantuml-api/`).

## What the skill gives an agent

- A tiny, dependency-free client (`scripts/plantuml_api.py`) to **render**, **check**,
  **encode**, **decode**, and list **libraries / themes / examples**.
- **URL-embedding** guidance — put a live diagram in a `.md`/HTML file by URL, no committed image.
- Two curated references so the agent writes *correct* PlantUML the first time:
  - `references/cheatsheet.md` — quick syntax for every diagram type.
  - `references/architecture-libraries.md` — the exact, verified `!include` paths and macros for
    AWS, Azure, Kubernetes, C4, GCP, OSA, Material, Office, Logos, Devicons and ArchiMate.
- A pointer to this live site (`/help`) for full depth.

## Use it

```bash
# render source to an image
python3 scripts/plantuml_api.py render diagram.puml --format svg --out diagram.svg

# validate a diagram renders before using it
python3 scripts/plantuml_api.py check diagram.puml

# get a shareable editor/PNG/SVG URL (for embedding by URL)
python3 scripts/plantuml_api.py encode diagram.puml

# discover what's available
python3 scripts/plantuml_api.py libraries
python3 scripts/plantuml_api.py themes
python3 scripts/plantuml_api.py example c4-container
```

The same operations are plain HTTP, so any agent or script can use them without the helper — see
[Getting Started](/help/getting-started) and the [REST API Reference](/help/api-reference).

## Why a skill?

Diagrams-as-code shines when the diagram lives beside the code and is regenerated automatically.
An agent equipped with this skill produces correct PlantUML, validates it, and drops the rendered
SVG into your docs — without anyone memorizing include paths. See
[Diagrams as Code](/help/diagrams-as-code).
