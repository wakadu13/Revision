---
tags:
  - windows
ordre: 14
---

# Sécurité Windows

---

La sécurité est un sujet essentiel dans les systèmes d'exploitation Windows. Les systèmes Windows comportent de nombreuses parties mobiles qui présentent une vaste surface d'attaque. En raison des nombreuses applications intégrées, des fonctionnalités et des couches de paramètres, les systèmes Windows peuvent être facilement mal configurés, les exposant ainsi aux attaques même s'ils sont entièrement corrigés.

Il possède de nombreuses fonctionnalités intégrées qui peuvent être détournées et a souffert d'une grande variété de vulnérabilités critiques, ce qui a donné lieu à des exploits locaux et à distance largement utilisés et très efficaces.

Microsoft a amélioré la sécurité de Windows au fil des ans. Alors que l'interconnexion de notre monde continue de s'étendre et que les attaquants deviennent plus sophistiqués, Microsoft a continué d'ajouter de nouvelles fonctionnalités qui peuvent être utilisées par les administrateurs système pour renforcer les systèmes et pour bloquer et détecter activement les tentatives d'intrusion et d'utilisation abusive.

Windows suit certains principes de sécurité pour contrôler l'accès et l'authentification au sein du système. Ces principes s'appliquent à diverses entités, telles que les utilisateurs, les ordinateurs en réseau, les threads et les processus, qui peuvent être autorisées à effectuer des actions spécifiques. Le modèle de sécurité est conçu pour minimiser le risque d'accès non autorisé, ce qui rend plus difficile pour les attaquants ou les logiciels malveillants d'exploiter le système.

---

## Identifiant de sécurité (SID)

Chacun des principaux de sécurité (security principals) sur le système possède un identifiant de sécurité (SID) unique. Le système génère automatiquement les SID. Cela signifie que même si, par exemple, nous avons deux utilisateurs identiques sur le système, Windows peut distinguer les deux et leurs droits en se basant sur leurs SID. Les SID sont des valeurs de chaîne de différentes longueurs, qui sont stockées dans la base de données de sécurité. Ces SID sont ajoutés au jeton d'accès (access token) de l'utilisateur pour identifier toutes les actions que l'utilisateur est autorisé à effectuer.

Un SID se compose de l'autorité d'identification (Identifier Authority) et de l'ID relatif (RID). Dans un environnement de domaine Active Directory (AD), le SID inclut également le SID de domaine.

```powershell
PS C:\htb> whoami /user  USER INFORMATION ----------------  User Name           SID
===================
============================================= ws01\bob S-1-5-21-674899381-4069889467-2080702030-1002
```

Le SID est décomposé selon ce modèle.

```powershell
(SID)-(revision level)-(identifier-authority)-(subauthority1)-(subauthority2)-(etc)
```

Décomposons le SID morceau par morceau.

