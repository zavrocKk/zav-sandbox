---
name: delivery-contract
description: "Template officiel et règles du Delivery Contract — le contrat formel entre Master et agent exécutant."
---

# Delivery Contract — Référence

## Template officiel

```
DC-{YYYYMMDD}-{NNN} | {AGENT} | {DATE}

TÂCHE : {quoi faire — verbe d'action}

CONTEXTE : {pourquoi — 1-2 phrases max}

FICHIERS CIBLES :
- chemin/exact/fichier.ext

CONTRAINTES :
- {règles non-négociables}

CRITÈRES D'ACCEPTANCE :
- AC-1 : {testable, mesurable}
- AC-2 : ...

AGENT PRINCIPAL : {agent}
VALIDATION : {agent}
```

## Numérotation

Format : `DC-YYYYMMDD-NNN` (date ISO + séquence 3 chiffres).
Exemples : `DC-20260410-001`, `DC-20260410-002`.
Chaque DC est unique par jour. Le compteur NNN repart à 001 chaque jour.

## DC complet vs incomplet

Un DC est **complet** quand tous les champs du template sont renseignés :
- TÂCHE avec verbe d'action
- Au moins 1 fichier cible
- Au moins 1 contrainte
- Au moins 1 AC testable (commande ou assert)
- Agent principal et validateur nommés

Un DC est **incomplet** si un champ est vide, si les AC ne sont pas mesurables, ou si aucun fichier cible n'est listé. Un DC incomplet est rejeté — l'agent refuse l'exécution.

## Fix trivial — exception DC

Un DC n'est **PAS requis** pour un fix trivial :
- Modification < 5 lignes
- Aucun changement de signature de fonction
- Aucun nouveau fichier créé
- Exemples : typo, mise à jour commentaire, bump version dans `version.txt`

Au-delà de ces critères → DC obligatoire, sans exception.

## Cohérence avec le workflow

1. Langis (Master) rédige le DC
2. L'agent assigné exécute selon les AC
3. Quinn (QA) valide chaque AC par PASS/FAIL
4. [CC] vérifie la complétion globale
5. Résultat archivé dans `_gsane-output/`
