# Documentation Standards — Tech Writer Sidecar
# GSANE Framework — bmm/agents/tech-writer memory
# Updated: 2026-03-02

## Core Principles

1. **Clarity above all** — Every word and phrase serves a purpose. No filler.
2. **Diagrams over prose** — Prefer Mermaid diagrams when visuals communicate better than text.
3. **Audience-first** — Always clarify or infer the intended audience before writing. Adjust depth accordingly.
4. **Living documents** — Docs evolve with code. Flag stale sections proactively.
5. **Task-oriented** — Structure all docs around what the reader needs to accomplish.

## Formatting Standards

- Use CommonMark markdown syntax
- Use ATX-style headings (`#`, `##`, `###`)
- Fenced code blocks with language identifier (` ```yaml `, ` ```typescript `, etc.)
- Tables for comparisons and structured data
- Bullet lists for enumeration; numbered lists for sequential steps only

## Mermaid Diagrams

- Always use valid Mermaid syntax inside fenced code blocks: ` ```mermaid `
- Prefer `flowchart TD` for process flows
- Prefer `sequenceDiagram` for agent/system interactions
- Prefer `classDiagram` for data models
- Keep diagrams focused — one concept per diagram

## GSANE-Specific Rules

- All file paths in documentation must be relative to `{project-root}`
- Reference agents by their `displayName (icon)` format: e.g., "Mary 📊"
- Reference workflows by their manifest name in backticks: e.g., `` `sprint-planning` ``
- Always note if a document references GSANE-exclusive features (flywheel, cc-verify, delegation)

## User Specified CRITICAL Rules

<!-- User preferences are appended here by the [US] Update Standards command -->
