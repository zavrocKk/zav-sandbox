---
type: module
referenced_by: .github/agents/orchestrator.agent.md
---

# Module — Mémoire persistante (checkpoints inter-sessions)

> Ce fichier est référencé par `orchestrator.agent.md`. Toute modification des règles
> de scoping ou de déclenchement doit être répercutée dans les commandes spéciales
> de l'orchestrator.

---

Le framework garde le fil **entre sessions** via des **checkpoints markdown**
versionnés dans [`docs/_scratch/memory/`](../../../docs/_scratch/memory/) (un fichier
par fil de travail). Cadre complet :
[`docs/architecture/2026-05-30-phase-7-persistent-memory.md`](../../../docs/architecture/2026-05-30-phase-7-persistent-memory.md).

## Lecture (reprise) — au démarrage d'une session

- Si l'utilisateur reprend un fil identifiable (phase, sujet, branche), tu DOIS
  **vérifier l'existence d'un checkpoint** dans `docs/_scratch/memory/` et, le cas
  échéant, **le relire EN PREMIER** avant l'ANALYSE du PRE-FLIGHT.
- Budget variable : tâche `tiny` → relire seulement `next_action` du front-matter ;
  tâche `deep` → relire tout le corps + suivre les pointeurs vers les ADR.

## Scoping mémoire — règle binaire

- Tu ne charges **QU'UN SEUL** checkpoint : celui dont le `thread` (front-matter)
  correspond au fil que l'utilisateur reprend explicitement. **Jamais** « tous les
  checkpoints » ni un balayage de `docs/_scratch/memory/`.
- **Critère de correspondance** : le `thread`, la `branch` active, ou le sujet
  annoncé par l'utilisateur. Si aucun ne correspond → **tu ne charges rien** et tu
  démarres une session neuve (pas de mémoire injectée).
- En cas de **doute** sur le fil à reprendre → **demander** lequel reprendre.
- Un checkpoint au statut `closed` n'est **pas** rechargé automatiquement.
- **Vérification binaire** : injecter du contexte mémoire non demandé pour le fil
  courant = bug.

## Écriture (checkpoint) — déclenchement hybride

- **Manuel** : commande `/checkpoint` → le Scribe écrit/met à jour le checkpoint du
  fil courant à partir du template [`agents/templates/memory-checkpoint.md`](../../../agents/templates/memory-checkpoint.md).
- **Proposition automatique** : à l'auto-check saturation **ou** en fin de session,
  le Scribe **propose** d'écrire un checkpoint (sans l'imposer — zéro charge
  cognitive imposée).

## Politique de rétention

- **Un fichier par fil** : on met à jour (écrase) le même fichier à chaque session
  sur ce fil — l'historique vit dans Git.
- **Archivage** : un checkpoint `closed` peut être déplacé dans
  `docs/_scratch/memory/archive/` lors d'un nettoyage manuel.
- **Nettoyage suggéré** : en début de trimestre, passer en revue via `/memory-list`
  les checkpoints `closed` depuis > 30 jours → archiver ou supprimer.
- **Règle Git** : les checkpoints sont **toujours versionnés** (ne pas gitignorer).

**Distinction à respecter** : le checkpoint est un **résumé de reprise** (forward),
à ne pas confondre avec le **bilan de session** ([`session-summary.md`](../../../agents/templates/session-summary.md),
rétrospectif).
