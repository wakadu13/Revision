---
tags:
  - windows
ordre: 7
---

# Autorisations de service

---

Rappelons que les services permettent de gérer des processus de longue durée et constituent un élément essentiel des systèmes d'exploitation Windows. Les administrateurs système les négligent souvent en tant que vecteurs de menace potentiels pouvant être utilisés pour charger des DLL malveillantes, exécuter des applications sans avoir accès à un compte administrateur, escalader les privilèges (escalate privileges) et même maintenir la persistance (maintain persistence). Ces vecteurs de menace dans les services Windows apparaissent souvent à cause de mauvaises configurations d'autorisations de service mises en place par des logiciels tiers et d'erreurs faciles à commettre par les administrateurs lors des processus d'installation.

La première étape pour prendre conscience de l'importance des autorisations de service est simplement de comprendre qu'elles existent et d'y être attentif. Sur les systèmes d'exploitation serveur, les services réseau critiques tels que DHCP et les services de domaine Active Directory sont généralement installés en utilisant le compte de l'administrateur qui effectue l'installation. Une partie du processus d'installation consiste à assigner un service spécifique pour qu'il s'exécute avec les informations d'identification et les privilèges d'un utilisateur désigné, qui par défaut est défini dans le contexte de l'utilisateur actuellement connecté.

Par exemple, si nous sommes connectés en tant que Bob sur un serveur lors de l'installation de DHCP, ce service sera configuré pour s'exécuter en tant que Bob, sauf indication contraire. Quelles mauvaises choses pourraient en résulter ? Eh bien, que se passerait-il si Bob quittait l'entreprise ou était licencié ? La pratique commerciale habituelle serait de désactiver le compte de Bob dans le cadre de son processus de départ. Dans ce cas, qu'arriverait-il à DHCP et aux autres services fonctionnant avec le compte de Bob ? Ces services ne parviendraient pas à démarrer. DHCP, ou Dynamic Host Configuration Protocol, est responsable de l'attribution d'adresses IP aux ordinateurs sur le réseau. Si ce service s'arrête sur un serveur DHCP Windows, les clients demandant une adresse IP n'en recevront pas. Cela signifie qu'une mauvaise configuration de service pourrait entraîner un temps d'arrêt (downtime) et une perte de productivité. Il est fortement recommandé de créer un compte utilisateur individuel pour exécuter les services réseau critiques. Ceux-ci sont appelés des comptes de service.

Nous devons également être attentifs aux autorisations de service et aux autorisations des répertoires à partir desquels ils s'exécutent, car il est possible de remplacer le chemin d'accès à un exécutable par un fichier DLL ou exécutable malveillant. Examinons les autorisations des services fonctionnant sur Windows 10 pour mieux comprendre cela.

---

## Examen des services avec services.msc

Comme nous l'avons vu dans la section sur les processus et les services, nous pouvons utiliser `services.msc` pour visualiser et gérer presque tous les détails concernant tous les services. Examinons de plus près le service associé à `Windows Update` (`wuauserv`).

![Fenêtre des services montrant les propriétés de Windows Update avec le nom du service, sa description et l'état en cours d'exécution.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/service_properties.png)

Notez les différentes propriétés disponibles pour la consultation et la configuration. Connaître le nom du service est particulièrement utile lorsque l'on utilise des outils en ligne de commande pour examiner et gérer les services. Le chemin d'accès à l'exécutable est le chemin complet du programme et de la commande à exécuter lorsque le service démarre. Si les autorisations NTFS du répertoire de destination sont configurées avec des permissions faibles, un attaquant pourrait remplacer l'exécutable d'origine par un autre créé à des fins malveillantes. Nous abordons plus en détail les autorisations NTFS dans la section Autorisations NTFS vs Autorisations de partage de ce module.

