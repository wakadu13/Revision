---
tags:
  - nmap
ordre: 4
---

# Scan d'hôtes et de ports

---

Il est essentiel de comprendre comment l'outil que nous utilisons fonctionne et comment il exécute et traite les différentes fonctions. Nous ne comprendrons les résultats que si nous savons ce qu'ils signifient et comment ils sont obtenus. Par conséquent, nous allons examiner de plus près et analyser certaines des méthodes de scan. Après avoir découvert que notre cible est active, nous voulons obtenir une image plus précise du système. Les informations dont nous avons besoin incluent :

- Les ports ouverts et leurs services
- Les versions des services
- Les informations fournies par les services
- Le système d'exploitation

Il y a un total de 6 états différents que nous pouvons obtenir pour un port scanné :

|**État**|**Description**|
|---|---|
|`open`|Cet état indique que la connexion au port scanné a été établie. Ces connexions peuvent être des **connexions TCP**, des **datagrammes UDP** ainsi que des **associations SCTP**.|
|`closed`|Lorsque le port est affiché comme fermé, le protocole TCP indique que le paquet que nous avons reçu en retour contient un drapeau (flag) `RST`. Cette méthode de scan peut également être utilisée pour déterminer si notre cible est active ou non.|
|`filtered`|Nmap ne peut pas identifier correctement si le port scanné est ouvert ou fermé, soit parce qu'aucune réponse n'est renvoyée par la cible pour ce port, soit parce que nous recevons un code d'erreur de la cible.|
|`unfiltered`|Cet état d'un port ne se produit que pendant le scan **TCP-ACK** et signifie que le port est accessible, mais il est impossible de déterminer s'il est ouvert ou fermé.|
|`open\|filtered`|Si nous n'obtenons pas de réponse pour un port spécifique, `Nmap` le mettra dans cet état. Cela indique qu'un pare-feu (firewall) ou un filtre de paquets peut protéger le port.|
|`closed\|filtered`|Cet état ne se produit que lors des scans **IP ID idle** et indique qu'il a été impossible de déterminer si le port scanné est fermé ou filtré par un pare-feu.|

---

## Découverte des ports TCP ouverts

Par défaut, `Nmap` scanne les 1000 ports TCP les plus populaires avec le scan SYN (`-sS`). Ce scan SYN n'est défini par défaut que lorsque nous l'exécutons en tant que root en raison des permissions de socket requises pour créer des paquets TCP bruts (raw packets). Sinon, le scan TCP (`-sT`) est effectué par défaut. Cela signifie que si nous ne définissons pas les ports et les méthodes de scan, ces paramètres sont définis automatiquement. Nous pouvons définir les ports un par un (`-p 22,25,80,139,445`), par plage (`-p 22-445`), par les ports les plus populaires (`--top-ports=10`) de la base de données `Nmap` qui ont été désignés comme les plus fréquents, en scannant tous les ports (`-p-`), mais aussi en définissant un scan de ports rapide, qui contient les 100 ports les plus populaires (`-F`).

#### Scan des 10 ports TCP les plus populaires

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 --top-ports=10

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 15:36 CEST
Nmap scan report for 10.129.2.28
Host is up (0.021s latency).

PORT     STATE    SERVICE
21/tcp   closed   ftp
22/tcp   open     ssh
23/tcp   closed   telnet
25/tcp   open     smtp
80/tcp   open     http
110/tcp  open     pop3
139/tcp  filtered netbios-ssn
443/tcp  closed   https
445/tcp  filtered microsoft-ds
3389/tcp closed   ms-wbt-server
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 1.44 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`--top-ports=10`|Scanne les ports les plus populaires spécifiés qui ont été définis comme les plus fréquents.|

---

Nous voyons que nous n'avons scanné que les 10 ports TCP les plus populaires de notre cible, et `Nmap` affiche leur état en conséquence. Si nous traçons les paquets que `Nmap` envoie, nous verrons le drapeau `RST` sur le `port TCP 21` que notre cible nous renvoie. Pour avoir une vue claire du scan SYN, nous désactivons les requêtes echo ICMP (`-Pn`), la résolution DNS (`-n`) et le scan ping ARP (`--disable-arp-ping`).

