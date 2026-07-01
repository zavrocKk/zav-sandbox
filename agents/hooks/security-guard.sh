#!/usr/bin/env bash
# PreToolUse hook (opt-in) -- flags destructive commands for confirmation.
# Scans the hook payload on stdin for dangerous patterns and asks for user
# confirmation instead of letting the agent auto-run them. Never executes the
# command -- only inspects and reports. Dependency-free (no jq required).
#
# Each rule carries a static, ASCII-only safe-alternative hint (ported from the
# awesome-copilot Tool Guardian hook). Only the rule's hint is surfaced -- the
# matched command text is NEVER echoed back. Patterns use [[:space:]] (not \s) and
# avoid \b for grep -E portability across GNU/BSD.
set -euo pipefail
raw="$(cat)"

# "REGEX:::MESSAGE" -- ::: delimiter avoids clashes with regex pipe characters.
rules=(
  "rm[[:space:]]+-rf:::rm -rf (recursive delete): target specific paths, or mv to back up first"
  "(rm|del|unlink)[[:space:]].*\\.env:::removing a .env file: back it up with mv before deleting"
  "(rm|del|unlink)[[:space:]].*\\.git($|[^A-Za-z]):::deleting the .git directory: use git commands to manage repo state"
  "git[[:space:]]+push[[:space:]].*--force:::force push: use git push --force-with-lease, or push to a feature branch"
  "git[[:space:]]+push[[:space:]].*-f([[:space:]]|$):::force push: use git push --force-with-lease, or push to a feature branch"
  "git[[:space:]]+reset[[:space:]]+--hard:::hard reset: use git stash or git reset --soft to preserve changes"
  "git[[:space:]]+clean[[:space:]]+-[a-z]*f:::git clean: run git clean -n (dry run) first to preview deletions"
  "--no-verify:::bypassing git hooks (--no-verify): run the checks instead of skipping them"
  "chmod[[:space:]]+(-R[[:space:]]+)?777:::chmod 777 (world-writable): use 755 for dirs, 644 for files"
  "DROP[[:space:]]+TABLE:::DROP TABLE: use a migration with rollback support"
  "DROP[[:space:]]+DATABASE:::DROP DATABASE: take a backup first; consider revoking DROP privileges"
  "TRUNCATE[[:space:]]+TABLE:::TRUNCATE: prefer DELETE FROM ... WHERE for safer removal"
  "DELETE[[:space:]]+FROM[[:space:]]+[A-Za-z0-9_.]+[[:space:]]*;:::DELETE without WHERE: add a WHERE clause to avoid deleting all rows"
  "curl.*\\|[[:space:]]*(ba)?sh:::curl | sh (remote exec): download, review, then run the script"
  "wget.*\\|[[:space:]]*(ba)?sh:::wget | sh (remote exec): download, review, then run the script"
  "curl.*--data.*@:::curl --data @file (upload): review what is being sent first"
  "terraform[[:space:]]+destroy:::terraform destroy: run terraform plan -destroy first and confirm scope"
  "kubectl[[:space:]]+delete:::kubectl delete: double-check namespace/resource; consider --dry-run"
  "sudo[[:space:]]:::sudo (privilege escalation): run with least privilege needed"
  "npm[[:space:]]+publish:::npm publish: run npm publish --dry-run first to verify contents"
)

for entry in "${rules[@]}"; do
  regex="${entry%%:::*}"
  msg="${entry#*:::}"
  if printf '%s' "$raw" | grep -iEq -e "$regex"; then
    printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Destructive pattern detected -- %s. Confirmation required before execution (Agentic Team safety policy)."}}' "$msg"
    exit 0
  fi
done

exit 0
