---
name: agent-customization
description: "How to personalize GSANE agents via .customize.yaml files — override persona, inject memories, add menu items — without touching governed .md files."
applyTo: "**"
---

# Agent Customization System

Every GSANE agent has a companion `.customize.yaml` file in `_gsane/_config/agents/`. This lets you personalize any agent for your project **without modifying the governed `.md` file**.

## File Naming Convention

```
_gsane/_config/agents/{module}-{agent-id}.customize.yaml
```

Examples:
- `bmb-morgan.customize.yaml` — for the Architect agent (Winston)
- `bmb-dev.customize.yaml` — for the Dev agent (Amelia)
- `core-master.customize.yaml` — for Gsane Master

## What You Can Customize

| Field | Effect | Merge Strategy |
|---|---|---|
| `agent.metadata.name` | Changes display name | Replace |
| `persona.role` | Changes the agent's role description | Replace |
| `persona.identity` | Changes identity/background | Replace |
| `persona.communication_style` | Changes how the agent communicates | Replace |
| `persona.principles` | Changes operating principles | Replace (full list) |
| `critical_actions` | Extra actions at startup | Appended after defaults |
| `memories` | Project facts the agent always knows | Prepended, available before sidecar loads |
| `menu` | Extra menu items | Appended after standard menu |

## What You CANNOT Override

The following are protected by governance and silently ignored if attempted:
- `<rules>` XML block — GSANE governance rules are inviolable
- `<activation>` step sequence
- `<menu-handlers>` block
- Delegation, git workflow, party mode, completion contract rules

## How It Works (activation step 2c)

At step 2c of every agent's activation:
1. Agent derives path: `{module}-{agent-id}.customize.yaml`
2. Reads the file silently — if absent or empty, skips and uses defaults
3. Stores non-empty fields as `{custom_*}` session variables
4. `memories` field → stored as `{injected_memories}`, available to the agent throughout the session

## Best Practices

**Good use of memories (static project knowledge):**
```yaml
memories:
  - "Ce projet est une API REST Node.js + PostgreSQL, déployée sur GCP Cloud Run."
  - "Standard architectural: jamais de logique métier dans les controllers — tout dans les services."
  - "Stack de tests : Vitest + Supertest + Playwright pour E2E."
```

**Good use of persona override (team naming convention):**
```yaml
agent:
  metadata:
    name: "Alex"  # Notre architecte interne s'appelle Alex
persona:
  communication_style: "Très direct, sans intro. Commence toujours par les risques avant les opportunités."
```

**What NOT to put in memories:**
- Dynamic information that changes per session (use sidecar memory for that)
- Sensitive data (API keys, tokens, passwords)

## Sidecar Memory vs Customize Memories

| Type | Where | Purpose | Who writes it |
|---|---|---|---|
| `customize.yaml memories` | `_gsane/_config/agents/` | Static project facts — always true | You (human) |
| Sidecar `learned-lessons.md` | `_gsane/_memory/{agent}-sidecar/` | Lessons from past sessions — evolves | Agent (via SESSION HOOK) |
| Sidecar `project-state.md` | `_gsane/_memory/{agent}-sidecar/` | Last session context | Agent (via CONTEXT_SENTINEL) |

Both types are loaded at activation. Sidecar data takes precedence over customize memories when there is a conflict (most recent = most relevant).

## Quick Start — Add Project Context to All Key Agents

Edit these three files to give all agents instant project knowledge:

```yaml
# bmb-morgan.customize.yaml
memories:
  - "Stack du projet : {technologies}"
  - "Pattern architectural imposé : {pattern}"

# bmb-dev.customize.yaml  
memories:
  - "Stack du projet : {technologies}"
  - "Convention de code : {conventions}"
  - "Tests : tous les tests sont dans /tests, runner = {test-runner}"

# bmb-pm.customize.yaml
memories:
  - "Projet : {nom} — {description courte}"
  - "Priorité actuelle : {sprint ou phase}"
```
