# CHANGELOG

Format basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.1.1](https://github.com/zavrocKk/zav-sandbox/compare/v2.1.0...v2.1.1) (2026-04-11)


### Bug Fixes

* **governance:** RIGOR Sprint 0-2 — 15 findings closed (3C, 3H, 6M, 3L) ([#64](https://github.com/zavrocKk/zav-sandbox/issues/64)) ([93a32e7](https://github.com/zavrocKk/zav-sandbox/commit/93a32e748f14c295ad2d6db3807728f4c4647e4a))

## [2.1.0](https://github.com/zavrocKk/zav-sandbox/compare/v2.0.0...v2.1.0) (2026-04-11)


### Features

* batch P6 — context budget, DC validator, agent versioning, flyw… ([f5013e7](https://github.com/zavrocKk/zav-sandbox/commit/f5013e7e05a92c27767bb274b844ca71b1aa1a95))
* batch P6 — context budget, DC validator, agent versioning, flywheel rollback ([3c68b30](https://github.com/zavrocKk/zav-sandbox/commit/3c68b301c563ac6fc61b16e59114ebaaa24dbc3b))
* batch P6b — token budget tests, subagents Vera/Sage, session resumption ([3c297bc](https://github.com/zavrocKk/zav-sandbox/commit/3c297bc5f7dbd4a6cedb93bc9e6363cd48b7aa05))
* Batch P6b — Token Budget, Subagents Vera/Sage, Session Resumption ([dd8d116](https://github.com/zavrocKk/zav-sandbox/commit/dd8d116fef0b6a4c12f6d2a2d6a5dd93d027d61e))
* **hooks:** activate Sage warning in session-start.sh ([052f8f6](https://github.com/zavrocKk/zav-sandbox/commit/052f8f62a0aecb7e417acc84e1c5b5660199e67b))


### Bug Fixes

* **agents:** add missing customize.yaml for vera and sage ([c7bd2c8](https://github.com/zavrocKk/zav-sandbox/commit/c7bd2c8818d2accafa1ad9649be5d3e4c6def779))
* **ci:** replace body length guard with template content comparison i… ([7553f6a](https://github.com/zavrocKk/zav-sandbox/commit/7553f6a5ba3bf2f2b3a5c4f630224d89f2c60bf8))
* **ci:** replace body length guard with template content comparison in pr-autofill ([c09fb53](https://github.com/zavrocKk/zav-sandbox/commit/c09fb534bbdcfcda9525abbe1cd756b3d570d81b))
* **ci:** resolve remaining ruff violations ([db79adb](https://github.com/zavrocKk/zav-sandbox/commit/db79adb0de96e3567a5f37e0773f3663b88f41b3))
* **cli:** absorb grep -v exit code in doc gate — set -e killed script when only _gsane/_memory/ was dirty ([261231e](https://github.com/zavrocKk/zav-sandbox/commit/261231e37d098b79f63db44b088f5b8c890af16c))
* close backlog-002 and backlog-003 ([e8484a0](https://github.com/zavrocKk/zav-sandbox/commit/e8484a0626ba572373ca5d58a546d4a33ea8f401))
* close backlog-002 and backlog-003 ([cdbcbd4](https://github.com/zavrocKk/zav-sandbox/commit/cdbcbd4756b558a94ccc40058aeed1bf6e83c24e))
* **gsane:** finalize P6-H agent structure, customize schema and docs ([de0f2aa](https://github.com/zavrocKk/zav-sandbox/commit/de0f2aada387d5398db681c0c3cd5f151bd6cc3a))
* **hooks:** normalize session-start.sh for bash runtime ([c34e8b0](https://github.com/zavrocKk/zav-sandbox/commit/c34e8b04b1855021225f891e948d3d6ffcebfe38))
* **lint:** collapse SIM102 branch in qa-linter ([58c049a](https://github.com/zavrocKk/zav-sandbox/commit/58c049a4fa1a1d97ab10aae1b0c69aee8c76bfaa))
* **release:** align release-please workflow for squash merge ([#60](https://github.com/zavrocKk/zav-sandbox/issues/60)) ([3ac9108](https://github.com/zavrocKk/zav-sandbox/commit/3ac9108999fb1973bc66d9bc66c55f554e36431b))
* **release:** enable squash merge strategy for release-please detection ([#61](https://github.com/zavrocKk/zav-sandbox/issues/61)) ([9aefd80](https://github.com/zavrocKk/zav-sandbox/commit/9aefd80dddad88d2017013c29543a6fbc841945d))

## [Unreleased]

### Fixed
- **fix(governance)**: C-01 — `SECURITY.md` réécrit en UTF-8 propre avec LF, accents restaurés (mojibake corrigé)
- **fix(governance)**: C-02 — versions agents alignées à 2.1.1 dans `AGENTS.md`, `release-please.yml` sync désormais `pyproject.toml`
- **fix(governance)**: C-03 — `config.yaml` unicode échappé remplacé par caractères natifs (—, ç)
- **fix(docs)**: H-08/H-09 — `TROUBLESHOOTING.md` seuil coverage corrigé (70% → 50%), référence v2.3+ supprimée
- **fix(ci)**: M-06 — GitHub Actions alignées (`checkout@v6`, `github-script@v9` partout)
- **fix(config)**: M-01 — `pytest.ini` supprimé, config consolidée dans `pyproject.toml` avec `pythonpath` et marker `token_budget`

### Removed
- **chore(cleanup)**: H-06 — `cleansing.py` (racine + `src/`) supprimés — dead migration code sans référence
- **chore(cleanup)**: L-07 — entrée legacy `_bmb/` retirée de `.gitignore`

### Added
- **feat(build)**: M-05 — `.editorconfig` ajouté (UTF-8, LF, indent standards)
- **feat(typing)**: M-13 — `py.typed` marker ajouté dans `src/`
- **feat(arch)**: M-10 — `src/__init__.py` avec `__all__` exports
- **feat(quality)**: M-11 — scope mypy étendu à `src/`, `_gsane/tools/`
- **chore(docs)**: L-03 — `notes_service_README.md` déplacé de `src/` vers `docs/`

- **docs**: README racine poli pour publication, ouverture réécrite, Party Mode clarifié comme workflow, runtime MCP corrigé à 12 outils et note licence explicitée

- **fix(agents)**: BACKLOG-002 — `master.md` compressé sous le budget interne avec sections obligatoires préservées, orchestration condensée et doublons de fin supprimés
- **fix(legacy)**: BACKLOG-003 — surfaces actives normalisées vers `Langis (Master)` et lexique legacy limité aux contextes historiques/tests autorisés

- **docs**: P6-H — README et CONTRIBUTING alignés sur 7 agents (5 core + 2 subagents), nouvelles commandes `gsane.sh` et règles customize/sections obligatoires
- **fix(config)**: P6-H — les 7 fichiers `_gsane/_config/agents/*.customize.yaml` sont désormais non vides avec `agent`, `status`, `scope` et `constraints` cohérents avec le manifest
- **fix(agents)**: P6-H — sections `## Activation` ajoutées aux 5 agents core, linter durci pour exiger littéralement les 8 sections sur tous les agents du manifest, et versions manifest bumpées pour les agents modifiés
- **fix(ci)**: validation PR agent-sync rendue compatible avec 7 agents déclarés dans `agent-manifest.yaml` au lieu d'un comptage figé à 5
- **feat(runtime)**: P6-H — câblage runtime Vera/Sage : étape Security Gate Vera dans `cc-verify`, step CI `Vera — Security Gate`, triggers Sage dans `master.md`, `post-session-analysis` et `session-start.sh`
- **feat(hooks)**: activation de Sage dans `session-start.sh` au-dessus du warning threshold du context budget avec suggestion de décharger les agents inactifs
- **fix(agents)**: ajout des fichiers `vera.customize.yaml` et `sage.customize.yaml` + garde qa-linter pour exiger un `.customize.yaml` par agent du manifest
- **feat(session)**: P6-F — Session resumption : reprise de session interrompue via checkpoint MCP, commande `gsane.sh session --resume`, marquage automatique dans session-stop.sh
- **feat(agents)**: P6-G — Subagents Vera (Security Reviewer 🔒) et Sage (Context Guardian 📊) : revue sécurité en lecture seule et surveillance budget tokens, status subagent dans agent-manifest.yaml
- **feat(tests)**: P6-E — Tests de token budget : métriques de régression pour détecter l'inflation des fichiers GSANE (seuils calibrés par Winston, marker pytest `token_budget`)
- **docs**: P6-DOC — Synchronisation documentation racine (README, CONTRIBUTING, AGENTS) avec l'état réel post-sprints P1→P6 Batch 1 : badges mis à jour (164 tests, 10 MCP), nouvelles commandes CLI documentées, Context Budget section ajoutée, version agents dans les tableaux, glossaire dédupliqué
- **feat(tools)**: P6-B — Validation JSON des Delivery Contracts : `dc-validator.py` + `dc-schema.json` + commande `gsane.sh dc --validate <fichier.md>` avec tests
- **feat(flywheel)**: P6-D — Mécanisme de rollback flywheel : tag git `gsane-flywheel-pre-{timestamp}` avant chaque auto-correction, revert automatique si tests échouent, commande `gsane.sh flywheel --rollback <tag>`
- **feat(agents)**: P6-C — Versioning sémantique des agents : `version` (semver X.Y.Z), `updated_at` (ISO date), `status` dans agent-manifest.yaml. Validation qa-linter + CI step dans validate-pr.yml
- **fix(cli)**: `grep -v` dans le gate documentaire de `gsane.sh validate` absorbé avec `|| true` — `set -e` tuait le script quand seul `_gsane/_memory/trace.log` était dirty (exit code 1 de grep sans résultat)
- **fix(ci)**: Guard pr-autofill remplacé — comparaison au contenu du PR template au lieu du seuil `body.length > 200` (le template GitHub de 746 chars déclenchait toujours le skip)
- **fix(cli)**: Gate CHANGELOG dans `gsane.sh validate` exclut `_gsane/_memory/` (fichiers runtime) pour éviter les faux positifs locaux
- **fix(cli)**: Bandit et pip-audit optionnels dans `gsane.sh validate` — warning + skip si non installés, CI reste la référence
- **feat(ci)**: Step post-release dans `release-please.yml` — sync automatique `version` dans `_gsane/config.yaml` et `version.txt` après chaque release
- **fix(style)**: Merge nested `if` statements dans `gsane_search_memory` — ruff SIM102 (compression_tool.py)
- **chore(git)**: Ignore `*.code-workspace` et retire `zav-sandbox.code-workspace` + `.vscode/launch.json` du suivi git (fichiers locaux, ne doivent pas être partagés)
- **fix(cli)**: `gsane.sh mcp --health` fallback gracieux si module `mcp` absent (Windows/WSL) — warning + EXIT 0 au lieu de EXIT 1, CI Ubuntu reste la référence
- **feat(mcp)**: P5-B — Refactor `gsane_search_memory` : contexte ±2 lignes, scopes `all/sessions/failures/decisions`, format retour `"Résultats pour '{query}' dans {scope}:"`
- **feat(mcp)**: P5-C — Refactor `gsane_emit_event` : signature `(event_type, agent, payload: dict, task_id)`, validation event_type standards avec warning non-standard, timestamp dans retour
- **feat(hooks)**: P5-D — Détection sessions sans post-session-analysis dans `session-start.sh` : warning si dernière session > 24h sans marqueur de clôture
- **feat(cli)**: P5-A — `gsane.sh trace --report` génère un rapport HTML auto-suffisant dans `_gsane-output/trace-report-{date}.html` via `_gsane/tools/trace-report.py`
- **feat(cli)**: P5-E — `gsane.sh trace --summary` enrichi avec métriques par agent (invocations, trust score moy, dernier event, ratio pass/fail)
- **feat(config)**: P6-A — Context Budget Strategy : section `context_budget` dans config.yaml, calcul du budget au démarrage dans session-start.sh, section Context Budget Management dans master.md

- **fix(ci)**: Correction syntaxe YAML dans `pr-autofill.yml` — template literal JS multi-lignes remplacé par array join (ligne 116 cassait le bloc `|`)
- **docs(contributing)**: Section "Prérequis Windows" ajoutée — WSL recommandé, Git Bash alternatif, CI comme validation de référence
- **fix(cli)**: `gsane.sh doctor` détecte Windows/Git Bash et affiche un warning explicite au lieu de crasher silencieusement
- **docs(skills)**: Batch P4 — création/réécriture de 5 skills Copilot : `prompt-engineering` (structure DC, AC, requêtes complexes), `delivery-contract` (template officiel, numérotation, fix trivial), `git-workflow` (cheat-sheet branches/commits/PR), `mcp-integration` (5 outils MCP avec exemples et retry pattern), `debugging-gsane` (arbre diagnostic 5 symptômes)
- **fix(agents)**: Suppression du BOM UTF-8 dans `qa.agent.md` qui empêchait le parsing du frontmatter YAML
- **fix(template)**: PR template corrigé — encodage UTF-8 restauré (accents + checkboxes), chemin ruff corrigé `_gsane/ tests/` au lieu de `src/`
- **feat(ci)**: Workflow `pr-autofill.yml` — auto-remplit le body de PR à l'ouverture (type de changement, agents impliqués, checklist pré-cochée, description depuis commits)
- **feat(agents)**: Architecture SSOT — manifest réduit à registre machine (10 champs, 2.5KB vs 6.9KB), adaptateurs Copilot standardisés, template agent officiel créé, validate-pr.yml aligné sur golden_rule/never_do
- **feat(agents)**: Optimisation token du manifest — titles raccourcis (2-3 mots), identity en 1 phrase, principles en listes YAML, ajout golden_rule, suppression "ship it" de Quinn. Réduction 15% (8142→6916 octets). 18 champs uniformes par agent.
- **feat(agents)**: Différenciation des blocs `<persona>` XML — chaque agent a désormais des balises `<identity>`, `<communication_style>`, `<principles>` uniques alignées sur ses sections narratives. Frontmatter unifié (version 2.0, persona-template-v2) sur les 5 agents.
- **feat(ci)**: Pipeline CI consolidé en un seul job `gsane-quality-gate` — checkout, setup Python 3.11, `pip install -e ".[mcp,test]"`, ruff check, mypy, pytest (149 tests, behavioral exclus), MCP health check
- **feat(lint)**: Configuration ruff (line-length=100, E501 ignoré, exclude _gsane-output/) et mypy (warn_unused_ignores, files mcp-server/) — 63 erreurs ruff corrigées, 10 erreurs mypy résolues
- **feat(coverage)**: Badge coverage (99% src) et 149 tests dans README, seuil coverage 50% validé
- **chore(deps)**: Dependabot étendu — ajout pip racine "/" avec ignore major updates, schedule monday pour tous les ecosystems
- **fix**: Correction erreurs CI mypy et ruff (18 erreurs) — typage explicite, imports triés, datetime.UTC, auto-exclusion security_gate du scan
- **chore**: Ajout [build-system] et extras mcp/test dans pyproject.toml

**[repo]** Sprint 2 : Nettoyage .vscode/ (seul extensions.json versionné, autres ignorés), suppression V2-RELEASE-NOTES.md, neutralisation release-v2.sh (supprimé, plus de génération accidentelle possible).

**[audit]** Aucun fichier fix_ci.py n'existe dans le dépôt (hors caches/artefacts ignorés). Conformité confirmée.

**[feat]** Modèle canonique activé: brief humain durable dans `_gsane/_memory/project-context.md`, vues MCP canoniques de lecture, et fichiers de session formellement déclassés en audit/continuité.

**[feat]** Mode sécurité léger centralisé: escalade Master avec owner Winston, gate Quinn, revue Bond conditionnelle, confinement MCP et quality gate enrichie par scan secrets, Bandit et pip-audit.

**[docs]** Nettoyage éditorial historique du module notes et clarification des notes de release V2, sans changement fonctionnel.

**[docs]** Fusion des points utiles de `V2-RELEASE-NOTES.md` dans l'historique `Unreleased`.

**[fix]** Durcissement hygiène sécurité: suppression de la config MCP VS Code versionnée, garde-fou Git contre chemins absolus/secrets, et sécurisation de `gsane.sh`.

**[fix]** Nettoyage des prompts, skills et configs IDE GSANE actifs; garde-fous QA/pytest ajoutés contre les références legacy cassées.

### ✨ Refonte Architecture — Flat Design Strike Team

**[Refactor]** Migration de l'architecture CIS/TEA/BMB (20+ agents) vers Flat Design 5 agents (Strike Team)
- Agents actifs : Langis (Master), Amelia (Dev), Quinn (QA), Winston (Architect), Bond (Agent Builder)
- ADR documenté : `docs/architecture/decisions/ADR-001-flat-design.md`

**[feat]** Intégration MCP complète et cohérente
- Point d'entrée unique : `_gsane/mcp-server/compression_tool.py` avec 8 outils MCP (3 vues canoniques + 5 outils historiques)
- Outils : `gsane_fetch_compressed_memory`, `gsane_write_session_checkpoint`, `gsane_read_checkpoint`, `gsane_route`, `gsane_memory_fetch`
- Chemins dérivés de `Path(__file__)` — indépendants du cwd
- Alignement schéma `delegation-matrix.yaml` : clés `trigger` + `agent`
- Commandes CLI : `bash gsane.sh mcp --health` et `mcp --smoke-test`
- 14 tests MCP dans `tests/test_mcp.py`

**[feat]** Quality Gate — 107 tests (structurel + comportemental + MCP)
- `tests/qa-linter.py` — lint structure agents + legacy scanner + hooks + manifests
- `tests/test_gsane_orchestration.py` — 62 tests (structurel + comportemental bash)
- `tests/test_mcp.py` — 14 tests smoke MCP
- Marker `behavioral` pour tests shell isolés (skip si Git Bash absent)

**[feat]** Observabilité trace.log
- Format YAML uniforme : timestamp, session_id, event, agent, task_id, duration_ms, trust_score, details
- Invocations MCP automatiquement journalisées
- Commandes : `bash gsane.sh trace --tail N | --summary | --p2p`

**[feat]** Gouvernance et workflows
- `delegation/workflow.md` v3.0 — trust_score, brief structuré, audit path unifié
- `party-mode/workflow.md` v2.0 — Niveau 1 Huddle (APPROVE/BLOCK), Niveau 2 Brainstorm
- `cc-verify/workflow.md` v2.0 — 4 étapes exécutables, PASS/FAIL/INCOMPLETE
- `standard-agent-behavior.md` v2.0 — PRE-FLIGHT, POST-FLIGHT, P2P, MEMORY-LIGHT

**[feat]** Mémoire persistante
- Master-sidecar + Bond-sidecar créés (project-state.md + learned-lessons.md)
- Taxonomie volatile/durable dans `manifest.yaml` v3.0.0
- Bootstrap : `bash _gsane/tools/gsane-bootstrap.sh`

**[chore]** Nettoyage références legacy
- Suppression de toutes les références Léo/Aria/Morgan/Wendy/CIS/TEA/BMB
- Hooks realignés : session-stop.sh, flywheel-trigger.sh, session-start.sh
- Skills GSANE corrigées : gsane-framework/SKILL.md, agent-customization/SKILL.md

---

## [Archive]

> L'historique détaillé des sessions de développement antérieures (architecture CIS/TEA/BMB, modules étendus) est disponible dans l'historique git.
