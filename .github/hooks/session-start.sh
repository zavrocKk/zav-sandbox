#!/usr/bin/env bash
# Session Start Hook — Initialise le contexte de session BMAD
# Déclenché par l'événement SessionStart dans hooks.json
set -euo pipefail

WORKSPACE_ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
SESSION_COUNT_FILE="$WORKSPACE_ROOT/_bmad/_memory/.session_count"

echo "[SessionStart] Initializing BMAD agent session..."

# ── 1. Vérifier la structure BMAD ─────────────────────────────────────────────
for required_file in \
  "$WORKSPACE_ROOT/_bmad/core/config.yaml" \
  "$WORKSPACE_ROOT/_bmad/_config/agent-manifest.csv" \
  "$WORKSPACE_ROOT/_bmad/_config/workflow-manifest.csv" \
  "$WORKSPACE_ROOT/_bmad/_config/agent-delegation-matrix.csv"; do
  if [[ ! -f "$required_file" ]]; then
    echo "[SessionStart] WARNING: $required_file not found"
  fi
done

# ── 2. Compter et valider les agents ──────────────────────────────────────────
EXPECTED_AGENTS=13
AGENT_COUNT=$(find "$WORKSPACE_ROOT/.github/agents" -name "*.agent.md" 2>/dev/null | wc -l)
echo "[SessionStart] Agents found: $AGENT_COUNT / $EXPECTED_AGENTS expected"
if [[ "$AGENT_COUNT" -lt "$EXPECTED_AGENTS" ]]; then
  echo "[SessionStart] WARNING: Expected $EXPECTED_AGENTS agents, found $AGENT_COUNT — run audit"
fi

# ── 3. Scanner les chemins dépréciés dans les prompts ─────────────────────────
DEPRECATED=$(grep -rl "_bmad/bmm/" "$WORKSPACE_ROOT/.github/prompts/" 2>/dev/null | wc -l)
if [[ "$DEPRECATED" -gt 0 ]]; then
  echo "[SessionStart] ERROR: $DEPRECATED prompt(s) still reference deprecated _bmad/bmm/ path!"
  grep -rl "_bmad/bmm/" "$WORKSPACE_ROOT/.github/prompts/" 2>/dev/null
else
  echo "[SessionStart] No deprecated paths detected. ✅"
fi

# ── 4. Incrémenter session_count ──────────────────────────────────────────────
mkdir -p "$(dirname "$SESSION_COUNT_FILE")"
if [[ -f "$SESSION_COUNT_FILE" ]]; then
  SESSION_COUNT=$(cat "$SESSION_COUNT_FILE")
  SESSION_COUNT=$((SESSION_COUNT + 1))
else
  SESSION_COUNT=1
fi
echo "$SESSION_COUNT" > "$SESSION_COUNT_FILE"
echo "[SessionStart] Session count: $SESSION_COUNT"

# ── 5. Créer les dossiers output ──────────────────────────────────────────────
OUTPUT_DIR="$WORKSPACE_ROOT/_bmad-output"
mkdir -p "$OUTPUT_DIR" "$OUTPUT_DIR/bmb-creations" "$OUTPUT_DIR/test-artifacts"

echo "[SessionStart] ✅ Session #$SESSION_COUNT ready. Output: $OUTPUT_DIR"
