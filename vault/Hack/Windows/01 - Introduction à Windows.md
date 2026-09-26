---
tags:
  - windows
ordre: 1
---

# Introduction à Windows

En tant que testeur d'intrusion (pentester), il est important de connaître une grande variété de technologies. Une compréhension approfondie des systèmes d'exploitation Windows et Linux est bénéfique pour un large éventail de types d'évaluations. La majorité des systèmes que nous rencontrons lors des évaluations, que ce soit sur site (on-premise) ou dans le cloud, seront basés sur ces deux systèmes d'exploitation. Il est important de comprendre comment attaquer et défendre ces systèmes d'exploitation et comment chacun peut être utilisé comme une plateforme pour effectuer d'autres activités de test d'intrusion.

---

## Le système d'exploitation Windows

Microsoft a introduit le système d'exploitation Windows pour la première fois le 20 novembre 1985. La première version de Windows était une interface graphique (shell) pour MS-DOS. Les versions ultérieures de Windows Desktop ont introduit les programmes Windows File Manager, Program Manager et Print Manager.

Windows 95 a été la première intégration complète de Windows et de DOS et a offert pour la première fois une prise en charge intégrée d'Internet. Cette version a également vu les débuts du navigateur web Internet Explorer. Depuis la version initiale, plus d'une douzaine de versions de Windows ont été publiées, telles que Windows XP, Vista et 8, jusqu'à la version actuelle : Windows 11. Au fil du temps, Microsoft a proposé diverses éditions de chaque version de Windows Desktop, s'adressant à tous, des consommateurs occasionnels aux entreprises.

Windows Server a été lancé pour la première fois en 1993 avec la sortie de Windows NT 3.1 Advanced Server. Windows NT a connu plusieurs mises à jour au fil des ans, ajoutant des technologies telles que Internet Information Services (IIS), divers protocoles réseau, des assistants d'administration pour faciliter les tâches d'administration, et plus encore. Avec la sortie de Windows 2000, Microsoft a inauguré Active Directory, initialement destiné à aider les administrateurs système à configurer le partage de fichiers, le chiffrement des données, les VPN, etc. Windows Server 2000 incluait également la Microsoft Management Console (MMC) et prenait en charge les volumes de disques dynamiques.

Windows Server 2003 a suivi avec les rôles de serveur, un pare-feu (firewall) intégré, le service de cliché instantané des volumes (Volume Shadow Copy Service), et plus encore. Windows Server 2008 incluait le clustering de basculement (failover clustering), le logiciel de virtualisation Hyper-V, Server Core, l'Observateur d'événements (Event Viewer) et des améliorations majeures d'Active Directory. Au fil des ans, Microsoft a publié d'autres versions de Server, notamment Server 2012, Server 2016 et, plus récemment, Server 2019. Cette dernière version a ajouté la prise en charge de Kubernetes, des conteneurs Linux et des fonctionnalités de sécurité plus avancées.

À mesure que de nouvelles versions de Windows sont introduites, les anciennes versions deviennent obsolètes et ne reçoivent plus de mises à jour de Microsoft (sauf si un contrat de support à long terme est souscrit dans certains cas). Windows Server 2008 et 2012 ont atteint leur fin de vie pour les mises à jour de sécurité le 14 janvier 2020. Actuellement, seules les versions Server 2012 R2 et ultérieures sont prises en charge. Cependant, Microsoft a publié des correctifs hors-bande (out-of-band patches) pour des versions antérieures de Windows ces dernières années en raison de la découverte de la vulnérabilité critique SMBv1 (EternalBlue).

De nombreuses versions de Windows sont maintenant considérées comme « obsolètes » (legacy) et ne sont plus prises en charge. Les organisations se retrouvent souvent à utiliser divers systèmes d'exploitation plus anciens pour prendre en charge des applications critiques ou pour des raisons opérationnelles ou budgétaires. Un évaluateur doit comprendre les différences entre les versions ainsi que les diverses mauvaises configurations et vulnérabilités inhérentes à chacune.

---

## Versions de Windows

Voici une liste des principaux systèmes d'exploitation Windows et des numéros de version associés :

|Noms des systèmes d'exploitation|Numéro de version|
|---|---|
|Windows NT 4|4.0|
|Windows 2000|5.0|
|Windows XP|5.1|
|Windows Server 2003, 2003 R2|5.2|
|Windows Vista, Server 2008|6.0|
|Windows 7, Server 2008 R2|6.1|
|Windows 8, Server 2012|6.2|
|Windows 8.1, Server 2012 R2|6.3|
|Windows 10, Server 2016, Server 2019|10.0|

