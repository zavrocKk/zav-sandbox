#!/usr/bin/env bash
# Flywheel Trigger Hook — Déclenché par post-session-analysis Step 6
# quand session_count % flywheel.trigger_every_n_sessions == 0
set -euo pipefail

WORKSPACE_ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
FLYWHEEL_WF="$WORKSPACE_ROOT/_gsane/workflows/flywheel/workflow.md"
SESSION_COUNT_FILE="$WORKSPACE_ROOT/_gsane/_memory/.session_count"

SESSION_COUNT=$(cat "$SESSION_COUNT_FILE" 2>/dev/null || echo "unknown")

echo "[FlywheelTrigger] 🔄 Flywheel fired at session #$SESSION_COUNT"

if [[ ! -f "$FLYWHEEL_WF" ]]; then
  echo "[FlywheelTrigger] ❌ ERROR: workflow.md not found at $FLYWHEEL_WF"
  exit 1
fi

# Note: L'exécution des workflows est gérée par l'agent (master).
# Ce script valide que le fichier cible existe et loggue le déclenchement.
echo "[FlywheelTrigger] ✅ Target verified:"
echo "  flywheel: $FLYWHEEL_WF"
echo "[FlywheelTrigger] Flywheel execution handed to master."
