# Script pour configurer gettext dans le PATH
# Exécutez ce script en tant qu'administrateur ou modifiez le PATH manuellement

Write-Host "Recherche de gettext..." -ForegroundColor Yellow

# Chemins communs pour gettext
$possiblePaths = @(
    "C:\Program Files\gettext\bin",
    "C:\gettext\bin",
    "$env:ProgramFiles\gettext\bin",
    "$env:LOCALAPPDATA\Programs\gettext\bin"
)

$gettextPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $msgfmt = Join-Path $path "msgfmt.exe"
        if (Test-Path $msgfmt) {
            $gettextPath = $path
            Write-Host "Gettext trouvé dans: $gettextPath" -ForegroundColor Green
            break
        }
    }
}

if ($null -eq $gettextPath) {
    Write-Host "Gettext non trouvé dans les emplacements standards." -ForegroundColor Red
    Write-Host "Veuillez indiquer le chemin d'installation de gettext:" -ForegroundColor Yellow
    $gettextPath = Read-Host "Chemin (ex: C:\Program Files\gettext\bin)"
    
    if (-not (Test-Path $gettextPath)) {
        Write-Host "Le chemin spécifié n'existe pas!" -ForegroundColor Red
        exit 1
    }
}

# Ajouter au PATH pour cette session
$env:PATH += ";$gettextPath"
Write-Host "Gettext ajouté au PATH pour cette session." -ForegroundColor Green

# Vérifier que ça fonctionne
$msgfmt = Get-Command msgfmt -ErrorAction SilentlyContinue
if ($msgfmt) {
    Write-Host "Gettext est maintenant disponible!" -ForegroundColor Green
    Write-Host "Pour l'ajouter de façon permanente, ajoutez ce chemin au PATH système:" -ForegroundColor Yellow
    Write-Host $gettextPath -ForegroundColor Cyan
} else {
    Write-Host "Erreur: gettext n'est toujours pas accessible." -ForegroundColor Red
}

