---
name: post-feature-doc
description: "Vérifie la complétude documentaire après chaque feature livrée. Déclenché par cc-verify. Non bloquant."
version: 1.0
---

# Workflow : Post-Feature Documentation

> Piloté par Langis (Master). Validé par Quinn (linting Markdown).
> Déclenché automatiquement par cc-verify après [CC] PASS.

## Déclencheur
Ce workflow s'exécute automatiquement à la fin de cc-verify quand [CC] = PASS.

## Étapes

### 1. Vérification CHANGELOG
- Le fichier CHANGELOG.md contient-il une entrée pour la feature/tâche courante ?
- Si non → émettre [DOC] WARN : "CHANGELOG entry manquante"

### 2. Vérification ADR (si décision architecture)
- La tâche implique-t-elle une décision d'architecture (nouveau pattern, nouvelle dépendance) ?
- Si oui, un ADR existe-t-il dans `docs/architecture/decisions/` ?
- Si non → émettre [DOC] WARN : "ADR recommandé pour cette décision"

### 3. Vérification README/AGENTS.md
- Les fichiers modifiés changent-ils l'interface publique du projet ?
- Si oui, README.md ou AGENTS.md reflète-t-il ces changements ?
- Si non → émettre [DOC] WARN : "README/AGENTS.md potentiellement obsolète"

### 4. Résultat
- Aucun WARN → [DOC] PASS
- Au moins 1 WARN → [DOC] WARN avec liste des avertissements
- Ce résultat n'est JAMAIS bloquant — il est informatif uniquement
