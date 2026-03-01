# CHANGELOG Integration Guide

**For**: All BMAD Agents and Users  
**Purpose**: How to properly update and maintain CHANGELOG.md  
**Enforced by**: Git Workflow Step 3.5

---

## QuickStart

### Before you commit via Git Workflow:

**Step 1: Update CHANGELOG.md**
```markdown
Open: CHANGELOG.md at project root

Find: [Unreleased] section

Add entry under module name:
- `[feature](core): my change description` - My Name or Agent Name
```

**Step 2: Save & Stage**
```bash
git add CHANGELOG.md
```

**Step 3: Continue Git Workflow**
- Proceed to Step 4 (Push) and beyond

---

## Module Categories

Use one of these:

| Module | Changes To | Category |
|--------|-----------|----------|
| **Core** | `_bmad/core/` | `### Core` |
| **BMB** | `_bmad/bmb/` | `### BMB` |
| **CIS** | `_bmad/cis/` | `### CIS` |
| **TEA** | `_bmad/tea/` | `### TEA` |
| **Config** | Config files, core config | `### Config` |
| **Docs** | README, guides, documentation | `### Docs` |

---

## Change Types

Use one of these in brackets:

| Type | When | Example |
|------|------|---------|
| `[feature]` | New functionality, additions, deployments | `[feature]` |
| `[fix]` | Bug fixes, corrections, improvements | `[fix]` |
| `[breaking]` | Breaking changes, renamed things | `[breaking]` |
| `[security]` | Security fixes, vulnerability patches | `[security]` |
| `[docs]` | Documentation updates (if major) | `[docs]` |
| `[refactor]` | Code restructuring | `[refactor]` |

---

## Entry Format

```
- `[{TYPE}]({MODULE}): {DESCRIPTION}` - {AGENT_OR_USER}
```

### Examples

#### Agents

```markdown
- `[feature](core): implement agent delegation system` - Bond, Wendy, Morgan
- `[fix](bmb): correct workflow validation` - Wendy
- `[feature](cis): add brainstorming enhancements` - Carson
```

#### Users

```markdown
- `[feature](core): add new configuration option` - Mon Seigneur
- `[docs](core): update user guide` - Mon Seigneur
```

#### GitHub Copilot

```markdown
- `[feature](docs): update README` - GitHub Copilot (orchestrated by bmad-master)
```

---

## Step-by-Step in Git Workflow

### When You're at Step 3.5:

**1. Open CHANGELOG.md**
```bash
# Or open in your editor:
code CHANGELOG.md
```

**2. Find [Unreleased]**
```markdown
## [Unreleased]

### Core
### BMB
### CIS
### TEA
### Docs
```

**3. Go to your module section**

Example: If you're changing core system, go to:
```markdown
## [Unreleased]

### Core
← ADD YOUR ENTRY HERE
```

**4. Add entry**

Add to the END of your module's list (newest entries at bottom):
```markdown
### Core
- `[feature](core): implement agent delegation system` - Bond, Wendy, Morgan
- `[fix](core): resolve configuration parsing` - bmad-master
← YOUR NEW ENTRY GOES HERE
- `[feature](core): add new documentation` - existing entry
```

**5. Copy from your git commit message**

Whatever you wrote in Step 3's commit message:
```bash
git commit -m "feature(core): implement agent delegation system"
                    ↑              ↑
                  TYPE          DESCRIPTION
```

Becomes in CHANGELOG:
```markdown
- `[feature](core): implement agent delegation system` - Your Name
```

**6. Save the file**
```
File → Save (Ctrl+S)
```

**7. Stage it**
```bash
git add CHANGELOG.md
```

**8. Continue workflow**
- Continue to Step 4

---

## Common Scenarios

### Scenario 1: Single Agent Change
```markdown
- `[feature](bmb): enhance agent builder` - Bond
```

### Scenario 2: Multi-Agent Collaboration
```markdown
- `[feature](core): implement delegation system` - Bond, Wendy, Morgan
```

### Scenario 3: Bug Fix
```markdown
- `[fix](cis): resolve brainstorming timeout issue` - Carson
```

### Scenario 4: Documentation Update
```markdown
- `[docs](core): update README with examples` - GitHub Copilot
```

### Scenario 5: Breaking Change
```markdown
- `[breaking](config): rename configuration schema` - Morgan
```

---

## Validation Rules

✅ **Must have:**
- Entry in [Unreleased] section
- Type in brackets: `[type]`
- Module in parentheses: `(module)`
- Clear description (lowercase, imperative mood)
- Attribution: who made this change

❌ **Must NOT have:**
- Entries in released version sections (those are readonly)
- Multiple entries for same change
- Unclear or vague descriptions
- No attribution
- Invalid module or type

---

## If You Miss This Step

### In Git Workflow:
- Step 3.5 validation will flag it
- Workflow will not proceed to Step 4
- You must update CHANGELOG.md to continue
- Violation will be logged

### Message:
```
⚠️ CHANGELOG.md not updated
Please add entry to CHANGELOG.md and retry
Format: - `[{type}]({module}): {description}` - {agent}
```

---

## Release Process

When it's time to release (handled by Morgan/bmad-master):

**1. Identify version number**
- Look at changes: major? minor? patch?

**2. Create release branch**
```bash
git checkout -b release/v1.1.0
```

**3. Update CHANGELOG.md**
```markdown
Change:
## [Unreleased]

To:
## [1.1.0] - 2026-03-15

## [Unreleased]
```

**4. Commit**
```bash
git commit -m "release(config): prepare v1.1.0 release"
```

**5. Tag**
```bash
git tag v1.1.0
```

**6. Merge back to main**

---

## Tools & Tips

### View CHANGELOG
```bash
cat CHANGELOG.md
```

### View just Unreleased
```bash
cat CHANGELOG.md | head -30
```

### Count entries
```bash
cat CHANGELOG.md | grep "^- \`" | wc -l
```

### Search for your entry
```bash
cat CHANGELOG.md | grep "your-text"
```

---

## Questions?

If unsure:
- Follow the examples in this guide
- Use format: `- `[type](module): description` - agent`
- When in doubt, ask in Party Mode discussion
- bmad-master can review and correct

---

**Version**: 1.0  
**Last Updated**: 2026-03-01  
**Enforced**: YES (mandatory in Git Workflow)  
**Questions**: Ask in `/bmad-chat`
