---
tags:
  - linux
ordre: 24
---

# Configuration du Réseau

En tant que testeur d'intrusion (pentester), l'une des compétences essentielles est la configuration et la gestion des paramètres réseau sur les systèmes Linux. Maîtriser cela nous permet de mettre en place efficacement des environnements de test, de manipuler le trafic réseau et d'identifier ou d'exploiter des vulnérabilités. Une solide compréhension de la configuration réseau sous Linux nous donne la capacité d'adapter notre approche de test pour répondre à des besoins spécifiques, aidant à optimiser à la fois nos procédures de test et nos résultats.

L'une des tâches principales de la configuration réseau est la gestion des interfaces réseau. Cela implique d'attribuer des adresses IP, de configurer des périphériques réseau tels que des routeurs et des commutateurs, et de mettre en place divers protocoles réseau. Une compréhension approfondie des protocoles réseau, y compris TCP/IP (la suite de protocoles de base pour les communications Internet), DNS (résolution de noms de domaine), DHCP (pour l'allocation dynamique d'adresses IP) et FTP (transfert de fichiers), est essentielle. Nous devons également être familiers avec les différents types d'interfaces réseau — qu'elles soient filaires ou sans fil — et être capables de dépanner les problèmes de connectivité.

### Contrôle d'Accès au Réseau

Un autre composant vital de la configuration réseau est le contrôle d'accès au réseau (`NAC`). En tant que testeurs d'intrusion, nous devons bien connaître la manière dont le NAC peut améliorer la sécurité du réseau et les diverses technologies disponibles. Les principaux modèles de NAC incluent :

|**Type**|**Description**|
|---|---|
|Contrôle d'accès discrétionnaire (`DAC`)|Ce modèle permet au propriétaire de la ressource de définir les autorisations pour ceux qui peuvent y accéder.|
|Contrôle d'accès obligatoire (`MAC`)|Les autorisations sont appliquées par le système d'exploitation, et non par le propriétaire de la ressource, ce qui le rend plus sécurisé mais moins flexible.|
|Contrôle d'accès basé sur les rôles (`RBAC`)|Les autorisations sont attribuées en fonction des rôles au sein d'une organisation, ce qui facilite la gestion des privilèges des utilisateurs.|

Configurer des périphériques réseau Linux pour le NAC implique de mettre en place des politiques de sécurité comme `SELinux` (Security-Enhanced Linux), des profils `AppArmor` pour la sécurité des applications, et d'utiliser des `TCP wrappers` pour contrôler l'accès aux services en fonction des adresses IP. Nous en reparlerons dans les sections suivantes.

Des outils tels que `syslog`, `rsyslog`, `ss` (pour les statistiques de sockets), `lsof` (pour lister les fichiers ouverts), et la `suite ELK` (Elasticsearch, Logstash et Kibana) peuvent être utilisés pour surveiller et analyser le trafic réseau. Ces outils aident à identifier les anomalies, les divulgations/expositions potentielles d'informations, les failles de sécurité et d'autres problèmes réseau critiques.

Pensez à la configuration réseau sous Linux comme à la construction et à la sécurisation d'un grand immeuble de bureaux. La configuration des interfaces réseau, c'est comme installer le câblage et l'infrastructure, en s'assurant que chaque pièce (périphérique réseau) dispose d'une connexion fonctionnelle. Le NAC, c'est comme gérer la sécurité du bâtiment où certaines pièces sont ouvertes à tous (`DAC`), tandis que d'autres ne sont accessibles qu'à certaines personnes selon des règles strictes (`MAC` ou `RBAC`). La surveillance du trafic réseau est similaire à l'installation de caméras de surveillance et d'alarmes, en gardant un œil sur qui se déplace dans le bâtiment, et le dépannage, c'est comme avoir une boîte à outils à portée de main pour résoudre tout problème — que ce soit une connexion interrompue (`ping`), une serrure défectueuse (`nslookup`), ou une entrée vulnérable (`nmap`). Nous explorerons le NAC et les outils plus en détail un peu plus tard dans cette section.

---

## Configuration des Interfaces Réseau

