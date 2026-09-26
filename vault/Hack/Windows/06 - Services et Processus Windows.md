---
tags:
  - windows
ordre: 6
---

# Services et Processus Windows

---

## Services Windows

Les services sont un composant majeur du système d'exploitation Windows. Ils permettent la création et la gestion de processus de longue durée. Les services Windows peuvent être démarrés automatiquement au lancement du système sans intervention de l'utilisateur. Ces services peuvent continuer à s'exécuter en arrière-plan même après que l'utilisateur se soit déconnecté de son compte sur le système.

Des applications peuvent également être créées pour être installées en tant que service, comme une application de surveillance réseau installée sur un serveur. Les services sous Windows sont responsables de nombreuses fonctions au sein du système d'exploitation, telles que les fonctions réseau, l'exécution de diagnostics système, la gestion des informations d'identification des utilisateurs, le contrôle des mises à jour Windows, etc.

Les services Windows sont gérés via le système Service Control Manager (SCM), accessible via le module complémentaire MMC `services.msc`.

Ce module complémentaire fournit une interface graphique (GUI) pour interagir avec les services et les gérer, et affiche des informations sur chaque service installé. Ces informations incluent le Nom du service, sa Description, son État, son Type de démarrage et l'utilisateur sous lequel le service s'exécute.

Il est également possible d'interroger et de gérer les services via la ligne de commande en utilisant `sc.exe` ou des cmdlets [PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-7) comme `Get-Service`.

```powershell
PS C:\htb> Get-Service | ? {$_.Status -eq "Running"}
| select -First 2 |fl   Name                : AdobeARMservice DisplayName         : Adobe Acrobat Update Service Status              : Running DependentServices   : {} ServicesDependedOn  : {} CanPauseAndContinue : False CanShutdown         : False CanStop             : True ServiceType         : Win32OwnProcess  Name                : Appinfo DisplayName         : Application Information Status              : Running DependentServices   : {} ServicesDependedOn  : {RpcSs, ProfSvc} CanPauseAndContinue : False CanShutdown         : False CanStop             : True ServiceType         : Win32OwnProcess, Win32ShareProcess
```

Les états des services peuvent être En cours d'exécution (Running), Arrêté (Stopped) ou En pause (Paused), et ils peuvent être configurés pour démarrer manuellement, automatiquement ou de manière différée au lancement du système. Les services peuvent également être affichés dans l'état Démarrage (Starting) ou Arrêt en cours (Stopping) si une action a déclenché leur démarrage ou leur arrêt. Windows a trois catégories de services : Services locaux, Services réseau et Services système. Les services ne peuvent généralement être créés, modifiés et supprimés que par des utilisateurs disposant de privilèges administratifs. Les mauvaises configurations des permissions des services sont un vecteur d'escalade de privilèges (privilege escalation) courant sur les systèmes Windows.

Sous Windows, il existe des [services système critiques](https://docs.microsoft.com/en-us/windows/win32/rstmgr/critical-system-services) qui ne peuvent pas être arrêtés et redémarrés sans un redémarrage du système. Si nous mettons à jour un fichier ou une ressource utilisé par l'un de ces services, nous devons redémarrer le système.

|Service|Description|
|---|---|
|smss.exe|Session Manager SubSystem. Responsable de la gestion des sessions sur le système.|
|csrss.exe|Client Server Runtime Process. La partie en mode utilisateur du sous-système Windows.|
|wininit.exe|Démarre le fichier .ini de Wininit qui liste tous les changements à apporter à Windows lorsque l'ordinateur est redémarré après l'installation d'un programme.|
|logonui.exe|Utilisé pour faciliter la connexion de l'utilisateur à un PC.|
|lsass.exe|Le Local Security Authentication Server vérifie la validité des connexions des utilisateurs à un PC ou un serveur. Il génère le processus responsable de l'authentification des utilisateurs pour le service Winlogon.|
|services.exe|Gère les opérations de démarrage et d'arrêt des services.|
|winlogon.exe|Responsable de la gestion de la séquence d'attention sécurisée, du chargement du profil utilisateur à la connexion et du verrouillage de l'ordinateur lorsqu'un économiseur d'écran est en cours d'exécution.|
|System|Un processus système d'arrière-plan qui exécute le noyau Windows.|
|svchost.exe with RPCSS|Gère les services système qui s'exécutent à partir de bibliothèques de liens dynamiques (fichiers avec l'extension .dll) telles que les « Mises à jour automatiques », le « Pare-feu Windows » et le « Plug and Play ». Utilise le service d'appel de procédure à distance (RPC) (RPCSS).|
|svchost.exe with Dcom/PnP|Gère les services système qui s'exécutent à partir de bibliothèques de liens dynamiques (fichiers avec l'extension .dll) telles que les « Mises à jour automatiques », le « Pare-feu Windows » et le « Plug and Play ». Utilise les services Distributed Component Object Model (DCOM) et Plug and Play (PnP).|

