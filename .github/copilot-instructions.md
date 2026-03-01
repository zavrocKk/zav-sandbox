<!-- BMAD:START -->
# BMAD Method — Project Instructions

## Project Configuration

- **Project**: {{project_name}}
- **User**: Mon Seigneur
- **Communication Language**: Français
- **Document Output Language**: Français
- **User Skill Level**: {{user_skill_level}}
- **Output Folder**: {project-root}/_bmad-output
- **Planning Artifacts**: {{planning_artifacts}}
- **Implementation Artifacts**: {{implementation_artifacts}}
- **Project Knowledge**: {{project_knowledge}}

## BMAD Runtime Structure

- **Agent definitions**: `_bmad/bmm/agents/` (BMM module) and `_bmad/core/agents/` (core)
- **Workflow definitions**: `_bmad/bmm/workflows/` (organized by phase)
- **Core tasks**: `_bmad/core/tasks/` (help, editorial review, indexing, sharding, adversarial review)
- **Core workflows**: `_bmad/core/workflows/` (brainstorming, party-mode, advanced-elicitation)
- **Workflow engine**: `_bmad/core/tasks/workflow.xml` (executes YAML-based workflows)
- **Module configuration**: `_bmad/bmm/config.yaml`
- **Core configuration**: `_bmad/core/config.yaml`
- **Agent manifest**: `_bmad/_config/agent-manifest.csv`
- **Workflow manifest**: `_bmad/_config/workflow-manifest.csv`
- **Help manifest**: `_bmad/_config/bmad-help.csv`
- **Agent memory**: `_bmad/_memory/`
- **CHANGELOG**: `CHANGELOG.md` (project root, tracks all changes)
- **Git Workflow**: `_bmad/core/workflows/git-workflow/workflow.md` (standardized commits)

## CHANGELOG System — PROJECT TRACKING

**This is CRITICAL:** All changes MUST be documented in CHANGELOG.md. It's the single source of truth for project evolution.

### The CHANGELOG Rule

Every commit via Git Workflow includes **Step 3.5: Update CHANGELOG.md**

1. **Open**: `CHANGELOG.md` at project root
2. **Find**: `[Unreleased]` section
3. **Add entry**: `` - `[{type}]({module}): {description}` - {agent} ``
4. **Types**: `[feature]`, `[fix]`, `[breaking]`, `[security]`, `[docs]`
5. **Modules**: `core`, `bmb`, `cis`, `tea`, `config`, `docs`

### Format

```markdown
## [Unreleased]

### Core
- `[feature](core): implement agent delegation` - Bond, Wendy, Morgan
- `[fix](core): resolve config parsing` - bmad-master

### CMB
- `[feature](bmb): enhance agent builder` - Bond
```

### Enforcement

From `_bmad/core/config.yaml`:
- ✅ `changelog.enabled: true` — System active
- ✅ `changelog.required_for_commits: true` — Mandatory  
- ✅ `changelog.enforcement_mode: strict` — No bypasses
- ✅ `changelog.validation: true` — Format validated

### Git Workflow Integration

The Git Workflow **cannot proceed past Step 3.5** without:
- ✅ CHANGELOG.md updated
- ✅ Entry added to [Unreleased]
- ✅ Correct format used
- ✅ File staged for commit

## Git Workflow — MANDATORY FOR ALL COMMITS

- Always load `_bmad/bmm/config.yaml` before any agent activation or workflow execution
- Store all config fields as session variables: `{user_name}`, `{communication_language}`, `{output_folder}`, `{planning_artifacts}`, `{implementation_artifacts}`, `{project_knowledge}`
- MD-based workflows execute directly — load and follow the `.md` file
- YAML-based workflows require the workflow engine — load `workflow.xml` first, then pass the `.yaml` config
- Follow step-based workflow execution: load steps JIT, never multiple at once
- Save outputs after EACH step when using the workflow engine
- The `{project-root}` variable resolves to the workspace root at runtime

## Available Agents

| Agent | Persona | Title | Capabilities |
|---|---|---|---|
| bmad-master | BMad Master | BMad Master Executor, Knowledge Custodian, and Workflow Orchestrator | runtime resource management, workflow orchestration, task execution, knowledge custodian |

## Slash Commands

Type `/bmad-` in Copilot Chat to see all available BMAD workflows and agent activators. Agents are also available in the agents dropdown.
<!-- BMAD:END -->
