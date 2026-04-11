# CHANGELOG

Format basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.4.0](https://github.com/zavrocKk/zav-sandbox/compare/v2.3.0...v2.4.0) (2026-04-11)


### Features

* **prompts:** add 7 gsane-* prompts + PRBodyCheck hook ([#73](https://github.com/zavrocKk/zav-sandbox/issues/73)) ([b20a876](https://github.com/zavrocKk/zav-sandbox/commit/b20a87627f38d6768800b5babe7b92e4c9ca5e58))
* **tests:** add agentic test suite (DC-BEHAVIORAL-TESTS-001) ([#75](https://github.com/zavrocKk/zav-sandbox/issues/75)) ([e685ccf](https://github.com/zavrocKk/zav-sandbox/commit/e685ccf9a1e111930d046c132a58c311419a0c28))


### Bug Fixes

* **governance:** add HUMAN-IN-THE-LOOP guardrail (FM-007) ([#76](https://github.com/zavrocKk/zav-sandbox/issues/76)) ([60c2639](https://github.com/zavrocKk/zav-sandbox/commit/60c2639c96723f66261168cd11c3175afb64d86f))

## [2.3.0](https://github.com/zavrocKk/zav-sandbox/compare/v2.2.0...v2.3.0) (2026-04-11)


### Features

* **context:** JIT triggers on 14 skills + /compact recommendations ([#70](https://github.com/zavrocKk/zav-sandbox/issues/70)) ([e259f45](https://github.com/zavrocKk/zav-sandbox/commit/e259f45b31ff271c496fb692aaff1ba970e0d41e))

## [Unreleased]

### Added
- **behavioral-tests**: Suite de tests agentiques — routing behavior (18 tests), agent decisions (6 tests), session scenarios (8 tests), circuit breakers (6 tests)
- **conftest**: 8 fixtures session-scoped pour les tests agentiques (trace_events, routing_oracle, gsane_config, etc.)
- **human-in-the-loop**: Règle HUMAN-IN-THE-LOOP ajoutée dans git-workflow (Step 5b), master.md, standard-agent-behavior.md, copilot-instructions.md, AGENTS.md, CLAUDE.md — merge/push-force/delete-branch interdit sans approbation explicite (FM-007)

### Fixed
- **skills-jit**: Remplacement applyTo: "**" par patterns ciblés sur 9 skills — économie ~4500 tokens/requête
- **H-04**: SHA-pin all GitHub Actions across 5 workflows (ci, validate-pr, release-please, pr-autofill, cleanup-branches)
- **H-05**: `notes_service.py` STORAGE_FILE anchored to `__file__` (CWD-independent)
- **H-07**: Remove `sys.path.insert` hacks from 3 test files (pythonpath in pyproject.toml)
- **Bandit CI**: Correct misleading "CI Ubuntu valide cette gate" message in gsane.sh
- **ShellCheck SC2053**: Fix glob match syntax in gsane.sh (`[` → `[[`)
- **Pyright**: Remove unused `type: ignore[import-not-found]` from test_mcp.py and test_security_gate.py
- **manifest**: Register missing `session-resume` workflow in workflow-manifest.yaml

### Added
- **prompts**: 7 nouveaux prompts `/gsane-*` pour mécanismes actifs (challenge, party-mode, session-resume, hypothesis, mutation, benchmark, delegation-audit)
- **hooks**: Script `pr-body-check.sh` pour PRBodyCheck — vérifie body non-vide, non-template, ≥20 mots
- **context-optimization**: Triggers JIT sur 14 skills, recommandations /compact dans session-start.sh, section context_optimization dans config.yaml, 4 tests compliance
- **claude-code**: Structure `.claude/` pour intégration Claude Code — CLAUDE.md, settings.json, 7 commandes, 4 agents, 6 skills migrées
- **test-pyramid**: Restructuration tests/ en 5 niveaux (unit, integration, compliance, performance, e2e) avec markers pytest strict
- **benchmarks**: 4 benchmarks MCP (gsane_route, yaml_parse, fetch_memory, checkpoint_read) + commande `bash gsane.sh benchmark`
- **mutation**: Support mutmut pour mutation testing + commande `bash gsane.sh mutation`
- **H-01**: Standard Python logging in 5 modules (math_utils, text_analyzer, notes_service, security_gate, compression_tool)
- **H-02**: Vera (security) and Sage (context budget) rules in delegation-matrix.yaml
- **H-03**: `requirements.lock` for reproducible builds
- **Bandit CI**: Bandit SAST step in ci.yml (`-ll` = MEDIUM+ only), bandit moved to `[test]` extras
- **nosec**: Documented `# nosec B404,B603,B607` annotations on legitimate subprocess calls in security_gate.py
- **governance:** section Délégation Obligatoire dans master.md (DELEG-ENFORCE-001)
- **governance:** règle orchestrateur pur dans delegation/workflow.md (DELEG-ENFORCE-001)
- **tests:** 2 tests qa-linter (test_master_never_do_delegation_rules + test_delegation_workflow_no_solo)
- **CHALLENGE**: Mécanisme CHALLENGE câblé dans 4 agents (master, dev, architect, vera), 3 workflows (party-mode, delegation, cc-verify), 4 event types, et 7 tests fonctionnels
- **Vera functions**: `check_prompt_injection()` and `check_ci_permissions()` in security_gate.py — `bash gsane.sh vera`

### Changed
- **flywheel**: Merged workflow-aggregate.md + workflow-apply.md + flywheel-test-checklist.md into unified workflow.md (3→1 file). Added Phase 0 trigger + Exclusions guard-rails
- **governance:** Never Do master.md renforcé — mapping 6 agents + interdictions spécialiste (DELEG-ENFORCE-001)
- **governance:** solo-creep detector renforcé — 4 critères objectifs, sévérité HIGH systématique (DELEG-ENFORCE-001)
- **governance:** fallback guard + output-nature guard dans delegation workflow (RIGOR-G1G5)
- **governance:** visible closure idempotence dans standard-agent-behavior et copilot-instructions

### Removed
- **Sage (Context Guardian)**: Dissolved — budget monitoring handled by session-start.sh + post-session-analysis + Langis direct
- **Vera (Security agent)**: Dissolved — 2 unique checks (prompt injection, CI permissions) integrated as functions in security_gate.py
- `/gsane-help` workflow and all 22 references across 12 files (declared obsolete)

---
