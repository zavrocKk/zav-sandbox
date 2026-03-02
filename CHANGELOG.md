# CHANGELOG

Toutes les modifications notables du projet zav-sandbox GSANE sont documentées ici.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
adapté à l'architecture multi-agents et multi-modules du framework GSANE.

> **Format d'entrée:**
> ```
> **[Type]** Description fonctionnelle
> - Agent: {nom_agent} | Workflow: {workflow_utilisé} | Initié par: {initiateur}
> - Impact: {agents/workflows affectés}
> ```

---

## [Unreleased]

### [Core]
**[docs]** Règle de réutilisation de branche ajoutée — une branche = une unité logique ; seule exception : corriger une erreur ou ajouter un oubli sur une PR non encore mergée
- Agent: Gsane Master (party: Aria, Wendy) | Workflow: party-mode | Initié par: Mon Seigneur
- Impact: `_gsane/core/workflows/git-workflow/workflow.md` — callout ⚠️ ajouté dans Step 2
- Impact: `CONTRIBUTING.md` — nouvelle règle §3 avec exemples ✅/❌, ancien §3 renommé §4
- Branche: `fix/branch-reuse-rule-2026-03-01`

**[fix]** Step 0 governance ajouté dans `git-workflow/workflow.md` — blocage PRE-EXECUTION GATE avant tout `git add/commit/push` sur fichiers GSANE (sévérité MEDIUM/HIGH → Party Mode obligatoire)
- Agent: Gsane Master (party: Aria, Léo, Wendy) | Workflow: party-mode | Initié par: Mon Seigneur
- Impact: `_gsane/core/workflows/git-workflow/workflow.md` — Step 0 checklist de gouvernance
- Impact: `_gsane/_config/agent-delegation-matrix.csv` — keywords `git commit;git add;git push;créer une branche` ajoutés à `implement-changes`
- Impact: `.github/copilot-instructions.md` — ligne git operations ajoutée dans la keyword table
- Résultat: Toute action git sur fichiers GSANE DOIT passer par Party Mode — violation = log dans violations.log
- Branche: `fix/delegation-gate-git-workflow-2026-03-01`

**[fix]** Tracking Git complet du répertoire `_gsane/` — ajout de 507 fichiers non trackés (`_gsane/`, `.github/agents/gsane-*`, `.github/prompts/gsane-*`), suppression de 41 fichiers `bmad-*` obsolètes
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: CI check T5 `_gsane/core/agents` présent, T4 `13 .agent.md files` valides
- Branche: `fix/track-gsane-directory-2026-03-01`

**[docs]** README — refonte section Installation & Setup en 5 étapes détaillées
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `README.md` — prérequis, hook pre-commit, session-start.sh, activation VS Code, vérification complète PowerShell

**[docs]** Création de `CONTRIBUTING.md` — guide de contribution complet pour le projet
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: Nouveau fichier racine — couvre branches, CHANGELOG, PR body, sévérité, CI checks

**[fix]** Suppression complète des références GitHub CLI (`gh`) — workflow PR via URL compare GitHub
- Agent: Gsane Master (party: Aria, Léo) | Workflow: party-mode | Initié par: Mon Seigneur
- Impact: `git-workflow/workflow.md`, `flywheel/workflow-apply.md`, `README.md`, `copilot-instructions.md`, `validate-pr.yml`, `gsane-framework/SKILL.md`, `hooks/hooks.json`
- Résultat: Aucune dépendance `gh` CLI — les PRs se créent via l'URL compare GitHub + body template collé manuellement

**[fix]** PRE-EXECUTION GATE ajouté en tête de `copilot-instructions.md` — bloque toute exécution solo avant check obligatoire de la matrice de délégation
- Agent: Gsane Master (party: Aria, Léo) | Workflow: party-mode | Initié par: Mon Seigneur
- Impact: `.github/copilot-instructions.md` — gate en 3 étapes avec table de keywords visibles avant toute autre règle
- Résultat: L'IA ne peut plus ignorer le routing sans violer une règle explicite et prioritaire

**[fix]** Matrice de délégation — 2 entrées manquantes ajoutées : `run-tests` et `project-audit` → TEA (Murat)
- Agent: Aria (qa-gsane) | Workflow: party-mode | Initié par: Mon Seigneur
- Impact: `_gsane/_config/agent-delegation-matrix.csv` — requêtes `tester/valider le projet/check ci/smoke test/regression check/audit projet` routent désormais vers Murat
- Résultat: Angle mort de délégation fermé — couverture complète des requêtes de type test/validation

**[feat]** Cognitive Flywheel — scoreboard par agent, workflow et prompt
- Agent: Gsane Master (party: Aria, Léo, Wendy, Murat, Bond, Dr. Quinn) | Workflow: post-session-analysis | Initié par: Mon Seigneur
- Impact: `_gsane/_memory/scoreboard.md` créé — scores A+/A/B/C par agent, exécutions par workflow, santé des prompts
- Impact: `workflow-aggregate.md` Step 5b — calcul automatique du scoreboard à chaque cycle flywheel

