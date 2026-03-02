#!/usr/bin/env bash
# Flywheel Trigger Hook — Déclenché par post-session-analysis Step 6
# quand session_count % flywheel.trigger_every_n_sessions == 0
set -euo pipefail

WORKSPACE_ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
AGGREGATE_WF="$WORKSPACE_ROOT/_gsane/core/workflows/flywheel/workflow-aggregate.md"
APPLY_WF="$WORKSPACE_ROOT/_gsane/core/workflows/flywheel/workflow-apply.md"
SESSION_COUNT_FILE="$WORKSPACE_ROOT/_gsane/_memory/.session_count"

SESSION_COUNT=$(cat "$SESSION_COUNT_FILE" 2>/dev/null || echo "unknown")

echo "[FlywheelTrigger] 🔄 Flywheel fired at session #$SESSION_COUNT"

if [[ ! -f "$AGGREGATE_WF" ]]; then
  echo "[FlywheelTrigger] ❌ ERROR: workflow-aggregate.md not found at $AGGREGATE_WF"
  exit 1
fi

if [[ ! -f "$APPLY_WF" ]]; then
  echo "[FlywheelTrigger] ❌ ERROR: workflow-apply.md not found at $APPLY_WF"
  exit 1
fi

# Note: L'exécution des workflows est gérée par l'agent (gsane-master).
# Ce script valide que les fichiers cibles existent et loggue le déclenchement.
echo "[FlywheelTrigger] ✅ Targets verified:"
echo "  aggregate: $AGGREGATE_WF"
echo "  apply:     $APPLY_WF"
echo "[FlywheelTrigger] Flywheel execution handed to gsane-master."
