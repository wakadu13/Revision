---
tags:
  - getting-started
ordre: 20
---

# Écueils courants

---

Lors de la réalisation de tests d'intrusion ou de l'attaque de machines/laboratoires HTB, nous pouvons commettre de nombreuses erreurs courantes qui entraveront notre progression. Dans cette section, nous aborderons certains de ces écueils courants et la manière de les surmonter.

---

## Problèmes de VPN

Nous pouvons parfois rencontrer des problèmes liés aux connexions VPN au réseau des laboratoires HTB. Tout d'abord, nous devons nous assurer que nous sommes bien connectés au réseau HTB.

#### Toujours connecté au VPN

La méthode la plus simple pour vérifier si nous nous sommes connectés avec succès au réseau VPN est de vérifier si le message `Initialization Sequence Completed` apparaît à la fin des messages de notre connexion VPN :

```bash
Hiterof13@htb[/htb]$ sudo openvpn ./htb.ovpn  ...SNIP...  Initialization Sequence Completed
```

#### Obtenir l'adresse VPN

Une autre façon de vérifier si nous sommes connectés au réseau VPN est de vérifier notre adresse VPN `tun0`, que nous pouvons trouver avec la commande suivante :

```bash
Hiterof13@htb[/htb]$ ip -4 a show tun0  6: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 500     inet 10.10.10.1/23 scope global tun0        valid_lft forever preferred_lft forever
```

Tant que nous récupérons notre adresse IP, nous devrions être connectés au réseau VPN.

#### Vérifier la table de routage

Une autre façon de vérifier la connectivité est d'utiliser la commande `sudo netstat -rn` pour afficher notre table de routage :

```bash
Hiterof13@htb[/htb]$ sudo netstat -rn
[sudo] password for user:   Kernel IP routing table Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface 0.0.0.0         192.168.195.2   0.0.0.0         UG        0 0          0 eth0 10.10.14.0      0.0.0.0         255.255.254.0   U         0 0          0 tun0 10.129.0.0      10.10.14.1      255.255.0.0     UG        0 0          0 tun0 192.168.1.0   0.0.0.0         255.255.255.0   U         0 0          0 eth0
```

#### Pinger la passerelle

À partir de là, nous pouvons voir que nous sommes connectés au réseau `10.10.14.0/23` sur l'adaptateur `tun0` et que nous avons accès au réseau `10.129.0.0/16`. Nous pouvons pinger la passerelle `10.10.14.1` pour confirmer l'accès.

```bash
Hiterof13@htb[/htb]$ ping -c 4 10.10.14.1 PING 10.10.14.1 (10.10.14.1) 56(84) bytes of data. 64 bytes from 10.10.14.1: icmp_seq=1 ttl=64 time=111 ms 64 bytes from 10.10.14.1: icmp_seq=2 ttl=64 time=111 ms 64 bytes from 10.10.14.1: icmp_seq=3 ttl=64 time=111 ms 64 bytes from 10.10.14.1: icmp_seq=4 ttl=64 time=111 ms  --- 10.10.14.1 ping statistics --- 4 packets transmitted, 4 received, 0% packet loss, time 3012ms rtt min/avg/max/mdev = 110.574/110.793/111.056/0.174 ms
```

Enfin, nous pouvons soit attaquer un hôte cible assigné sur le réseau 10.129.0.0/16, soit commencer l'énumération des hôtes actifs.

#### Travailler sur deux appareils

Le VPN HTB ne peut pas être connecté à plus d'un appareil simultanément. Si nous sommes connectés sur un appareil et que nous essayons de nous connecter depuis un autre appareil, la deuxième tentative de connexion échouera.

Par exemple, cela peut se produire lorsque notre connexion VPN est établie dans notre PwnBox, et que nous essayons ensuite de nous y connecter depuis notre VM Parrot en même temps. Ou encore, nous sommes peut-être connectés sur notre VM Parrot, puis nous voulons passer à une VM Windows pour tester quelque chose.

#### Vérifier la région

Si nous ressentons un décalage notable dans notre connexion VPN, comme une latence dans les pings ou les connexions ssh, nous devons nous assurer que nous sommes connectés à la région la plus appropriée. HTB fournit des serveurs VPN dans le monde entier, en `Europe`, aux `États-Unis`, en `Australie` et à `Singapour`. Idéalement, il serait utile d'essayer de se connecter au serveur le plus proche de nous pour obtenir la meilleure connexion possible.

