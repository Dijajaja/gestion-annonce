# Script rapide pour trouver gettext
$paths = @(
    "C:\Program Files\gettext\bin",
    "C:\gettext\bin",
    "$env:ProgramFiles\gettext\bin",
    "$env:LOCALAPPDATA\Programs\gettext\bin",
    "C:\Users\PC\Desktop\gettext\bin",
    "C:\Users\PC\Desktop\tools\gettext\bin",
    "C:\Users\PC\Desktop\soft\gettext\bin"
)

foreach ($path in $paths) {
    if (Test-Path "$path\msgfmt.exe") {
        Write-Host "Trouvé: $path" -ForegroundColor Green
        $env:PATH += ";$path"
        Write-Host "Ajouté au PATH!" -ForegroundColor Green
        break
    }
}

if (-not (Get-Command msgfmt -ErrorAction SilentlyContinue)) {
    Write-Host "Gettext non trouvé. Indiquez le chemin exact du dossier 'bin' de gettext:" -ForegroundColor Yellow
    Write-Host "Exemple: C:\Program Files\gettext\bin" -ForegroundColor Cyan
}

