---
name: debugging-gsane
description: "Diagnostiquer les problèmes courants du framework GSANE : boucles, TTL, hallucinations, MCP, sidecars."
---

# Debugging GSANE — Arbre de diagnostic

## 1. Tests rouges après un changement

```
SYMPTÔME : pytest échoue après modification
  ├─ Erreur dans src/ ?
  │   → Agent : Amelia (Dev) — corriger le code
  │   → Commande : pytest tests/test_{module}.py -v --tb=short
  ├─ Erreur dans tests/ (test obsolète) ?
  │   → Agent : Quinn (QA) — mettre à jour le test
  │   → Commande : pytest tests/ -k "test_qui_echoue" -v
  └─ Erreur d'import / dépendance manquante ?
      → Commande : pip install -e ".[test]"
      → Puis : pytest tests/ -v
```

## 2. MCP health check échoue

```
SYMPTÔME : bash gsane.sh mcp --health retourne erreur
  ├─ ImportError ?
  │   → pip install -e ".[mcp]"
  │   → Vérifier : python -c "from mcp.server.fastmcp import FastMCP"
  ├─ FileNotFoundError (chemins) ?
  │   → Vérifier : Path(__file__).resolve() dans compression_tool.py
  │   → Les chemins doivent dériver de __file__, jamais du cwd
  ├─ Erreur de schéma YAML ?
  │   → python -c "import yaml; yaml.safe_load(open('_gsane/_config/delegation-matrix.yaml'))"
  └─ Tout OK mais timeout ?
      → Agent : Winston (Architect) — vérifier la config réseau
```

## 3. gsane.sh validate échoue sur CHANGELOG

```
SYMPTÔME : validate signale CHANGELOG manquant
  → Cause : nouveau code dans src/ sans entrée CHANGELOG
  → Fix : ajouter une ligne dans CHANGELOG.md section [Unreleased]
  → Format : - **{type}({scope})**: {description}
  → Relancer : bash gsane.sh validate
```

## 4. delegation-matrix route vers le mauvais agent

```
SYMPTÔME : requête envoyée au mauvais agent
  ├─ Identifier le faux positif :
  │   → Lire _gsane/_config/delegation-matrix.yaml
  │   → Chercher le trigger qui a matché par erreur
  │   → Comparer keywords requête vs triggers agent
  ├─ Corriger :
  │   → Ajouter/retirer des keywords dans le trigger fautif
  │   → Agent : Bond (Agent Builder) pour modifier la matrice
  └─ Valider :
      → bash gsane.sh validate
      → Tester : gsane_route("requête problématique")
```

## 5. Session dégradée (réponses incohérentes)

```
SYMPTÔME : agent répond hors sujet ou se contredit
  ├─ Signaux d'alerte :
  │   → Répétitions dans les réponses
  │   → Références à des fichiers inexistants
  │   → Ignorance du Delivery Contract actif
  ├─ Actions immédiates :
  │   → Recharger config : relire _gsane/config.yaml
  │   → Compresser mémoire : gsane_fetch_compressed_memory(agent)
  │   → Vérifier sidecar : < 60 lignes, sinon compacter
  └─ Si persistant :
      → [DA] pour fermer la session
      → Redémarrer une session propre
```
