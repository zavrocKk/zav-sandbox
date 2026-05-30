#!/usr/bin/env pwsh
# PreToolUse hook (opt-in) — flags destructive commands for confirmation.
# Reads the hook payload on stdin, scans for dangerous patterns, and asks for
# user confirmation (permissionDecision: ask) instead of letting the agent
# auto-run them. It NEVER executes the command — it only inspects and reports.
# Aligns with the Agentic Team safety policy (copilot-instructions.md).
$ErrorActionPreference = 'Stop'
$raw = [Console]::In.ReadToEnd()

$patterns = @(
    'rm\s+-rf',
    'git\s+push\s+.*--force',
    'git\s+push\s+.*\s-f(\s|$)',
    'git\s+reset\s+--hard',
    '--no-verify',
    'DROP\s+TABLE',
    'DROP\s+DATABASE',
    'TRUNCATE\s+TABLE',
    'terraform\s+destroy',
    'kubectl\s+delete'
)

foreach ($p in $patterns) {
    if ($raw -imatch $p) {
        $reason = "Destructive pattern detected ($p). Confirmation required before execution (Agentic Team safety policy)."
        $out = @{
            hookSpecificOutput = @{
                hookEventName            = 'PreToolUse'
                permissionDecision       = 'ask'
                permissionDecisionReason = $reason
            }
        } | ConvertTo-Json -Depth 5 -Compress
        Write-Output $out
        exit 0
    }
}

# No dangerous pattern — stay silent, allow normal flow.
exit 0
