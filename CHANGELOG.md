# CHANGELOG

Toutes les modifications notables du projet zav-sandbox BMAD sont documentées ici.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
adapté à l'architecture multi-agents et multi-modules du framework BMAD.

> **Format d'entrée:**
> ```
> **[Type]** Description fonctionnelle
> - Agent: {nom_agent} | Workflow: {workflow_utilisé} | Initié par: {initiateur}
> - Impact: {agents/workflows affectés}
> ```

---

## [Unreleased]

### [Core]
**[feat]** Cognitive Flywheel — cycle d'auto-amélioration complet
- Agent: BMad Master (party mode tous agents) | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `_bmad/core/workflows/flywheel/workflow-aggregate.md`, `workflow-apply.md`, `_bmad/_memory/flywheel-report.md`, `flywheel-history.md`, `session-analysis-log.md`, `config.yaml` (section flywheel), `hooks.json` (FlywheelTrigger), `workflow-manifest.csv`, `agent-delegation-matrix.csv`, `README.md`
- Mécanisme: post-session-analysis compte les sessions et auto-déclenche l'agrégateur toutes les N sessions (défaut: 5). Patterns ≥3 occurrences → confirmed. Corrections low/medium auto-appliquées sur branche fix/flywheel-* avec PR.

**[fix]** Activation universelle du flywheel — câblage exec sur 13 agents DA manquants + hook global
- Agent: BMad Master | Workflow: post-session-analysis (auto-correction) | Initié par: auto
- Impact: `agent-builder.md`, `module-builder.md`, `workflow-builder.md`, `qa-bmad.md`, `brainstorming-coach.md`, `creative-problem-solver.md`, `design-thinking-coach.md`, `innovation-strategist.md`, `presentation-master.md`, `storyteller.md`, `bmad-optimizer.md`, `tea.md`, `agent-compilation.md` (template), `architect.md` (ref), `.github/copilot-instructions.md`
- Résultat: 15/15 DA items câblés — flywheel s'active peu importe quel agent est utilisé

**[feat]** Principe de sévérité low/medium/high — source de vérité centrale dans config.yaml
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `core/config.yaml`, `bmad-master.md`, `qa-bmad.md`, `bmad-optimizer.md`

### [Infrastructure]
**[feat]** Score Elite 65/65 sur le scan de maturité agentique Copilot
- Agent: BMad Master (party mode) | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.github/agents/` (10 sub-agents), `.github/skills/` (2 nouveaux), `.github/hooks/` (2 nouveaux fichiers)
- Détail: Architecture +14pts (user-invokable + orchestrated-by), Automation +15pts (hooks), Knowledge +7pts (skills), Coverage +5pts, pénalité monoculture supprimée

**[feat]** Skills Copilot — bmad-framework + agent-design-patterns
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.github/skills/bmad-framework/SKILL.md`, `.github/skills/agent-design-patterns/SKILL.md`

