---
tags:
  - windows
ordre: 8
---

# Sessions Windows

---

#### Interactif

Une session interactive, ou session d'ouverture de session locale (local logon session), est initiée par un utilisateur qui s'authentifie auprès d'un système local ou de domaine en saisissant ses informations d'identification. Une ouverture de session interactive peut être initiée en se connectant directement au système, en demandant une session d'ouverture de session secondaire à l'aide de la commande `runas` via la ligne de commande, ou via une connexion Bureau à distance (Remote Desktop).

#### Non-interactif

Les comptes non interactifs sous Windows diffèrent des comptes d'utilisateurs standard car ils ne nécessitent pas d'informations de connexion. Il existe 3 types de comptes non interactifs : le Compte Système Local (Local System Account), le Compte Service Local (Local Service Account) et le Compte Service Réseau (Network Service Account). Les comptes non interactifs sont généralement utilisés par le système d'exploitation Windows pour démarrer automatiquement des services et des applications sans nécessiter d'interaction de la part de l'utilisateur. Ces comptes n'ont pas de mot de passe associé et sont habituellement utilisés pour démarrer des services au démarrage du système ou pour exécuter des tâches planifiées.

Il existe des différences entre les trois types de comptes :

|Compte|Description|
|---|---|
|Compte Système Local|Également connu sous le nom de compte `NT AUTHORITY\SYSTEM`, c'est le compte le plus puissant des systèmes Windows. Il est utilisé pour une variété de tâches liées au système d'exploitation, telles que le démarrage des services Windows. Ce compte est plus puissant que les comptes du groupe des administrateurs locaux.|
|Compte Service Local|Connu sous le nom de compte `NT AUTHORITY\LocalService`, il s'agit d'une version moins privilégiée du compte SYSTEM et elle possède des privilèges similaires à ceux d'un compte d'utilisateur local. Des fonctionnalités limitées lui sont accordées et il peut démarrer certains services.|
|Compte Service Réseau|Connu sous le nom de compte `NT AUTHORITY\NetworkService`, il est similaire à un compte d'utilisateur de domaine standard. Il possède des privilèges similaires à ceux du Compte Service Local sur la machine locale. Il peut établir des sessions authentifiées pour certains services réseau.|
---

← [[07 - Autorisations de service]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[09 - Interagir avec le système d'exploitation Windows]] →
