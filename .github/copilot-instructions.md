<!-- BMAD:START -->
# BMAD Method — Project Instructions

## Project Configuration

- **Project**: zav-sandbox — BMAD Framework Enhancement Project
- **User**: Mon Seigneur
- **Communication Language**: Français
- **Document Output Language**: Français
- **Output Folder**: `_bmad-output/`

## BMAD Runtime Structure

- **Agent definitions**:
  - `_bmad/core/agents/` — bmad-master (core orchestrator)
  - `_bmad/bmb/agents/` — BMB module (agent-builder, module-builder, workflow-builder)
  - `_bmad/cis/agents/` — CIS module (brainstorming, creative, design-thinking, innovation, presentation, storyteller)
  - `_bmad/tea/agents/` — TEA module (test architect)
- **Workflow definitions**:
  - `_bmad/core/workflows/` — brainstorming, party-mode, delegation, git-workflow, advanced-elicitation
  - `_bmad/bmb/workflows/` — agent/module/workflow creation and validation
  - `_bmad/cis/workflows/` — design-thinking, innovation-strategy, problem-solving, storytelling
  - `_bmad/tea/workflows/` — test architecture workflows
- **Core tasks**: `_bmad/core/tasks/` (help, editorial review, indexing, sharding, adversarial review)
- **Workflow engine**: `_bmad/core/tasks/workflow.xml` (executes YAML-based workflows)
- **Module configurations**: `_bmad/core/config.yaml`, `_bmad/bmb/config.yaml`, `_bmad/cis/config.yaml`, `_bmad/tea/config.yaml`
- **Core configuration**: `_bmad/core/config.yaml`
- **Agent manifest**: `_bmad/_config/agent-manifest.csv`
- **Workflow manifest**: `_bmad/_config/workflow-manifest.csv`
- **Help manifest**: `_bmad/_config/bmad-help.csv`
- **Agent memory**: `_bmad/_memory/`
- **Delegation Matrix**: `_bmad/_config/agent-delegation-matrix.csv`
- **Delegation Workflow**: `_bmad/core/workflows/delegation/workflow.md`
- **Git Workflow**: `_bmad/core/workflows/git-workflow/workflow.md` (standardized commit & PR process)

## Agent Delegation System — MANDATORY ROUTING

**This is CRITICAL:** All capability requests MUST be routed through the Agent Delegation System. No direct execution. Ever.

### The Core Rule

When ANY request comes in that needs an agent:
1. **NEVER execute directly** — This violates the routing system
2. **ALWAYS check the Delegation Matrix first** — Find the right agent
3. **ALWAYS load the target agent** — Follow their activation sequence
4. **ALWAYS route through delegation workflow** — Maintain audit trail

### How Routing Works

```
User Request
    ↓
[Need to access an agent capability]
    ↓
Load: _bmad/core/workflows/delegation/workflow.md
    ↓
Step 1: Analyze request type
    ↓
Step 2: Match against _bmad/_config/agent-delegation-matrix.csv
    ↓
Step 3: Load appropriate agent
    ↓
Step 4: Agent executes their workflow
    ↓
Step 5: Log routing decision
```

### Enforcement Rules

From `_bmad/core/config.yaml`:
- ✅ `delegation.enabled: true` — System is active
- ✅ `delegation.enforcement_mode: strict` — No bypasses allowed
- ✅ `delegation.delegation_required: true` — All requests must route
- ✅ `delegation.agents_can_self_execute: false` — Agents cannot self-dispatch
- ✅ `violations.auto_escalate_on_violation: true` — Violations trigger escalation

### What This Prevents

- ❌ Direct agent activation without routing
- ❌ Bypassing the delegation matrix
- ❌ Executing tasks outside proper workflow
- ❌ Skipping audit trails and governance

## Git Workflow — MANDATORY FOR ALL COMMITS

**This is CRITICAL:** Every commit in this project MUST follow the Git Workflow. No exceptions.

