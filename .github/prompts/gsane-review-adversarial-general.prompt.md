---
description: 'Adversarial review'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

1. Load `_gsane/config.yaml` and communicate in `{communication_language}`.
2. Review the target artifact critically to find concrete weaknesses, contradictions, broken paths, missing guards, and unverifiable claims.
3. Report findings only. Do not add praise, summary fluff, or speculative issues without evidence from the file.
4. For each finding, provide: `Severite | Evidence | Risque | Correction suggeree`.
5. Prefer root-cause issues over surface comments. If a path, workflow, or agent reference is dead in the current flat-design runtime, treat it as a high-severity finding.
6. If no actionable finding exists, state that explicitly and mention any residual testing or validation gap.
