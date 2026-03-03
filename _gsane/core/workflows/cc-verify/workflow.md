---
name: cc-verify
description: "Completion Contract — 20-point checklist to verify a task is truly done before declaring it complete. Covers git, CHANGELOG, quality, manifests, and CI."
---

# Completion Contract (CC) — Workflow

**Commande**: `[CC]` ou `/gsane-cc-verify`  
**Agent**: Gsane Master  
**Déclenchement**: Avant de déclarer toute tâche terminée

---

## Objectif

Vérifier qu'une tâche GSANE est **réellement complète** avant de la clore — rien de manqué, rien de cassé, rien de non-commité.

**Règle absolue** : aucun "c'est fait !" sans avoir passé ce contrat.

---

## Checklist CC — 20 vérifications en 5 sections

### A — Git & Branches

- [ ] **A1** — Tous les fichiers modifiés sont stagés (`git status` clean)
- [ ] **A2** — Un commit existe sur une branche `feature/*` ou `fix/*` (jamais direct sur `main`)
- [ ] **A3** — La branche a été pushée sur `origin`
- [ ] **A4** — L'URL de PR a été fournie à l'utilisateur : `https://github.com/zavrocKk/zav-sandbox/pull/new/{branch}`
- [ ] **A5** — Le nom de branche respecte la convention `{type}/{description}-YYYY-MM-DD`

### B — CHANGELOG

- [ ] **B1** — Une entrée existe sous `## [Unreleased]` pour cette tâche
- [ ] **B2** — L'entrée inclut : type, description, agent, workflow, impact, branche
- [ ] **B3** — Aucune entrée CHANGELOG ne fait référence à des chemins de l'ancien framework source

### C — Qualité du changement

- [ ] **C1** — Les fichiers créés/modifiés ne contiennent aucune référence cassée (path inexistant)
- [ ] **C2** — Aucune référence vers l'ancien framework source dans les fichiers `_gsane/` ou `.github/`
- [ ] **C3** — Les nouveaux fichiers ont le bon format (frontmatter YAML si agent/workflow)
- [ ] **C4** — Le Failure Museum a été consulté avant implémentation (pas de repeat FM-XXX)
- [ ] **C5** — Si le changement est MEDIUM/HIGH sévérité → Party Mode a été activé

### D — Manifests & Config

- [ ] **D1** — Si un nouveau workflow créé → entrée ajoutée dans `_gsane/_config/workflow-manifest.csv`
- [ ] **D2** — Si un nouvel agent créé → entrée ajoutée dans `_gsane/_config/agent-manifest.csv`
- [ ] **D3** — Si un nouveau task créé → entrée ajoutée dans `_gsane/_config/task-manifest.csv`
- [ ] **D4** — `_gsane/core/config.yaml` n'a pas été modifié pour des raisons non-prévues

### E — CI & Tests

- [ ] **E1** — Les checks CI T1–T8 sont attendus PASS sur cette PR (aucun déprecated path, structure OK, CHANGELOG format OK)
- [ ] **E2** — Si un nouveau CI check a été ajouté → il est documenté dans le CHANGELOG
- [ ] **E3** — `_gsane-output/bmb-creations/.gitkeep` et `test-artifacts/.gitkeep` sont présents dans git

---

## Résultat

**CC PASS** → Tous les items cochés → La tâche est officiellement complète, la PR peut être créée/soumise.

**CC FAIL** → Au moins un item non-coché → Corriger avant de déclarer "fait".

---

## Usage

Gsane Master doit exécuter ce workflow automatiquement quand l'utilisateur dit :
- "c'est bon", "c'est fait", "c'est terminé", "on peut merger", "push it"
- Ou explicitement : `[CC]` ou `/gsane-cc-verify`

Format de sortie minimal :
```
[CC] ✅ PASS — {N}/20 checks OK — Prêt pour PR
[CC] ❌ FAIL — {N}/20 checks OK — Items manquants : {liste}
```
