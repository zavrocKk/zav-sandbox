#!/usr/bin/env bash
# gsane-bootstrap.sh — Initialise les fichiers runtime GSANE sur un clone propre
# Usage: bash _gsane/tools/gsane-bootstrap.sh

set -euo pipefail
WORKSPACE_ROOT="${GITHUB_WORKSPACE:-$(pwd)}"

echo "[Bootstrap] Initialisation GSANE runtime..."

# ── Dossiers output ──────────────────────────────────────────────────────────
mkdir -p "$WORKSPACE_ROOT/_gsane-output"
mkdir -p "$WORKSPACE_ROOT/_gsane-output/test-artifacts"
mkdir -p "$WORKSPACE_ROOT/docs/architecture/decisions"
echo "[Bootstrap] ✅ Dossiers output créés"

# ── Sidecars mémoire ─────────────────────────────────────────────────────────
for sidecar in master-sidecar dev-sidecar qa-sidecar architect-sidecar bond-sidecar; do
    mkdir -p "$WORKSPACE_ROOT/_gsane/_memory/$sidecar"
    if [ ! -f "$WORKSPACE_ROOT/_gsane/_memory/$sidecar/project-state.md" ]; then
        echo "last_session: null" > "$WORKSPACE_ROOT/_gsane/_memory/$sidecar/project-state.md"
        echo "[Bootstrap] ✅ $sidecar/project-state.md créé"
    fi
done

# ── trace.log ────────────────────────────────────────────────────────────────
TRACE_LOG="$WORKSPACE_ROOT/_gsane/_memory/trace.log"
if [ ! -f "$TRACE_LOG" ]; then
    cat > "$TRACE_LOG" << 'EOF'
- timestamp: bootstrap
  session_id: bootstrap
  event: session_started
  agent: master
  task_id: null
  duration_ms: null
  trust_score: null
  details: "trace.log initialized by gsane-bootstrap.sh"
EOF
    echo "[Bootstrap] ✅ trace.log créé"
fi

# ── Session count ─────────────────────────────────────────────────────────────
SESSION_COUNT_FILE="$WORKSPACE_ROOT/_gsane/_memory/.session_count"
if [ ! -f "$SESSION_COUNT_FILE" ]; then
    echo "0" > "$SESSION_COUNT_FILE"
    echo "[Bootstrap] ✅ .session_count initialisé"
fi

# ── Delegation audit ──────────────────────────────────────────────────────────
AUDIT="$WORKSPACE_ROOT/_gsane-output/delegation-audit.md"
if [ ! -f "$AUDIT" ]; then
    cat > "$AUDIT" << 'EOF'
# Delegation Audit Log

| timestamp | agent | task_id | intent | verdict | trust_score |
|---|---|---|---|---|---|
EOF
    echo "[Bootstrap] ✅ delegation-audit.md créé"
fi

echo "[Bootstrap] ✅ Runtime GSANE initialisé."
