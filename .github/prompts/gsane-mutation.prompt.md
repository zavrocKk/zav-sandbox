---
name: gsane-mutation
description: >
  Lancer le mutation testing (mute-mute) pour
  valider que les tests détectent de vrais bugs.
mode: ask
---

Lancement du Mutation Testing GSANE (Mute-Mute).

⚠️ Opération longue : 5-15 minutes.
Scope : `_gsane/mcp-server/` + `_gsane/tools/`
Tests : `tests/unit/` uniquement.

```bash
bash gsane.sh mutation
```

Interprétation du score :
- Score ≥ 70% → tests solides ✅
- Score < 70% → [CHALLENGE] Quinn → Amelia :
  "Tests insuffisants — mutants survivants détectés.
   Renforcer les assertions dans tests/unit/"

Le score est loggé dans config.yaml (last_score).

Veux-tu lancer le mutation testing maintenant ?
