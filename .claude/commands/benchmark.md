# Benchmark — Tests de performance MCP

Exécuter les 4 benchmarks de performance des composants MCP critiques.

```bash
bash gsane.sh benchmark
```

## Métriques mesurées

| Benchmark | Seuil | Composant |
|-----------|-------|-----------|
| gsane_route | < 500ms | Routage delegation-matrix |
| yaml_parse | < 200ms | Parsing config.yaml |
| fetch_memory | < 1000ms | Lecture mémoire compressée |
| checkpoint_read | < 500ms | Lecture checkpoint session |

Si un benchmark dépasse son seuil → FAIL avec détail de la métrique.
