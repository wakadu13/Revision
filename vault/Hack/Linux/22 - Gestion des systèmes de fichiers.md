---
tags:
  - linux
ordre: 22
---

# Gestion des systèmes de fichiers

La gestion des systèmes de fichiers sous Linux est une tâche cruciale qui consiste à organiser, stocker et maintenir les données sur un disque ou un autre périphérique de stockage. Linux est un système d'exploitation polyvalent qui prend en charge de nombreux systèmes de fichiers différents, notamment ext2, ext3, ext4, XFS, Btrfs et NTFS, entre autres. Chacun de ces systèmes de fichiers possède des caractéristiques uniques et est adapté à des cas d'utilisation spécifiques. Le meilleur choix de système de fichiers dépend des exigences spécifiques de l'application ou de l'utilisateur, telles que :

- `ext2` est un ancien système de fichiers sans capacités de journalisation (journaling), ce qui le rend moins adapté aux systèmes modernes mais toujours utile dans certains scénarios à faible surcharge (comme les clés USB).
- `ext3` et `ext4` sont plus avancés, avec la journalisation (qui aide à la récupération après un plantage), et ext4 est le choix par défaut pour la plupart des systèmes Linux modernes car il offre un équilibre entre performance, fiabilité et prise en charge des fichiers volumineux.
- `Btrfs` est connu pour ses fonctionnalités avancées comme la création d'instantanés (snapshotting) et les vérifications d'intégrité des données intégrées, ce qui le rend idéal pour les configurations de stockage complexes.
- `XFS` excelle dans la gestion des fichiers volumineux et offre des performances élevées. Il est particulièrement adapté aux environnements avec de fortes demandes d'E/S.
- `NTFS`, initialement développé pour Windows, est utile pour la compatibilité lors de la gestion de systèmes en double amorçage (dual-boot) ou de disques externes qui doivent fonctionner à la fois sur les systèmes Linux et Windows.

Lors de la sélection d'un système de fichiers, il est essentiel d'analyser les besoins de l'application ou de l'utilisateur. Des facteurs tels que la performance, l'intégrité des données, la compatibilité et les exigences de stockage influenceront la décision.

L'architecture du système de fichiers de Linux est basée sur le modèle Unix, organisé en une structure hiérarchique. Cette structure se compose de plusieurs éléments, le plus essentiel étant les `inodes`. Les `inodes` sont des structures de données qui stockent des métadonnées sur chaque fichier et répertoire, y compris les permissions, la propriété, la taille et les horodatages. Les inodes ne stockent pas les données réelles ou le nom du fichier, mais ils contiennent des pointeurs vers les blocs où les données du fichier sont stockées sur le disque.

La table d'`inodes` est une collection de ces inodes, agissant essentiellement comme une base de données que le noyau Linux utilise pour suivre chaque fichier et répertoire sur le système. Cette structure permet au système d'exploitation d'accéder et de gérer efficacement les fichiers. Comprendre et gérer les inodes est un aspect crucial de la gestion des systèmes de fichiers sous Linux, en particulier dans les scénarios où un disque est à court d'espace d'inodes avant d'être à court de capacité de stockage réelle.

Pour prendre une analogie, pensez au système de fichiers Linux comme à une bibliothèque. Les `inodes` sont comme les fiches du catalogue de la bibliothèque (la table d'`inodes`). Chaque fiche contient des informations détaillées sur un livre (fichier) : son titre, son auteur, son emplacement et d'autres détails, mais pas le livre lui-même. La table d'`inodes` est le catalogue entier qui aide la bibliothèque (le système d'exploitation) à trouver et à gérer rapidement les livres (fichiers).

Sous Linux, les fichiers peuvent être stockés sous l'un de ces types principaux :

- Fichiers ordinaires
- Répertoires
- Liens symboliques

### Fichiers ordinaires

Les fichiers ordinaires sont le type le plus courant et se composent généralement de données texte (comme de l'ASCII) et/ou de données binaires (comme des images, de l'audio ou des exécutables). Ils résident dans divers répertoires à travers le système de fichiers, pas seulement dans le répertoire racine. Le répertoire racine (/) est simplement le sommet de l'arborescence hiérarchique des répertoires, et les fichiers peuvent exister dans n'importe quel répertoire de cette structure.

### Répertoires

