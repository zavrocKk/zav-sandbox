#!/usr/bin/env bash
# PreCompact / Stop hook (opt-in) — reminds to write a memory checkpoint.
# Emits a non-blocking systemMessage nudging the user to run /checkpoint so the
# current thread state is saved in docs/_scratch/memory/ before context is lost.
# Does NOT block the agent — zero risk of loops or extra premium requests.
set -euo pipefail
cat > /dev/null
printf '{"systemMessage":"Memoire persistante : pense a /checkpoint pour sauver l etat du fil dans docs/_scratch/memory/ avant de perdre du contexte."}'
exit 0
