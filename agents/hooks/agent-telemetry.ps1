#!/usr/bin/env pwsh
# PostToolUse / SubagentStart / SubagentStop observer hook (opt-in).
#
# Pattern: pure OBSERVER. It appends a single JSONL metadata line to a local,
# gitignored telemetry log so you can track agent activity, tool usage and
# subagent lifecycle for performance/state analysis. It NEVER blocks the agent,
# NEVER emits decision/permission output, and NEVER logs prompt or command
# content (privacy/security): only a timestamp, the event name and the payload
# byte size are recorded.
#
# The event name is passed as a trusted argument from hooks.json (not parsed from
# the payload), so there is no injection surface. Everything runs inside a
# try/catch and the script always exits 0 — a telemetry failure can never affect
# the main flow.
#
# Note encodage : le JSONL est volontairement ASCII pur (pas d'accents) pour rester
# parseable quelle que soit la config PowerShell/locale (cf. memory-nudge.ps1).
param([string]$EventName = 'unknown')

try {
    $payload = [Console]::In.ReadToEnd()
    $bytes = if ($payload) { [System.Text.Encoding]::UTF8.GetByteCount($payload) } else { 0 }

    $logDir = Join-Path $PSScriptRoot '..\..\docs\_scratch\telemetry'
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    $logFile = Join-Path $logDir 'agent-telemetry.jsonl'

    # Size-based rotation: keep a single .1 backup, cap the live log at ~1 MB.
    # Cheap (single stat) and best-effort — never blocks the observer.
    $maxBytes = 1MB
    if ((Test-Path -LiteralPath $logFile) -and ((Get-Item -LiteralPath $logFile).Length -ge $maxBytes)) {
        $backup = "$logFile.1"
        if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Force }
        Move-Item -LiteralPath $logFile -Destination $backup -Force
    }

    $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ')
    $safeEvent = ($EventName -replace '[^A-Za-z0-9_.-]', '')
    $line = '{"ts":"' + $ts + '","event":"' + $safeEvent + '","payloadBytes":' + $bytes + '}'

    Add-Content -LiteralPath $logFile -Value $line -Encoding utf8
}
catch {
    # Observer hook: never affect the agent flow. Swallow all errors silently.
}

exit 0
