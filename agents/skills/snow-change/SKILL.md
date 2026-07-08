---
name: snow-change
version: "1.0.0"
description: Rédige un change request ServiceNow prêt à coller au format ITIL (justification, implementation plan, risk & impact analysis, test plan, backout plan, fenêtre, CIs affectés). À utiliser pour préparer un change normal, standard ou emergency. Ne crée rien dans ServiceNow — sortie markdown copiable uniquement.
---

# ServiceNow Change — change request prêt à coller

Produit un change request **approuvable du premier coup** : le CAB (ou
l'approbateur) ne devrait avoir aucune question sans réponse. Skill de
**format** : aucune connexion, aucun appel API.

## Types de change (rappel)

| Type | Quand | Approbation |
|---|---|---|
| **Standard** | Pré-approuvé, répétable, risque connu (ex. patch routinier) | Automatique |
| **Normal** | Changement planifié non répétable | CAB / approbateur |
| **Emergency** | Correctif urgent (incident en cours) | Voie accélérée, justification renforcée |

## Format de sortie

```text
Short description : <Quoi — sur quel système — dans quel but>   [une ligne]
Type              : <standard | normal | emergency>

Justification :
<pourquoi ce change, maintenant — lien incident/bilan/ticket si applicable>

Configuration Items affectés :
- <CI / service / application>

Risk & impact analysis :
- Impact   : <qui/quoi est touché si ça se passe bien ET si ça se passe mal>
- Risque   : <probabilité × gravité, en une ligne justifiée>
- Priorité proposée : impact × urgence — décision finale humaine

Implementation plan :
1. <étape numérotée, exécutable par quelqu'un d'autre que l'auteur>
2. <…>

Test plan :
- [ ] <vérification binaire post-implémentation — quoi observer, valeur attendue>

Backout plan :
1. <comment revenir à l'état antérieur, étape par étape>
2. <critère de déclenchement du backout : quel signal → on annule>

Schedule : <fenêtre début-fin, fuseau> — <durée estimée + durée du backout>
```

## Règles (binaires)

- **Pas de backout plan = change non conforme.** Même règle que le plan de
  rollback obligatoire du workflow [`data-pipeline`](../../workflows/data-pipeline.md)
  et de la checklist [`pre-deploy`](../../checklists/pre-deploy.md) — cette skill
  formate une discipline que le framework impose déjà.
- **Test plan présent** avec au moins un critère binaire observable.
- **Implementation plan exécutable par un tiers** : si une étape suppose un savoir
  implicite de l'auteur, elle est incomplète.
- **La priorité finale est humaine** : la skill propose impact × urgence (ITIL),
  l'analyste tranche.
- **La fenêtre inclut la durée du backout** : une fenêtre qui ne couvre que le
  chemin heureux est trop courte par construction.

## Adaptation à ton instance

Les formulaires SNOW varient par organisation (champs obligatoires, assignment
groups, modèles de standard changes). À compléter avec 1-2 changes réels
**anonymisés** dans `docs/_scratch/mvp-inputs/` :

```text
<!-- À remplir après fixtures :
Champs obligatoires de l'instance : <…>
Assignment group par défaut       : <…>
Modèles de standard change dispo  : <…>
-->
```

## Anti-patterns

- ❌ Risk analysis générique copiée-collée (« risque faible ») sans justification.
- ❌ Backout plan = « restaurer le backup » sans étapes ni critère de déclenchement.
- ❌ Emergency change utilisé pour contourner la planification d'un change normal.
- ❌ Fenêtre sans fuseau horaire, ou sans marge pour le backout.
- ❌ Test plan = « vérifier que ça marche ».
