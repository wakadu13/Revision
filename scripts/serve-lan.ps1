# Lance le wiki en HTTPS sur le réseau local (autres appareils du même Wi-Fi).
#
#   navigateur --HTTPS--> Caddy (port 443, toutes les interfaces)
#                           --HTTP--> Django (127.0.0.1:8000, invisible du réseau)
#
# Prérequis (une seule fois) : winget install CaddyServer.Caddy
# Usage :  .\scripts\serve-lan.ps1              (adresse IP détectée)
#          .\scripts\serve-lan.ps1 -Ip 10.0.0.17
# Arrêt :  Ctrl+C

param([string]$Ip)

$ErrorActionPreference = "Stop"
$port = 8000

# Caddy : dans le PATH, sinon là où winget l'installe (le PATH des terminaux
# n'est mis à jour qu'au redémarrage de VS Code / du terminal).
$caddyExe = (Get-Command caddy -ErrorAction SilentlyContinue).Source
if (-not $caddyExe) {
    $caddyExe = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Links\caddy.exe"
    if (-not (Test-Path $caddyExe)) {
        Write-Error "Caddy n'est pas installé : winget install CaddyServer.Caddy"
    }
}

# Adresse du PC sur le réseau local : carte physique active avec une passerelle
# (ignore VPN, Tailscale et cartes virtuelles).
if (-not $Ip) {
    $Ip = Get-NetAdapter -Physical | Where-Object Status -eq Up | ForEach-Object {
        $config = Get-NetIPConfiguration -InterfaceIndex $_.ifIndex
        if ($config.IPv4DefaultGateway) { $config.IPv4Address.IPAddress }
    } | Select-Object -First 1
    if (-not $Ip) { Write-Error "Adresse IP locale introuvable : préciser -Ip 192.168.x.x" }
}

# Django : seule cette adresse est acceptée ; HTTPS, cookies sécurisés et HSTS
# s'activent automatiquement. Caddy transmet l'IP du client et le protocole.
$env:DJANGO_DEBUG = "0"
$env:DJANGO_ALLOWED_HOSTS = $Ip
$env:DJANGO_CSRF_TRUSTED_ORIGINS = "https://$Ip"
$env:DJANGO_BEHIND_PROXY = "1"
Remove-Item Env:DJANGO_HTTPS -ErrorAction SilentlyContinue

# Caddy crée sa propre autorité de certification locale au premier lancement
# (Windows demande de l'approuver : répondre Oui).
$caddy = Start-Process $caddyExe -NoNewWindow -PassThru -ArgumentList @(
    "reverse-proxy", "--from", "https://$Ip", "--to", "127.0.0.1:$port", "--internal-certs"
)

$root = Join-Path $env:APPDATA "Caddy\pki\authorities\local\root.crt"
Write-Host ""
Write-Host "Wiki : https://$Ip/  (appareils du même réseau)"
Write-Host "Certificat à installer sur les autres appareils : $root"
Write-Host "Après une mise à jour du code (git pull, changement de branche) : Ctrl+C puis relancer ce script."
Write-Host ""

try {
    Set-Location (Join-Path $PSScriptRoot "..")
    # --noreload : le code n'est pas relu à chaud, il faut relancer le script
    # après une mise à jour (sinon : erreurs 500 sur les pages qui ont changé).
    uv run python manage.py runserver "127.0.0.1:$port" --noreload
}
finally {
    Stop-Process -Id $caddy.Id -ErrorAction SilentlyContinue
}
