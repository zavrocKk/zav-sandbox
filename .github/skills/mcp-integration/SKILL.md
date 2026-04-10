# Skill: MCP Integration — Utilisation des outils depuis un agent

## Vue d'ensemble
Ce skill enseigne aux agents GSANE comment **invoquer** les 8 outils MCP disponibles
dans le runtime, quand les utiliser, et comment interpréter leurs résultats.

## Outils disponibles

| Outil | Usage | Quand l'utiliser |
|-------|-------|-----------------|
| `gsane_read_canonical_brief()` | Lire le brief humain canonique | Début de session, orientation |
| `gsane_read_active_delivery_contract()` | Lire le contrat actif | Avant toute implémentation |
| `gsane_read_project_snapshot()` | Snapshot du repo (agents, workflows, contrat) | Vue d'ensemble rapide |
| `gsane_fetch_compressed_memory(query)` | Chercher dans _memory/ | Avant de prendre une décision |
| `gsane_write_session_checkpoint(...)` | Sérialiser un checkpoint audit | Fin de session ou changement de contexte |
| `gsane_read_checkpoint()` | Lire le dernier checkpoint | Reprise de session |
| `gsane_route(query)` | Routage déterministe via delegation-matrix | Triage d'une requête entrante |
| `gsane_memory_fetch(agent, topic)` | Mémoire sidecar d'un agent | Consultation inter-agent |

## Règles d'utilisation
1. **Toujours** lire le brief canonique en début de session
2. **Toujours** lire le Delivery Contract avant de coder
3. **Ne jamais** écrire dans session-state.md manuellement — utiliser `gsane_write_session_checkpoint`
4. Les résultats sont en YAML compressé — ne pas reformatter
5. `gsane_route()` est déterministe — respecter le routage retourné

## Erreurs courantes
- Oublier de consulter `gsane_fetch_compressed_memory` avant une décision (perte de contexte durable)
- Ignorer le routage de `gsane_route()` (violation de gouvernance)
- Écrire directement dans les fichiers mémoire au lieu d'utiliser les outils MCP
