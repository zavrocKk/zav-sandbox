---
name: ci-setup
description: "Setup CI/CD pipeline pour le projet. Piloté par Winston (Architect), validé par Quinn (QA)."
version: 1.0
---

# Workflow : CI Setup

> Piloté par Winston. Validé par Quinn.

## Déclencheur
Ce workflow est invoqué quand le projet a besoin d'une configuration CI/CD initiale ou d'une mise à jour significative du pipeline.

## Étapes

### 1. Analyse des besoins CI
- Identifier les langages et frameworks du projet
- Lister les checks requis : linting, tests, security scan, coverage

### 2. Création/mise à jour du pipeline
- Fichier cible : `.github/workflows/ci.yml`
- Outils : ruff (lint), mypy (types), pytest-cov (coverage), bandit (SAST), pip-audit (deps)
- Configurer Dependabot si non présent : `.github/dependabot.yml`

### 3. Validation
- `bash gsane.sh validate` doit passer
- Le pipeline CI doit s'exécuter sans erreur sur la branche courante

### 4. Documentation
- Mettre à jour CHANGELOG.md avec entrée [chore]
- Documenter les décisions CI dans un ADR si choix significatifs
