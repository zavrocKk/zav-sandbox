---
name: index-cleanup
description: "Nettoyage et resynchronisation des manifests YAML avec le filesystem réel."
version: 1.0
---

# Task : Index Cleanup

## Déclencheur
Après ajout/suppression de fichiers GSANE (agents, workflows, skills).

## Étapes
1. Lister tous les fichiers dans `_gsane/agents/`, `_gsane/workflows/`, `.github/skills/`
2. Comparer avec les entrées dans `_gsane/_config/agent-manifest.yaml`, `workflow-manifest.yaml`, `task-manifest.yaml`
3. Identifier :
   - Fichiers présents mais absents du manifest → ajouter
   - Entrées dans le manifest mais fichiers absents → signaler (jamais supprimer silencieusement)
4. Mettre à jour les manifests avec les entrées manquantes
5. Exécuter `bash gsane.sh validate` pour confirmer la cohérence

## Livrable
Rapport de diff (ajouts/suppressions) + confirmation Quality Gate.
