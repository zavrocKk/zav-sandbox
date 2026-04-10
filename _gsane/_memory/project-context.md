# Brief Canonique — zav-sandbox / GSANE Framework

## 1. Cap du Projet

- **zav-sandbox** est le runtime opérationnel du framework GSANE : système de gouvernance multi-agents IA livré via GitHub Copilot.
- Cinq agents core constituent la Strike Team : Master (Langis), Dev (Amelia), QA (Quinn), Architect (Winston), Bond.
- Objectif permanent : maintenir un runtime lisible, gouverné et auto-améliorant à travers des Delivery Contracts explicites, des tests automatisés et un flywheel cognitif.
- Le projet évolue par lots incrémentaux — chaque changement est tracé, testé et livré via un DC avant merge.

## 2. Invariants de Fonctionnement

- Exactement 5 agents actifs en Flat Design — ni plus, ni moins. Toute extension passe par Bond et party mode.
- Tout travail actif est porté par `_gsane-output/current-delivery-contract.md` et ses critères d'acceptation explicites.
- Ce brief reste court, stable et non-narratif — pas de session state, pas de statuts de branche, pas de next-steps opérationnels.
- Les manifests YAML dans `_gsane/_config/*.yaml` restent la base structurelle du runtime actif.
- Quality gate obligatoire avant tout merge : `pytest` vert + `qa-linter.py` PASS.
- Git workflow non-négociable : branche → commit → PR — jamais de push direct sur `main`.
- Le solo trip wire s'applique à tout fichier GSANE : écriture sans validation d'équipe = violation.

## 3. Carte des Sources de Vérité (Ordre de Lecture)

**Primaires — lire en premier :**
- `_gsane/config.yaml` → configuration globale du runtime (user_name, langue, options)
- `_gsane/_config/*.yaml` → manifests, matrix de délégation, inventaires et configs d'agents
- `_gsane/_memory/project-context.md` → ce fichier — brief canonique humain, stable et court

**Active — lire pour comprendre l'état courant :**
- `_gsane-output/current-delivery-contract.md` → tâche active, scope, critères d'acceptation et owner

**Dérivée — lecture snapshot, jamais source de décision :**
- Vue MCP `gsane_read_canonical_brief()` → contenu de ce fichier sérialisé
- Vue MCP `gsane_read_active_delivery_contract()` → métadonnées et contenu du contrat actif
- Vue MCP `gsane_read_project_snapshot()` → snapshot repo dérivé (agents, workflows, memory)

**Non-sources de vérité :**
- `_gsane/_memory/sessions/` → fichiers d'audit de continuité technique uniquement
- Sidecars d'agents (`_gsane/_memory/*-sidecar/`) → apprentissage interne, pas état courant
- Archives, notes de release et résumés de session ne définissent pas l'état courant du projet
- Aucun prompt ou résumé de session ne doit devenir une source concurrente du brief ou du contrat actif

## 4. Règles d'Usage Humain

- Mettre à jour ce brief uniquement quand la mission, les invariants ou les frontières de vérité changent réellement.
- Garder ce fichier court et durable : pas de narratif de session, pas de statut de branche, pas de next-steps.
- Ordre de lecture du contexte à chaque session : brief → contrat actif → snapshot MCP.
- Traiter tous les fichiers `_gsane/_memory/sessions/` comme archives d'audit, jamais comme vérité du présent.
- Le MCP expose des vues dérivées du repo — il ne remplace ni le Master, ni les Delivery Contracts, ni la gouvernance.
- En cas de doute sur l'état du runtime, lire les manifests YAML (`_gsane/_config/`) — pas les sessions.

## 5. Politique de Migration & Règles de Mise à Jour

- Les headings de ce brief sont des clés de contrat testées automatiquement par `tests/test_canonical_context.py` et `tests/qa-linter.py`. Les changer implique de mettre à jour les assertions dans ces deux fichiers simultanément.
- Toute refonte structurelle du projet nécessite un ADR dans `docs/architecture/decisions/` avant modification du brief.
- En cas de pivot d'architecture (ex: migration vers un packaging `pyproject.toml` ou module dédié), créer d'abord les artefacts réels, puis mettre à jour ce brief pour y référencer uniquement des fichiers qui existent.
- Ce brief ne doit jamais dépasser 120 lignes ni passer sous 80 — s'il grossit, consolider les sections ; s'il rétrécit, maintenir le niveau de détail minimum sur les 5 sections.
- Toute modification de ce brief passe par un Delivery Contract et suit le git workflow obligatoire (branche → PR → merge).
