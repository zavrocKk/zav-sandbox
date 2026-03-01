# AGENTS.md — zav-sandbox

> Universal agent guidance file. Read this first before navigating or modifying this repository.
> Compatible with: GitHub Copilot, OpenAI Codex, Claude Code, and any LLM-based coding agent.

## What Is This Project?

**zav-sandbox** is a BMAD (Better Method for AI-Driven Development) framework enhancement project.
The goal is to continuously improve the BMAD multi-agent system — optimizing token usage, agent orchestration, workflows, and developer experience.

**Owner**: Mon Seigneur  
**Communication language**: Français (all user-facing output must be in French)  
**Output folder**: `_bmad-output/`

---

## Repository Structure

```
_bmad/                        ← BMAD framework root
  _config/                    ← Manifests and config (CSV-based registry)
    agent-manifest.csv        ← All agents: name, persona, capabilities
    workflow-manifest.csv     ← All workflows: name, description, path
    task-manifest.csv         ← All tasks: name, description, path
    agent-delegation-matrix.csv ← Request routing rules
  _memory/                    ← Persistent agent memory across sessions
  core/                       ← Core module: bmad-master agent + orchestration workflows
    agents/bmad-master.md     ← Primary orchestrator agent
    config.yaml               ← Global project config (user_name, language, output_folder)
    tasks/                    ← Reusable tasks (editorial review, help, indexing, sharding)
    workflows/                ← Core workflows (party-mode, delegation, brainstorming, git)
  bmb/                        ← BMB module: agent/module/workflow builders
    agents/                   ← Bond (agent-builder), Morgan (module-builder), Wendy (workflow-builder)
    workflows/agent/          ← Create, edit, validate agents
    workflows/module/         ← Create, edit, validate modules
    workflows/workflow/       ← Create, edit, validate, rework workflows
  cis/                        ← CIS module: creative/innovation/storytelling agents
    agents/                   ← Carson, Dr. Quinn, Maya, Victor, Caravaggio, Sophia
    workflows/                ← design-thinking, innovation-strategy, problem-solving, storytelling
  tea/                        ← TEA module: test architecture
    agents/tea.md             ← Murat (test architect)
    workflows/testarch/       ← ATDD, CI, coverage, NFR, framework, review, trace workflows
_bmad-output/                 ← Generated artifacts (never commit large outputs to main)
.github/
  copilot-instructions.md     ← GitHub Copilot-specific instructions (subset of this file)
AGENTS.md                     ← This file — universal agent entry point
```

---

## How to Navigate

| Goal | Where to look |
|---|---|
| Find an agent | `_bmad/_config/agent-manifest.csv` |
| Find a workflow | `_bmad/_config/workflow-manifest.csv` |
| Find a task | `_bmad/_config/task-manifest.csv` |
| Understand routing rules | `_bmad/_config/agent-delegation-matrix.csv` |
| Global config (user, language) | `_bmad/core/config.yaml` |
| Agent memory/state | `_bmad/_memory/` |
| Generated outputs | `_bmad-output/` |

---

## Key Conventions

### Config Loading
- **Always** load `_bmad/core/config.yaml` first — it defines `{user_name}`, `{communication_language}`, `{output_folder}`
- If config is already in session context, **never reload it** — use the cached values
- `{project-root}` resolves to the workspace root at runtime

### Agent Activation
- All agent requests **must** route through `_bmad/core/workflows/delegation/workflow.md`
- Never activate an agent directly without checking the delegation matrix first
- BMad Master (`_bmad/core/agents/bmad-master.md`) is the entry point for all operations

### Workflow Execution
- `.md` workflows → execute directly by reading and following the file
- `.yaml` workflows → require the workflow engine: load `_bmad/core/tasks/workflow.xml` first
- Load steps **JIT** (just-in-time) — never preload multiple steps at once

### Party Mode (Smart JIT)
- BMad Master is the sole orchestrator — no separate coordinator agent
- Initialization loads only a lightweight index (name, icon, capabilities) — NOT full profiles
- Per turn: score agents against topic keywords, select 2-3 max, load their CSV row, generate response, discard profile data
- Full agent `.md` files are never loaded during party mode unless explicitly requested

### Git Workflow (MANDATORY)
- **Never commit directly to `main`**
- Always create a branch: `feature/{description}-{date}` or `fix/{description}-{date}`
- Always create a PR after pushing
- Full workflow: `_bmad/core/workflows/git-workflow/workflow.md`

### Token Efficiency Rules
- Load resources at runtime only — never preload
- Config resolved once per session — do not reload
- Agent profiles loaded per-turn in party mode — discarded after each turn
- Prefer CSV rows over full `.md` files for personality data in party mode

---

## Available Agents (Summary)

| Agent | Persona | Module | Specialty |
|---|---|---|---|
| bmad-master | 🧙 BMad Master | core | Orchestration, task execution, party mode |
| agent-builder | 🤖 Bond | bmb | Create/edit/validate BMAD agents |
| module-builder | 🏗️ Morgan | bmb | Create/edit/validate BMAD modules |
| workflow-builder | 🔄 Wendy | bmb | Create/edit/validate BMAD workflows |
| brainstorming-coach | 🧠 Carson | cis | Brainstorming, ideation |
| creative-problem-solver | 🔬 Dr. Quinn | cis | Systematic problem solving |
| design-thinking-coach | 🎨 Maya | cis | Human-centered design |
| innovation-strategist | ⚡ Victor | cis | Innovation strategy |
| presentation-master | 🎨 Caravaggio | cis | Presentations, visual communication |
| storyteller | 📖 Sophia | cis | Narrative, storytelling |
| tea | 🧪 Murat | tea | Test architecture, quality |

---

## Slash Commands (GitHub Copilot Chat)

Type `/bmad-` in Copilot Chat to see all available commands. Key ones:

- `/bmad-master` — Activate BMad Master orchestrator
- `/bmad-help` — Get advice on what to do next
- `/bmad-git-workflow` — Follow mandatory git workflow

---

## Do Not

- ❌ Modify files in `_bmad/_config/` without updating related manifests
- ❌ Commit generated outputs in `_bmad-output/` to main unless explicitly requested
- ❌ Skip the delegation workflow when activating agents
- ❌ Commit directly to `main`
- ❌ Reload config if already resolved in session
