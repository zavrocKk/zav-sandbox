---
name: session-resume
description: "Workflow de reprise de session interrompue"
trigger: "gsane.sh session --resume ou détection automatique au démarrage"
---

# Session Resumption Workflow

## Objectif
Permettre la reprise d'une session GSANE interrompue en restaurant le contexte du dernier checkpoint.

## Étapes

### Step 1 — Détection
Lire le checkpoint via `gsane_read_checkpoint()`. Si `interrupted: true` :
- Afficher le contexte de reprise (tâche, agent, prochaine étape)
- Proposer la reprise

### Step 2 — Reprise
Si l'utilisateur confirme :
1. Charger le Delivery Contract actif (`_gsane-output/current-delivery-contract.md`)
2. Restaurer le contexte de l'agent interrompu
3. Reprendre à la prochaine étape indiquée

### Step 3 — Reset
Si l'utilisateur refuse :
1. Marquer `interrupted: false` dans session-state.md
2. Démarrer une session fraîche

## Intégration
- **CLI** : `bash gsane.sh session --resume`
- **MCP** : `gsane_read_checkpoint()` détecte automatiquement
- **Hook** : `session-stop.sh` marque les interruptions
