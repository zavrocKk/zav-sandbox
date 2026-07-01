#!/usr/bin/env bash
# PostToolUse / SubagentStart / SubagentStop observer hook (opt-in).
#
# Pattern: pure OBSERVER. Appends a single JSONL metadata line to a local,
# gitignored telemetry log so you can track agent activity, tool usage and
# subagent lifecycle. It NEVER blocks the agent, NEVER emits decision/permission
# output, and NEVER logs prompt or command content (privacy/security): only a
# timestamp, the event name and the payload byte size are recorded.
#
# The event name is passed as a trusted argument from hooks.json (not parsed from
# the payload), so there is no injection surface. All logic is wrapped so a
# telemetry failure can never affect the main flow. Dependency-free (no jq).
#
# IMPORTANT: no `set -e` here on purpose — the observer must never fail the flow.
set -uo pipefail

EVENT="${1:-unknown}"
# Keep the event label to a safe charset.
EVENT="$(printf '%s' "$EVENT" | tr -cd 'A-Za-z0-9_.-')"

{
  payload="$(cat)"
  bytes=${#payload}

  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  log_dir="$script_dir/../../docs/_scratch/telemetry"
  mkdir -p "$log_dir" 2>/dev/null || true
  log_file="$log_dir/agent-telemetry.jsonl"

  # Size-based rotation: keep a single .1 backup, cap the live log at ~1 MB.
  # Best-effort — never blocks the observer.
  max_bytes=1048576
  if [ -f "$log_file" ]; then
    size=$(wc -c < "$log_file" 2>/dev/null || echo 0)
    if [ "${size:-0}" -ge "$max_bytes" ]; then
      mv -f "$log_file" "$log_file.1" 2>/dev/null || true
    fi
  fi

  ts="$(date -u +%Y-%m-%dT%H:%M:%S.000Z 2>/dev/null || echo unknown)"
  printf '{"ts":"%s","event":"%s","payloadBytes":%s}\n' "$ts" "$EVENT" "$bytes" \
    >> "$log_file"
} 2>/dev/null || true

exit 0