Les répertoires sont des types de fichiers spéciaux qui agissent comme des conteneurs pour d'autres fichiers (à la fois des fichiers ordinaires et d'autres répertoires). Lorsqu'un fichier est stocké dans un répertoire, ce répertoire est appelé le répertoire parent du fichier. Les répertoires aident à organiser les fichiers au sein du système de fichiers Linux, permettant une gestion efficace des collections de fichiers.

### Liens symboliques

En plus des fichiers ordinaires et des répertoires, Linux prend également en charge les liens symboliques (`symlinks`), qui agissent comme des raccourcis ou des références vers d'autres fichiers ou répertoires. Les liens symboliques permettent un accès rapide aux fichiers situés dans différentes parties du système de fichiers sans dupliquer le fichier lui-même. Les liens symboliques peuvent être utilisés pour rationaliser l'accès ou organiser des structures de répertoires complexes en pointant vers des fichiers importants à travers divers emplacements.

Chaque catégorie d'utilisateur peut avoir des niveaux de permission différents. Par exemple, le propriétaire d'un fichier peut avoir la permission de le lire, de l'écrire et de l'exécuter, tandis que d'autres peuvent n'avoir que l'accès en lecture. Ces permissions sont indépendantes pour chaque catégorie, ce qui signifie que les modifications des permissions d'un utilisateur n'affectent pas nécessairement les autres.

```bash
Hiterof13@htb[/htb]$ ls -il
total 0
10678872 -rw-r--r--  1 cry0l1t3  htb  234123 Feb 14 19:30 myscript.py
10678869 -rw-r--r--  1 cry0l1t3  htb   43230 Feb 14 11:52 notes.txt
```

---

## Disques et lecteurs

La gestion des disques sous Linux implique la gestion des périphériques de stockage physiques, y compris les disques durs, les disques SSD (solid-state drives) et les périphériques de stockage amovibles. L'outil principal pour la gestion des disques sous Linux est `fdisk`, qui nous permet de créer, supprimer et gérer des partitions sur un disque. Il peut également afficher des informations sur la table de partition, y compris la taille et le type de chaque partition. Le partitionnement d'un disque sous Linux consiste à diviser l'espace de stockage physique en sections logiques distinctes. Chaque partition peut ensuite être formatée avec un système de fichiers spécifique, tel que ext4, NTFS ou FAT32, et peut être montée comme un système de fichiers séparé. Les outils de partitionnement les plus courants sous Linux sont également `fdisk`, `gpart` et `GParted`.

### Fdisk

