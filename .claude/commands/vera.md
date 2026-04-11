# Vera — Security Checks

Exécuter les 2 checks de sécurité Vera intégrés dans security_gate.py.

```bash
bash gsane.sh vera
```

## Checks exécutés

1. **Prompt Injection** — Scanne les fichiers `_gsane/agents/*.md` pour détecter des patterns d'injection (ignore previous instructions, disregard your rules, etc.)
2. **CI Permissions** — Vérifie les workflows `.github/workflows/*.yml` pour des permissions trop larges (`write-all`, writes non-essentiels)

## Résultats

- EXIT 0 (CLEAR) → aucun finding HIGH
- EXIT 1 (FINDING) → au moins un finding HIGH détecté — corriger avant merge
