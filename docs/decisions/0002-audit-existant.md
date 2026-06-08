---
type: decision
number: 0002
status: accepted
date: 2026-05-02
deciders: [zavrocKk]
tags: [audit, phase-5, gouvernance]
supersedes: none
---

# ADR-0002 — Audit de l'existant (Phase 5.1)

> Document de référence sur l'état du framework Agentic Team à la sortie des Phases 0-3, évalué contre la vision posée en Phase 4.5. Sert de base à la Phase 5.3 (refonte ciblée).

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-05-02
**Décideurs** : utilisateur (zavrocKk)

## Contexte

À l'issue de la Phase 4.5, le projet a posé sa vision dans `VISION.md` : framework agentique pour analystes techniques, équipes DevOps/CI-CD/Platform/SRE, architectes solutions et PO techniques. Différenciation : 100% markdown, natif VSCode + Copilot, anti-drift par design, anti-clone BMAD/AutoGen/CrewAI/LangGraph.

Avant d'attaquer la Phase 5 (MVP basé sur la vision), il fallait évaluer si les artefacts construits en Phases 0-3 (8 personas, 5 workflows, 3 templates, 3 checklists, 1 orchestrator agent, 1 fichier d'instructions) sont **alignés** avec cette vision, ou s'ils nécessitent des ajustements.

Cet audit répond à la question : **« que garde-t-on, qu'adapte-t-on, que supprime-t-on ? »**

## Décision

Audit méthodique en 4 lots séquentiels (gouvernance / personas / workflows / templates+checklists), évaluant chaque artefact contre les 6 filtres de la boussole VISION.md. Verdict par artefact : 🟢 GARDE / 🟡 ADAPTE / 🔄 FUSIONNE / 🔴 SUPPRIME / 🆕 MANQUE.

## Méthode

### Boussole d'évaluation (6 filtres VISION.md)

1. **Pour qui ?** — sert un analyste technique ou une équipe DevOps/CI-CD ?
2. **Configuration ?** — markdown lisible par un non-dev ?
3. **Outils ?** — compatible VSCode + Copilot natif ?
4. **Complexité ?** — un dev senior est-il nécessaire pour le configurer ?
5. **Drift ?** — tient-il sur une session longue ?
6. **Livrables ?** — produit-il un livrable markdown structuré ?

### Périmètre audité (22 artefacts)

| Catégorie | Fichiers |
|---|---|
| Gouvernance (lot A) | `orchestrator.md` (persona), `orchestrator.agent.md` (custom agent), `copilot-instructions.md` |
| Personas (lot B) | `devops`, `developer`, `qa`, `security`, `architect`, `product-analyst`, `data-engineer`, `scribe` |
| Workflows (lot C) | `incident-response`, `code-analysis`, `feature-development`, `architecture-design`, `data-pipeline` |
| Templates + Checklists (lot D) | `incident-report`, `adr`, `prd` (templates) ; `incident-triage`, `security-review`, `pre-deploy` (checklists) |

## Résultats

### Score global

| Lot | Artefacts | 🟢 GARDE | 🟡 ADAPTE | 🔴 SUPPRIME |
|---|---|---|---|---|
| A — Gouvernance | 3 | 1 | 2 | 0 |
| B — Personas | 8 | 6 | 2 | 0 |
| C — Workflows | 5 | 1 | 4 | 0 |
| D — Templates + Checklists | 6 | 6 | 0 | 0 |
| **TOTAL** | **22** | **14 (64%)** | **8 (36%)** | **0 (0%)** |

**+ 2 MANQUE détectés** : templates `runbook.md` et `architecture.md` (avoués comme dette dans `orchestrator.agent.md`).

### Lot A — Gouvernance

| Artefact | Verdict | Raison principale |
|---|---|---|
| `orchestrator.md` (persona) | 🟡 ADAPTE | Redondance avec `orchestrator.agent.md` — 2 sources de vérité. Alléger à ~15-20 lignes, déléguer au custom agent. |
| `orchestrator.agent.md` (custom agent) | 🟡 ADAPTE | 205 lignes, redondance interne. PRE-FLIGHT et Type A/B sont d'excellentes innovations. Refactor en protocoles externes. |
| `copilot-instructions.md` | 🟢 GARDE | Concis, clair. Ajustements mineurs : ref VISION.md, ressources, retirer liste personas dupliquée. |

### Lot B — Personas

