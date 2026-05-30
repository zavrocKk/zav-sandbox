#!/usr/bin/env bash
# PreToolUse hook (opt-in) — flags destructive commands for confirmation.
# Scans the hook payload on stdin for dangerous patterns and asks for user
# confirmation instead of letting the agent auto-run them. Never executes the
# command — only inspects and reports. Dependency-free (no jq required).
set -euo pipefail
raw="$(cat)"

patterns='rm[[:space:]]+-rf|git[[:space:]]+push[[:space:]].*--force|git[[:space:]]+reset[[:space:]]+--hard|--no-verify|DROP[[:space:]]+TABLE|DROP[[:space:]]+DATABASE|TRUNCATE[[:space:]]+TABLE|terraform[[:space:]]+destroy|kubectl[[:space:]]+delete'

if printf '%s' "$raw" | grep -iEq "$patterns"; then
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Destructive pattern detected. Confirmation required before execution (Agentic Team safety policy)."}}'
fi

exit 0
