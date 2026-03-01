---
name: flywheel-aggregate
description: "Cognitive Flywheel — Aggregation cycle. Reads session-analysis-log.md, extracts recurring patterns, calculates flywheel-score, and writes flywheel-report.md. Triggered automatically every N sessions (configured in config.yaml flywheel.trigger_every_n_sessions). Runs silently — no user interaction required."
---

# Flywheel Aggregate Workflow

**Goal:** Extract signal from accumulated session data. Transform raw log entries into actionable, prioritized correction recommendations.

**Your Role:** BMad Master briefly embodies Léo (analysis) and Aria (compliance lens) to produce an objective aggregate report. Silent execution — output is `flywheel-report.md` only.

---

## RULES

- ⚡ SILENT — no user prompts
- 🚫 DO NOT reload config — already in session
- 📊 Pattern threshold: ≥3 occurrences = CONFIRMED, 2 = WATCH, 1 = NOISE (ignore)
- 🔢 MAX 10 recommendations in report (prioritize by occurrence count + severity)
- 📝 OVERWRITE `flywheel-report.md` (not append — it's a point-in-time report)
- ✅ Always call `workflow-apply.md` after writing the report

---

## EXECUTION SEQUENCE

### Step 1 — Load Session Log

Load `{project-root}/_bmad/_memory/session-analysis-log.md`.

Extract all session entries. For each entry, collect:
- `waste_signals` from Léo sections
- `optimization_opportunities` from Léo sections
- `compliance_status` (PASS/FAIL/WARNING) from Aria sections
- `violations` from Aria sections
- `regression_signals` from Aria sections
- `top_recommendation` from Léo sections
- `top_finding` from Aria sections
- `AUTO_CORRECTIONS` applied

Count total sessions in log → `{total_sessions}`
Count sessions since last flywheel cycle (check `flywheel-history.md` for last_cycle date) → `{sessions_this_cycle}`

---

### Step 2 — Extract Patterns (Léo lens)

Group all collected values by type. Count occurrences of each unique value:

**Token waste patterns:**
```
{pattern_value}: {count} occurrences → CONFIRMED | WATCH | NOISE
```

**Optimization opportunities:**
```
{opportunity_value}: {count} occurrences → CONFIRMED | WATCH | NOISE
```

Keep only CONFIRMED patterns (≥3). Rank by occurrence count descending.

For each CONFIRMED pattern, determine:
- `target_type`: skill | prompt | workflow | manifest | config
- `target_hint`: which file category is most likely affected
- `suggested_action`: what correction would address this pattern
- `severity`: low | medium | high (per config.yaml automation.severity)

---

### Step 3 — Compliance Aggregate (Aria lens)

From Aria sections across all sessions in this cycle:

```
compliance_rate = (count of PASS) / (total sessions) * 100
recurring_violations = violations appearing ≥3 times → CONFIRMED
regression_signals_confirmed = signals appearing ≥3 times → CONFIRMED
```

For each confirmed violation/regression:
- `severity`: low | medium | high
- `suggested_action`: what correction addresses this

---

### Step 4 — Calculate Flywheel Score

```yaml
flywheel_score:
  compliance_rate: "{compliance_rate}%"
  avg_token_impact: # most frequent token impact level across sessions
  auto_corrections_applied: # total from AUTO_CORRECTIONS fields
  high_severity_pending: # count of high items not yet addressed
  trend: # compare to previous cycle in flywheel-history.md
         # improving = compliance_rate up OR waste patterns fewer
         # degrading = compliance_rate down OR waste patterns more
         # stable = no significant change (< 5% delta)
```

---

### Step 5 — Write `flywheel-report.md`

Overwrite `{project-root}/_bmad/_memory/flywheel-report.md` with:

```markdown
# Flywheel Report
generated: {today_date}
sessions_analyzed: {sessions_this_cycle}
total_sessions_in_log: {total_sessions}
trigger_threshold: {flywheel.trigger_every_n_sessions from config}

## Flywheel Score
- Compliance rate: {compliance_rate}%
- Avg token impact: {avg_token_impact}
- Auto-corrections applied this cycle: {auto_corrections_applied}
- High severity pending: {high_severity_pending}
- Trend: {trend} {📈 if improving | ➡️ if stable | 📉 if degrading}

## Confirmed Patterns — Token & Optimization (Léo)
{for each confirmed pattern:}
- Pattern: {pattern_value}
  Occurrences: {count}
  Severity: {low|medium|high}
  Target: {target_type} — {target_hint}
  Action: {suggested_action}
  Status: pending

## Confirmed Patterns — Compliance & Quality (Aria)
{for each confirmed violation/regression:}
- Pattern: {violation_value}
  Occurrences: {count}
  Severity: {low|medium|high}
  Target: {target_type} — {target_hint}
  Action: {suggested_action}
  Status: pending

## Watch List (2 occurrences — not yet actionable)
{list patterns with count=2}
```

Then immediately proceed to `workflow-apply.md`.

---

## SUCCESS METRICS

✅ Session log read and all entries parsed
✅ Patterns extracted with occurrence counts
✅ Only CONFIRMED patterns (≥3) included in report
✅ Flywheel score calculated with trend
✅ `flywheel-report.md` written
✅ `workflow-apply.md` called

## FAILURE MODES

❌ Calling workflow-apply without writing the report first
❌ Including NOISE patterns (count=1) in corrections
❌ Overwriting flywheel-history.md (aggregate writes report only)
❌ Asking the user questions
