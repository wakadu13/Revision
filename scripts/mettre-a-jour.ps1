# Met le wiki à jour depuis GitHub (branche main).
#
# Usage, dans le dossier du projet :  .\scripts\mettre-a-jour.ps1
# Puis relancer le serveur (Ctrl+C dans sa fenêtre, puis relancer son script).
#
# Les notes du coffre (vault/) modifiées ou créées depuis le wiki ne sont pas
# touchées. Si un fichier du programme a été modifié à la main sur ce PC et que
# la mise à jour le change aussi, le script le dit et propose de remettre sa
# version d'origine (sinon Git refuse de mettre à jour).

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [Text.Encoding]::UTF8  # accents des messages de Git
Set-Location (Join-Path $PSScriptRoot "..")

function Invoke-Git {
    & git @args
    if ($LASTEXITCODE -ne 0) { throw "La commande « git $args » a échoué (voir le message ci-dessus)." }
}

Write-Host "Version actuelle : $(git log -1 --format='%h du %cd : %s' --date=format:'%d/%m %H:%M')"
Invoke-Git fetch --quiet origin main

$aJour = git rev-list --count HEAD..origin/main
if ($aJour -eq "0") {
    Write-Host "Déjà à jour." -ForegroundColor Green
    exit 0
}
git merge-base --is-ancestor HEAD origin/main
if ($LASTEXITCODE -ne 0) {
    throw "Ce dossier contient des commits qui ne sont pas sur GitHub : mise à jour automatique impossible."
}

# Fichiers modifiés à la main que la mise à jour change aussi.
$changes = @(git diff --name-only HEAD origin/main)
$locales = @(git diff --name-only HEAD)
$bloquants = @($locales | Where-Object { $changes -contains $_ })
if ($bloquants.Count -gt 0) {
    Write-Host ""
    Write-Host "Ces fichiers ont été modifiés à la main sur ce PC, et la mise à jour les change aussi :" -ForegroundColor Yellow
    $bloquants | ForEach-Object { Write-Host "  $_" }
    $reponse = Read-Host "Remettre leur version d'origine pour pouvoir mettre à jour ? Leurs modifications locales seront perdues (o/n)"
    if ($reponse -notmatch '^[oOyY]') {
        Write-Host "Mise à jour annulée : rien n'a changé."
        exit 1
    }
    $bloquants | ForEach-Object { Invoke-Git checkout -- $_ }
}

# Avance jusqu'à la dernière version (la branche courante suit main).
Invoke-Git merge --ff-only --quiet origin/main

# Nouvelles tables dans la mise à jour : base de données mise à jour (avec les
# variables d'environnement de cette fenêtre, comme DJANGO_DATA_DIR si le serveur s'en sert).
if ($changes | Where-Object { $_ -match '/migrations/' }) {
    Write-Host "Mise à jour de la base de données…"
    uv run python manage.py migrate
    if ($LASTEXITCODE -ne 0) { throw "La mise à jour de la base de données a échoué." }
}

Write-Host ""
Write-Host "À jour : $(git log -1 --format='%h du %cd : %s' --date=format:'%d/%m %H:%M')" -ForegroundColor Green
Write-Host "Relancez maintenant le serveur : Ctrl+C dans sa fenêtre, puis relancez son script." -ForegroundColor Yellow
