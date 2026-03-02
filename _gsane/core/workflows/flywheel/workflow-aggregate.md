---
name: flywheel-aggregate
description: "Cognitive Flywheel — Aggregation cycle. Reads session-analysis-log.md, extracts recurring patterns, calculates flywheel-score, and writes flywheel-report.md. Triggered automatically every N sessions (configured in config.yaml flywheel.trigger_every_n_sessions). Runs silently — no user interaction required."
---

# Flywheel Aggregate Workflow

**Goal:** Extract signal from accumulated session data. Transform raw log entries into actionable, prioritized correction recommendations.

**Your Role:** Gsane Master briefly embodies Léo (analysis) and Aria (compliance lens) to produce an objective aggregate report. Silent execution — output is `flywheel-report.md` only.

---

## RULES

- ⚡ SILENT — no user prompts
- 🚫 DO NOT reload config — already in session
- 📊 Pattern threshold: ≥3 occurrences = CONFIRMED, 2 = WATCH, 1 = NOISE (ignore)
- 🔢 MAX 10 recommendations in report (prioritize by occurrence count + severity)
- 📝 OVERWRITE `flywheel-report.md` (not append — it's a point-in-time report)
- ✅ Always call `workflow-apply.md` after writing the report
- ⚠️ SEVERITY ENFORCEMENT — Every CONFIRMED pattern with severity=low or medium MUST appear in the report with `status: pending`. NEVER write "requires verification" or defer medium items at this stage — deferral logic belongs exclusively in workflow-apply.md Gates 1+2. "Requires verification" is not a valid status here — it is a violation of the severity principle.

---

## EXECUTION SEQUENCE

### Step 1 — Load Session Log

Load `{project-root}/_gsane/_memory/session-analysis-log.md`.

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

Overwrite `{project-root}/_gsane/_memory/flywheel-report.md` with:

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

### Step 5b — Calculate Scoreboard

From all session entries in the log, compute per-entity performance metrics:

**Per-agent scoring** (from `agents_invoked` + Aria sections):
```
for each unique agent in all session entries:
  sessions_active = count of sessions where agent appears in agents_invoked
  pass_count = count of PASS compliance in those sessions
  compliance_rate = pass_count / sessions_active * 100
  avg_token_impact = most frequent token impact level when agent is active
  prompt_signals = collect all prompt_improvement_signals from those sessions
  score = A+ if compliance_rate == 100% AND avg_token_impact == low
          A  if compliance_rate >= 80%
          B  if compliance_rate >= 60% OR avg_token_impact == medium
          C  if compliance_rate < 60% OR high severity flagged
```

**Per-workflow scoring** (from `workflows_run` fields):
```
for each unique workflow in all session entries:
  executions = total count across all sessions
  corrections_generated = count of auto-corrections linked to that workflow
  avg_turns = average turns_count when workflow was active
```

**Per-prompt health** (from corrections applied to `.github/prompts/**`):
```
corrections_this_cycle = count of workflow-apply corrections targeting prompts
prompt_improvement_confirmed = count of flywheel-prompt-confirmed signals across sessions
```

Write scores to `{project-root}/_gsane/_memory/scoreboard.md` (overwrite each cycle):

```markdown
# GSANE Scoreboard
> Généré automatiquement par flywheel-aggregate — ne pas éditer manuellement.
> Cycle: {today_date} | Sessions analysées: {sessions_this_cycle} | Total: {total_sessions}

---
## 📊 Agent Performance

| Agent | Sessions Actives | Compliance | Token Impact | Prompt Signals | Score |
|---|---|---|---|---|---|
{for each agent: | {name} | {sessions_active} | {compliance_rate}% | {avg_token_impact} | {prompt_signals_summary} | {score} |}

---
## 📋 Workflow Performance

| Workflow | Exécutions | Corrections Générées | Score |
|---|---|---|---|
{for each workflow: | {name} | {executions} | {corrections_generated} | {score} |}

---
## 📝 Prompt Health

| Catégorie | Total | Corrections ce cycle | Améliorations confirmées | Santé |
|---|---|---|---|---|
| agents (.github/prompts/gsane-agent-*) | {count} | {corrections} | {confirmed} | {health_icon} |
| workflows (.github/prompts/gsane-*workflow*) | {count} | {corrections} | {confirmed} | {health_icon} |
| skills (.github/skills/**) | {count} | {corrections} | {confirmed} | {health_icon} |

---
## 🔄 Flywheel Métriques

- Cycle actuel: {session_count / trigger_n}
- Sessions par cycle: {trigger_n}
- Compliance globale: {global_compliance_rate}%
- Trend: {trend}
- Dernier cycle: {today_date}
- Prochain déclenchement: session {session_count + trigger_n}
```

Also update the FLYWHEEL TRIGGERED marker in session-analysis-log.md (find the entry written by post-session-analysis Step 6 with `Status: running`) and update it:
```
Status: running → workflow-aggregate.md
```
→ replace with:
```
Status: ✅ completé — {applied_count} corrections appliquées | scoreboard à jour
```

✅ Session log read and all entries parsed
✅ Patterns extracted with occurrence counts
✅ Only CONFIRMED patterns (≥3) included in report
✅ Flywheel score calculated with trend
✅ `flywheel-report.md` written
✅ `scoreboard.md` written with per-agent, per-workflow, per-prompt scores
✅ FLYWHEEL TRIGGERED marker updated in session-analysis-log.md
✅ `workflow-apply.md` called

## FAILURE MODES

❌ Calling workflow-apply without writing the report first
❌ Including NOISE patterns (count=1) in corrections
❌ Overwriting flywheel-history.md (aggregate writes report only)
❌ Asking the user questions
❌ Skipping scoreboard.md write — scoreboard is the visible output of flywheel health
