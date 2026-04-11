---
name: gsane-benchmark
description: >
  Mesurer les performances GSANE et détecter
  les régressions vs baseline.
mode: ask
---

Benchmark GSANE — mesure de performance.

```bash
bash gsane.sh benchmark
```

Métriques mesurées vs baseline (config.yaml) :
- `gsane_route()`          < 100ms
- `gsane_fetch_memory()`   < 200ms
- YAML manifests parse     < 50ms
- checkpoint read          < 100ms

Interprétation :
- Tout PASS → baseline respectée ✅
- Régression > 20% → [CHALLENGE] Quinn → Amelia
  avec delta précis : "{outil} {actual}ms > {limit}ms"
- Cause architecturale → Winston produit un ADR

Veux-tu lancer le benchmark maintenant ?
