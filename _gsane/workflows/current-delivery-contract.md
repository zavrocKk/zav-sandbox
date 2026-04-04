# Delivery Contract : Refonte Onboarding (README & CONTRIBUTING)

## 📌 Contexte & Objectif
Suite à l'analyse des lacunes documentaires (Gap Analysis), les fichiers README.md et CONTRIBUTING.md sont trop abstraits pour un développeur externe. L'objectif est de professionnaliser l'Accueil (Onboarding) du dépôt avec les standards Open Source (badges, prérequis, commandes concrètes, architecture visuelle) et un glossaire métier clair.

## 🎯 Critères d'Acceptation

### 1️⃣ README.md (Vitrine)
- [ ] Ajouter les Badges de statut (CI, Version, Maintien).
- [ ] Ajouter une définition vulgarisée de GSANE (Governance System for AI-Native Execution).
- [ ] Créer une section **Prérequis** (Python 3.14+, pytest, bash).
- [ ] Créer une section **Installation** (git clone, venv, activation, pip install).
- [ ] Fournir l'**exemple de commande réel** pour interagir avec l'outil (`bash gsane.sh validate`).
- [ ] Ajouter le **Schéma d'Architecture** (Strike Team O(1)) et ses rôles clés.
- [ ] Corriger la coquille dans l'arborescence (remplacer les références corrompues par `tests/`).
- [ ] Ajouter des liens rapides vers AGENTS.md, CHANGELOG.md et CONTRIBUTING.md.

### 2️⃣ CONTRIBUTING.md (Règles Métier)
- [ ] Insérer un **Glossaire des termes GSANE** ("Delivery Contract", "Zero-Touch Fix-Loop", "Quality Gate").
- [ ] Détailler le **Setup Développeur** complet (clone -> venv -> tests).
- [ ] Fixer la **Convention de Nommage Git** (Branches `feat/`, `fix/` et Conventional Commits).
- [ ] Détailler le **Workflow de Pull Request** (Description CI obligatoire, jamais de push direct sur main).
- [ ] Clarifier les **Règles de Qualité (Style/Linting)** : tests obligatoires dans `tests/` et ligne obligatoire dans CHANGELOG.md.
- [ ] Expliquer brièvement comment **Ajouter un Nouvel Agent** dans la Strike Team (Création de md + manifests).

## 🛃 Risques et Impacts
- **Risque** : Aucun risque fonctionnel sur l'application (src/). Modification 100% Markdown.
- **Impact** : Amélioration drastique de la DX (Developer Experience) et fiabilisation de l'Open Source.

