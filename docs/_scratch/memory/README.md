# `docs/_scratch/memory/` — Checkpoints de mémoire (Phase 7)

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

## Cadre de référence

Voir la note de cadrage
[`docs/architecture/2026-05-30-phase-7-persistent-memory.md`](../../architecture/2026-05-30-phase-7-persistent-memory.md).