Lorsque vous travaillez avec Ubuntu, vous pouvez configurer les interfaces réseau locales en utilisant la commande `ifconfig` ou `ip`. Ces commandes puissantes nous permettent de visualiser et de configurer les interfaces réseau de notre système. Que nous cherchions à modifier notre configuration réseau existante ou que nous ayons besoin de vérifier l'état de nos interfaces, ces commandes peuvent grandement simplifier le processus. De plus, développer une solide maîtrise des subtilités des interfaces réseau est une compétence essentielle dans le monde moderne et interconnecté. Avec l'avancement rapide de la technologie et la dépendance croissante à la communication numérique, avoir une connaissance approfondie de la manière de travailler avec les interfaces réseau peut vous permettre de naviguer efficacement dans la diversité des réseaux qui existent aujourd'hui.

Une façon d'obtenir des informations sur les interfaces réseau, telles que les adresses IP, les masques de sous-réseau et l'état, est d'utiliser la commande `ifconfig`. En exécutant cette commande, nous pouvons voir les interfaces réseau disponibles et leurs attributs respectifs de manière claire et organisée. Ces informations peuvent être particulièrement utiles lors du dépannage de problèmes de connectivité réseau ou de la mise en place d'une nouvelle configuration réseau. Il convient de noter que la commande `ifconfig` a été dépréciée dans les versions plus récentes de Linux et remplacée par la commande `ip`, qui offre des fonctionnalités plus avancées. Néanmoins, la commande `ifconfig` est encore largement utilisée dans de nombreuses distributions Linux et continue d'être un outil fiable pour la gestion du réseau.

### Paramètres réseau

```bash
cry0l1t3@htb:~$ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 178.62.32.126  netmask 255.255.192.0  broadcast 178.62.63.255
        inet6 fe80::88d9:faff:fecf:797a  prefixlen 64  scopeid 0x20<link>
        ether 8a:d9:fa:cf:79:7a  txqueuelen 1000  (Ethernet)
        RX packets 7910  bytes 717102 (700.2 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 7072  bytes 24215666 (23.0 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.106.0.66  netmask 255.255.240.0  broadcast 10.106.15.255
        inet6 fe80::b8ab:52ff:fe32:1f33  prefixlen 64  scopeid 0x20<link>
        ether ba:ab:52:32:1f:33  txqueuelen 1000  (Ethernet)
        RX packets 14  bytes 1574 (1.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 15  bytes 1700 (1.6 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 15948  bytes 24561302 (23.4 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 15948  bytes 24561302 (23.4 MiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

cry0l1t3@htb:~$ ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 8a:d9:fa:cf:79:7a brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    altname ens3
    inet 178.62.32.126/18 brd 178.62.63.255 scope global dynamic eth0
       valid_lft 85274sec preferred_lft 85274sec
    inet6 fe80::88d9:faff:fecf:797a/64 scope link
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether ba:ab:52:32:1f:33 brd ff:ff:ff:ff:ff:ff
    altname enp0s4
    altname ens4
    inet 10.106.0.66/20 brd 10.106.15.255 scope global dynamic eth1
       valid_lft 85274sec preferred_lft 85274sec
    inet6 fe80::b8ab:52ff:fe32:1f33/64 scope link
       valid_lft forever preferred_lft forever
```

Pour activer les interfaces réseau, les commandes `ifconfig` et `ip` sont deux outils couramment utilisés. Ces commandes permettent aux utilisateurs de modifier et d'activer les paramètres pour une interface spécifique, telle que `eth0`. Nous pouvons ajuster les paramètres réseau pour répondre à nos besoins en utilisant la syntaxe appropriée et en spécifiant le nom de l'interface.

### Activer l'Interface Réseau

```bash
Hiterof13@htb[/htb]$ sudo ifconfig eth0 up
# OR
Hiterof13@htb[/htb]$ sudo ip link set eth0 up
```

Une façon d'allouer une adresse IP à une interface réseau est d'utiliser la commande `ifconfig`. Pour ce faire, nous devons spécifier le nom de l'interface et l'adresse IP comme arguments. C'est une étape cruciale dans la mise en place d'une connexion réseau. L'adresse IP sert d'identifiant unique pour l'interface et permet la communication entre les appareils sur le réseau.

### Attribuer une Adresse IP à une Interface

