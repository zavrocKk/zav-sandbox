---
name: mcp-integration
description: "Guide d'utilisation des outils MCP GSANE depuis un agent — appels, retry, anti-patterns."
applyTo: "**"
trigger: "utiliser MCP en session, appeler gsane_route, checkpoints MCP"
load: on-demand
priority: medium
---

# MCP Integration — Guide Agent

## 1. gsane_fetch_compressed_memory(agent_name)

**Quand** : Avant toute décision architecturale ou quand le contexte historique est nécessaire.
**Retour** : YAML compressé des fichiers mémoire de l'agent (sidecar, failure-museum, decision-log).

```
résultat = gsane_fetch_compressed_memory("master")
# → YAML avec les entrées mémoire pertinentes
```

## 2. gsane_write_session_checkpoint(agent, status, summary, next_steps)

**Quand** : Fin de tâche longue, avant handoff inter-agent, avant [DA].
**Effet** : Écrit dans `_gsane/_memory/sessions/session-state.md`.

```
gsane_write_session_checkpoint(
  agent="amelia",
  status="IN_PROGRESS",
  summary="AC-1 et AC-2 validés, AC-3 en cours",
  next_steps="Finaliser tests edge cases"
)
```

## 3. gsane_read_checkpoint()

**Quand** : Reprise de session interrompue, cold start avec contexte antérieur.
**Retour** : Dernier checkpoint sérialisé (agent, status, summary, next_steps).

```
checkpoint = gsane_read_checkpoint()
# → Reprendre là où la session précédente s'est arrêtée
```

## 4. gsane_route(request_text)

**Quand** : Triage d'une requête entrante quand l'agent cible n'est pas évident.
**Retour** : Agent recommandé + score de matching.
**vs delegation-matrix directe** : `gsane_route` applique le scoring pondéré + trust_bonus. Utiliser la matrice directe uniquement pour le debug.

```
résultat = gsane_route("créer un nouvel agent de monitoring")
# → {agent: "bond", score: 3, keywords_matched: ["créer", "agent"]}
```

## 5. gsane_memory_fetch(agent, query)

**Quand** : Consultation ciblée de la mémoire d'un agent spécifique sur un sujet.  
**vs gsane_fetch_compressed_memory** : `fetch_compressed_memory` retourne tout le sidecar compressé. `memory_fetch` filtre par query — plus léger, plus précis.

```
résultat = gsane_memory_fetch("winston", "décision architecture MCP")
# → Entrées filtrées du sidecar Winston sur le sujet
```

## Pattern de retry

Si un outil MCP échoue (timeout, FileNotFoundError, connexion perdue) :
1. **Retry 1** : Attendre 2s, réessayer avec les mêmes paramètres
2. **Retry 2** : Vérifier les prérequis (`bash gsane.sh mcp --health`)
3. **Après 2 échecs** : Abandon + log dans failure-museum. Ne PAS boucler.

## Anti-patterns

- Ne PAS appeler MCP en boucle (circuit-breaker = 2 retries max)
- Ne PAS écrire des checkpoints à chaque tour — uniquement aux jalons significatifs
- Ne PAS ignorer le résultat de `gsane_route()` (violation de gouvernance)
- Ne PAS reformatter le YAML compressé retourné — le consommer tel quel
