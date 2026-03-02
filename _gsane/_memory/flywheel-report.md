# Flywheel Report

> Generated automatically by `workflow-aggregate.md` — do NOT edit manually.
> Overwritten at each flywheel cycle. See `flywheel-history.md` for historical records.

<!-- FLYWHEEL REPORT WRITTEN HERE BY workflow-aggregate.md -->

---
## Flywheel Report
generated: 2026-03-01
sessions_analyzed: 5
total_sessions_in_log: 5
trigger_threshold: 5

### Flywheel Score
- Compliance rate: 40% (2 PASS / 5 sessions)
- Avg token impact: medium
- Auto-corrections applied this cycle: 2 (sessions 3+5, pre-cycle)
- High severity pending: 0
- Trend: stable ➡️ (premier cycle — pas de baseline comparative)

### Confirmed Patterns — Token & Optimization (Léo)
- Pattern: unnecessary-load
  Occurrences: 4
  Severity: medium
  Target: skill — .github/skills/gsane-framework/SKILL.md
  Action: Ajouter section "JIT Loading Protocol" avec les 4 signaux de violation
  Status: applied ✅

### Confirmed Patterns — Compliance & Quality (Aria)
- Pattern: manifest-sync
  Occurrences: 3
  Severity: medium
  Target: manifest — _gsane/_config/workflow-manifest.csv
  Action: Ajouter entrées flywheel-aggregate et flywheel-apply
  Status: applied ✅ (corrigé dans la même session avant le cycle)

### Watch List (2 occurrences — pas encore actionnable)
- (aucun)

### Bruit ignoré (1 occurrence)
- config-reload-waste (session 4 seulement)
- profile-overload (session 2 seulement)