#### Nmap - Tracer les paquets

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 21 --packet-trace -Pn -n --disable-arp-ping

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 15:39 CEST
SENT (0.0429s) TCP 10.10.14.2:63090 > 10.129.2.28:21 S ttl=56 id=57322 iplen=44  seq=1699105818 win=1024 <mss 1460>
RCVD (0.0573s) TCP 10.129.2.28:21 > 10.10.14.2:63090 RA ttl=64 id=0 iplen=40  seq=0 win=0
Nmap scan report for 10.129.2.28
Host is up (0.014s latency).

PORT   STATE  SERVICE
21/tcp closed ftp
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.07 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p 21`|Scanne uniquement le port spécifié.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|

---

Nous pouvons voir sur la ligne SENT que nous (`10.10.14.2`) avons envoyé un paquet TCP avec le drapeau `SYN` (`S`) à notre cible (`10.129.2.28`). Dans la ligne RCVD suivante, nous pouvons voir que la cible répond avec un paquet TCP contenant les drapeaux `RST` et `ACK` (`RA`). Les drapeaux `RST` et `ACK` sont utilisés pour accuser réception du paquet TCP (`ACK`) et pour mettre fin à la session TCP (`RST`).

#### Requête

|**Message**|**Description**|
|---|---|
|`SENT (0.0429s)`|Indique l'opération SENT de Nmap, qui envoie un paquet à la cible.|
|`TCP`|Affiche le protocole qui est utilisé pour interagir avec le port cible.|
|`10.10.14.2:63090 >`|Représente notre adresse IPv4 et le port source, qui seront utilisés par Nmap pour envoyer les paquets.|
|`10.129.2.28:21`|Affiche l'adresse IPv4 et le port de la cible.|
|`S`|Drapeau SYN du paquet TCP envoyé.|
|`ttl=56 id=57322 iplen=44 seq=1699105818 win=1024 mss 1460`|Paramètres supplémentaires de l'en-tête TCP.|

#### Réponse

|**Message**|**Description**|
|---|---|
|`RCVD (0.0573s)`|Indique un paquet reçu de la cible.|
|`TCP`|Affiche le protocole qui est utilisé.|
|`10.129.2.28:21 >`|Représente l'adresse IPv4 et le port source de la cible, qui seront utilisés pour répondre.|
|`10.10.14.2:63090`|Affiche notre adresse IPv4 et le port auquel la réponse sera envoyée.|
|`RA`|Drapeaux RST et ACK du paquet TCP envoyé.|
|`ttl=64 id=0 iplen=40 seq=0 win=0`|Paramètres supplémentaires de l'en-tête TCP.|

#### Scan de connexion (Connect Scan)

Le [scan de connexion TCP](https://nmap.org/book/scan-methods-connect-scan.html) (`-sT`) de Nmap utilise la poignée de main en trois temps (three-way handshake) TCP pour déterminer si un port spécifique sur un hôte cible est ouvert ou fermé. Le scan envoie un paquet `SYN` au port cible et attend une réponse. Il est considéré comme ouvert si le port cible répond avec un paquet `SYN-ACK` et fermé s'il répond avec un paquet `RST`.

Le scan de connexion (également connu sous le nom de scan de connexion TCP complet) est très précis car il complète la poignée de main en trois temps TCP, ce qui nous permet de déterminer l'état exact d'un port (ouvert, fermé ou filtré). Cependant, il n'est pas des plus furtifs. En fait, le scan de connexion est l'une des techniques les moins furtives, car il établit une connexion complète, ce qui crée des journaux (logs) sur la plupart des systèmes et est facilement détecté par les solutions IDS/IPS (Systèmes de Détection/Prévention d'Intrusion) modernes. Cela dit, le scan de connexion peut toujours être utile dans certaines situations, en particulier lorsque la précision est une priorité et que l'objectif est de cartographier le réseau sans perturber de manière significative les services. Comme le scan établit une connexion TCP complète, il interagit proprement avec les services, ce qui le rend moins susceptible de provoquer des erreurs de service ou de l'instabilité par rapport à des scans plus intrusifs. Bien que ce ne soit pas la méthode la plus furtive, il est parfois considéré comme un scan plus « poli » car il se comporte comme une connexion client normale, ayant ainsi un impact minimal sur les services cibles.

Les scans comme le scan SYN (également connu sous le nom de scan semi-ouvert ou half-open scan) sont généralement considérés comme plus furtifs car ils ne complètent pas la poignée de main complète, laissant la connexion inachevée après l'envoi du paquet SYN initial. Cela minimise les chances de déclencher des journaux de connexion tout en recueillant des informations sur l'état des ports. Les systèmes IDS/IPS avancés, cependant, se sont adaptés pour détecter même ces techniques plus subtiles.

#### Scan de connexion sur le port TCP 443

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 443 --packet-trace --disable-arp-ping -Pn -n --reason -sT

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 16:26 CET
CONN (0.0385s) TCP localhost > 10.129.2.28:443 => Operation now in progress
CONN (0.0396s) TCP localhost > 10.129.2.28:443 => Connected
Nmap scan report for 10.129.2.28
Host is up, received user-set (0.013s latency).

PORT    STATE SERVICE REASON
443/tcp open  https   syn-ack

Nmap done: 1 IP address (1 host up) scanned in 0.04 seconds
```

