#!/usr/bin/env pwsh
# PreCompact / Stop hook (opt-in) — reminds to write a memory checkpoint.
# Emits a non-blocking systemMessage nudging the user to run /checkpoint so the
# current thread state is saved in docs/_scratch/memory/ before context is lost.
# It does NOT block the agent (no decision: block) — zero risk of loops or extra
# premium requests.
$ErrorActionPreference = 'Stop'
$null = [Console]::In.ReadToEnd()
Write-Output '{"systemMessage":"Memoire persistante : pense a /checkpoint pour sauver l etat du fil dans docs/_scratch/memory/ avant de perdre du contexte."}'
exit 0
