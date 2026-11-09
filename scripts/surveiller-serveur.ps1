# Surveille le wiki sur ce PC : si l'adresse de statut ne répond pas, affiche une
# notification Windows, note l'incident dans scripts\surveillance.log et, si on
# lui donne un script de relance, le lance.
#
# Usage manuel :  .\scripts\surveiller-serveur.ps1
#                 .\scripts\surveiller-serveur.ps1 -Relance "C:\...\scripts\serve-lan.ps1"
#
# Toutes les 5 minutes, par le Planificateur de tâches (dans une console admin,
# en adaptant le chemin) :
#   schtasks /Create /SC MINUTE /MO 5 /TN "Wiki - surveillance" /RL HIGHEST ^
#     /TR "powershell -NoProfile -ExecutionPolicy Bypass -File C:\chemin\Revision\scripts\surveiller-serveur.ps1"
#
# Depuis l'extérieur (le PC lui-même peut être éteint), un moniteur gratuit comme
# UptimeRobot qui appelle https://wiki.airhiterofprovence.fr/api/status/ toutes les
# 5 minutes prévient par mail ou notification ; et l'application Android avertit les
# admins quand le rappel quotidien ne joint pas le serveur.

param(
    [string]$Url = "http://127.0.0.1:8000/api/status/",
    [string]$Relance = "",
    [int]$Delai = 10
)

$journal = Join-Path $PSScriptRoot "surveillance.log"
$quand = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

try {
    $reponse = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec $Delai
    if ($reponse.StatusCode -eq 200) {
        exit 0
    }
    $raison = "code HTTP $($reponse.StatusCode)"
} catch {
    $raison = $_.Exception.Message
}

Add-Content -Path $journal -Value "$quand  le wiki ne répond pas ($Url) : $raison"

# Notification Windows (toast), sans dépendance.
try {
    [void][Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
    [void][Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]
    $texte = "Le wiki ne répond pas : $raison"
    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xml.LoadXml("<toast><visual><binding template='ToastGeneric'><text>ProjetPluri</text><text>$([Security.SecurityElement]::Escape($texte))</text></binding></visual></toast>")
    $appId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show([Windows.UI.Notifications.ToastNotification]::new($xml))
} catch {
    Write-Warning "Notification impossible : $($_.Exception.Message)"
}

if ($Relance) {
    Add-Content -Path $journal -Value "$quand  relance : $Relance"
    Start-Process powershell -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$Relance`""
}

Write-Host "Le wiki ne répond pas ($raison)." -ForegroundColor Red
exit 1
