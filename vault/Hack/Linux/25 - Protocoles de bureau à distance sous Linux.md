---
tags:
  - linux
ordre: 25
---

# Protocoles de bureau à distance sous Linux

Les protocoles de bureau à distance (remote desktop protocols) sont utilisés sous Windows, Linux et macOS pour fournir un accès graphique à distance à un système. Ces protocoles permettent aux administrateurs de gérer, dépanner et mettre à jour les systèmes à distance, ce qui en fait des outils essentiels pour de tels scénarios. Pour ce faire, un administrateur se connecte au système distant en utilisant le protocole approprié en fonction du système d'exploitation qu'il gère.

Par exemple, lorsque les administrateurs doivent installer des logiciels ou gérer un système distant, ils utilisent le protocole pertinent pour établir une session graphique. Deux des protocoles les plus courants pour ce type d'accès sont :

- `Protocole de bureau à distance` (`RDP`) : Principalement utilisé dans les environnements Windows. Le RDP permet aux administrateurs de se connecter à distance et d'interagir avec le bureau d'une machine Windows comme s'ils étaient assis juste devant.
- `Virtual Network Computing` (`VNC`) : Un protocole populaire dans les environnements Linux, bien qu'il soit également multiplateforme. VNC fournit un accès graphique aux bureaux distants, permettant aux administrateurs d'effectuer des tâches sur les systèmes Linux d'une manière similaire à RDP sur Windows.

Imaginez les protocoles de bureau à distance comme ayant différents trousseaux de clés pour différents types de bâtiments. RDP est comme avoir une clé spécialement conçue pour les bâtiments Windows, vous permettant d'accéder et de gérer les pièces (les bureaux) à distance, comme si vous étiez à l'intérieur. VNC, d'autre part, ressemble plus à une clé universelle qui peut fonctionner sur de nombreux bâtiments, mais elle est souvent utilisée pour les structures Linux. Tout comme vous utiliseriez la clé appropriée en fonction du bâtiment, les administrateurs choisissent le bon protocole en fonction du système auquel ils doivent accéder et qu'ils doivent contrôler.

---

## XServer

Le XServer est la partie côté utilisateur du `protocole réseau X Window System` (`X11` / `X`). Le `X11` est un système fixe qui se compose d'un ensemble de protocoles et d'applications qui nous permettent d'appeler des fenêtres d'application sur des écrans dans une interface utilisateur graphique. X11 est prédominant sur les systèmes Unix, mais des serveurs X sont également disponibles pour d'autres systèmes d'exploitation. De nos jours, le XServer fait partie de presque toutes les installations de bureau d'Ubuntu et de ses dérivés et n'a pas besoin d'être installé séparément.

Lorsqu'un bureau est démarré sur un ordinateur Linux, la communication de l'interface utilisateur graphique avec le système d'exploitation se fait via un serveur X. Le réseau interne de l'ordinateur est utilisé, même si l'ordinateur ne se trouve pas dans un réseau. L'aspect pratique du protocole X est la transparence du réseau (network transparency). Ce protocole utilise principalement TCP/IP comme base de transport mais peut également être utilisé sur de purs sockets Unix. Les ports utilisés pour le serveur X se situent généralement dans la plage de `TCP/6001-6009`, permettant la communication entre le client et le serveur. Lors du démarrage d'une nouvelle session de bureau via le serveur X, le port `TCP 6000` serait ouvert pour le premier affichage X `:0`. Cette plage de ports permet au serveur d'effectuer ses tâches telles que l'hébergement d'applications, ainsi que la fourniture de services aux clients. Ils sont souvent utilisés pour fournir un accès à distance à un système, permettant aux utilisateurs d'accéder aux applications et aux données depuis n'importe où dans le monde. De plus, ces ports sont également essentiels pour le partage sécurisé de fichiers et de données, ce qui en fait une partie intégrante de l'Open X Server. Ainsi, un serveur X ne dépend pas de l'ordinateur local, il peut être utilisé pour accéder à d'autres ordinateurs, et d'autres ordinateurs peuvent utiliser le serveur X local. À condition que les ordinateurs locaux et distants contiennent des systèmes Unix/Linux, les protocoles supplémentaires tels que VNC et RDP sont superflus. VNC et RDP génèrent la sortie graphique sur l'ordinateur distant et la transportent sur le réseau. Alors qu'avec X11, le rendu est effectué sur l'ordinateur local. Cela économise du trafic et de la charge sur l'ordinateur distant. Cependant, l'inconvénient majeur de X11 est la transmission de données non chiffrée. Cependant, cela peut être surmonté en tunnelisant le protocole SSH.

