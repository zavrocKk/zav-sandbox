# Git Workflow Guide for BMAD Agents

**Applicable to**: All BMAD agents (BMB, CIS, TEA, Core, etc.)  
**Language**: Français  
**Updated**: 2026-03-01

---

## TL;DR - Quick Reference

Every time you need to commit changes:

```
1. Call: /bmad-git-workflow
2. Type: feature (or fix)
3. Description: "What you're changing"
4. Let the workflow handle the rest
```

**That's it.** No more direct commits to main.

---

## The Rules (Non-Negotiable)

### ✅ DO THIS
- ✅ Create a `feature/*` or `fix/*` branch
- ✅ Commit to the feature branch
- ✅ Push the branch
- ✅ Create a PR
- ✅ Merge only after review

### ❌ NEVER DO THIS
- ❌ Commit directly to `main`
- ❌ Push to `main` without a PR
- ❌ Skip branch creation
- ❌ Force push to main
- ❌ Merge without a PR

---

## Git Workflow vs Your Agent Work

Your agent performs its main task (building, creating, solving, etc.). **At the end**, when you have files to commit:

### Your Agent's Final Step Should Be:
```markdown
## Final: Commit Changes

[Brief summary of what was created]

**Files changed/created:**
- file1.md
- file2.yml
- etc.

**Next step:** We need to commit these changes using the Git Workflow.

Type: feature (or fix)
Description: [Your description here]
```

**Then the system loads the Git Workflow** (`_bmad/core/workflows/git-workflow/workflow.md`) and handles everything else.

---

## Branch Naming Explained

### Feature Branch
Use for new features, updates, additions:
```
feature/{category}/{short-description}-{date}
```

**Examples:**
- `feature/bmb/create-new-agent-builder-2026-03-01`
- `feature/docs/update-readme-with-examples-2026-03-01`
- `feature/cis/add-brainstorming-workflow-2026-03-01`
- `feature/core/enhance-workflow-engine-2026-03-01`

### Fix Branch
Use for bug fixes, corrections:
```
fix/{category}/{short-description}-{date}
```

**Examples:**
- `fix/core/correct-config-parsing-error-2026-03-01`
- `fix/docs/fix-broken-link-in-readme-2026-03-01`
- `fix/bmb/resolve-agent-creation-bug-2026-03-01`

---

## Commit Message Format

Keep it structured and clear:

```
{type}({module}): {short description}

{Detailed explanation}
- Change 1
- Change 2
- Change 3
```

**Example:**
```
feature(cis): add innovation-strategist agent

This agent brings strategic thinking to innovation processes:
- Created agent definition with persona
- Added workflows for strategy evaluation
- Integrated with creative-squad team
- Added documentation and examples
```

---

## Workflow Diagram

```
Your Agent Task
    ↓
[Creates/Modifies Files]
    ↓
Agent Output: "Ready to commit"
    ↓
System: Load Git Workflow
    ↓
Step 1: Get commit info (type, description)
    ↓
Step 2: Create branch (feature/* or fix/*)
    ↓
Step 3: Stage & commit changes
    ↓
Step 4: Push to remote
    ↓
Step 5: Create PR on GitHub
    ↓
✅ Done - Changes awaiting review
```

---

## Integration Example

**Agent Output:**
```markdown
## Step 5: Export Configuration

I've created the configuration file.

**Files:**
- _bmad/new-module/config.yaml
- _bmad/new-module/agents/agent-definition.md

**Status:** Ready to commit

---

**Next:** Commit these changes using the Git Workflow

Type: feature
Description: Create new innovation module with agent-builder integration
```

**Then system responds:**
```
Loading Git Workflow from: _bmad/core/workflows/git-workflow/workflow.md

[Git Workflow Step 1: Initialization & Verification]
...
```

---

## What Happens Behind the Scenes

### Git Workflow Does This Automatically

1. **Creates branch** → `feature/innovation/create-new-module-2026-03-01`
2. **Stages files** → `git add .`
3. **Commits** → `git commit -m "feature(innovation): create new innovation module..."`
4. **Pushes** → `git push -u origin feature/...`
5. **Creates PR** → Opens on GitHub automatically
6. **Logs it** → Records in commit history

**Your agent doesn't need to do any of this.** The workflow owns it.

---

## Error Scenarios & Recovery

### Scenario 1: Files Already Committed to Main Somewhere

If somehow files got on main before the workflow:
1. Create the branch anyway
2. The workflow detects uncommitted changes
3. Moves them to the new branch
4. Continues normally

### Scenario 2: Network/Push Issues

The workflow tries, catches the error, and:
1. Informs you of the issue
2. Provides the manual PR link
3. Continues so you can fix it

### Scenario 3: Branch Already Exists

The workflow:
1. Detects it exists
2. Appends timestamp to branch name
3. Creates `feature/...-20260301-1234` instead
4. Continues

---

## Accessing the Workflow

### From User Request
```
Hey, let's commit these changes following the Git Workflow
```

### From Agent Code
In your agent's markdown, add at the end:
```markdown
## Commit Action

**Type:** feature  
**Description:** Brief description of changes  
**Files:** List of files to commit
```

### Direct Command (Copilot Chat)
```
/bmad-git-workflow
```

---

## Audit & History

All commits using this workflow are logged:

**Location**: `{output_folder}/git-commits/`  
**File**: `commit-log-{date}.md`

**Contains:**
- Timestamp
- Branch name
- Commit hash
- Agent/User who triggered it
- PR URL
- Files changed

---

## FAQ

### Q: Can I commit manually outside this workflow?
**A:** No. All commits must follow the workflow. Period. Update the workflow if you need different rules.

### Q: What if I need to commit directly to main?
**A:** You don't. The workflow was designed to prevent exactly this.

### Q: Can agents bypass the workflow?
**A:** Absolutely not. Agents must call the workflow just like users.

### Q: How long does the workflow take?
**A:** 2-3 minutes top. Mostly automated.

### Q: What if there are merge conflicts?
**A:** The workflow flags them. You resolve in the PR, then merge.

### Q: Do I merge the PR myself?
**A:** The workflow can auto-merge, or you can review and merge manually on GitHub.

---

## Compliance Checklist

Before each commit, verify:

- [ ] Branch is not `main`
- [ ] Branch is named `feature/*` or `fix/*` with date
- [ ] Commit message follows format
- [ ] PR has been created
- [ ] PR has description and file list
- [ ] Changes are properly logged

---

**Remember**: This workflow exists to keep your git history clean, traceable, and auditable. Every commit is a decision point. Embrace it.

**Version**: 1.0  
**Enforcement**: Mandatory  
**Last Review**: 2026-03-01
