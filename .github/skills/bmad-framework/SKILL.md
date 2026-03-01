---
name: bmad-framework
description: Core knowledge of the BMAD multi-agent framework — architecture, modules, conventions, JIT loading, delegation system, and git workflow.
applyTo: "**"
---

# BMAD Framework Knowledge

BMAD (Better Method for AI-Driven Development) is a multi-agent system running on GitHub Copilot Chat. Agents are organized in modules and orchestrated by BMad Master.

## Module Structure

- `core/` — BMad Master orchestrator + shared tasks + core workflows
- `bmb/` — Builder agents (agent-builder, module-builder, workflow-builder)
- `cis/` — Creative/Innovation/Storytelling agents
- `tea/` — Test architecture agent (Murat)

## JIT Loading Protocol

**Load Only What Is Needed, When It Is Needed.** This is the core token-efficiency rule of BMAD.

| Context | What to load | What NOT to load |
|---|---|---|
| Party mode init | CSV index (4 fields: name, icon, capabilities, path) | Full agent `.md` files |
| Per turn | 1 CSV row for the selected agent only | All other agent profiles |
| Workflow exec | The workflow file being executed | Future steps in advance |
| Config | Once per session from `core/config.yaml` | Never reload if already resolved |

**Signals that JIT is being violated (tracked by Léo):**
- `unnecessary-load` — file loaded but never referenced after load
- `profile-overload` — full agent `.md` loaded when CSV row would suffice
- `config-reload-waste` — `config.yaml` loaded more than once per session
- `redundant-step` — same step or file loaded again after already in context

When any of these signals recur ≥3 times across sessions, the Cognitive Flywheel will auto-apply a correction.

## Key Conventions

- Always load `_bmad/core/config.yaml` first — defines `{user_name}`, `{communication_language}`, `{output_folder}`
- Config is loaded once per session — never reload if already in context
- `{project-root}` resolves to the workspace root at runtime
- All outputs go to `_bmad-output/`

## JIT Loading Pattern

Agents and workflows are loaded just-in-time — never preloaded:
- Party mode: load lightweight CSV index at init, load one CSV row per turn, discard after turn
- Full `.md` agent files loaded only when executing a specific workflow
- Config resolved once — cached for entire session

## Delegation System

All agent requests route through `_bmad/core/workflows/delegation/workflow.md`:
1. Check `_bmad/_config/agent-delegation-matrix.csv` for routing rules
2. Load target agent
3. Agent executes workflow
4. Log routing decision

Enforcement is strict — no direct agent activation without delegation check.

## Git Workflow

- Never commit to `main` directly
- Branch naming: `feature/{description}-{date}` or `fix/{description}-{date}`
- Always push + create PR after commit
- Full workflow: `_bmad/core/workflows/git-workflow/workflow.md`

## Manifests

| File | Purpose |
|---|---|
| `_bmad/_config/agent-manifest.csv` | Registry of all agents |
| `_bmad/_config/workflow-manifest.csv` | Registry of all workflows |
| `_bmad/_config/agent-delegation-matrix.csv` | Request routing rules |
| `_bmad/_config/task-manifest.csv` | Registry of all tasks |
