---
tags:
  - linux
ordre: 16
---

# Gestion de paquets

Que l'on travaille en tant qu'administrateur système, que l'on maintienne nos propres machines Linux à la maison, ou que l'on construise/mette à jour/maintienne notre distribution de tests d'intrusion (penetration testing) de prédilection, il est crucial de bien maîtriser les gestionnaires de paquets Linux disponibles et les diverses manières de les utiliser pour installer, mettre à jour ou supprimer des paquets. Les paquets sont des archives qui contiennent les binaires des logiciels, les fichiers de configuration, des informations sur les dépendances et qui assurent le suivi des mises à jour et des mises à niveau. Les fonctionnalités que la plupart des systèmes de gestion de paquets fournissent sont :

- Le téléchargement de paquets
- La résolution des dépendances
- Un format de paquet binaire standard
- Des emplacements d'installation et de configuration communs
- Des configurations et fonctionnalités supplémentaires liées au système
- Le contrôle qualité

Nous pouvons utiliser de nombreux systèmes de gestion de paquets différents qui couvrent différents types de fichiers comme « .deb », « .rpm » et autres. L'exigence de la gestion de paquets est que le logiciel à installer soit disponible sous forme de paquet correspondant. Généralement, celui-ci est créé, proposé et maintenu de manière centralisée dans les distributions Linux. De cette manière, le logiciel est directement intégré au système, et ses divers répertoires sont répartis dans tout le système. Le logiciel de gestion de paquets récupère les modifications nécessaires à l'installation système à partir du paquet lui-même, puis met en œuvre ces modifications pour installer le paquet avec succès. Si le logiciel de gestion de paquets reconnaît que des paquets supplémentaires sont requis pour le bon fonctionnement du paquet qui n'ont pas encore été installés, une dépendance est incluse et il avertit l'administrateur ou essaie de recharger le logiciel manquant depuis un dépôt, par exemple, et de l'installer au préalable.

Si un logiciel installé a été supprimé, le système de gestion de paquets reprend alors les informations du paquet, les modifie en fonction de sa configuration et supprime les fichiers. Il existe différents programmes de gestion de paquets que nous pouvons utiliser pour cela. Voici une liste d'exemples de tels programmes :

|**Commande**|**Description**|
|---|---|
|`dpkg`|`dpkg` est un outil pour installer, construire, supprimer et gérer les paquets Debian. L'interface (front-end) principale et plus conviviale pour `dpkg` est aptitude.|
|`apt`|Apt fournit une interface en ligne de commande de haut niveau pour le système de gestion de paquets.|
|`aptitude`|Aptitude est une alternative à apt et est une interface de haut niveau pour le gestionnaire de paquets.|
|`snap`|Installer, configurer, actualiser et supprimer les paquets snap. Les Snaps permettent la distribution sécurisée des dernières applications et utilitaires pour le cloud, les serveurs, les ordinateurs de bureau et l'internet des objets.|
|`gem`|Gem est l'interface (front-end) de RubyGems, le gestionnaire de paquets standard pour Ruby.|
|`pip`|Pip est un installateur de paquets Python recommandé pour installer des paquets Python qui ne sont pas disponibles dans l'archive Debian. Il peut fonctionner avec des dépôts de contrôle de version (actuellement uniquement les dépôts Git, Mercurial et Bazaar), journalise les sorties de manière extensive et empêche les installations partielles en téléchargeant toutes les dépendances avant de commencer l'installation.|
|`git`|Git est un système de contrôle de version distribué, rapide et évolutif, doté d'un jeu de commandes exceptionnellement riche qui offre à la fois des opérations de haut niveau et un accès complet aux composants internes.|

Il est fortement recommandé de configurer notre machine virtuelle (VM) localement pour l'expérimenter. Expérimentons un peu dans notre VM locale et étendons-la avec quelques paquets supplémentaires. D'abord, installons `git` en utilisant `apt`.

---

### Gestionnaire de paquets avancé (APT)

