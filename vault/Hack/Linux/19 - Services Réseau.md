---
tags:
  - linux
ordre: 19
---

# Services Réseau

Lorsque l'on travaille avec Linux, la gestion des différents services réseau est essentielle. La maîtrise de ces services est cruciale pour plusieurs raisons. Les services réseau sont conçus pour effectuer des tâches spécifiques, dont beaucoup permettent des opérations à distance. Il est important d'avoir les connaissances et les compétences nécessaires pour communiquer avec d'autres ordinateurs sur le réseau, établir des connexions, transférer des fichiers, analyser le trafic réseau et configurer ces services efficacement. Cette expertise nous permet d'identifier les vulnérabilités potentielles lors des tests d'intrusion (penetration testing). De plus, la compréhension des options de configuration de chaque service améliore notre compréhension globale de la sécurité réseau.

Imaginons un scénario où nous effectuons un test d'intrusion et rencontrons un hôte Linux en cours d'évaluation pour des vulnérabilités. En surveillant le trafic réseau, nous observons qu'un utilisateur sur cet hôte Linux se connecte à un autre serveur via un serveur FTP non chiffré. Par conséquent, nous sommes en mesure de capturer les identifiants de l'utilisateur en clair. Cette situation serait beaucoup moins probable si l'utilisateur était conscient que le protocole FTP ne chiffre ni les connexions ni les données transmises. Pour un administrateur Linux, cela représente un oubli critique, car non seulement cela expose des faiblesses de sécurité au sein du réseau, mais cela donne également une mauvaise image des administrateurs responsables du maintien de la sécurité du réseau.

Bien qu'il ne soit pas possible de couvrir tous les services réseau, nous nous concentrerons sur les plus importants. Cette approche est bénéfique non seulement pour les administrateurs et les utilisateurs, mais aussi pour les testeurs d'intrusion qui ont besoin de comprendre les interactions entre les différents hôtes et leurs propres systèmes.

---

## SSH

Le Secure Shell (`SSH`) est un protocole réseau qui permet la transmission sécurisée de données et de commandes sur un réseau. Il est largement utilisé pour gérer en toute sécurité des systèmes distants et y accéder pour exécuter des commandes ou transférer des fichiers. Pour se connecter à notre hôte Linux ou à un hôte distant via SSH, un serveur SSH correspondant doit être disponible et en cours d'exécution.

Le serveur SSH le plus couramment utilisé est le serveur OpenSSH. OpenSSH est une implémentation libre et open-source du protocole Secure Shell (SSH) qui permet la transmission sécurisée de données et de commandes sur un réseau.

Les administrateurs utilisent OpenSSH pour gérer en toute sécurité les systèmes distants en établissant une connexion chiffrée vers un hôte distant. Avec OpenSSH, les administrateurs peuvent exécuter des commandes sur des systèmes distants, transférer des fichiers en toute sécurité et établir une connexion à distance sécurisée sans que la transmission de données et de commandes puisse être interceptée par des tiers.

### Installer OpenSSH

```bash
Hiterof13@htb[/htb]$ sudo apt install openssh-server -y
```

Pour vérifier si le serveur est en cours d'exécution, nous pouvons utiliser la commande suivante :

### État du serveur

```bash
Hiterof13@htb[/htb]$ systemctl status ssh
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/system/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2023-02-12 21:15:27 GMT; 1min 22s ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 7740 (sshd)
      Tasks: 1 (limit: 9458)
     Memory: 2.5M
        CPU: 236ms
     CGroup: /system.slice/ssh.service
             └─7740 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups
```

En tant que testeurs d'intrusion, nous utilisons OpenSSH pour accéder en toute sécurité aux systèmes distants lors de la réalisation d'un audit de réseau. Pour ce faire, nous pouvons utiliser la commande suivante :

### SSH - Connexion

```bash
Hiterof13@htb[/htb]$ ssh cry0l1t3@10.129.17.122
The authenticity of host '10.129.17.122 (10.129.17.122)' can't be established.
ECDSA key fingerprint is SHA256:bKzhv+n2pYqr2r...Egf8LfqaHNxk.

Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

Warning: Permanently added '10.129.17.122' (ECDSA) to the list of known hosts.

cry0l1t3@10.129.17.122's password: ***********
```

OpenSSH peut être configuré et personnalisé en modifiant le fichier `/etc/ssh/sshd_config` avec un éditeur de texte. Ici, nous pouvons ajuster des paramètres tels que le nombre maximum de connexions simultanées, l'utilisation de mots de passe ou de clés pour les connexions, la vérification de la clé d'hôte, et plus encore. Cependant, il est important pour nous de noter que les modifications du fichier de configuration d'OpenSSH doivent être effectuées avec soin.

