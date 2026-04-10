---
name: gsane-framework
description: Core knowledge of the GSANE multi-agent framework — architecture, modules, conventions, JIT loading, delegation system, and git workflow.
applyTo: "**"
---

# GSANE Framework Knowledge

GSANE (Governance System for AI-Native Execution) is a flat-design multi-agent system running on GitHub Copilot Chat. The active runtime is the 5-agent Strike Team orchestrated by Gsane Master.

## Setup Requirements (one-time per machine)

| Tool | Purpose | Setup command |
|---|---|---|
| **Git** | Branch management, commits, push | `git remote -v` to verify origin |

## PR Body Rule

Every PR MUST have a filled description body. Open the GitHub compare URL, fill the title, and paste the body template into the description field. NEVER submit with an empty description. This is enforced by:
- `validate-pr.yml` CI check (blocks merge if body empty)
- `git-workflow/workflow.md` Step 5 (compare URL + body template)
- `copilot-instructions.md` PR DESCRIPTION convention

## Active Runtime Structure

- `_gsane/agents/` — the 5 active agents: master, bond, architect, dev, qa
- `_gsane/workflows/` — active workflows executed directly from markdown files
- `_gsane/_config/*.yaml` — manifests, routing rules, IDE config, and global metadata
- `.github/prompts/` and `.github/skills/` — active user-facing guidance surfaces

## JIT Loading Protocol

**Load Only What Is Needed, When It Is Needed.** This is the core token-efficiency rule of GSANE.

| Context | What to load | What NOT to load |
|---|---|---|
| Party mode init | The manifest or routing data needed to score the 5 active agents | Full agent `.md` files for every agent |
| Per turn | Only the selected agent file or manifest entries needed for the current turn | All other agent profiles |
| Workflow exec | The workflow file being executed or the targeted YAML manifest | Future steps in advance |
| Config | Once per session from `_gsane/config.yaml` | Never reload if already resolved |

**Signals that JIT is being violated:**
- `unnecessary-load` — file loaded but never referenced after load
- `profile-overload` — multiple agent files loaded when one target agent or manifest entry would suffice
- `config-reload-waste` — `config.yaml` loaded more than once per session
- `redundant-step` — same step or file loaded again after already in context

When any of these signals recur ≥3 times across sessions, the Cognitive Flywheel will auto-apply a correction.

## Key Conventions

- Always load `_gsane/config.yaml` first — defines `{user_name}`, `{communication_language}`, `{output_folder}`
- Config is loaded once per session — never reload if already in context
- `{project-root}` resolves to the workspace root at runtime
- All outputs go to `_gsane-output/`

## JIT Loading Pattern

Agents and workflows are loaded just-in-time — never preloaded:
- Party mode: score active agents from the current manifests, then load only the selected agent guidance needed for that turn
- Full `.md` agent files loaded only when executing a specific workflow
- Config resolved once — cached for entire session

## Delegation System

All agent requests route through `_gsane/workflows/delegation/workflow.md`:
1. Check `_gsane/_config/delegation-matrix.yaml` for routing rules
2. Load target agent
3. Agent executes workflow
4. Log routing decision

Enforcement is strict — no direct agent activation without delegation check.

## Git Workflow

- Never commit to `main` directly
- Branch naming: `feature/{description}-{date}` or `fix/{description}-{date}`
- Always push + create PR after commit
- **PRs MUST have a description** — open the GitHub compare URL, fill the title and paste the body template into the description field before submitting
- Full workflow: `_gsane/workflows/git-workflow/workflow.md`

## Manifests

| File | Purpose |
|---|---|
| `_gsane/_config/agent-manifest.yaml` | Registry of all agents |
| `_gsane/_config/workflow-manifest.yaml` | Registry of all workflows |
| `_gsane/_config/delegation-matrix.yaml` | Request routing rules |
| `_gsane/_config/task-manifest.yaml` | Registry of all tasks |
