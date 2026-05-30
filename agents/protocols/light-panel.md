---
type: protocol
used_by: [orchestrator]
scope: multi-personas
related: [docs/architecture/2026-05-30-party-mode-panel-vs-debate.md]
---

# Protocole PANEL — Party Mode par défaut (multi-angles, une passe)

> Sémantique figée par
> [`docs/architecture/2026-05-30-party-mode-panel-vs-debate.md`](../../docs/architecture/2026-05-30-party-mode-panel-vs-debate.md).
> Ce protocole en est la mise en œuvre opérationnelle. Ne pas re-discuter la
> définition ici.

## Règle binaire

> **PANEL** : chaque persona convoqué émet **UNE** carte d'angle. **Une seule passe.**
> **Aucun persona ne réagit à un autre.** Puis le Scribe synthétise.

Si les personas doivent se répondre entre eux → ce n'est plus le Panel, c'est le
**Débat** (`/debate`, protocole séparé). Le Panel est **borné par construction** :
aucun garde-fou max rounds nécessaire.

## Quand l'appliquer

- **Panel = mode nominal** du Party Mode, sur demande **multi-angles** (problème
  fermé : incident, analyse, doc, design où plusieurs domaines éclairent la réponse).
- **Sélection des agents par l'orchestrateur** : toutes les sessions n'ont pas
  besoin de toute l'équipe. Question simple / mono-domaine → **un seul persona,
  pas de Panel**. L'orchestrateur convoque uniquement l'équipe pertinente.
- Point d'ancrage naturel : les phases « persona variable » des workflows
  (ex. phase 4 Cause racine d'[`incident-response.md`](../workflows/incident-response.md)).

## Format — Carte d'angle (plafond strict : 3 lignes)

Chaque persona convoqué émet exactement :

```text
─── 🛠️ DevOps — Angle ───
Position : <1 ligne>
Risque clé : <1 ligne>
Reco : <1 ligne>
```

- **Position** : l'angle que défend le persona sur la question.
- **Risque clé** : le risque dominant vu depuis son domaine.
- **Reco** : sa recommandation actionnable, en une ligne.

Plafond **non négociable** : 3 lignes par carte (hors en-tête). Discipline tokens
(sert la Phase 5.8) **et** lisibilité multi-perspectives.

## Format — Synthèse Scribe (fixe)

Une fois toutes les cartes émises, le Scribe **ferme toujours** par :

```text
─── 📝 Scribe — Synthèse panel ───
Convergences : …
Divergences : …
Options dégagées : …
Reco / question ouverte : …
```

La synthèse alimente le **livrable normal du workflow en cours** (post-mortem,
ADR, note d'archi…). Le Panel n'invente **aucun** nouveau type d'artefact.

## Orthogonalité des commandes

Le Panel reste **cumulable** avec les commandes existantes :

| Commande | Effet | Interaction avec le Panel |
| --- | --- | --- |
| `/quick` | Saute CONFIRM | Le Panel s'exécute sans étape de validation intermédiaire |
| `/light` | Allège le FORMAT seulement | En-têtes compacts ; les cartes restent au format 3 lignes |
| `/debate` | Bascule Panel → Débat | Quitte ce protocole pour la boucle N rounds |

`/quick`, `/light` et `/debate` restent **orthogonaux et cumulables**.

## Conséquences d'une violation

- Un persona qui réagit à un autre en mode Panel → violation : soit on coupe la
  réaction, soit on bascule explicitement en `/debate`.
- Une carte d'angle qui dépasse 3 lignes → la retailler.
- Un Panel qui se termine sans synthèse Scribe → l'ajouter avant de clore.
