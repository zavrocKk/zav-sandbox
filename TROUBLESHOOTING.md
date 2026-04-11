# Troubleshooting — zav-sandbox / GSANE

## Problèmes fréquents

### L'agent ne répond pas dans la bonne langue
**Cause** : `{communication_language}` non chargé depuis `_gsane/config.yaml`.
**Fix** : Vérifier que `config.yaml` contient `communication_language: "Français"` et que l'agent le charge à l'étape d'activation.

### Les tests échouent sur un fichier manquant
**Cause** : Migration V2 incomplète — certains fichiers référencés n'ont pas été recréés.
**Fix** : Exécuter `pytest tests/ -v` et créer les fichiers manquants signalés.

### MCP server ne démarre pas
**Cause** : Dépendances non installées.
**Fix** :
```bash
cd _gsane/mcp-server
pip install -r requirements.txt
python server.py
```

### Le flywheel tourne en boucle
**Cause** : Pas de seuil de convergence défini.
**Fix** : Vérifier `_gsane/_memory/flywheel-history.md` — si les 3 dernières entrées sont identiques, le flywheel a convergé.

### Delivery Contract non généré
**Cause** : La demande n'a pas été routée via Master. Un agent dev ne génère jamais de contract seul.
**Fix** : Toujours commencer par Master (`@Langis` ou mode Master).

### Coverage en dessous du seuil (50%)
**Cause** : Le seuil CI est `--cov-fail-under=50` (configuré dans `.github/workflows/ci.yml`).
**Fix** :
```bash
pytest tests/ --cov=src --cov-report=term-missing
```
Identifier les modules non couverts et ajouter les tests manquants.

### trace.log corrompu (YAML invalide)
**Cause** : Ancien format YAML avec append séquentiel.
**Fix** : Migrer vers le format JSONL. Chaque entrée = 1 ligne JSON indépendante.

### Agent en boucle sur [CC] FAIL
**Cause** : Pas de circuit-breaker configuré.
**Fix** : Vérifier que `standard-agent-behavior.md` Section 10 R-CC contient `max_retries = 2`.

## Commandes utiles

| Action | Commande |
|--------|----------|
| Lancer les tests | `pytest tests/ -v` |
| Lancer les tests avec coverage | `pytest tests/ --cov=src --cov-report=term-missing` |
| Lint Python | `ruff check src/ tests/` |
| Type check | `mypy src/ --ignore-missing-imports` |
| Scan sécurité | `bandit -r src/ _gsane/tools/ -ll` |
| Health check MCP | `python _gsane/mcp-server/server.py --help` |
| Vérifier les manifests | `grep "^- name:" _gsane/_config/agent-manifest.yaml` |
