<!-- GSANE:START -->
# GSANE Method — Project Instructions

## ⛔ PRE-EXECUTION GATE — MANDATORY BEFORE ANY ACTION

**This gate fires BEFORE every task, every command, every file edit, no exceptions.**

Before producing any output or taking any action, the AI MUST check these 3 questions in order:

1. **Does this request involve any GSANE capability, agent, validation, test, CI check, file modification, or implementation?**
   - If YES → proceed to step 2
   - If NO (pure explanation/conversation with no action) → proceed normally

2. **Is this request covered by the Delegation Matrix?**
   - Load `_gsane/_config/delegation-matrix.yaml`
    - Match request keywords against the active declarative routing rules (`rules[*].trigger`) and, when relevant, the `security_gate` block
   - If match found → load target agent, route through delegation workflow
   - If no match → escalate to master, DO NOT self-execute

3. **Am I about to execute solo what an agent should execute?**
   - If yes → STOP, load delegation workflow, route correctly
   - Solo execution = violation — auto-escalate to master

**Keyword coverage table (non-exhaustive — always check the full matrix):**

| Trigger words | Target agent |
|---|---|
| implement, modifier, fix, apply changes, corriger, ajouter, supprimer | 🧙 Gsane Master (party mode) |
| **git commit, git add, git push, créer une branche, stager, pousser** sur fichiers GSANE | 🧙 Gsane Master (party mode) — Step 0 git-workflow obligatoire |

> ⚠️ **If this gate is not applied, the response is in violation of GSANE governance rules.**

---

## Project Configuration

- **Project**: zav-sandbox — GSANE Framework Enhancement Project
- **User**: Mon Seigneur
- **Communication Language**: Français
- **Document Output Language**: Français
- **Output Folder**: `_gsane-output/`

## GSANE Runtime Structure

- **Strike Team definitions**: `_gsane/agents/*.md`
- **Workflow definitions**: `_gsane/workflows/` (delegation, cc-verify, git-workflow, etc.)
- **Core tasks**: `_gsane/tasks/`
- **Core configuration**: `_gsane/config.yaml`
- **Manifests**: `_gsane/_config/*.yaml`
- **Agent memory**: `_gsane/_memory/`
- **Git Workflow**: `_gsane/workflows/git-workflow/workflow.md` (standardized commit & PR process)

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
Load: _gsane/workflows/delegation/workflow.md
    ↓
Step 1: Analyze request type
    ↓
Step 2: Match against _gsane/_config/delegation-matrix.yaml
    ↓
Step 3: Load appropriate agent
    ↓
Step 4: Agent executes their workflow
    ↓
