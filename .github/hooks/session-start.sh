#!/usr/bin/env bash
# Session Start Hook — Initialise le contexte de session BMAD
set -euo pipefail

WORKSPACE_ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
echo "[SessionStart] Initializing BMAD agent session..."

# Vérifier la structure BMAD
if [[ ! -f "$WORKSPACE_ROOT/_bmad/core/config.yaml" ]]; then
  echo "[SessionStart] WARNING: _bmad/core/config.yaml not found"
fi

if [[ ! -f "$WORKSPACE_ROOT/_bmad/_config/agent-manifest.csv" ]]; then
  echo "[SessionStart] WARNING: agent-manifest.csv not found"
fi

# Vérifier la présence des agents
AGENT_COUNT=$(find "$WORKSPACE_ROOT/.github/agents" -name "*.agent.md" 2>/dev/null | wc -l)
echo "[SessionStart] Found $AGENT_COUNT agent(s)"

# Créer le dossier output si nécessaire
OUTPUT_DIR="${WORKSPACE_ROOT}/_bmad-output"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/bmb-creations"
mkdir -p "$OUTPUT_DIR/test-artifacts"

echo "[SessionStart] Session ready. Output path: $OUTPUT_DIR"
