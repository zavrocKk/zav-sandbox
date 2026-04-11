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

### Added

* **governance:** section Délégation Obligatoire dans master.md — filtre 3 questions avant toute action Langis (DELEG-ENFORCE-001)
* **governance:** règle orchestrateur pur dans delegation/workflow.md avec 4 exceptions autorisées (DELEG-ENFORCE-001)
* **tests:** 2 tests qa-linter — test_master_never_do_delegation_rules + test_delegation_workflow_no_solo (DELEG-ENFORCE-001)

### Changed

* **governance:** Never Do master.md renforcé — mapping 6 agents (Amelia, Quinn, Winston, Bond, Vera, Sage) + interdictions spécialiste (DELEG-ENFORCE-001)
* **governance:** solo-creep detector renforcé — 4 critères objectifs, sévérité HIGH systématique (DELEG-ENFORCE-001)
* **governance:** fallback guard dans delegation-matrix — re-scoring obligatoire avant self-execute (RIGOR-G1G5)
* **governance:** output-nature guard dans delegation workflow — master interdit si tâche produit un fichier (RIGOR-G1G5)
* **governance:** visible closure idempotence dans standard-agent-behavior et copilot-instructions

---
## [Archive]

> L'historique détaillé des sessions de développement antérieures (architecture CIS/TEA/BMB, modules étendus) est disponible dans l'historique git.
