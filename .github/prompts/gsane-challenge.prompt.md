---
name: gsane-challenge
description: >
  Émettre un [CHALLENGE] formel contre un artefact
  ou une décision d'un autre agent GSANE.
mode: ask
---

Tu vas émettre un [CHALLENGE] formel.

Réponds en produisant exactement ce format :

```
[CHALLENGE] {agent-source} → {agent-cible}
Sujet      : {DC-ID ou artefact concerné}
Domaine    : {architecture|implémentation|qualité|gouvernance|sécurité|performance}
Argument   : {raison technique précise — 1-3 phrases}
Demande    : {justification|révision|abandon}
```

Règles :
- L'argument doit être technique et précis
- Sans argument précis → CHALLENGE invalide
- Langis arbitre si pas de consensus en 2 échanges
- Logger via gsane_emit_event("challenge_issued")

Quel artefact ou décision veux-tu challenger ?
