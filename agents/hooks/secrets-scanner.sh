#!/usr/bin/env bash
# Stop hook (opt-in) -- scans files modified during the session for leaked secrets.
#
# Pattern: WARN-ONLY, FAIL-OPEN post-processing guard. On session end it inspects
# files changed vs HEAD (plus untracked files) against ~25 secret patterns and, on
# a finding, appends a REDACTED JSONL record to the local, gitignored telemetry log
# and emits a single non-blocking systemMessage. It NEVER blocks the agent, NEVER
# exits non-zero, and NEVER re-exposes a secret in the chat (matches truncated to
# first4...last4). Dependency-free: uses only git + grep (no jq, no `file`).
#
# IMPORTANT: no `set -e` here on purpose -- the guard must never fail the flow.
# Text detection uses `grep -I` (skips binary). Detection is case-sensitive; the
# placeholder filter is case-insensitive. ASCII-only output for locale robustness.
set -uo pipefail

{
  cat > /dev/null  # drain stdin; payload content is not used

  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  repo_root="$(cd "$script_dir/../.." && pwd)"

  # Only run inside a git work tree.
  if ! git -C "$repo_root" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    exit 0
  fi

  # Collect modified files (added/copied/modified/renamed vs HEAD) + untracked.
  files=()
  while IFS= read -r f; do [ -n "$f" ] && files+=("$f"); done < <(
    git -C "$repo_root" diff --name-only --diff-filter=ACMR HEAD 2>/dev/null \
      || git -C "$repo_root" diff --name-only --diff-filter=ACMR 2>/dev/null
  )
  while IFS= read -r f; do [ -n "$f" ] && files+=("$f"); done < <(
    git -C "$repo_root" ls-files --others --exclude-standard 2>/dev/null
  )

  # De-duplicate and cap to 300 files.
  if [ "${#files[@]}" -gt 0 ]; then
    mapfile -t files < <(printf '%s\n' "${files[@]}" | awk '!seen[$0]++' | head -n 300)
  fi

  # "NAME:::SEVERITY:::REGEX" -- ::: delimiter avoids clashes with regex pipes.
  PATTERNS=(
    "AWS_ACCESS_KEY:::critical:::AKIA[0-9A-Z]{16}"
    "AWS_SECRET_KEY:::critical:::aws_secret_access_key[[:space:]]*[:=][[:space:]]*['\"]?[A-Za-z0-9/+=]{40}"
    "GCP_SERVICE_ACCOUNT:::critical:::\"type\"[[:space:]]*:[[:space:]]*\"service_account\""
    "GCP_API_KEY:::high:::AIza[0-9A-Za-z_-]{35}"
    "AZURE_CLIENT_SECRET:::critical:::azure[_-]?client[_-]?secret[[:space:]]*[:=][[:space:]]*['\"]?[A-Za-z0-9_~.-]{34,}"
    "GITHUB_PAT:::critical:::ghp_[0-9A-Za-z]{36}"
    "GITHUB_OAUTH:::critical:::gho_[0-9A-Za-z]{36}"
    "GITHUB_APP_TOKEN:::critical:::ghs_[0-9A-Za-z._-]{36,}"
    "GITHUB_REFRESH_TOKEN:::critical:::ghr_[0-9A-Za-z]{36}"
    "GITHUB_FINE_GRAINED_PAT:::critical:::github_pat_[0-9A-Za-z_]{82}"
    "PRIVATE_KEY:::critical:::-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"
    "PGP_PRIVATE_BLOCK:::critical:::-----BEGIN PGP PRIVATE KEY BLOCK-----"
    "GENERIC_SECRET:::high:::(secret|token|password|passwd|pwd|api[_-]?key|apikey|access[_-]?key|auth[_-]?token|client[_-]?secret)[[:space:]]*[:=][[:space:]]*['\"]?[A-Za-z0-9_/+=~.-]{8,}"
    "CONNECTION_STRING:::high:::(mongodb(\\+srv)?|postgres(ql)?|mysql|redis|amqp|mssql)://[^[:space:]'\"]{10,}"
    "BEARER_TOKEN:::medium:::[Bb]earer[[:space:]]+[A-Za-z0-9_-]{20,}\\.[A-Za-z0-9_-]{20,}"
    "SLACK_TOKEN:::high:::xox[baprs]-[0-9]{10,}-[0-9A-Za-z-]+"
    "SLACK_WEBHOOK:::high:::https://hooks\\.slack\\.com/services/T[0-9A-Z]{8,}/B[0-9A-Z]{8,}/[0-9A-Za-z]{24}"
    "DISCORD_TOKEN:::high:::[MN][A-Za-z0-9]{23,}\\.[A-Za-z0-9_-]{6}\\.[A-Za-z0-9_-]{27,}"
    "TWILIO_API_KEY:::high:::SK[0-9a-fA-F]{32}"
    "SENDGRID_API_KEY:::high:::SG\\.[0-9A-Za-z_-]{22}\\.[0-9A-Za-z_-]{43}"
    "STRIPE_SECRET_KEY:::critical:::sk_live_[0-9A-Za-z]{24,}"
    "STRIPE_RESTRICTED_KEY:::high:::rk_live_[0-9A-Za-z]{24,}"
    "NPM_TOKEN:::high:::npm_[0-9A-Za-z]{36}"
    "JWT_TOKEN:::medium:::eyJ[A-Za-z0-9_-]{10,}\\.eyJ[A-Za-z0-9_-]{10,}\\.[A-Za-z0-9_-]{10,}"
  )

  json_escape() { printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'; }

  FINDINGS=()
  FINDING_COUNT=0
  MAX_FINDINGS=100

  for rel in "${files[@]}"; do
    [ "$FINDING_COUNT" -ge "$MAX_FINDINGS" ] && break
    full="$repo_root/$rel"
    [ -f "$full" ] || continue

    # Skip large files (> 1 MB) and lock files.
    size=$(wc -c < "$full" 2>/dev/null || echo 0)
    [ "${size:-0}" -gt 1048576 ] && continue
    case "$rel" in
      *.lock|*.sum|package-lock.json|yarn.lock|pnpm-lock.yaml) continue ;;
      */secrets-scanner.ps1|*/secrets-scanner.sh|secrets-scanner.ps1|secrets-scanner.sh) continue ;;
    esac
    # Skip binary files (grep -I -> no match on binary).
    grep -Iq . "$full" 2>/dev/null || continue

    for entry in "${PATTERNS[@]}"; do
      [ "$FINDING_COUNT" -ge "$MAX_FINDINGS" ] && break
      name="${entry%%:::*}"
      rest="${entry#*:::}"
      severity="${rest%%:::*}"
      regex="${rest#*:::}"

      while IFS=: read -r line_num matched_line; do
        [ -z "${line_num:-}" ] && continue
        match=$(printf '%s\n' "$matched_line" | grep -oE "$regex" 2>/dev/null | head -1)
        [ -z "$match" ] && continue
        # Drop obvious placeholders / example values.
        if printf '%s\n' "$match" | grep -qiE '(example|placeholder|your[_-]|xxx|changeme|todo|fixme|replace[_-]?me|dummy|fake|test[_-]?key|sample)'; then
          continue
        fi
        # Redact: first 4 + last 4 chars.
        if [ "${#match}" -le 12 ]; then
          redacted="[REDACTED]"
        else
          redacted="${match:0:4}...${match: -4}"
        fi
        FINDINGS+=("$(json_escape "$rel")	$line_num	$name	$severity	$(json_escape "$redacted")")
        FINDING_COUNT=$((FINDING_COUNT + 1))
        [ "$FINDING_COUNT" -ge "$MAX_FINDINGS" ] && break
      done < <(grep -nE "$regex" "$full" 2>/dev/null || true)
    done
  done

  # --- Log (JSONL, gitignored, rotated like agent-telemetry) ---
  log_dir="$repo_root/docs/_scratch/telemetry"
  mkdir -p "$log_dir" 2>/dev/null || true
  log_file="$log_dir/secrets-scan.jsonl"
  if [ -f "$log_file" ]; then
    lsize=$(wc -c < "$log_file" 2>/dev/null || echo 0)
    if [ "${lsize:-0}" -ge 1048576 ]; then
      mv -f "$log_file" "$log_file.1" 2>/dev/null || true
    fi
  fi

  ts="$(date -u +%Y-%m-%dT%H:%M:%S.000Z 2>/dev/null || echo unknown)"
  status="clean"
  [ "$FINDING_COUNT" -gt 0 ] && status="findings"

  findings_json="["
  first=true
  for finding in "${FINDINGS[@]}"; do
    IFS=$'\t' read -r fpath fline pname psev fred <<< "$finding"
    [ "$first" != "true" ] && findings_json+=","
    first=false
    findings_json+="{\"file\":\"$fpath\",\"line\":$fline,\"pattern\":\"$pname\",\"severity\":\"$psev\",\"match\":\"$fred\"}"
  done
  findings_json+="]"

  printf '{"ts":"%s","event":"secrets_scan","status":"%s","filesScanned":%d,"findingCount":%d,"findings":%s}\n' \
    "$ts" "$status" "${#files[@]}" "$FINDING_COUNT" "$findings_json" >> "$log_file"

  # --- Non-blocking chat signal (only on findings; no secret re-exposed) ---
  if [ "$FINDING_COUNT" -gt 0 ]; then
    printf '{"systemMessage":"Secrets scan: %d potential secret(s) across %d modified file(s). Redacted details in docs/_scratch/telemetry/secrets-scan.jsonl. Review before commit."}' \
      "$FINDING_COUNT" "${#files[@]}"
  fi
} 2>/dev/null || true

exit 0