Les distributions Linux basées sur Debian utilisent le gestionnaire de paquets `APT`. Un paquet est un fichier d'archive contenant plusieurs fichiers « .deb ». L'utilitaire `dpkg` est utilisé pour installer des programmes à partir du fichier « .deb » associé. `APT` facilite la mise à jour et l'installation des programmes car de nombreux programmes ont des dépendances. Lors de l'installation d'un programme à partir d'un fichier « .deb » autonome, nous pouvons rencontrer des problèmes de dépendances et avoir besoin de télécharger et d'installer un ou plusieurs paquets supplémentaires. `APT` rend cela plus facile et plus efficace en regroupant toutes les dépendances nécessaires à l'installation d'un programme.

Chaque distribution Linux utilise des dépôts de logiciels qui sont souvent mis à jour. Lorsque nous mettons à jour un programme ou en installons un nouveau, le système interroge ces dépôts pour le paquet souhaité. Les dépôts peuvent être étiquetés comme stables, de test ou instables. La plupart des distributions Linux utilisent le dépôt le plus stable ou « principal » (main). Cela peut être vérifié en consultant le contenu du fichier `/etc/apt/sources.list`. La liste des dépôts pour Parrot OS se trouve dans `/etc/apt/sources.list.d/parrot.list`.

```bash
Hiterof13@htb[/htb]$ cat /etc/apt/sources.list.d/parrot.list
# parrot repository
# this file was automatically generated by parrot-mirror-selector
deb http://htb.deb.parrot.sh/parrot/ rolling main contrib non-free
#deb-src https://deb.parrot.sh/parrot/ rolling main contrib non-free
deb http://htb.deb.parrot.sh/parrot/ rolling-security main contrib non-free
#deb-src https://deb.parrot.sh/parrot/ rolling-security main contrib non-free
```

APT utilise une base de données appelée le cache APT. Il est utilisé pour fournir des informations sur les paquets installés sur notre système hors ligne. Nous pouvons rechercher dans le cache APT, par exemple, pour trouver tous les paquets liés à `Impacket`.

```bash
Hiterof13@htb[/htb]$ apt-cache search impacket
impacket-scripts - Links to useful impacket scripts examples
polenum - Extracts the password policy from a Windows system
python-pcapy - Python interface to the libpcap packet capture library (Python 2)
python3-impacket - Python3 module to easily build and dissect network protocols
python3-pcapy - Python interface to the libpcap packet capture library (Python 3)
```

Nous pouvons ensuite afficher des informations supplémentaires sur un paquet.

```bash
Hiterof13@htb[/htb]$ apt-cache show impacket-scripts
Package: impacket-scripts
Version: 1.4
Architecture: all
Maintainer: Kali Developers <devel@kali.org>
Installed-Size: 13
Depends: python3-impacket (>= 0.9.20), python3-ldap3 (>= 2.5.0), python3-ldapdomaindump
Breaks: python-impacket (<< 0.9.18)
Replaces: python-impacket (<< 0.9.18)
Priority: optional
Section: misc
Filename: pool/main/i/impacket-scripts/impacket-scripts_1.4_all.deb
Size: 2080
<SNIP>
```

Nous pouvons également lister tous les paquets installés.

```bash
Hiterof13@htb[/htb]$ apt list --installed
Listing... Done
accountsservice/rolling,now 0.6.55-2 amd64 [installed,automatic]
adapta-gtk-theme/rolling,now 3.95.0.11-1 all [installed]
adduser/rolling,now 3.118 all [installed]
adwaita-icon-theme/rolling,now 3.36.1-2 all [installed,automatic]
aircrack-ng/rolling,now 1:1.6-4 amd64 [installed,automatic]
<SNIP>
```

S'il nous manque des paquets, nous pouvons les rechercher et les installer à l'aide de la commande suivante.

```bash
Hiterof13@htb[/htb]$ sudo apt install impacket-scripts -y
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following NEW packages will be installed:
  impacket-scripts
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to get 2,080 B of archives.
After this operation, 13.3 kB of additional disk space will be used.
Get:1 https://euro2-emea-mirror.parrot.sh/mirrors/parrot rolling/main amd64 impacket-scripts all 1.4 [2,080 B]
Fetched 2,080 B in 0s (15.2 kB/s)
Selecting previously unselected package impacket-scripts.
(Reading database ... 378459 files and directories currently installed.)
Preparing to unpack .../impacket-scripts_1.4_all.deb ...
Unpacking impacket-scripts (1.4) ...
Setting up impacket-scripts (1.4) ...
Scanning application launchers
Removing duplicate launchers from Debian
Launchers are updated
```

