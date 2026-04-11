# Git Workflow

**Workflow ID:** git-workflow
**Trigger:** Any agent needing to commit changes to GSANE artifacts.
**Enforcement:** Mandatory — zero exceptions. Never commit to `main`.

---

## STEP 1 — Verify current branch

Run: `git branch --show-current`

- If on `main` → continue to Step 2 (create branch)
- If already on `feature/*` or `fix/*` → run: `gh pr list --head $(git branch --show-current) --state open`
  - If an **open** PR exists → skip to Step 3
  - If **no open PR** (merged or none) → continue to Step 2 (create a NEW branch from `origin/main`). Never reuse a branch whose PR was already merged.

## STEP 2 — Create branch

Branch naming convention:
- New code / updates → `feature/{description}-{YYYY-MM-DD}`
- Fixes / corrections → `fix/{description}-{YYYY-MM-DD}`

```bash
git checkout -b feature/my-description-2025-01-01
```

## STEP 3 — Stage and commit

Stage only the relevant files:

```bash
git add <files>
git commit -m "type: short description of change"
```

Commit message format: `type: description` (e.g., `fix: remove dead path refs in agent files`)

## STEP 4 — Push branch

```bash
git push -u origin HEAD
```

## STEP 5 — Create Pull Request

Open a PR on GitHub:
- **Title:** Match the commit message
- **Description:** Must NOT be empty. Include:
  - What changed
  - Why it was needed
  - Files affected
  - Quality Gate status (`bash gsane.sh validate` result)

**NEVER submit with an empty PR description.**

## STEP 5b — Human approval before merge (MANDATORY)

After creating the PR and CI checks pass:
1. **STOP** — Present the PR URL, CI status, and diff summary to the user.
2. **WAIT** for explicit user approval ("merge", "go", "approuvé", or equivalent).
3. **NEVER** execute `gh pr merge` or any merge command without the user's explicit green light in the current exchange.

This step is **non-negotiable**. The user is part of the team — no agent may bypass human review.

**Violations:** Merging without user approval is logged to `_gsane/_memory/failure-museum.md` as a `GOVERNANCE-VIOLATION` and auto-escalated.

## STEP 6 — Merge (after approval)

Only after Step 5b approval:

```bash
gh pr merge <number> --squash --delete-branch
```

## STEP 7 — Log completion

Append a line to `CHANGELOG.md` documenting the change.

---

**Violations:** Any commit directly to `main` is logged to `_gsane/_memory/failure-museum.md` and escalated to Master. Any merge without human approval is a `GOVERNANCE-VIOLATION`.