| Artefact | Verdict | Raison principale |
|---|---|---|
| `devops.md` | 🟢 GARDE | Exemplaire. Section "Checklists à consulter" déjà présente. |
| `developer.md` | 🟢 GARDE | Solide. Petit manque : ref `pre-deploy.md`. |
| `qa.md` | 🟢 GARDE | Solide. Section "Différence avec Developer" 👍. |
| `security.md` | 🟢 GARDE | Exemplaire. Validé par Phase 4. Section "Checklists" présente. |
| `architect.md` | 🟢 GARDE | Solide. Référence template ADR. |
| `product-analyst.md` | 🟢 GARDE | Solide. Section "Différence avec Architect" 👍. |
| `data-engineer.md` | 🟡 ADAPTE | **Décision actée** : alléger pour analyste qui touche à la data. Retirer Z-ordering, Iceberg, Delta, Spark internals. Garder ce qui sert un non-data-engineer. |
| `scribe.md` | 🟡 ADAPTE | Contrat Scribe (Type A/B + procédure templates) éclaté avec `orchestrator.agent.md`. Centraliser ici. |

### Lot C — Workflows

| Artefact | Verdict | Raison principale |
|---|---|---|
| `incident-response.md` | 🟡 ADAPTE | Phase 1 = Triage mais ne référence pas `incident-triage.md`. |
| `code-analysis.md` | 🟡 ADAPTE | Phase 4 = Sécurité mais ne référence pas `security-review.md`. Petit bug typo ligne 37. |
| `feature-development.md` | 🟡 ADAPTE | Phase 6 = DevOps mais ne référence pas `pre-deploy.md`. Pas de mode "fast track". |
| `architecture-design.md` | 🟢 GARDE | **Exemplaire — modèle à suivre.** Court, parallélisation, règles précises. |
| `data-pipeline.md` | 🟡 ADAPTE | Présuppose un Data Engineer expert — incompatible avec persona allégé (Option A actée). À aligner. |

### Lot D — Templates + Checklists

| Artefact | Verdict | Raison principale |
|---|---|---|
| `incident-report.md` (template) | 🟢 GARDE | Cause technique vs systémique — clé du blameless. |
| `adr.md` (template) | 🟢 GARDE | Format Nygard impeccable. Immutabilité. |
| `prd.md` (template) | 🟢 GARDE | Règle d'or "max 2 pages". |
| `incident-triage.md` (checklist) | 🟢 GARDE | Solide. **Mais sous-utilisée** dans l'écosystème. |
| `security-review.md` (checklist) | 🟢 GARDE | Validé par Phase 4. **Mais sous-utilisée** dans l'écosystème. |
| `pre-deploy.md` (checklist) | 🟢 GARDE | Solide. **Mais sous-utilisée** dans l'écosystème. |

## Patterns transversaux détectés

### 🚨 Pattern 1 — Dette d'intégration des checklists (CRITIQUE)

Les 3 checklists sont **solides en contenu** mais **partiellement orphelines** dans l'écosystème :

- Référencées par : `devops.md` ✅, `security.md` ✅
- **Non référencées par** : 6 personas sur 8, **0 workflow sur 5**, l'orchestrator agent
- Conséquence probable : drift identifié dans `test-notes.md` (« Solo difrt ou oublie de créer les artefacts de synthèse »)

**Diagnostic** : Phase 3 a livré les checklists, Phase 4 a testé un cas (audit sécurité), mais l'**intégration systémique** des checklists dans l'orchestration et les workflows n'a jamais été faite.

### Pattern 2 — Sources de vérité multiples

- **Persona Orchestrator** : `orchestrator.md` + `orchestrator.agent.md` (chevauchement identité, responsabilités, ton, anti-patterns)
- **Liste des personas** : `copilot-instructions.md` + `orchestrator.agent.md` (à 2 endroits)
- **Contrat Scribe** : `scribe.md` + `orchestrator.agent.md` (Type A/B uniquement dans le custom agent)

### Pattern 3 — Pas de fast-track / mode allégé

`feature-development.md` impose 7 phases pour TOUTE feature, même triviale. Risque que l'utilisateur saute des phases en violation du protocole.

### Pattern 4 — Contenu atomique solide, glue manquante

100% des problèmes détectés sont des problèmes d'**INTÉGRATION et GOUVERNANCE**, jamais des problèmes de contenu individuel d'un artefact. Le framework a besoin d'un étage de "glue" entre les fichiers atomiques.

### Pattern 5 — Data Engineer hors-cible

VISION.md ne mentionne pas explicitement les Data Engineers/data analysts dans la cible. Le persona `data-engineer.md` (103 lignes) couvre des sujets pointus (Z-ordering, Iceberg, Delta) qui dépassent le profil "analyste qui touche à la data".

**Décision actée** : 🟡 ADAPTE — alléger pour servir un analyste qui touche à la data sans être Data Engineer expert. `data-pipeline.md` à aligner également.

