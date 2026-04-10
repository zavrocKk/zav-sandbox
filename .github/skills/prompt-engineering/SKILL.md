---
name: prompt-engineering
description: "Structure un Delivery Contract, un brief agent, ou une requête composée pour maximiser la qualité de réponse."
---

# Prompt Engineering — GSANE

## Structurer un Delivery Contract

Un Delivery Contract est le document de référence entre Master (Langis) et un agent exécutant.

### Template minimal

```
## Delivery Contract — {TASK_ID}

**Objectif** : {description claire en 1 phrase}
**Agent assigné** : {nom}
**Sévérité** : LOW | MEDIUM | HIGH
**Date** : {ISO 8601}

### Critères d'acceptation (AC)
- [ ] AC1: {critère vérifiable}
- [ ] AC2: {critère vérifiable}

### Contraintes
- {contrainte technique ou métier}

### Fichiers concernés
- {chemin/fichier.ext} — {action: créer|modifier|supprimer}

### Definition of Done
- Tous les AC cochés
- Tests passent (`pytest tests/ -v`)
- [CC] PASS via cc-verify
```

## Structurer un brief agent (runSubagent)

```
Contexte: {1 phrase sur l'état actuel}
Tâche: {verbe d'action + objet + critère de succès}
Contraintes: {ce qui est interdit ou obligatoire}
Output attendu: {format exact de la réponse}
```

## Requête composée (multi-step)

Pour les tâches complexes, décomposer en étapes numérotées :
1. **Analyser** — lire les fichiers X, Y, Z
2. **Décider** — choisir l'approche selon {critère}
3. **Implémenter** — modifier {fichier} avec {changement}
4. **Valider** — exécuter les tests et confirmer [CC] PASS

## Anti-patterns

- ❌ Prompt vague : "améliore le code"
- ❌ Pas de critère de succès mesurable
- ❌ Mélanger analyse et implémentation dans un seul prompt
- ❌ Oublier de spécifier le format de sortie attendu
```
