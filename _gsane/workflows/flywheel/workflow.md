# Cognitive Flywheel Workflow

**Workflow ID:** flywheel
**Purpose:** Self-improvement entry point. Routes to the aggregate or apply sub-workflows.

This workflow is the top-level entry — it is called from post-session-analysis when the session count threshold is met.

---

## STEP 1 — Run aggregation

Load and execute: `_gsane/workflows/flywheel/workflow-aggregate.md`

This reads `_gsane/_memory/sessions/session-analysis-log.md`, extracts patterns, and writes `_gsane/_memory/flywheel-report.md`.

## STEP 2 — Run application

After aggregation completes, load and execute: `_gsane/workflows/flywheel/workflow-apply.md`

This applies low/medium corrections automatically and escalates high findings to the user.

## STEP 3 — Log flywheel run

Append a summary line to `_gsane/_memory/flywheel-history.md`:
```
## Flywheel Run: {date}
- Patterns found: {N}
- Auto-applied: {N_applied}
- Escalated: {N_escalated}
```

---

**Output:** Silent unless high-severity findings need escalation.
