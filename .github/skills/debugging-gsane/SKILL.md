---
name: debugging-gsane
description: "Diagnostiquer les problèmes courants du framework GSANE : boucles, TTL, hallucinations, MCP, sidecars."
---

# Debugging GSANE

## Diagnostic rapide

| Symptôme | Cause probable | Action |
|----------|---------------|--------|
| Agent en boucle infinie | Pas de circuit-breaker, [CC] FAIL répété | Vérifier max_retries dans R-CC (max 2) |
| Réponse hors sujet | Sidecar pollué (> 60 lignes) | Lancer compaction du sidecar |
| MCP tool timeout | Chemin Windows vs Unix | Vérifier `Path(__file__).resolve()` |
| Agent ne charge pas le contexte | Fichier sidecar absent | Créer `_gsane/_memory/{agent}-sidecar/project-state.md` |
| [DA] ne ferme pas la session | Syntaxe Markdown interceptée | Utiliser `/DA` ou vérifier le parser |
| Trust score toujours > 90 | Auto-évaluation biaisée | Forcer cross-validation par un autre agent |
| trace.log corrompu | Format YAML avec append | Migrer vers JSONL (v2.3+) |

## Vérifier la santé MCP

```bash
# Test de connectivité
python _gsane/mcp-server/server.py --help

# Vérifier les chemins
python -c "from _gsane.mcp-server.compression_tool import MEMORY_DIR; print(MEMORY_DIR.exists())"
```

## Lire les logs

```bash
# Dernières entrées trace.log
tail -20 _gsane/_memory/trace.log

# Échecs dans le failure museum
grep "OPEN" _gsane/_memory/failure-museum.md
```

## Vérifier la cohérence des manifests

```bash
# Compter les agents déclarés vs fichiers réels
ls _gsane/agents/*.md | wc -l          # doit être 5
grep "^- name:" _gsane/_config/agent-manifest.yaml | wc -l  # doit être 5
```

## Patterns d'erreur fréquents

### 1. Flywheel qui ne converge pas
- Vérifier `_gsane/_memory/flywheel-history.md` — les entrées se répètent-elles ?
- Cause : pas de delta mesurable entre les itérations
- Fix : ajouter un `delta_threshold` dans le workflow flywheel

### 2. Delivery Contract manquant
- L'agent dev refuse de coder → comportement NORMAL (gouvernance)
- Fix : demander à Master de générer le contract d'abord

### 3. Cross-validation impossible
- Tous les validateurs sont aussi producteurs → deadlock
- Fix : vérifier le mapping dans standard-agent-behavior.md Section 7
```
