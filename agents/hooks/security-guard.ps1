#!/usr/bin/env pwsh
# PreToolUse hook (opt-in) -- flags destructive commands for confirmation.
# Reads the hook payload on stdin, scans for dangerous patterns, and asks for
# user confirmation (permissionDecision: ask) instead of letting the agent
# auto-run them. It NEVER executes the command -- it only inspects and reports.
# Aligns with the Agentic Team safety policy (copilot-instructions.md).
#
# Each rule carries a static, ASCII-only safe-alternative hint (ported from the
# awesome-copilot Tool Guardian hook). Only the rule's hint is surfaced -- the
# matched command text is NEVER echoed back (no injection surface, no context
# pollution). On the first match the hook asks for confirmation and stops.
$ErrorActionPreference = 'Stop'
$raw = [Console]::In.ReadToEnd()

# Ordered rules: @{ Rx = <regex> ; Msg = <safe-alternative hint, ASCII only> }
$rules = @(
    @{ Rx = 'rm\s+-rf'; Msg = 'rm -rf (recursive delete): target specific paths, or mv to back up first' },
    @{ Rx = '(rm|del|unlink)\b.*\.env'; Msg = 'removing a .env file: back it up with mv before deleting' },
    @{ Rx = '(rm|del|unlink)\b.*\.git($|[^A-Za-z])'; Msg = 'deleting the .git directory: use git commands to manage repo state' },
    @{ Rx = 'git\s+push\s+.*--force'; Msg = 'force push: use git push --force-with-lease, or push to a feature branch' },
    @{ Rx = 'git\s+push\s+.*\s-f(\s|$)'; Msg = 'force push: use git push --force-with-lease, or push to a feature branch' },
    @{ Rx = 'git\s+reset\s+--hard'; Msg = 'hard reset: use git stash or git reset --soft to preserve changes' },
    @{ Rx = 'git\s+clean\s+-\w*f'; Msg = 'git clean: run git clean -n (dry run) first to preview deletions' },
    @{ Rx = '--no-verify'; Msg = 'bypassing git hooks (--no-verify): run the checks instead of skipping them' },
    @{ Rx = 'chmod\s+(-R\s+)?777'; Msg = 'chmod 777 (world-writable): use 755 for dirs, 644 for files' },
    @{ Rx = 'DROP\s+TABLE'; Msg = 'DROP TABLE: use a migration with rollback support' },
    @{ Rx = 'DROP\s+DATABASE'; Msg = 'DROP DATABASE: take a backup first; consider revoking DROP privileges' },
    @{ Rx = 'TRUNCATE\s+TABLE'; Msg = 'TRUNCATE: prefer DELETE FROM ... WHERE for safer removal' },
    @{ Rx = 'DELETE\s+FROM\s+[A-Za-z0-9_.]+\s*;'; Msg = 'DELETE without WHERE: add a WHERE clause to avoid deleting all rows' },
    @{ Rx = 'curl\b.*\|\s*(ba)?sh'; Msg = 'curl | sh (remote exec): download, review, then run the script' },
    @{ Rx = 'wget\b.*\|\s*(ba)?sh'; Msg = 'wget | sh (remote exec): download, review, then run the script' },
    @{ Rx = 'curl\b.*--data\b.*@'; Msg = 'curl --data @file (upload): review what is being sent first' },
    @{ Rx = 'terraform\s+destroy'; Msg = 'terraform destroy: run terraform plan -destroy first and confirm scope' },
    @{ Rx = 'kubectl\s+delete'; Msg = 'kubectl delete: double-check namespace/resource; consider --dry-run' },
    @{ Rx = 'sudo\s'; Msg = 'sudo (privilege escalation): run with least privilege needed' },
    @{ Rx = 'npm\s+publish'; Msg = 'npm publish: run npm publish --dry-run first to verify contents' }
)

foreach ($rule in $rules) {
    if ($raw -imatch $rule.Rx) {
        $reason = "Destructive pattern detected -- $($rule.Msg). Confirmation required before execution (Agentic Team safety policy)."
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

# No dangerous pattern -- stay silent, allow normal flow.
exit 0
