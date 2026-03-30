#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# GSANE — Git pre-commit hook : Completion Contract guard
# ═══════════════════════════════════════════════════════════════════════════════
#
# Warns (does NOT block) if GSANE artifacts are staged but CC has not been
# logged as PASS in _gsane-output/ for the current session.
#
# Philosophy: soft gate — warn, log, let the developer override consciously.
# Hard blocks belong to CI, not local hooks.
#
# Installation: bash _gsane/core/hooks/install-hooks.sh
# ═══════════════════════════════════════════════════════════════════════════════

set -uo pipefail

GIT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0

# Only active in a GSANE project
[[ -d "$GIT_ROOT/_gsane" ]] || exit 0

# GSANE artifact extensions / paths to watch
GSANE_PATTERNS="^_gsane/|^\.github/"

STAGED=$(git diff --cached --name-only 2>/dev/null || true)
if ! echo "$STAGED" | grep -qE "$GSANE_PATTERNS"; then
    exit 0  # No GSANE files staged — skip
fi

GSANE_STAGED_COUNT=$(echo "$STAGED" | grep -cE "$GSANE_PATTERNS" || true)

echo ""
echo "🧙 GSANE pre-commit — ${GSANE_STAGED_COUNT} artefact(s) GSANE staté(s)"

# Check if a CC PASS was logged today in _gsane-output/
TODAY=$(date +%Y-%m-%d)
CC_LOG="$GIT_ROOT/_gsane-output/session-distillate-${TODAY}.md"
CC_PASS_FOUND=false

if [[ -f "$CC_LOG" ]] && grep -q "\[CC\].*PASS\|CC PASS" "$CC_LOG" 2>/dev/null; then
    CC_PASS_FOUND=true
fi

# Also check session-analysis-log.md for today's CC PASS
SESSION_LOG="$GIT_ROOT/_gsane/_memory/session-analysis-log.md"
if [[ -f "$SESSION_LOG" ]] && grep -A5 "$TODAY" "$SESSION_LOG" 2>/dev/null | grep -q "CC.*PASS\|PASS.*CC"; then
    CC_PASS_FOUND=true
fi

if [[ "$CC_PASS_FOUND" == "false" ]]; then
    echo ""
    echo "⚠️  Aucun CC PASS détecté pour aujourd'hui ($TODAY)."
    echo "   Conseil : lancer [CC] dans Gsane Master avant de committer des artefacts GSANE."
    echo "   Pour ignorer : git commit --no-verify  (déconseillé)"
    echo ""
    # Warn only — do NOT exit 1 (developer decides)
fi

exit 0
