---
type: decision
number: "0006"
status: proposed
date: 2026-05-30
tags: [audit, correctifs, devx, hygiène, phase-9]
---

# ADR-0006 — Plan de correctifs — Audit technique 2026-05-30

## Contexte

Audit technique complet du framework (5 piliers : Code & Architecture, Flux
utilisateur, UX & Fonctionnalités, Fiabilité & DevOps, Périmètre) réalisé le
2026-05-30. **18 problèmes identifiés**, répartis par sévérité :

- 🔴 Critique (4) — bloquent l'adoption ou causent une perte silencieuse
- 🟠 Élevé (7) — friction significative ou risque de régression
- 🟡 Moyen (5) — polish et clarté
- 🟢 Mineur (2) — hygiène

Ce plan organise les correctifs en **8 lots thématiques** exécutables en une
ou plusieurs sessions, par priorité décroissante.

---

## Lot A — Sécurité & Infrastructure (Critique)

> **Objectif** : protéger les données sensibles et valider la cohérence Markdown en CI.

| # | Action | Fichier(s) créés/modifiés |
|---|---|---|
| A1 | Créer `.gitignore` racine (`.DS_Store`, `Thumbs.db`, `*.log`, `.venv/`) | `.gitignore` |
| A2 | Créer `docs/_scratch/.gitignore` (ignorer `inputs/`) | `docs/_scratch/.gitignore` |
| A3 | Ajouter note "ne jamais committer d'inputs réels" dans `docs/_scratch/memory/README.md` | `docs/_scratch/memory/README.md` |
| A4 | Créer `.github/workflows/ci.yml` (markdownlint + markdown-link-check + vérif CHANGELOG) | `.github/workflows/ci.yml` |

**Commit** : `chore: add gitignore and markdown CI pipeline`

---

## Lot B — Cohérence documentaire (Élevé)

> **Objectif** : corriger les incohérences de placement et de format qui cassent la traçabilité.