**[feat]** Hooks de cycle de vie Copilot (SessionStart, SubagentStart/Stop, PreToolUse, PostToolUse, Stop)
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.github/hooks/hooks.json`, `.github/hooks/session-start.sh`

### [Core]
**[feat]** Agents bmad-optimizer (Léo ⚙️) et qa-bmad (Aria 🔍) créés et validés
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `_bmad/core/agents/bmad-optimizer.md`, `_bmad/bmb/agents/qa-bmad.md`, manifests mis à jour (13 agents)

**[feat]** Workflow post-session-analysis — analyse automatique silencieuse à chaque fin de session
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `_bmad/core/workflows/post-session-analysis/workflow.md`, hook DA et party-mode step-03 câblés

**[feat]** Refactoring Party Mode — architecture JIT (Just-In-Time) pour optimisation tokens
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `workflow.md` + 3 steps party-mode, `bmad-master.md` — section `<smart-party-mode>` ajoutée

**[fix]** Alignement Codex — AGENTS.md universel, copilot-instructions nettoyé, github-copilot.yaml configuré
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `AGENTS.md` (racine), `.github/copilot-instructions.md`, `_bmad/_config/ides/github-copilot.yaml`, `_bmad/core/config.yaml`

### [Infrastructure]
**[fix]** Correction des permissions du workflow de nettoyage de branches
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `cleanup-branches.yml` — remplacement de `dawidd6/action-delete-branch` par `actions/github-script` avec permissions `contents: write` explicites

**[feat]** Ajout du pipeline CI/CD avec validation automatique des PRs
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: Toutes les PRs vers `main` — validation CHANGELOG, structure BMAD, et état Git obligatoires avant merge

**[feat]** Nettoyage automatique des branches après merge
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: Toutes les branches `feature/*` et `fix/*` — suppression automatique post-merge

**[feat]** Branch protection rules activées sur `main`
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: Branche `main` — push direct bloqué, PR obligatoire, status checks requis

### [Core]
**[docs]** Section Testing & Validation ajoutée au README
- Agent: BMad Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: Documentation projet — références vers Git Workflow, CHANGELOG et Delegation System

---

## [1.0.0-alpha.1] - 2026-03-01

### Release initiale — Fondations BMAD

#### [Core]
**[feat]** Agent BMad Master 🧙 et système d'orchestration
- Exécuteur principal, gestionnaire de workflows et gardien de la connaissance

**[feat]** Système de configuration central (`config.yaml`)
- Variables de session, langue, dossier de sortie, gouvernance

**[feat]** Workflows fondamentaux
- `brainstorming`, `party-mode`, `advanced-elicitation`
- Moteur de workflow (`workflow.xml`) pour workflows YAML

**[feat]** Système de délégation d'agents
- Matrice de délégation (14 types de requêtes → agents)
- Workflow de routage obligatoire (`delegation/workflow.md`)
- Mode enforcement: `strict` — aucun bypass autorisé

**[feat]** Git Workflow v2.0
- Steps 1-6 standardisés avec Step 3.5 CHANGELOG obligatoire
- Convention de nommage: `feature/{desc}-YYYY-MM-DD` / `fix/{desc}-YYYY-MM-DD`

#### [BMB] — Builder Module
**[feat]** Agent Bond 🤖 (Agent Builder) — Création et validation d'agents BMAD

**[feat]** Agent Wendy 🔄 (Workflow Builder) — Design et validation de workflows

**[feat]** Agent Morgan 🏗️ (Module Builder) — Construction de modules BMAD complets

#### [CIS] — Creative Innovation Suite
**[feat]** Agent Carson 🧠 (Brainstorming Coach)

**[feat]** Agent Maya 🎨 (Design Thinking Coach)

**[feat]** Agent Dr. Quinn 🔬 (Creative Problem Solver)

**[feat]** Agent Victor ⚡ (Innovation Strategist)

**[feat]** Agent Caravaggio 🎨 (Presentation Master)

**[feat]** Agent Sophia 📖 (Storyteller)

#### [TEA] — Test Architecture
**[feat]** Agent Murat 🧪 (Master Test Architect)
- Architecture de tests, quality gates, CI/CD governance

#### [Config & Gouvernance]
**[feat]** Système de manifests (agents, workflows, tasks, tools)

**[feat]** Mémoire et gestion d'état (`_bmad/_memory/`)

**[feat]** Structure de sortie des artefacts (`_bmad-output/`)

---

## Format de version

Ce projet utilise un versioning sémantique adapté au contexte BMAD:

```
[MAJOR].[MINOR].[PATCH]-[PHASE]

Exemples:
- 1.0.0-alpha.1  (Développement initial)
- 1.0.0-beta.1   (Fonctionnalités complètes)
- 1.0.0          (Release stable)
- 1.1.0          (Nouvelles fonctionnalités)
- 1.1.1          (Corrections)
```

---

## Planning de release

- **Phase Alpha**: Établissement du système Core (actuel)
- **Phase Beta**: Validation de la coordination multi-agents
- **GA (1.0.0)**: Prêt pour production
- **Post-1.0**: Expansion de fonctionnalités et optimisation

---

## Guide de maintenance

### Ajouter une entrée (Step 3.5 du Git Workflow)

1. Ajouter sous `[Unreleased]` dans la section du bon module: `[Core]`, `[BMB]`, `[CIS]`, `[TEA]`, `[Infrastructure]`
2. Utiliser le format:
   ```
   **[type]** Description fonctionnelle (agents/workflows impactés)
   - Agent: {nom} | Workflow: {workflow} | Initié par: {initié_par}
   - Impact: {ce qui est affecté}
   ```
3. **Types**: `[feat]`, `[fix]`, `[breaking]`, `[security]`, `[refactor]`, `[docs]`, `[chore]`
4. **Modules**: `[Core]`, `[BMB]`, `[CIS]`, `[TEA]`, `[Infrastructure]`

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
