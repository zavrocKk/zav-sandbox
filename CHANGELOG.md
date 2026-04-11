# CHANGELOG

Format basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Fixed
- **H-04**: SHA-pin all GitHub Actions across 5 workflows (ci, validate-pr, release-please, pr-autofill, cleanup-branches)
- **H-05**: `notes_service.py` STORAGE_FILE anchored to `__file__` (CWD-independent)
- **H-07**: Remove `sys.path.insert` hacks from 3 test files (pythonpath in pyproject.toml)
- **Bandit CI**: Correct misleading "CI Ubuntu valide cette gate" message in gsane.sh
- **ShellCheck SC2053**: Fix glob match syntax in gsane.sh (`[` → `[[`)
- **Pyright**: Remove unused `type: ignore[import-not-found]` from test_mcp.py and test_security_gate.py
- **manifest**: Register missing `session-resume` workflow in workflow-manifest.yaml

### Added
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
