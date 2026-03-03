# AGENTS.md — zav-sandbox

> Universal agent guidance file. Read this first before navigating or modifying this repository.
> Compatible with: GitHub Copilot, OpenAI Codex, Claude Code, and any LLM-based coding agent.

## What Is This Project?

**zav-sandbox** is a GSANE (Governance System for AI-Native Execution) framework enhancement project.
The goal is to continuously improve the GSANE multi-agent system — optimizing token usage, agent orchestration, workflows, and developer experience.

**Owner**: Mon Seigneur  
**Communication language**: Français (all user-facing output must be in French)  
**Output folder**: `_gsane-output/`

---

## Repository Structure

```
_gsane/                       ← GSANE framework root
  _config/                    ← Manifests and config (CSV-based registry)
    agent-manifest.csv        ← All agents: name, persona, capabilities
    workflow-manifest.csv     ← All workflows: name, description, path
    task-manifest.csv         ← All tasks: name, description, path
    agent-delegation-matrix.csv ← Request routing rules
  _memory/                    ← Persistent agent memory across sessions
    failure-museum.md         ← Catalogue des défaillances passées (FM-001+)
    decision-log.md           ← Journal des décisions architecturales (DL-001+)
    session-analysis-log.md   ← Post-session analysis logs
  core/                       ← Core module: gsane-master agent + orchestration workflows
    agents/gsane-master.md    ← Primary orchestrator agent
    config.yaml               ← Global project config (user_name, language, output_folder)
    tasks/                    ← Reusable tasks (editorial review, help, indexing, sharding)
    workflows/                ← Core workflows (party-mode, delegation, brainstorming, git, cc-verify)
  bmb/                        ← BMB module: agent/module/workflow builders
    agents/                   ← Bond (agent-builder), Morgan (module-builder), Wendy (workflow-builder)
    workflows/agent/          ← Create, edit, validate agents
    workflows/module/         ← Create, edit, validate modules
    workflows/workflow/       ← Create, edit, validate, rework workflows
  bmm/                        ← BMM module: business methodology agents (analyst→dev pipeline)
    agents/                   ← analyst, pm, architect, sm, ux-designer, dev, qa, tech-writer, quick-flow-solo-dev
    workflows/                ← Full product lifecycle: analysis, planning, solutioning, implementation
    data/                     ← project-context-template.md
    teams/                    ← default-party.csv, team-fullstack.yaml
  cis/                        ← CIS module: creative/innovation/storytelling agents
    agents/                   ← Carson, Dr. Quinn, Maya, Victor, Caravaggio, Sophia
    workflows/                ← design-thinking, innovation-strategy, problem-solving, storytelling
  tea/                        ← TEA module: test architecture
    agents/tea.md             ← Murat (test architect)
    workflows/testarch/       ← ATDD, CI, coverage, NFR, framework, review, trace workflows
_gsane-output/                ← Generated artifacts (never commit large outputs to main)
.github/
  copilot-instructions.md     ← GitHub Copilot-specific instructions (subset of this file)
AGENTS.md                     ← This file — universal agent entry point
```

---

## How to Navigate

| Goal | Where to look |
|---|---|
| Find an agent | `_gsane/_config/agent-manifest.csv` |
| Find a workflow | `_gsane/_config/workflow-manifest.csv` |
| Find a task | `_gsane/_config/task-manifest.csv` |
| Understand routing rules | `_gsane/_config/agent-delegation-matrix.csv` |
| Global config (user, language) | `_gsane/core/config.yaml` |
| Agent memory/state | `_gsane/_memory/` |
| Past failures & decisions | `_gsane/_memory/failure-museum.md`, `_gsane/_memory/decision-log.md` |
| Generated outputs | `_gsane-output/` |

---

## Key Conventions

### Config Loading
- **Always** load `_gsane/core/config.yaml` first — it defines `{user_name}`, `{communication_language}`, `{output_folder}`
- If config is already in session context, **never reload it** — use the cached values
- `{project-root}` resolves to the workspace root at runtime

### Agent Activation
- All agent requests **must** route through `_gsane/core/workflows/delegation/workflow.md`
- Never activate an agent directly without checking the delegation matrix first
- Gsane Master (`_gsane/core/agents/gsane-master.md`) is the entry point for all operations

### Workflow Execution
- `.md` workflows → execute directly by reading and following the file
- `.yaml` workflows → require the workflow engine: load `_gsane/core/tasks/workflow.xml` first
- Load steps **JIT** (just-in-time) — never preload multiple steps at once

### Party Mode (Smart JIT)
- Gsane Master is the sole orchestrator — no separate coordinator agent
- Initialization loads only a lightweight index (name, icon, capabilities) — NOT full profiles
- Per turn: score agents against topic keywords, select 2-3 max, load their CSV row, generate response, discard profile data
- Full agent `.md` files are never loaded during party mode unless explicitly requested