---

## Ports filtrés

Lorsqu'un port est affiché comme filtré, il peut y avoir plusieurs raisons. Dans la plupart des cas, les pare-feux ont certaines règles définies pour gérer des connexions spécifiques. Les paquets peuvent être soit abandonnés (`dropped`), soit rejetés (`rejected`). Lorsqu'un paquet est abandonné, `Nmap` ne reçoit aucune réponse de notre cible, et par défaut, le taux de nouvelles tentatives (`--max-retries`) est fixé à `10`. Cela signifie que `Nmap` renverra la requête au port cible pour déterminer si le paquet précédent a été accidentellement mal géré ou non.

Examinons un exemple où le pare-feu abandonne (`drops`) les paquets TCP que nous envoyons pour le scan de port. Pour ce faire, nous scannons le port TCP **139**, qui était déjà affiché comme filtré. Pour pouvoir suivre la manière dont nos paquets envoyés sont traités, nous désactivons à nouveau les requêtes echo ICMP (`-Pn`), la résolution DNS (`-n`) et le scan ping ARP (`--disable-arp-ping`).

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 139 --packet-trace -n --disable-arp-ping -Pn

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 15:45 CEST
SENT (0.0381s) TCP 10.10.14.2:60277 > 10.129.2.28:139 S ttl=47 id=14523 iplen=44  seq=4175236769 win=1024 <mss 1460>
SENT (1.0411s) TCP 10.10.14.2:60278 > 10.129.2.28:139 S ttl=45 id=7372 iplen=44  seq=4175171232 win=1024 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up.

PORT    STATE    SERVICE
139/tcp filtered netbios-ssn
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 2.06 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p 139`|Scanne uniquement le port spécifié.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`-Pn`|Désactive les requêtes Echo ICMP.|

---

Nous voyons dans le dernier scan que `Nmap` a envoyé deux paquets TCP avec le drapeau SYN. Par la durée (`2.06s`) du scan, nous pouvons reconnaître qu'il a pris beaucoup plus de temps que les précédents (`~0.05s`). Le cas est différent si le pare-feu rejette les paquets. Pour cela, nous examinons le port TCP `445`, qui est traité en conséquence par une telle règle du pare-feu.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 445 --packet-trace -n --disable-arp-ping -Pn

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 15:55 CEST
SENT (0.0388s) TCP 10.129.2.28:52472 > 10.129.2.28:445 S ttl=49 id=21763 iplen=44  seq=1418633433 win=1024 <mss 1460>
RCVD (0.0487s) ICMP [10.129.2.28 > 10.129.2.28 Port 445 unreachable (type=3/code=3) ] IP [ttl=64 id=20998 iplen=72 ]
Nmap scan report for 10.129.2.28
Host is up (0.0099s latency).

PORT    STATE    SERVICE
445/tcp filtered microsoft-ds
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p 445`|Scanne uniquement le port spécifié.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`-Pn`|Désactive les requêtes Echo ICMP.|