Pour changer notre serveur VPN, allez sur [HackTheBox](https://app.hackthebox.eu/home), cliquez sur l'icône en haut à droite qui indique `Lab Access` ou `Offline`, cliquez sur `Labs`, puis sur `OpenVPN`. Une fois que c'est fait, nous devrions pouvoir choisir l'emplacement de notre serveur VPN et sélectionner n'importe lequel des serveurs de cette région :

https://app.hackthebox.eu/home

![Tableau de bord Hack The Box avec 801 joueurs en ligne, statistiques des machines et des challenges, et options de connexion VPN.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_vpn.jpg)

Remarque : Les utilisateurs disposant d'un abonnement gratuit ne peuvent se connecter qu'à 1 à 3 serveurs gratuits dans chaque région. Les utilisateurs disposant d'un abonnement VPN peuvent se connecter aux serveurs VIP, qui offrent une connexion plus rapide avec moins de trafic.

#### Dépannage du VPN

En cas de problèmes techniques lors de la connexion au VPN, nous pouvons trouver des conseils détaillés sur le dépannage des connexions VPN sur cette [page d'aide de HackTheBox](https://help.hackthebox.eu/troubleshooting/v2-vpn-connection-troubleshooting).

---

## Problèmes avec le proxy Burp Suite

[Burp Suite](https://portswigger.net/burp/communitydownload) est un outil crucial lors des tests d'intrusion d'applications web (ainsi que pour d'autres types d'évaluations). Burp Suite est un proxy d'application web et peut causer quelques problèmes sur nos systèmes.

#### Ne pas désactiver le proxy

Lorsque nous activons le proxy Burp dans notre navigateur, Burp commence à capturer notre trafic et à intercepter nos requêtes. Cela aura pour effet de bloquer toutes les requêtes que nous faisons dans le navigateur, c'est-à-dire la visite d'une page, jusqu'à ce que nous allions dans Burp, examinions la requête et la transmettions.

Un écueil courant est d'oublier de désactiver le proxy du navigateur après avoir fermé Burp, de sorte qu'il continue à intercepter nos requêtes. Si cela se produit, nous constaterons que notre navigateur ne charge aucune page. Nous devrions donc vérifier si le proxy du navigateur est toujours activé. Nous pouvons le faire en cliquant sur l'icône du plugin `Foxy Proxy` dans `Firefox`, et en nous assurant qu'il est réglé sur `Turn Off` (Désactiver) :

![Interface de FoxyProxy avec les options 'Options', 'What's My IP?', et 'Log'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/30/foxyproxy_options.jpg)

Si nous n'utilisons pas un plugin comme `Foxy Proxy`, nous pouvons vérifier les paramètres de connexion du navigateur et nous assurer que le proxy est désactivé. Une fois que c'est fait, nous devrions pouvoir continuer à naviguer sans aucun problème.

---

## Changer la clé et le mot de passe SSH

Si nous commençons à rencontrer des problèmes pour nous connecter à des serveurs SSH ou pour nous connecter à notre machine depuis un serveur distant, nous pouvons vouloir renouveler ou changer notre clé SSH et notre mot de passe pour nous assurer qu'ils ne sont pas à l'origine de problèmes. Nous pouvons le faire avec la commande `ssh-keygen`, comme suit :

```bash
Hiterof13@htb[/htb]$ ssh-keygen  Generating public/private rsa key pair. Enter file in which to save the key (/home/parrot/.ssh/id_rsa):  Enter passphrase (empty for no passphrase): Enter same passphrase again:  Your identification has been saved in /home/parrot/.ssh/id_rsa Our public key has been saved in /home/parrot/.ssh/id_rsa.pub The key fingerprint is: SHA256:...SNIP... parrot@parrot The key's randomart image is: +---[RSA 3072]----+ |            o..  | |     ...SNIP     | |     ...SNIP     | |     ...SNIP     | |     ...SNIP     | |     ...SNIP     | |     ...SNIP     | |       + +oo+o   | +----[SHA256]-----+
```

Par défaut, les clés SSH sont stockées dans le dossier `.ssh` de notre répertoire personnel (par exemple, `/home/htb-student/.ssh`). Si nous voulions créer une clé ssh dans un répertoire différent, nous pourrions saisir un chemin absolu pour la clé lorsque cela nous est demandé. Nous pouvons chiffrer notre clé SSH avec une phrase de passe lorsque cela nous est demandé, ou la laisser vide si nous ne voulons pas en utiliser.
---

← [[19 - Nibbles - Méthode alternative pour l'utilisateur - Metasploit]] | [[00 - Sommaire Getting Started|Sommaire]] | [[21 - Obtenir de l'aide]] →