## Conséquences

### Positives

- 0 fichier à supprimer → **les Phases 0-3 ne sont pas du temps perdu**
- 64% des artefacts sont 🟢 GARDE direct → socle solide
- Tous les templates et checklists sont exemplaires (lot D : 6/6 GARDE)
- L'innovation **Type A vs Type B** dans `orchestrator.agent.md` est une force unique du framework
- L'innovation **PRE-FLIGHT en 4 questions** est un mécanisme anti-drift remarquable

### Négatives

- 36% des artefacts nécessitent des ajustements
- Dette d'intégration des checklists à résoudre **avant** la Phase 5.4 (test du MVP)
- Refactor de `orchestrator.agent.md` non trivial (205 lignes → 3 fichiers ciblés)
- Décision Data Engineer impacte 2 artefacts (persona + workflow)

### Neutres / À surveiller

- 8 nouvelles entrées ajoutées au parking lot `IDEAS.md` (à examiner aux phases appropriées)
- 2 templates manquants à créer : `runbook.md` et `architecture.md` (Phase 5.3)

## Liste consolidée des correctifs (Phase 5.3)

### 🔴 PRIORITÉ HAUTE — Dette d'intégration

1. **Brancher les 3 checklists dans l'écosystème** :
   - `incident-triage.md` → référencer dans `incident-response.md` (phase 1) + `orchestrator.agent.md` (mapping)
   - `security-review.md` → référencer dans `code-analysis.md` (phase 4) + `orchestrator.agent.md`
   - `pre-deploy.md` → référencer dans `feature-development.md` (phase 6) + `developer.md`, `qa.md`, `architect.md`

2. **Centraliser le contrat Scribe dans `scribe.md`** :
   - Déplacer Type A/B (fichier vs consultation) depuis `orchestrator.agent.md`
   - Déplacer la procédure templates obligatoires
   - Déplacer l'anti-pattern interdit (« le PLAN validé est un contrat »)
   - Laisser un simple pointeur dans `orchestrator.agent.md`

3. **Refactor `orchestrator.agent.md`** :
   - Extraire PRE-FLIGHT dans `agents/protocols/preflight.md`
   - Extraire le contrat Scribe (déjà déplacé en action 2)
   - Réduire le fichier principal à ~80 lignes (frontmatter + flux + mapping + références)

### 🟡 PRIORITÉ MOYENNE — Cohérence gouvernance

1. **Alléger `orchestrator.md` (persona)** : passer de 57 lignes à ~15-20 lignes, déléguer au custom agent

2. **Mettre à jour `copilot-instructions.md`** :
   - Ajouter pointeur vers `VISION.md` ("la boussole en cas de doute")
   - Ajouter section "Ressources de référence" listant checklists, templates, workflows
   - Retirer la liste détaillée des personas (lignes 46-55) — déléguer au custom agent

3. **Adapter `data-engineer.md`** :
   - Retirer expertise pointue (Z-ordering, Iceberg vs Delta, Spark internals, formats spécifiques)
   - Garder modélisation, ETL/ELT haut niveau, idempotence, PII, qualité de données
   - Cible : passer de 103 lignes à ~50-60 lignes

4. **Aligner `data-pipeline.md`** avec le persona Data Engineer allégé (workflow plus accessible)

### 🟢 PRIORITÉ BASSE — Cohérence détail

1. **Workflows — corrections ciblées** :
   - `incident-response.md` : clarifier critère de choix persona phase 4 (RCA)
   - `code-analysis.md` : corriger sauts de ligne ligne 37 (anti-patterns collés)

### 🆕 CRÉATIONS (Phase 5.3, après les correctifs)

1. **Créer `agents/templates/runbook.md`** (dette avouée dans `orchestrator.agent.md`)
2. **Créer `agents/templates/architecture.md`** (dette avouée dans `orchestrator.agent.md`)

## Implémentation

Voir le prompt de correctifs : `prompt-correctifs-5.3.md` (à utiliser dans Copilot Chat avec Claude Sonnet 4.6, Agent par défaut).

Ordre d'exécution recommandé :
1. Priorité HAUTE (actions 1-3) — validation utilisateur après chaque
2. Priorité MOYENNE (actions 4-7) — validation utilisateur après chaque
3. Priorité BASSE (action 8)
4. Créations (actions 9-10)
5. Test d'intégration sur un cas réel (Phase 5.4)

## Références

- `VISION.md` — boussole stratégique (Phase 4.5)
- `ROADMAP.md` — feuille de route du projet
- `IDEAS.md` — parking lot enrichi de 8 entrées suite à cet audit
- `test-notes.md` — observations qui ont motivé l'audit
