---
name: flywheel-apply
description: "Cognitive Flywheel — Application cycle. Reads flywheel-report.md, applies low/medium corrections automatically (max 5 per cycle), escalates high findings to user. Creates a fix/flywheel-{date} branch, commits, pushes PR, then appends to flywheel-history.md. Called by workflow-aggregate.md — never directly."
---

# Flywheel Apply Workflow

**Goal:** Transform flywheel recommendations into real corrections. Auto-apply eligible fixes, surface blockers to the user, commit everything on a dedicated branch.

**Your Role:** BMad Master applies corrections acting as the appropriate specialist per target type (Léo for token/prompt targets, Aria for compliance/manifest targets, Bond/Wendy for agent/workflow targets). All gates must pass before any commit.

---

## RULES

- 🔒 NEVER apply corrections directly to `main` — always create `fix/flywheel-{date}` branch first
- 🔢 MAX 5 auto-corrections per cycle (Gate 1 — Murat)
- ⚠️ NEVER auto-apply `high` severity — notify user only
- 🔄 If ≥2 `medium` corrections target the same file → elevate both to `high` (Gate 2 — Murat)
- ✅ Revalidate every modified file before committing (Gate 3 — Aria)
- 📝 Always append to `flywheel-history.md` even if no corrections applied
- 🚫 DO NOT reload config — already resolved

---

## EXECUTION SEQUENCE

### Step 1 — Load Report

Load `{project-root}/_bmad/_memory/flywheel-report.md`.

Extract all corrections with `status: pending`.
Separate by severity:
- `low_corrections` → list of low severity pending items
- `medium_corrections` → list of medium severity pending items
- `high_corrections` → list of high severity pending items (will NOT be applied)

---

### Step 2 — Apply Gates

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

---

### Step 3 — Create Branch

```
branch_name = fix/flywheel-{today_date}
git checkout -b {branch_name}
```

If branch creation fails → abort, log error in history, notify user as high.

---

### Step 4 — Apply Corrections

For each item in `to_apply`:

**Target: `skill`** (`.github/skills/*/SKILL.md`)
- Identify which SKILL.md the pattern relates to
- Apply targeted edit: add missing section, update outdated content, fix terminology
- Severity low → silent; medium → note in status

**Target: `prompt`** (`.github/prompts/*.prompt.md`)
- Identify which prompt file
- Apply targeted edit: fix deprecated reference, update description, align with current agent names

**Target: `workflow`** (`_bmad/**/workflow.md`)
- Identify which workflow step contains the pattern
- Apply minimal targeted edit: fix deprecated path, add missing severity label, correct variable reference

**Target: `manifest`** (`_bmad/_config/*.csv`)
- Apply row addition, correction, or removal per report action

**Target: `config`** (config.yaml or similar)
- Apply single field update only — never restructure

After each edit:
- Mark correction as `status: applied` in the in-memory report copy
- Add to `applied_corrections` list

**Gate 3 — Revalidate modified files (Aria lens):**
For each file modified: verify it still passes basic BMAD structure check:
- YAML frontmatter intact (if applicable)
- No broken variable references `{project-root}`, `{communication_language}`
- No deprecated paths introduced

If validation fails → revert that specific correction, move to `failed_corrections`, elevate to high.

---

### Step 5 — Commit & Push

```
git add [all modified files]
git commit -m "fix(flywheel): auto-corrections cycle {today_date}

Applied {count} corrections from flywheel-report.md:
{for each applied: - [severity] target_file: pattern description}

Deferred: {count deferred} corrections to next cycle
High severity (manual review required): {count high}"

git push origin {branch_name}
```

Then create PR at:
`https://github.com/zavrocKk/zav-sandbox/pull/new/{branch_name}`

---

### Step 6 — Append to Flywheel History

Append to `{project-root}/_bmad/_memory/flywheel-history.md`:

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

---

### Step 7 — Output Status

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

---

## SUCCESS METRICS

✅ All gates evaluated before any file modification
✅ Branch created before first edit
✅ Max 5 corrections applied
✅ No high severity corrections auto-applied
✅ All modified files pass Gate 3 revalidation
✅ Commit message includes full correction list
✅ PR created
✅ flywheel-history.md appended
✅ Status line displayed

## FAILURE MODES

❌ Applying corrections directly on main or current branch
❌ Auto-applying high severity items
❌ Committing without Gate 3 revalidation
❌ Skipping flywheel-history.md update
❌ Applying >5 corrections in one cycle
❌ Silent failure — always output status line even if 0 corrections
