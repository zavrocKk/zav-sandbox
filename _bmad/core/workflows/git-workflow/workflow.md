---
name: git-workflow
description: 'Standardized Git workflow for all commits. Creates feature/fix branches, commits changes, updates changelog, and creates PRs. Use for ALL code changes across the project.'
context_file: ''
---

# Git Workflow — Standardized Commit & Pull Request Process

**Goal:** Enforce consistent, traceable git history across all project commits

**Your Role:** You are a Git Workflow Guardian. You ensure EVERY commit (from any agent or user action) follows the standardized branching strategy with proper CHANGELOG updates, commits, and PR creation. No commits go directly to `main`.

**Critical Rules:**
1. **NEVER commit directly to `main`**
2. **ALWAYS create a feature or fix branch first**
3. **ALWAYS update CHANGELOG.md before committing**
4. **ALWAYS create a PR after committing**
5. **Branch naming must reflect commit type**: `feature/*` for new code/updates, `fix/*` for corrections
6. **Apply to ALL commits**: past, present, future, and all agents

**Commit Type Classification:**
- **feature**: New functionality, updates, deployments, additions, enhancements
- **fix**: Bug fixes, corrections, refactoring, error resolution

---

## WORKFLOW ARCHITECTURE

This uses **sequential validation** for disciplined execution:

- Branch creation with type-based naming
- Change verification before commit
- CHANGELOG update and validation
- PR creation with automatic linking
- PR review and merge protocol
- Document state in git history

---

## INITIALIZATION

### Configuration Loading

Load config from `{project-root}/_bmad/core/config.yaml` and resolve:

- `user_name`, `communication_language`, `project_root`
- Current branch should be `main` (verify before starting)
- Remote should be `origin`

### Paths & Variables

- `project_root` = `{project-root}`
- `repo_url` = Get from `git remote -v` (origin/fetch)
- `output_folder` = `{project-root}/_bmad-output`
- `changelog_path` = `{project-root}/CHANGELOG.md`

---

## WORKFLOW STEPS

### Step 1: Initialization & Verification

**What do we need to know?**
- What type of commit is this? (feature | fix)
- What is the commit description? (short, clear description)
- What files will be changed/added?
- Which module(s) are affected? (core | bmb | cis | tea | docs | config)

**System Actions:**
1. Verify current branch is `main`
2. Run `git status` to check for uncommitted changes
3. Load commit context from user or agent

**Output:**
- Confirm all prerequisites met
- Display: commit type, description, affected files, modules

---

### Step 2: Create Feature/Fix Branch

**Branch Naming Convention:**
```
feature/{type}/{description}-{date}
fix/{type}/{description}-{date}
```

**Examples:**
- `feature/docs/update-readme-2026-03-01`
- `feature/core/add-new-workflow-2026-03-01`
- `fix/bmad/fix-config-parsing-2026-03-01`
- `fix/docs/correct-typo-2026-03-01`

**System Actions:**
1. Create branch: `git checkout -b {branch_name}`
2. Verify branch creation: `git branch --show-current`
3. Display: "Branch created: {branch_name}"

**Output:**
- Confirm successful branch creation
- Show active branch

---

### Step 3: Make Changes & Commit

**User/Agent Actions:**
- Implement changes in code/files
- Save all modifications

**System Actions:**
1. Run `git status` to verify changes
2. Stage changes: `git add {files}` or `git add .`
3. Create commit: `git commit -m "{type}({category}): {description}"`

**Commit Message Format:**
```
{type}({category}): {description}

Detailed explanation (optional)
- Change 1
- Change 2
```

**Examples:**
```
feature(core): add git-workflow to BMad system

- Created standardized commit workflow
- Added branch naming conventions
- Implemented CHANGELOG integration

fix(docs): correct README link formatting

- Fixed broken links in documentation
```

**Output:**
- Display commit hash and message
- Show changed files count
- Confirm commit success

---

### Step 3.5: Update CHANGELOG.md (MANDATORY)

**⚠️ CRITICAL STEP - DO NOT SKIP**

This step ensures every commit is tracked and auditable.

**CHANGELOG Requirements:**

1. **Load CHANGELOG.md**: `{project_root}/CHANGELOG.md`

2. **Find [Unreleased] section** at the top

3. **Identify module** for this change:
   - `### Core` — Changes to `_bmad/core/`
   - `### BMB` — Changes to `_bmad/bmb/`
   - `### CIS` — Changes to `_bmad/cis/`
   - `### TEA` — Changes to `_bmad/tea/`
   - `### Config` — Changes to configs
   - `### Docs` — Changes to documentation

4. **Add new entry** to appropriate module section:
   ```
   - `[{type}]({module}): {description}` - {agent_name_or_user}
   ```

5. **Format examples:**
   ```markdown
   - `[feature](core): implement agent delegation system` - Bond, Wendy, Morgan
   - `[fix](bmb): resolve validation bug` - Wendy
   - `[docs](core): update README` - GitHub Copilot
   ```

6. **Validation:**
   - ✅ Entry is in [Unreleased] section
   - ✅ Module is correctly categorized
   - ✅ Format follows convention
   - ✅ Agent/user attribution is clear

7. **Save and stage:**
   ```bash
   git add CHANGELOG.md
   ```

**System Actions:**
1. Verify CHANGELOG.md exists
2. Check for [Unreleased] section
3. Confirm entry format
4. Stage CHANGELOG.md with other changes
5. Display: "CHANGELOG.md updated - entry added"

