#!/usr/bin/env bash
# Session Stop Hook — Déclenché par l'événement Stop (fin de session BMAD)
# Garantit que post-session-analysis s'exécute même sans commande DA explicite.
set -euo pipefail

WORKSPACE_ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
PSA_WORKFLOW="$WORKSPACE_ROOT/_bmad/core/workflows/post-session-analysis/workflow.md"

echo "[SessionStop] Session ending — triggering post-session-analysis..."

if [[ ! -f "$PSA_WORKFLOW" ]]; then
  echo "[SessionStop] WARNING: post-session-analysis/workflow.md not found — skipping"
  exit 0
fi

# Note: L'exécution réelle du workflow est gérée par l'agent (bmad-master).
# Ce script sert de signal d'audit — l'agent lit hooks.json et sait que
# Stop → post-session-analysis doit être déclenché avant de rendre la main.
echo "[SessionStop] ✅ Post-session hook signaled. Workflow: $PSA_WORKFLOW"
