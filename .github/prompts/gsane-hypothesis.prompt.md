---
name: gsane-hypothesis
description: >
  Formuler et tracker une hypothèse testable
  avant d'implémenter un AC complexe.
mode: ask
---

Formulation d'hypothèse GSANE.

Pour l'AC que tu vas implémenter, produis exactement ce format :

```
[HYPOTHÈSE] DC-{ID} AC-{N}
Niveau     : unit | integration | e2e
Condition  : "Si j'appelle X avec input Y..."
Attendu    : "...alors le résultat sera Z"
Contre-ex  : "Sauf si W, auquel cas..."
Test       : "def test_{fonction}_{scenario}():"
Risque     : "Si faux → impact sur AC-{N+1}"
```

Cette hypothèse devient le docstring du test.
Si l'hypothèse est invalidée :
→ Bug dans l'hypothèse → réviser
→ Bug dans le code → fixer
→ Bug architectural → [CHALLENGE] Winston

Quel AC veux-tu couvrir ?