```bash
Hiterof13@htb[/htb]$ sudo ifconfig eth0 192.168.1.2
```

Pour définir le masque de sous-réseau pour une interface réseau, nous pouvons exécuter la commande suivante avec le nom de l'interface et le masque de sous-réseau :

### Attribuer un Masque de Sous-Réseau à une Interface

```bash
Hiterof13@htb[/htb]$ sudo ifconfig eth0 netmask 255.255.255.0
```

Lorsque nous voulons définir la passerelle par défaut pour une interface réseau, nous pouvons utiliser la commande `route` avec l'option `add`. Cela nous permet de spécifier l'adresse IP de la passerelle et l'interface réseau à laquelle elle doit être appliquée. En définissant la passerelle par défaut, nous désignons l'adresse IP du routeur qui sera utilisée pour envoyer le trafic vers des destinations en dehors du réseau local. Il est important de s'assurer que la passerelle par défaut est correctement définie, car une configuration incorrecte peut entraîner des problèmes de connectivité.

### Attribuer la Route à une Interface

```bash
Hiterof13@htb[/htb]$ sudo route add default gw 192.168.1.1 eth0
```

Lors de la configuration d'une interface réseau sous Linux, il est souvent nécessaire de définir des serveurs DNS (Domain Name System) pour assurer le bon fonctionnement du réseau. Les serveurs DNS sont responsables de la traduction des noms de domaine (comme example.com) en adresses IP, ce qui permet aux appareils de se localiser et de se connecter les uns aux autres sur Internet. Une configuration DNS correcte est cruciale pour permettre aux appareils d'accéder aux sites web, aux services en ligne et à d'autres ressources en réseau. Sans serveurs DNS correctement configurés, les appareils peuvent rencontrer des problèmes tels que l'incapacité de résoudre les noms de domaine, entraînant des problèmes de connectivité réseau.

Sur les systèmes Linux, cela peut être réalisé en mettant à jour le fichier `/etc/resolv.conf`, qui est un simple fichier texte contenant les informations DNS du système. En ajoutant les adresses de serveur DNS appropriées (le DNS public de Google - `8.8.8.8` ou `8.8.4.4`), le système peut résoudre correctement les noms de domaine en adresses IP, assurant une communication fluide sur le réseau.

### Modification des Paramètres DNS

```bash
Hiterof13@htb[/htb]$ sudo vim /etc/resolv.conf
```

### /etc/resolv.conf

```text
nameserver 8.8.8.8
nameserver 8.8.4.4
```

Après avoir effectué les modifications nécessaires à la configuration du réseau, il est essentiel de s'assurer que ces changements sont sauvegardés pour persister après les redémarrages. Cela peut être réalisé en modifiant le fichier `/etc/network/interfaces`, qui définit les interfaces réseau pour les systèmes d'exploitation basés sur Linux. Il est donc vital de sauvegarder toutes les modifications apportées à ce fichier pour éviter tout problème potentiel de connectivité réseau.

Il est important de noter que les modifications apportées directement au fichier `/etc/resolv.conf` ne sont pas persistantes après un redémarrage ou des changements de configuration réseau. C'est parce que le fichier peut être automatiquement écrasé par des services de gestion de réseau comme `NetworkManager` ou `systemd-resolved`. Pour rendre les changements DNS permanents, vous devez configurer les paramètres DNS via l'outil de gestion de réseau approprié, comme la modification des fichiers de configuration réseau ou l'utilisation d'utilitaires de gestion de réseau qui stockent des paramètres persistants.

### Modification des Interfaces

```bash
Hiterof13@htb[/htb]$ sudo vim /etc/network/interfaces
```

Cela ouvrira le fichier `interfaces` dans l'éditeur vim. Nous pouvons ajouter les paramètres de configuration réseau au fichier comme ceci :

### /etc/network/interfaces

```text
auto eth0
iface eth0 inet static
  address 192.168.1.2
  netmask 255.255.255.0
  gateway 192.168.1.1
  dns-nameservers 8.8.8.8 8.8.4.4
```

