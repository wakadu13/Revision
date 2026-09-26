---
tags:
  - windows
ordre: 12
---

# Sous-système Windows pour Linux (WSL)

---

[WSL](https://docs.microsoft.com/en-us/windows/wsl/) est une fonctionnalité qui permet d'exécuter des binaires Linux nativement sur Windows 10 et Windows Server 2019. Elle a été initialement conçue pour les développeurs qui avaient besoin d'exécuter Bash, Ruby et des outils en ligne de commande Linux natifs tels que `sed`, `awk`, `grep`, etc., directement sur leur poste de travail Windows. La deuxième version de WSL, sortie en mai 2019, a introduit un véritable noyau Linux utilisant un sous-ensemble des fonctionnalités d'Hyper-V.

WSL peut être installé en exécutant la commande PowerShell `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux` en tant qu'administrateur. Une fois cette fonctionnalité activée, nous pouvons soit télécharger une distribution Linux depuis le Microsoft Store et l'installer, soit télécharger manuellement la distribution Linux de notre choix, la décompresser et l'installer depuis la ligne de commande.

WSL installe une application nommée `Bash.exe`, qui peut être exécutée en tapant simplement `bash` dans une console Windows pour lancer un shell Bash. Depuis ce shell, nous avons toute l'apparence et le comportement d'un hôte Linux, y compris la structure de répertoires standard de Linux.

```powershell
PS C:\htb> ls /  bin dev home lib lLib64 media opt root sbin srv tmp var boot etc init 1lib32 Libx32 mnt proc run Snap sys usr
```

Nous pouvons accéder au volume `C$` et aux autres volumes du système d'exploitation hôte via le répertoire `mnt`, ce qui rend la transition entre l'hôte WSL et le SE hôte Windows transparente. Une fois dans ce shell bash, nous pouvons interagir avec WSL comme nous le ferions avec n'importe quel système d'exploitation basé sur Linux : exécuter des commandes, installer des mises à jour/paquets, etc.

```powershell
PS C:\htb> uname -a  Linux WS01 4.4.0-18362-Microsoft #476-Microsoft Frit Nov 01 16:53:00 PST 2019 x86_64 x86 _64 x86_64 GNU/Linux
```

---

← [[11 - Microsoft Management Console (MMC)]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[13 - Expérience utilisateur vs. Server Core]] →
