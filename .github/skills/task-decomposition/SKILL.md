---
name: task-decomposition
description: "Comment Langis (Master) décompose une demande ambiguë en sous-tâches assignables aux agents de la Strike Team."
---

# Task Decomposition — Master Protocol

## Principe

Toute demande utilisateur passe par une décomposition en tâches atomiques avant dispatch.

## Algorithme de décomposition

```
INPUT: requête utilisateur (texte libre)

ÉTAPE 1 — CLASSIFICATION
  → Identifier le type: code | architecture | test | documentation | agent | workflow
  → Si ambigu: appliquer le protocole d'ambiguïté (2 options max)

ÉTAPE 2 — DÉCOUPAGE  
  → Décomposer en sous-tâches indépendantes (max 5 par requête)
  → Chaque sous-tâche = 1 agent assigné + 1 AC vérifiable
  → Identifier les dépendances (séquentiel vs parallèle)

ÉTAPE 3 — ASSIGNATION (via delegation-matrix.yaml)
  code/implémentation  → Amelia (dev)
  tests/validation     → Quinn (qa)  
  architecture/design  → Winston (architect)
  agents/workflows     → Bond
  orchestration/multi  → Langis (master, self)

ÉTAPE 4 — GÉNÉRATION DU DELIVERY CONTRACT
  → Pour chaque sous-tâche assignée à un agent ≠ master
  → Générer un contract avec AC, contraintes, et DoD
  → Dispatch via runSubagent avec le contract en brief

ÉTAPE 5 — SUIVI
  → Attendre le résultat de chaque sous-agent
  → Vérifier [CC] PASS sur chaque livrable
  → Consolider et livrer à l'utilisateur
```

## Exemple concret

**Requête** : "Ajoute un endpoint /health au serveur MCP et teste-le"

**Décomposition** :
1. `[Winston]` Valider le design de l'endpoint (idempotent, stateless)
2. `[Amelia]` Implémenter l'endpoint dans `server.py`
3. `[Quinn]` Écrire les tests dans `test_mcp.py`
4. `[Master]` Vérifier [CC] PASS et merger

## Anti-patterns de décomposition

- ❌ Tout envoyer à un seul agent
- ❌ Sous-tâches avec dépendances circulaires
- ❌ AC non vérifiable ("améliorer la qualité")
- ❌ Plus de 5 sous-tâches (re-découper en phases)
```
