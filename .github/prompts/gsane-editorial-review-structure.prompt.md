---
description: 'Editorial review structure'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

1. Load `_gsane/config.yaml` and communicate in `{communication_language}`.
2. Review the target document for structure only: heading hierarchy, section ordering, duplication, missing transitions, and opportunities to compress or split content.
3. Keep the technical content intact. Avoid sentence-level prose polishing unless it directly supports a structural recommendation.
4. Output findings as a three-column markdown table: `Section | Probleme structurel | Recommandation`.
5. Apply directly only low-risk structural fixes such as heading normalization or obvious duplicate removal. For larger reorganizations, propose the change plan before editing.
6. If the document is too large to remain maintainable, recommend `gsane-shard-doc` with a concrete shard plan.