**[feat]** Cognitive Flywheel — tracking des améliorations de prompts (`prompt_improvement_signals`)
- Agent: Gsane Master | Workflow: post-session-analysis | Initié par: Mon Seigneur
- Impact: `post-session-analysis/workflow.md` Step 2 — Léo détecte prompt-quality-up, prompt-efficiency-up, flywheel-prompt-confirmed
- Résultat: Le flywheel peut maintenant corréler les gains observés par l'utilisateur avec les corrections appliquées

**[feat]** Cognitive Flywheel — marker `FLYWHEEL TRIGGERED` dans le log de sessions
- Agent: Gsane Master | Workflow: post-session-analysis | Initié par: auto
- Impact: `post-session-analysis/workflow.md` Step 6 — marker écrit avant déclenchement + status mis à jour après
- Impact: `workflow-aggregate.md` Step 5b — marker status mis à jour après completion
- Résultat: Auditabilité complète — on sait exactement quand et pourquoi le flywheel a tiré

**[feat]** Cognitive Flywheel — `session_count` dans chaque entrée de log
- Agent: Gsane Master | Workflow: post-session-analysis | Initié par: auto
- Impact: `post-session-analysis/workflow.md` Step 5 template — `| Count: {session_count}` dans le header
- Impact: `session-analysis-log.md` — 6 entrées existantes rétroactivement mises à jour
- Résultat: Comptage O(1) sans scanner tout le fichier

**[feat]** Cognitive Flywheel — checklist de test end-to-end (6 tests)
- Agent: Gsane Master (Murat) | Workflow: party-mode | Initié par: Mon Seigneur
- Impact: `_gsane/core/workflows/flywheel/flywheel-test-checklist.md` — T1 compteur, T2 report, T3 corrections, T4 prompt signals, T5 scoreboard, T6 régression

**[fix]** workflow-apply — PR créée avec body complet (règle PR description)
- Agent: Gsane Master | Workflow: git-workflow | Initié par: auto
- Impact: `workflow-apply.md` Step 5 — `gh pr create --body` avec template complet incluant Prompt Improvements Confirmed

**[docs]** Diagrammes Mermaid ajoutés dans 5 fichiers clés (0 → 5 Mermaid)
- Agent: Gsane Master | Workflow: party-mode | Initié par: Mon Seigneur
- Impact: README.md, cognitive-flywheel/SKILL.md, delegation/workflow.md, git-workflow/workflow.md, post-session-analysis/workflow.md

### [Core]
**[fix]** Audit A1 — correction de 46 slash commands `/gsane-*` non fonctionnels (chemin déprécié)
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: 46 fichiers `.github/prompts/*.prompt.md` — `_gsane/bmm/config.yaml` (inexistant) → `_gsane/core/config.yaml`
- Résultat: Tous les slash commands Copilot Chat fonctionnels

**[feat]** Audit A1 — agents Léo (gsane-optimizer) et Aria (qa-gsane) activables dans Copilot
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.github/agents/gsane-agent-core-gsane-optimizer.agent.md`, `.github/agents/gsane-agent-bmb-qa-gsane.agent.md`
- Impact: `.github/prompts/gsane-gsane-optimizer.prompt.md`, `.github/prompts/gsane-qa-gsane.prompt.md`

**[feat]** Audit A1 — slash command `/gsane-git-workflow` créé (référencé mais manquant)
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.github/prompts/gsane-git-workflow.prompt.md`

**[feat]** Audit A1 — Skill cognitive-flywheel ajoutée
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.github/skills/cognitive-flywheel/SKILL.md`

**[fix]** Audit A1 — `ides/github-copilot.yaml` : Léo, Aria et Murat ajoutés à la liste agents
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `_gsane/_config/ides/github-copilot.yaml`

**[fix]** Audit A1 — `gsane-help.csv` : entrées manquantes pour Léo et Aria ajoutées
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `_gsane/_config/gsane-help.csv`

**[feat]** Audit A1 — `.gitignore` créé (instructions.md + _gsane-output/ + OS artifacts)
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.gitignore`

**[feat]** Cognitive Flywheel — cycle d'auto-amélioration complet
- Agent: Gsane Master (party mode tous agents) | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `_gsane/core/workflows/flywheel/workflow-aggregate.md`, `workflow-apply.md`, `_gsane/_memory/flywheel-report.md`, `flywheel-history.md`, `session-analysis-log.md`, `config.yaml` (section flywheel), `hooks.json` (FlywheelTrigger), `workflow-manifest.csv`, `agent-delegation-matrix.csv`, `README.md`
- Mécanisme: post-session-analysis compte les sessions et auto-déclenche l'agrégateur toutes les N sessions (défaut: 5). Patterns ≥3 occurrences → confirmed. Corrections low/medium auto-appliquées sur branche fix/flywheel-* avec PR.

**[fix]** Activation universelle du flywheel — câblage exec sur 13 agents DA manquants + hook global
- Agent: Gsane Master | Workflow: post-session-analysis (auto-correction) | Initié par: auto
- Impact: `agent-builder.md`, `module-builder.md`, `workflow-builder.md`, `qa-gsane.md`, `brainstorming-coach.md`, `creative-problem-solver.md`, `design-thinking-coach.md`, `innovation-strategist.md`, `presentation-master.md`, `storyteller.md`, `gsane-optimizer.md`, `tea.md`, `agent-compilation.md` (template), `architect.md` (ref), `.github/copilot-instructions.md`
- Résultat: 15/15 DA items câblés — flywheel s'active peu importe quel agent est utilisé

