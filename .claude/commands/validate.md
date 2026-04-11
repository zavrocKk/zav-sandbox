# Quality Gate — GSANE Validate

Exécuter la quality gate complète du projet : pytest + qa-linter + vérification CHANGELOG.

```bash
bash gsane.sh validate
```

Si EXIT 0 → tout est propre.
Si EXIT 1 → lire le rapport d'erreurs et proposer les corrections.