En réponse, nous recevons une réponse `ICMP` avec le `type 3` et le `code d'erreur 3`, ce qui indique que le port souhaité est inaccessible. Néanmoins, si nous savons que l'hôte est actif, nous pouvons fortement supposer que le pare-feu sur ce port rejette les paquets, et nous devrons examiner ce port de plus près plus tard.

---

## Découverte des ports UDP ouverts

Certains administrateurs système oublient parfois de filtrer les ports UDP en plus des ports TCP. Comme l'`UDP` est un protocole sans état (`stateless protocol`) et ne nécessite pas de poignée de main en trois temps comme le TCP, nous ne recevons aucun accusé de réception. Par conséquent, le délai d'attente (timeout) est beaucoup plus long, ce qui rend l'ensemble du `scan UDP` (`-sU`) beaucoup plus lent que le `scan TCP` (`-sS`).

Regardons un exemple de ce à quoi un scan UDP (`-sU`) peut ressembler et quels résultats il nous donne.

#### Scan de port UDP

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -F -sU

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 16:01 CEST
Nmap scan report for 10.129.2.28
Host is up (0.059s latency).
Not shown: 95 closed ports
PORT     STATE         SERVICE
68/udp   open|filtered dhcpc
137/udp  open          netbios-ns
138/udp  open|filtered netbios-dgm
631/udp  open|filtered ipp
5353/udp open          zeroconf
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 98.07 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-F`|Scanne les 100 ports les plus populaires.|
|`-sU`|Effectue un scan UDP.|

---

Un autre inconvénient est que nous n'obtenons souvent pas de réponse car `Nmap` envoie des datagrammes vides aux ports UDP scannés, et nous ne recevons aucune réponse. Nous ne pouvons donc pas déterminer si le paquet UDP est bien arrivé ou non. Si le port UDP est `ouvert`, nous n'obtenons une réponse que si l'application est configurée pour le faire.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -sU -Pn -n --disable-arp-ping --packet-trace -p 137 --reason

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 16:15 CEST
SENT (0.0367s) UDP 10.10.14.2:55478 > 10.129.2.28:137 ttl=57 id=9122 iplen=78
RCVD (0.0398s) UDP 10.129.2.28:137 > 10.10.14.2:55478 ttl=64 id=13222 iplen=257
Nmap scan report for 10.129.2.28
Host is up, received user-set (0.0031s latency).

PORT    STATE SERVICE    REASON
137/udp open  netbios-ns udp-response ttl 64
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.04 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-sU`|Effectue un scan UDP.|
|`-Pn`|Désactive les requêtes Echo ICMP.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|
|`-p 137`|Scanne uniquement le port spécifié.|
|`--reason`|Affiche la raison pour laquelle un port est dans un état particulier.|

---

Si nous obtenons une réponse ICMP avec le `code d'erreur 3` (port inaccessible), nous savons que le port est bien `fermé`.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -sU -Pn -n --disable-arp-ping --packet-trace -p 100 --reason

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 16:25 CEST
SENT (0.0445s) UDP 10.10.14.2:63825 > 10.129.2.28:100 ttl=57 id=29925 iplen=28
RCVD (0.1498s) ICMP [10.129.2.28 > 10.10.14.2 Port unreachable (type=3/code=3) ] IP [ttl=64 id=11903 iplen=56 ]
Nmap scan report for 10.129.2.28
Host is up, received user-set (0.11s latency).