### Git Workflow (MANDATORY)
- **Never commit directly to `main`**
- Always create a branch: `feature/{description}-{date}` or `fix/{description}-{date}`
- 1 branch = 1 logical unit of change (see `CONTRIBUTING.md §3`)
- Always create a PR after pushing
- Full workflow: `_gsane/core/workflows/git-workflow/workflow.md`

### Token Efficiency Rules
- Load resources at runtime only — never preload
- Config resolved once per session — do not reload
- Agent profiles loaded per-turn in party mode — discarded after each turn
- Prefer CSV rows over full `.md` files for personality data in party mode

### Governance Rules
- **PRE-EXECUTION GATE**: Before any GSANE action, check the delegation matrix — solo execution = violation
- **Plan/Act Mode**: say `[PLAN]` to structure before acting, `[ACT]` to execute
- **[THINK]**: say `[THINK]` for deep deliberation on HIGH severity decisions (≥3 options)
- **Completion Contract**: run `[CC]` or `/gsane-cc-verify` before declaring any task done
- **Failure Museum**: check `_gsane/_memory/failure-museum.md` before implementing — avoid repeating past failures
- **Solo Trip Wire**: at the exact moment a file-write is about to be called on any GSANE artifact — STOP and declare: (1) target file, (2) trivial per closed list or not, (3) agents who validated. No validation → abort and activate party mode. Read-only operations exempt.

---

## Available Agents (Summary)

### Core & Governance

| Agent | Persona | Module | Specialty |
|---|---|---|---|
| gsane-master | 🧙 Gsane Master | core | Orchestration, task execution, party mode, Plan/Act, [THINK] |
| gsane-optimizer | ⚙️ Léo | core | Token analysis, GSANE optimization, framework improvement |
| agent-builder | 🤖 Bond | bmb | Create/edit/validate GSANE agents |
| module-builder | 🏗️ Morgan | bmb | Create/edit/validate GSANE modules |
| workflow-builder | 🔄 Wendy | bmb | Create/edit/validate GSANE workflows |
| qa-gsane | 🔍 Aria | bmb | GSANE quality assurance, persona regression, workflow compliance |
| tea | 🧪 Murat | tea | Test architecture, ATDD, CI/CD, quality gates |

### BMM Module — Business Methodology

| Agent | Persona | Module | Specialty |
|---|---|---|---|
| analyst | 📊 Mary | bmm | Market research, competitive analysis, requirements elicitation |
| pm | 📋 John | bmm | PRD creation, user stories, stakeholder alignment |
| architect | 🏗️ Winston | bmm | System design, distributed systems, API design |
| sm | 🏃 Bob | bmm | Sprint planning, scrum ceremonies, backlog management |
| dev | 💻 Amelia | bmm | Story execution, TDD, code implementation |
| ux-designer | 🎨 Sally | bmm | User research, interaction design, UX patterns |
| qa | 🧪 Quinn | bmm | Quick test automation, E2E coverage (simple projects) |
| tech-writer | 📚 Paige | bmm | Documentation, Mermaid diagrams, standards compliance |
| quick-flow-solo-dev | 🚀 Barry | bmm | Rapid spec+dev cycle for small-medium features |

### CIS Module — Creative & Innovation

| Agent | Persona | Module | Specialty |
|---|---|---|---|
| brainstorming-coach | 🧠 Carson | cis | Brainstorming, ideation |
| creative-problem-solver | 🔬 Dr. Quinn | cis | Systematic problem solving |
| design-thinking-coach | 🎨 Maya | cis | Human-centered design |
| innovation-strategist | ⚡ Victor | cis | Innovation strategy |
| presentation-master | 🎨 Caravaggio | cis | Presentations, visual communication |
| storyteller | 📖 Sophia | cis | Narrative, storytelling |

---

## Slash Commands (GitHub Copilot Chat)

Type `/gsane-` in Copilot Chat to see all available commands. Key ones:

- `/gsane-master` — Activate Gsane Master orchestrator
- `/gsane-help` — Get advice on what to do next
- `/gsane-git-workflow` — Follow mandatory git workflow
- `/gsane-cc-verify` — Run Completion Contract before closing a task

---

## Do Not

- ❌ Modify files in `_gsane/_config/` without updating related manifests
- ❌ Commit generated outputs in `_gsane-output/` to main unless explicitly requested
- ❌ Skip the delegation workflow when activating agents
- ❌ Bypass the PRE-EXECUTION GATE — always check delegation matrix first
- ❌ Commit directly to `main`
- ❌ Put multiple unrelated changes on the same branch
- ❌ Reload config if already resolved in session
- ❌ Declare a task done without running the Completion Contract (`[CC]`)
