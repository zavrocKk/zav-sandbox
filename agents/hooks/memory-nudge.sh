#!/usr/bin/env bash
# PreCompact / Stop hook (opt-in) -- reminds to write a memory checkpoint.
# Emits a non-blocking systemMessage nudging the user to run /checkpoint so the
# current thread state is saved in docs/_scratch/memory/ before context is lost.
# Does NOT block the agent -- zero risk of loops or extra premium requests.
#
# Note encodage : les accents et apostrophes sont intentionnellement omis dans le
# systemMessage. Raison : la valeur JSON est produite via printf sur stdout et
# transmise a VS Code. Sur certains systemes (macOS, WSL, locales non-UTF-8),
# les caracteres multi-octets peuvent corrompre le JSON. ASCII pur = robustesse
# maximale sans dependance a la locale.
set -euo pipefail
cat > /dev/null
# Le rappel "journal de session" est temporaire : a retirer quand le test terrain
# (docs/_scratch/2026-07-01-plan-job-test-protocol.md) sera clos.
printf '{"systemMessage":"Memoire persistante : pense a /checkpoint pour sauver l etat du fil dans docs/_scratch/memory/ avant de perdre du contexte. Test terrain en cours : logue la session (tours / confirmations / routage) dans le journal section 4 de docs/_scratch/2026-07-01-plan-job-test-protocol.md."}'
exit 0
