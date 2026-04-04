# Decision Log — GSANE

> Journal des décisions architecturales et de gouvernance du projet zav-sandbox.
> Chaque entrée documente une décision importante, son contexte et sa justification.

---

## Format d'entrée

```
## DL-XXX — {titre court}
- **Date**: YYYY-MM-DD
- **Décision**: Ce qui a été décidé
- **Contexte**: Pourquoi cette décision était nécessaire
- **Alternatives écartées**: Ce qui a été considéré mais rejeté
- **Impact**: Fichiers/règles affectés
```

---

## DL-001 — gh CLI banni du projet

- **Date**: 2026-03-01
- **Décision**: L'outil `gh` (GitHub CLI) est banni de tous les fichiers GSANE (workflows, scripts, agents, prompts)
- **Contexte**: `gh` a été introduit dans plusieurs fichiers sans validation de disponibilité dans l'environnement, causant des erreurs silencieuses. L'environnement cible (VS Code + Copilot Chat) ne garantit pas la présence de `gh`
- **Alternatives écartées**: Conditionner l'usage (`if command -v gh`) — rejeté car ajoutait de la complexité sans valeur ajoutée
- **Impact**: `git-workflow/workflow.md`, `flywheel/workflow-apply.md`, `README.md`, `copilot-instructions.md`, `validate-pr.yml`, `gsane-framework/SKILL.md`, `hooks/hooks.json`

---

## DL-002 — Délégation stricte obligatoire

- **Date**: 2026-03-01
- **Décision**: `enforcement_mode: strict` dans `core/config.yaml` — tous les appels d'agents DOIVENT passer par la delegation matrix, aucune auto-exécution directe
- **Contexte**: Plusieurs instances de solo execution détectées (FM-001). Le système de délégation existait mais n'était pas enforced
- **Alternatives écartées**: Mode `permissive` (warn only) — rejeté car n'élimine pas les violations, crée juste du bruit
- **Impact**: `core/config.yaml`, `copilot-instructions.md`, `AGENTS.md` — PRE-EXECUTION GATE ajouté

---

## DL-003 — 1 branche = 1 unité logique

- **Date**: 2026-03-01
- **Décision**: Une branche ne peut contenir qu'une seule unité logique de changement. Exception unique : corriger un oubli sur une PR non encore mergée
- **Contexte**: Des commits multi-sujets (FM-003) rendaient les PRs difficiles à reviewer, à comprendre dans le CHANGELOG, et impossibles à reverter proprement
- **Alternatives écartées**: Branches longues "feature/sprint-X" — rejeté car crée des PRs géantes et des merge conflicts fréquents
- **Impact**: `git-workflow/workflow.md`, `CONTRIBUTING.md §3`

---

## DL-004 — GSANE = protocole de gouvernance, pas des outils CLI

- **Date**: 2026-03-01
- **Décision**: GSANE est défini comme un protocole de gouvernance pour AI-Native Execution — aucune dépendance à des CLIs tiers (gh, jq, etc.) dans les workflows agents
- **Contexte**: La migration vers GSANE incluait des patterns hérités qui dépendaient d'outils externes. GSANE doit fonctionner dans tout environnement LLM sans prérequis CLI
- **Alternatives écartées**: Wrapper scripts — rejeté car déplace le problème sans le résoudre
- **Impact**: Architecture complète — tous les workflows utilisent maintenant des URLs et des templates manuels

---

## DL-005 — _gsane-output/ tracké via exceptions .gitignore

- **Date**: 2026-03-01
- **Décision**: `_gsane-output/` reste ignoré dans `.gitignore` sauf les `.gitkeep` qui maintiennent la structure de répertoires dans git
- **Contexte**: Le dossier `_gsane-output/` disparaissait à chaque clone — la structure `creations/` et `test-artifacts/` devait être présente dès le clone
- **Alternatives écartées**: Tracker tout `_gsane-output/` — rejeté car les artefacts générés ne doivent pas polluer l'historique git par défaut
- **Impact**: `.gitignore` — ajout des exceptions `!_gsane-output/creations/.gitkeep` et `!_gsane-output/test-artifacts/.gitkeep`


## DL-006 — Éradication du Squeuomorphisme (BMM -> CIS) et standardisation YAML

- **Date**: 2026-03-30
- **Décision**: Suppression complète du sous-module fantôme _gsane/bmm/ (et son avatar temporaire mad), migration finale vers une architecture de manifestes strictement hiérarchiques en YAML au lieu du CSV.
- **Contexte**: Le système tentait de déléguer à des paths morts ou bloquait sur des hooks Git rigides cherchant des magic strings. Le projet abandonne le format de données tabulaire (CSV) limitant pour un YAML qui supporte des structures de listes et d'attributs riches (Semantic ready).
- **Impact**: La Matrice de Délégation, les hooks de pre-commit bash/ps1 (+ Blacklist Linter), copilot-instructions, configs, et les scripts CI.

## DL-007 — Architecture V3 / Roadmap (Mémoire, Tests, Sémantique)

- **Date**: 2026-03-30
- **Décision**: Enregistrement des 3 axes de développement post-V2 identifiés pour la résilience à long terme de GSANE.
- **Contexte**: La V2 est validée pour la production immédiate, mais de potentielles dettes techniques lointaines ont été soulevées en phase de stabilisation :
  1. **Lossless Context Compression (Critique)** : Prévenir le Prompt Bloat. Un agent devra résumer dynamiquement (ou filtrer) les anciens learned-lessons.md ou états de sidecar via MCP au lieu de faire un grep brut.
  2. **Adversarial Unit Tests (	ests/agents/)** : Mettre en place un juge-LLM pour tester dynamiquement le respect du MAX_TTL et du TRIPARTITE_CONSENSUS par les agents.
  3. **Semantic Routing** : Remplacer les expressions régulières de delegation-matrix.yaml par un résolveur d'intentions lisant et pondérant les meta-descriptions des agents.
- **Impact**: Priorisation de la *Context Compression* pour le prochain cycle de développement V3.

## DL-008 — Transition vers la Strike Team (Absorption Analyste/PM par le Master)
- **Date**: 2026-04-04
- **Décision**: Purge des agents superflus (Analyste, PM, Scrum Master, spécialistes) pour ne conserver qu'une "Strike Team" d'élite de 5 agents (Master, Dev, QA, Architect, Agent Builder). L'Orchestrateur (Master) absorbe les responsabilités d'analyse technique et de Delivery Contract.
- **Contexte**: Aligner l'architecture sur le modèle Grimoire-kit (ultra-lean) pour éliminer le téléphone arabe et la latence liés aux intermédiaires (comme l'Analyste). Le LLM du Master est déjà compétent pour analyser avant de déléguer, réduisant la consommation de tokens.
- **Alternatives écartées**: Maintenir une équipe complète virtuellement complète — rejeté, génère trop de bruit et ralentit l'enchaînement.
- **Impact**: Suppression massive de fichiers dans .github/agents/, agent-manifest.yaml, mise à jour des permissions tools.


