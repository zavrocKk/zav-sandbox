#!/usr/bin/env pwsh
# Stop hook (opt-in) -- scans files modified during the session for leaked secrets.
#
# Pattern: WARN-ONLY, FAIL-OPEN post-processing guard. When the agent session ends
# it inspects the files changed vs HEAD (plus untracked files) against ~25 secret
# patterns (cloud keys, PATs, private keys, connection strings, JWTs...). On a
# finding it appends a REDACTED JSONL record to the local, gitignored telemetry log
# and emits a single non-blocking systemMessage. It NEVER blocks the agent, NEVER
# exits non-zero, and NEVER re-exposes a secret in the chat (matches are truncated
# to first4...last4). A scan failure can never affect the main flow.
#
# Detection is case-sensitive (mirrors the upstream grep -E behaviour); the
# placeholder filter is case-insensitive to drop obvious example/fixture values.
#
# Note encodage : le JSONL et le systemMessage sont volontairement ASCII pur (pas
# d'accents) pour rester parseables quelle que soit la config PowerShell/locale.
param()

try {
    $null = [Console]::In.ReadToEnd()  # drain stdin; payload content is not used

    $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

    # Only run inside a git work tree.
    $inside = & git -C $repoRoot rev-parse --is-inside-work-tree 2>$null
    if ($LASTEXITCODE -ne 0 -or "$inside".Trim() -ne 'true') { exit 0 }

    # Collect modified files (added/copied/modified/renamed vs HEAD) + untracked.
    $changed = & git -C $repoRoot diff --name-only --diff-filter=ACMR HEAD 2>$null
    if ($LASTEXITCODE -ne 0) {
        $changed = & git -C $repoRoot diff --name-only --diff-filter=ACMR 2>$null
    }
    $untracked = & git -C $repoRoot ls-files --others --exclude-standard 2>$null
    $files = @(@($changed) + @($untracked) | Where-Object { $_ } | Select-Object -Unique)

    $maxFiles = 300
    if ($files.Count -gt $maxFiles) { $files = $files[0..($maxFiles - 1)] }

    # "NAME|SEVERITY|REGEX" -- edit to add/remove patterns.
    $defs = @(
        @('AWS_ACCESS_KEY', 'critical', 'AKIA[0-9A-Z]{16}'),
        @('AWS_SECRET_KEY', 'critical', 'aws_secret_access_key\s*[:=]\s*[''"]?[A-Za-z0-9/+=]{40}'),
        @('GCP_SERVICE_ACCOUNT', 'critical', '"type"\s*:\s*"service_account"'),
        @('GCP_API_KEY', 'high', 'AIza[0-9A-Za-z_-]{35}'),
        @('AZURE_CLIENT_SECRET', 'critical', 'azure[_-]?client[_-]?secret\s*[:=]\s*[''"]?[A-Za-z0-9_~.-]{34,}'),
        @('GITHUB_PAT', 'critical', 'ghp_[0-9A-Za-z]{36}'),
        @('GITHUB_OAUTH', 'critical', 'gho_[0-9A-Za-z]{36}'),
        @('GITHUB_APP_TOKEN', 'critical', 'ghs_[0-9A-Za-z._-]{36,}'),
        @('GITHUB_REFRESH_TOKEN', 'critical', 'ghr_[0-9A-Za-z]{36}'),
        @('GITHUB_FINE_GRAINED_PAT', 'critical', 'github_pat_[0-9A-Za-z_]{82}'),
        @('PRIVATE_KEY', 'critical', '-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----'),
        @('PGP_PRIVATE_BLOCK', 'critical', '-----BEGIN PGP PRIVATE KEY BLOCK-----'),
        @('GENERIC_SECRET', 'high', '(secret|token|password|passwd|pwd|api[_-]?key|apikey|access[_-]?key|auth[_-]?token|client[_-]?secret)\s*[:=]\s*[''"]?[A-Za-z0-9_/+=~.-]{8,}'),
        @('CONNECTION_STRING', 'high', '(mongodb(\+srv)?|postgres(ql)?|mysql|redis|amqp|mssql)://[^\s''"]{10,}'),
        @('BEARER_TOKEN', 'medium', '[Bb]earer\s+[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}'),
        @('SLACK_TOKEN', 'high', 'xox[baprs]-[0-9]{10,}-[0-9A-Za-z-]+'),
        @('SLACK_WEBHOOK', 'high', 'https://hooks\.slack\.com/services/T[0-9A-Z]{8,}/B[0-9A-Z]{8,}/[0-9A-Za-z]{24}'),
        @('DISCORD_TOKEN', 'high', '[MN][A-Za-z0-9]{23,}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27,}'),
        @('TWILIO_API_KEY', 'high', 'SK[0-9a-fA-F]{32}'),
        @('SENDGRID_API_KEY', 'high', 'SG\.[0-9A-Za-z_-]{22}\.[0-9A-Za-z_-]{43}'),
        @('STRIPE_SECRET_KEY', 'critical', 'sk_live_[0-9A-Za-z]{24,}'),
        @('STRIPE_RESTRICTED_KEY', 'high', 'rk_live_[0-9A-Za-z]{24,}'),
        @('NPM_TOKEN', 'high', 'npm_[0-9A-Za-z]{36}'),
        @('JWT_TOKEN', 'medium', 'eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}')
    )
    $patterns = foreach ($d in $defs) {
        [pscustomobject]@{ Name = $d[0]; Sev = $d[1]; Rx = [regex]::new($d[2]) }
    }
    $placeholder = [regex]::new('(example|placeholder|your[_-]|xxx|changeme|todo|fixme|replace[_-]?me|dummy|fake|test[_-]?key|sample)', 'IgnoreCase')

    $textExt = @('.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.cfg', '.conf',
        '.sh', '.bash', '.zsh', '.ps1', '.bat', '.cmd', '.py', '.rb', '.js', '.ts', '.jsx', '.tsx',
        '.go', '.rs', '.java', '.kt', '.cs', '.cpp', '.c', '.h', '.php', '.swift', '.scala', '.lua',
        '.pl', '.ex', '.exs', '.hs', '.ml', '.html', '.css', '.scss', '.less', '.svg', '.sql',
        '.graphql', '.proto', '.properties')
    $textNames = @('dockerfile', 'makefile', 'vagrantfile', 'gemfile', 'rakefile')

    $maxFindings = 100
    $findings = New-Object System.Collections.Generic.List[object]

    foreach ($rel in $files) {
        if ($findings.Count -ge $maxFindings) { break }
        $full = Join-Path $repoRoot $rel
        if (-not (Test-Path -LiteralPath $full -PathType Leaf)) { continue }
        $item = Get-Item -LiteralPath $full -ErrorAction SilentlyContinue
        if (-not $item -or $item.Length -gt 1MB) { continue }

        $name = $item.Name.ToLowerInvariant()
        if ($name -like '*.lock' -or $name -like '*.sum' -or
            $name -eq 'package-lock.json' -or $name -eq 'yarn.lock' -or $name -eq 'pnpm-lock.yaml' -or
            $name -eq 'secrets-scanner.ps1' -or $name -eq 'secrets-scanner.sh') {
            continue
        }
        $ext = $item.Extension.ToLowerInvariant()
        $isText = ($textExt -contains $ext) -or ($textNames -contains $name) -or ($name -like '.env*')
        if (-not $isText) { continue }

        $lines = @(Get-Content -LiteralPath $full -ErrorAction SilentlyContinue)
        if (-not $lines) { continue }

        for ($i = 0; $i -lt $lines.Count; $i++) {
            if ($findings.Count -ge $maxFindings) { break }
            $line = $lines[$i]
            if ([string]::IsNullOrEmpty($line)) { continue }
            foreach ($p in $patterns) {
                $m = $p.Rx.Match($line)
                if (-not $m.Success) { continue }
                $val = $m.Value
                if ($placeholder.IsMatch($val)) { continue }
                if ($val.Length -le 12) {
                    $red = '[REDACTED]'
                }
                else {
                    $red = $val.Substring(0, 4) + '...' + $val.Substring($val.Length - 4)
                }
                $findings.Add([pscustomobject]@{
                        file     = $rel
                        line     = $i + 1
                        pattern  = $p.Name
                        severity = $p.Sev
                        match    = $red
                    })
                if ($findings.Count -ge $maxFindings) { break }
            }
        }
    }

    # --- Log (JSONL, gitignored, rotated like agent-telemetry) ---
    $logDir = Join-Path $PSScriptRoot '..\..\docs\_scratch\telemetry'
    if (-not (Test-Path -LiteralPath $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    $logFile = Join-Path $logDir 'secrets-scan.jsonl'
    $maxBytes = 1MB
    if ((Test-Path -LiteralPath $logFile) -and ((Get-Item -LiteralPath $logFile).Length -ge $maxBytes)) {
        $backup = "$logFile.1"
        if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Force }
        Move-Item -LiteralPath $logFile -Destination $backup -Force
    }

    $ts = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ')
    $status = if ($findings.Count -gt 0) { 'findings' } else { 'clean' }

    # Build JSON manually (ASCII-safe, no ordered-dict quirks). pattern/severity
    # come from the trusted table; match is already redacted; only file needs escaping.
    $esc = {
        param($s)
        if ($null -eq $s) { return '""' }
        '"' + ($s -replace '\\', '\\' -replace '"', '\"') + '"'
    }
    $items = foreach ($f in $findings) {
        '{"file":' + (& $esc $f.file) + ',"line":' + $f.line +
        ',"pattern":"' + $f.pattern + '","severity":"' + $f.severity +
        '","match":' + (& $esc $f.match) + '}'
    }
    $findingsJson = '[' + ($items -join ',') + ']'
    $recordLine = '{"ts":"' + $ts + '","event":"secrets_scan","status":"' + $status +
    '","filesScanned":' + $files.Count + ',"findingCount":' + $findings.Count +
    ',"findings":' + $findingsJson + '}'
    Add-Content -LiteralPath $logFile -Value $recordLine -Encoding utf8

    # --- Non-blocking chat signal (only on findings; no secret re-exposed) ---
    if ($findings.Count -gt 0) {
        $msg = "Secrets scan: $($findings.Count) potential secret(s) across $($files.Count) modified file(s). Redacted details in docs/_scratch/telemetry/secrets-scan.jsonl. Review before commit."
        (@{ systemMessage = $msg } | ConvertTo-Json -Compress) | Write-Output
    }
}
catch {
    # Fail-open: a scan failure must never affect the agent flow.
}

exit 0