Pour cela, nous devons autoriser la redirection X11 (X11 forwarding) dans le fichier de configuration SSH (`/etc/ssh/sshd_config`) sur le serveur qui fournit l'application en changeant cette option à `yes`.

### X11Forwarding

```bash
Hiterof13@htb[/htb]$ cat /etc/ssh/sshd_config | grep X11Forwarding
X11Forwarding yes
```

Avec cela, nous pouvons démarrer l'application depuis notre client avec la commande suivante :

```bash
Hiterof13@htb[/htb]$ ssh -X htb-student@10.129.23.11 /usr/bin/firefox
htb-student@10.129.14.130's password: ********
<SKIP>
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@NIX02' exécutant 'ssh -X htb-student@10.129.2.210 /usr/bin/firefox'. La fenêtre du navigateur Firefox est ouverte, affichant un nouvel onglet.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/xserver.png)

### Sécurité de X11

Comme nous l'avons mentionné précédemment, X11 n'est pas un protocole sécurisé par défaut car sa communication n'est pas chiffrée. En tant que tel, nous devons être attentifs et rechercher ces ports TCP (6000-6010) lorsque nous traitons des cibles basées sur Linux. Sans mesures de sécurité appropriées, un serveur `X` ouvert peut exposer des données sensibles sur le réseau. Par exemple, un attaquant sur le même réseau pourrait lire le contenu des fenêtres du serveur `X` à l'insu de l'utilisateur, rendant même inutile pour eux d'effectuer une analyse de réseau (network sniffing) traditionnelle. Cette vulnérabilité permet de graves failles de sécurité. Un attaquant pourrait potentiellement intercepter des informations sensibles, telles que des mots de passe ou des données personnelles, en utilisant simplement des outils X11 standard comme `xwd` (qui capture des captures d'écran des fenêtres X) et `xgrabsc`.

En plus de cela, d'autres vulnérabilités de sécurité ont été découvertes au fil des ans, relatives aux bibliothèques XServer et au logiciel lui-même. Par exemple, en 2017, un ensemble de vulnérabilités a été trouvé dans XOrg Server, une implémentation open source du X Window System. Provenant de clés de session faibles, prévisibles ou pouvant être forcées par brute-force, dont l'exploitation pourrait permettre à un attaquant d'exécuter du code arbitraire dans la session Xorg d'un autre utilisateur. Un large éventail de systèmes a été affecté, tels que Unix, Red Hat Enterprise Linux, Ubuntu Linux et SUSE Linux. Ces vulnérabilités sont devenues connues sous les noms de CVE-2017-2624, CVE-2017-2625 et CVE-2017-2626. [Cet](https://www.x41-dsec.de/lab/advisories/x41-2017-001-xorg/) article en fournit un excellent résumé.

---

## XDMCP

Le protocole `X Display Manager Control Protocol` (`XDMCP`) est utilisé par le `X Display Manager` pour la communication via le port UDP 177 entre les terminaux X et les ordinateurs fonctionnant sous Unix/Linux. Il est utilisé pour gérer les sessions X Window à distance sur d'autres machines et est souvent utilisé par les administrateurs système Linux pour fournir un accès aux bureaux à distance. XDMCP est un protocole non sécurisé et ne doit pas être utilisé dans un environnement qui exige des niveaux de sécurité élevés. Avec cela, il est possible de rediriger une interface utilisateur graphique (`GUI`) entière (telle que KDE ou Gnome) vers un client correspondant. Pour qu'un système Linux agisse en tant que serveur XDMCP, un système X avec une GUI doit être installé et configuré sur le serveur. Après le démarrage de l'ordinateur, une interface graphique doit être disponible localement pour l'utilisateur.

Une manière potentielle d'exploiter XDMCP est via une attaque de l'homme du milieu (man-in-the-middle attack). Dans ce type d'attaque, un attaquant intercepte la communication entre l'ordinateur distant et le serveur X Window System, et se fait passer pour l'une des parties afin d'obtenir un accès non autorisé au serveur. L'attaquant pourrait alors utiliser le serveur pour exécuter des commandes arbitraires, accéder à des données sensibles ou effectuer d'autres actions qui pourraient compromettre la sécurité du système.

---

## VNC

`Virtual Network Computing` (`VNC`) est un système de partage de bureau à distance basé sur le protocole RFB qui permet aux utilisateurs de contrôler un ordinateur à distance. Il permet à un utilisateur de visualiser et d'interagir avec un environnement de bureau à distance via une connexion réseau. L'utilisateur peut contrôler l'ordinateur distant comme s'il était assis devant. C'est aussi l'un des protocoles les plus courants pour les connexions graphiques à distance pour les hôtes Linux.

VNC est généralement considéré comme sécurisé. Il utilise le chiffrement pour garantir la sécurité des données en transit et requiert une authentification avant qu'un utilisateur puisse y accéder. Les administrateurs utilisent VNC pour accéder à des ordinateurs qui ne sont pas physiquement accessibles. Cela peut être utilisé pour dépanner et maintenir des serveurs, accéder à des applications sur d'autres ordinateurs ou fournir un accès à distance à des postes de travail. VNC peut également être utilisé pour le partage d'écran (screen sharing), permettant à plusieurs utilisateurs de collaborer sur un projet ou de résoudre un problème.

Il existe deux concepts différents pour les serveurs VNC. Le serveur habituel offre l'écran réel de l'ordinateur hôte pour le support utilisateur. Comme le clavier et la souris restent utilisables sur l'ordinateur distant, une coordination est recommandée. Le deuxième groupe de programmes serveur permet la connexion des utilisateurs à des sessions virtuelles, similaire au concept de serveur de terminaux (terminal server).

Des programmes serveur et client (viewer) pour VNC sont disponibles pour tous les systèmes d'exploitation courants. Par conséquent, de nombreux services informatiques sont effectués avec VNC. Les logiciels propriétaires TeamViewer et RDP ont des utilisations similaires.

Traditionnellement, le serveur VNC écoute sur le port TCP 5900. Il y offre donc son `display 0`. D'autres affichages peuvent être proposés via des ports supplémentaires, principalement `590[x]`, où `x` est le numéro de l'affichage. L'ajout de plusieurs connexions serait attribué à un port TCP plus élevé comme 5901, 5902, 5903, etc.

Pour ces connexions VNC, de nombreux outils différents sont utilisés. Parmi eux se trouvent par exemple :

- [TigerVNC](https://tigervnc.org/)
- [TightVNC](https://www.tightvnc.com/)
- [RealVNC](https://www.realvnc.com/en/)
- [UltraVNC](https://uvnc.com/)

Les outils les plus utilisés pour ce type de connexions sont UltraVNC et RealVNC en raison de leur chiffrement et de leur sécurité accrue.

Dans cet exemple, nous mettons en place un serveur `TigerVNC`, et pour cela, nous avons besoin, entre autres, du gestionnaire de bureau `XFCE4` car les connexions VNC avec GNOME sont quelque peu instables. Par conséquent, nous devons installer les paquets nécessaires et créer un mot de passe pour la connexion VNC.

### Installation de TigerVNC

```bash
htb-student@ubuntu:~$ sudo apt install xfce4 xfce4-goodies tigervnc-standalone-server -y
htb-student@ubuntu:~$ vncpasswd
Password: ******
Verify: ******
Would you like to enter a view-only password (y/n)? n
```

Pendant l'installation, un dossier caché est créé dans le répertoire personnel appelé `.vnc`. Ensuite, nous devons créer deux fichiers supplémentaires, `xstartup` et `config`. Le `xstartup` détermine comment la session VNC est créée en lien avec le gestionnaire d'affichage, et le `config` détermine ses paramètres.

### Configuration

```bash
htb-student@ubuntu:~$ touch ~/.vnc/xstartup ~/.vnc/config
htb-student@ubuntu:~$ cat <<EOT >> ~/.vnc/xstartup
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
/usr/bin/startxfce4
[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
x-window-manager &
EOT
```

```bash
htb-student@ubuntu:~$ cat <<EOT >> ~/.vnc/config
geometry=1920x1080
dpi=96
EOT
```

De plus, l'exécutable `xstartup` a besoin des droits pour être démarré par le service.

```bash
htb-student@ubuntu:~$ chmod +x ~/.vnc/xstartup
```

Nous pouvons maintenant démarrer le serveur VNC.

### Démarrer le serveur VNC

```bash
htb-student@ubuntu:~$ vncserver
New 'linux:1 (htb-student)' desktop at :1 on machine linux

Starting applications specified in /home/htb-student/.vnc/xstartup
Log file is /home/htb-student/.vnc/linux:1.log

Use xtigervncviewer -SecurityTypes VncAuth -passwd /home/htb-student/.vnc/passwd :1 to connect to the VNC server.
```

De plus, nous pouvons également afficher l'ensemble des sessions avec les ports associés et l'ID de processus.

### Lister les sessions

```bash
htb-student@ubuntu:~$ vncserver -list
TigerVNC server sessions:

X DISPLAY #     RFB PORT #      PROCESS ID
:1              5901            79746
```

Pour chiffrer la connexion et la rendre plus sûre, nous pouvons créer un tunnel SSH à travers lequel toute la connexion est tunnelisée. Nous apprendrons en détail le fonctionnement du tunneling dans le module [Pivoting, Tunneling, and Port Forwarding](https://academy.hackthebox.com/module/details/158).

### Mise en place d'un tunnel SSH

```bash
Hiterof13@htb[/htb]$ ssh -L 5901:127.0.0.1:5901 -N -f -l htb-student 10.129.14.130
htb-student@10.129.14.130's password: *******
```

Enfin, nous pouvons nous connecter au serveur via le tunnel SSH en utilisant le `xtightvncviewer`.

### Connexion au serveur VNC

```bash
Hiterof13@htb[/htb]$ xtightvncviewer localhost:5901
Connected to RFB server, using protocol version 3.8
Performing standard VNC authentication

Password: ******

Authentication successful
Desktop name "linux:1 (htb-student)"
VNC server default format:
  32 bits per pixel.
  Least significant byte first in each pixel.
  True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0
Using default colormap which is TrueColor.

Pixel format:
  32 bits per pixel.
  Least significant byte first in each pixel.
  True colour: max red 255 green 255 blue 255, shift red 16 green 8 blue 0
Same machine: preferring raw encoding
```

![Bureau affichant une fenêtre de terminal avec l'utilisateur 'htb-student@linux' exécutant la commande 'id'. La sortie affiche l'ID utilisateur, l'ID de groupe et les appartenances aux groupes.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/vncviewer.png)

---

← [[24 - Configuration du Réseau]] | [[00 - Sommaire Linux|Sommaire]] | [[26 - Sécurité Linux]] →
