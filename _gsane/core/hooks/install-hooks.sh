#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# GSANE — Git hooks installer
# ═══════════════════════════════════════════════════════════════════════════════
#
# Links GSANE hooks into .git/hooks/ for the current repository.
# Safe to run multiple times (idempotent).
#
# Usage:
#   bash _gsane/core/hooks/install-hooks.sh
#
# Hooks installed:
#   pre-commit  → pre-commit-cc.sh   (CC PASS warning on GSANE artifacts)
#   commit-msg  → commit-msg.sh      (Conventional Commits validation)
#   pre-push    → pre-push.sh        (Blocks direct push to main)
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

GIT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
    echo "❌ Pas dans un repository git. Exécuter depuis la racine du projet."
    exit 1
}

HOOKS_SRC="$GIT_ROOT/_gsane/core/hooks"
HOOKS_DST="$GIT_ROOT/.git/hooks"

if [[ ! -d "$HOOKS_SRC" ]]; then
    echo "❌ Dossier _gsane/core/hooks/ introuvable."
    exit 1
fi

echo ""
echo "🧙 GSANE — Installation des git hooks"
echo "   Source  : $HOOKS_SRC"
echo "   Dest    : $HOOKS_DST"
echo ""

install_hook() {
    local src_file="$1"
    local hook_name="$2"
    local src_path="$HOOKS_SRC/$src_file"
    local dst_path="$HOOKS_DST/$hook_name"

    if [[ ! -f "$src_path" ]]; then
        echo "   ⚠️  Source introuvable : $src_file — ignoré"
        return
    fi

    # Backup existing hook if it's not already a GSANE hook
    if [[ -f "$dst_path" ]] && ! grep -q "GSANE" "$dst_path" 2>/dev/null; then
        cp "$dst_path" "${dst_path}.backup"
        echo "   📦 Hook existant sauvegardé : ${hook_name}.backup"
    fi

    cp "$src_path" "$dst_path"
    chmod +x "$dst_path"
    echo "   ✅ $hook_name installé"
}

install_hook "pre-commit-cc.sh"  "pre-commit"
install_hook "commit-msg.sh"     "commit-msg"
install_hook "pre-push.sh"       "pre-push"

echo ""
echo "✅ GSANE git hooks installés avec succès."
echo ""
echo "   Pour désinstaller : rm .git/hooks/pre-commit .git/hooks/commit-msg .git/hooks/pre-push"
echo ""
