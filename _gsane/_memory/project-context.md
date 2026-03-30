# Contexte Projet — zav-sandbox

> Ce fichier est chargé par tous les agents GSANE au démarrage.
> Il est la source de vérité pour le contexte projet partagé entre toutes les sessions.
> **Remplis les sections marquées ✏️ — c'est le seul fichier que tous les agents lisent.**
> Mis à jour manually ou via `/gsane-session-bootstrap` lors de la première session.

---

## Projet

- **Nom** : zav-sandbox — GSANE Framework Enhancement Project
- **Objectif** : ✏️ _Amélioration continue du framework GSANE multi-agents — optimisation token, orchestration, workflows, DX_
- **Phase actuelle** : ✏️ _Phase 4 — Benchmark BMAD+Grimoire, auto-routing, session artifacts_
- **Branche active** : ✏️ _feature/bmm-module-import-2026-03-02_

---

## Stack & Technologies

| Couche | Technologie | Notes |
|--------|-------------|-------|
| Framework | GSANE v6.0.5 | Multi-agent, Copilot-native |
| Modules | core, bmb, cis, tea, bmm | 22 agents |
| Runtime | GitHub Copilot (VS Code) | Pas de subagents disponibles |
| Config | YAML + CSV | agent-manifest, workflow-manifest |
| Outputs | `_gsane-output/` | Jamais commités sur main |

---

## Architecture

```
_gsane/
  core/     → orchestration, gsane-master, workflows fondamentaux
  bmb/      → agent-builder (Bond), module-builder (Morgan), workflow-builder (Wendy), qa-gsane (Aria)
  bmm/      → pipeline business : analyst→pm→architect→sm→ux→dev→qa→tech-writer
  cis/      → créativité : brainstorming, design-thinking, innovation, storytelling
  tea/      → tests : Murat (ATDD, CI/CD)
_gsane-output/ → artefacts générés (session-plans, distillates, rapports)
.github/
  prompts/  → slash commands Copilot (/gsane-*)
  agents/   → mode fichiers Copilot (gsane-master, etc.)
  skills/   → compétences domaine (gsane-framework, agent-design-patterns, etc.)
```

---

## Conventions

- **Langue** : Français (communication) + Français (documents)
- **Commits** : Conventional Commits (`feat/fix/chore(scope): description`)
- **Branches** : `feature/{description}-YYYY-MM-DD` ou `fix/{description}-YYYY-MM-DD`
- **Jamais** commit direct sur `main`
- **Party Mode** obligatoire avant tout changement aux artefacts GSANE non-trivial
- **CC obligatoire** avant "c'est fait"

---

## Décisions architecturales clés

<!-- Ajouter ici les décisions majeures pour informer tous les agents -->
- **YAML double-format** : certains workflows ont YAML + MD par design (engine requis) — ne pas supprimer
- **advanced-elicitation** : utilisé dans 20+ workflows BMB/BMM — ne pas modifier
- **Party Mode** : roleplay JIT (pas de subagents Copilot) — l'agent simule les voix

---

## Agents & Points de contact

| Besoin | Agent | Module |
|--------|-------|--------|
| Implémenter/corriger | Amelia (dev) | bmm |
| Architecture système | Winston (architect) | bmm |
| PRD / spécifications | John (pm) | bmm |
| Tests & CI | Murat (tea) | tea |
| Créer un agent GSANE | Bond (agent-builder) | bmb |
| Créer un workflow | Wendy (workflow-builder) | bmb |
| Valider conformité | Aria (qa-gsane) | bmb |
| Optimiser tokens | Léo (gsane-optimizer) | core |
| Brainstorming | Carson (brainstorming-coach) | cis |

---

## Points de vigilance

<!-- Mis à jour au fil des sessions -->
- Toujours bumper `manifest.yaml` lors de changements de schéma CSV
- `session-plan-{date}.md` dans `_gsane-output/` — lire avant de lancer une phase
- `project-context.md` (ce fichier) — mettre à jour si la phase ou branche change

---

## État de session récent

→ Voir `_gsane/_memory/session-state.md` pour l'état de la dernière session.