Par exemple, nous pouvons utiliser SSH pour nous connecter en toute sécurité à un système distant et exécuter des commandes ou utiliser la tunnellisation et la redirection de port (port forwarding) pour faire passer des données par un tunnel via une connexion chiffrée afin de vérifier les paramètres réseau et d'autres paramètres système sans que des tiers puissent intercepter la transmission des données et des commandes.

---

## NFS

Le Système de Fichiers en Réseau (Network File System, `NFS`) est un protocole réseau qui nous permet de stocker et de gérer des fichiers sur des systèmes distants comme s'ils étaient stockés sur le système local. Il permet une gestion simple et efficace des fichiers à travers les réseaux. Par exemple, les administrateurs utilisent NFS pour stocker et gérer des fichiers de manière centralisée (pour les systèmes Linux et Windows) afin de faciliter la collaboration et la gestion des données. Pour Linux, il existe plusieurs serveurs NFS, notamment NFS-UTILS (`Ubuntu`), NFS-Ganesha (`Solaris`), et OpenNFS (`Redhat Linux`).

Il peut également être utilisé pour partager et gérer efficacement les ressources, par exemple, pour répliquer des systèmes de fichiers entre serveurs. Il offre également des fonctionnalités telles que des contrôles d'accès, le transfert de fichiers en temps réel et la prise en charge de plusieurs utilisateurs accédant aux données simultanément. Nous pouvons utiliser ce service tout comme le FTP au cas où il n'y aurait pas de client FTP installé sur le système cible, ou si NFS est en cours d'exécution à la place de FTP.

Nous pouvons installer NFS sur Linux avec la commande suivante :

### Installer NFS

```bash
Hiterof13@htb[/htb]$ sudo apt install nfs-kernel-server -y
```

Pour vérifier si le serveur est en cours d'exécution, nous pouvons utiliser la commande suivante :

### État du serveur

```bash
Hiterof13@htb[/htb]$ systemctl status nfs-kernel-server
● nfs-server.service - NFS server and services
     Loaded: loaded (/lib/system/system/nfs-server.service; enabled; vendor preset: enabled)
     Active: active (exited) since Sun 2023-02-12 21:35:17 GMT; 13s ago
    Process: 9234 ExecStartPre=/usr/sbin/exportfs -r (code=exited, status=0/SUCCESS)
    Process: 9235 ExecStart=/usr/sbin/rpc.nfsd $RPCNFSDARGS (code=exited, status=0/SUCCESS)
   Main PID: 9235 (code=exited, status=0/SUCCESS)
        CPU: 10ms
```

Nous pouvons configurer NFS via le fichier de configuration `/etc/exports`. Ce fichier spécifie quels répertoires doivent être partagés et les droits d'accès pour les utilisateurs et les systèmes. Il est également possible de configurer des paramètres tels que la vitesse de transfert et l'utilisation du chiffrement. Les droits d'accès NFS déterminent quels utilisateurs et systèmes peuvent accéder aux répertoires partagés et quelles actions ils peuvent effectuer. Voici quelques droits d'accès importants qui peuvent être configurés dans NFS :

|**Permissions**|**Description**|
|---|---|
|`rw`|Donne aux utilisateurs et aux systèmes les permissions de lecture et d'écriture sur le répertoire partagé.|
|`ro`|Donne aux utilisateurs et aux systèmes un accès en lecture seule au répertoire partagé.|
|`no_root_squash`|Empêche l'utilisateur root sur le client d'être restreint aux droits d'un utilisateur normal.|
|`root_squash`|Restreint les droits de l'utilisateur root sur le client aux droits d'un utilisateur normal.|
|`sync`|Synchronise le transfert de données pour garantir que les modifications ne sont transférées qu'après avoir été enregistrées sur le système de fichiers.|
|`async`|Transfère les données de manière asynchrone, ce qui accélère le transfert, mais peut entraîner des incohérences dans le système de fichiers si les modifications n'ont pas été entièrement validées.|

Par exemple, nous pouvons créer un nouveau dossier et le partager temporairement dans NFS. Nous le ferions comme suit :

### Créer un partage NFS

```bash
cry0l1t3@htb:~$ mkdir nfs_sharing
cry0l1t3@htb:~$ echo '/home/cry0l1t3/nfs_sharing hostname(rw,sync,no_root_squash)' >> /etc/exports
cry0l1t3@htb:~$ cat /etc/exports | grep -v "#"
/home/cry0l1t3/nfs_sharing hostname(rw,sync,no_root_squash)
```

Si nous avons créé un partage NFS et que nous voulons travailler avec celui-ci sur le système cible, nous devons d'abord le monter. Nous pouvons le faire avec la commande suivante :

### Monter un partage NFS

