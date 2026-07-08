---
name: confluence-doc
version: "1.0.0"
description: Structure une page Confluence selon son intention — how-to, troubleshooting, runbook ou référence — avec titre orienté recherche, règle « une page = une intention » et en-tête de fraîcheur « Vérifié le / par ». À utiliser pour rédiger ou restructurer de la documentation destinée à Confluence. Sortie markdown collable dans l'éditeur Cloud — aucune connexion API.
---

# Confluence Doc — une page, une intention

Produit une page que **quelqu'un d'autre trouve et utilise sans son auteur**.
Skill de **format** : la sortie est du markdown propre — l'éditeur Confluence
Cloud le colle nativement (pas de wiki markup legacy).

## Règle n°1 — une page = une intention

Avant d'écrire, déclarer le **type** de page. Chaque type a sa structure — les
mélanger produit la « page fourre-tout » que personne ne retrouve :

| Type | Répond à | Structure |
|---|---|---|
| **How-to** | « Comment faire X ? » | Pré-requis → étapes numérotées → résultat attendu → erreurs fréquentes |
| **Troubleshooting** | « Pourquoi X est cassé ? » | Symptôme → vérifications ordonnées → résolutions → quand escalader |
| **Runbook** | « Comment opérer X ? » | Vue d'ensemble → procédures (start/stop/relance) → monitoring → contacts. Version repo : table de localisation (`docs/runbooks/`) — cette skill le met en forme pour Confluence |
| **Référence** | « C'est quoi X ? » | Définition → schéma → détails par section → pages liées |

## En-tête obligatoire (fraîcheur)

Toute page commence par :

```text
> Vérifié le : <YYYY-MM-DD> — par : <nom/rôle>
> S'applique à : <version/environnement>
```

Une doc dont on ne sait pas si elle est encore vraie est **pire** qu'une absence
de doc : elle fait perdre du temps avec autorité.

## Règles (binaires)

- **Type déclaré** avant rédaction (un des 4 ci-dessus), sinon non conforme.
- **Titre orienté recherche** : la question ou la tâche que le lecteur taperait
  (« Relancer le pipeline X après échec » — pas « Notes pipeline »).
- **En-tête de fraîcheur présent** (Vérifié le / par / s'applique à).
- **Toute capture d'écran est accompagnée de texte** : les images ne sont ni
  cherchables ni lisibles par un lecteur d'écran, et périment plus vite que le texte.
- **Section « Pages liées »** en pied de page (≥ 1 lien ou mention explicite
  « page orpheline volontaire »).

## Adaptation à ton espace

Conventions d'espace (arborescence, labels, gabarits maison) à compléter avec
1-2 pages réelles **anonymisées** dans `docs/_scratch/mvp-inputs/` :

```text
<!-- À remplir après fixtures :
Espace cible et arborescence : <…>
Labels obligatoires          : <…>
Gabarits maison existants    : <…>
-->
```

## Anti-patterns

- ❌ Page fourre-tout (how-to + référence + historique de décisions mélangés).
- ❌ Titre générique (« Notes », « Doc API ») introuvable en recherche.
- ❌ Page sans date de vérification ni owner.
- ❌ Capture d'écran seule pour documenter une procédure.
- ❌ Dupliquer une doc du repo au lieu de la pointer (source unique — même règle
  que la table de localisation du workspace).
