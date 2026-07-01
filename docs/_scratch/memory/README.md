# `docs/_scratch/memory/` — Checkpoints de mémoire (Phase 7)

> ⚠️ **Sécurité** : ne jamais committer d'inputs réels (données clients, tokens, exports CSV/JSON bruts) dans `docs/_scratch/`. Ces fichiers doivent rester en local et sont couverts par `docs/_scratch/.gitignore`. Seuls les checkpoints de mémoire (ce dossier) sont intentionnellement versionnés.

Zone des **checkpoints de reprise** inter-sessions du framework Agentic Team.

## Règles

- **Un fichier par fil de travail** (`<thread-slug>.md`), pas un par session.
  On **met à jour** (écrase) le même fichier à chaque session sur le sujet —
  l'historique vit dans Git.
- **Versionné** (contrairement aux inputs bruts qui, eux, peuvent être gitignored) :
  la mémoire DOIT survivre et suivre le repo (promesse VISION « mémoire persistante
  via artefacts »).
- **Format** : voir le template [`agents/templates/memory-checkpoint.md`](../../../agents/templates/memory-checkpoint.md)
  (front-matter YAML léger + corps markdown structuré).
- **Promotion** : quand un checkpoint accouche d'une décision structurante, son
  contenu est **promu** en ADR / note d'archi dans `docs/`. Le checkpoint reste un
  brouillon de travail, jamais la source de vérité finale.

## Politique de rétention

- **Cycle de vie nominal** : un checkpoint par fil, mis à jour à chaque session sur
  ce fil. Statut possible : `active` | `paused` | `closed`.
- **Archivage** : un checkpoint `closed` peut être déplacé dans
  `docs/_scratch/memory/archive/` lors d'un nettoyage manuel.
- **Nettoyage suggéré** : en début de trimestre, utilise `/memory-list` pour
  lister les checkpoints `closed` depuis > 30 jours, puis archiver ou supprimer.
- **Règle Git** : les checkpoints sont **toujours versionnés** (ne pas gitignorer).
- **Limite de taille** : ~50 lignes (hors front-matter YAML). À chaque mise à jour,
  élaguer : supprimer les ✅ de la session précédente, les étapes exécutées et les
  risques tranchés. Voir les règles détaillées dans
  [`.github/agents/modules/memory.md`](../../../.github/agents/modules/memory.md).

## Cadre de référence

Voir la note de cadrage
[`docs/architecture/2026-05-30-phase-7-persistent-memory.md`](../../architecture/2026-05-30-phase-7-persistent-memory.md).

Règles de chargement complètes :
[`.github/agents/modules/memory.md`](../../../.github/agents/modules/memory.md).
