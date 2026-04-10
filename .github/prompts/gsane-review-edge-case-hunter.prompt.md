---
description: 'Edge Case Hunter Review'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

1. Load `_gsane/config.yaml` and communicate in `{communication_language}`.
2. Walk the target artifact for unhandled boundaries only: empty inputs, invalid values, missing files, threshold edges, branching gaps, alias drift, and config mismatches.
3. Ignore style or general quality comments unless they create a real edge-case failure.
4. Report only the missing edge cases as a markdown table: `Cas limite | Pourquoi ca casse | Mitigation suggeree`.
5. When reviewing configuration or prompts, include runtime edges such as invalid agent names, stale manifest paths, and references to removed workflows.
6. If every meaningful boundary appears covered, say so explicitly and stop.
