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

# ── 5. Détection sessions sans post-session-analysis ─────────────────────────
SESSION_LOG="$WORKSPACE_ROOT/_gsane/_memory/sessions/session-analysis-log.md"
if [[ -f "$SESSION_LOG" ]]; then
  # Extraire la date de la dernière entrée "## Session: YYYY-MM-DD"
  LAST_SESSION_DATE=$(grep -oE '## Session: [0-9]{4}-[0-9]{2}-[0-9]{2}' "$SESSION_LOG" 2>/dev/null | tail -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')
  if [[ -n "${LAST_SESSION_DATE:-}" ]]; then
    # Vérifier si la dernière session a un marqueur de clôture
    LAST_SESSION_BLOCK=$(awk "/## Session: ${LAST_SESSION_DATE}/,/^## Session:/" "$SESSION_LOG" | head -20)
    HAS_CLOSURE=$(echo "$LAST_SESSION_BLOCK" | grep -c 'compliance:' 2>/dev/null || true)
    if [[ "$HAS_CLOSURE" -eq 0 ]]; then
      # Calculer l'âge de la session (compatible Git Bash + Linux/Mac)
      NOW_EPOCH=$(date +%s 2>/dev/null || echo 0)
      SESSION_EPOCH=$(date -d "$LAST_SESSION_DATE" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$LAST_SESSION_DATE" +%s 2>/dev/null || echo 0)
      if [[ "$NOW_EPOCH" -gt 0 ]] && [[ "$SESSION_EPOCH" -gt 0 ]]; then
        AGE_SECONDS=$((NOW_EPOCH - SESSION_EPOCH))
        AGE_HOURS=$((AGE_SECONDS / 3600))
        if [[ "$AGE_HOURS" -ge 24 ]]; then
          echo "[SessionStart] ⚠️ Session précédente ($LAST_SESSION_DATE) sans post-session-analysis détectée."
          echo "   Lancer /gsane-post-session pour clôturer."
        fi
      fi
    fi
  fi
fi

echo "[SessionStart] ✅ Session #$SESSION_COUNT ready."
