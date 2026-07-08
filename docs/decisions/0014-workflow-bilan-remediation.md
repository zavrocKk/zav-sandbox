---
type: adr
number: 0014
status: accepted
date: 2026-07-07
deciders: [Zav]
tags: [workflow, phase-9.3, test-terrain]
---

# ADR-0014 — Créer le workflow `bilan-remediation` avant la fin du test terrain (amendement ciblé du gel Phase 9.3)

> Format : Michael Nygard. Une décision = un fichier, immuable une fois `accepted`. Si on change d'avis, on crée un nouvel ADR qui `supersedes` celui-ci.

---

## Statut

**État actuel** : accepted
**Décidé le** : 2026-07-07
**Décideurs** : Zav (après débat contradictoire à 3 agents indépendants : avocat du diable, optimiste, expert ingénierie LLM — régime divergent, briefs neutres)

## Contexte

La décision du 2026-07-01 (Phase 9.3, ROADMAP) gèle les décisions structurantes — roster,
nouveaux workflows, MCP — jusqu'aux données du test terrain (~5-10 sessions,
[protocole](../_scratch/2026-07-01-plan-job-test-protocol.md)).

Or deux faits, vérifiés sur pièces le 2026-07-07 :

1. **Le journal du test est vide** (protocole §4 : zéro session loggée). Il n'existe
   aucune mesure en cours à contaminer — et c'est le dernier moment où ajouter un
   workflow est gratuit pour la mesure : après la première session loggée, tout ajout
   fausserait la comparabilité.
2. **Les 5 workflows existants s'arrêtent à l'écriture du document.** Le métier réel de
   l'utilisateur (analyste incidents/bugs/changes, trajectoire SRE) continue après :
   bilan → approbation → remise au développeur → vérification du fix → clôture.
   Sans workflow couvrant cette boucle, le test terrain mesurerait un proxy du job,
   pas le job — le résultat même que le gel voulait protéger serait biaisé.

## Décision

Nous créons `agents/workflows/bilan-remediation.md` (6 phases, vérification ré-entrante)
**avant** le démarrage effectif du test terrain, comme **correction de représentativité
du test** — pas comme abandon du gel. Quatre garde-fous issus du débat :

1. **Cet ADR est rédigé avant le workflow** (pas d'auto-autorisation après coup).
2. **L'état persistant vit dans le bilan lui-même** (front-matter `status`), document
   committé — pas dans un checkpoint `_scratch`. La vérification relit le bilan cité.
3. **Exclusion du mode playbook pendant la validation terrain** : CONFIRM obligatoire,
   aucun mauvais routage ne peut être silencieux. Levée conditionnée au protocole (§3).
4. **Taille dans la norme des workflows existants** (~60-95 lignes), markdown pur,
   réversible par suppression de 3 fichiers + 3 lignes de câblage.

Le protocole de test intègre le nouveau workflow (critères de routage ajoutés au §3) :
il sera évalué **par** le test, pas à côté.

## Alternatives considérées

### Option B — Phases 1-5 seulement (sans vérification ré-entrante)

- Description : même workflow, arrêté au paquet dev.
- Avantages : périmètre plus petit ; évitait le maillon faible identifié (ré-entrance via checkpoint).
- Inconvénients : boucle métier ouverte — on ne sait jamais si le fix adresse les findings.
- **Pourquoi rejetée** : la réserve technique visait le design initial (état dans un
  checkpoint) ; corrigée par le garde-fou 2 (état dans le bilan), elle ne tient plus.

### Option C — Différer au test terrain (position de l'avocat du diable)

- Description : parquer en IDEAS.md, laisser 2-3 sessions prouver le besoin.
- Avantages : respect littéral du gel ; besoin prouvé par les données.
- Inconvénients : le test mesurerait un framework sans le workflow du métier principal ;
  ajout ultérieur en cours de test = contamination réelle de la mesure.
- **Pourquoi rejetée** : ses deux appuis factuels (mesure en cours à protéger, infra de
  phase 6 inexistante) sont tombés à la vérification (journal vide ; état porté par le bilan).

## Conséquences

### Positives

- Le test terrain mesure la boucle métier complète (bilan → remise → vérification).
- Règle « raisonnement visible » (signal → hypothèse → preuve → conclusion) : chaque
  bilan devient un support d'apprentissage de la méthode RCA — objectif SRE de l'utilisateur.

### Négatives

- Amendement de la lettre d'une décision vieille de 6 jours — coût de crédibilité du
  gel ; assumé et documenté ici, à ne pas répéter sans données.
- 6e entrée au mapping : surface de routage accrue (chevauchement possible avec
  `incident-response` et `code-analysis`), mitigée par la désambiguïsation + l'exclusion playbook.

### Neutres / À surveiller

- Critères §3 du protocole : routage confondu ≥ 2 fois → affiner le mapping ;
  routage correct sur ≥ 3 sessions → lever l'exclusion playbook.

## Implémentation

`agents/workflows/bilan-remediation.md` + `agents/templates/bilan.md` + ligne de mapping
(orchestrateur) + note d'exclusion playbook + 2 critères au protocole §3 + câblage README
et table de localisation.

## Références

- [ROADMAP — Phase 9.3](../../ROADMAP.md)
- [Protocole de test terrain](../_scratch/2026-07-01-plan-job-test-protocol.md)
- ADR-0008 (sous-agents réels), ADR-0009 (seuil Panel)
