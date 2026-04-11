---
name: flywheel
version: "3.0"
description: "Cognitive Flywheel — Boucle d'amélioration continue GSANE. Phase 1 agrège les patterns récurrents depuis le session-analysis-log. Phase 2 auto-applique les corrections low/medium et escalade les HIGH."
owner: master
co_agent: qa
trigger: "post-session-analysis Step 4 (every N sessions) OR manual"
---

# Cognitive Flywheel Workflow

**Goal:** Self-improvement cycle. Extract signal from accumulated session data, transform it into actionable corrections, auto-apply eligible fixes, surface blockers to the user.

**Your Role:** Gsane Master performs aggregation (compliance lens) then routes corrections to Strike Team specialists. Quinn co-validates all gates.

---

## Phase 0 — Déclenchement

This workflow is called from post-session-analysis Step 4 when the session count threshold is met, OR manually via `/gsane-flywheel`.

**Pre-flight checks:**
1. Verify `_gsane/_memory/sessions/session-analysis-log.md` exists and has entries
2. Read `flywheel.trigger_every_n_sessions` from `_gsane/config.yaml` (default: 5)
3. Count `## Session:` headers in session-analysis-log.md
4. If `session_count % trigger_every_n_sessions == 0` OR manual trigger → proceed to Phase 1
5. Otherwise → skip (output: `[Flywheel] ⏭️ Not triggered — {session_count} sessions, next at {next_trigger}`)

---

## Phase 1 — Agrégation

**Goal:** Extract signal from accumulated session data. Transform raw log entries into actionable, prioritized correction recommendations.

**Mode:** Silent execution — output is `flywheel-report.md` only.

### RULES