### The Single Rule
- **NEVER commit directly to `main`**
- **ALWAYS create a branch first** (feature/* or fix/*)
- **ALWAYS create a PR after commit**

### Branch Naming
- `feature/{description}-{date}` — New code, updates, deployments
- `fix/{description}-{date}` — Corrections, bug fixes

### Workflow Steps
1. Create feature/fix branch
2. Make changes and commit
3. Push branch to remote
4. Create pull request
5. Merge after review

### Applying to Agents
When any agent or workflow needs to commit changes:
1. Load: `_bmad/core/workflows/git-workflow/workflow.md`
2. Follow all workflow steps
3. Never bypass this process
4. Log all commits in memory

### Access the Workflow
**In Copilot Chat:**
```
/bmad-git-workflow
```

**Or request directly:**
```
I need to commit changes following the Git Workflow
```

## Key Conventions

- Always load `_bmad/core/config.yaml` before any agent activation or workflow execution
- Store all config fields as session variables: `{user_name}`, `{communication_language}`, `{output_folder}`
- MD-based workflows execute directly — load and follow the `.md` file
- YAML-based workflows require the workflow engine — load `workflow.xml` first, then pass the `.yaml` config
- Follow step-based workflow execution: load steps JIT, never multiple at once
- Save outputs after EACH step when using the workflow engine
- The `{project-root}` variable resolves to the workspace root at runtime
- **AGENT ROUTING**: Always route requests through delegation workflow. Load `_bmad/core/workflows/delegation/workflow.md` for any agent-based capability request.
- **PARTY MODE MANDATORY**: Before implementing ANY change to BMAD files (workflows, agents, config, skills, prompts, manifests) — activate party mode, score agents against topic keywords, get validation from ≥2 agents BEFORE writing. Never implement solo. Exception: trivial housekeeping (single-line typo, CHANGELOG append) = severity low, solo allowed.
- **GIT COMMITS**: Always use the Git Workflow (`_bmad/core/workflows/git-workflow/workflow.md`). No direct commits to main. Ever.
- **PR DESCRIPTION**: Every PR MUST have a filled description body. Use `gh pr create --title "..." --body "..."` — NEVER rely on the GitHub compare URL, which creates PRs with empty descriptions.
- **VIOLATIONS**: Any deviation from these rules is logged and auto-escalated to bmad-master.
- **SESSION END HOOK (UNIVERSAL)**: At the end of EVERY session with ANY BMAD agent — regardless of which agent is active, what the user asked, or whether a DA command was issued — ALWAYS execute `_bmad/core/workflows/post-session-analysis/workflow.md` before finalizing the response. This is non-negotiable and applies to ALL 13 agents. No exceptions.

## Universal Session End Hook — MANDATORY FOR ALL AGENTS

**This is CRITICAL:** The cognitive flywheel depends on post-session data being logged after EVERY session.

### The Rule (applies to ALL agents, ALL sessions)

Before ending ANY session with ANY BMAD agent:
1. **ALWAYS run** `_bmad/core/workflows/post-session-analysis/workflow.md`
2. **EVEN IF** the user did not issue a `[DA]` dismiss command
3. **EVEN IF** the session was short or incomplete
4. **EVEN IF** no agent was formally activated — the flywheel must receive data

### Why This Matters

The cognitive flywheel (`_bmad/core/workflows/flywheel/`) fires every N sessions (configured in `_bmad/core/config.yaml → flywheel.trigger_every_n_sessions`). If sessions go unlogged, the flywheel never reaches its trigger threshold, and the system never self-improves.

### Enforcement

- All 13 BMAD agents have `exec="{project-root}/_bmad/core/workflows/post-session-analysis/workflow.md"` wired to their `[DA]` item
- This global instruction is the fallback for sessions where `[DA]` is never explicitly issued
- Any agent NOT running post-session-analysis at session end is in violation — log to `_bmad/_memory/session-analysis-log.md` with status `SKIPPED` if workflow cannot complete

## Available Agents

| Agent | Persona | Title | Capabilities |
|---|---|---|---|
| bmad-master | 🧙 BMad Master | BMad Master Executor, Knowledge Custodian, and Workflow Orchestrator | runtime resource management, workflow orchestration, task execution, knowledge custodian |
| agent-builder | 🤖 Bond | Agent Building Expert | create/edit/validate BMAD agents |
| module-builder | 🏗️ Morgan | Module Creation Master | create/edit/validate BMAD modules |
| workflow-builder | 🔄 Wendy | Workflow Building Master | create/edit/validate BMAD workflows |
| brainstorming-coach | 🧠 Carson | Elite Brainstorming Specialist | brainstorming, ideation, creative techniques |
| creative-problem-solver | 🔬 Dr. Quinn | Master Problem Solver | TRIZ, systematic problem solving, root cause analysis |
| design-thinking-coach | 🎨 Maya | Design Thinking Maestro | human-centered design, empathy mapping, prototyping |
| innovation-strategist | ⚡ Victor | Disruptive Innovation Oracle | innovation strategy, business model disruption |
| presentation-master | 🎨 Caravaggio | Visual Communication Expert | presentations, pitch decks, visual storytelling |
| storyteller | 📖 Sophia | Master Storyteller | narrative, storytelling, brand stories |
| tea | 🧪 Murat | Master Test Architect | test architecture, ATDD, CI/CD, quality gates |
| bmad-optimizer | ⚙️ Léo | BMAD Framework Optimizer | token analysis, session metrics, framework improvement, BMAD evolution |
| qa-bmad | 🔍 Aria | BMAD Quality Assurance Specialist | workflow validation, agent consistency, persona regression detection, BMAD compliance |

## Slash Commands

Type `/bmad-` in Copilot Chat to see all available BMAD workflows and agent activators. Agents are also available in the agents dropdown.
<!-- BMAD:END -->
