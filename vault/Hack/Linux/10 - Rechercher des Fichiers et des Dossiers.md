---
tags:
  - linux
ordre: 10
---

# Rechercher des Fichiers et des Dossiers

Il est crucial de pouvoir trouver les fichiers et les dossiers dont nous avons besoin. Une fois que nous avons obtenu l'accès à un système basé sur Linux, il sera essentiel de trouver des fichiers de configuration, des scripts créés par les utilisateurs ou l'administrateur, et d'autres fichiers et dossiers. Nous n'avons pas à parcourir manuellement chaque dossier et à vérifier quand il a été modifié pour la dernière fois. Il existe des outils que nous pouvons utiliser pour faciliter ce travail.

---

## Which

L'un des outils courants est `which`. Cet outil renvoie le chemin vers le fichier ou le lien qui doit être exécuté. Cela nous permet de déterminer si des programmes spécifiques, comme cURL, netcat, wget, python, gcc, sont disponibles sur le système d'exploitation. Utilisons-le pour rechercher Python dans notre instance interactive.

```bash
Hiterof13@htb[/htb]$ which python
/usr/bin/python
```

Si le programme que nous recherchons n'existe pas, aucun résultat ne sera affiché.

---

## Find

Un autre outil pratique est `find`. Outre la fonction de recherche de fichiers et de dossiers, cet outil contient également la fonction de filtrage des résultats. Nous pouvons utiliser des paramètres de filtre comme la taille du fichier ou la date. Nous pouvons également spécifier si nous recherchons uniquement des fichiers ou des dossiers.

### Syntaxe - find

```bash
Hiterof13@htb[/htb]$ find <location> <options>
```

Voyons un exemple de ce à quoi ressemblerait une telle commande avec plusieurs options.

```bash
Hiterof13@htb[/htb]$ find / -type f -name *.conf -user root -size +20k -newermt 2020-03-03 -exec ls -al {} \; 2>/dev/null
-rw-r--r-- 1 root root 136392 Apr 25 20:29 /usr/src/linux-headers-5.5.0-1parrot1-amd64/include/config/auto.conf
-rw-r--r-- 1 root root 82290 Apr 25 20:29 /usr/src/linux-headers-5.5.0-1parrot1-amd64/include/config/tristate.conf
-rw-r--r-- 1 root root 95813 May  7 14:33 /usr/share/metasploit-framework/data/jtr/repeats32.conf
-rw-r--r-- 1 root root 60346 May  7 14:33 /usr/share/metasploit-framework/data/jtr/dynamic.conf
-rw-r--r-- 1 root root 96249 May  7 14:33 /usr/share/metasploit-framework/data/jtr/dumb32.conf
-rw-r--r-- 1 root root 54755 May  7 14:33 /usr/share/metasploit-framework/data/jtr/repeats16.conf
-rw-r--r-- 1 root root 22635 May  7 14:33 /usr/share/metasploit-framework/data/jtr/korelogic.conf
-rwxr-xr-x 1 root root 108534 May  7 14:33 /usr/share/metasploit-framework/data/jtr/john.conf
-rw-r--r-- 1 root root 55285 May  7 14:33 /usr/share/metasploit-framework/data/jtr/dumb16.conf
-rw-r--r-- 1 root root 21254 May  2 11:59 /usr/share/doc/sqlmap/examples/sqlmap.conf
-rw-r--r-- 1 root root 25086 Mar  4 22:04 /etc/dnsmasq.conf
-rw-r--r-- 1 root root 21254 May  2 11:59 /etc/sqlmap/sqlmap.conf
```

Examinons maintenant de plus près les options que nous avons utilisées dans la commande précédente. Si nous survolons les options respectives avec la souris, une petite fenêtre apparaîtra avec une explication. Ces explications se retrouveront également dans d'autres modules, ce qui devrait nous aider si nous ne sommes pas encore familiers avec l'un des outils.

|**Option**|**Description**|
|---|---|
|`-type f`|Ici, nous définissons le type de l'objet recherché. Dans ce cas, '`f`' signifie '`file`' (fichier).|
|`-name *.conf`|Avec '`-name`', nous indiquons le nom du fichier que nous recherchons. L'astérisque (`*`) représente 'tous' les fichiers avec l'extension '`.conf`'.|
|`-user root`|Cette option filtre tous les fichiers dont le propriétaire est l'utilisateur root.|
|`-size +20k`|Nous pouvons ensuite filtrer tous les fichiers localisés et spécifier que nous voulons voir uniquement les fichiers qui sont plus grands que 20 Kio.|
|`-newermt 2020-03-03`|Avec cette option, nous définissons la date. Seuls les fichiers plus récents que la date spécifiée seront présentés.|
|`-exec ls -al {} \;`|Cette option exécute la commande spécifiée, en utilisant les accolades comme espaces réservés (placeholders) pour chaque résultat. L'antislash (backslash) échappe le caractère suivant pour qu'il ne soit pas interprété par le shell, car sinon, le point-virgule mettrait fin à la commande et n'atteindrait pas la redirection.|
|`2>/dev/null`|Il s'agit d'une redirection `STDERR` vers le 'périphérique nul' (`null device`), sur lequel nous reviendrons dans la section suivante. Cette redirection garantit qu'aucune erreur ne s'affiche dans le terminal. Cette redirection ne doit `pas` être une option de la commande 'find'.|

---

## Locate

Rechercher nos fichiers et dossiers dans tout le système pour effectuer de nombreuses recherches différentes prendra beaucoup de temps. La commande `locate` nous offre un moyen plus rapide de faire des recherches dans le système. Contrairement à la commande `find`, `locate` fonctionne avec une base de données locale qui contient toutes les informations sur les fichiers et dossiers existants. Nous pouvons mettre à jour cette base de données avec la commande suivante.

```bash
Hiterof13@htb[/htb]$ sudo updatedb
```

Si nous recherchons maintenant tous les fichiers avec l'extension "`.conf`", vous constaterez que cette recherche produit des résultats beaucoup plus rapidement qu'en utilisant `find`.

```bash
Hiterof13@htb[/htb]$ locate *.conf
/etc/GeoIP.conf
/etc/NetworkManager/NetworkManager.conf
/etc/UPower/UPower.conf
/etc/adduser.conf
<SNIP>
```

Cependant, cet outil ne dispose pas d'autant d'options de filtre que nous pouvons utiliser. Il est donc toujours judicieux de se demander si nous pouvons utiliser la commande `locate` ou si nous devons plutôt utiliser la commande `find`. Tout dépend toujours de ce que nous cherchons.

---

← [[09 - Édition de Fichiers]] | [[00 - Sommaire Linux|Sommaire]] | [[11 - Descripteurs de Fichiers et Redirections]] →
