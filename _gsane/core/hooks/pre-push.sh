#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# GSANE — Git pre-push hook : branch protection guard
# ═══════════════════════════════════════════════════════════════════════════════
#
# Blocks any direct push to 'main' branch.
# GSANE governance rule: NEVER commit directly to main.
#
# Installation: bash _gsane/core/hooks/install-hooks.sh
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

GIT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[[ -d "$GIT_ROOT/_gsane" ]] || exit 0

PROTECTED_BRANCH="main"
CURRENT_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo '')"

if [[ "$CURRENT_BRANCH" == "$PROTECTED_BRANCH" ]]; then
    echo ""
    echo "🚫 GSANE pre-push : push direct sur 'main' interdit"
    echo ""
    echo "   Règle GSANE : toujours travailler sur une branche feature/* ou fix/*"
    echo "   Étapes :"
    echo "     1. git checkout -b feature/<description>-$(date +%Y-%m-%d)"
    echo "     2. git cherry-pick <commits> ou recommencer les changements"
    echo "     3. git push origin <nouvelle-branche>"
    echo "     4. Créer une PR sur GitHub"
    echo ""
    echo "   Workflow complet : _gsane/core/workflows/git-workflow/workflow.md"
    echo ""
    exit 1
fi

exit 0
