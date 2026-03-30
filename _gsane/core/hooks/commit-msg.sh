#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# GSANE — Git commit-msg hook : Conventional Commits validation
# ═══════════════════════════════════════════════════════════════════════════════
#
# Validates that commit messages follow Conventional Commits format when
# GSANE artifacts are involved.
#
# Mode: STRICT for _gsane/ changes (blocks), WARN for other files
#
# Format required: <type>(<scope>): <description>
# Types: feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert
#
# Installation: bash _gsane/core/hooks/install-hooks.sh
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

COMMIT_MSG_FILE="$1"
GIT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0

[[ -d "$GIT_ROOT/_gsane" ]] || exit 0

# Read message (strip comments and blank lines)
MSG=$(grep -v '^#' "$COMMIT_MSG_FILE" | sed '/^[[:space:]]*$/d' | head -1 || true)

# Minimum length
MIN_LEN=10
if [[ ${#MSG} -lt $MIN_LEN ]]; then
    echo ""
    echo "🚫 GSANE commit-msg : message trop court (${#MSG} chars, minimum ${MIN_LEN})"
    echo "   Message : \"$MSG\""
    echo ""
    exit 1
fi

# Conventional Commits pattern
CC_TYPES="feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert"
CC_PATTERN="^(${CC_TYPES})(\([a-zA-Z0-9_/-]+\))?(!)?: .{1,}"

# Check if GSANE artifacts are staged
STAGED=$(git diff --cached --name-only 2>/dev/null || true)
GSANE_STAGED=$(echo "$STAGED" | grep -cE "^_gsane/|^\.github/" || true)

if [[ "$GSANE_STAGED" -gt 0 ]]; then
    # STRICT mode for GSANE artifacts
    if ! echo "$MSG" | grep -qE "$CC_PATTERN"; then
        echo ""
        echo "🚫 GSANE commit-msg : format Conventional Commits requis pour les artefacts GSANE"
        echo "   Message   : \"$MSG\""
        echo "   Format    : <type>(<scope>): <description>"
        echo "   Types     : feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert"
        echo "   Exemples  :"
        echo "     feat(gsane-master): add context distillator prompt"
        echo "     fix(party-mode): resolve context overflow after round 5"
        echo "     chore(manifest): bump schema version to 2.0.0"
        echo ""
        echo "   Pour bypasser : git commit --no-verify  (déconseillé)"
        echo ""
        exit 1
    fi
else
    # WARN mode for non-GSANE files
    if ! echo "$MSG" | grep -qE "$CC_PATTERN"; then
        echo "💡 GSANE: message hors format Conventional Commits — pensez à prefixer avec feat:/fix:/chore: etc."
    fi
fi

exit 0
