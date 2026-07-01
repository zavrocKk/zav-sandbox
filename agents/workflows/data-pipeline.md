# Workflow — Data Pipeline

Tâches data : ETL/ELT, migration de schéma, modélisation BI, nouveau pipeline d'ingestion.

## Diagramme des phases

```mermaid
flowchart LR
  B[1. Cadrage besoins data<br/>📊 Product Analyst] --> M[2. Modélisation<br/>🗄️ Data Engineer]
  M --> S[3. Sécurité & conformité<br/>🔒 Security]
  M --> I[4. Implémentation pipeline<br/>🗄️ Data Engineer + 💻 Dev]
  S --> I
  I --> O[5. Orchestration & monitoring<br/>🛠️ DevOps]
  O --> Q[6. Stratégie de tests data<br/>🧪 QA]
  Q --> D[7. Documentation<br/>📝 Scribe]
```

> Les phases 3 et 4 démarrent en parallèle dès la fin de la modélisation.

## Personas par phase

| # | Phase                        | Persona principal        | Personas secondaires   | Sortie attendue                                                         |
| - | ---------------------------- | ------------------------ | ---------------------- | ----------------------------------------------------------------------- |
| 1 | Cadrage besoins data         | 📊 Product Analyst       | —                      | Qui consomme, à quelle fraîcheur, pour quelle décision, SLA attendu     |
| 2 | Modélisation                 | 🗄️ Data Engineer         | —                      | Schéma source/cible (DDL), transformations, règles de déduplication     |
| 3 | Sécurité & conformité        | 🔒 Security              | 🗄️ Data Engineer       | PII identifiée, plan de masquage, RGPD, contrôles d'accès               |
| 4 | Implémentation pipeline      | 🗄️ Data Engineer         | 💻 Developer           | Pipeline implémenté, idempotence vérifiée, gestion des erreurs          |
| 5 | Orchestration & monitoring   | 🛠️ DevOps                | —                      | Scheduling, alertes sur SLA, observabilité (freshness, row count, drift) |
| 6 | Stratégie de tests data      | 🧪 QA                    | 🗄️ Data Engineer       | Tests de qualité, contrôles de cohérence, tests de régression           |
| 7 | Documentation                | 📝 Scribe                | —                      | Data dictionary, runbook du pipeline, `docs/YYYY-MM-DD-data-<slug>.md` |

## Règles spécifiques

- **Phase 1 obligatoire** : on ne modélise pas sans savoir qui consomme quoi et à quelle fréquence. Un pipeline sans consommateur identifié est un candidat à la suppression.
- **PII** : dès la phase 2, toute colonne susceptible de contenir un PII est **flaggée**. La phase 3 valide le traitement (masquage, pseudonymisation, droit à l'effacement).
- **Idempotence obligatoire** : tout pipeline doit pouvoir être re-exécuté sur la même fenêtre sans dupliquer les données.
- **Plan de rollback** : toute migration de schéma doit documenter les étapes de rollback avant d'être appliquée.
- **Phase 5 (Orchestration) — utiliser la checklist** `agents/checklists/pre-deploy.md` avant tout déploiement en production.
- **Confirmation utilisateur requise** pour : `DROP TABLE`, `TRUNCATE`, modification d'une colonne utilisée en prod, suppression d'un pipeline actif.

## Anti-patterns

- ❌ Transformation dans le BI (Tableau, Looker, PowerBI) au lieu d'amont dans le pipeline — la logique métier doit vivre dans le pipeline, pas dans un dashboard.
- ❌ Pipeline non idempotent : un re-run duplique les lignes.
- ❌ Pas de monitoring de fraîcheur / volume : on découvre les données manquantes en prod quand un utilisateur se plaint.
- ❌ PII non masquée dans les environnements de dev/test/staging.
- ❌ Schéma sans contraintes (tout nullable) : migration douloureuse garantie.
- ❌ Construire sans cadrage (phase 1) : pipeline inutile ou avec le mauvais grain de données.

## Livrable final

- `docs/YYYY-MM-DD-data-<slug>.md` avec :
  - Résumé : source → transformations → destination → consommateurs
  - Schéma final (DDL)
  - Data dictionary (table des colonnes, types, descriptions, PII flag)
  - Runbook d'exploitation (relance, monitoring, SLA, alertes)
  - Plan de rollback de la migration (si applicable)

> Le runbook d'exploitation est inclus dans le document principal si court (≤ 1 page). Si le pipeline est complexe, l'extraire dans `docs/runbooks/<pipeline>-exploitation.md`.
> Si la migration implique un choix structurant (nouvelle technologie, stratégie de backfill) → l'Architect crée un ADR dans `docs/decisions/`.
> ❌ Les plans de correctifs et lots d'actions → `docs/_scratch/YYYY-MM-DD-plan-<slug>.md` — pas dans `docs/decisions/`.
