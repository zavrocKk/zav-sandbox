#!/usr/bin/env bash
# Session Start Hook — GSANE Strike Team (5 agents, YAML manifests)
# Appelé par gsane.sh doctor

set -euo pipefail

WORKSPACE_ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
SESSION_COUNT_FILE="$WORKSPACE_ROOT/_gsane/_memory/.session_count"

echo "[SessionStart] Initializing GSANE session..."

# ── 1. Vérifier les fichiers de configuration ─────────────────────────────────
for required_file in \
  "$WORKSPACE_ROOT/_gsane/config.yaml" \
  "$WORKSPACE_ROOT/_gsane/_config/agent-manifest.yaml" \
  "$WORKSPACE_ROOT/_gsane/_config/workflow-manifest.yaml" \
  "$WORKSPACE_ROOT/_gsane/_config/delegation-matrix.yaml"; do
  if [[ ! -f "$required_file" ]]; then
    echo "[SessionStart] WARNING: $required_file not found"
  else
    echo "[SessionStart] ✅ $required_file"
  fi
done

# ── 2. Compter et valider les agents Strike Team ──────────────────────────────
EXPECTED_AGENTS=5
AGENT_COUNT=$(find "$WORKSPACE_ROOT/_gsane/agents" -name "*.md" 2>/dev/null | wc -l)
echo "[SessionStart] Strike Team agents found: $AGENT_COUNT / $EXPECTED_AGENTS expected"
if [[ "$AGENT_COUNT" -lt "$EXPECTED_AGENTS" ]]; then
  echo "[SessionStart] WARNING: Expected $EXPECTED_AGENTS agents, found $AGENT_COUNT"
fi

# ── 3. Incrémenter session_count ──────────────────────────────────────────────
mkdir -p "$(dirname "$SESSION_COUNT_FILE")"
if [[ -f "$SESSION_COUNT_FILE" ]]; then
  SESSION_COUNT=$(cat "$SESSION_COUNT_FILE")
  SESSION_COUNT=$((SESSION_COUNT + 1))
else
  SESSION_COUNT=1
fi
echo "$SESSION_COUNT" > "$SESSION_COUNT_FILE"
echo "[SessionStart] Session count: $SESSION_COUNT"

# ── 4. Vérifier les dossiers output ──────────────────────────────────────────
OUTPUT_DIR="$WORKSPACE_ROOT/_gsane-output"
mkdir -p "$OUTPUT_DIR"
echo "[SessionStart] Output dir: $OUTPUT_DIR"

echo "[SessionStart] ✅ Session #$SESSION_COUNT ready."
