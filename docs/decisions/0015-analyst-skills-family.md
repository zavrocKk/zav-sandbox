---
type: adr
number: 0015
status: accepted
date: 2026-07-07
deciders: [Zav]
tags: [skills, templates-de-sortie, atlassian, servicenow, observability, phase-9.3]
---

# ADR-0015 — Famille de skills « analyste » : évidence en entrée, formats outillés en sortie

> Format : Michael Nygard (inventeur du format ADR, « Documenting Architecture
> Decisions », 2011). Une décision = un fichier, immuable une fois `accepted`.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-07
**Décideurs** : Zav

## Contexte

Le métier réel de l'utilisateur est un pipeline : évidence extraite des outils
d'observabilité (Splunk, Datadog, AWS CloudWatch) → analyse (workflows
incident-response / bilan-remediation) → livrables dans les outils d'entreprise
(JIRA, ServiceNow, Confluence). Le framework couvrait le milieu du pipeline,
pas les deux extrémités.

Recherche du 2026-07-07 : les skills publiques existantes pour ces outils sont
toutes **integration-first** (CLI, API, MCP — jira-cli, datadog-labs/agent-skills,
servicenow-agent-skills couvre le SDK). Le **savoir-faire de format et de méthode**
— comment écrire un bon ticket, un bon change, une preuve re-exécutable — n'existe
nulle part en SKILL.md. Par ailleurs, SKILL.md est devenu un standard ouvert
multi-outils (26+ assistants dont Copilot et Claude) : une skill écrite ici est
portable au travail telle quelle.

Le chantier « templates JIRA/SNOW/Confluence » était différé au test terrain
(décision 2026-07-01, Phase 9.3). Cet ADR l'ouvre par anticipation — deuxième
amendement du gel après [ADR-0014](0014-workflow-bilan-remediation.md).

## Décision

Créer une famille de **4 skills standalone** (markdown pur, zéro connexion,
zéro câblage aux workflows) :

- **Entrée (méthode)** : `observability-triage` — une seule skill-méthode
  (golden signals, rétrécissement, preuve re-exécutable = requête + fenêtre UTC +
  extrait anonymisé), avec **une annexe `reference/` par outil** (splunk,
  datadog, aws-cloudwatch). Ajouter un outil = ajouter une annexe, pas une skill.
- **Sortie (format)** : `jira-issue`, `snow-change`, `confluence-doc` — une skill
  par format de livrable, chacune avec sa **règle de conformité binaire**
  (champs obligatoires présents sinon non conforme) et une section « Adaptation
  à ton instance » en placeholders, à remplir avec des fixtures réelles
  anonymisées (`docs/_scratch/mvp-inputs/`).

Restent explicitement **hors périmètre** : toute connexion (API/MCP — évaluée
plus tard, au travail, par ADR dédié), tout câblage des skills dans les workflows
(décision séparée, après usage réel), et l'adaptation aux instances d'entreprise
(après fixtures).

## Alternatives considérées

### Option B — Une skill par outil (6 skills : splunk, datadog, aws, jira, snow, confluence)

- Description : symétrie totale, chaque outil sa skill.
- Avantages : granularité maximale.
- Inconvénients : la sélection de skill se fait par matching de `description` —
  3 skills d'observabilité aux descriptions quasi identiques dégradent la
  sélection ; 3 copies de la même méthode = drift assuré (leçon TOK-01).
- **Pourquoi rejetée** : le savoir-faire d'évidence est unique, seule la syntaxe
  varie — c'est la définition d'une annexe, pas d'une skill.

### Option C — Attendre le signal du protocole §3 (« besoin ressenti à chaque session »)

- Description : respecter la lettre du gel, construire après données.
- Avantages : besoin prouvé.
- Inconvénients : les skills sont additives et non câblées — elles ne changent ni
  routage ni comportement mesuré par le test ; l'utilisateur a exprimé le besoin
  métier directement (3 demandes successives le 2026-07-07).
- **Pourquoi rejetée** : contrairement à un workflow, une skill n'altère pas
  l'objet du test terrain ; le coût d'attendre est réel (bilans sans format
  d'entreprise), le bénéfice d'attendre est nul.

## Conséquences

### Positives

- Le pipeline métier complet est couvert ; les livrables sortent prêts à coller.
- Règles binaires par skill → candidates à des gates scriptés si drift observé
  (pattern « verify, don't trust » — cf. entrée IDEAS « migration règles
  binaires → hooks »).
- Portabilité : SKILL.md standard ouvert, réutilisable au travail avec MCP en tuyau.

### Négatives

- Deuxième amendement du gel en une soirée — la crédibilité du gel s'use ;
  le prochain chantier différé (roster, MCP) ne doit **pas** être ouvert sans données.
- 4 skills non testées sur des scénarios réels (critère qualité du registre) —
  la validation terrain est due.

### Neutres / À surveiller

- Sections « Adaptation à ton instance » vides tant que les fixtures anonymisées
  ne sont pas déposées — les skills restent utilisables en générique.
- Si la sélection de skill se trompe entre les 4 (description matching), affiner
  les descriptions — signal à noter au journal du test terrain.

## Implémentation

`agents/skills/{jira-issue,snow-change,confluence-doc,observability-triage}/SKILL.md`,
3 annexes `observability-triage/reference/*.md`, registres (`agents/skills/README.md`,
`.github/agents/modules/skills.md`), arborescence README, protocole §3 mis à jour.

## Références

- [ADR-0014](0014-workflow-bilan-remediation.md) — précédent d'amendement du gel.
- [Protocole de test terrain](../_scratch/2026-07-01-plan-job-test-protocol.md) — §3.
- Standard Agent Skills : agentskills.io (SKILL.md multi-assistants).
