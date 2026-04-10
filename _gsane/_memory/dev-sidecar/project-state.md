# dev — Project State
<!-- 3-bullet session summary — updated by SESSION HOOK -->

- Delivery Contract `SECURITY-GATE-LITE-2026-04-09-01` implémenté avec source de vérité déclarative `security_gate`, helper `_gsane/tools/security_gate.py` et nettoyage des doublons MCP dans `_gsane/mcp-server/compression_tool.py`.
- Quality gate élargie sans refonte: scan secrets bloquant, Bandit, `pip-audit`, hook pre-commit stage-aware, CI PR et docs/prompt minimaux alignés sur owner Winston + gate Quinn + Bond conditionnel.
- Validation locale PASS via Git Bash explicite: `131 passed, 6 deselected`, QA Linter PASS, `bash gsane.sh validate` PASS, `bash gsane.sh mcp --health` PASS, `bash gsane.sh mcp --smoke-test` PASS; le shim `bash` VS Code reste pointé vers WSL non configuré.
