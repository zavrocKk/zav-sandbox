---
type: memory-checkpoint
thread: phase-7-persistent-memory
phase: "7"
branch: feat/phase-7-memory-framing
status: in-progress
last_session: 2026-05-30
next_action: "Trancher la politique de rétention/cleanup des checkpoints (sous-phase 7.x)"
---

# Checkpoint de mémoire — Phase 7 : Mémoire persistante

> **Rôle :** résumé de **reprise** (pas un transcript). À relire EN PREMIER au
> démarrage d'une nouvelle session sur ce fil, pour repartir sans re-explication.
> Mis à jour (écrasé) à chaque session — l'historique vit dans Git.

## Objectif courant
Implémenter la Phase 7 (mémoire persistante inter-sessions) du framework Agentic
Team : artefacts markdown qui survivent entre sessions pour « reprendre où on
s'était arrêté ». Cadrage fait, mécanisme 7.1 livré.

## État (fait / en cours / bloqué)
- ✅ Note de cadrage d'architecture rédigée et committée
- ✅ Mécanisme 7.1 livré : template checkpoint + zone versionnée + câblage orchestrateur (`/checkpoint`, lecture-au-démarrage, auto-check saturation)
- ✅ ROADMAP Phase 7 mise à jour (🟦 cadrage + 7.1) ; table de localisation mise à jour
- ✅ PR #108 ouverte (pas encore mergée — attente validation utilisateur)
- 🔄 Règle de scoping de la mémoire (ne charger QUE le fil pertinent) en cours de durcissement
- ⛔ Rien de bloqué

## Décisions arrêtées
- **Quoi** : résumé de reprise en 6 rubriques, pas un transcript ; distinction pérenne / session / éphémère
- **Où** : `docs/_scratch/memory/<slug>.md`, 1 fichier par fil, versionné, promu vers `docs/` si structurant
- **Format** : markdown structuré + front-matter YAML léger (réutilise la convention du repo)
- **Comment** : écrire (manuel `/checkpoint` + proposition auto Scribe à saturation/fin) ↔ relire en premier au démarrage
- **Articulation** : checkpoint = handoff-packet inter-sessions ; lu à budget variable tiny→deep ; task-envelope reconstruite à la reprise
- **Inspiration externe** (MemPalace, In-Memoria, Mem0, Letta, LocalRecall) : conceptuelle seulement — infra lourde écartée (filtres VISION 2/3/4)
- **Pas de hooks** : la persistance = convention de fichier + instruction orchestrateur + Git ; pas de démon d'auto-save

## Prochaines étapes
1. Trancher la politique de rétention / cleanup des checkpoints clos (auto-archivage ? proposition Scribe ? statut `closed` → archive)
2. Valider à l'usage la granularité « 1 fichier par fil »
3. (Optionnel) restructuration `inputs/`/`outputs/` (IDEAS 2026-05-03)
4. Décider du merge de la PR #108

## Pointeurs (artefacts pérennes produits)
- `docs/architecture/2026-05-30-phase-7-persistent-memory.md` — note de cadrage
- `agents/templates/memory-checkpoint.md` — template de checkpoint
- `docs/_scratch/memory/README.md` — règles de la zone mémoire
- `.github/agents/orchestrator.agent.md` — section « Mémoire persistante »
- PR #108 — https://github.com/zavrocKk/zav-sandbox/pull/108

## Hypothèses / risques ouverts
- Risque : charger un checkpoint non pertinent au démarrage → mitigé par la règle de scoping par `thread` (ne lire que le fil explicitement repris)
- Granularité « 1 fichier par fil » suppose un découpage clair des fils — à valider à l'usage
- Politique de rétention non tranchée → risque d'accumulation de checkpoints clos
