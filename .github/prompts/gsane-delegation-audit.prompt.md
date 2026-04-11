---
name: gsane-delegation-audit
description: >
  Auditer l'historique des routages et détecter
  les patterns de solo-creep ou mauvais routing.
mode: ask
---

Audit de délégation GSANE.

Analyse des derniers événements de routing :

```bash
bash gsane.sh trace --summary
```

Vérification anti-solo-creep :
```bash
bash gsane.sh trace --p2p
```

Points à analyser :
1. Langis a-t-il modifié des fichiers directement ?
   → solo-creep HIGH si oui
2. Les requêtes sont-elles routées vers le bon agent ?
   → Vérifier delegation-matrix.yaml si doute
3. Y a-t-il des CHALLENGEs non résolus ?
   → Logger via gsane_emit_event si trouvé
4. Le trust_score moyen est-il acceptable (≥3) ?

Résumé attendu :
- Ratio solo-creep : X%
- Routages corrects : X/Y
- CHALLENGEs ouverts : N
- Trust score moyen : X.X
