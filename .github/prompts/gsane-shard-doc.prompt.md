---
description: 'Shard document'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

1. Load `_gsane/config.yaml` and communicate in `{communication_language}`.
2. Inspect the target document and decide whether sharding is justified. Default threshold: document too large to maintain comfortably or contains clearly separable sections.
3. If sharding is not justified, say so briefly and explain the blocking reason.
4. If sharding is justified, produce a shard plan with: source file, target files, section-to-file mapping, preserved entrypoint, and link updates required.
5. When applying the split, preserve the source document's role as index or overview unless the user explicitly asks for a full move.
6. Avoid creating archive-style detours or legacy backends. The result must stay navigable from the active flat-design workspace.
