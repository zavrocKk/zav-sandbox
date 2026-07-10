---
okf_version: "0.1"
type: index
title: Bundle OKF — fiches d'applications
description: Index des applications connues — une ligne par app. Seul fichier du bundle scanné au PLAN, et seulement si la demande nomme une app ou un alias.
timestamp: 2026-07-09
---

> **Règle de chargement** (module [`memory.md`](../../.github/agents/modules/memory.md)) :
> cet index est le **seul** fichier scanné au PLAN, et **seulement** si la demande
> nomme une application ou un alias. Corps d'une fiche chargé sur match uniquement —
> **max 2 fiches par session**. Pas de match → rien n'est chargé.

| Identifiant | Description | Tags | Aliases |
|---|---|---|---|
| _(aucune fiche encore — voir « Ajouter une fiche »)_ | | | |

## Registre de types (contrat local du bundle)

| `type` | Champs requis | Champs custom |
|---|---|---|
| `application` | `type`, `title`, `description`, `timestamp` | `aliases`, `verified`, `criticality` |

Une fiche à qui il manque un champ requis est **non conforme** — le Scribe complète
avant de committer.

## Ajouter une fiche

1. Copier [`agents/templates/app-card.md`](../../agents/templates/app-card.md) vers `docs/apps/<slug>.md` (le chemin est l'identité OKF).
2. Remplir le front-matter (aliases : noms de services, codes JIRA, surnoms d'équipe — c'est eux qui font marcher le rappel par nom).
3. Ajouter la ligne dans la table ci-dessus **et** une entrée dans [`log.md`](log.md).

> Écriture réservée au **Scribe**, à la SYNTHESIS, après approbation utilisateur
> ([ADR-0017](../decisions/0017-okf-apps-bundle.md)).
