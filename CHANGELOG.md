# CHANGELOG

Format basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

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
