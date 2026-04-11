---
name: gsane-party-mode
description: >
  Lancer le party-mode collectif sur une décision
  ou modification GSANE. Vote APPROVE/BLOCK/CHALLENGE.
mode: ask
---

Lancement du Party Mode GSANE.

Décris la décision ou modification à soumettre au vote collectif de la Strike Team.

La Strike Team va voter :
- APPROVE  → valide la décision
- BLOCK    → arrête l'action (besoin de ≥2)
- CHALLENGE → force une justification technique
- ABSTAIN  → neutre

Format de vote attendu par agent :
```
[{AGENT}] {APPROVE|BLOCK|CHALLENGE|ABSTAIN}
Raison : {1 phrase}
```

Consensus requis : ≥2 APPROVE pour procéder.
BLOCK ≥2 : action stoppée.
CHALLENGE : l'auteur doit défendre en 1 échange.

Quelle décision soumets-tu au vote ?
