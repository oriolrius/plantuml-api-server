# Claude Code skill — `plantuml-api`

This project has a companion **Claude Code skill** that drives this API to create, render,
encode and **embed** diagrams as code, with verified references for every diagram type and
architecture icon library (AWS, Azure, Kubernetes, C4, GCP, OSA, Material, Office, Logos,
Devicons, ArchiMate).

- **Install** (from a Claude Code plugin marketplace):
  ```
  /plugin install skill-plantuml-api@litellm --scope project
  ```
- **What it does & how to use it:** https://plantuml.joor.net/help/claude-skill
- **The API it drives:** https://plantuml.joor.net · full docs at https://plantuml.joor.net/help

The skill is maintained as a **standalone single-skill repository** (`SKILL.md` at the root,
plus `scripts/plantuml_api.py` and `references/`) and published to a plugin marketplace on each
`v*` tag. It's a thin client over this public HTTP API plus two reference cheatsheets, so you can
also build an equivalent skill directly from the public docs linked above.
