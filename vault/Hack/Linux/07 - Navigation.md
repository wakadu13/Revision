---
tags:
  - linux
ordre: 7
---

# Navigation

La navigation est essentielle, tout comme le travail avec la souris pour un utilisateur standard de Windows. Grâce à elle, nous nous déplaçons dans le système et travaillons dans les répertoires et avec les fichiers dont nous avons besoin et que nous voulons. Par conséquent, nous utilisons différentes commandes et outils pour afficher des informations sur un répertoire ou un fichier et pouvons utiliser des options avancées pour optimiser l'affichage selon nos besoins.

L'une des meilleures façons d'apprendre quelque chose de nouveau est d'expérimenter. Ici, nous couvrons les sections sur la navigation dans Linux, la création, le déplacement, la modification et la suppression de fichiers et de dossiers, leur recherche sur le système d'exploitation, les différents types de redirections, et ce que sont les descripteurs de fichiers (file descriptors). Nous trouverons également des raccourcis pour rendre notre travail avec le shell beaucoup plus facile et plus confortable. Nous vous recommandons d'expérimenter sur notre VM hébergée localement. Assurez-vous d'avoir créé un instantané (snapshot) de votre VM au cas où votre système serait endommagé de manière inattendue.

Commençons par la navigation. Avant de nous déplacer dans le système, nous devons savoir dans quel répertoire nous nous trouvons. Nous pouvons le découvrir avec la commande `pwd`.

```bash
cry0l1t3@htb[~]$ pwd
/home/cry0l1t3
```

Seule la commande `ls` est nécessaire pour lister tout le contenu d'un répertoire. Elle dispose de nombreuses options supplémentaires qui peuvent compléter l'affichage du contenu du dossier actuel.

```bash
cry0l1t3@htb[~]$ ls
Desktop  Documents  Downloads  Music  Pictures  Public  Templates  Videos
```

L'utiliser sans aucune option supplémentaire n'affichera que les répertoires et les fichiers. Cependant, nous pouvons également ajouter l'option `-l` pour afficher plus d'informations sur ces répertoires et fichiers.

```bash
cry0l1t3@htb[~]$ ls -l
total 32
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:37 Desktop
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Documents
drwxr-xr-x 3 cry0l1t3 htbacademy 4096 Nov 15 03:26 Downloads
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Music
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Pictures
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Public
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Templates
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Videos
```

Premièrement, nous voyons le nombre total de blocs (de 1024 octets) utilisés par les fichiers et répertoires listés dans le répertoire courant, ce qui indique la taille totale utilisée. Cela signifie qu'il a utilisé 32 blocs * 1024 octets/bloc = 32 768 octets (ou 32 Ko) d'espace disque. Ensuite, nous voyons quelques colonnes qui sont structurées comme suit :

|**Contenu de la colonne**|**Description**|
|---|---|
|`drwxr-xr-x`|Type et permissions|
|`2`|Nombre de liens durs (hard links) vers le fichier/répertoire|
|`cry0l1t3`|Propriétaire du fichier/répertoire|
|`htbacademy`|Groupe propriétaire du fichier/répertoire|
|`4096`|Taille du fichier ou nombre de blocs utilisés pour stocker les informations du répertoire|
|`Nov 13 17:37`|Date et heure|
|`Desktop`|Nom du répertoire|

Cependant, nous ne verrons pas tout ce qui se trouve dans ce dossier. Un répertoire peut aussi avoir des fichiers cachés qui commencent par un point au début de leur nom (par ex., `.bashrc` ou `.bash_history`). Par conséquent, nous devons utiliser la commande `ls -la` pour `lister tout` (`list all`) le contenu d'un répertoire :

```bash
cry0l1t3@htb[~]$ ls -la
total 403188
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:37 .bash_history
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:37 .bashrc
...SNIP...
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:37 Desktop
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Documents
drwxr-xr-x 3 cry0l1t3 htbacademy 4096 Nov 15 03:26 Downloads
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Music
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Pictures
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Public
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Templates
drwxr-xr-x 2 cry0l1t3 htbacademy 4096 Nov 13 17:34 Videos
```

