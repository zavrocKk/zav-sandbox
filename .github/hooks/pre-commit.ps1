$Branch = git rev-parse --abbrev-ref HEAD
if ($Branch -eq 'main') {
    Write-Host 'Error: Direct commits to main are forbidden.' -ForegroundColor Red
    exit 1
}

$StagedFiles = git diff --cached --name-only
foreach ($File in $StagedFiles) {
    if ($File.EndsWith('.md')) {
        $Content = Get-Content $File -Raw
        if ($Content -match '\{project-root\}') {
            Write-Host 'Error: Found {project-root} in ' $File '. This pseudo-variable is forbidden.' -ForegroundColor Red
            exit 1
        }
    }
}
exit 0