**Output:**
- ✅ CHANGELOG updated successfully
- ✅ Entry visible and formatted correctly
- ✅ Ready for commit in next step

**IF CHANGELOG UPDATE MISSING:**
- ⚠️ Workflow flags as incomplete
- ⚠️ Cannot proceed to Step 4 without CHANGELOG update
- ⚠️ Violation logged and escalated to bmad-master

---

### Step 4: Push Branch to Remote

**System Actions:**
1. Push branch: `git push -u origin {branch_name}`
2. Verify push: `git log --oneline -3`
3. Display: "Branch pushed to origin/{branch_name}"

**Output:**
- Confirm remote upload
- Show commit details

---

### Step 5: Create Pull Request

**System Actions:**
1. Generate PR title from commit message
2. Generate PR description from commit details and changed files
3. Open PR on GitHub: `https://github.com/zavrocKk/zav-sandbox/compare/main...{branch_name}`
4. Display PR URL to user

**PR Template:**
```
## Description
{commit description}

## Type of Change
- [ ] ✨ Feature (new functionality)
- [ ] 🐛 Fix (bug fix)
- [ ] 📚 Documentation
- [ ] 🔧 Configuration

## Changed Files
- {file1}
- {file2}
- CHANGELOG.md (required)

## CHANGELOG Entry
- `[{type}]({module}): {description}` - {agent}

## Related Issues
Closes #(issue number if applicable)

## Checklist
- [x] CHANGELOG.md has been updated
- [ ] Code follows project conventions
- [ ] Comments added for complex logic
- [ ] Documentation updated
```

**Output:**
- Display PR creation confirmation
- Show PR URL
- Provide link for manual review if needed

---

### Step 6: Merge Protocol & Confirmation

**Decision Point:**
- Auto-merge: Configured to merge on approval
- Manual review: PR ready for user/reviewer validation

**Merge Requirements:**
- ✅ All checks passing
- ✅ CHANGELOG.md includes entry
- ✅ PR reviewed and approved
- ✅ No merge conflicts

**Final Actions:**
1. Verify PR status
2. Display merge instructions if manual approval needed
3. Log workflow completion
4. Verify CHANGELOG.md now in main

**Output:**
- Workflow summary
- Confirmation of changes in main branch
- CHANGELOG.md successfully merged

---

## POST-WORKFLOW VALIDATION

### Pull Requests History

All PRs are tracked and stored in:
- GitHub PR history: https://github.com/zavrocKk/zav-sandbox/pulls
- Local git history: `git log --oneline --all`
- Project CHANGELOG: `CHANGELOG.md` in root

### Commit History

View all commits following this workflow:
```bash
# See all commits with branch info
git log --oneline --all --graph --decorate

# See only merged commits to main
git log --oneline main

# View CHANGELOG entries
cat CHANGELOG.md
```

### CHANGELOG Verification

```bash
# Verify CHANGELOG has entry for recent commits
cat CHANGELOG.md | grep -A 20 "[Unreleased]"
```

---

## AGENT INTEGRATION

**All BMAD Agents MUST use this workflow for commits:**

1. **Before any commit**, agents load this workflow
2. Agents provide: commit type, description, affected files, module
3. **Step 3.5 is MANDATORY** — CHANGELOG must be updated
4. Workflow engine handles: branching, committing, CHANGELOG, PR creation
5. Agent continues with next task after workflow completes

**Integration point in agent files:**
```markdown
## Commit Action

This step requires the Git Workflow. Load: `_bmad/core/workflows/git-workflow/workflow.md`

Type: feature | fix
Module: core | bmb | cis | tea | docs | config
Description: [Short description of changes]
Files: [List affected files]
```

---

## ERROR HANDLING

### CHANGELOG Not Updated
- **Violation**: Step 3.5 incomplete
- **Action**: Workflow cannot proceed to Step 4
- **Resolution**: Update CHANGELOG.md and retry
- **Escalation**: Logged and reported

### Branch Already Exists
- Append timestamp or random suffix
- Retry creation
- Confirm with user

### Uncommitted Changes on Main
- Stash changes: `git stash`
- Create branch
- Apply changes: `git stash pop`
- Continue workflow

### Push Failed
- Check network connectivity
- Run `git pull` to sync
- Retry push
- Display error for manual intervention

### PR Creation Failure
- Verify repository access
- Check branch exists on remote
- Provide manual PR link
- Continue workflow anyway

---

## DOCUMENTATION & AUDIT

All workflows are logged in:
- **Output Folder**: `{output_folder}/git-commits/`
- **File Format**: `commit-log-{date}.md`
- **CHANGELOG**: `{project_root}/CHANGELOG.md` (main artifact)

Each log contains:
- Timestamp
- Branch name
- Commit hash
- Files changed
- CHANGELOG entry
- PR URL
- Agent/User who initiated

---

## ACTIVATION

To activate this workflow from any agent or user request:

**Command in Copilot Chat:**
```
/bmad-git-workflow
```

**Or directly:**
```
Let's use the Git Workflow to commit these changes
```

**Or from agent output:**
```
Agent: "I need to commit these changes"
System: Load git-workflow/workflow.md and proceed with Step 1
```

---

**Version**: 2.0 (with CHANGELOG integration)  
**Last Updated**: 2026-03-01  
**Language**: Français  
**Applies to**: All commits, all agents, all users  
**CHANGELOG Required**: YES — Step 3.5 is mandatory
