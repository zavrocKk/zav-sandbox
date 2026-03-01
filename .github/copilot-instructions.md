<!-- GSANE:START -->
# GSANE Method — Project Instructions

## ⛔ PRE-EXECUTION GATE — MANDATORY BEFORE ANY ACTION

**This gate fires BEFORE every task, every command, every file edit, no exceptions.**

Before producing any output or taking any action, the AI MUST check these 3 questions in order:

1. **Does this request involve any GSANE capability, agent, validation, test, CI check, file modification, or implementation?**
   - If YES → proceed to step 2
   - If NO (pure explanation/conversation with no action) → proceed normally

2. **Is this request covered by the Delegation Matrix?**
   - Load `_gsane/_config/agent-delegation-matrix.csv`
   - Match request keywords against `trigger_keywords` column
   - If match found → load target agent, route through delegation workflow
   - If no match → escalate to gsane-master, DO NOT self-execute

3. **Am I about to execute solo what an agent should execute?**
   - If yes → STOP, load delegation workflow, route correctly
   - Solo execution = violation — auto-escalate to gsane-master

**Keyword coverage table (non-exhaustive — always check the full matrix):**

| Trigger words | Target agent |
|---|---|
| tester, valider, run tests, check CI, vérifier le projet, smoke test, regression | 🧪 Murat (TEA) |
| validate agent/workflow, qa gsane, persona check, manifest sync | 🔍 Aria (qa-gsane) |
| create/edit agent, workflow, module | 🤖 Bond / 🔄 Wendy / 🏗️ Morgan |
| implement, modifier, fix, apply changes | 🧙 Gsane Master (party mode) |
| optimize gsane, token usage | ⚙️ Léo (gsane-optimizer) |

> ⚠️ **If this gate is not applied, the response is in violation of GSANE governance rules.**

---

## Project Configuration

- **Project**: zav-sandbox — GSANE Framework Enhancement Project
- **User**: Mon Seigneur
- **Communication Language**: Français
- **Document Output Language**: Français
- **Output Folder**: `_gsane-output/`

## GSANE Runtime Structure

- **Agent definitions**:
  - `_gsane/core/agents/` — gsane-master (core orchestrator)
  - `_gsane/bmb/agents/` — BMB module (agent-builder, module-builder, workflow-builder)
  - `_gsane/cis/agents/` — CIS module (brainstorming, creative, design-thinking, innovation, presentation, storyteller)
  - `_gsane/tea/agents/` — TEA module (test architect)
- **Workflow definitions**:
  - `_gsane/core/workflows/` — brainstorming, party-mode, delegation, git-workflow, advanced-elicitation
  - `_gsane/bmb/workflows/` — agent/module/workflow creation and validation
  - `_gsane/cis/workflows/` — design-thinking, innovation-strategy, problem-solving, storytelling
  - `_gsane/tea/workflows/` — test architecture workflows
- **Core tasks**: `_gsane/core/tasks/` (help, editorial review, indexing, sharding, adversarial review)
- **Workflow engine**: `_gsane/core/tasks/workflow.xml` (executes YAML-based workflows)
- **Module configurations**: `_gsane/core/config.yaml`, `_gsane/bmb/config.yaml`, `_gsane/cis/config.yaml`, `_gsane/tea/config.yaml`
- **Core configuration**: `_gsane/core/config.yaml`
- **Agent manifest**: `_gsane/_config/agent-manifest.csv`
- **Workflow manifest**: `_gsane/_config/workflow-manifest.csv`
- **Help manifest**: `_gsane/_config/gsane-help.csv`
- **Agent memory**: `_gsane/_memory/`
- **Delegation Matrix**: `_gsane/_config/agent-delegation-matrix.csv`
- **Delegation Workflow**: `_gsane/core/workflows/delegation/workflow.md`
- **Git Workflow**: `_gsane/core/workflows/git-workflow/workflow.md` (standardized commit & PR process)

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
Load: _gsane/core/workflows/delegation/workflow.md
    ↓
Step 1: Analyze request type
    ↓
Step 2: Match against _gsane/_config/agent-delegation-matrix.csv
    ↓
Step 3: Load appropriate agent
    ↓
Step 4: Agent executes their workflow
    ↓
