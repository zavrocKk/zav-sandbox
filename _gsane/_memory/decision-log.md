# 📋 Decision Log — GSANE

> Journal des décisions architecturales et de gouvernance. Chaque décision importante est horodatée, justifiée, et chaînable.
> Utiliser `[THINK]` avant toute décision HIGH pour délibérer formellement avant d'écrire ici.
> Format inspiré des ADR (Architecture Decision Records).

---

## Comment utiliser ce fichier

- **Créer une entrée** pour toute décision qui affecte l'architecture, les conventions, les outils, ou la gouvernance du projet
- **Ne jamais supprimer** une entrée — utiliser le statut `SUPERSEDED` si une décision est remplacée
- **Chaîner les décisions** — si DL-003 remplace DL-001, noter `supersedes: DL-001` dans DL-003
- **Consulter ce log** avant toute modification de config, workflow, ou structure — une décision similaire a peut-être déjà été prise

---

## Décisions enregistrées

---

### DL-001 — Suppression de GitHub CLI comme dépendance

| Champ | Valeur |
|---|---|
| **ID** | DL-001 |
| **Date** | 2026-03-01 |
| **Statut** | ✅ ACTIVE |
| **Décision** | GitHub CLI (`gh`) est **banni** du projet. Les PRs sont créées via l'URL compare GitHub + body template collé manuellement. |
| **Justification** | Mon Seigneur ne souhaite pas de dépendance CLI externe non explicitement installée. L'URL compare GitHub est suffisante et universelle. |
| **Alternatives rejetées** | `gh pr create` — dépendance externe, nécessite authentification |
| **Impact** | `git-workflow/workflow.md`, `flywheel/workflow-apply.md`, `README.md`, `copilot-instructions.md` |
| **Agents impliqués** | Gsane Master (party: Aria, Léo) |
| **Supersedes** | — |

---

### DL-002 — Enforcement strict de la délégation (no solo execution)

| Champ | Valeur |
|---|---|
| **ID** | DL-002 |
| **Date** | 2026-03-01 |
| **Statut** | ✅ ACTIVE |
| **Décision** | Toute exécution d'action GSANE (modification de fichier, git action, workflow) passe par le PRE-EXECUTION GATE. Sévérité MEDIUM/HIGH → Party Mode obligatoire avant toute écriture. |
| **Justification** | Violations répétées de solo execution détectées en session. Le gate implicite était ignoré par l'IA. |
| **Mécanismes** | PRE-EXECUTION GATE dans `copilot-instructions.md`, Step 0 dans `git-workflow/workflow.md`, matrice de délégation complétée |
| **Agents impliqués** | Gsane Master (party: Aria, Léo, Wendy) |
| **Supersedes** | — |

---

### DL-003 — 1 branche Git = 1 unité logique de changement

| Champ | Valeur |
|---|---|
| **ID** | DL-003 |
| **Date** | 2026-03-01 |
| **Statut** | ✅ ACTIVE |
| **Décision** | Chaque modification, feature, fix, ou suppression doit avoir sa propre branche depuis `main`. Exception unique : corriger une erreur ou un oubli sur une PR non encore mergée. |
| **Justification** | La branche `feature/project-a1-audit-fixes-2026-03-01` contenait des commits de natures différentes, rendant le suivi difficile. |
| **Impact** | `git-workflow/workflow.md` Step 2, `CONTRIBUTING.md` §3 |
| **Agents impliqués** | Gsane Master (party: Aria, Wendy) |
| **Supersedes** | — |

---

### DL-004 — GSANE = protocole de gouvernance IA, pas un outil CLI

| Champ | Valeur |
|---|---|
| **ID** | DL-004 |
| **Date** | 2026-03-01 |
| **Statut** | ✅ ACTIVE |
| **Décision** | GSANE ne développe pas d'outils CLI en Python/Shell. Son périmètre est la qualité des interactions IA — agents, workflows, délégation, mémoire. Les outils exécutables appartiennent aux projets applicatifs, pas au framework de gouvernance. |
| **Justification** | Analyse comparative vs BMAD Custom Kit (88.8% Python). Porter des outils CLI dans GSANE changerait sa nature fondamentale. |
| **Alternatives rejetées** | CLI d'initialisation, outils Python de mesure performance |
| **Exception** | Les scripts Shell hooks (pre-commit, session-start/stop) sont acceptés car ils font partie du cycle de vie Git |
| **Agents impliqués** | Gsane Master (party: Aria, Léo, Aria, Victor, Dr. Quinn, Wendy, Murat) |
| **Supersedes** | — |

---

## Ajouter une entrée

Copier ce template et incrémenter l'ID :

```markdown
### DL-XXX — {Titre court}

| Champ | Valeur |
|---|---|
| **ID** | DL-XXX |
| **Date** | YYYY-MM-DD |
| **Statut** | ✅ ACTIVE / ❌ SUPERSEDED / 🔄 PENDING |
| **Décision** | Description précise de la décision prise |
| **Justification** | Pourquoi cette décision a été prise |
| **Alternatives rejetées** | Ce qui a été envisagé et écarté |
| **Impact** | Fichiers ou conventions affectés |
| **Agents impliqués** | Agent(s) ayant validé la décision |
| **Supersedes** | DL-XXX (si cette décision en remplace une autre) |
```