---

## Git

Maintenant que nous avons installé `git`, nous pouvons l'utiliser pour télécharger des outils utiles depuis Github. L'un de ces projets s'appelle 'Nishang'. Nous aborderons et travaillerons avec le projet lui-même plus tard. D'abord, nous devons nous rendre sur le [dépôt du projet](https://github.com/samratashok/nishang) et copier le lien Github avant d'utiliser git pour le télécharger.

![Page GitHub pour 'samratashok/nishang' avec l'URL mise en évidence, le bouton 'Clone or download', et l'URL de clonage 'https://github.com/samratashok/nishangl' affichée.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/git-nishang.png)

Néanmoins, avant de télécharger le projet, ses scripts et ses listes, nous devrions créer un dossier spécifique.

```bash
Hiterof13@htb[/htb]$ mkdir ~/nishang/ && git clone https://github.com/samratashok/nishang.git ~/nishang
Cloning into '/opt/nishang/'...
remote: Enumerating objects: 15, done.
remote: Counting objects: 100% (15/15), done.
remote: Compressing objects: 100% (13/13), done.
remote: Total 1691 (delta 4), reused 6 (delta 2), pack-reused 1676
Receiving objects: 100% (1691/1691), 7.84 MiB | 4.86 MiB/s, done.
Resolving deltas: 100% (1055/1055), done.
```

---

## DPKG

Nous pouvons également télécharger les programmes et les outils des dépôts séparément. Dans cet exemple, nous téléchargeons 'strace' pour Ubuntu 18.04 LTS.

```bash
Hiterof13@htb[/htb]$ wget http://archive.ubuntu.com/ubuntu/pool/main/s/strace/strace_4.21-1ubuntu1_amd64.deb
--2020-05-15 03:27:17--  http://archive.ubuntu.com/ubuntu/pool/main/s/strace/strace_4.21-1ubuntu1_amd64.deb
Resolving archive.ubuntu.com (archive.ubuntu.com)... 91.189.88.142, 91.189.88.152, 2001:67c:1562::18, ...
Connecting to archive.ubuntu.com (archive.ubuntu.com)|91.189.88.142|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 333388 (326K) [application/x-debian-package]
Saving to: ‘strace_4.21-1ubuntu1_amd64.deb’

strace_4.21-1ubuntu1_amd64.deb       100%[===================================================================>] 325,57K  --.-KB/s    in 0,1s

2020-05-15 03:27:18 (2,69 MB/s) - ‘strace_4.21-1ubuntu1_amd64.deb’ saved [333388/333388]
```

De plus, nous pouvons maintenant utiliser à la fois `apt` et `dpkg` pour installer le paquet. Comme nous avons déjà travaillé avec `apt`, nous nous tournerons vers `dpkg` dans l'exemple suivant.

```bash
Hiterof13@htb[/htb]$ sudo dpkg -i strace_4.21-1ubuntu1_amd64.deb
(Reading database ... 154680 files and directories currently installed.)
Preparing to unpack strace_4.21-1ubuntu1_amd64.deb ...
Unpacking strace (4.21-1ubuntu1) over (4.21-1ubuntu1) ...
Setting up strace (4.21-1ubuntu1) ...
Processing triggers for man-db (2.8.3-2ubuntu0.1) ...
```

Avec cela, nous avons déjà installé l'outil et pouvons tester s'il fonctionne correctement.

```bash
Hiterof13@htb[/htb]$ strace -h
usage: strace [-CdffhiqrtttTvVwxxy] [-I n] [-e expr]...
              [-a column] [-o file] [-s strsize] [-P path]...
              -p pid... / [-D] [-E var=val]... [-u username] PROG [ARGS]
   or: strace -c[dfw] [-I n] [-e expr]... [-O overhead] [-S sortby]
              -p pid... / [-D] [-E var=val]... [-u username] PROG [ARGS]

Output format:
  -a column      alignment COLUMN for printing syscall results (default 40)
  -i             print instruction pointer at time of syscall
```

---

← [[15 - Gestion des utilisateurs]] | [[00 - Sommaire Linux|Sommaire]] | [[17 - Gestion des services et des processus]] →