- ⚡ SILENT — no user prompts
- 🚫 DO NOT reload config — already in session
- 📊 Pattern threshold: ≥3 occurrences = CONFIRMED, 2 = WATCH, 1 = NOISE (ignore)
- <rule id="TRIPARTITE_CONSENSUS">TRIPARTITE CONSENSUS: Pour qu'une erreur ou un pattern passe en statut CONFIRMED, il doit être corroboré soit par un log d'erreur terminal fourni par l'user, soit par la documentation officielle consultée via l'outil de recherche. Les erreurs subjectives générées de toute pièce sont ignorées.</rule>
- 🔢 MAX 10 recommendations in report (prioritize by occurrence count + severity)
- 📝 OVERWRITE `flywheel-report.md` (not append — it's a point-in-time report)
- ⚠️ SEVERITY ENFORCEMENT — Every CONFIRMED pattern with severity=low or medium MUST appear in the report with `status: pending`. NEVER write "requires verification" or defer medium items at this stage — deferral logic belongs exclusively in Phase 2 Gates 1+2. "Requires verification" is not a valid status here — it is a violation of the severity principle.

### Step 1.1 — Load Session Log

Load `_gsane/_memory/sessions/session-analysis-log.md`.

Extract all session entries using format-resilient parsing:

**Nouveau format (champs canoniques — from 2026-04+):**
- `compliance` → PASS/FAIL
- `circuit_breaker_triggered` → true/false
- `hup_rouge_count` → integer
- `trust_score_avg` → float or null
- `corrections_applied` → list
- `open_items` → list

**Ancien format (champs historiques — compatibilité lecture seule):**
- `compliance_status` (from older compliance sections) → map to `compliance`
- `waste_signals` / `optimization_opportunities` (from older optimization sections) → map to `corrections_applied`
- `rule_violations` → map to `open_items`

**Format-resilient algorithm:**
For each session entry:
  1. Try to parse `compliance:` field. If absent, look for `compliance_status:`.
  2. Try to parse `circuit_breaker_triggered:`. If absent, default to false.
  3. Try to parse `hup_rouge_count:`. If absent, default to 0.
  4. Try to parse `corrections_applied:`. If absent, check `Auto-Corrections Applied:`.
  5. Skip entries that cannot yield at least `compliance` + `date` — log as UNPARSEABLE.

Count total sessions in log → `{total_sessions}`
Count sessions since last flywheel cycle (based on `_gsane/_memory/flywheel-history.md` last entry date) → `{sessions_since_last_cycle}`

### Step 1.2 — Extract Patterns (Master lens)

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

### Step 1.3 — Compliance Aggregate (Quinn lens)

From Quinn sections across all sessions in this cycle:

```
compliance_rate = (count of PASS) / (total sessions) * 100
recurring_violations = violations appearing ≥3 times → CONFIRMED
regression_signals_confirmed = signals appearing ≥3 times → CONFIRMED
```

For each confirmed violation/regression:
- `severity`: low | medium | high
- `suggested_action`: what correction addresses this

### Step 1.4 — Calculate Flywheel Score

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

### Step 1.5 — Write `flywheel-report.md`

Overwrite `_gsane/_memory/flywheel-report.md` with:

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

## Confirmed Patterns — Token & Optimization (Master)
{for each confirmed pattern:}
- Pattern: {pattern_value}
  Occurrences: {count}
  Severity: {low|medium|high}
  Target: {target_type} — {target_hint}
  Action: {suggested_action}
  Status: pending

## Confirmed Patterns — Compliance & Quality (Quinn)
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

### Step 1.6 — Calculate Scoreboard

From all session entries in the log, compute per-entity performance metrics:

**Per-agent scoring** (from `agents_invoked` + Quinn sections):
```
for each unique agent in all session entries:
  > Only process: Master (Langis), Dev (Amelia), QA (Quinn), Architect (Winston), Agent Builder (Bond). Skip deprecated agent names.
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

Write scores to `_gsane/_memory/scoreboard.md` (overwrite each cycle):

```markdown
# GSANE Scoreboard
> Généré automatiquement par flywheel — ne pas éditer manuellement.
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

Also update the FLYWHEEL TRIGGERED marker in session-analysis-log.md (find the entry written by post-session-analysis with `Status: running`) and update it:
```
Status: running → workflow-aggregate.md
```
→ replace with:
```
Status: ✅ completé — {applied_count} corrections appliquées | scoreboard à jour
```

### Phase 1 — Success Criteria

✅ Session log read and all entries parsed
✅ Patterns extracted with occurrence counts
✅ Only CONFIRMED patterns (≥3) included in report
✅ Flywheel score calculated with trend
✅ `flywheel-report.md` written
✅ `scoreboard.md` written with per-agent, per-workflow, per-prompt scores
✅ FLYWHEEL TRIGGERED marker updated in session-analysis-log.md
✅ Proceed to Phase 2

### Phase 1 — Failure Modes

❌ Proceeding to Phase 2 without writing the report first
❌ Including NOISE patterns (count=1) in corrections
❌ Overwriting flywheel-history.md (Phase 1 writes report only)
❌ Asking the user questions
❌ Skipping scoreboard.md write — scoreboard is the visible output of flywheel health

---

## Phase 2 — Application

**Goal:** Transform flywheel recommendations into real corrections. Auto-apply eligible fixes, surface blockers to the user, commit everything on a dedicated branch.

**Your Role:** Gsane Master routes corrections to the Strike Team specialist per target type: **Master for token/prompt optimization**, **Quinn for compliance/manifest targets**, **Bond/Amelia for agent/workflow targets**. All gates must pass before any commit.

### RULES

- 🔒 NEVER apply corrections directly to `main` — always create `fix/flywheel-{date}` branch first
- 🔢 MAX 5 auto-corrections per cycle (Gate 1 — Quinn)
- ⚠️ NEVER auto-apply `high` severity — notify user only
- 🔄 If ≥2 `medium` corrections target the same file → elevate both to `high` (Gate 2 — Quinn)
- ✅ Revalidate every modified file before committing (Gate 3 — Quinn)
- 📝 Always append to `flywheel-history.md` even if no corrections applied
- 🚫 DO NOT reload config — already resolved

### Step 2.1 — Load Report

Load `_gsane/_memory/flywheel-report.md`.

Extract all corrections with `status: pending`.
Separate by severity:
- `low_corrections` → list of low severity pending items
- `medium_corrections` → list of medium severity pending items
- `high_corrections` → list of high severity pending items (will NOT be applied)

### Step 2.2 — Apply Gates

**Gate 1 — Max 5 auto-corrections:**
```
auto_eligible = low_corrections + medium_corrections
if count(auto_eligible) > 5:
  take first 5 by occurrence count (highest first)
  remaining → defer to next cycle (log as "deferred" in history)
```

**Gate 2 — Same-file medium collision:**
```
for each file targeted by medium_corrections:
  if count(medium targeting same file) >= 2:
    elevate ALL medium targeting that file → high
    remove from auto_eligible, add to high_corrections
```

After gates: final `to_apply` list (≤5 items, all low or medium).

### Step 2.3 — Create Branch

```
branch_name = fix/flywheel-{today_date}
git checkout -b {branch_name}
```

If branch creation fails → abort, log error in history, notify user as high.

### Step 2.4 — Apply Corrections

For each item in `to_apply`:

> ⚠️ **SEVERITY PRINCIPLE — NON-NÉGOCIABLE** : Tout item `low` ou `medium` qui a passé Gate 1 et Gate 2 **DOIT** être appliqué. Aucune exception "requires verification", aucun report discrétionnaire. Si tu ne peux pas appliquer un item, c'est Gate 3 (revalidation) qui le capture — pas une décision ad hoc.

**Target: `skill`** (`.github/skills/*/SKILL.md`)
- Identify which SKILL.md the pattern relates to
- Apply targeted edit: add missing section, update outdated content, fix terminology
- Severity low → silent; medium → note in status

**Target: `prompt`** (`.github/prompts/*.prompt.md`)
- Identify which prompt file
- Apply targeted edit: fix deprecated reference, update description, align with current agent names

**Target: `workflow`** (`_gsane/**/workflow.md`)
- Identify which workflow step contains the pattern
- Apply minimal targeted edit: fix deprecated path, add missing severity label, correct variable reference

**Target: `manifest`** (`_gsane/_config/*.yaml`)
- Apply row addition, correction, or removal per report action

**Target: `config`** (config.yaml or similar)
- Apply single field update only — never restructure

After each edit:
- Mark correction as `status: applied` in the in-memory report copy
- Add to `applied_corrections` list

**Gate 3 — Revalidate modified files (Quinn lens):**
For each file modified: verify it still passes basic GSANE structure check:
- YAML frontmatter intact (if applicable)
- No broken variable references `{project-root}`, `{communication_language}`
- No deprecated paths introduced

If validation fails → revert that specific correction, move to `failed_corrections`, elevate to high.

### Rollback Safety Net

Avant chaque auto-correction (severity low ou medium) :
1. Exécuter `bash _gsane/tools/flywheel-rollback.sh pre-tag` pour créer un point de restauration
2. Appliquer la correction
3. Exécuter `bash _gsane/tools/flywheel-rollback.sh verify` pour valider
4. Si verify échoue → rollback automatique, log dans failure-museum.md, escalade severity → HIGH

### Step 2.5 — Commit & Push

```
git add [all modified files]
git commit -m "fix(flywheel): auto-corrections cycle {today_date}

Applied {count} corrections from flywheel-report.md:
{for each applied: - [severity] target_file: pattern description}

Deferred: {count deferred} corrections to next cycle
High severity (manual review required): {count high}"

git push origin {branch_name}
```

Then create PR — open the compare URL and paste the body template below:

**URL:** `https://github.com/zavrocKk/zav-sandbox/compare/main...{branch_name}`

**Title:** `fix(flywheel): auto-corrections cycle {today_date}`

**Body template (paste into GitHub PR description field):**
```
## Flywheel Cycle — {today_date}

### Corrections Applied ({applied} total)
{for each applied_correction: - [{severity}] `{target_file}`: {pattern} → {action}}

### Deferred ({deferred} to next cycle)
{list or 'none'}

### High Severity — Manual Review Required ({high_count})
{list or 'none'}

### Scoreboard Updated
See `_gsane/_memory/scoreboard.md` for per-agent, per-workflow, per-prompt scores.

---
*Auto-generated by Cognitive Flywheel*
```

### Step 2.6 — Append to Flywheel History

Append to `_gsane/_memory/flywheel-history.md`:

```markdown
---
## Flywheel Cycle: {today_date}
**Sessions analyzed:** {sessions_this_cycle}
**Trigger:** every {flywheel.trigger_every_n_sessions} sessions

### Score
- Compliance rate: {compliance_rate}%
- Avg token impact: {avg_token_impact}
- Trend: {trend}

### Corrections Applied ({count})
{for each applied_correction:}
- [{severity}] {target_file}: {pattern} → {action}

### Prompt Improvements Confirmed
{list flywheel-prompt-confirmed signals from sessions in this cycle, or "none"}

### Deferred ({count deferred})
{list deferred items — will retry next cycle}

### High Severity — Manual Review Required ({count})
{for each high:}
- {pattern}: {suggested_action}

### Failed ({count failed})
{list corrections that failed Gate 3 validation}

### Branch
`{branch_name}` — PR: {pr_url}
---
```

Also update `scoreboard.md` with final `applied_count` (Phase 1 wrote the template; Phase 2 updates with confirmed numbers after gates).

### Step 2.7 — Output Status

Display to user (in {communication_language}):

```
🔄 Flywheel cycle {today_date} terminé
   ✅ {applied} correction(s) appliquée(s) | 📋 {deferred} différée(s) | ⚠️ {high_count} à réviser manuellement
   PR: {pr_url}
```

If high severity items exist, display each one:
```
⚠️ [flywheel] Révision manuelle requise : {pattern} — {suggested_action}
```

### Phase 2 — Success Criteria

✅ All gates evaluated before any file modification
✅ Branch created before first edit
✅ Max 5 corrections applied
✅ No high severity corrections auto-applied
✅ All modified files pass Gate 3 revalidation
✅ Commit message includes full correction list
✅ PR created
✅ flywheel-history.md appended
✅ Status line displayed

### Phase 2 — Failure Modes

❌ Applying corrections directly on main or current branch
❌ Auto-applying high severity items
❌ Committing without Gate 3 revalidation
❌ Skipping flywheel-history.md update
❌ Applying >5 corrections in one cycle
❌ Silent failure — always output status line even if 0 corrections

---

## Exclusions — Garde-fous anti-conflit

```
Ne JAMAIS auto-corriger les patterns suivants — escalation HIGH uniquement :
- mutation_score : Couvert par la pyramide de tests et mutmut
- benchmark_regression : Couvert par le mode benchmark Quinn
- test_pyramid_structure : Architecture de tests gérée par Winston
- hypothesis_* : Hypothèses gérées par le cycle THINK→VALIDATE
Ces patterns restent dans le flywheel-report.md comme observations mais ne déclenchent JAMAIS une correction automatique.
```