| # | Action | Fichier(s) |
|---|---|---|
| B1 | Retirer toutes les entrées manuelles de `CHANGELOG.md` (garder uniquement les blocs `release-please`) | `CHANGELOG.md` |
| B2 | Déplacer `docs/0002-audit-existant.md` → `docs/decisions/0002-audit-existant.md` | `docs/0002-audit-existant.md` |
| B3 | Supprimer la section Archives de `IDEAS.md` (16 entrées + en-tête + intro) — convention actée : idée close = supprimer de `IDEAS.md`, pas archiver. Mettre à jour le Sommaire en conséquence. | `IDEAS.md` |
| B4 | Vérifier la licence de `docs/_reference/BMAD_FRAMEWORK_GUIDE_COMPLET.md` — retirer du repo (et de l'historique git si nécessaire) si non compatible avec une publication publique future | `docs/_reference/BMAD_FRAMEWORK_GUIDE_COMPLET.md` |

**Commit** : `chore: fix doc placement, ideas archives removal + convention, BMAD check`

---

## Lot C — Réduction de duplication (Élevé)

> **Objectif** : éliminer les divergences silencieuses entre fichiers miroir.

| # | Action | Fichier(s) |
|---|---|---|
| C1 | Réduire `agents/personas/orchestrator.md` à identité + ton + lien — supprimer les sections "Règles absolues" et "Anti-patterns" (dupliquées dans `orchestrator.agent.md`) | `agents/personas/orchestrator.md` |
| C2 | Ajouter champ `version: "1.0.0"` dans le frontmatter de `agents/skills/root-cause-analysis/SKILL.md` | `agents/skills/root-cause-analysis/SKILL.md` |
| C3 | Documenter la politique de versioning des skills dans `docs/architecture/2026-05-30-phase-8-skills.md` | `docs/architecture/2026-05-30-phase-8-skills.md` |

**Commit** : `refactor: deduplicate orchestrator persona, add skill versioning`

---

## Lot D — Onboarding & UX (Élevé)

> **Objectif** : rendre le framework testable en < 5 min et ses commandes découvrables.

| # | Action | Fichier(s) |
|---|---|---|
| D1 | Ajouter section "Test rapide — 2 minutes" dans `README.md` (prompt minimal + résultat attendu) | `README.md` |
| D2 | Ajouter table "Commandes disponibles" dans `README.md` (`/quick`, `/light`, `/debate`, `/debate max=N`, `/checkpoint`, `/pre-pr`) | `README.md` |
| D3 | Ajouter badge version `release-please` dans `README.md` | `README.md` |
| D4 | Documenter le protocole de recalibration LLM drift (template prompt `/reset`) dans `README.md` ou `orchestrator.agent.md` | `README.md` |

| D5 | Ajouter une ligne dans `README.md` pointant vers `agents/hooks/README.md` (hooks opt-in — "Pour aller plus loin") | `README.md` |
| D6 | Ajouter règle dans `agents/protocols/preflight.md` : au premier message de session, scanner `docs/_scratch/memory/` et signaler les checkpoints ouverts disponibles (règle textuelle, pas de code) | `agents/protocols/preflight.md` |

**Commit** : `docs: improve onboarding — quick test, commands reference, badge, recalibration, hooks discovery, session restore`

---

## Lot E — Politique de rétention (Élevé)

> **Objectif** : éviter l'accumulation des checkpoints sans politique définie.

| # | Action | Fichier(s) |
|---|---|---|
| E1 | Décider et documenter la politique de rétention dans `docs/_scratch/memory/README.md` : statut `closed` → Scribe propose archivage dans `docs/_scratch/memory/archive/` | `docs/_scratch/memory/README.md` |
| E2 | Ajouter la valeur `closed` aux options de statut dans le frontmatter de `agents/templates/memory-checkpoint.md` | `agents/templates/memory-checkpoint.md` |

**Commit** : `feat: checkpoint retention policy — closed status + archive zone`

---

## Lot F — Scripts & Hooks (Moyen)

> **Objectif** : robustesse des scripts d'installation et clarté des prérequis OS.

| # | Action | Fichier(s) |
|---|---|---|
| F1 | Ajouter `set -e` + vérification `git rev-parse --is-inside-work-tree` dans `scripts/install-hooks.sh` | `scripts/install-hooks.sh` |
| F2 | Ajouter note de version VS Code (Preview API) + reminder de revalidation dans `agents/hooks/README.md` | `agents/hooks/README.md` |
| F3 | Ajouter commentaire explication encodage UTF-8 (accents/apostrophes intentionnellement omis) dans `agents/hooks/memory-nudge.ps1` et `agents/hooks/memory-nudge.sh` | `agents/hooks/memory-nudge.ps1`, `agents/hooks/memory-nudge.sh` |
| F4 | Ajouter note compatibilité OS (`Get-Command pwsh` + fallback `powershell`) dans `agents/hooks/README.md` | `agents/hooks/README.md` |

| F5 | Ajouter procédure de test manuel dans `agents/hooks/README.md` : comment valider que `security-guard` et `memory-nudge` s'activent correctement | `agents/hooks/README.md` |

**Commit** : `fix: install-hooks robustness, hooks docs OS compat + test procedure`

---

## Lot G — Skills & Templates (Moyen)

> **Objectif** : réduire la barrière à la création de nouvelles skills et améliorer les métadonnées templates.

| # | Action | Fichier(s) |
|---|---|---|
| G1 | Créer `agents/skills/TEMPLATE.md` (guide pratique : frontmatter, structure, exemple copiable) | `agents/skills/TEMPLATE.md` |
| G2 | Ajouter champ `used_by_workflow` dans le frontmatter de `agents/templates/prd.md` et `agents/templates/architecture.md` | `agents/templates/prd.md`, `agents/templates/architecture.md` |
| G3 | Vérifier que `agents/workflows/code-analysis.md` est à parité avec `incident-response.md` (diagramme Mermaid + table personas + anti-patterns) — compléter si absent | `agents/workflows/code-analysis.md` |

| G4 | Créer `agents/skills/README.md` — tableau des skills disponibles (nom, statut, description 1 ligne, exemple d'invocation) | `agents/skills/README.md` |
| G5 | Ajouter règle tiebreaker dans `agents/protocols/light-panel.md` : "En cas de contradiction directe entre deux personas, le Scribe la signale explicitement et propose `/debate` pour résolution" | `agents/protocols/light-panel.md` |

**Commit** : `feat: skill template, skills registry, template metadata, code-analysis parity, panel tiebreaker`

---

## Lot H — Personas (Faible)

> **Objectif** : documenter les frontières de périmètre pour éviter les chevauchements.

| # | Action | Fichier(s) |
|---|---|---|
| H1 | Ajouter section "Différence avec / périmètre" dans `developer.md` | `agents/personas/developer.md` |
| H2 | Ajouter section "Différence avec / périmètre" dans `devops.md` | `agents/personas/devops.md` |
| H3 | Ajouter section "Différence avec / périmètre" dans `security.md` | `agents/personas/security.md` |
| H4 | Ajouter section "Différence avec / périmètre" dans `architect.md` | `agents/personas/architect.md` |
| H5 | Ajouter section "Différence avec / périmètre" dans `scribe.md` | `agents/personas/scribe.md` |

**Commit** : `docs: add persona boundary sections for 5 personas`

---

## Tableau de priorisation global

| Lot | Urgence | Effort estimé | Dépendances |
|---|---|---|---|
| A — Sécurité & Infra | 🔴 Critique | ~45 min | Aucune |
| B — Cohérence doc | 🟠 Élevé | ~40 min | Aucune (B4 peut être bloquant — traiter en premier) |
| C — Déduplication | 🟠 Élevé | ~20 min | Aucune |
| D — Onboarding UX | 🟠 Élevé | ~60 min | Aucune |
| E — Rétention | 🟠 Élevé | ~15 min | Aucune |
| F — Scripts & Hooks | 🟡 Moyen | ~40 min | Aucune |
| G — Skills & Templates | 🟡 Moyen | ~55 min | C2 (versioning) |
| H — Personas | 🟢 Faible | ~40 min | Aucune |

**Lots A-E = session prioritaire (~3h)**. Lots F-H = session de polish (~2h30).

---

## Notes d'exécution

- Exécuter un lot complet avant de passer au suivant (commits atomiques).
- Lots A-E peuvent être exécutés dans la même session sans risque de conflit.
- Lot G.G3 peut nécessiter une lecture de `incident-response.md` pour comparaison — prévoir ~10 min.
- Lot C.C1 (`orchestrator.md` → stub) : conserver les sections "Identité" et "Ton" ; supprimer tout ce qui duplique `orchestrator.agent.md`.
- Pour le badge version (D3) : URL format `https://img.shields.io/github/v/release/[OWNER]/[REPO]`.