En configurant l'interface réseau `eth0` pour utiliser une adresse IP statique de `192.168.1.2`, avec un masque de sous-réseau de `255.255.255.0` et une passerelle par défaut de `192.168.1.1`, nous pouvons nous assurer que votre connexion réseau reste stable et fiable. De plus, en spécifiant les serveurs DNS `8.8.8.8` et `8.8.4.4`, nous pouvons garantir que notre ordinateur peut facilement accéder à Internet et résoudre les noms de domaine. Une fois que nous avons apporté ces modifications au fichier de configuration, il est important de sauvegarder le fichier et de quitter l'éditeur. Ensuite, nous devons redémarrer le service réseau pour appliquer les modifications.

### Redémarrer le Service Réseau

```bash
Hiterof13@htb[/htb]$ sudo systemctl restart networking
```

---

## Contrôle d'Accès au Réseau

Le contrôle d'accès au réseau (NAC) est un composant crucial de la sécurité réseau, surtout à l'ère actuelle des cybermenaces croissantes. En tant que testeur d'intrusion, il est vital de comprendre l'importance du NAC dans la protection du réseau et les diverses technologies NAC qui peuvent être utilisées pour renforcer les mesures de sécurité. Le NAC est un système de sécurité qui garantit que seuls les appareils autorisés et conformes obtiennent l'accès au réseau, empêchant ainsi l'accès non autorisé, les fuites de données et autres menaces de sécurité. En mettant en œuvre le NAC, les organisations peuvent être confiantes dans leur capacité à protéger leurs actifs et leurs données contre les cybercriminels qui cherchent toujours à exploiter les vulnérabilités du système. Voici les différentes technologies NAC qui peuvent être utilisées pour renforcer les mesures de sécurité :

- Contrôle d'accès discrétionnaire (DAC)
- Contrôle d'accès obligatoire (MAC)
- Contrôle d'accès basé sur les rôles (RBAC)

Ces technologies sont conçues pour fournir différents niveaux de contrôle d'accès et de sécurité. Chaque technologie a ses caractéristiques uniques et convient à différents cas d'utilisation. En tant que testeur d'intrusion, il est essentiel de comprendre ces technologies et leurs cas d'utilisation spécifiques pour tester et évaluer efficacement la sécurité du réseau.

### Contrôle d'Accès Discrétionnaire

Le DAC est un composant crucial des systèmes de sécurité modernes car il aide les organisations à fournir un accès à leurs ressources tout en gérant les risques associés d'accès non autorisé. C'est un système de contrôle d'accès largement utilisé qui permet aux utilisateurs de gérer l'accès à leurs ressources en confiant aux propriétaires des ressources la responsabilité de contrôler les permissions d'accès à leurs ressources. Cela signifie que les utilisateurs et les groupes qui possèdent une ressource spécifique peuvent décider qui a accès à leurs ressources et quelles actions ils sont autorisés à effectuer. Ces permissions peuvent être définies pour la lecture, l'écriture, l'exécution ou la suppression de la ressource.

### Contrôle d'Accès Obligatoire

Le MAC est utilisé dans des infrastructures qui fournissent un contrôle plus granulaire sur l'accès aux ressources que les systèmes DAC. Ces systèmes définissent des règles qui déterminent l'accès aux ressources en fonction du niveau de sécurité de la ressource et du niveau de sécurité de l'utilisateur ou du processus qui demande l'accès. Chaque ressource se voit attribuer une étiquette de sécurité qui identifie son niveau de sécurité, et chaque utilisateur ou processus se voit attribuer une habilitation de sécurité qui identifie son niveau de sécurité. L'accès à une ressource n'est accordé que si le niveau de sécurité de l'utilisateur ou du processus est égal ou supérieur au niveau de sécurité de la ressource. Le MAC est souvent utilisé dans les systèmes d'exploitation et les applications qui nécessitent un haut niveau de sécurité, tels que les systèmes militaires ou gouvernementaux, les systèmes financiers et les systèmes de santé. Les systèmes MAC sont conçus pour empêcher l'accès non autorisé aux ressources et minimiser l'impact des failles de sécurité.

### Contrôle d'Accès Basé sur les Rôles