Step 5: Log routing decision
```

### Enforcement Rules

From `_gsane/config.yaml`:
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
1. Load: `_gsane/workflows/git-workflow/workflow.md`
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
- **APPEND-ONLY PREFERENCE**: When writing large documents, do not overwrite the full file or mid-frontmatter. Ask the tool to Append-Only to the end of the file unless restructuring is mandatory.

- Always load `_gsane/config.yaml` before any agent activation or workflow execution
- MD-based workflows execute directly — load and follow the `.md` file
- YAML files in the active runtime are manifests/config data — read them directly; do not route them through a legacy workflow engine
- Follow step-based workflow execution: load steps JIT, never multiple at once
- Save outputs after EACH workflow step when the workflow explicitly requires persisted outputs
- **AGENT ROUTING**: Always route requests through delegation workflow. Load `_gsane/workflows/delegation/workflow.md` for any agent-based capability request.
- **SECURITY GATE LITE**: If a request matches the declarative `security_gate` topics in `_gsane/_config/delegation-matrix.yaml`, escalate to Master and preserve `owner=Winston (Architect)` plus `validation=Quinn (QA)`. Add Bond only when the request touches GSANE, policy, guardrails, or runtime-critical surfaces.
- **SOLO TRIP WIRE**: At the exact moment a file-write operation (edit, create, replace) is about to be called on any GSANE artifact — STOP. Declare: (1) target file, (2) trivial or not per the closed list, (3) which agents validated if non-trivial. No validation on record → abort, activate party mode first. Read-only operations do not trigger this rule.
- **GIT COMMITS**: Always use the Git Workflow (`_gsane/workflows/git-workflow/workflow.md`). No direct commits to main. Ever.
- **PR DESCRIPTION**: Every PR MUST have a filled description body. Open the GitHub compare URL, fill the title and paste the body template — NEVER submit with an empty description.
- **HUMAN-IN-THE-LOOP**: NEVER merge a PR, push --force, delete a remote branch, or perform any irreversible shared-system action without explicit user approval in the current exchange. Present the action and wait for green light. The user is part of the team — no agent bypasses human review. Violation = `GOVERNANCE-VIOLATION` logged to failure-museum.md.
- **VIOLATIONS**: Any deviation from these rules is logged and auto-escalated to master.
- **SESSION END HOOK (UNIVERSAL)**: At the end of EVERY session with ANY GSANE agent — regardless of which agent is active, what the user asked, or whether a DA command was issued — ALWAYS execute `_gsane/workflows/post-session-analysis/workflow.md` before finalizing the response. This is non-negotiable and applies to ALL tous les agents. No exceptions.
- **VISIBLE CLOSURE IDEMPOTENCE**: The user-facing final response must appear only once per task. If a complete final response has already been sent, post-session-analysis, hooks, and `task_complete` preparation must remain silent and MUST NOT emit a second brief summary, status line, or mini-closeout.

## Universal Session End Hook — MANDATORY FOR ALL AGENTS

**This is CRITICAL:** The cognitive flywheel depends on post-session data being logged after EVERY session.

### The Rule (applies to ALL agents, ALL sessions)

Before ending ANY session with ANY GSANE agent:
1. **ALWAYS run** `_gsane/workflows/post-session-analysis/workflow.md`
2. **EVEN IF** the user did not issue a `[DA]` dismiss command
3. **EVEN IF** the session was short or incomplete
4. **EVEN IF** no agent was formally activated — the flywheel must receive data
5. **NEVER** let this hook create a second user-visible closeout if the final answer has already been emitted

### Why This Matters

The cognitive flywheel (`_gsane/workflows/flywheel/`) fires every N sessions (configured in `_gsane/config.yaml → flywheel.trigger_every_n_sessions`). If sessions go unlogged, the flywheel never reaches its trigger threshold, and the system never self-improves.

### Enforcement

- All tous les agents GSANE have `exec="{project-root}/_gsane/workflows/post-session-analysis/workflow.md"` wired to their `[DA]` item
- This global instruction is the fallback for sessions where `[DA]` is never explicitly issued
- Any agent NOT running post-session-analysis at session end is in violation — log to `_gsane/_memory/sessions/session-analysis-log.md` with status `SKIPPED` if workflow cannot complete

> ⚠️ **NOTE**: Le projet a exactement **5 agents actifs** (Strike Team). Tous les agents suivent ce session end hook.

## Available Agents

| Agent | Persona | Specialty |
|---|---|---|
| Master | 🧙 Langis | Orchestration, task execution, Delivery Contracts |
| Dev | 💻 Amelia | TDD Code implementation |
| QA | 🧪 Quinn | Test execution, quality gate validation |
| Architect | 🏗️ Winston | System design, toolsmithing |
| Builder | 🤖 Bond | Create/edit/validate GSANE agents |

## Slash Commands

Type `/gsane-` in Copilot Chat to see all available GSANE workflows and agent activators. Agents are also available in the agents dropdown.
<!-- GSANE:END -->

---

## Available Skills (JIT — chargement ciblé)

Les skills se chargent automatiquement si un fichier correspondant à leur `applyTo:` est ouvert.
Sinon, les sélectionner manuellement dans le skill picker Copilot ou via `#file:`.
Ne jamais demander de "charger toutes les skills" — elles sont JIT par design.

| Skill | applyTo (auto) | Usage |
|-------|----------------|-------|
| `gsane-framework` | `_gsane/**` | Modifier le framework |
| `agent-design-patterns` | `_gsane/agents/**` | Créer un agent |
| `agent-customization` | `_gsane/agents/**` | Modifier un agent |
| `cognitive-flywheel` | `_gsane/_memory/**` | Sessions flywheel |
| `debugging-gsane` | `gsane.sh` | Debug et diagnostic |
| `git-workflow` | `.github/**` | Git et PR |
| `mcp-integration` | `_gsane/mcp-server/**` | Outils MCP |
| `delivery-contract` | _(manuel)_ | Créer un DC |
| `prompt-engineering` | _(manuel)_ | Améliorer un prompt |
| `mcp-development` | _(manuel)_ | Développer MCP |
| `qa-linter` | _(manuel)_ | Linter agents |
| `session-management` | _(manuel)_ | Sessions |
| `task-decomposition` | _(manuel)_ | Décomposer tâches |
| `zero-touch-fix-loop` | _(manuel)_ | Fix-loop Quinn |