```bash
Hiterof13@htb[/htb]$ sudo fdisk -l
Disk /dev/vda: 160 GiB, 171798691840 bytes, 335544320 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x5223435f

Device     Boot     Start       End   Sectors  Size Id Type
/dev/vda1  *         2048 158974027 158971980 75.8G 83 Linux
/dev/vda2       158974028 167766794   8792767  4.2G 82 Linux swap / Solaris

Disk /dev/vdb: 452 KiB, 462848 bytes, 904 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

---

## Montage

Chaque partition logique ou disque de stockage doit être assigné à un répertoire spécifique dans le système de fichiers. Ce processus est connu sous le nom de `montage` (`mounting`). Le montage consiste à lier un disque ou une partition à un répertoire, rendant son contenu accessible au sein de la hiérarchie globale du système de fichiers. Une fois qu'un disque est monté sur un répertoire (également appelé point de montage), il peut être accédé et utilisé comme n'importe quel autre répertoire sur le système.

La commande `mount` est couramment utilisée pour monter manuellement des systèmes de fichiers sous Linux. Cependant, si vous souhaitez que certains systèmes de fichiers ou partitions soient automatiquement montés au démarrage du système, vous pouvez les définir dans le fichier `/etc/fstab`. Ce fichier liste les systèmes de fichiers et leurs points de montage associés, ainsi que des options comme les permissions de lecture/écriture et les types de système de fichiers, garantissant que des disques ou partitions spécifiques soient disponibles au démarrage sans nécessiter d'intervention manuelle.

### Systèmes de fichiers montés au démarrage

```bash
Hiterof13@htb[/htb]$ cat /etc/fstab
# /etc/fstab : informations statiques sur le système de fichiers.
#
# Utilisez 'blkid' pour afficher l'identifiant unique universel d'un périphérique ;
# ceci peut être utilisé avec UUID= comme un moyen plus robuste de nommer les périphériques
# qui fonctionne même si des disques sont ajoutés ou retirés. Voir fstab(5).
#
# <file system>                      <mount point>  <type>  <options>  <dump>  <pass>
UUID=3d6a020d-...SNIP...-9e085e9c927a /              btrfs   subvol=@,defaults,noatime,nodiratime,nodatacow,space_cache,autodefrag 0 1
UUID=3d6a020d-...SNIP...-9e085e9c927a /home          btrfs   subvol=@home,defaults,noatime,nodiratime,nodatacow,space_cache,autodefrag 0 2
UUID=21f7eb94-...SNIP...-d4f58f94e141 swap           swap    defaults,noatime 0 0
```

Pour afficher les systèmes de fichiers actuellement montés, nous pouvons utiliser la commande `mount` sans aucun argument. La sortie affichera une liste de tous les systèmes de fichiers actuellement montés, y compris le nom du périphérique, le type de système de fichiers, le point de montage et les options.

### Lister les lecteurs montés

```bash
Hiterof13@htb[/htb]$ mount
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
udev on /dev type devtmpfs (rw,nosuid,relatime,size=4035812k,nr_inodes=1008953,mode=755,inode64)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,nodev,noexec,relatime,size=814580k,mode=755,inode64)
/dev/vda1 on / type btrfs (rw,noatime,nodiratime,nodatasum,nodatacow,space_cache,autodefrag,subvolid=257,subvol=/@)
```

Pour monter un système de fichiers, nous pouvons utiliser la commande `mount` suivie du nom du périphérique et du point de montage. Par exemple, pour monter un lecteur USB avec le nom de périphérique `/dev/sdb1` dans le répertoire `/mnt/usb`, nous utiliserions la commande suivante :

### Monter un lecteur USB

```bash
Hiterof13@htb[/htb]$ sudo mount /dev/sdb1 /mnt/usb
Hiterof13@htb[/htb]$ cd /mnt/usb && ls -l
total 32
drwxr-xr-x 1 root root   18 Oct 14  2021 'Account Takeover'
drwxr-xr-x 1 root root   18 Oct 14  2021 'API Key Leaks'
drwxr-xr-x 1 root root   18 Oct 14  2021 'AWS Amazon Bucket S3'
drwxr-xr-x 1 root root   34 Oct 14  2021 'Command Injection'
drwxr-xr-x 1 root root   18 Oct 14  2021 'CORS Misconfiguration'
drwxr-xr-x 1 root root   52 Oct 14  2021 'CRLF Injection'
drwxr-xr-x 1 root root   30 Oct 14  2021 'CSRF Injection'
drwxr-xr-x 1 root root   18 Oct 14  2021 'CSV Injection'
drwxr-xr-x 1 root root 1166 Oct 14  2021 'CVE Exploits'
...SNIP...
```

Pour démonter un système de fichiers sous Linux, nous pouvons utiliser la commande `umount` suivie du point de montage du système de fichiers que nous voulons démonter. Le point de montage est l'emplacement dans le système de fichiers où le système de fichiers est monté et nous est accessible. Par exemple, pour démonter le lecteur USB qui a été précédemment monté dans le répertoire `/mnt/usb`, nous utiliserions la commande suivante :

### Démonter

```bash
Hiterof13@htb[/htb]$ sudo umount /mnt/usb
```

Il est important de noter que nous devons avoir des permissions suffisantes pour démonter un système de fichiers. Nous ne pouvons pas non plus démonter un système de fichiers qui est utilisé par un processus en cours d'exécution. Pour s'assurer qu'aucun processus en cours n'utilise le système de fichiers, nous pouvons utiliser la commande `lsof` pour lister les fichiers ouverts sur le système de fichiers.

```bash
cry0l1t3@htb:~$ lsof | grep cry0l1t3
vncserver 6006        cry0l1t3  mem       REG      0,24       402274 /usr/bin/perl (path dev=0,26)
vncserver 6006        cry0l1t3  mem       REG      0,24      1554101 /usr/lib/locale/aa_DJ.utf8/LC_COLLATE (path dev=0,26)
vncserver 6006        cry0l1t3  mem       REG      0,24       402326 /usr/lib/x86_64-linux-gnu/perl-base/auto/POSIX/POSIX.so (path dev=0,26)
vncserver 6006        cry0l1t3  mem       REG      0,24       402059 /usr/lib/x86_64-linux-gnu/perl/5.32.1/auto/Time/HiRes/HiRes.so (path dev=0,26)
vncserver 6006        cry0l1t3  mem       REG      0,24      1444250 /usr/lib/x86_64-linux-gnu/libnss_files-2.31.so (path dev=0,26)
vncserver 6006        cry0l1t3  mem       REG      0,24       402327 /usr/lib/x86_64-linux-gnu/perl-base/auto/Socket/Socket.so (path dev=0,26)
vncserver 6006        cry0l1t3  mem       REG      0,24       402324 /usr/lib/x86_64-linux-gnu/perl-base/auto/IO/IO.so (path dev=0,26)
...SNIP...
```

Si nous trouvons des processus qui utilisent le système de fichiers, nous devons les arrêter avant de pouvoir le démonter. Le fichier `/etc/fstab` contient des informations sur les systèmes de fichiers qui doivent être montés sur le système, y compris des options pour le montage automatique au démarrage et d'autres options de montage. Tous les systèmes de fichiers montés (qu'ils soient listés dans `/etc/fstab` ou montés manuellement) seront proprement démontés automatiquement lors de l'arrêt du système par le SE. Si nous voulons empêcher un système de fichiers de se monter automatiquement au démarrage, nous devons ajouter l'option `noauto` à son entrée dans le fichier `/etc/fstab`. Cela ressemblerait, par exemple, à ce qui suit :

### Fichier Fstab

```text
/dev/sda1 / ext4 defaults 0 0
/dev/sda2 /home ext4 defaults 0 0
/dev/sdb1 /mnt/usb ext4 rw,noauto,user 0 0
192.168.1.100:/nfs /mnt/nfs nfs defaults 0 0
```

---

## SWAP

L'espace d'échange (swap) est une partie essentielle de la gestion de la mémoire sous Linux et joue un rôle critique pour assurer une performance système fluide, en particulier lorsque la mémoire physique disponible (RAM) est entièrement utilisée. Lorsque le système manque de mémoire physique, le noyau déplace les pages de mémoire inactives (données non utilisées immédiatement) vers l'espace d'échange, libérant ainsi de la RAM pour les processus actifs. Ce processus est connu sous le nom d'échange (swapping).

### Création d'un espace d'échange

L'espace d'échange peut être configuré soit lors de l'installation du système d'exploitation, soit ajouté ultérieurement à l'aide des commandes mkswap et swapon.

- `mkswap` est utilisé pour préparer un périphérique ou un fichier à être utilisé comme espace d'échange en créant une zone d'échange Linux.
- `swapon` active l'espace d'échange, permettant au système de l'utiliser.

### Dimensionnement et gestion de l'espace d'échange

La taille de l'`espace d'échange` n'est pas fixe et dépend de la mémoire physique de votre système et de l'utilisation prévue. Par exemple, un système avec moins de RAM ou exécutant des applications gourmandes en mémoire pourrait avoir besoin de plus d'espace d'échange. Cependant, les systèmes modernes avec de grandes quantités de RAM peuvent nécessiter moins, voire pas du tout, d'espace d'échange, en fonction des cas d'utilisation spécifiques.

Lors de la configuration de l'espace d'échange, il est important de l'allouer sur une partition ou un fichier dédié, séparé du reste du système de fichiers. Cela évite la fragmentation et assure une utilisation efficace de la zone d'échange en cas de besoin. De plus, comme des données sensibles peuvent être temporairement stockées dans l'espace d'échange, il est recommandé de chiffrer l'espace d'échange pour se prémunir contre une éventuelle exposition de données.

### Espace d'échange pour l'hibernation

En plus d'étendre la mémoire physique, l'espace d'échange est également utilisé pour l'`hibernation`. L'hibernation est une fonctionnalité d'économie d'énergie qui enregistre l'état du système (y compris les applications et processus ouverts) dans l'espace d'échange et éteint le système. Lorsque le système est rallumé, il restaure son état précédent à partir de l'espace d'échange, reprenant exactement là où il s'était arrêté.

---

← [[21 - Sauvegarde et Restauration]] | [[00 - Sommaire Linux|Sommaire]] | [[23 - Conteneurisation]] →
