#!/usr/bin/env bash
# Pre-Commit Hook — Bloque les commits directs sur main.
# Vérifie le nommage de branche, la syntaxe YAML récursive et les garde-fous sécurité locaux.
set -euo pipefail

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
PYTHON_CMD=()

resolve_python_cmd() {
  if command -v python3 >/dev/null 2>&1 && python3 -c "import sys" >/dev/null 2>&1; then
    PYTHON_CMD=(python3)
    return 0
  fi
  if command -v python >/dev/null 2>&1 && python -c "import sys" >/dev/null 2>&1; then
    PYTHON_CMD=(python)
    return 0
  fi
  if command -v py >/dev/null 2>&1 && py -3 -c "import sys" >/dev/null 2>&1; then
    PYTHON_CMD=(py -3)
    return 0
  fi
  return 1
}

echo "[PreCommit] Branch: $CURRENT_BRANCH"

if [[ "$CURRENT_BRANCH" == "main" ]]; then
  echo "[PreCommit] ❌ BLOCKED: Direct commit to 'main' is forbidden!"
  echo "  Create a feature/* or fix/* branch first (Git Workflow — copilot-instructions.md)."
  exit 1
fi

if [[ ! "$CURRENT_BRANCH" =~ ^(feature|fix)\/[a-z0-9\-]+-[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "[PreCommit] ⚠️  WARNING: Branch '$CURRENT_BRANCH' doesn't follow feature/fix-YYYY-MM-DD convention"
fi

if ! resolve_python_cmd; then
  echo "[PreCommit] ❌ Python introuvable : impossible d'exécuter la validation YAML et la gate sécurité locale."
  exit 1
fi

STAGED_FILES=$(git diff --cached --name-only)
if [[ -n "$STAGED_FILES" ]]; then
  BANNED_WORDS=("bmm" "bmad" "_tmad")
  for word in "${BANNED_WORDS[@]}"; do
    if echo "$STAGED_FILES" | xargs grep -ilw "$word" 2>/dev/null; then
      echo "[PreCommit] ❌ ÉCHEC : Le mot déprécié '$word' a été détecté dans les fichiers stagés."
      echo "  💡 Utilise des chemins relatifs ou des variables de projet régulières plutôt que d'anciens noms de modules."
      exit 1
    fi
  done
fi

echo "🔍 Vérification récursive de la syntaxe YAML..."
YAML_STATUS=0

if "${PYTHON_CMD[@]}" - <<'EOF'
from pathlib import Path
import sys

try:
    import yaml  # type: ignore[import]
except ImportError:
    sys.exit(42)

files = sorted(Path("_gsane/_config").rglob("*.yaml"))
if not files:
    sys.exit(1)

for file_path in files:
    with file_path.open(encoding='utf-8') as handle:
        yaml.safe_load(handle)
EOF
then
  YAML_STATUS=0
else
  PY_STATUS=$?
  if [[ "$PY_STATUS" -eq 42 ]]; then
    echo "[PreCommit] ❌ Le module Python 'yaml' est requis par la validation locale et la gate sécurité."
    echo "  Installe-le avec : python -m pip install pyyaml"
  else
    echo "[PreCommit] ❌ Validation YAML récursive impossible sur _gsane/_config/**."
  fi
  YAML_STATUS=1
fi

if [[ "$YAML_STATUS" -ne 0 ]]; then
  echo "❌ YAML invalide ! Interruption du commit."
  exit 1
fi
echo "✅ YAML valide sur _gsane/_config/**."

echo "🔍 Scan secrets sur le staging..."
"${PYTHON_CMD[@]}" _gsane/tools/security_gate.py scan-secrets --staged

echo "🔍 Bandit sur les fichiers Python stagés..."
"${PYTHON_CMD[@]}" _gsane/tools/security_gate.py run-bandit --staged

echo "[PreCommit] ✅ All checks passed."