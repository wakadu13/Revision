---
tags:
  - linux
ordre: 29
---

# Solaris

Solaris est un système d'exploitation basé sur Unix développé par Sun Microsystems (racheté plus tard par Oracle Corporation) dans les années 1990. Il est connu pour sa robustesse, sa scalabilité et sa prise en charge des systèmes matériels et logiciels haut de gamme. Solaris est largement utilisé dans les environnements d'entreprise pour des applications critiques, telles que la gestion de bases de données, le cloud computing et la virtualisation. Par exemple, il inclut un hyperviseur intégré appelé `Oracle VM Server for SPARC`, qui permet à plusieurs machines virtuelles de s'exécuter sur un seul serveur physique. Globalement, il est conçu pour gérer de grandes quantités de données et fournir des services fiables et sécurisés aux utilisateurs. Il est souvent utilisé dans des environnements d'entreprise où la sécurité, la performance et la stabilité sont des exigences clés.

L'objectif de Solaris est de fournir une plateforme hautement stable, sécurisée et évolutive pour l'informatique d'entreprise. Il dispose de fonctionnalités intégrées pour la haute disponibilité (high availability), la tolérance aux pannes (fault tolerance) et la gestion de système, ce qui le rend idéal pour les applications critiques. Il est largement utilisé dans les secteurs bancaire, financier et gouvernemental, où la sécurité, la fiabilité et la performance sont primordiales. Il est également utilisé dans les centres de données à grande échelle, les environnements de cloud computing et les plateformes de virtualisation. Des entreprises telles qu'Amazon, IBM et Dell utilisent Solaris dans leurs produits et services, ce qui souligne son importance dans l'industrie.

---

## Distributions Linux vs Solaris

Solaris et les distributions Linux sont deux types de systèmes d'exploitation qui diffèrent de manière significative. Premièrement, Solaris est un système d'exploitation propriétaire détenu et développé par Oracle Corporation, et son code source n'est pas accessible au grand public. En revanche, la plupart des distributions Linux sont open source, ce qui signifie que leur code source est disponible pour que quiconque puisse le modifier et l'utiliser. De plus, les distributions Linux utilisent couramment le système de fichiers Zettabyte (`ZFS`), qui est un système de fichiers très avancé offrant des fonctionnalités telles que la compression de données, les instantanés (snapshots) et une grande scalabilité. D'un autre côté, Solaris utilise une facilité de gestion des services (`SMF`), qui est un framework de gestion des services très avancé offrant une meilleure fiabilité et disponibilité pour les services système.

|**Répertoire**|**Description**|
|---|---|
|`/`|Le répertoire racine contient tous les autres répertoires et fichiers du système de fichiers.|
|`/bin`|Il contient les binaires système essentiels requis pour le démarrage et les opérations de base du système.|
|`/boot`|Le répertoire boot contient des fichiers liés au démarrage tels que le chargeur d'amorçage et les images du noyau.|
|`/dev`|Le répertoire dev contient des fichiers de périphériques qui représentent les périphériques physiques et logiques connectés au système.|
|`/etc`|Le répertoire etc contient des fichiers de configuration du système, tels que les scripts de démarrage du système et les données d'authentification des utilisateurs.|
|`/home`|Répertoires personnels des utilisateurs.|
|`/kernel`|Ce répertoire contient des modules du noyau et d'autres fichiers liés au noyau.|
|`/lib`|Répertoire pour les bibliothèques requises par les binaires dans les répertoires /bin et /sbin.|
|`/lost+found`|Ce répertoire est utilisé par l'outil de vérification et de réparation de la cohérence du système de fichiers pour stocker les fichiers récupérés.|
|`/mnt`|Répertoire pour monter temporairement des systèmes de fichiers.|
|`/opt`|Ce répertoire contient les paquets logiciels optionnels qui sont installés sur le système.|
|`/proc`|Le répertoire proc fournit une vue sur l'état des processus et du noyau du système sous forme de fichiers.|
|`/sbin`|Ce répertoire contient les binaires système requis pour les tâches d'administration système.|
|`/tmp`|Les fichiers temporaires créés par le système et les applications sont stockés dans ce répertoire.|
|`/usr`|Le répertoire usr contient des données et des programmes en lecture seule à l'échelle du système, tels que la documentation, les bibliothèques et les exécutables.|
|`/var`|Ce répertoire contient des fichiers de données variables, tels que les journaux système, les files d'attente de courriels et les files d'attente d'impression.|

Solaris possède un certain nombre de caractéristiques uniques qui le distinguent des autres systèmes d'exploitation. L'un de ses principaux atouts est sa prise en charge des systèmes matériels et logiciels haut de gamme. Il est conçu pour fonctionner avec des centres de données à grande échelle et des infrastructures réseau complexes, et il peut gérer de grandes quantités de données sans aucun problème de performance.