**[feat]** Principe de sévérité low/medium/high — source de vérité centrale dans config.yaml
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `core/config.yaml`, `gsane-master.md`, `qa-gsane.md`, `gsane-optimizer.md`

### [Infrastructure]
**[feat]** Score Elite 65/65 sur le scan de maturité agentique Copilot
- Agent: Gsane Master (party mode) | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.github/agents/` (10 sub-agents), `.github/skills/` (2 nouveaux), `.github/hooks/` (2 nouveaux fichiers)
- Détail: Architecture +14pts (user-invokable + orchestrated-by), Automation +15pts (hooks), Knowledge +7pts (skills), Coverage +5pts, pénalité monoculture supprimée

**[feat]** Skills Copilot — gsane-framework + agent-design-patterns
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.github/skills/gsane-framework/SKILL.md`, `.github/skills/agent-design-patterns/SKILL.md`

**[feat]** Hooks de cycle de vie Copilot (SessionStart, SubagentStart/Stop, PreToolUse, PostToolUse, Stop)
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `.github/hooks/hooks.json`, `.github/hooks/session-start.sh`

### [Core]
**[feat]** Agents gsane-optimizer (Léo ⚙️) et qa-gsane (Aria 🔍) créés et validés
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `_gsane/core/agents/gsane-optimizer.md`, `_gsane/bmb/agents/qa-gsane.md`, manifests mis à jour (13 agents)

**[feat]** Workflow post-session-analysis — analyse automatique silencieuse à chaque fin de session
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `_gsane/core/workflows/post-session-analysis/workflow.md`, hook DA et party-mode step-03 câblés

**[feat]** Refactoring Party Mode — architecture JIT (Just-In-Time) pour optimisation tokens
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `workflow.md` + 3 steps party-mode, `gsane-master.md` — section `<smart-party-mode>` ajoutée

**[fix]** Alignement Codex — AGENTS.md universel, copilot-instructions nettoyé, github-copilot.yaml configuré
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `AGENTS.md` (racine), `.github/copilot-instructions.md`, `_gsane/_config/ides/github-copilot.yaml`, `_gsane/core/config.yaml`

### [Infrastructure]
**[fix]** Correction des permissions du workflow de nettoyage de branches
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: `cleanup-branches.yml` — remplacement de `dawidd6/action-delete-branch` par `actions/github-script` avec permissions `contents: write` explicites

**[feat]** Ajout du pipeline CI/CD avec validation automatique des PRs
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: Toutes les PRs vers `main` — validation CHANGELOG, structure GSANE, et état Git obligatoires avant merge

**[feat]** Nettoyage automatique des branches après merge
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: Toutes les branches `feature/*` et `fix/*` — suppression automatique post-merge

**[feat]** Branch protection rules activées sur `main`
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: Branche `main` — push direct bloqué, PR obligatoire, status checks requis

### [Core]
**[docs]** Section Testing & Validation ajoutée au README
- Agent: Gsane Master | Workflow: git-workflow | Initié par: Mon Seigneur
- Impact: Documentation projet — références vers Git Workflow, CHANGELOG et Delegation System

---

## [1.0.0-alpha.1] - 2026-03-01

### Release initiale — Fondations GSANE

#### [Core]
**[feat]** Agent Gsane Master 🧙 et système d'orchestration
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
**[feat]** Agent Bond 🤖 (Agent Builder) — Création et validation d'agents GSANE

**[feat]** Agent Wendy 🔄 (Workflow Builder) — Design et validation de workflows

**[feat]** Agent Morgan 🏗️ (Module Builder) — Construction de modules GSANE complets

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

**[feat]** Mémoire et gestion d'état (`_gsane/_memory/`)

**[feat]** Structure de sortie des artefacts (`_gsane-output/`)

---

## Format de version

Ce projet utilise un versioning sémantique adapté au contexte GSANE:

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
- `[security](config): improve credential handling` - gsane-master
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

### Core Module (`_gsane/core/`)
- **Owner**: gsane-master
- **Focus**: System foundation, orchestration, core workflows
- **Changelog Section**: Core

### BMB Module (`_gsane/bmb/`)
- **Agents**: Bond, Wendy, Morgan
- **Focus**: Building and extending GSANE system
- **Changelog Section**: BMB

### CIS Module (`_gsane/cis/`)
- **Agents**: Carson, Maya, Dr. Quinn, Victor, Caravaggio, Sophia
- **Focus**: Creative problem-solving and innovation
- **Changelog Section**: CIS

### TEA Module (`_gsane/tea/`)
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
- Escalation → Violation logged and reported to gsane-master

---

**Last Updated**: 2026-03-01  
**Format Version**: 1.0 (Adapted from Keep a Changelog)  
**Maintainers**: All GSANE agents via Git Workflow
