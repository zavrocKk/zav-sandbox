---
type: memory-checkpoint
thread: <slug-du-fil>          # identifiant stable du fil de travail (kebab-case)
phase: "<N>"                   # phase ROADMAP concernée, si applicable
branch: <feat/...>             # branche Git active sur ce fil
status: in-progress            # in-progress | blocked | closed
last_session: <YYYY-MM-DD>     # date de la dernière mise à jour
next_action: "<la toute prochaine action, en une ligne>"
---

# Checkpoint de mémoire — <Topic>

> **Rôle :** résumé de **reprise** (pas un transcript). À relire EN PREMIER au
> démarrage d'une nouvelle session sur ce fil, pour repartir sans re-explication.
> Mis à jour (écrasé) à chaque session — l'historique vit dans Git.

## Objectif courant
<la tâche / phase en cours, en 1-2 lignes>

## État (fait / en cours / bloqué)
- ✅ <ce qui est fait>
- 🔄 <ce qui est en cours>
- ⛔ <ce qui est bloqué, et pourquoi>

## Décisions arrêtées
<les choix déjà tranchés — à NE PAS rouvrir. Lien ADR si applicable.>
- <décision 1>
- <décision 2>

## Prochaines étapes
<la todo pour reprendre, dans l'ordre>
1. <étape 1>
2. <étape 2>

## Pointeurs (artefacts pérennes produits)
- `<path>` — <ADR / note d'archi / PR / doc>

## Hypothèses / risques ouverts
- <ce qui reste incertain à valider>