En matière de gestion de paquets, Solaris utilise le gestionnaire de paquets Image Packaging System (`IPS`), qui offre un moyen puissant et flexible de gérer les paquets et les mises à jour. Solaris fournit également des fonctionnalités de sécurité avancées, telles que le contrôle d'accès basé sur les rôles (`RBAC` - Role-Based Access Control) et les contrôles d'accès obligatoires (mandatory access controls), qui ne sont pas disponibles dans toutes les distributions Linux.

---

## Différences

Approfondissons les différences entre Solaris et les distributions Linux. L'une des différences les plus importantes est que le code source n'est pas open source et n'est connu que dans des cercles fermés. Cela signifie que, contrairement à Ubuntu ou à de nombreuses autres distributions, le code source ne peut pas être consulté et analysé par le public. En résumé, les principales différences peuvent être regroupées dans les catégories suivantes :

- Système de fichiers
- Gestion des processus
- Gestion des paquets
- Noyau et support matériel
- Surveillance du système
- Sécurité

Pour mieux comprendre les différences, examinons quelques exemples et commandes.

### Informations système

Sur Ubuntu, nous utilisons la commande `uname` pour afficher des informations sur le système, telles que le nom du noyau, le nom d'hôte et le système d'exploitation. Cela peut ressembler à ceci :

```bash
Hiterof13@htb[/htb]$ uname -a
Linux ubuntu 5.4.0-1045 #48-Ubuntu SMP Fri Jan 15 10:47:29 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
```

D'un autre côté, sous Solaris, la commande `showrev` peut être utilisée pour afficher des informations sur le système, y compris la version de Solaris, le type de matériel et le niveau de correctif. Voici un exemple de sortie :

```bash
$ showrev -a

Hostname: solaris
Kernel architecture: sun4u
OS version: Solaris 10 8/07 s10s_u4wos_12b SPARC
Application architecture: sparc
Hardware provider: Sun_Microsystems
Domain: sun.com
Kernel version: SunOS 5.10 Generic_139555-08
```

La principale différence entre les deux commandes est que `showrev` fournit des informations plus détaillées sur le système Solaris, telles que le niveau de correctif et le fournisseur de matériel, tandis que `uname` ne fournit que des informations de base sur le système Linux.

### Installation de paquets

Sur Ubuntu, la commande `apt-get` est utilisée pour installer des paquets. Cela pourrait ressembler à ce qui suit :

```bash
Hiterof13@htb[/htb]$ sudo apt-get install apache2
```

Cependant, sous Solaris, nous devons utiliser `pkgadd` pour installer des paquets comme `SUNWapchr`.

```bash
$ pkgadd -d SUNWapchr
```

La principale différence entre les deux commandes est la syntaxe et le gestionnaire de paquets utilisé. Ubuntu utilise l'outil de paquetage avancé (APT) pour gérer les paquets, tandis que Solaris utilise le gestionnaire de paquets Solaris (SPM). Notez également que nous n'utilisons pas `sudo` dans ce cas. C'est parce que Solaris utilisait l'outil de gestion des privilèges `RBAC`, qui permettait l'attribution de permissions granulaires aux utilisateurs. Cependant, `sudo` est pris en charge depuis Solaris 11.

### Gestion des permissions

Sur les systèmes Linux comme Ubuntu mais aussi sur Solaris, la commande `chmod` est utilisée pour modifier les permissions des fichiers et des répertoires. Voici un exemple de commande pour donner les permissions de lecture, d'écriture et d'exécution au propriétaire du fichier :

```bash
Hiterof13@htb[/htb]$ chmod 700 filename
```

Pour trouver des fichiers avec des permissions spécifiques dans Ubuntu, nous utilisons la commande `find`. Jetons un œil à un exemple de fichier avec le bit SUID positionné :

```bash
Hiterof13@htb[/htb]$ find / -perm 4000
```

Pour trouver des fichiers avec des permissions spécifiques, comme avec le bit SUID positionné sur Solaris, nous pouvons également utiliser la commande find, mais avec un petit ajustement.

```bash
$ find / -perm -4000
```

La principale différence entre ces deux commandes est l'utilisation du `-` avant la valeur de la permission dans la commande Solaris. C'est parce que Solaris utilise un système de permissions différent de celui de Linux.

### NFS sous Solaris

Solaris a sa propre implémentation de NFS, qui est légèrement différente de celle des distributions Linux comme Ubuntu. Sous Solaris, le serveur NFS peut être configuré à l'aide de la commande `share`, qui est utilisée pour partager un répertoire sur le réseau. Elle nous permet également de spécifier diverses options telles que les permissions de lecture/écriture, les restrictions d'accès, etc. Pour partager un répertoire via NFS sous Solaris, nous pouvons utiliser la commande suivante :

