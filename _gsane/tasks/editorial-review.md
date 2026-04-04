---
name: editorial-review
description: "Révision éditoriale d'un document GSANE : orthographe, cohérence, style."
version: 1.0
---

# Task : Editorial Review

## Déclencheur
Un document GSANE (workflow, agent, skill) doit être relu avant commit.

## Étapes
1. Lire le document cible
2. Vérifier : orthographe, cohérence des termes (Strike Team, noms d'agents corrects)
3. Vérifier : liens et chemins de fichiers présents dans le document
4. Produire une liste de corrections suggérées (format : `ligne X — avant → après`)
5. Si corrections mineures (typos, style) → appliquer directement
6. Si corrections structurelles → présenter à l'utilisateur avant d'appliquer

## Livrable
Liste de corrections appliquées + avertissements le cas échéant.
