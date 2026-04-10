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

# ── 6. Context Budget Check ──────────────────────────────────────────────────
CONFIG_FILE="$WORKSPACE_ROOT/_gsane/config.yaml"
if [[ -f "$CONFIG_FILE" ]]; then
  if command -v python3 &>/dev/null; then
    python3 - "$CONFIG_FILE" "$WORKSPACE_ROOT" <<'PYEOF'
import sys, os
try:
    import yaml
except ImportError:
    sys.exit(0)

config_path = sys.argv[1]
workspace = sys.argv[2]

with open(config_path) as f:
    cfg = yaml.safe_load(f)

budget = cfg.get("context_budget")
if not budget:
    sys.exit(0)

max_tokens = budget.get("max_tokens_per_session", 8000)
warning_thr = budget.get("warning_threshold", 0.75)
critical_thr = budget.get("critical_threshold", 0.90)
skills_budget = budget.get("skills_budget", 1500)
agents_budget = budget.get("agents_budget", 2000)
workflows_budget = budget.get("workflows_budget", 1000)

# Count skills
skills_dir = os.path.join(workspace, ".github", "skills")
skills_count = 0
if os.path.isdir(skills_dir):
    for entry in os.listdir(skills_dir):
        skill_file = os.path.join(skills_dir, entry, "SKILL.md")
        if os.path.isfile(skill_file):
            skills_count += 1

# Count agents
agents_dir = os.path.join(workspace, "_gsane", "agents")
agents_count = 0
if os.path.isdir(agents_dir):
    for entry in os.listdir(agents_dir):
        if entry.endswith(".md"):
            agents_count += 1

# Config size (approximate tokens ~ bytes / 4)
config_size = os.path.getsize(config_path)
config_tokens = config_size // 4

# Estimate budget used
skills_used = min(skills_count * (skills_budget // max(skills_count, 1)), skills_budget) if skills_count > 0 else 0
agents_used = min(agents_count * (agents_budget // max(agents_count, 1)), agents_budget) if agents_count > 0 else 0
workflows_used = workflows_budget  # assume loaded at start
budget_used = skills_used + agents_used + workflows_used + config_tokens

percentage = (budget_used / max_tokens) * 100 if max_tokens > 0 else 0

print(f"[SessionStart] Context Budget: {budget_used}/{max_tokens} tokens ({percentage:.0f}%)")

if percentage > critical_thr * 100:
    print(f"[SessionStart] \U0001f534 CRITICAL: Context budget near exhaustion ({percentage:.0f}%) — consider reducing loaded context")
elif percentage > warning_thr * 100:
    print(f"[SessionStart] ⚠️ WARNING: Context budget approaching limit ({percentage:.0f}%)")

if percentage > warning_thr * 100:
  print(f"[SessionStart] ⚡ Sage activé — budget à {percentage:.0f}%")
  print("[SessionStart] Suggestion : décharger les agents inactifs")
PYEOF
  else
    # Fallback: basic estimation without python3
    SKILLS_COUNT=$(find "$WORKSPACE_ROOT/.github/skills" -name "SKILL.md" 2>/dev/null | wc -l)
    AGENTS_COUNT=$(find "$WORKSPACE_ROOT/_gsane/agents" -name "*.md" 2>/dev/null | wc -l)
    CONFIG_SIZE=$(wc -c < "$CONFIG_FILE" 2>/dev/null || echo 0)
    CONFIG_TOKENS=$((CONFIG_SIZE / 4))
    BUDGET_USED=$((1500 + 2000 + 1000 + CONFIG_TOKENS))
    MAX_TOKENS=8000
    if [[ "$MAX_TOKENS" -gt 0 ]]; then
      PERCENTAGE=$((BUDGET_USED * 100 / MAX_TOKENS))
    else
      PERCENTAGE=0
    fi
    echo "[SessionStart] Context Budget: $BUDGET_USED/$MAX_TOKENS tokens (${PERCENTAGE}%)"
    if [[ "$PERCENTAGE" -gt 90 ]]; then
      echo "[SessionStart] 🔴 CRITICAL: Context budget near exhaustion (${PERCENTAGE}%) — consider reducing loaded context"
    elif [[ "$PERCENTAGE" -gt 75 ]]; then
      echo "[SessionStart] ⚠️ WARNING: Context budget approaching limit (${PERCENTAGE}%)"
    fi
    if [[ "$PERCENTAGE" -gt 75 ]]; then
      echo "[SessionStart] ⚡ Sage activé — budget à ${PERCENTAGE}%"
      echo "[SessionStart] Suggestion : décharger les agents inactifs"
    fi
  fi
fi

echo "[SessionStart] ✅ Session #$SESSION_COUNT ready."
