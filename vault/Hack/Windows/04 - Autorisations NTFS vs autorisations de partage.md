---
tags:
  - windows
ordre: 4
---

# Autorisations NTFS vs autorisations de partage

---

Microsoft détient plus de [70 %](https://gs.statcounter.com/os-market-share/desktop/worldwide/#monthly-201804-202104) de la part de marché mondiale des systèmes d'exploitation pour ordinateurs de bureau avec Windows. Cela explique pourquoi la plupart des auteurs de logiciels malveillants choisissent de développer des malwares pour Windows et pourquoi beaucoup perçoivent Windows comme moins sécurisé que d'autres systèmes d'exploitation. D'un point de vue commercial, il est tout simplement logique pour les auteurs de logiciels malveillants de consacrer des ressources à l'écriture de malwares pour Windows. C'est une cible de grande valeur. L'idée qu'un système d'exploitation est immunisé contre les logiciels malveillants est une hérésie technique. S'il est possible d'écrire un logiciel pour un système d'exploitation, alors il est possible d'écrire un virus pour ce système d'exploitation. Gardez à l'esprit qu'un virus, par définition, est un logiciel écrit avec une intention malveillante et peut être écrit pour n'importe quel système d'exploitation. De nombreuses variantes de logiciels malveillants écrits pour Windows peuvent se propager sur le réseau via des partages réseau avec des autorisations laxistes. Il convient également de noter qu'à ce jour, la tristement célèbre vulnérabilité `EternalBlue` hante encore les systèmes Windows non corrigés exécutant `SMBv1` et ouvre souvent la voie aux rançongiciels (ransomware) pour paralyser des organisations.

Le protocole `Server Message Block` (`SMB`) est utilisé dans Windows pour connecter des ressources partagées comme les fichiers et les imprimantes. Il est utilisé dans les environnements de grande, moyenne et petite entreprise. Voir l'image ci-dessous pour visualiser ce concept :

![Schéma du partage de fichiers à l'aide de SMB : un client envoie une requête SMB à un serveur, qui répond. Le serveur accède aux systèmes de fichiers et aux imprimantes, affichant un répertoire de fichiers.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/smb_diagram.png)

Remarque : Chaque fois que vous voyez une visualisation/un schéma d'un concept, prenez votre temps pour le comprendre en profondeur. Une image vaut mille mots, mais il est très tentant de la sauter lors de la lecture.

On pense souvent que les autorisations NTFS et les autorisations de partage sont la même chose. Sachez qu'elles ne sont pas identiques, mais qu'elles s'appliquent souvent à la même ressource partagée. Examinons les autorisations individuelles qui peuvent être définies pour sécuriser/accorder l'accès des objets à un partage réseau hébergé sur un système d'exploitation Windows utilisant le système de fichiers NTFS.

#### Autorisations de partage

|Autorisation|Description|
|---|---|
|`Full Control`|Les utilisateurs sont autorisés à effectuer toutes les actions accordées par les autorisations de Modification (Change) et de Lecture (Read), ainsi qu'à modifier les autorisations pour les fichiers et sous-dossiers NTFS.|
|`Change`|Les utilisateurs sont autorisés à lire, modifier, supprimer et ajouter des fichiers et des sous-dossiers.|
|`Read`|Les utilisateurs sont autorisés à afficher le contenu des fichiers et des sous-dossiers.|

#### Autorisations de base NTFS

|Autorisation|Description|
|---|---|
|`Full Control`|Les utilisateurs sont autorisés à ajouter, modifier, déplacer, supprimer des fichiers et des dossiers, ainsi qu'à modifier les autorisations NTFS qui s'appliquent à tous les dossiers autorisés.|
|`Modify`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de visualiser et de modifier les fichiers et les dossiers. Cela inclut l'ajout ou la suppression de fichiers.|
|`Read & Execute`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de lire le contenu des fichiers et d'exécuter des programmes.|
|`List folder contents`|Les utilisateurs sont autorisés ou se voient refuser les autorisations d'afficher une liste des fichiers et des sous-dossiers.|
|`Read`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de lire le contenu des fichiers.|
|`Write`|Les utilisateurs sont autorisés ou se voient refuser les autorisations d'écrire des modifications dans un fichier et d'ajouter de nouveaux fichiers à un dossier.|
|`Special Permissions`|Une variété d'options d'autorisations avancées.|

#### Autorisations spéciales NTFS

|Autorisation|Description|
|---|---|
|`Full control`|Les utilisateurs sont autorisés ou se voient refuser les autorisations d'ajouter, de modifier, de déplacer, de supprimer des fichiers et des dossiers, ainsi que de modifier les autorisations NTFS qui s'appliquent à tous les dossiers autorisés.|
|`Traverse folder / execute file`|Les utilisateurs sont autorisés ou se voient refuser les autorisations d'accéder à un sous-dossier dans une structure de répertoires, même si l'accès au contenu au niveau du dossier parent leur est refusé. Les utilisateurs peuvent également être autorisés ou se voir refuser les autorisations d'exécuter des programmes.|
|`List folder/read data`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de visualiser les fichiers et les dossiers contenus dans le dossier parent. Les utilisateurs peuvent également être autorisés à ouvrir et à visualiser des fichiers.|
|`Read attributes`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de visualiser les attributs de base d'un fichier ou d'un dossier. Exemples d'attributs de base : système, archive, lecture seule et caché.|
|`Read extended attributes`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de visualiser les attributs étendus d'un fichier ou d'un dossier. Les attributs diffèrent selon le programme.|
|`Create files/write data`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de créer des fichiers dans un dossier et d'apporter des modifications à un fichier.|
|`Create folders/append data`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de créer des sous-dossiers dans un dossier. Des données peuvent être ajoutées aux fichiers, mais le contenu préexistant ne peut pas être écrasé.|
|`Write attributes`|Les utilisateurs sont autorisés ou se voient refuser la modification des attributs de fichier. Cette autorisation ne donne pas accès à la création de fichiers ou de dossiers.|
|`Write extended attributes`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de modifier les attributs étendus d'un fichier ou d'un dossier. Les attributs diffèrent selon le programme.|
|`Delete subfolders and files`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de supprimer des sous-dossiers et des fichiers. Les dossiers parents ne seront pas supprimés.|
|`Delete`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de supprimer les dossiers parents, les sous-dossiers et les fichiers.|
|`Read permissions`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de lire les autorisations d'un dossier.|
|`Change permissions`|Les utilisateurs sont autorisés ou se voient refuser les autorisations de modifier les autorisations d'un fichier ou d'un dossier.|
|`Take ownership`|Les utilisateurs sont autorisés ou se voient refuser l'autorisation de prendre possession d'un fichier ou d'un dossier. Le propriétaire d'un fichier dispose de toutes les autorisations pour modifier n'importe quelle autorisation.|

Gardez à l'esprit que les autorisations NTFS s'appliquent au système sur lequel le dossier et les fichiers sont hébergés. Les dossiers créés dans NTFS héritent par défaut des autorisations des dossiers parents. Il est possible de désactiver l'héritage pour définir des autorisations personnalisées sur les dossiers parents et les sous-dossiers, comme nous le ferons plus tard dans ce module. Les autorisations de partage s'appliquent lorsque l'on accède au dossier via SMB, généralement depuis un système différent sur le réseau. Cela signifie qu'une personne connectée localement à la machine ou via RDP peut accéder au dossier et aux fichiers partagés en naviguant simplement vers l'emplacement sur le système de fichiers et n'a qu'à prendre en compte les autorisations NTFS. Les autorisations au niveau NTFS offrent aux administrateurs un contrôle beaucoup plus granulaire sur ce que les utilisateurs peuvent faire dans un dossier ou un fichier.

---

## Création d'un partage réseau

Pour acquérir une solide compréhension fondamentale de SMB et de sa relation avec NTFS, nous allons créer un partage réseau sur la `machine cible Windows 10`.

Remarque : L'expérience d'apprentissage est idéale si vous disposez de la Pwnbox en plein écran sur un moniteur distinct, ce qui nous permet d'avoir au moins un écran dédié à l'affichage du contenu écrit et un autre pour les machines avec lesquelles nous interagissons. Alternativement, si nous n'avons accès qu'à un seul écran, nous pouvons l'utiliser pour les interactions avec les machines et utiliser un smartphone ou une tablette pour consulter le contenu écrit.

Dans ce cas, nous allons créer un dossier partagé en créant d'abord un nouveau dossier sur le bureau de Windows 10. Gardez à l'esprit que dans la plupart des grands environnements d'entreprise, les partages sont créés sur un réseau de stockage (SAN), un périphérique de stockage en réseau (NAS) ou une partition distincte sur des disques accessibles via un système d'exploitation serveur comme Windows Server. Si nous tombons sur des partages sur un système d'exploitation de bureau, il s'agira soit d'une petite entreprise, soit d'un système tête de pont utilisé par un testeur d'intrusion (pentester) ou un attaquant malveillant pour collecter et exfiltrer des données.

Nous allons suivre ce processus en utilisant l'interface graphique de Windows.

#### Création du dossier

![Bureau Windows avec un menu contextuel ouvert, montrant les options pour créer de nouveaux dossiers, raccourcis et documents.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/creating_directory.png)

Nous allons utiliser l'option `Advanced Sharing` pour configurer notre partage.

#### Transformer le dossier en partage

![Bureau Windows montrant les 'Propriétés de Company Data' avec les paramètres de partage avancé, incluant le nom du partage, la limite d'utilisateurs et les commentaires.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/configuring_share.png)

Remarquez que le nom du partage prend automatiquement par défaut le nom du dossier. Nous pouvons également voir qu'il est possible de limiter le nombre d'utilisateurs pouvant être connectés simultanément à ce partage. Dans un environnement réel, c'est une bonne pratique pour les administrateurs de définir ce nombre en fonction du nombre d'utilisateurs qui ont régulièrement besoin d'accéder à la ressource partagée.

Semblable aux autorisations NTFS, il existe une `liste de contrôle d'accès` (`ACL`) pour les ressources partagées. Nous pouvons considérer cela comme la liste des autorisations SMB. Gardez à l'esprit qu'avec les ressources partagées, les listes d'autorisations SMB et NTFS s'appliquent à chaque ressource partagée dans Windows. L'ACL contient des `entrées de contrôle d'accès` (`ACE`). Typiquement, ces ACE sont composées d'`utilisateurs` et de `groupes` (également appelés principaux de sécurité), car ils constituent un mécanisme approprié pour gérer et suivre l'accès aux ressources partagées.

Remarquez l'entrée de contrôle d'accès par défaut et les paramètres d'autorisation.

#### ACL des autorisations de partage (onglet Partage)

![Fenêtre d'autorisations pour 'Company Data' montrant le groupe 'Everyone' avec l'autorisation de lecture autorisée.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/share_permissions.png)

Pour l'instant, nous allons appliquer ces paramètres pour tester l'effet de cette ACL et des autorisations appliquées telles quelles. Nous allons tester la connectivité depuis la Pwnbox en ouvrant un terminal et en utilisant `smbclient`.

Remarque : Un serveur est techniquement une fonction logicielle utilisée pour répondre aux requêtes d'un client. Dans ce cas, la Pwnbox est notre client, et la machine cible Windows 10 est notre serveur.

#### Utilisation de smbclient pour lister les partages disponibles

```bash
Hiterof13@htb[/htb]$ smbclient -L SERVER_IP -U htb-student Enter WORKGROUP\htb-student's password:       Sharename       Type      Comment     ---------       ----      -------     ADMIN$          Disk      Remote Admin     C$              Disk      Default share     Company Data    Disk           IPC$            IPC       Remote IPC
```

#### Connexion au partage Company Data

```bash
Hiterof13@htb[/htb]$ smbclient '\\SERVER_IP\Company Data' -U htb-student Password for [WORKGROUP\htb-student]: Try "help" to get a list of possible commands.  smb: \>
```

Qu'est-ce qui pourrait potentiellement nous empêcher d'accéder à ce partage si toutes nos entrées sont correctes et que notre liste d'autorisations contient le groupe `Everyone` avec au moins les autorisations de lecture (`Read`) ?

---

## Considérations sur le pare-feu Windows Defender

C'est le Pare-feu Windows Defender qui pourrait potentiellement bloquer l'accès au partage SMB. Comme nous nous connectons depuis un système basé sur Linux, le pare-feu a bloqué l'accès de tout appareil qui n'est pas joint au même `workgroup`. Il est également important de noter que lorsqu'un système Windows fait partie d'un groupe de travail (workgroup), toutes les requêtes `netlogon` sont authentifiées auprès de la base de données `SAM` de ce système Windows particulier. Lorsqu'un système Windows est joint à un environnement de domaine Windows, toutes les requêtes netlogon sont authentifiées auprès d'`Active Directory`. La principale différence entre un groupe de travail et un domaine Windows en termes d'authentification est qu'avec un groupe de travail, la base de données SAM locale est utilisée, et dans un domaine Windows, une base de données centralisée en réseau (Active Directory) est utilisée. Nous devons connaître cette information lorsque nous tentons de nous connecter et de nous authentifier auprès d'un système Windows. Pensez à l'endroit où le compte htb-student est hébergé pour vous connecter correctement à la cible.

En ce qui concerne le blocage des connexions par le pare-feu, cela peut être testé en désactivant complètement chaque profil de pare-feu dans Windows ou en activant des règles de pare-feu entrantes prédéfinies spécifiques dans les `Paramètres de sécurité avancés du Pare-feu Windows Defender`. Comme la plupart des pare-feu, le Pare-feu Windows Defender autorise ou refuse le trafic (demandes d'accès et de connexion dans ce cas) circulant en `entrant` et/ou en `sortant`.

Les différentes règles entrantes et sortantes sont associées aux différents profils de pare-feu dans Defender.

Profils du Pare-feu Windows Defender :

- `Public`
- `Private`
- `Domain`

Il est de bonne pratique d'activer des règles prédéfinies ou d'ajouter des exceptions personnalisées plutôt que de désactiver complètement le pare-feu. Malheureusement, il est très courant que les pare-feu soient laissés complètement désactivés par souci de commodité ou par manque de compréhension. Les règles de pare-feu sur les systèmes de bureau peuvent être gérées de manière centralisée lorsqu'ils sont joints à un environnement de domaine Windows grâce à l'utilisation de la `stratégie de groupe (Group Policy)`. Les concepts et les configurations de la stratégie de groupe sortent du cadre de ce module.

Une fois que les bonnes règles de pare-feu `entrantes` sont activées, nous pourrons nous connecter avec succès au partage. Gardez à l'esprit que nous ne pouvons nous connecter au partage que parce que le compte utilisateur que nous utilisons (`htb-student`) est dans le `groupe Everyone`. Rappelez-vous que nous avons laissé les autorisations de partage spécifiques pour le groupe `Everyone` sur `Read`, ce qui signifie littéralement que nous ne pourrons que lire les fichiers sur ce partage. Une fois qu'une connexion est établie avec un partage, nous pouvons créer un `point de montage` depuis notre Pwnbox vers le système de fichiers de la machine cible Windows 10. C'est là que nous devons également considérer que les autorisations NTFS s'appliquent en même temps que les autorisations de partage. Rappelons que NTFS est le système de fichiers par défaut de Windows. Revenons à notre session xfreerdp avec notre machine cible Windows 10 et examinons les autorisations NTFS sur le dossier Company Data.

#### ACL des autorisations NTFS (onglet Sécurité)

![Fenêtre des Propriétés de Company Data montrant les autorisations de sécurité pour SYSTEM, htb-student et Administrateurs, avec le contrôle total autorisé pour htb-student.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/ntfs.png)

Il y a un contrôle plus granulaire avec les autorisations NTFS qui peut être appliqué aux utilisateurs et aux groupes. Chaque fois que nous voyons une coche grise à côté d'une autorisation, cela signifie qu'elle a été héritée d'un répertoire parent. Par défaut, toutes les autorisations NTFS sont héritées du répertoire parent. Dans le monde Windows, le `lecteur C:\` est le répertoire parent qui régit tous les répertoires, à moins qu'un administrateur système ne désactive l'héritage dans les paramètres de sécurité avancés d'un dossier nouvellement créé.

Dans de nombreux cas, le ou les administrateurs système d'une organisation sont responsables de décider des autorisations qu'un utilisateur ou un groupe d'utilisateurs obtient sur les ressources réseau. C'est pourquoi de nombreuses attaques de harponnage (spear-phishing) ciblent les administrateurs système et autres responsables informatiques. Ils ont beaucoup d'influence sur ce qui est autorisé dans les environnements qu'ils supervisent, même plus que les dirigeants non techniques de haut niveau (C-level) d'une organisation dans de nombreux cas. Par exemple, les médecins ou les cadres travaillant dans un hôpital n'auront pas de droits administratifs sur le réseau, mais les administrateurs système, si.

Donnons maintenant au groupe `Everyone` le `Contrôle total` (`Full control`) au niveau du partage et testons l'impact du changement en essayant de créer un point de montage vers le partage depuis le bureau de notre Pwnbox.

#### Montage sur le partage

```bash
Hiterof13@htb[/htb]$ sudo mount -t cifs -o username=htb-student,password=Academy_WinFun! //ipaddoftarget/"Company Data" /home/user/Desktop/
```

Si cette commande ne fonctionne pas, vérifiez la syntaxe. Si la syntaxe est correcte mais que la commande ne fonctionne toujours pas, `cifs-utils` doit peut-être être installé. Cela peut être fait avec la commande suivante :

#### Installation des utilitaires CIFS

```bash
Hiterof13@htb[/htb]$ sudo apt-get install cifs-utils
```

Une fois que nous avons réussi à créer le point de montage sur le bureau de notre Pwnbox, nous devrions examiner quelques outils intégrés à Windows qui nous permettront de suivre et de surveiller ce que nous avons fait.

La commande `net share` nous permet de voir tous les dossiers partagés sur le système. Remarquez le partage que nous avons créé ainsi que le lecteur C:.

`Vous souvenez-vous avoir partagé le lecteur C:\ ?`

Nous n'avons pas partagé manuellement C:. Le lecteur le plus important avec les fichiers les plus critiques sur un système Windows est partagé via SMB lors de l'installation. Cela signifie que toute personne disposant de l'accès approprié pourrait accéder à distance à l'intégralité du C:\ de chaque système Windows sur un réseau.

Nous pouvons également voir le partage que nous avons créé.

#### Affichage des partages avec net share

```cmd
C:\Users\htb-student> net share  Share name   Resource                        Remark  ------------------------------------------------------------------------------- C$           C:\                             Default share IPC$                                         Remote IPC ADMIN$       C:\WINDOWS                      Remote Admin Company Data C:\Users\htb-student\Desktop\Company Data  The command completed successfully.
```

La `Gestion de l'ordinateur (Computer Management)` est un autre outil que nous pouvons utiliser pour identifier et surveiller les ressources partagées sur un système Windows.

#### Surveillance des partages depuis la Gestion de l'ordinateur

![Fenêtre de la Gestion de l'ordinateur montrant les dossiers partagés, y compris 'Company Data', avec des options de menu contextuel comme développer, gérer et propriétés.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/computer_management.png)

Nous pouvons explorer `Partages`, `Sessions` et `Fichiers ouverts` pour avoir une idée des informations que cela nous fournit. Si nous devions aider un individu ou une organisation à répondre à une violation liée à SMB, ce sont d'excellents endroits à vérifier pour commencer à comprendre comment la violation a pu se produire et ce qui a pu être laissé derrière.

#### Visualisation des journaux d'accès aux partages dans l'Observateur d'événements

L'`Observateur d'événements (Event Viewer)` est un autre bon endroit pour enquêter sur les actions effectuées sur Windows. Presque tous les systèmes d'exploitation ont un mécanisme de journalisation et un utilitaire pour visualiser les journaux qui ont été capturés. Sachez qu'un journal est comme une entrée de journal de bord pour un ordinateur, où l'ordinateur note toutes les actions qui ont été effectuées et de nombreux détails associés à cette action. Nous pouvons visualiser les journaux créés pour chaque action que nous avons effectuée en accédant à la machine cible Windows 10, ainsi que lors de la création, de la modification et de l'accès au dossier partagé.

![Observateur d'événements montrant les journaux de sécurité avec plusieurs entrées 'Audit Success', mettant en évidence l'ID d'événement 5059 pour l'audit de sécurité Microsoft Windows.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/49/event_viewer.png)
---

← [[03 - Système de fichiers]] | [[00 - Sommaire Windows Fundamentals|Sommaire]] | [[05 - Registre Windows]] →
