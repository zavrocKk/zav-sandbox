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
par fil de travail).

## Lecture (reprise) — au démarrage d'une session

- Si l'utilisateur reprend un fil identifiable (phase, sujet, branche), tu DOIS
  **vérifier l'existence d'un checkpoint** dans `docs/_scratch/memory/` et, le cas
  échéant, **le relire EN PREMIER** avant l'ANALYSE du PRE-FLIGHT.
- Budget variable : tâche `tiny` → relire seulement `next_action` du front-matter ;
  tâche `deep` → relire tout le corps + suivre les pointeurs vers les ADR.

## Scoping mémoire — règle binaire

- Tu ne charges **QU'UN SEUL** checkpoint : celui dont le `thread` (front-matter)
  correspond au fil que l'utilisateur reprend explicitement. **Jamais** « tous les
  checkpoints » chargés en contexte.
- **Lister ≠ charger** : le scan des seuls front-matter (`thread`, `status`,
  `next_action`) au premier message — règle « Restauration de session » du
  [preflight](../../../agents/protocols/preflight.md#règle--restauration-de-session-premier-message) —
  est autorisé et n'est **pas** un chargement. L'interdit porte sur le chargement
  du **corps** d'un checkpoint sans correspondance de fil.
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

## Limite de taille et élagage

- **Maximum : 50 lignes** (hors front-matter YAML). Au-delà, le Scribe DOIT élaguer
  avant de sauvegarder.
- **Règle d'élagage** : à chaque mise à jour, supprimer :
  - Les items `✅` dans `## État` qui datent de la session précédente ou plus
    (ils sont faits — inutile de les garder en mémoire forward)
  - Les entrées `## Hypothèses / risques ouverts` qui ont été tranchées
  - Les `## Prochaines étapes` déjà exécutées
- **Ce qu'on garde toujours** : `next_action` (front-matter), `## Décisions arrêtées`,
  `## Pointeurs`, et l'état courant (`🔄` + `⛔`).
- **Principe** : le checkpoint est un **résumé de reprise forward**, pas un journal.
  Toute ligne qui regarde en arrière plutôt qu'en avant est candidate à la suppression.

**Distinction à respecter** : le checkpoint est un **résumé de reprise** (forward),
à ne pas confondre avec le **bilan de session** ([`session-summary.md`](../../../agents/templates/session-summary.md),
rétrospectif).
