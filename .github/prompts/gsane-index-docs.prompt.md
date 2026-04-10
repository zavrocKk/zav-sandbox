---
description: 'Index documents'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

1. Load `_gsane/config.yaml` and communicate in `{communication_language}`.
2. Build a lightweight index for the requested file set. If no scope is provided, default to the active documentation or prompt/workflow surface the user is working on.
3. For each file, capture: relative path, purpose, major sections or headings, and 3 to 5 keywords. Do not paraphrase the full document.
4. Output the result as a compact markdown table: `Fichier | But | Sections clefs | Mots-clefs`.
5. If the user asks to persist the index, update or create a nearby index file with the same compact structure. Otherwise return the index in chat only.
6. Never point to archived or missing backends when a direct lightweight index can be generated from the current workspace.