Le RBAC attribue des autorisations aux utilisateurs en fonction de leurs rôles au sein d'une organisation. Les utilisateurs se voient attribuer des rôles en fonction de leurs responsabilités professionnelles ou d'autres critères, et chaque rôle se voit accorder un ensemble de permissions qui déterminent les actions qu'ils peuvent effectuer. Le RBAC simplifie la gestion des permissions d'accès, réduit le risque d'erreurs et garantit que les utilisateurs ne peuvent accéder qu'aux ressources nécessaires pour accomplir leurs fonctions professionnelles. Il peut restreindre l'accès aux ressources et données sensibles, limiter l'impact des failles de sécurité et garantir la conformité aux exigences réglementaires. Comparé aux systèmes de contrôle d'accès discrétionnaire (DAC), le RBAC offre une approche plus flexible et évolutive de la gestion de l'accès aux ressources. Dans un système RBAC, chaque utilisateur se voit attribuer un ou plusieurs rôles, et chaque rôle se voit attribuer un ensemble de permissions qui définissent les actions de l'utilisateur. L'accès aux ressources est accordé en fonction du rôle attribué à l'utilisateur plutôt que de son identité ou de sa propriété de la ressource. Les systèmes RBAC sont généralement utilisés dans des environnements avec de nombreux utilisateurs et ressources, tels que les grandes organisations, les agences gouvernementales et les institutions financières.

---

## Surveillance