Nous pouvons utiliser le [cmdlet](https://docs.microsoft.com/en-us/powershell/scripting/developer/cmdlet/cmdlet-overview?view=powershell-7) [Get-WmiObject](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-wmiobject?view=powershell-5.1) pour trouver des informations sur le système d'exploitation. Ce cmdlet peut être utilisé pour obtenir des instances de classes WMI ou des informations sur les classes WMI disponibles. Il existe plusieurs façons de trouver la version et le numéro de build de notre système. Nous pouvons facilement obtenir ces informations en utilisant la classe `win32_OperatingSystem`, qui montre que nous sommes sur un hôte Windows 10, avec le numéro de build 19041.

```powershell
PS C:\htb> Get-WmiObject -Class win32_OperatingSystem
| select Version,BuildNumber  Version    BuildNumber -------    ----------- 10.0.19041 19041
```

D'autres classes utiles pouvant être utilisées avec `Get-WmiObject` sont `Win32_Process` pour obtenir une liste des processus, `Win32_Service` pour obtenir une liste des services, et `Win32_Bios` pour obtenir des informations sur le [Système Élémentaire d'Entrée/Sortie](https://fr.wikipedia.org/wiki/Basic_Input/Output_System) (`BIOS`). Le BIOS est un micrologiciel (firmware) installé sur la carte mère d'un ordinateur qui contrôle les fonctions essentielles de l'ordinateur, telles que la gestion de l'alimentation, les interfaces d'entrée/sortie et la configuration du système. Nous pouvons utiliser le paramètre `ComputerName` pour obtenir des informations sur les ordinateurs distants. `Get-WmiObject` peut être utilisé pour démarrer et arrêter des services sur des ordinateurs locaux et distants, et plus encore. De plus amples informations sur ce cmdlet peuvent être trouvées [ici](https://ss64.com/ps/get-wmiobject.html) et [ici](https://adamtheautomator.com/get-wmiobject/).

---

## Accéder à Windows

#### Concepts d'accès local

Si vous lisez ces mots en ce moment, vous avez un accès local à un ordinateur quelconque. Que ce soit un smartphone, une tablette, un ordinateur portable, un Raspberry Pi ou un ordinateur de bureau. L'accès local est le moyen le plus courant d'accéder à n'importe quel ordinateur, y compris ceux qui fonctionnent sous Windows. `L'entrée` se fait probablement via un clavier, un pavé tactile (trackpad) et/ou une souris. `La sortie` provient de l'écran ou des écrans d'affichage. Les organisations disposant de bureaux où les employés travaillent au quotidien élaborent des politiques de sécurité et des contrôles de sécurité autour de l'idée que leurs employés travaillent dans des espaces de travail dédiés sur des ordinateurs appartenant à l'organisation. Il est de plus en plus courant de voir les organisations augmenter leur soutien au télétravail pour leurs effectifs techniques et non techniques. Ce n'est pas une nouvelle réalité pour les professionnels techniques travaillant dans l'informatique, le développement de logiciels et la sécurité de l'information (Infosec). Chaque jour, un professionnel technique peut accéder à plusieurs machines localement et à distance. Ceci dit, discutons du concept d'accès à distance.

#### Concepts d'accès à distance

L'accès à distance consiste à accéder à un ordinateur via un réseau. Un accès local à un ordinateur est nécessaire avant de pouvoir accéder à un autre ordinateur à distance. Il existe d'innombrables méthodes d'accès à distance. Dans ce module, nous utiliserons principalement des méthodes d'accès à distance pour nous connecter et interagir avec les systèmes d'exploitation Windows. Les avancées dans les technologies de réseau et d'Internet ont donné naissance à des industries entières qui dépendent complètement de l'accès à distance et de l'administration à distance des systèmes informatiques.

Considérez les [Fournisseurs de Services Gérés (MSP)](https://www.techtarget.com/searchitchannel/definition/managed-service-provider) et les [Fournisseurs de Services de Sécurité Gérés (MSSP)](https://www.gartner.com/en/information-technology/glossary/mssp-managed-security-service-provider), deux industries qui dépendent principalement de la gestion à distance des systèmes informatiques de leurs clients. Cette fonctionnalité leur permet de centraliser la gestion, de standardiser les technologies utilisées, d'automatiser de nombreuses tâches, de permettre des arrangements de télétravail et d'assurer un temps de réponse rapide lorsque des problèmes surviennent ou que des menaces de sécurité potentielles émergent. L'accès à distance n'est pas seulement limité aux MSP et MSSP. Les organisations dotées d'équipes informatiques, de développement de logiciels et/ou de sécurité utilisent quotidiennement des méthodes d'accès à distance pour créer des applications, gérer des serveurs et administrer les postes de travail des employés. Certaines des technologies d'accès à distance les plus courantes incluent, sans s'y limiter :

- Réseaux Privés Virtuels (VPN)
- Secure Shell (SSH)
- Protocole de Transfert de Fichiers (FTP)
- Virtual Network Computing (VNC)
- Windows Remote Management (ou PowerShell Remoting) (WinRM)
- Protocole de Bureau à Distance (RDP)

Nous nous concentrerons principalement sur l'utilisation du RDP dans ce module.

#### Protocole de Bureau à Distance (RDP)

Le RDP utilise une architecture client/serveur où une application côté client est utilisée pour spécifier l'adresse IP ou le nom d'hôte cible d'un ordinateur sur un réseau où l'accès RDP est activé. L'ordinateur cible où l'accès à distance RDP est activé est considéré comme le serveur. Il est important de noter que le RDP écoute par défaut sur le port logique `3389`. Gardez à l'esprit qu'une adresse IP est utilisée comme identifiant logique pour un ordinateur sur un réseau, et un port logique est un identifiant attribué à une application. En termes plus simples, nous pourrions considérer un sous-réseau comme une rue dans une ville (le réseau de l'entreprise), une adresse IP dans ce sous-réseau attribuée à un hôte comme une maison dans cette rue, et les ports logiques comme des fenêtres/portes qui peuvent être utilisées pour accéder à la maison.

Une fois qu'une requête (encapsulée dans un paquet) a atteint un ordinateur de destination via son adresse IP, la requête sera dirigée vers une application hébergée sur l'ordinateur en fonction du port spécifié dans cette requête (inclus en tant qu'en-tête dans un paquet). L'adressage IP et l'encapsulation de protocole sont traités plus en détail dans le module [Introduction au Réseau](https://academy.hackthebox.com/module/details/34). D'un point de vue réseau, dans ce module, nous devons seulement comprendre que chaque ordinateur a une adresse IP assignée pour communiquer sur un réseau, et que les applications hébergées sur les ordinateurs cibles écoutent sur des ports logiques spécifiques.

Nous pouvons utiliser le RDP pour nous connecter à une cible Windows depuis une machine d'attaque fonctionnant sous Linux ou Windows. Si nous nous connectons à une cible Windows depuis un hôte Windows, nous pouvons utiliser l'application client RDP intégrée appelée `Connexion Bureau à Distance` ([mstsc.exe](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/mstsc)). Regardez le clip ci-dessous pour voir une utilisation de base :

![GIF présentant l'utilisation de l'application Connexion Bureau à Distance.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/UsingRemoteDesktopConnection.gif)

Pour que cela fonctionne, l'accès à distance doit déjà être [autorisé](https://docs.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-allow-access) sur le système Windows cible. Par défaut, l'accès à distance n'est pas autorisé sur les systèmes d'exploitation Windows. L'équipe de HTB Academy a configuré plusieurs de nos cibles Windows pour permettre l'accès RDP une fois connecté aux laboratoires de l'Academy via VPN.

La Connexion Bureau à Distance nous permet également d'enregistrer des profils de connexion. C'est une habitude courante chez les administrateurs informatiques car cela rend la connexion aux systèmes distants plus pratique.

![GIF présentant l'enregistrement des informations d'identification dans l'application Connexion Bureau à Distance.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/SavingRDPConnections.gif)

En tant que pentesters, nous pouvons tirer profit de la recherche de ces fichiers Bureau à Distance enregistrés (`.rdp`) lors d'une mission.

De nombreuses autres applications clientes de Bureau à Distance existent, dont certaines sont listées dans cet article de Microsoft intitulé [Clients Bureau à Distance](https://docs.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/remote-desktop-clients). Nous ne couvrirons pas toutes les applications clientes de Bureau à Distance dans ce module.

#### Utilisation de xfreerdp

Depuis une machine d'attaque basée sur Linux, nous pouvons utiliser un outil appelé [xfreerdp](https://linux.die.net/man/1/xfreerdp) pour accéder à distance aux cibles Windows. Vous remarquerez que nous utilisons xfreerdp dans plusieurs modules en raison de sa facilité d'utilisation, de son ensemble de fonctionnalités, de son utilitaire en ligne de commande et de son efficacité. Regardez le clip ci-dessous pour voir une utilisation de base depuis Pwnbox :

![GIF présentant l'utilisation de l'outil xfreerdp sur le poste de travail Linux.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/ConnectingwithXfreerdp.gif)

N'oubliez pas que nous pouvons également copier et coller des commandes xfreerdp dans la ligne de commande, nous n'avons donc pas besoin de saisir les options manuellement. Plusieurs options sont disponibles avec xfreerdp, telles que la redirection de lecteur pour pouvoir transférer des fichiers vers/depuis l'hôte cible, qui méritent d'être pratiquées et que nous couvrirons dans d'autres modules de HTB Academy.

D'autres clients RDP existent, tels que [Remmina](https://remmina.org/) et [rdesktop](http://www.rdesktop.org/), et nous vous encourageons à en expérimenter d'autres pour voir ce qui vous convient le mieux. Maintenant que nous avons abordé ces concepts, mettons-les en pratique en lançant la cible ci-dessous et en nous y connectant en utilisant RDP avec les informations d'identification fournies.

---

## Connexion à la cible Windows

Connectez-vous via le Bureau à Distance (RDP) en utilisant la commande suivante :

```bash
Hiterof13@htb[/htb]$ xfreerdp /v:<targetIp> /u:htb-student /p:Password
```

Remarque : Le lancement de votre instance cible peut prendre 1 à 2 minutes.
---

[[00 - Sommaire Windows Fundamentals|Sommaire]] | [[02 - Structure du système d'exploitation]] →
