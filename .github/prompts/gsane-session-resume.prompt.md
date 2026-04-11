---
name: gsane-session-resume
description: >
  Reprendre une session GSANE interrompue depuis
  le dernier checkpoint MCP.
mode: ask
---

Reprise de session GSANE.

Vérification du dernier checkpoint :

```bash
bash gsane.sh session --resume
```

Si une session interrompue est détectée :
→ Afficher : tâche, agent, prochaine étape
→ Demander : reprendre ou démarrer nouvelle tâche

Si aucune session interrompue :
→ Afficher l'état actuel du projet :
```bash
bash gsane.sh doctor
```
→ Proposer les actions disponibles
