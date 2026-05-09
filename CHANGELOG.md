# Changelog — Agentic Team Framework

---

## [2026-05-09] - Règle périmètre projet (orchestrator)

### Added

Ajout d'une section "Périmètre projet — règle absolue" rendant explicite que mentionner
un autre projet ≠ autoriser son accès. Protège contre l'interprétation extensive d'une
mention contextuelle utilisateur.
Fichiers modifiés : `.github/agents/orchestrator.agent.md`
Réf : ADR-0004 correctif 1.A

---

## [2026-05-02] - Référencer incident-triage dans incident-response

### Changed

Ajout d'une règle explicite en phase 1 (Triage) pointant vers la checklist `incident-triage.md`.
Fichiers modifiés : `agents/workflows/incident-response.md`
Réf : ADR-0002 action 1.a

---

## [2026-05-02] - Référencer incident-triage dans le mapping orchestrator

### Changed

Ajout d'une colonne Checklist dans le tableau de mapping de l'orchestrateur, avec `incident-triage.md` sur la ligne incident/panne.
Fichiers modifiés : `.github/agents/orchestrator.agent.md`
Réf : ADR-0002 action 1.b

---

## [2026-05-02] - Référencer security-review dans code-analysis

### Changed

Ajout d'une règle explicite en phase 4 (Sécurité) pointant vers la checklist `security-review.md`.
Fichiers modifiés : `agents/workflows/code-analysis.md`
Réf : ADR-0002 action 1.c

---

## [2026-05-02] - Référencer security-review dans le mapping orchestrator

### Changed

Ajout de `security-review.md` dans la colonne Checklist du mapping pour la ligne audit/review.
Fichiers modifiés : `.github/agents/orchestrator.agent.md`
Réf : ADR-0002 action 1.d

---

## [2026-05-02] - Référencer pre-deploy dans feature-development

### Changed

Ajout d'une règle explicite en phase 6 (Infra/déploiement) pointant vers la checklist `pre-deploy.md`.
Fichiers modifiés : `agents/workflows/feature-development.md`
Réf : ADR-0002 action 1.e

---

## [2026-05-02] - Ajouter section Checklists dans developer, qa, architect

### Changed

Ajout de la section "Checklists à consulter" (modèle devops.md) pointant vers `pre-deploy.md`.
Fichiers modifiés : `agents/personas/developer.md`, `agents/personas/qa.md`, `agents/personas/architect.md`
Réf : ADR-0002 action 1.f

---

## [2026-05-02] - Centraliser le contrat Scribe dans scribe.md

### Changed

Déplacement de la définition Type A/B, de la table de templates et de l'anti-pattern interdit depuis `orchestrator.agent.md` vers `scribe.md` (source de vérité unique). Remplacement par des pointeurs dans l'orchestrateur.
Fichiers modifiés : `agents/personas/scribe.md`, `.github/agents/orchestrator.agent.md`
Réf : ADR-0002 actions 2.a-2.d

---

## [2026-05-02] - Refactor orchestrator.agent.md (PRE-FLIGHT extrait + compaction)

### Added

Création de `agents/protocols/preflight.md` avec les 4 questions PRE-FLIGHT.

### Changed

Remplacement de la section PRE-FLIGHT par un pointeur vers le protocole. Compaction du fichier de 205 à 100 lignes (SYNTHESIS inline, anti-pattern condensé, RAPPEL FINAL supprimé).
Fichiers modifiés : `.github/agents/orchestrator.agent.md`, `agents/protocols/preflight.md` (créé)
Réf : ADR-0002 actions 3.a-3.c

---

## [2026-05-02] - Alléger orchestrator.md (persona)

### Changed

Réduction de 57 à 20 lignes. Suppression des redondances avec `orchestrator.agent.md`. Ajout d'un pointeur vers le custom agent pour les règles complètes.
Fichiers modifiés : `agents/personas/orchestrator.md`
Réf : ADR-0002 action 4

---

## [2026-05-02] - Mettre à jour copilot-instructions.md

### Changed

Ajout du pointeur vers `VISION.md` en tête de fichier. Remplacement de la table des personas par un lien vers `orchestrator.agent.md`. Ajout de la section "Ressources de référence".
Fichiers modifiés : `.github/copilot-instructions.md`
Réf : ADR-0002 action 5

---

## [2026-05-02] - Adapter data-engineer.md (alléger)

### Changed

Réduction de 103 à ~60 lignes. Suppression des sujets experts (Z-ordering, Iceberg/Delta, Spark internals, formats Parquet/Avro/ORC, partitionnement avancé). Ajout section Checklists. Persona recentré sur analyste qui touche à la data.
Fichiers modifiés : `agents/personas/data-engineer.md`
Réf : ADR-0002 action 6

---

## [2026-05-02] - Aligner data-pipeline.md avec le persona allégé

### Changed

Suppression des références expert (data contracts inter-équipes, dbt internals, DAG/XComs). Ajout de la référence `pre-deploy.md` en phase 5. Simplification des descriptions pour un analyste qui touche à la data.
Fichiers modifiés : `agents/workflows/data-pipeline.md`
Réf : ADR-0002 action 7

---

## [2026-05-02] - Corrections ciblées workflows (8.a + 8.b)

### Fixed

**8.a** : Ajout du critère de choix persona pour la phase 4 RCA dans `incident-response.md` (Dev / DevOps / Security selon nature des hypothèses).
**8.b** : Restauration des sauts de ligne entre anti-patterns collés dans `code-analysis.md`.
Fichiers modifiés : `agents/workflows/incident-response.md`, `agents/workflows/code-analysis.md`
Réf : ADR-0002 actions 8.a-8.b

---

## [2026-05-02] - Créer agents/templates/runbook.md

### Added

Template de runbook opérationnel avec frontmatter, vue d'ensemble, prérequis, procédures (démarrage/arrêt/scaling), procédures d'incident (symptôme/diagnostic/mitigation/vérification), métriques, contacts d'escalade, historique.
Fichiers modifiés : `agents/templates/runbook.md` (créé)
Réf : ADR-0002 action 9

---

## [2026-05-02] - Créer agents/templates/architecture.md

### Added

Template de document d'architecture avec frontmatter, vue d'ensemble, diagramme C4 Container en Mermaid, tableau des composants, flux principaux (séquence Mermaid), décisions structurantes (liens ADRs), considérations transverses (sécurité, performance, observabilité, coûts).
Fichiers modifiés : `agents/templates/architecture.md` (créé)
Réf : ADR-0002 action 10