```bash
$ share -F nfs -o rw /export/home
```

Cette commande partage le répertoire `/export/home` avec des permissions de lecture et d'écriture via NFS. Un client NFS peut monter le système de fichiers NFS en utilisant la commande `mount`, de la même manière qu'avec Ubuntu. Pour monter un système de fichiers NFS sous Solaris, nous devons spécifier le nom du serveur et le chemin d'accès au répertoire partagé. Par exemple, pour monter un partage NFS depuis un serveur avec l'adresse IP `10.129.15.122` et le répertoire partagé `/nfs_share`, nous utilisons la commande suivante :

```bash
Hiterof13@htb[/htb]$ mount -F nfs 10.129.15.122:/nfs_share /mnt/local
```

Sous Solaris, la configuration de NFS est stockée dans le fichier `/etc/dfs/dfstab`. Ce fichier contient des entrées pour chaque répertoire partagé, ainsi que les différentes options pour le partage NFS.

```bash
# cat /etc/dfs/dfstab

share -F nfs -o rw /export/home
```

### Cartographie des processus

La cartographie des processus est un aspect essentiel de l'administration système et du dépannage. La commande `lsof` est un utilitaire puissant qui liste tous les fichiers ouverts par un processus, y compris les sockets réseau et autres descripteurs de fichiers, que nous pouvons utiliser dans les distributions Debian comme Ubuntu. Nous pouvons utiliser `lsof` pour lister tous les fichiers ouverts par un processus. Par exemple, pour lister tous les fichiers ouverts par le processus du serveur web Apache, nous pouvons utiliser la commande suivante :

```bash
Hiterof13@htb[/htb]$ sudo lsof -c apache2
```

Sous Solaris, la commande `pfiles` peut être utilisée pour lister tous les fichiers ouverts par un processus. Par exemple, pour lister tous les fichiers ouverts par le processus du serveur web Apache, nous pouvons utiliser la commande suivante :

```bash
$ pfiles `pgrep httpd`
```

Cette commande liste tous les fichiers ouverts par le processus du serveur web Apache. La sortie de la commande `pfiles` est similaire à celle de la commande `lsof` et fournit des informations sur le type de descripteur de fichier, le numéro du descripteur de fichier et le nom du fichier.

### Accès aux exécutables

Sous Solaris, on utilise `truss`, un utilitaire très utile pour les développeurs et les administrateurs système qui ont besoin de déboguer des problèmes logiciels complexes sur le système d'exploitation Solaris. En traçant les appels système (system calls) effectués par un processus, `truss` peut aider à identifier la source des erreurs, des problèmes de performance et d'autres problèmes, mais il peut également révéler certaines informations sensibles qui peuvent apparaître lors du développement d'applications ou de la maintenance du système. L'utilitaire peut également fournir des informations détaillées sur les appels système, y compris les arguments qui leur sont passés et leurs valeurs de retour, permettant aux utilisateurs de mieux comprendre le comportement de leurs applications et du système d'exploitation sous-jacent.

`Strace` est une alternative à `truss` mais pour Ubuntu, et c'est un outil essentiel pour les administrateurs système comme pour les développeurs, les aidant à diagnostiquer et à résoudre des problèmes en temps réel. Il permet aux utilisateurs d'analyser les interactions entre le système d'exploitation et les applications qui s'y exécutent, ce qui est particulièrement utile dans des environnements très complexes et critiques. Avec `truss`, les utilisateurs peuvent rapidement identifier et isoler les problèmes liés à la performance des applications, à la connectivité réseau et à l'utilisation des ressources système, entre autres.

Par exemple, pour tracer les appels système effectués par le processus du serveur web Apache, nous pouvons utiliser la commande suivante :

```bash
Hiterof13@htb[/htb]$ sudo strace -p `pgrep apache2`
```

Voici un exemple d'utilisation de `truss` pour tracer les appels système effectués par la commande `ls` sous Solaris :

```bash
$ truss ls

execve("/usr/bin/ls", 0xFFBFFDC4, 0xFFBFFDC8)  argc = 1
...SNIP...
```

La sortie est similaire à celle de `strace`, mais le format est légèrement différent. Une différence entre `strace` et `truss` est que `truss` peut également tracer les signaux envoyés à un processus, alors que `strace` ne le peut pas. Une autre différence est que `truss` a la capacité de tracer les appels système effectués par les processus enfants, tandis que `strace` ne peut tracer que les appels système effectués par le processus spécifié sur la ligne de commande.

---

← [[28 - Journaux système]] | [[00 - Sommaire Linux|Sommaire]] | [[30 - Raccourcis]] →
