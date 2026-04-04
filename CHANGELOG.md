# CHANGELOG

Format basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### ✨ Refonte Architecture — Flat Design Strike Team

**[Refactor]** Migration de l'architecture CIS/TEA/BMB (20+ agents) vers Flat Design 5 agents (Strike Team)
- Agents actifs : Langis (Master), Amelia (Dev), Quinn (QA), Winston (Architect), Bond (Agent Builder)
- ADR documenté : `docs/architecture/decisions/ADR-001-flat-design.md`

**[feat]** Intégration MCP complète et cohérente
- Point d'entrée unique : `_gsane/mcp-server/compression_tool.py` avec 5 outils MCP
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
