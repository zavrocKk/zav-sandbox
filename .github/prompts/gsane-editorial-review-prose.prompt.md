---
description: 'Editorial review prose'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

1. Load `_gsane/config.yaml` and communicate in `{communication_language}`.
2. Review the target document or current selection for prose quality only: clarity, tone, ambiguity, grammar, repetition, and terminology drift.
3. Preserve structure and technical intent. Do not reorder sections or rewrite large passages unless a sentence-level fix requires it.
4. Report findings as a three-column markdown table: `Extrait | Probleme | Suggestion`.
5. Apply directly only trivial, low-risk fixes such as typos, punctuation, or obvious wording cleanups when the file is editable in the current session.
6. Flag broken file paths, stale agent names, and flat-design inconsistencies as high-priority prose issues.
