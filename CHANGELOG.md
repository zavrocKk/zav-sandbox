# CHANGELOG

All notable changes to the zav-sandbox BMAD project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
adapted for the BMAD framework's multi-agent, multi-module architecture.

---

## [Unreleased]

### Core
- `[feature](core): implement CHANGELOG system for project tracking` - Bond, Wendy, Morgan
  - Created CHANGELOG.md with Keep a Changelog format adapted for BMAD
  - Integrated CHANGELOG updates into Git Workflow Step 3.5
  - Added enforcement rules and validation
  - Established per-module change tracking

- `[feature](core): integrate CHANGELOG into Git Workflow (Step 3.5)` - Wendy
  - Updated Git Workflow v2 with mandatory CHANGELOG update step
  - CHANGELOG.md must be updated before any commit
  - Validation ensures proper formatting
  - Step 3.5 blocks workflow if CHANGELOG not updated

### Docs
- `[feature](docs): create CHANGELOG Integration Guide` - Bond, Wendy, Morgan
  - Guide for agents and users on maintaining CHANGELOG.md
  - Format examples and step-by-step instructions
  - Release process documentation
  - Validation rules and common scenarios

- `[docs](core): add CHANGELOG configuration to core config.yaml` - GitHub Copilot
  - Added changelog system configuration
  - Enabled strict enforcement mode
  - Configured module section ordering

- `[docs](docs): update copilot-instructions with CHANGELOG system` - GitHub Copilot
  - Documented CHANGELOG tracking system
  - Added enforcement rules and format specifications
  - Integrated with Git Workflow documentation

---

## [1.0.0-alpha.1] - 2026-03-01

### Initial Release - BMAD Foundation

#### Core
- BMad Master agent and orchestration system
- Core configuration system
- Task execution framework (editorial review, indexing, adversarial review)
- Core workflows (brainstorming, party-mode, advanced-elicitation)
- Workflow engine support

#### BMB (Builder Module)
- Agent Builder (Bond) - Create and validate BMAD agents
- Workflow Builder (Wendy) - Design and validate BMAD workflows
- Module Builder (Morgan) - Build complete BMAD modules
- Full build pipeline with validation

#### CIS (Creative Innovation Suite)
- Brainstorming Coach (Carson)
- Design Thinking Coach (Maya)
- Creative Problem Solver (Dr. Quinn)
- Innovation Strategist (Victor)
- Presentation Master (Caravaggio)
- Storyteller (Sophia)
- Team collaboration workflows

#### TEA (Test Architecture)
- Master Test Architect (Murat)
- Test architecture patterns and best practices
- Quality gate framework

#### Configuration & Governance
- Manifest system for agents, workflows, and tasks
- Memory and state management
- Project output structure

---

## Version Format

This project uses a modified semantic versioning with BMAD context:

```
[MAJOR].[MINOR].[PATCH]-[PHASE]

Examples:
- 1.0.0-alpha.1  (Early development)
- 1.0.0-beta.1   (Feature complete)
- 1.0.0          (Stable release)
- 1.1.0          (New features)
- 1.1.1          (Bugfixes)
```

---

## Release Planning

- **Alpha Phase**: Core system establishment (current)
- **Beta Phase**: Multi-agent coordination validation
- **GA (1.0.0)**: Production ready
- **Post-1.0**: Feature expansion and optimization

---

## Guidelines for Maintaining This File

### Adding Entries

When committing changes via the Git Workflow:

1. **Update CHANGELOG.md** in Step 3.5 of the Git Workflow
2. **Add entry to [Unreleased]** section under appropriate module
3. **Format**: `` - `[{type}]({module}): {description}` - {agent_name} ``
4. **Types**: `[feature]`, `[fix]`, `[breaking]`, `[security]`, `[docs]`, `[refactor]`
5. **Modules**: `core`, `bmb`, `cis`, `tea`, `config`, `docs`

### Examples

```markdown
- `[feature](core): add new workflow type` - Wendy
- `[fix](bmb): resolve agent validation bug` - Bond
- `[breaking](core): change agent manifest format` - Morgan
- `[security](config): improve credential handling` - bmad-master
- `[docs](core): update delegation system guide` - GitHub Copilot
```

### Release Process

1. Identify version number based on changes
2. Create release branch: `release/v{version}`
3. Move `[Unreleased]` entries to `[{version}]` section with date
4. Add release summary if needed
5. Commit as: `release({version}): prepare release`
6. Create git tag: `v{version}`
7. Merge to main and develop

---

## Module Overview

### Core Module (`_bmad/core/`)
- **Owner**: bmad-master
- **Focus**: System foundation, orchestration, core workflows
- **Changelog Section**: Core

### BMB Module (`_bmad/bmb/`)
- **Agents**: Bond, Wendy, Morgan
- **Focus**: Building and extending BMAD system
- **Changelog Section**: BMB

### CIS Module (`_bmad/cis/`)
- **Agents**: Carson, Maya, Dr. Quinn, Victor, Caravaggio, Sophia
- **Focus**: Creative problem-solving and innovation
- **Changelog Section**: CIS

### TEA Module (`_bmad/tea/`)
- **Owner**: Murat
- **Focus**: Testing and quality architecture
- **Changelog Section**: TEA

---

## Governance

### CHANGELOG Requirements

- ✅ **Mandatory**: Every commit must update CHANGELOG.md
- ✅ **Validation**: Git Workflow Step 3.5 requires CHANGELOG update
- ✅ **Audit**: All entries include agent/user attribution
- ✅ **Traceable**: Links to git commits and PRs
- ✅ **Integrated**: Part of core configuration system

### Violation Handling

- Missing CHANGELOG update → Git Workflow flags as incomplete
- Invalid format → Git Workflow validation fails
- Escalation → Violation logged and reported to bmad-master

---

**Last Updated**: 2026-03-01  
**Format Version**: 1.0 (Adapted from Keep a Changelog)  
**Maintainers**: All BMAD agents via Git Workflow
