---
name: agent-design-patterns
description: >
  Patterns de conception d'agents GSANE,
  frontmatter, menus, structure agent.
  Charger pour créer ou modifier un agent.
applyTo: "_gsane/agents/**"
trigger: "créer agent, concevoir agent, patterns agent"
---

# Agent Design Patterns

Standards for creating and maintaining agents in the gsane framework.

## Agent File Structure

Every agent `.md` file follows this structure:

```
---
name: agent-id
description: 'Persona — Title: capabilities'
---
<agent> block with:
  - <activation> steps
  - <persona> with name, icon, identity, communication_style
  - <menu> with numbered items and exec paths
  - <rules> with behavioral constraints
  - <prompts> with named prompt blocks
</agent>
```

## Frontmatter Standards

- `name` — kebab-case identifier matching the filename
- `description` — format: `'PersonaName — Title: capability1, capability2'`
- Config reference: always `_gsane/config.yaml` or the active manifest/config file for the surface being designed

## Menu Item Pattern

```xml
<item cmd="XY or fuzzy match on keyword">[XY] Label</item>
<item cmd="XY or fuzzy match on keyword" exec="{project-root}/path/to/workflow.md">[XY] Label</item>
```

- `cmd` — 2-letter shortcut + fuzzy match alternatives
- `exec` — path to workflow to load and follow (optional)
- Items without `exec` are handled inline by the agent

## Workflow Types

| Type | Execution |
|---|---|
| `.md` workflow | Load and follow directly |
| `.yaml` manifest/config | Read directly as data; do not route through a legacy workflow engine |

## Party Mode Agent Protocol

In party mode, Langis (Master) is the sole orchestrator:
1. Init: load only the active manifest or delegation summary needed to score the 5 core agents
2. Per turn: score agents against keywords, select 2-3 max
3. Load only the selected agent files if deeper instructions are actually needed
4. Generate response, discard profile data
5. Never load every agent file in one pass during party mode

## Sub-Agent Declaration (GitHub Copilot)

For GitHub Copilot agent files (`.agent.md`), sub-agents must declare:
```yaml
user-invokable: false
orchestrated-by: master
```

The main orchestrator (`master`) must NOT have `user-invokable: false`.

## Validation Checklist

- [ ] Persona name and icon defined
- [ ] Communication style specified
- [ ] All menu items have valid `cmd` shortcuts
- [ ] `exec` paths point to files that exist in the active workspace
- [ ] Rules include language constraint
- [ ] Agent passes repo validation (`pytest` + `bash gsane.sh validate` when applicable)
