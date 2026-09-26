---
tags:
  - windows
ordre: 13
---

# Expérience utilisateur vs. Server Core

---

[Windows Server Core](https://docs.microsoft.com/en-us/windows-server/administration/server-core/what-is-server-core) a été lancé pour la première fois avec Windows Server 2008 en tant qu'environnement serveur minimaliste ne contenant que les fonctionnalités serveur essentielles. Par conséquent, Server Core a des exigences de gestion moindres, une surface d'attaque (attack surface) plus réduite, et utilise moins d'espace disque et de mémoire que son homologue avec l'Expérience utilisateur (Desktop Experience) (GUI). Dans Server Core, toutes les tâches de configuration et de maintenance sont effectuées via la ligne de commande, PowerShell, ou l'administration à distance avec MMC ou les Outils d'administration de serveur distant (RSAT).

Bien que Server Core vise à avoir une empreinte plus faible en l'absence d'interface graphique, certains programmes graphiques sont toujours pris en charge, tels que l'Éditeur du Registre, le Bloc-notes, les Informations système, Windows Installer, le Gestionnaire des tâches et PowerShell. Il prend également en charge certains outils de la suite Sysinternals tels que Active Directory Explorer, Process Explorer, Process Monitor et TCPView.

Depuis Windows Server 2019, l'option Server Core ou Expérience utilisateur doit être sélectionnée à l'installation, et il n'est plus possible de revenir en arrière (c'est-à-dire convertir Server Core en Expérience utilisateur). Une fois l'installation terminée, la configuration initiale de Server Core peut être effectuée via `Sconfig`, qui est une interface en mode texte (en réalité un VBScript exécuté par WScript). `Sconfig` est utilisé pour exécuter diverses commandes courantes telles que la configuration du réseau, la recherche/l'installation des mises à jour Windows, la gestion des comptes, la configuration de l'administration à distance, l'activation de Windows, et plus encore.

![Invite de commandes affichant les options de configuration du serveur, y compris le domaine, le nom de l'ordinateur, l'administration à distance et les paramètres de mise à jour.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/sconfig.png)

Certaines applications serveur ne peuvent pas s'exécuter sur Server Core, notamment Microsoft Server Virtual Machine Manager 2019 (SCVMM), System Center Data Protection Manager 2019, SharePoint Server 2019, Project Server 2019.

En résumé, Server Core est plus léger et moins gourmand en ressources, mais sa courbe d'apprentissage est plus abrupte et il peut être plus difficile à gérer. Il présente également certaines limitations, comme l'impossibilité d'effectuer des tâches de gestion à l'aide de certains programmes à interface graphique.

Dans n'importe quel environnement, le choix entre l'utilisation de l'Expérience utilisateur ou de Server Core pour l'installation d'un serveur doit être fait en fonction du besoin métier, de l'utilisation prévue du serveur, et du niveau de compétence des administrateurs chargés de sa maintenance. Le tableau suivant présente certaines des applications disponibles sur Server Core par rapport à l'Expérience utilisateur. Il s'agit d'une liste d'applications courantes et non d'une liste exhaustive.

|**Application**|**Server Core**|**Expérience utilisateur**|
|---|---|---|
|Invite de commandes|Disponible|Disponible|
|Windows PowerShell/ Microsoft .NET|Disponible|Disponible|
|Regedit|Disponible|Disponible|
|Diskmgmt.msc|Non disponible|Disponible|
|Gestionnaire de serveur|Non disponible|Disponible|
|Mmc.exe|Non disponible|Disponible|
|Eventvwr|Non disponible|Disponible|
|Services.msc|Non disponible|Disponible|
|Panneau de configuration|Non disponible|Disponible|
|Explorateur Windows|Non disponible|Disponible|
|Taskmgr|Disponible|Disponible|
|Internet Explorer ou Edge|Non disponible|Disponible|
|Services Bureau à distance|Disponible|Disponible|
---

← [[12 - Sous-système Windows pour Linux (WSL)]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[14 - Sécurité Windows]] →
