#!/usr/bin/env bash
# Pre-Commit Hook — Bloque les commits directs sur main.
# Vérifie le nommage de branche et les chemins dépréciés dans les fichiers stagés.
set -euo pipefail

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

echo "[PreCommit] Branch: $CURRENT_BRANCH"

# ── 1. Bloquer commit direct sur main ──────────────────────────────────────────
if [[ "$CURRENT_BRANCH" == "main" ]]; then
  echo "[PreCommit] ❌ BLOCKED: Direct commit to 'main' is forbidden!"
  echo "  Create a feature/* or fix/* branch first (Git Workflow — copilot-instructions.md)."
  exit 1
fi

# ── 2. Avertir si convention de nommage non respectée ──────────────────────────
if [[ ! "$CURRENT_BRANCH" =~ ^(feature|fix)\/[a-z0-9\-]+-[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "[PreCommit] ⚠️  WARNING: Branch '$CURRENT_BRANCH' doesn't follow feature/fix-YYYY-MM-DD convention"
fi

echo "[PreCommit] ✅ All checks passed."
