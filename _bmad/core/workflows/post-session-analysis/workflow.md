---
name: post-session-analysis
description: "Automated post-session hook. Runs silently after every bmad-master session or party mode exit. Léo (bmad-optimizer) logs token patterns and optimization insights. Aria (qa-bmad) logs compliance findings and regression signals. Auto-applies low/medium severity corrections. No user interaction required — appends results to session memory log."
---

# Post-Session Analysis Workflow

**Goal:** Automatically capture session learnings AND apply low/medium severity corrections for continuous BMAD improvement. Runs without interrupting the user — silent, fast, and always-on.

**Your Role:** BMad Master executes this workflow as a background analysis hook at session end. You embody both Léo and Aria briefly to produce their findings, apply eligible corrections, then log everything to persistent memory. The user is NOT prompted for low/medium corrections — only high-severity issues surface.

---

## RULES

- ⚡ SILENT by default — do NOT ask the user questions
- ⏱️ FAST — analysis targets under 7 reasoning steps total
- 📝 APPEND ONLY — never overwrite existing log entries, always append
- 🚫 DO NOT reload config — already resolved in session
- 🚫 DO NOT load any agent .md files — use in-context session knowledge only
- ✅ Log findings even if minimal — a clean session is a valid finding
- ✅ AUTO-APPLY corrections with severity "low" or "medium" — no user prompt needed
- ⚠️ HIGH severity findings → surface to user with single notification, do NOT auto-apply

## SEVERITY CLASSIFICATION

| Severity | Examples | Action |
|---|---|---|
| `low` | Missing CHANGELOG entry, manifest row out of sync, outdated comment | Auto-apply + log |
| `medium` | Deprecated path in workflow, agent description mismatch, stale memory file | Auto-apply + log |
| `high` | Rule violation (commit to main, delegation bypass), breaking schema change | Notify user, no auto-apply |

---

## EXECUTION SEQUENCE

### Step 1 — Build Session Summary (in-context, no file loads)

From the current session context, extract:

- `{session_date}` — today's date (YYYY-MM-DD)
- `{session_type}` — "bmad-master" | "party-mode" | "workflow:{name}"
- `{topics_discussed}` — 3-5 keywords summarizing what was worked on
- `{agents_invoked}` — which agents participated (from context)
- `{workflows_run}` — which workflows were executed (from context)
- `{files_loaded}` — approximate count of files loaded during session
- `{turns_count}` — approximate number of conversation turns

---

### Step 2 — ⚙️ Léo's Token & Optimization Analysis

Acting as Léo (bmad-optimizer), analyze the session for:

**Token waste signals:**
- Was config reloaded more than once? → flag as `config-reload-waste`
- Were full agent .md files loaded when only CSV data was needed? → flag as `profile-overload`
- Were any files loaded but never referenced again? → flag as `unnecessary-load`
- Were any steps repeated that could have been cached? → flag as `redundant-step`

**Optimization opportunities:**
- Any pattern that could be simplified or deferred?
- Any workflow path that felt longer than necessary?

**Format findings as:**
```
LEO_FINDINGS:
  waste_signals: [list or "none"]
  optimization_opportunities: [list or "none"]
  estimated_token_impact: "low | medium | high"
  top_recommendation: "[single most impactful change, or 'none this session']"
```

---

### Step 3 — 🔍 Aria's Quality & Compliance Check

Acting as Aria (qa-bmad), analyze the session for:

**Compliance signals:**
- Were all BMAD rules followed? (JIT loading, no direct agent bypass, config once)
- Were any deprecated paths used? (e.g., `_bmad/bmm/`)
- Were any manifests referenced that might be out of sync?

**Regression signals:**
- Did any agent respond out of character?
- Were any workflow steps skipped or reordered?
- Were any standards violated (e.g., commit to main, direct agent exec without delegation)?

**Format findings as:**
```
ARIA_FINDINGS:
  compliance_status: "PASS | FAIL | WARNING"
  violations: [list or "none"]
  regression_signals: [list or "none"]
  top_finding: "[most urgent issue, or 'all clear']"
```

---

### Step 4 — Auto-Apply Corrections (low + medium severity only)

Before logging, apply all eligible corrections identified in Steps 2 and 3:

**Eligible auto-corrections (apply silently):**

1. **Missing CHANGELOG entry** → Append entry under `[Unreleased]` in `CHANGELOG.md` with format:
   ```
   **[type]** {description of what was done this session}
   - Agent: BMad Master | Workflow: post-session-analysis | Initié par: auto
   - Impact: {files affected}
   ```

2. **Manifest row out of sync** (agent or workflow added but not in CSV) → Append correct row to the relevant manifest CSV

3. **Deprecated path reference** (e.g., `_bmad/bmm/` in any file) → Replace with correct path

4. **Stale comment or outdated description** in manifest → Update in-place

**For each correction applied:**
- Note it in `AUTO_CORRECTIONS` list for logging
- Apply the file edit directly (no branch — these are minor housekeeping fixes)

**Do NOT auto-apply if:**
- The fix requires creating a new agent/workflow/module (route to Bond/Wendy/Morgan instead)
- The fix changes any rule, schema, or convention (severity = high)
- You are uncertain about the correct value

**High severity findings** → after completing all steps, display single line:
```
⚠️ [post-session] Problème détecté nécessitant ton attention : {finding}
```

---

### Step 5 — Append to Session Memory Log

Load path: `{project-root}/_bmad/_memory/session-analysis-log.md`

Append the following block to the END of the file (never overwrite):

```markdown
---
## Session: {session_date} | Type: {session_type}
**Topics:** {topics_discussed}
**Agents invoked:** {agents_invoked}
**Workflows run:** {workflows_run}
**Files loaded (est.):** {files_loaded} | **Turns:** {turns_count}

### ⚙️ Léo — Token & Optimization
- Waste signals: {LEO_FINDINGS.waste_signals}
- Opportunities: {LEO_FINDINGS.optimization_opportunities}
- Token impact: {LEO_FINDINGS.estimated_token_impact}
- Top recommendation: {LEO_FINDINGS.top_recommendation}

### 🔍 Aria — Quality & Compliance
- Compliance: {ARIA_FINDINGS.compliance_status}
- Violations: {ARIA_FINDINGS.violations}
- Regression signals: {ARIA_FINDINGS.regression_signals}
- Top finding: {ARIA_FINDINGS.top_finding}

### 🔧 Auto-corrections appliquées
- {AUTO_CORRECTIONS list or "aucune"}
---
```

---

### Step 6 — Output Single Status Line

Display to user (in {communication_language}):

```
📊 Analyse post-session terminée — {AUTO_CORRECTIONS.count} correction(s) appliquée(s) — résultats dans _bmad/_memory/session-analysis-log.md
```

Then return control to whatever triggered this workflow (DA dismiss or party-mode exit).

---

## SUCCESS METRICS

✅ Session summary extracted from context (no file loads)
✅ Léo findings produced with waste signals and recommendation
✅ Aria findings produced with compliance status
✅ Low/medium corrections auto-applied before logging
✅ Log entry appended to session-analysis-log.md with AUTO_CORRECTIONS section
✅ Single status line displayed with correction count, then silent exit
✅ Total workflow execution: ≤ 7 reasoning steps

## FAILURE MODES

❌ Asking the user questions during analysis (except high-severity notification)
❌ Auto-applying high-severity findings without user confirmation
❌ Reloading config or agent files already in context
❌ Overwriting existing log entries (append only)
❌ Generating a wall of text — this is a background hook, not a report
❌ Blocking the session exit — analysis failure must not prevent DA/exit
