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
- **GIT COMMITS**: Always use the Git Workflow (`_bmad/core/workflows/git-workflow/workflow.md`). No direct commits to main. Ever.
- **VIOLATIONS**: Any deviation from these rules is logged and auto-escalated to bmad-master.

## Available Agents

| Agent | Persona | Title | Capabilities |
|---|---|---|---|
| bmad-master | BMad Master | BMad Master Executor, Knowledge Custodian, and Workflow Orchestrator | runtime resource management, workflow orchestration, task execution, knowledge custodian |

## Slash Commands

Type `/bmad-` in Copilot Chat to see all available BMAD workflows and agent activators. Agents are also available in the agents dropdown.
<!-- BMAD:END -->
