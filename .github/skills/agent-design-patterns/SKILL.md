---
name: agent-design-patterns
description: Patterns and standards for designing GSANE-compatible agents — frontmatter, menus, prompts, persona, workflow types, and party mode behavior.
applyTo: "**"
---

# Agent Design Patterns

Standards for creating and maintaining agents in the GSANE framework.

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
- Config reference: always `{project-root}/_gsane/core/config.yaml` or module config

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
| `.yaml` workflow | Requires workflow engine — load `_gsane/core/tasks/workflow.xml` first |

## Party Mode Agent Protocol

In party mode, Gsane Master is the sole orchestrator:
1. Init: load CSV index (name, icon, capabilities) only
2. Per turn: score agents against keywords, select 2-3 max
3. Load CSV row for selected agents only
4. Generate response, discard profile data
5. Never load full `.md` files during party mode

## Sub-Agent Declaration (GitHub Copilot)

For GitHub Copilot agent files (`.agent.md`), sub-agents must declare:
```yaml
user-invokable: false
orchestrated-by: gsane-master
```

The main orchestrator (`gsane-master`) must NOT have `user-invokable: false`.

## Validation Checklist

- [ ] Persona name and icon defined
- [ ] Communication style specified
- [ ] All menu items have valid `cmd` shortcuts
- [ ] `exec` paths use `{project-root}` variable
- [ ] Rules include language constraint
- [ ] Agent passes Aria (qa-gsane) validation