```bash
cry0l1t3@htb:~$ mkdir ~/target_nfs
cry0l1t3@htb:~$ mount 10.129.12.17:/home/john/dev_scripts ~/target_nfs
cry0l1t3@htb:~$ tree ~/target_nfs
target_nfs/
├── css.css
├── html.html
├── javascript.js
├── php.php
└── xml.xml

0 directories, 5 files
```

Nous avons donc monté le partage NFS (`dev_scripts`) de notre cible (`10.129.12.17`) localement sur notre système dans le point de montage `target_nfs` sur le réseau et pouvons voir le contenu comme si nous étions sur le système cible. Il existe même certaines méthodes qui peuvent être utilisées dans des cas spécifiques pour élever nos privilèges sur le système distant en utilisant NFS.

---

## Serveur Web

Comprendre le fonctionnement des serveurs web est essentiel pour les testeurs d'intrusion, car ces serveurs font partie intégrante des applications web et servent fréquemment de cibles principales lors des évaluations de sécurité. Un serveur web est un logiciel qui fournit des données, des documents, des applications et diverses fonctions sur Internet. Il utilise le protocole de transfert hypertexte (Hypertext Transfer Protocol, `HTTP`) pour transmettre des données à des clients tels que des navigateurs web et pour recevoir des requêtes de ces clients. Les données reçues sont ensuite rendues sous forme de langage de balisage hypertexte (Hypertext Markup Language, `HTML`) dans le navigateur du client, facilitant la création de pages web dynamiques qui répondent de manière interactive aux requêtes des utilisateurs. Par conséquent, une compréhension approfondie des fonctionnalités du serveur web est vitale pour développer des applications web sécurisées et efficaces et pour maintenir la sécurité globale du système. Parmi les serveurs web les plus utilisés sur les plateformes Linux figurent Apache, Nginx, Lighttpd et Caddy, Apache étant particulièrement populaire en raison de sa large compatibilité avec des systèmes d'exploitation tels qu'Ubuntu, Solaris et Red Hat Linux.

Pour les testeurs d'intrusion, les serveurs web offrent diverses utilités. Ils peuvent être employés pour faciliter les transferts de fichiers, permettant aux testeurs de se connecter et d'interagir avec les systèmes cibles via les ports HTTP ou HTTPS. De plus, les serveurs web peuvent être exploités pour mener des attaques de phishing en hébergeant des répliques de pages cibles, tentant ainsi de capturer les identifiants des utilisateurs. Au-delà de ces applications, les serveurs web offrent de nombreuses autres opportunités pour tester et exploiter les vulnérabilités au sein d'un réseau.

Le serveur web Apache dispose d'une variété de fonctionnalités qui nous permettent d'héberger une application web sécurisée et efficace. De plus, nous pouvons également configurer la journalisation pour obtenir des informations sur le trafic de notre serveur, ce qui nous aide à analyser les attaques. Nous pouvons installer Apache en utilisant la commande suivante :

### Installer le serveur Web Apache

```bash
Hiterof13@htb[/htb]$ sudo apt install apache2 -y
```

Pour Apache2, pour spécifier les dossiers accessibles, nous pouvons modifier le fichier `/etc/apache2/apache2.conf` avec un éditeur de texte. Ce fichier contient les paramètres globaux. Nous pouvons modifier les paramètres pour spécifier quels répertoires peuvent être consultés et quelles actions peuvent être effectuées sur ces répertoires.

### Configuration d'Apache

```apache
<Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
</directory>
```

Cette section spécifie que le dossier par défaut `/var/www/html` est accessible, que les utilisateurs peuvent utiliser les options `Indexes` et `FollowSymLinks`, que les modifications des fichiers dans ce répertoire peuvent être outrepassées avec `AllowOverride All`, et que `Require all granted` accorde à tous les utilisateurs l'accès à ce répertoire. Par exemple, si nous voulons transférer des fichiers vers l'un de nos systèmes cibles à l'aide d'un serveur web, nous pouvons placer les fichiers appropriés dans le dossier `/var/www/html` et utiliser `wget` ou `curl` ou d'autres applications pour télécharger ces fichiers sur le système cible.

Il est également possible de personnaliser les paramètres individuels au niveau du répertoire en utilisant le fichier `.htaccess`, que nous pouvons créer dans le répertoire en question. Ce fichier nous permet de configurer certains paramètres au niveau du répertoire, tels que les contrôles d'accès, sans avoir à personnaliser le fichier de configuration d'Apache. Nous pouvons également ajouter des modules pour obtenir des fonctionnalités comme `mod_rewrite`, `mod_security`, et `mod_ssl` qui nous aident à améliorer la sécurité de notre application web.