Step 5: Log routing decision
```

### Enforcement Rules

From `_gsane/core/config.yaml`:
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
1. Load: `_gsane/core/workflows/git-workflow/workflow.md`
2. Follow all workflow steps
3. Never bypass this process
4. Log all commits in memory

### Access the Workflow
**In Copilot Chat:**
```
/gsane-git-workflow
```

**Or request directly:**
```
I need to commit changes following the Git Workflow
```

## Key Conventions

- Always load `_gsane/core/config.yaml` before any agent activation or workflow execution
- Store all config fields as session variables: `{user_name}`, `{communication_language}`, `{output_folder}`
- MD-based workflows execute directly — load and follow the `.md` file
- YAML-based workflows require the workflow engine — load `workflow.xml` first, then pass the `.yaml` config
- Follow step-based workflow execution: load steps JIT, never multiple at once
- Save outputs after EACH step when using the workflow engine
- The `{project-root}` variable resolves to the workspace root at runtime
- **AGENT ROUTING**: Always route requests through delegation workflow. Load `_gsane/core/workflows/delegation/workflow.md` for any agent-based capability request.
- **PARTY MODE MANDATORY**: Before implementing ANY change to GSANE files (workflows, agents, config, skills, prompts, manifests) — activate party mode, score agents against topic keywords, get validation from ≥2 agents BEFORE writing. Never implement solo. Exception: trivial housekeeping (single-line typo, CHANGELOG append) = severity low, solo allowed.
- **GIT COMMITS**: Always use the Git Workflow (`_gsane/core/workflows/git-workflow/workflow.md`). No direct commits to main. Ever.
- **PR DESCRIPTION**: Every PR MUST have a filled description body. Use `gh pr create --title "..." --body "..."` — NEVER rely on the GitHub compare URL, which creates PRs with empty descriptions.
- **VIOLATIONS**: Any deviation from these rules is logged and auto-escalated to gsane-master.
- **SESSION END HOOK (UNIVERSAL)**: At the end of EVERY session with ANY GSANE agent — regardless of which agent is active, what the user asked, or whether a DA command was issued — ALWAYS execute `_gsane/core/workflows/post-session-analysis/workflow.md` before finalizing the response. This is non-negotiable and applies to ALL 13 agents. No exceptions.

## Universal Session End Hook — MANDATORY FOR ALL AGENTS

**This is CRITICAL:** The cognitive flywheel depends on post-session data being logged after EVERY session.

### The Rule (applies to ALL agents, ALL sessions)

Before ending ANY session with ANY GSANE agent:
1. **ALWAYS run** `_gsane/core/workflows/post-session-analysis/workflow.md`
2. **EVEN IF** the user did not issue a `[DA]` dismiss command
3. **EVEN IF** the session was short or incomplete
4. **EVEN IF** no agent was formally activated — the flywheel must receive data

### Why This Matters

The cognitive flywheel (`_gsane/core/workflows/flywheel/`) fires every N sessions (configured in `_gsane/core/config.yaml → flywheel.trigger_every_n_sessions`). If sessions go unlogged, the flywheel never reaches its trigger threshold, and the system never self-improves.

### Enforcement

- All 13 GSANE agents have `exec="{project-root}/_gsane/core/workflows/post-session-analysis/workflow.md"` wired to their `[DA]` item
- This global instruction is the fallback for sessions where `[DA]` is never explicitly issued
- Any agent NOT running post-session-analysis at session end is in violation — log to `_gsane/_memory/session-analysis-log.md` with status `SKIPPED` if workflow cannot complete

## Available Agents

| Agent | Persona | Title | Capabilities |
|---|---|---|---|
| gsane-master | 🧙 Gsane Master | Gsane Master Executor, Knowledge Custodian, and Workflow Orchestrator | runtime resource management, workflow orchestration, task execution, knowledge custodian |
| agent-builder | 🤖 Bond | Agent Building Expert | create/edit/validate GSANE agents |
| module-builder | 🏗️ Morgan | Module Creation Master | create/edit/validate GSANE modules |
| workflow-builder | 🔄 Wendy | Workflow Building Master | create/edit/validate GSANE workflows |
| brainstorming-coach | 🧠 Carson | Elite Brainstorming Specialist | brainstorming, ideation, creative techniques |
| creative-problem-solver | 🔬 Dr. Quinn | Master Problem Solver | TRIZ, systematic problem solving, root cause analysis |
| design-thinking-coach | 🎨 Maya | Design Thinking Maestro | human-centered design, empathy mapping, prototyping |
| innovation-strategist | ⚡ Victor | Disruptive Innovation Oracle | innovation strategy, business model disruption |
| presentation-master | 🎨 Caravaggio | Visual Communication Expert | presentations, pitch decks, visual storytelling |
| storyteller | 📖 Sophia | Master Storyteller | narrative, storytelling, brand stories |
| tea | 🧪 Murat | Master Test Architect | test architecture, ATDD, CI/CD, quality gates |
| gsane-optimizer | ⚙️ Léo | GSANE Framework Optimizer | token analysis, session metrics, framework improvement, GSANE evolution |
| qa-gsane | 🔍 Aria | GSANE Quality Assurance Specialist | workflow validation, agent consistency, persona regression detection, GSANE compliance |

## Slash Commands

Type `/gsane-` in Copilot Chat to see all available GSANE workflows and agent activators. Agents are also available in the agents dropdown.
<!-- GSANE:END -->