![Fenêtre des services montrant les propriétés de Windows Update avec les options d'ouverture de session pour le compte Système local et un compte utilisateur spécifique.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/logon.png)

La plupart des services s'exécutent par défaut avec les privilèges LocalSystem, qui représentent le plus haut niveau d'accès autorisé sur un système d'exploitation Windows individuel. Toutes les applications n'ont pas besoin de permissions de niveau compte Système Local, il est donc bénéfique d'effectuer des recherches au cas par cas lorsque l'on envisage d'installer de nouvelles applications dans un environnement Windows. Il est de bonne pratique d'identifier les applications qui peuvent fonctionner avec le moins de privilèges possible pour s'aligner avec le principe de moindre privilège.

[Voici une explication du principe de moindre privilège](https://www.cloudflare.com/learning/access-management/principle-of-least-privilege/)

Comptes de service intégrés notables dans Windows :

- LocalService
- NetworkService
- LocalSystem

Note : Nous pouvons également créer de nouveaux comptes et les utiliser dans le seul but d'exécuter un service.

![Propriétés de Windows Update montrant les options de récupération en cas d'échec du service, y compris des actions comme le redémarrage du service ou de l'ordinateur.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/recovery_screen.png)

L'onglet de récupération permet de configurer des étapes en cas d'échec d'un service. Remarquez comment ce service peut être configuré pour exécuter un programme après la première défaillance. C'est encore un autre vecteur qu'un attaquant pourrait utiliser pour exécuter des programmes malveillants en utilisant un service légitime.

---

## Examen des services avec sc

La commande sc peut également être utilisée pour configurer et gérer les services. Expérimentons avec quelques commandes.

```cmd
C:\Users\htb-student>sc qc wuauserv [SC] QueryServiceConfig SUCCESS  SERVICE_NAME: wuauserv         TYPE               : 20  WIN32_SHARE_PROCESS         START_TYPE         : 3   DEMAND_START         ERROR_CONTROL      : 1   NORMAL         BINARY_PATH_NAME   : C:\WINDOWS\system32\svchost.exe -k netsvcs -p         LOAD_ORDER_GROUP   :         TAG                : 0         DISPLAY_NAME       : Windows Update         DEPENDENCIES       : rpcss         SERVICE_START_NAME : LocalSystem
```

La commande `sc qc` est utilisée pour interroger le service. C'est là que la connaissance des noms des services peut s'avérer utile. Si nous voulions interroger un service sur un appareil sur le réseau, nous pourrions spécifier le nom d'hôte ou l'adresse IP immédiatement après `sc`.

```cmd
C:\Users\htb-student>sc \\hostname or ip of box query ServiceName
```

Nous pouvons également utiliser sc pour démarrer et arrêter des services.

```cmd
C:\Users\htb-student> sc stop wuauserv  [SC] OpenService FAILED 5:  Access is denied.
```

Remarquez comment l'accès nous est refusé pour effectuer cette action sans l'exécuter dans un contexte administratif. Si nous exécutons une invite de commandes avec des `privilèges élevés (elevated privileges)`, nous serons autorisés à effectuer cette action.

```cmd
C:\WINDOWS\system32> sc config wuauserv binPath=C:\Winbows\Perfectlylegitprogram.exe  [SC] ChangeServiceConfig SUCCESS  C:\WINDOWS\system32> sc qc wuauserv  [SC] QueryServiceConfig SUCCESS  SERVICE_NAME: wuauserv         TYPE               : 20  WIN32_SHARE_PROCESS         START_TYPE         : 3   DEMAND_START         ERROR_CONTROL      : 1   NORMAL         BINARY_PATH_NAME   : C:\Winbows\Perfectlylegitprogram.exe         LOAD_ORDER_GROUP   :         TAG                : 0         DISPLAY_NAME       : Windows Update         DEPENDENCIES       : rpcss         SERVICE_START_NAME : LocalSystem
```

Si nous enquêtions sur une situation où nous soupçonnions la présence de logiciels malveillants sur le système, sc nous donnerait la possibilité de rechercher et d'analyser rapidement les services couramment ciblés et les services nouvellement créés. C'est aussi beaucoup plus facile à scripter que d'utiliser des outils graphiques comme `services.msc`.

Une autre manière utile d'examiner les autorisations de service avec `sc` est d'utiliser la commande `sdshow`.

```cmd
C:\WINDOWS\system32> sc sdshow wuauserv  D:(A;;CCLCSWRPLORC;;;AU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)S:(AU;FA;CCDCLCSWRPWPDTLOSDRCWDWO;;;WD)
```

À première vue, la sortie semble folle. On pourrait presque croire que nous avons fait une erreur dans notre commande, mais il y a une logique à cette folie. Chaque objet nommé dans Windows est un [objet sécurisable (securable object)](https://docs.microsoft.com/en-us/windows/win32/secauthz/securable-objects), et même certains objets non nommés sont sécurisables. S'il est sécurisable dans un SE Windows, il aura un [descripteur de sécurité (security descriptor)](https://docs.microsoft.com/en-us/windows/win32/secauthz/security-descriptors). Les descripteurs de sécurité identifient le propriétaire de l'objet et un groupe principal contenant une `liste de contrôle d'accès discrétionnaire (DACL)` et une `liste de contrôle d'accès système (SACL)`.

Généralement, une DACL est utilisée pour contrôler l'accès à un objet, et une SACL est utilisée pour comptabiliser et journaliser les tentatives d'accès. Cette section examinera la DACL, mais les mêmes concepts s'appliqueraient à une SACL.

```text
D:(A;;CCLCSWRPLORC;;;AU)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;BA)(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;SY)
```

Cet amalgame de caractères regroupés et délimités par des parenthèses ouvertes et fermées est dans un format connu sous le nom de `langage de définition de descripteur de sécurité (SDDL)`.

Nous pourrions être tentés de lire de gauche à droite, car c'est ainsi que la langue française est généralement écrite, mais cela peut être très différent lorsque l'on interagit avec des ordinateurs. Lisez l'ensemble du descripteur de sécurité pour le service `Windows Update` (`wuauserv`) dans cet ordre, en commençant par la première lettre et le premier jeu de parenthèses :

`D: (A;;CCLCSWRPLORC;;;AU)`

1. D: - les caractères qui suivent sont des autorisations DACL
2. AU: - définit le principal de sécurité (security principal) Utilisateurs authentifiés
3. A;; - l'accès est autorisé
4. CC - SERVICE_QUERY_CONFIG est le nom complet, et c'est une requête au gestionnaire de contrôle des services (SCM) pour la configuration du service
5. LC - SERVICE_QUERY_STATUS est le nom complet, et c'est une requête au SCM pour l'état actuel du service
6. SW - SERVICE_ENUMERATE_DEPENDENTS est le nom complet, et cela énumérera une liste des services dépendants
7. RP - SERVICE_START est le nom complet, et cela démarrera le service
8. LO - SERVICE_INTERROGATE est le nom complet, et cela interrogera le service sur son état actuel
9. RC - READ_CONTROL est le nom complet, et cela interrogera le descripteur de sécurité du service

En lisant le descripteur de sécurité, il peut être facile de se perdre dans l'ordre apparemment aléatoire des caractères, mais rappelons que nous visualisons essentiellement des entrées de contrôle d'accès dans une liste de contrôle d'accès. Chaque ensemble de 2 caractères entre les points-virgules représente des actions autorisées pour un utilisateur ou un groupe spécifique.

`;;CCLCSWRPLORC;;;`

Après le dernier ensemble de points-virgules, les caractères spécifient le principal de sécurité (Utilisateur et/ou Groupe) qui est autorisé à effectuer ces actions.

`;;;AU`

Le caractère immédiatement après la parenthèse ouvrante et avant le premier ensemble de points-virgules définit si les actions sont Autorisées ou Refusées.

`A;;`

Ce descripteur de sécurité complet associé au service `Windows Update` (`wuauserv`) comporte trois ensembles d'entrées de contrôle d'accès car il y a trois principaux de sécurité différents. Chaque principal de sécurité a des autorisations spécifiques qui lui sont appliquées.

---

## Examiner les autorisations de service avec PowerShell

En utilisant le cmdlet PowerShell `Get-Acl`, nous pouvons examiner les autorisations de service en ciblant le chemin d'un service spécifique dans le registre.

```powershell
PS C:\Users\htb-student> Get-ACL -Path HKLM:\System\CurrentControlSet\Services\wuauserv
| Format-List  Path   : Microsoft.PowerShell.Core\Registry::HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\wuauserv Owner  : NT AUTHORITY\SYSTEM Group  : NT AUTHORITY\SYSTEM Access : BUILTIN\Users Allow  ReadKey          BUILTIN\Users Allow  -2147483648          BUILTIN\Administrators Allow  FullControl          BUILTIN\Administrators Allow  268435456          NT AUTHORITY\SYSTEM Allow  FullControl          NT AUTHORITY\SYSTEM Allow  268435456          CREATOR OWNER Allow  268435456          APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES Allow  ReadKey          APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES Allow  -2147483648          S-1-15-3-1024-1065365936-1281604716-3511738428-1654721687-432734479-3232135806-4053264122-3456934681 Allow          ReadKey          S-1-15-3-1024-1065365936-1281604716-3511738428-1654721687-432734479-3232135806-4053264122-3456934681 Allow          -2147483648 Audit  : Sddl   : O:SYG:SYD:AI(A;ID;KR;;;BU)(A;CIIOID;GR;;;BU)(A;ID;KA;;;BA)(A;CIIOID;GA;;;BA)(A;ID;KA;;;SY)(A;CIIOID;GA;;;SY)(A          ;CIIOID;GA;;;CO)(A;ID;KR;;;AC)(A;CIIOID;GR;;;AC)(A;ID;KR;;;S-1-15-3-1024-1065365936-1281604716-3511738428-1654          721687-432734479-3232135806-4053264122-3456934681)(A;CIIOID;GR;;;S-1-15-3-1024-1065365936-1281604716-351173842          8-1654721687-432734479-3232135806-4053264122-3456934681)
```

Remarquez comment cette commande renvoie les autorisations de compte spécifiques dans un format facile à lire et en SDDL. De plus, le SID qui représente chaque principal de sécurité (Utilisateur et/ou Groupe) est présent dans le SDDL. C'est quelque chose que nous n'obtenons pas en exécutant `sc` depuis l'invite de commandes.

Savoir comment interagir avec les services et leurs autorisations associées depuis la ligne de commande facilite l'écriture de scripts pour ces tâches. Bien qu'il soit bon de savoir comment effectuer ces tâches depuis l'interface graphique, cela n'est pas facilement adaptable (does not scale well) lorsque l'on travaille dans des environnements réseau plus vastes et des domaines.
---

← [[06 - Services et Processus Windows]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[08 - Sessions Windows]] →