Pour lister le contenu d'un répertoire, nous n'avons pas nécessairement besoin de nous y rendre d'abord. Nous pouvons aussi utiliser « `ls` » pour spécifier le chemin dont nous voulons connaître le contenu.

```bash
cry0l1t3@htb[~]$ ls -l /var/
total 52
drwxr-xr-x  2 root root     4096 Mai 15 18:54 backups
drwxr-xr-x 18 root root     4096 Nov 15 16:55 cache
drwxrwsrwt  2 root whoopsie 4096 Jul 25  2018 crash
drwxr-xr-x 66 root root     4096 Mai 15 03:08 lib
drwxrwsr-x  2 root staff    4096 Nov 24  2018 local
<SNIP>
```

Nous pouvons faire la même chose pour nous rendre dans le répertoire. Pour se déplacer entre les répertoires, nous utilisons la commande `cd`. Changeons pour le répertoire `/dev/shm`. Bien sûr, nous pourrions d'abord aller dans le répertoire `/dev` puis dans `/shm`. Néanmoins, nous pouvons aussi entrer le chemin complet et y sauter directement.

```bash
cry0l1t3@htb[~]$ cd /dev/shm
cry0l1t3@htb[/dev/shm]$
```

Comme nous étions dans le répertoire personnel (home) auparavant, nous pouvons rapidement revenir au dernier répertoire où nous étions.

```bash
cry0l1t3@htb[/dev/shm]$ cd -
cry0l1t3@htb[~]$
```

Le shell nous offre également la fonction d'auto-complétion, ce qui facilite la navigation. Si nous tapons maintenant `cd /dev/s` et appuyons sur `[TAB] deux fois`, nous obtiendrons toutes les entrées commençant par la lettre « `s` » dans le répertoire `/dev/`.

```bash
cry0l1t3@htb[~]$ cd /dev/s [TAB 2x]
shm/ snd/
```

Si nous ajoutons la lettre « `h` » à la lettre « `s` », le shell complètera la saisie car il n'y aura pas d'autres dossiers dans ce répertoire commençant par les lettres « `sh` ». Si nous affichons maintenant tout le contenu du répertoire, nous ne verrons que le contenu suivant.

```bash
cry0l1t3@htb[/dev/shm]$ ls -la /dev/shm
total 0
drwxrwxrwt  2 root root   40 Mai 15 18:31 .
drwxr-xr-x 17 root root 4000 Mai 14 20:45 ..
```

La première entrée avec un seul point (`.`) indique le répertoire actuel dans lequel nous nous trouvons. La deuxième entrée avec deux points (`..`) représente le répertoire parent `/dev`. Cela signifie que nous pouvons sauter vers le répertoire parent avec la commande suivante.

```bash
cry0l1t3@htb[/dev/shm]$ cd ..
cry0l1t3@htb[/dev]$
```

Comme notre shell est rempli de quelques enregistrements, nous pouvons le nettoyer avec la commande `clear`. Cependant, retournons d'abord dans le répertoire `/dev/shm` avant d'exécuter la commande `clear` pour nettoyer notre terminal.

```bash
cry0l1t3@htb[/dev]$ cd shm && clear
```

Une autre façon de nettoyer notre terminal est d'utiliser le raccourci `[Ctrl] + [L]`. Nous pouvons également utiliser les touches fléchées (`↑` ou `↓`) pour faire défiler l'historique des commandes, ce qui nous montrera les commandes que nous avons utilisées auparavant. Mais nous pouvons aussi rechercher dans l'historique des commandes en utilisant le raccourci `[Ctrl] + [R]` et en tapant une partie du texte que nous recherchons.

---

← [[06 - Informations système]] | [[00 - Sommaire Linux|Sommaire]] | [[08 - Travailler avec les Fichiers et les Répertoires]] →