Le serveur web Python est une alternative simple et rapide à Apache et peut être utilisé pour héberger un seul dossier avec une seule commande afin de transférer des fichiers vers un autre système. Pour installer le serveur web Python, nous devons installer Python3 sur notre système, puis exécuter la commande suivante :

### Installer Python & le serveur Web

```bash
Hiterof13@htb[/htb]$ sudo apt install python3 -y
Hiterof13@htb[/htb]$ python3 -m http.server
```

Lorsque nous exécutons cette commande, notre serveur web Python sera démarré sur le port `TCP/8000`, et nous pourrons accéder au dossier dans lequel nous nous trouvons actuellement. Nous pouvons également héberger un autre dossier avec la commande suivante :

```bash
Hiterof13@htb[/htb]$ python3 -m http.server --directory /home/cry0l1t3/target_files
```

Cela démarrera un serveur web Python sur le port `TCP/8000`, et nous pourrons accéder au dossier `/home/cry0l1t3/target_files` depuis le navigateur, par exemple. Lorsque nous accédons à notre serveur web Python, nous pouvons transférer des fichiers vers l'autre système en tapant le lien dans notre navigateur et en téléchargeant les fichiers. Nous pouvons également héberger notre serveur web Python sur un port autre que le port par défaut :

```bash
Hiterof13@htb[/htb]$ python3 -m http.server 443
```

Cela hébergera notre serveur web Python sur le port 443 au lieu du port par défaut `TCP/8000`. Nous pouvons accéder à ce serveur web en tapant le lien dans notre navigateur.

---

## VPN

Un Réseau Privé Virtuel (Virtual Private Network, `VPN`) fonctionne comme un tunnel sécurisé et invisible qui nous connecte à un autre réseau, permettant un accès transparent et protégé comme si nous y étions physiquement présents. Ceci est réalisé en établissant un tunnel chiffré entre le client et le serveur, garantissant que toutes les données transmises via cette connexion restent confidentielles et protégées contre tout accès non autorisé.

Les organisations utilisent principalement les VPN pour accorder à leurs employés un accès sécurisé au réseau interne sans qu'ils aient besoin d'être sur site. Cette flexibilité permet aux employés d'accéder aux ressources et applications internes depuis n'importe quel endroit, améliorant ainsi la productivité et la mobilité. De plus, les VPN servent à anonymiser le trafic Internet et à bloquer les intrusions externes, renforçant ainsi davantage la sécurité.

Parmi les solutions VPN les plus utilisées pour les serveurs Linux figurent OpenVPN, L2TP/IPsec, PPTP, SSTP et SoftEther. OpenVPN se distingue comme une option open-source populaire compatible avec divers systèmes d'exploitation, notamment Ubuntu, Solaris et Red Hat Linux. Les administrateurs exploitent OpenVPN pour faciliter l'accès à distance sécurisé aux réseaux d'entreprise, chiffrer le trafic réseau et préserver l'anonymat des utilisateurs en ligne.

Pour les testeurs d'intrusion, OpenVPN offre des capacités inestimables. Il permet aux testeurs de se connecter en toute sécurité aux réseaux internes, en particulier lorsque l'accès direct n'est pas possible en raison de contraintes géographiques. En utilisant OpenVPN, les testeurs d'intrusion peuvent effectuer des évaluations de sécurité complètes des systèmes internes, en identifiant et en traitant les vulnérabilités potentielles. La polyvalence d'OpenVPN, avec des fonctionnalités telles que le chiffrement, la tunnellisation, la mise en forme du trafic (traffic shaping), le routage réseau et l'adaptabilité aux environnements réseau dynamiques, en fait un outil essentiel dans l'arsenal des administrateurs réseau et des professionnels de la sécurité. Nous pouvons installer le serveur et le client avec la commande suivante :

### Installer OpenVPN

```bash
Hiterof13@htb[/htb]$ sudo apt install openvpn -y
```

OpenVPN peut être personnalisé et configuré en modifiant le fichier de configuration `/etc/openvpn/server.conf`. Ce fichier contient les paramètres du serveur OpenVPN. Nous pouvons modifier les paramètres pour configurer certaines fonctionnalités telles que le chiffrement, la tunnellisation, la mise en forme du trafic, etc.

Si nous voulons nous connecter à un serveur OpenVPN, nous pouvons utiliser le fichier `.ovpn` que nous avons reçu du serveur et le sauvegarder sur notre système. Nous pouvons le faire avec la commande suivante sur la ligne de commande :

### Se connecter au VPN

```bash
Hiterof13@htb[/htb]$ sudo openvpn --config internal.ovpn
```

Une fois la connexion établie, nous pouvons communiquer avec les hôtes internes sur le réseau interne.

---

← [[18 - Planification de tâches]] | [[00 - Sommaire Linux|Sommaire]] | [[20 - Travailler avec les services web]] →