|**Numéro**|**Signification**|**Description**|
|---|---|---|
|S|SID|Identifie la chaîne comme étant un SID.|
|1|Niveau de révision|À ce jour, il n'a jamais changé et a toujours été `1`.|
|5|Autorité d'identification|Une chaîne de 48 bits qui identifie l'autorité (l'ordinateur ou le réseau) qui a créé le SID.|
|21|Sous-autorité1|C'est un nombre variable qui identifie la relation de l'utilisateur ou du groupe décrit par le SID avec l'autorité qui l'a créé. Il nous indique dans quel ordre cette autorité a créé le compte de l'utilisateur.|
|674899381-4069889467-2080702030|Sous-autorité2|Nous indique quel ordinateur (ou domaine) a créé le numéro.|
|1002|Sous-autorité3|Le RID qui distingue un compte d'un autre. Il nous indique si cet utilisateur est un utilisateur normal, un invité, un administrateur, ou s'il fait partie d'un autre groupe.|

---

## Gestionnaire des comptes de sécurité (SAM) et Entrées de contrôle d'accès (ACE)

Le SAM (Security Accounts Manager) accorde des droits à un réseau pour exécuter des processus spécifiques.

Les droits d'accès eux-mêmes sont gérés par des Entrées de contrôle d'accès (ACE) dans des Listes de contrôle d'accès (ACL). Les ACL contiennent des ACE qui définissent quels utilisateurs, groupes ou processus ont accès à un fichier ou peuvent exécuter un processus, par exemple.

Les permissions d'accès à un objet sécurisable sont données par le descripteur de sécurité (security descriptor), classé en deux types d'ACL : la `Discretionary Access Control List (DACL)` ou la `System Access Control List (SACL)`. Chaque thread et processus démarré ou initié par un utilisateur passe par un processus d'autorisation. Les jetons d'accès (access tokens), validés par l'Autorité de sécurité locale (LSA), font partie intégrante de ce processus. En plus du SID, ces jetons d'accès contiennent d'autres informations pertinentes pour la sécurité. Comprendre ces fonctionnalités est une partie essentielle de l'apprentissage de l'utilisation et du contournement de ces mécanismes de sécurité pendant la phase d'escalade de privilèges.

---

## Contrôle de compte d'utilisateur (UAC)

Le [Contrôle de compte d'utilisateur (UAC)](https://docs.microsoft.com/fr-fr/windows/security/identity-protection/user-account-control/how-user-account-control-works) est une fonctionnalité de sécurité de Windows visant à empêcher les logiciels malveillants de s'exécuter ou de manipuler des processus qui pourraient endommager l'ordinateur ou son contenu. Il existe le Mode d'approbation administrateur (Admin Approval Mode) dans l'UAC, qui est conçu pour empêcher l'installation de logiciels indésirables à l'insu de l'administrateur ou pour empêcher que des modifications à l'échelle du système ne soient effectuées. Vous avez sûrement déjà vu l'invite de consentement (consent prompt) si vous avez installé un logiciel spécifique et que votre système vous a demandé de confirmer si vous souhaitiez l'installer. Comme l'installation nécessite des droits d'administrateur, une fenêtre apparaît, vous demandant si vous voulez confirmer l'installation. Avec un utilisateur standard qui n'a pas les droits pour l'installation, l'exécution sera refusée, ou le mot de passe de l'administrateur vous sera demandé. Cette invite de consentement interrompt l'exécution des scripts ou des binaires que les logiciels malveillants ou les attaquants essaient d'exécuter jusqu'à ce que l'utilisateur entre le mot de passe ou confirme l'exécution. Pour comprendre comment fonctionne l'UAC, nous devons savoir comment il est structuré, comment il fonctionne et ce qui déclenche l'invite de consentement. Le diagramme suivant, adapté de la source [ici](https://docs.microsoft.com/fr-fr/windows/security/identity-protection/user-account-control/how-user-account-control-works), illustre le fonctionnement de l'UAC.

![Organigramme des interactions entre l'utilisateur et le système pour les invites d'élévation, la gestion à distance et les paramètres UAC.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/uacarchitecture1.png)

---

## Registre

Le [Registre](https://fr.wikipedia.org/wiki/Base_de_registre) est une base de données hiérarchique dans Windows, essentielle au système d'exploitation. Il stocke les paramètres de bas niveau pour le système d'exploitation Windows et les applications qui choisissent de l'utiliser. Il est divisé en données spécifiques à l'ordinateur et spécifiques à l'utilisateur. Nous pouvons ouvrir l'Éditeur du Registre en tapant `regedit` depuis la ligne de commande ou la barre de recherche de Windows.

![Éditeur du Registre montrant HKEY_LOCAL_MACHINE avec le DWORD Analysis défini sur 0.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/regedit.png)

La structure arborescente se compose de dossiers principaux (clés racines) dans lesquels se trouvent des sous-dossiers (sous-clés) avec leurs entrées/fichiers (valeurs). Il existe 11 types de valeurs différents qui peuvent être saisis dans une sous-clé.

|**Valeur**|**Type**|
|---|---|
|REG_BINARY|Données binaires sous n'importe quelle forme.|
|REG_DWORD|Un nombre de 32 bits.|
|REG_DWORD_LITTLE_ENDIAN|Un nombre de 32 bits au format little-endian. Windows est conçu pour fonctionner sur des architectures informatiques little-endian. Par conséquent, cette valeur est définie comme REG_DWORD dans les fichiers d'en-tête de Windows.|
|REG_DWORD_BIG_ENDIAN|Un nombre de 32 bits au format big-endian. Certains systèmes UNIX prennent en charge les architectures big-endian.|
|REG_EXPAND_SZ|Une chaîne terminée par un caractère nul qui contient des références non développées à des variables d'environnement (par exemple, "%PATH%"). Ce sera une chaîne Unicode ou ANSI selon que vous utilisez les fonctions Unicode ou ANSI. Pour développer les références de variables d'environnement, utilisez la fonction [**ExpandEnvironmentStrings**](https://docs.microsoft.com/en-us/windows/win32/api/processenv/nf-processenv-expandenvironmentstringsa).|
|REG_LINK|Une chaîne Unicode terminée par un caractère nul contenant le chemin cible d'un lien symbolique créé en appelant la fonction [**RegCreateKeyEx**](https://docs.microsoft.com/en-us/windows/desktop/api/Winreg/nf-winreg-regcreatekeyexa) avec REG_OPTION_CREATE_LINK.|
|REG_MULTI_SZ|Une séquence de chaînes terminées par un caractère nul, terminée par une chaîne vide (\0). Voici un exemple : _String1_\0_String2_\0_String3_\0_LastString_\0\0 Le premier \0 termine la première chaîne, le deuxième à l'avant-dernier \0 termine la dernière chaîne, et le \0 final termine la séquence. Notez que le terminateur final doit être pris en compte dans la longueur de la chaîne.|
|REG_NONE|Aucun type de valeur défini.|
|REG_QWORD|Un nombre de 64 bits.|
|REG_QWORD_LITTLE_ENDIAN|Un nombre de 64 bits au format little-endian. Windows est conçu pour fonctionner sur des architectures informatiques little-endian. Par conséquent, cette valeur est définie comme REG_QWORD dans les fichiers d'en-tête de Windows.|
|REG_SZ|Une chaîne terminée par un caractère nul. Ce sera soit une chaîne Unicode, soit une chaîne ANSI, selon que vous utilisez les fonctions Unicode ou ANSI.|

Source : [https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry-value-types](https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry-value-types)

Chaque dossier sous `Computer` est une clé. Les clés racines commencent toutes par `HKEY`. Une clé telle que `HKEY-LOCAL-MACHINE` est abrégée en `HKLM`. HKLM contient tous les paramètres pertinents pour le système local. Cette clé racine contient six sous-clés comme `SAM`, `SECURITY`, `SYSTEM`, `SOFTWARE`, `HARDWARE`, et `BCD`, chargées en mémoire au moment du démarrage (sauf `HARDWARE` qui est chargée dynamiquement).

![Éditeur du Registre montrant HKEY_LOCAL_MACHINE avec le DWORD Analysis défini sur 0.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/regedit2.png)

L'intégralité du registre système est stockée dans plusieurs fichiers sur le système d'exploitation. Vous pouvez les trouver sous `C:\Windows\System32\Config\`.

```powershell
PS C:\htb> ls      Directory: C:\Windows\system32\config  Mode                 LastWriteTime         Length Name ----                 -------------         ------ ---- d-----         12/7/2019   4:14 AM                Journal d-----         12/7/2019   4:14 AM                RegBack d-----         12/7/2019   4:14 AM                systemprofile d-----         8/12/2020   1:43 AM                TxR -a----         8/13/2020   6:02 PM        1048576 BBI -a----         6/25/2020   4:36 PM          28672 BCD-Template -a----         8/30/2020  12:17 PM       33816576 COMPONENTS -a----         8/13/2020   6:02 PM         524288 DEFAULT -a----         8/26/2020   7:51 PM        4603904 DRIVERS -a----         6/25/2020   3:37 PM          32768 ELAM -a----         8/13/2020   6:02 PM          65536 SAM -a----         8/13/2020   6:02 PM          65536 SECURITY -a----         8/13/2020   6:02 PM       87818240 SOFTWARE -a----         8/13/2020   6:02 PM       17039360 SYSTEM
```

La ruche de registre spécifique à l'utilisateur (HKCU) est stockée dans le dossier de l'utilisateur (c'est-à-dire, `C:\Users\<USERNAME>\Ntuser.dat`).

```powershell
PS C:\htb> gci -Hidden      Directory: C:\Users\bob  Mode                 LastWriteTime         Length Name ----                 -------------         ------ ---- d--h--         6/25/2020   5:12 PM                AppData d--hsl         6/25/2020   5:12 PM                Application Data d--hsl         6/25/2020   5:12 PM                Cookies d--hsl         6/25/2020   5:12 PM                Local Settings d--h--         6/25/2020   5:12 PM                MicrosoftEdgeBackups d--hsl         6/25/2020   5:12 PM                My Documents d--hsl         6/25/2020   5:12 PM                NetHood d--hsl         6/25/2020   5:12 PM                PrintHood d--hsl         6/25/2020   5:12 PM                Recent d--hsl         6/25/2020   5:12 PM                SendTo d--hsl         6/25/2020   5:12 PM                Start Menu d--hsl         6/25/2020   5:12 PM                Templates -a-h--         8/13/2020   6:01 PM        2883584 NTUSER.DAT -a-hs-         6/25/2020   5:12 PM         524288 ntuser.dat.LOG1 -a-hs-         6/25/2020   5:12 PM        1011712 ntuser.dat.LOG2 -a-hs-         8/17/2020   5:46 PM        1048576 NTUSER.DAT{53b39e87-18c4-11ea-a811-000d3aa4692b}.TxR.0.regtrans-ms -a-hs-         8/17/2020  12:13 PM        1048576 NTUSER.DAT{53b39e87-18c4-11ea-a811-000d3aa4692b}.TxR.1.regtrans-ms -a-hs-         8/17/2020  12:13 PM        1048576 NTUSER.DAT{53b39e87-18c4-11ea-a811-000d3aa4692b}.TxR.2.regtrans-ms -a-hs-         8/17/2020   5:46 PM          65536 NTUSER.DAT{53b39e87-18c4-11ea-a811-000d3aa4692b}.TxR.blf -a-hs-         6/25/2020   5:15 PM          65536 NTUSER.DAT{53b39e88-18c4-11ea-a811-000d3aa4692b}.TM.blf -a-hs-         6/25/2020   5:12 PM         524288 NTUSER.DAT{53b39e88-18c4-11ea-a811-000d3aa4692b}.TMContainer000000000                                                   00000000001.regtrans-ms -a-hs-         6/25/2020   5:12 PM         524288 NTUSER.DAT{53b39e88-18c4-11ea-a811-000d3aa4692b}.TMContainer000000000                                                   00000000002.regtrans-ms ---hs-         6/25/2020   5:12 PM             20 ntuser.ini
```

---

## Clés de registre Run et RunOnce

Il existe également ce que l'on appelle des ruches de registre (registry hives), qui contiennent un groupe logique de clés, de sous-clés et de valeurs pour prendre en charge les logiciels et les fichiers chargés en mémoire au démarrage du système d'exploitation ou à la connexion d'un utilisateur. Ces ruches sont utiles pour maintenir l'accès au système. On les appelle les [clés de registre Run et RunOnce](https://docs.microsoft.com/fr-fr/windows/win32/setupapi/run-and-runonce-registry-keys).

Le registre de Windows comprend les quatre clés suivantes :

```powershell
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

Voici un exemple de la clé `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run` lorsque vous êtes connecté à un système.

```powershell
PS C:\htb> reg query HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run  HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run     SecurityHealth    REG_EXPAND_SZ    %windir%\system32\SecurityHealthSystray.exe     RTHDVCPL    REG_SZ    "C:\Program Files\Realtek\Audio\HDA\RtkNGUI64.exe" -s     Greenshot    REG_SZ    C:\Program Files\Greenshot\Greenshot.exe
```

Voici un exemple de la clé `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run` montrant les applications s'exécutant sous l'utilisateur actuel lorsque vous êtes connecté à un système.

```powershell
PS C:\htb> reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run  HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run     OneDrive    REG_SZ    "C:\Users\bob\AppData\Local\Microsoft\OneDrive\OneDrive.exe" /background     OPENVPN-GUI    REG_SZ    C:\Program Files\OpenVPN\bin\openvpn-gui.exe     Docker Desktop    REG_SZ    C:\Program Files\Docker\Docker\Docker Desktop.exe
```

---

## Liste blanche d'applications (Application Whitelisting)

Une liste blanche d'applications (application whitelist) est une liste d'applications logicielles ou d'exécutables approuvés autorisés à être présents et à s'exécuter sur un système. L'objectif est de protéger l'environnement contre les logiciels malveillants nuisibles et les logiciels non approuvés qui ne correspondent pas aux besoins métier spécifiques d'une organisation. La mise en œuvre d'une liste blanche appliquée peut être un défi, en particulier dans un grand réseau. Une organisation devrait initialement mettre en œuvre une liste blanche en mode audit pour s'assurer que toutes les applications nécessaires sont bien sur la liste blanche et ne sont pas bloquées par une erreur d'omission, ce qui peut causer plus de problèmes que de solutions.

La liste noire (Blacklisting), en revanche, spécifie une liste de logiciels/applications nuisibles ou non autorisés à bloquer, et tous les autres sont autorisés à s'exécuter/être installés. La liste blanche est basée sur un principe de "confiance zéro" (zero trust) dans lequel tous les logiciels/applications sont considérés comme "mauvais", à l'exception de ceux spécifiquement autorisés. La maintenance d'une liste blanche a généralement moins de frais généraux car un administrateur système n'aura qu'à spécifier ce qui est autorisé et non à mettre constamment à jour une "liste noire" avec de nouvelles applications malveillantes.

La mise en place de listes blanches est recommandée par des organisations telles que le [NIST](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-167.pdf), en particulier dans les environnements à haute sécurité.

---

## AppLocker

[AppLocker](https://docs.microsoft.com/fr-fr/windows/security/threat-protection/windows-defender-application-control/applocker/applocker-overview) est la solution de liste blanche d'applications de Microsoft et a été introduite pour la première fois dans Windows 7. AppLocker donne aux administrateurs système le contrôle sur les applications et les fichiers que les utilisateurs peuvent exécuter. Il offre un contrôle granulaire sur les exécutables, les scripts, les fichiers d'installation Windows, les DLL, les applications packagées et les installateurs d'applications packagées.

Il permet de créer des règles basées sur des attributs de fichier tels que le nom de l'éditeur (qui peut être dérivé de la signature numérique), le nom du produit, le nom du fichier et la version. Des règles peuvent également être établies en fonction des chemins de fichiers et des hachages. Les règles peuvent être appliquées à des groupes de sécurité ou à des utilisateurs individuels, en fonction des besoins de l'entreprise. AppLocker peut être déployé en mode audit d'abord pour tester l'impact avant d'appliquer toutes les règles.

---

## Stratégie de groupe locale

La Stratégie de groupe (Group Policy) permet aux administrateurs de définir, configurer et ajuster une variété de paramètres. Dans un environnement de domaine, les stratégies de groupe sont transmises d'un Contrôleur de domaine à toutes les machines jointes au domaine auxquelles les Objets de stratégie de groupe (GPO) sont liés. Ces paramètres peuvent également être définis sur des machines individuelles à l'aide de la Stratégie de groupe locale.

La Stratégie de groupe peut être configurée localement, à la fois dans des environnements de domaine et hors domaine. La Stratégie de groupe locale peut être utilisée pour ajuster certains paramètres graphiques et réseau qui ne sont autrement pas accessibles via le Panneau de configuration. Elle peut également être utilisée pour verrouiller la politique d'un ordinateur individuel avec des paramètres de sécurité stricts, tels que n'autoriser que l'installation/l'exécution de certains programmes ou imposer des exigences strictes en matière de mots de passe de compte utilisateur.

Nous pouvons ouvrir l'Éditeur de stratégie de groupe locale en ouvrant le menu Démarrer et en tapant `gpedit.msc`. L'éditeur est divisé en deux catégories sous Stratégie de l'ordinateur local : `Computer Configuration` et `User Configuration`.

![Éditeur de stratégie de groupe locale montrant les modèles d'administration sous Configuration de l'ordinateur.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/Local_GP.png)

Par exemple, nous pouvons ouvrir la Stratégie de l'ordinateur local pour activer Credential Guard en activant le paramètre `Turn On Virtualization Based Security`. Credential Guard est une fonctionnalité de Windows 10 qui protège contre les attaques par vol d'identifiants en isolant le processus LSA du système d'exploitation.

![Fenêtre des paramètres 'Activer la sécurité basée sur la virtualisation' avec des options pour activer le démarrage sécurisé et la protection DMA.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/credguard.png)

Nous pouvons également activer un audit de compte affiné et configurer AppLocker depuis l'Éditeur de stratégie de groupe locale. Il est utile d'explorer la Stratégie de groupe locale et d'apprendre les nombreuses façons dont elle peut être utilisée pour verrouiller un système Windows.

---

## Antivirus Windows Defender

Windows Defender Antivirus (Defender), anciennement connu sous le nom de Windows Defender, est un antivirus intégré fourni gratuitement avec les systèmes d'exploitation Windows. Il a d'abord été publié en tant qu'outil anti-logiciels espions téléchargeable pour Windows XP et Server 2003. Defender a commencé à être pré-installé dans le système d'exploitation avec Windows Vista/Server 2008. Le programme a été renommé Windows Defender Antivirus avec la mise à jour Windows 10 Creators Update.

Defender est livré avec plusieurs fonctionnalités telles que la protection en temps réel (real-time protection), qui protège l'appareil contre les menaces connues en temps réel, et la protection fournie par le cloud (cloud-delivered protection), qui fonctionne en conjonction avec la soumission automatique d'échantillons pour télécharger les fichiers suspects pour analyse. Lorsque les fichiers sont soumis au service de protection cloud, ils sont "verrouillés" pour empêcher tout comportement potentiellement malveillant jusqu'à ce que l'analyse soit terminée. Une autre fonctionnalité est la Protection contre les falsifications (Tamper Protection), qui empêche la modification des paramètres de sécurité via le Registre, les cmdlets PowerShell ou la stratégie de groupe.

Windows Defender est géré depuis le Centre de sécurité, à partir duquel une variété de fonctionnalités et de paramètres de sécurité supplémentaires peuvent être activés et gérés.

![Tableau de bord de la Sécurité Windows montrant l'état de la protection antivirus désactivée, de la protection du compte correcte et du pare-feu désactivé.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/Defender_sec_center.png)

Les paramètres de protection en temps réel peuvent être ajustés pour ajouter des fichiers, des dossiers et des zones de mémoire à l'accès contrôlé aux dossiers afin d'empêcher les modifications non autorisées. Nous pouvons également ajouter des fichiers ou des dossiers à une liste d'exclusion, afin qu'ils ne soient pas analysés. Un exemple serait d'exclure de l'analyse un dossier d'outils utilisés pour les tests d'intrusion, car ils seront signalés comme malveillants et mis en quarantaine ou supprimés du système. L'accès contrôlé aux dossiers est la protection intégrée de Defender contre les ransomwares.

Nous pouvons utiliser la cmdlet PowerShell `Get-MpComputerStatus` pour vérifier quels paramètres de protection sont activés.

```powershell
PS C:\htb> Get-MpComputerStatus
| findstr "True" AMServiceEnabled                : True AntispywareEnabled              : True AntivirusEnabled                : True BehaviorMonitorEnabled          : True IoavProtectionEnabled           : True IsTamperProtected               : True NISEnabled                      : True OnAccessProtectionEnabled       : True RealTimeProtectionEnabled       : True
```

Bien qu'aucune solution antivirus ne soit parfaite, Windows Defender s'en sort très bien dans les tests mensuels de taux de détection par rapport à d'autres solutions, même payantes. De plus, comme il est préinstallé dans le système d'exploitation, il n'introduit pas de "surcharge" (bloat) sur le système, comme d'autres programmes qui ajoutent des extensions de navigateur et des traqueurs. D'autres produits sont connus pour ralentir le système en raison de la manière dont ils s'accrochent au système d'exploitation.

Windows Defender n'est pas sans défauts et doit faire partie d'une stratégie de défense en profondeur (defense-in-depth) construite autour des principes fondamentaux de la gestion de la configuration et des correctifs, et non être traité comme une solution miracle pour protéger nos systèmes. Les définitions sont constamment mises à jour, et de nouvelles versions de Windows Defender sont intégrées aux versions majeures du système d'exploitation telles que Windows 10, version 1909, qui est la version la plus récente au moment de la rédaction.

Windows Defender détectera les charges utiles des frameworks open-source courants tels que Metasploit ou les versions non modifiées d'outils tels que Mimikatz.

![Historique de la protection montrant les pare-feu désactivés et une menace grave détectée : Trojan.Win32/Meterpreter.O.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/meterp_caught.png)

Bien que cela devienne de plus en plus difficile, il est toujours possible de contourner entièrement les protections de Windows Defender appliquées par la dernière version avec les définitions les plus à jour installées.
---

← [[13 - Expérience utilisateur vs. Server Core]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[15 - Évaluation des compétences - Principes fondamentaux de Windows]] →