La surveillance réseau implique la capture, l'analyse et l'interprétation du trafic réseau pour identifier les menaces de sécurité, les problèmes de performance et les comportements suspects. L'objectif principal de l'analyse et de la surveillance du trafic réseau est d'identifier les menaces et les vulnérabilités de sécurité. Par exemple, en tant que testeurs d'intrusion, nous pouvons capturer des identifiants lorsque quelqu'un utilise une connexion non chiffrée et tente de se connecter à un serveur FTP. En conséquence, nous obtiendrons les identifiants de cet utilisateur qui pourraient nous aider à infiltrer davantage le réseau ou à élever nos privilèges à un niveau supérieur. En bref, en analysant le trafic réseau, nous pouvons obtenir des informations sur le comportement du réseau et identifier des schémas qui peuvent indiquer des menaces de sécurité. Une telle analyse inclut la détection d'activités réseau suspectes, l'identification de trafic malveillant et l'identification de risques de sécurité potentiels. Cependant, nous couvrons ce vaste sujet dans le module [Introduction à l'Analyse du Trafic Réseau](https://academy.hackthebox.com/module/details/81), où nous utilisons plusieurs outils pour la surveillance réseau sur des systèmes Linux comme Ubuntu et des systèmes Windows, tels que Wireshark, tshark et Tcpdump.

---

## Dépannage

Le dépannage réseau est un processus essentiel qui consiste à diagnostiquer et à résoudre les problèmes réseau pouvant affecter négativement les performances et la fiabilité du réseau. Ce processus est essentiel pour garantir que le réseau fonctionne de manière optimale et pour éviter les perturbations qui pourraient avoir un impact sur les opérations commerciales pendant nos tests d'intrusion. Il implique également l'identification, l'analyse et la mise en œuvre de solutions pour résoudre les problèmes. Ces problèmes incluent les problèmes de connectivité, les vitesses de réseau lentes et les erreurs réseau. Divers outils peuvent nous aider à identifier et à résoudre les problèmes de dépannage réseau sur les systèmes Linux. Certains des outils les plus couramment utilisés incluent :

1. Ping
2. Traceroute
3. Netstat
4. Tcpdump
5. Wireshark
6. Nmap

En utilisant ces outils et d'autres similaires, nous pouvons mieux comprendre le fonctionnement du réseau et diagnostiquer rapidement tout problème qui pourrait survenir. Par exemple, `ping` est un outil en ligne de commande utilisé pour tester la connectivité entre deux appareils. Il envoie des paquets à un hôte distant et mesure le temps qu'ils mettent à revenir. Pour utiliser `ping`, nous pouvons entrer la commande suivante :

### Ping

```bash
Hiterof13@htb[/htb]$ ping <remote_host>
```

Par exemple, envoyer un ping au serveur DNS de Google enverra des paquets ICMP au serveur DNS de Google et affichera les temps de réponse.

```bash
Hiterof13@htb[/htb]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=1.61 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=1.06 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=0.636 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=119 time=0.685 ms
^C
--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3017ms
rtt min/avg/max/mdev = 0.636/0.996/1.607/0.388 ms
```

Un autre outil est `traceroute`, qui trace la route que les paquets empruntent pour atteindre un hôte distant. Il envoie des paquets avec des valeurs de Time-to-Live (TTL) croissantes à un hôte distant et affiche les adresses IP des appareils que les paquets traversent. Par exemple, pour tracer la route vers [www.inlanefreight.com](http://www.inlanefreight.com/), nous entrerions la commande suivante :

### Traceroute

```bash
Hiterof13@htb[/htb]$ traceroute www.inlanefreight.com
traceroute to www.inlanefreight.com (134.209.24.248), 30 hops max, 60 byte packets
 1  * * *
 2  10.80.71.5 (10.80.71.5)  2.716 ms  2.700 ms  2.730 ms
 3  * * *
 4  10.80.68.175 (10.80.68.175)  7.147 ms  7.132 ms 10.80.68.161 (10.80.68.161)  7.393 ms
```

La sortie fournit une vue détaillée du chemin que les paquets empruntent pour atteindre le serveur web Inlanefreight, situé à [www.inlanefreight.com](http://www.inlanefreight.com/) avec l'adresse IP 134.209.24.248. Elle affiche les adresses IP de tous les appareils intermédiaires que les paquets traversent. Chaque ligne de la sortie de traceroute contient des informations précieuses, offrant des aperçus sur la route du réseau et ses performances.

Lors de la mise en place d'une connexion réseau, il est important de spécifier l'hôte de destination et l'adresse IP. Dans cet exemple, l'hôte de destination est 134.209.24.248, et le nombre maximal de sauts (hops) autorisés est de 30. Cela garantit que la connexion est établie de manière efficace et fiable. En fournissant ces informations, le système peut acheminer le trafic vers la bonne destination et limiter le nombre d'arrêts intermédiaires que les données doivent effectuer.

La deuxième ligne montre le premier saut dans le traceroute, qui est la passerelle du réseau local avec l'adresse IP 10.80.71.5, suivi des trois colonnes suivantes qui montrent le temps qu'il a fallu à chacun des trois paquets envoyés pour atteindre la passerelle en millisecondes (2.716 ms, 2.700 ms et 2.730 ms).

Ensuite, nous voyons le deuxième saut dans le traceroute. Cependant, il n'y a pas eu de réponse de l'appareil à ce saut, indiqué par les trois astérisques au lieu de l'adresse IP. Cela pourrait signifier que l'appareil est en panne, qu'il bloque le trafic ICMP, ou qu'un problème de réseau a provoqué la perte des paquets.

Sur la quatrième ligne, nous pouvons voir le troisième saut dans le traceroute, composé de deux appareils avec les adresses IP 10.80.68.175 et 10.80.68.161, et encore une fois les trois colonnes suivantes montrent le temps qu'il a fallu à chacun des trois paquets pour atteindre le premier appareil (7.147 ms, 7.132 ms et 7.393 ms).

### Netstat

`Netstat` est utilisé pour afficher les connexions réseau actives et leurs ports associés. Il peut être utilisé pour identifier le trafic réseau et dépanner les problèmes de connectivité. Pour utiliser `netstat`, nous pouvons entrer la commande suivante :

```bash
Hiterof13@htb[/htb]$ netstat -a
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 localhost:5901          0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:sunrpc          0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:http            0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:ssh             0.0.0.0:*               LISTEN
...SNIP...
```

Nous pouvons nous attendre à recevoir des informations détaillées sur chaque connexion lors de l'utilisation de cet outil. Cela inclut le protocole utilisé, le nombre d'octets reçus et envoyés, les adresses IP, les numéros de port des appareils locaux et distants, et l'état actuel de la connexion. La sortie fournit des informations précieuses sur l'activité réseau du système, mettant en évidence quatre connexions spécifiques actuellement actives et en écoute sur des ports spécifiques. Ces connexions incluent le logiciel de bureau à distance VNC, le service Sun Remote Procedure Call, le protocole HTTP pour le trafic web, et le protocole SSH pour l'accès shell distant sécurisé. En sachant quels ports sont utilisés par quels services, les utilisateurs peuvent rapidement identifier tout problème réseau et le dépanner en conséquence. Les problèmes réseau les plus courants que nous rencontrerons lors de nos tests d'intrusion sont les suivants :

- Problèmes de connectivité réseau
- Problèmes de résolution DNS (c'est toujours la faute du DNS)
- Perte de paquets de données
- Problèmes de performance du réseau

Les causes les plus courantes sont :

- Pare-feu ou routeurs mal configurés,
- câbles ou connexions réseau endommagés,
- paramètres réseau incorrects,
- pannes matérielles,
- paramètres de serveur DNS incorrects ou pannes de serveur DNS
- entrées DNS mal configurées,
- congestion du réseau,
- matériel réseau obsolète ou paramètres réseau mal configurés,
- logiciels ou firmwares non patchés et absence de contrôles de sécurité.

Comprendre ces problèmes réseau courants et leurs causes est important pour identifier et exploiter efficacement les vulnérabilités dans les systèmes réseau lors de nos tests.

---

## Durcissement

Plusieurs mécanismes sont très efficaces pour sécuriser les systèmes Linux afin de protéger nos données et celles d'autres entreprises. Trois de ces mécanismes sont SELinux, AppArmor et les TCP wrappers. Ces outils sont conçus pour protéger les systèmes Linux contre diverses menaces de sécurité, allant de l'accès non autorisé aux attaques malveillantes. Ceci est essentiel non seulement pendant les tests d'intrusion, où les systèmes sont intentionnellement mis à l'épreuve pour découvrir des vulnérabilités, mais aussi dans des scénarios réels où une compromission effective pourrait avoir de graves conséquences (peu de situations sont aussi graves qu'une faille dans la vie réelle). En mettant en œuvre ces mesures de sécurité et en nous assurant de mettre en place une protection correspondante contre les attaquants potentiels, nous pouvons réduire considérablement le risque de fuites de données et garantir que nos systèmes restent sécurisés. Bien que ces outils partagent certaines similitudes, ils présentent également des différences importantes.

### Security-Enhanced Linux

Security-Enhanced Linux (`SELinux`) est un système de contrôle d'accès obligatoire (`MAC`) intégré au noyau Linux. Il fournit un contrôle granulaire sur l'accès aux ressources et applications du système en appliquant des politiques de sécurité. Ces politiques définissent les permissions pour chaque processus et fichier sur le système, limitant considérablement les dommages qu'un processus ou un service compromis peut causer. SELinux fonctionne à un bas niveau, et bien qu'il offre une sécurité robuste, il peut être complexe à configurer et à gérer en raison de ses contrôles granulaires.

### AppArmor

Comme SELinux, `AppArmor` est un système MAC qui contrôle l'accès aux ressources système et aux applications, mais il fonctionne de manière plus simple et conviviale. AppArmor est implémenté comme un module de sécurité Linux (`LSM`) et utilise des profils d'application pour définir les ressources auxquelles une application peut accéder. Bien qu'il ne fournisse peut-être pas le même niveau de contrôle granulaire que SELinux, AppArmor est souvent plus facile à configurer et est généralement considéré comme plus simple pour une utilisation quotidienne.

### TCP Wrappers

Les `TCP wrappers` sont un outil de contrôle d'accès réseau basé sur l'hôte qui restreint l'accès aux services réseau en fonction de l'adresse IP des connexions entrantes. Lorsqu'une requête réseau est effectuée, les TCP wrappers l'interceptent, vérifiant la requête par rapport à une liste d'adresses IP autorisées ou refusées. C'est un moyen simple mais efficace de contrôler l'accès aux services, en particulier pour bloquer l'accès des systèmes non autorisés aux ressources en réseau. Bien qu'il n'offre pas le contrôle granulaire de SELinux ou d'AppArmor, les TCP wrappers sont un excellent outil pour une protection de base au niveau du réseau.

En ce qui concerne les similitudes, les trois mécanismes de sécurité partagent l'objectif commun d'assurer la sûreté et la sécurité des systèmes Linux. En plus de fournir une protection supplémentaire, ils peuvent restreindre l'accès aux ressources et aux services, réduisant ainsi le risque d'accès non autorisé et de fuites de données. Il convient également de noter que ces mécanismes sont facilement disponibles dans la plupart des distributions Linux, ce qui nous les rend accessibles pour améliorer la sécurité de leurs systèmes. De plus, ces mécanismes peuvent être facilement personnalisés et configurés à l'aide d'outils et d'utilitaires standard, ce qui en fait un choix pratique pour les utilisateurs de Linux.

Bien que `SELinux` et `AppArmor` soient tous deux des systèmes MAC offrant un contrôle granulaire, ils fonctionnent de différentes manières. SELinux est profondément intégré au noyau et offre des contrôles de sécurité plus détaillés, mais il peut être plus complexe à configurer et à maintenir. En revanche, AppArmor fonctionne comme un module du noyau et utilise une sécurité basée sur des profils, ce qui le rend plus facile à gérer, bien qu'il n'offre peut-être pas le même niveau de granularité que SELinux.

D'un autre côté, les `TCP wrappers` se concentrent sur le contrôle de l'accès aux services réseau en fonction des adresses IP des clients, ce qui le rend plus simple mais limité au contrôle d'accès au niveau du réseau. Il n'offre pas les protections plus larges des ressources système que SELinux et AppArmor fournissent, mais il est utile pour restreindre l'accès aux services depuis des systèmes non autorisés.

---

## Mise en Place

En naviguant dans le monde de Linux, nous rencontrons inévitablement un large éventail de technologies, d'applications et de services avec lesquels nous devons nous familiariser. C'est une compétence cruciale, en particulier si nous travaillons dans la cybersécurité et cherchons à améliorer continuellement notre expertise. Pour cette raison, nous vous recommandons vivement de consacrer du temps à apprendre à configurer par vous-même des mesures de sécurité importantes telles que `SELinux`, `AppArmor` et les `TCP wrappers`. En relevant ce défi (facultatif mais très efficace), vous approfondirez votre compréhension de ces technologies, renforcerez vos compétences en résolution de problèmes et acquerrez une expérience précieuse qui vous sera très utile à l'avenir. Nous vous recommandons vivement d'utiliser une VM personnelle et de faire des instantanés (snapshots) avant d'effectuer des modifications.

Lorsqu'il s'agit de mettre en œuvre des mesures de cybersécurité, il n'y a pas d'approche unique. Il est important de considérer les informations spécifiques que vous souhaitez protéger et les outils que vous utiliserez pour le faire. Cependant, vous pouvez pratiquer et mettre en œuvre plusieurs tâches facultatives avec d'autres sur le canal Discord pour accroître vos connaissances et compétences dans ce domaine. En profitant de l'aide des autres et en partageant votre propre expertise, vous pouvez approfondir votre compréhension de la cybersécurité et aider les autres à faire de même. N'oubliez pas, expliquer des concepts aux autres est essentiel pour enseigner et apprendre.

### SELinux

|||
|---|---|
|1.|Installez SELinux sur votre VM.|
|2.|Configurez SELinux pour empêcher un utilisateur d'accéder à un fichier spécifique.|
|3.|Configurez SELinux pour autoriser un seul utilisateur à accéder à un service réseau spécifique mais refuser l'accès à tous les autres.|
|4.|Configurez SELinux pour refuser l'accès à un service réseau spécifique pour un utilisateur ou un groupe donné.|

### AppArmor

|||
|---|---|
|5.|Configurez AppArmor pour empêcher un utilisateur d'accéder à un fichier spécifique.|
|6.|Configurez AppArmor pour autoriser un seul utilisateur à accéder à un service réseau spécifique mais refuser l'accès à tous les autres.|
|7.|Configurez AppArmor pour refuser l'accès à un service réseau spécifique pour un utilisateur ou un groupe donné.|

### TCP Wrappers

|||
|---|---|
|8.|Configurez les TCP wrappers pour autoriser l'accès à un service réseau spécifique depuis une adresse IP spécifique.|
|9.|Configurez les TCP wrappers pour refuser l'accès à un service réseau spécifique depuis une adresse IP spécifique.|
|10.|Configurez les TCP wrappers pour autoriser l'accès à un service réseau spécifique depuis une plage d'adresses IP.|

---

← [[23 - Conteneurisation]] | [[00 - Sommaire Linux|Sommaire]] | [[25 - Protocoles de bureau à distance sous Linux]] →
