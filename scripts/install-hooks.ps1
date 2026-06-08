# Install git hooks from scripts/hooks/ into .git/hooks/

# Verify we are inside a git repository
try {
    git rev-parse --is-inside-work-tree | Out-Null
} catch {
    Write-Host "Error: not inside a git repository." -ForegroundColor Red
    exit 1
}

$gitRoot = git rev-parse --show-toplevel
$hooksDir = Join-Path $gitRoot "scripts" "hooks"
$gitHooksDir = Join-Path $gitRoot ".git" "hooks"

if (-not (Test-Path $hooksDir)) {
    Write-Host "Error: hooks directory not found at $hooksDir" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $gitHooksDir)) {
    Write-Host "Error: git hooks directory not found at $gitHooksDir" -ForegroundColor Red
    exit 1
}

Get-ChildItem -Path $hooksDir | ForEach-Object {
    $name = $_.Name
    $source = $_.FullName
    $dest = Join-Path $gitHooksDir $name

    Copy-Item -Path $source -Destination $dest -Force

    # Make it executable (on Windows this is implicit for files in .git/hooks/)
    # On Unix-like systems via WSL, we'd need to chmod +x, but that's handled by git

    Write-Host "Installed hook: $name"
}

Write-Host "All hooks installed." -ForegroundColor Green
