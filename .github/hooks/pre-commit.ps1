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

$BannedWords = @('bmm', 'bmad', '_tmad')
foreach ($File in $StagedFiles) {
    if (Test-Path $File -PathType Leaf) {
        $Content = Get-Content $File -Raw
        foreach ($Word in $BannedWords) {
            if ($Content -match "\b$Word\b") {
                Write-Host "[PreCommit] ❌ ÉCHEC : Le mot déprécié '$Word' a été détecté dans le fichier stagé : $File" -ForegroundColor Red
                Write-Host "  💡 Utilise des chemins relatifs ou des variables de projet plutôt que d'anciens noms de modules." -ForegroundColor Yellow
                exit 1
            }
        }
    }
}


# ── 4. Validation des fichiers YAML (Prévention Crash Parser) ───────────────────
Write-Host "
🔍 Vérification de la syntaxe YAML..." -ForegroundColor Cyan
try {
    python -c "import yaml, sys, glob; [yaml.safe_load(open(f, encoding='utf-8')) for f in glob.glob('_gsane/_config/*.yaml')]" *>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "✅ YAML valide." -ForegroundColor Green
} catch {
    Write-Host "❌ YAML invalide ! Interruption du commit." -ForegroundColor Red
    exit 1
}
exit 0

