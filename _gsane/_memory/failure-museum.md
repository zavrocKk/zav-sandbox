# Failure Museum — GSANE

> Catalogue des défaillances passées du projet zav-sandbox.
> Chaque entrée documente un échec réel, sa cause, et le correctif appliqué.
> **CONSULTER CE FICHIER AVANT TOUTE IMPLÉMENTATION** — pour éviter de répéter les mêmes erreurs.

---

## Format d'entrée

```
## FM-XXX — {titre court}
- **Date**: YYYY-MM-DD
- **Sévérité**: low | medium | high
- **Agent(s) impliqué(s)**: {noms}
- **Description**: Ce qui s'est passé
- **Cause racine**: Pourquoi ça s'est produit
- **Correctif**: Ce qui a été fait pour corriger
- **Règle ajoutée**: Quelle règle/guard a été créée pour l'éviter
```

---

## FM-001 — Solo execution sans délégation

- **Date**: 2026-03-01
- **Sévérité**: high
- **Agent(s) impliqué(s)**: Gsane Master
- **Description**: Gsane Master a exécuté des tâches GSANE directement sans passer par le système de délégation — violation du PRE-EXECUTION GATE
- **Cause racine**: Absence de gate de gouvernance obligatoire avant l'exécution
- **Correctif**: Ajout du PRE-EXECUTION GATE dans `copilot-instructions.md` et `AGENTS.md`
- **Règle ajoutée**: PRE-EXECUTION GATE — vérification obligatoire de la delegation matrix avant toute action GSANE

---

## FM-002 — Fichiers `_gsane/` non trackés dans git

- **Date**: 2026-03-01
- **Sévérité**: medium
- **Agent(s) impliqué(s)**: Gsane Master
- **Description**: 507 fichiers du répertoire `_gsane/` n'étaient pas trackés par git — ancien dossier source toujours actif dans le tracking alors que `_gsane/` n'existait pas encore côté git
- **Cause racine**: Migration du framework source vers GSANE partielle — le `git add` initial n'avait pas inclus `_gsane/`
- **Correctif**: `git add _gsane/` explicite + `git add -u` pour désindexer les anciens fichiers du framework source
- **Règle ajoutée**: Validation CI T5 — check `_gsane/core/agents` présent dans la structure

---

## FM-003 — Commits multi-sujets sur une seule branche

- **Date**: 2026-03-01
- **Sévérité**: medium
- **Agent(s) impliqué(s)**: Gsane Master
- **Description**: Plusieurs sujets non liés commités sur la même branche, rendant les PRs difficiles à reviewer et à reverter
- **Cause racine**: Absence de règle explicite de portée de branche
- **Correctif**: Ajout de la règle "1 branche = 1 unité logique" dans `git-workflow/workflow.md` et `CONTRIBUTING.md §3`
- **Règle ajoutée**: Branch reuse rule — seule exception : corriger un oubli sur une PR non encore mergée

---

## FM-004 — CLI `gh` introduit sans validation

- **Date**: 2026-03-01
- **Sévérité**: high
- **Agent(s) impliqué(s)**: Gsane Master
- **Description**: La commande `gh` (GitHub CLI) a été introduite dans plusieurs workflows et scripts sans vérifier sa disponibilité dans l'environnement. Causait des erreurs silencieuses dans CI et hooks.
- **Cause racine**: Dépendance directe à un outil externe non validé comme prérequis du projet
- **Correctif**: Suppression complète de `gh` dans 7 fichiers — PRs remplacées par URL compare GitHub + body template manuel
- **Règle ajoutée**: DL-001 — gh CLI banni du projet GSANE

---

## FM-005 — Branche Tier 1 supprimée avant merge

- **Date**: 2026-03-01
- **Sévérité**: medium
- **Agent(s) impliqué(s)**: Gsane Master
- **Description**: La branche `feature/gsane-tier1-improvements-2026-03-01` contenant Failure Museum, Decision Log, CC-verify, Plan/Act, [THINK] a été supprimée avant d'être mergée dans `main` — perte de travail
- **Cause racine**: Confusion entre "supprimer une branche" et "fermer une PR" — la branche était encore non-mergée
- **Correctif**: Re-implémentation complète de Tier 1 + Tier 2 sur nouvelle branche
- **Règle ajoutée**: Vérifier `git branch -a` + `git log branch ^main` avant toute suppression de branche

---

## FM-006 — Tests et implémentation exécutés solo sans party mode ni routing

- **Date**: 2026-03-02
- **Sévérité**: high
- **Agent(s) impliqué(s)**: Gsane Master
- **Description**: Gsane Master a exécuté des validations automatiques (paths, flywheel), des migrations persona V2 (architect, pm), puis "joué" les rôles d'Aria et Murat pour valider ses propres outputs — le tout sans activer le party mode, sans router via la delegation workflow, sans validation ≥2 agents réels.
- **Cause racine**: Momentum de session — les étapes précédentes avaient été validées correctement, mais l'exécution concrète a continué en solo. Absence d'un trip wire spécifique pour les run_in_terminal sur artefacts GSANE. Absence d'une règle interdisant explicitement la substitution de persona.
- **Correctif**: Ajout de NO_PERSONA_SUBSTITUTION et PRE-ACTION-GATE dans gsane-master.md. Party mode élargi à 5 agents. Règle d'or universelle sur tous les agents.
- **Règle ajoutée**: NO_PERSONA_SUBSTITUTION dans gsane-master.md — toute simulation non routée est [NON-AUTHORITATIVE]. PRE-ACTION-GATE step — obligatoire avant toute validation/test/review.
