---
name: cc-verify
description: "Completion Contract — checklist obligatoire avant toute déclaration de tâche terminée. Empêche tout agent de déclarer 'c'est fait' sans vérification objective. Doit être exécuté avant le DA ou la fin de chaque workflow substantiel."
---

# Completion Contract (CC) — Vérification avant "Terminé"

**Goal:** Aucun agent ne peut déclarer une tâche terminée sans avoir passé cette checklist. Remplace la parole par une vérification objective.

**Inspiration:** BMAD Custom Kit `cc-verify.sh` — porté en workflow Markdown pour GSANE.

**Déclenchement :**
- **Obligatoire** : avant tout `[DA] Dismiss Agent` sur une session de travail substantielle
- **Obligatoire** : à la fin de tout workflow qui produit un artefact ou modifie des fichiers
- **Optionnel** : à la demande de Mon Seigneur via `/gsane-cc-verify`

---

## CHECKLIST DE COMPLETION

Exécuter chaque section et noter PASS / FAIL / N/A.

---

### Section A — Git & Branche

| # | Vérification | Statut |
|---|---|---|
| A1 | Je suis sur une branche feature/* ou fix/* (pas main) | |
| A2 | Tous les fichiers modifiés ont été `git add`-és | |
| A3 | `git status --short` ne montre pas de fichiers oubliés (pas de `??` non intentionnels) | |
| A4 | Un commit existe sur cette branche (pas de travail non committé) | |
| A5 | La branche a été pushée sur origin | |
| A6 | Cette branche couvre une seule unité logique de changement (règle DL-003) | |

---

### Section B — CHANGELOG

| # | Vérification | Statut |
|---|---|---|
| B1 | Une entrée `[Unreleased]` a été ajoutée au CHANGELOG.md pour ce changement | |
| B2 | L'entrée contient : Agent, Workflow, Initié par, Impact | |
| B3 | Le type est valide : `[feat]` `[fix]` `[docs]` `[chore]` `[breaking]` `[security]` `[refactor]` | |

---

### Section C — Qualité du changement

| # | Vérification | Statut |
|---|---|---|
| C1 | Party Mode a été appliqué si sévérité MEDIUM ou HIGH | |
| C2 | ≥ 2 agents ont validé le changement (si MEDIUM/HIGH) | |
| C3 | Le Failure Museum a été consulté — ce pattern n'a pas déjà échoué ici | |
| C4 | Le Decision Log a été consulté — cette décision n'est pas en conflit avec une existante | |
| C5 | Les fichiers modifiés correspondent à l'intention déclarée (pas de modificaton collatérale non intentionnelle) | |

---

### Section D — Manifests & Structure

| # | Vérification | Statut |
|---|---|---|
| D1 | Si un nouvel agent a été créé : `agent-manifest.csv` a été mis à jour | |
| D2 | Si un nouveau workflow a été créé : `workflow-manifest.csv` a été mis à jour | |
| D3 | Si un nouveau fichier a été créé dans `_gsane/` : il est inclus dans `files-manifest.csv` ou le manifest pertinent | |
| D4 | Aucun chemin déprécié `_bmad/` ou `_gsane/bmm/` n'a été introduit | |

---

### Section E — CI (simulation locale)

| # | Vérification | Statut |
|---|---|---|
| E1 | `CHANGELOG.md` contient la section `[Unreleased]` | |
| E2 | Aucun fichier `_gsane/bmm/` n'existe dans le repo | |
| E3 | Les 13 fichiers `.agent.md` GSANE sont présents dans `.github/agents/` | |
| E4 | La structure `_gsane/core`, `_gsane/core/agents`, `_gsane/core/workflows` existe | |
| E5 | Les hooks sont présents : `pre-commit.sh`, `session-start.sh`, `session-stop.sh`, `flywheel-trigger.sh` | |

---

## RÉSULTAT

Calculer le score :

```
PASS total  : X / 20
FAIL        : liste des items échoués
N/A         : liste des items non applicables
```

### Seuil de completion

| Score | Décision |
|---|---|
| 20/20 (ou tous N/A justifiés) | ✅ **CC PASS** — la tâche est terminée |
| 1+ FAIL dans Section A ou B | ❌ **CC FAIL** — corriger avant de continuer |
| 1+ FAIL dans Section C | ⚠️ **CC WARNING** — notifier Mon Seigneur, attendre validation |
| 1+ FAIL dans Section D ou E | ❌ **CC FAIL** — corriger avant de continuer |

---

## OUTPUT

Afficher à Mon Seigneur :

```
✅ CC PASS — [X]/[total] vérifications réussies — tâche déclarée terminée
```
ou
```
❌ CC FAIL — [N] items échoués : [liste] — corriger avant de déclarer terminé
```

---

## NOTES

- Ce workflow ne nécessite **pas** de fichiers à charger — tout se fait depuis le contexte de session
- En cas de CC FAIL : ne pas déclarer la tâche terminée, ne pas fermer le workflow parent
- Les items N/A doivent être justifiés (ex: "A1 N/A — pas de changement de fichier cette session")
