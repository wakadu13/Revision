---
tags:
  - getting-started
ordre: 6
---

# Outils de base

---

Des outils tels que `SSH`, `Netcat`, `Tmux` et `Vim` sont essentiels et utilisés quotidiennement par la plupart des professionnels de la sécurité de l'information. Bien que ces outils ne soient pas destinés à être des outils de test d'intrusion, ils sont cruciaux pour le processus de test d'intrusion, nous devons donc les maîtriser.

---

## Utilisation de SSH

Le [Secure Shell (SSH)](https://en.wikipedia.org/wiki/SSH_\(Secure_Shell\)) est un protocole réseau qui s'exécute par défaut sur le port `22` et offre aux utilisateurs, tels que les administrateurs système, un moyen sécurisé d'accéder à un ordinateur à distance. SSH peut être configuré avec une authentification par mot de passe ou sans mot de passe en utilisant une [authentification par clé publique](https://serverpilot.io/docs/how-to-use-ssh-public-key-authentication/) via une paire de clés publique/privée SSH. SSH peut être utilisé pour accéder à distance à des systèmes sur le même réseau, sur Internet, pour faciliter les connexions à des ressources sur d'autres réseaux en utilisant la redirection de port/le proxying, et pour téléverser/télécharger des fichiers vers et depuis des systèmes distants.

SSH utilise un modèle client-serveur, connectant un utilisateur exécutant une application cliente SSH telle que `OpenSSH` à un serveur SSH. Lors de l'attaque d'une machine ou d'une évaluation en conditions réelles, nous obtenons souvent des identifiants en clair ou une clé privée SSH qui peuvent être utilisés pour se connecter directement à un système via SSH. Une connexion SSH est généralement beaucoup plus stable qu'une connexion de type shell inversé (reverse shell) et peut souvent être utilisée comme « hôte de rebond » (jump host) pour énumérer et attaquer d'autres hôtes sur le réseau, transférer des outils, mettre en place de la persistance, etc. Si nous obtenons un jeu d'identifiants, nous pouvons utiliser SSH pour nous connecter à distance au serveur en utilisant le nom d'utilisateur `@` l'adresse IP du serveur distant, comme suit :

```bash
Hiterof13@htb[/htb]$ ssh Bob@10.10.10.10  Bob@remotehost's password: *********  Bob@remotehost#
```

Il est également possible de lire des clés privées locales sur un système compromis ou d'ajouter notre clé publique pour obtenir un accès SSH à un utilisateur spécifique, comme nous le verrons dans une section ultérieure. Comme nous pouvons le voir, SSH est un excellent outil pour se connecter de manière sécurisée à une machine distante. Il fournit également un moyen de mapper des ports locaux sur la machine distante vers notre localhost, ce qui peut parfois s'avérer pratique.

---

## Utilisation de Netcat

[Netcat](https://linux.die.net/man/1/nc), `ncat`, ou `nc`, est un excellent utilitaire réseau pour interagir avec les ports TCP/UDP. Il peut être utilisé pour de nombreuses choses lors d'un pentest. Son utilisation principale est la connexion à des shells, que nous aborderons plus loin dans ce module. En plus de cela, `netcat` peut être utilisé pour se connecter à n'importe quel port en écoute et interagir avec le service fonctionnant sur ce port. Par exemple, `SSH` est programmé pour gérer les connexions sur le port 22 afin d'envoyer toutes les données et les clés. Nous pouvons nous connecter au port TCP 22 avec `netcat` :

```bash
Hiterof13@htb[/htb]$ netcat 10.10.10.10 22  SSH-2.0-OpenSSH_8.4p1 Debian-3
```

Comme nous pouvons le voir, le port 22 nous a envoyé sa bannière, indiquant que `SSH` y est en cours d'exécution. Cette technique est appelée `Banner Grabbing` (capture de bannière), et peut aider à identifier quel service fonctionne sur un port particulier. `Netcat` est pré-installé dans la plupart des distributions Linux. Nous pouvons également télécharger une copie pour les machines Windows à partir de ce [lien](https://nmap.org/download.html). Il existe une autre alternative Windows à `netcat` codée en PowerShell appelée [PowerCat](https://github.com/besimorhino/powercat). `Netcat` peut également être utilisé pour transférer des fichiers entre machines, comme nous le verrons plus tard.

Un autre utilitaire réseau similaire est [socat](https://linux.die.net/man/1/socat), qui possède quelques fonctionnalités que `netcat` ne prend pas en charge, comme la redirection de ports et la connexion à des périphériques série. `Socat` peut également être utilisé pour [passer d'un shell simple à un TTY entièrement interactif](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/#method-2-using-socat). Nous en verrons quelques exemples dans une section ultérieure. `Socat` est un utilitaire très pratique qui devrait faire partie de la boîte à outils de tout testeur d'intrusion. Un [binaire autonome](https://github.com/andrew-d/static-binaries) de `Socat` peut être transféré sur un système après avoir obtenu une exécution de code à distance pour obtenir une connexion de type shell inversé plus stable.

---

## Utilisation de Tmux

Les multiplexeurs de terminal, comme `tmux` ou `Screen`, sont d'excellents utilitaires pour étendre les fonctionnalités d'un terminal Linux standard, comme avoir plusieurs fenêtres au sein d'un même terminal et passer de l'une à l'autre. Voyons quelques exemples d'utilisation de `tmux`, qui est le plus courant des deux. Si `tmux` n'est pas présent sur notre système Linux, nous pouvons l'installer avec la commande suivante :

```bash
Hiterof13@htb[/htb]$ sudo apt install tmux -y
```

Une fois que nous avons `tmux`, nous pouvons le démarrer en entrant `tmux` comme commande :![Terminal Parrot avec une invite utilisateur affichant la commande 'tmux'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/getting_started_tmux_1.jpg)

La combinaison de touches par défaut pour entrer les commandes `tmux` est `[CTRL + B]`. Pour ouvrir une nouvelle fenêtre dans `tmux`, nous pouvons appuyer sur le préfixe (c'est-à-dire `[CTRL + B]`) puis sur `C` :![Terminal Parrot avec une invite utilisateur prête pour la saisie.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/getting_started_tmux_2.jpg)

Nous voyons les fenêtres numérotées en bas. Nous pouvons passer à chaque fenêtre en appuyant sur le préfixe puis en entrant le numéro de la fenêtre, comme `0` ou `1`. Nous pouvons également diviser une fenêtre verticalement en volets en appuyant sur le préfixe puis sur `[SHIFT + %]` :![Terminal Parrot avec deux volets, chacun affichant une invite utilisateur prête pour la saisie.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/getting_started_tmux_3.jpg)

Nous pouvons également diviser en volets horizontaux en appuyant sur le préfixe puis sur `[SHIFT + "]` :![Terminal Parrot avec deux volets, chacun affichant une invite utilisateur prête pour la saisie.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/getting_started_tmux_4.jpg)

Nous pouvons basculer entre les volets en appuyant sur le préfixe puis sur les flèches `gauche` ou `droite` pour un basculement horizontal ou sur les flèches `haut` ou `bas` pour un basculement vertical. Les commandes ci-dessus couvrent une utilisation basique de `tmux`. C'est un outil puissant qui peut être utilisé pour de nombreuses choses, y compris la journalisation, ce qui est très important lors de tout engagement technique. Cette [aide-mémoire](https://tmuxcheatsheet.com/) est une référence très pratique. De plus, cette vidéo [Introduction to tmux](https://www.youtube.com/watch?v=Lqehvpe_djs) par `ippsec` vaut le détour.

---

## Utilisation de Vim

[Vim](https://linuxcommand.org/lc3_man_pages/vim1.html) est un excellent éditeur de texte qui peut être utilisé pour écrire du code ou éditer des fichiers texte sur les systèmes Linux. L'un des grands avantages de l'utilisation de `Vim` est qu'il repose entièrement sur le clavier, vous n'avez donc pas à utiliser la souris, ce qui (une fois que nous en aurons pris l'habitude) augmentera considérablement votre productivité et votre efficacité dans l'écriture/l'édition de code. Nous trouvons généralement `Vim` ou `Vi` installés sur les systèmes Linux compromis, donc apprendre à l'utiliser nous permet d'éditer des fichiers même sur des systèmes distants. `Vim` possède également de nombreuses autres fonctionnalités, comme des extensions et des plugins, qui peuvent considérablement étendre son utilisation et en faire un excellent éditeur de code. Voyons quelques-unes des bases de `Vim`. Pour ouvrir un fichier avec `Vim`, nous pouvons ajouter le nom du fichier après la commande :

```bash
Hiterof13@htb[/htb]$ vim /etc/hosts
```

![Terminal Parrot affichant un fichier de configuration avec des paramètres réseau et des commentaires.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/getting_started_vim_1.jpg)

Si nous voulons créer un nouveau fichier, entrez le nom du nouveau fichier, et `Vim` ouvrira une nouvelle fenêtre avec ce fichier. Une fois que nous ouvrons un fichier, nous sommes en `mode normal` (`normal mode`) en lecture seule, ce qui nous permet de naviguer et de lire le fichier. Pour éditer le fichier, nous appuyons sur `i` pour entrer en `mode insertion` (`insert mode`), indiqué par le "`-- INSERT --`" en bas de `Vim`. Ensuite, nous pouvons déplacer le curseur de texte et éditer le fichier :

![Terminal Parrot affichant un fichier de configuration avec des paramètres réseau et des commentaires.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/getting_started_vim_2.jpg)

Une fois que nous avons fini d'éditer un fichier, nous pouvons appuyer sur la touche d'échappement `esc` pour sortir du `mode insertion` et revenir en `mode normal`. Lorsque nous sommes en `mode normal`, nous pouvons utiliser les touches suivantes pour effectuer des raccourcis utiles :

|Commande|Description|
|---|---|
|`x`|Couper un caractère|
|`dw`|Couper un mot|
|`dd`|Couper une ligne complète|
|`yw`|Copier un mot|
|`yy`|Copier une ligne complète|
|`p`|Coller|

Astuce : Nous pouvons multiplier n'importe quelle commande pour l'exécuter plusieurs fois en ajoutant un nombre avant elle. Par exemple, '4yw' copierait 4 mots au lieu d'un, et ainsi de suite.

Si nous voulons enregistrer un fichier ou quitter `Vim`, nous devons appuyer sur `:` pour passer en `mode commande` (`command mode`). Une fois que nous le faisons, nous verrons toutes les commandes que nous tapons en bas de la fenêtre de vim :![Terminal Parrot affichant un fichier de configuration avec des paramètres réseau et des commentaires.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/getting_started_vim_3.jpg)

De nombreuses commandes sont à notre disposition. Voici quelques-unes d'entre elles :

|Commande|Description|
|---|---|
|`:1`|Aller à la ligne numéro 1.|
|`:w`|Écrire le fichier, enregistrer|
|`:q`|Quitter|
|`:q!`|Quitter sans enregistrer|
|`:wq`|Écrire et quitter|

`Vim` est un outil très puissant et possède de nombreuses autres commandes et fonctionnalités. Cette [aide-mémoire](https://vimsheet.com/) est une excellente ressource pour libérer davantage la puissance de `Vim`.
---

← [[05 - Termes Courants]] | [[00 - Sommaire Getting Started|Sommaire]] | [[07 - Analyse de services]] →