Ce [lien](https://en.wikipedia.org/wiki/List_of_Microsoft_Windows_components#Services) contient une liste des composants Windows, y compris les services clés.

---

## Processus

Les processus s'exécutent en arrière-plan sur les systèmes Windows. Ils s'exécutent soit automatiquement en tant que partie intégrante du système d'exploitation Windows, soit sont démarrés par d'autres applications installées.

Les processus associés aux applications installées peuvent souvent être terminés sans causer d'impact grave sur le système d'exploitation. Certains processus sont critiques et, s'ils sont terminés, empêcheront certains composants du système d'exploitation de fonctionner correctement. Quelques exemples incluent l'application d'ouverture de session Windows (Windows Logon Application), le processus Système (System), le processus inactif du système (System Idle Process), l'application de démarrage Windows (Windows Start-Up Application), l'exécution client-serveur (Client Server Runtime), le gestionnaire de session Windows (Windows Session Manager), l'hôte de service (Service Host), et le processus du service du sous-système de l'autorité de sécurité locale (LSASS).

---

## Service du sous-système de l'autorité de sécurité locale (LSASS)

`lsass.exe` est le processus chargé d'appliquer la politique de sécurité sur les systèmes Windows. Lorsqu'un utilisateur tente de se connecter au système, ce processus vérifie sa tentative de connexion et crée des jetons d'accès (access tokens) en fonction des niveaux de permission de l'utilisateur. LSASS est également responsable des changements de mot de passe des comptes utilisateurs. Tous les événements associés à ce processus (tentatives de connexion/déconnexion, etc.) sont enregistrés dans le journal de sécurité Windows. LSASS est une cible de très grande valeur car plusieurs outils existent pour extraire de la mémoire de ce processus les informations d'identification, qu'elles soient en clair ou hachées.

---

## Outils Sysinternals

La suite d'outils [SysInternals Tools](https://docs.microsoft.com/en-us/sysinternals) est un ensemble d'applications Windows portables qui peuvent être utilisées pour administrer des systèmes Windows (la plupart du temps sans nécessiter d'installation). Les outils peuvent être soit téléchargés depuis le site web de Microsoft, soit chargés directement depuis un partage de fichiers accessible par Internet en tapant `\\live.sysinternals.com\tools` dans une fenêtre de l'Explorateur Windows.

Par exemple, nous pouvons exécuter procdump.exe directement depuis ce partage sans le télécharger sur le disque.

```cmd
C:\htb> \\live.sysinternals.com\tools\procdump.exe -accepteula  ProcDump v9.0 - Sysinternals process dump utility Copyright (C) 2009-2017 Mark Russinovich and Andrew Richards Sysinternals - www.sysinternals.com  Monitors a process and writes a dump file when the process exceeds the specified criteria or has an exception.  Capture Usage:    procdump.exe [-mm] [-ma] [-mp] [-mc Mask] [-md Callback_DLL] [-mk]                 [-n Count]                 [-s Seconds]                 [-c|-cl CPU_Usage [-u]]                 [-m|-ml Commit_Usage]                 [-p|-pl Counter_Threshold]                 [-h]                 [-e [1 [-g] [-b]]]                 [-l]                 [-t]                 [-f  Include_Filter, ...]                 [-fx Exclude_Filter, ...]                 [-o]                 [-r [1..5] [-a]]                 [-wer]                 [-64]                 {                  {{[-w] Process_Name
| Service_Name
| PID} [Dump_File
| Dump_Folder]}                 |                  {-x Dump_Folder Image_File [Argument, ...]}                 }                  <SNIP>
```

La suite comprend des outils tels que `Process Explorer`, une version améliorée du `Gestionnaire des tâches`, et `Process Monitor`, qui peut être utilisé pour surveiller le système de fichiers, le registre et l'activité réseau liés à tout processus en cours d'exécution sur le système. D'autres outils supplémentaires sont TCPView, utilisé pour surveiller l'activité Internet, et PSExec, qui peut être utilisé pour gérer/se connecter à distance à des systèmes via le protocole SMB.

Ces outils peuvent être utiles pour les testeurs d'intrusion (penetration testers) pour, par exemple, découvrir des processus intéressants et des chemins d'escalade de privilèges possibles, ainsi que pour le mouvement latéral (lateral movement).

---

## Gestionnaire des tâches

Le Gestionnaire des tâches de Windows (Windows Task Manager) est un outil puissant pour la gestion des systèmes Windows. Il fournit des informations sur les processus en cours, les performances du système, les services en cours d'exécution, les programmes au démarrage, les utilisateurs connectés/processus des utilisateurs connectés, et les services. Le Gestionnaire des tâches peut être ouvert en faisant un clic droit sur la barre des tâches et en sélectionnant `Gestionnaire des tâches`, en appuyant sur ctrl + shift + Esc, en appuyant sur ctrl + alt + del et en sélectionnant `Gestionnaire des tâches`, en ouvrant le menu Démarrer et en tapant `Gestionnaire des tâches`, ou en tapant `taskmgr` depuis une console CMD ou PowerShell.

![Gestionnaire des tâches affichant les processus avec l'utilisation du processeur, de la mémoire, du disque et du réseau, mettant en évidence Google Chrome et Windows PowerShell.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/taskmgr.png)

|Onglet|Description|
|---|---|
|Onglet Processus|Affiche une liste des applications en cours d'exécution et des processus d'arrière-plan, ainsi que l'utilisation du processeur, de la mémoire, du disque, du réseau et de l'énergie pour chacun.|
|Onglet Performance|Affiche des graphiques et des données telles que l'utilisation du processeur, la durée de fonctionnement du système, l'utilisation de la mémoire, du disque, du réseau et du GPU. Nous pouvons également ouvrir le `Moniteur de ressources` (Resource Monitor), qui nous donne une vue beaucoup plus détaillée de l'utilisation actuelle des ressources du processeur, de la mémoire, du disque et du réseau.|

![Moniteur de ressources affichant les processus avec les détails d'utilisation de la mémoire et le graphique de la mémoire physique.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/resource_monitor.png)

|Onglet|Description|
|---|---|
|Onglet Historique des applications|Affiche l'utilisation des ressources pour le compte utilisateur actuel pour chaque application sur une période donnée.|
|Onglet Démarrage|Affiche les applications configurées pour démarrer au lancement du système ainsi que leur impact sur le processus de démarrage.|
|Onglet Utilisateurs|Affiche les utilisateurs connectés et les processus/l'utilisation des ressources associés à leur session.|
|Onglet Détails|Affiche le nom, l'ID de processus (PID), l'état, le nom d'utilisateur associé, l'utilisation du processeur et de la mémoire pour chaque application en cours d'exécution.|
|Onglet Services|Affiche le nom, le PID, la description et l'état de chaque service installé. Le module complémentaire Services est également accessible depuis cet onglet.|

---

## Process Explorer

[Process Explorer](https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer) fait partie de la suite d'outils Sysinternals. Cet outil peut montrer quels handles et processus DLL sont chargés lorsqu'un programme s'exécute. `Process Explorer` affiche une liste des processus en cours d'exécution, et à partir de là, nous pouvons voir quels handles le processus a sélectionnés dans une vue, ou les DLL et les fichiers échangés en mémoire qui ont été chargés dans une autre vue. Nous pouvons également effectuer une recherche dans l'outil pour montrer quels processus sont liés à un handle ou une DLL spécifique. L'outil peut également être utilisé pour analyser les relations parent-enfant entre les processus afin de voir quels processus enfants sont générés par une application et aider à résoudre les problèmes tels que les processus orphelins qui peuvent subsister lorsqu'un processus est terminé.
---

← [[05 - Registre Windows]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[07 - Autorisations de service]] →