PORT    STATE  SERVICE REASON
100/udp closed unknown port-unreach ttl 64
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in  0.15 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-sU`|Effectue un scan UDP.|
|`-Pn`|Désactive les requêtes Echo ICMP.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|
|`-p 100`|Scanne uniquement le port spécifié.|
|`--reason`|Affiche la raison pour laquelle un port est dans un état particulier.|

---

Pour toutes les autres réponses ICMP, les ports scannés sont marqués comme (`open|filtered`).

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -sU -Pn -n --disable-arp-ping --packet-trace -p 138 --reason

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 16:32 CEST
SENT (0.0380s) UDP 10.10.14.2:52341 > 10.129.2.28:138 ttl=50 id=65159 iplen=28
SENT (1.0392s) UDP 10.10.14.2:52342 > 10.129.2.28:138 ttl=40 id=24444 iplen=28
Nmap scan report for 10.129.2.28
Host is up, received user-set.

PORT    STATE         SERVICE     REASON
138/udp open|filtered netbios-dgm no-response
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 2.06 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-sU`|Effectue un scan UDP.|
|`-Pn`|Désactive les requêtes Echo ICMP.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|
|`-p 138`|Scanne uniquement le port spécifié.|
|`--reason`|Affiche la raison pour laquelle un port est dans un état particulier.|

Une autre méthode pratique pour scanner les ports est l'option `-sV` qui est utilisée pour obtenir des informations supplémentaires disponibles sur les ports ouverts. Cette méthode peut identifier les versions, les noms de service et des détails sur notre cible.

#### Scan de version

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -Pn -n --disable-arp-ping --packet-trace -p 445 --reason  -sV

Starting Nmap 7.80 ( https://nmap.org ) at 2022-11-04 11:10 GMT
SENT (0.3426s) TCP 10.10.14.2:44641 > 10.129.2.28:445 S ttl=55 id=43401 iplen=44  seq=3589068008 win=1024 <mss 1460>
RCVD (0.3556s) TCP 10.129.2.28:445 > 10.10.14.2:44641 SA ttl=63 id=0 iplen=44  seq=2881527699 win=29200 <mss 1337>
NSOCK INFO [0.4980s] nsock_iod_new2(): nsock_iod_new (IOD #1)
NSOCK INFO [0.4980s] nsock_connect_tcp(): TCP connection requested to 10.129.2.28:445 (IOD #1) EID 8
NSOCK INFO [0.5130s] nsock_trace_handler_callback(): Callback: CONNECT SUCCESS for EID 8 [10.129.2.28:445]
Service scan sending probe NULL to 10.129.2.28:445 (tcp)
NSOCK INFO [0.5130s] nsock_read(): Read request from IOD #1 [10.129.2.28:445] (timeout: 6000ms) EID 18
NSOCK INFO [6.5190s] nsock_trace_handler_callback(): Callback: READ TIMEOUT for EID 18 [10.129.2.28:445]
Service scan sending probe SMBProgNeg to 10.129.2.28:445 (tcp)
NSOCK INFO [6.5190s] nsock_write(): Write request for 168 bytes to IOD #1 EID 27 [10.129.2.28:445]
NSOCK INFO [6.5190s] nsock_read(): Read request from IOD #1 [10.129.2.28:445] (timeout: 5000ms) EID 34
NSOCK INFO [6.5190s] nsock_trace_handler_callback(): Callback: WRITE SUCCESS for EID 27 [10.129.2.28:445]
NSOCK INFO [6.5320s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 34 [10.129.2.28:445] (135 bytes)
Service scan match (Probe SMBProgNeg matched with SMBProgNeg line 13836): 10.129.2.28:445 is netbios-ssn.  Version: |Samba smbd|3.X - 4.X|workgroup: WORKGROUP|
NSOCK INFO [6.5320s] nsock_iod_delete(): nsock_iod_delete (IOD #1)
Nmap scan report for 10.129.2.28
Host is up, received user-set (0.013s latency).

PORT    STATE SERVICE     REASON         VERSION
445/tcp open  netbios-ssn syn-ack ttl 63 Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
Service Info: Host: Ubuntu

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.55 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-Pn`|Désactive les requêtes Echo ICMP.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|
|`-p 445`|Scanne uniquement le port spécifié.|
|`--reason`|Affiche la raison pour laquelle un port est dans un état particulier.|
|`-sV`|Effectue un scan de service.|

Nous pouvons trouver plus d'informations sur les techniques de scan de port sur : [https://nmap.org/book/man-port-scanning-techniques.html](https://nmap.org/book/man-port-scanning-techniques.html)
---

← [[03 - Découverte d'Hôtes]] | [[00 - Sommaire Nmap|Sommaire]] | [[05 - Sauvegarde des Résultats]] →
