#!/usr/bin/env pwsh
# PreCompact / Stop hook (opt-in) -- reminds to write a memory checkpoint.
# Emits a non-blocking systemMessage nudging the user to run /checkpoint so the
# current thread state is saved in docs/_scratch/memory/ before context is lost.
# It does NOT block the agent (no decision: block) -- zero risk of loops or extra
# premium requests.
#
# Note encodage : les accents et apostrophes sont intentionnellement omis dans le
# systemMessage. Raison : la valeur JSON est consommee par VS Code via stdout ; les
# encodages PowerShell (UTF-8 BOM, UTF-16) varient selon la version et la config
# systeme. Supprimer les caracteres non-ASCII garantit que le JSON reste parseable
# partout, independamment de la console ou du profil PowerShell actif.
$ErrorActionPreference = 'Stop'
$null = [Console]::In.ReadToEnd()
# Le rappel "journal de session" est temporaire : a retirer quand le test terrain
# (docs/_scratch/2026-07-01-plan-job-test-protocol.md) sera clos.
Write-Output '{"systemMessage":"Memoire persistante : pense a /checkpoint pour sauver l etat du fil dans docs/_scratch/memory/ avant de perdre du contexte. Test terrain en cours : logue la session (tours / confirmations / routage) dans le journal section 4 de docs/_scratch/2026-07-01-plan-job-test-protocol.md."}'
exit 0
