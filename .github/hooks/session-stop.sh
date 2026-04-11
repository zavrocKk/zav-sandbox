#!/usr/bin/env bash
# Session Stop Hook — Déclenché par l'événement Stop (fin de session gsane)
# Garantit que post-session-analysis s'exécute même sans commande DA explicite.
set -euo pipefail

WORKSPACE_ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
PSA_WORKFLOW="$WORKSPACE_ROOT/_gsane/workflows/post-session-analysis/workflow.md"

echo "[SessionStop] Session ending — triggering post-session-analysis..."

if [[ ! -f "$PSA_WORKFLOW" ]]; then
  echo "[SessionStop] WARNING: post-session-analysis/workflow.md not found — skipping"
  exit 0
fi

# Note: L'exécution réelle du workflow est gérée par l'agent (master).
# Ce script sert de signal d'audit — l'agent lit hooks.json et sait que
# Stop → post-session-analysis doit être déclenché avant de rendre la main.

# Mark checkpoint as interrupted if no post-session-analysis was completed
SESSION_STATE="$WORKSPACE_ROOT/_gsane/_memory/sessions/session-state.md"
PSA_LOG="$WORKSPACE_ROOT/_gsane/_memory/session-analysis-log.md"

if [[ -f "$SESSION_STATE" ]]; then
  # Check if post-session-analysis ran today
  TODAY=$(date +%Y-%m-%d)
  PSA_RAN=false
  if [[ -f "$PSA_LOG" ]] && grep -q "$TODAY" "$PSA_LOG" 2>/dev/null; then
    PSA_RAN=true
  fi

  if [[ "$PSA_RAN" == "false" ]]; then
    # Mark as interrupted — sed portable
    if grep -q "^interrupted:" "$SESSION_STATE" 2>/dev/null; then
      sed -i "s/^interrupted:.*/interrupted: true/" "$SESSION_STATE"
    else
      echo "interrupted: true" >> "$SESSION_STATE"
    fi
    echo "[SessionStop] ⚠️ Session marked as interrupted (no post-session-analysis today)"
  else
    # Mark as NOT interrupted
    if grep -q "^interrupted:" "$SESSION_STATE" 2>/dev/null; then
      sed -i "s/^interrupted:.*/interrupted: false/" "$SESSION_STATE"
    fi
    echo "[SessionStop] ✅ Post-session-analysis completed — session clean"
  fi
fi

echo "[SessionStop] ✅ Post-session hook signaled. Workflow: $PSA_WORKFLOW"
