# Health Check — Diagnostic GSANE

Exécuter le diagnostic complet de l'environnement GSANE.

```bash
bash gsane.sh doctor
```

## Vérifie

1. Liens morts dans les hooks de session
2. Intégrité de l'arbre YAML `_gsane/_config/`
3. Existence des fichiers référencés dans les manifestes
4. Environnement Python et dépendances
5. Détection Windows/WSL et recommandations

Si EXIT 0 → environnement sain.
Si EXIT 1 → lire les erreurs et appliquer les corrections suggérées.
