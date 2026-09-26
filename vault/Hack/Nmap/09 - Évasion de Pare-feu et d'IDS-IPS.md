---
tags:
  - nmap
ordre: 9
---

# Évasion de Pare-feu et d'IDS/IPS

---

`Nmap` nous offre de nombreuses façons de contourner les règles des pare-feu et les IDS/IPS. Ces méthodes incluent la fragmentation des paquets, l'utilisation de leurres, et d'autres que nous aborderons dans cette section.

---

## Pare-feu

Un pare-feu (firewall) est une mesure de sécurité contre les tentatives de connexion non autorisées provenant de réseaux externes. Chaque système de sécurité de pare-feu est basé sur des composants logiciels et/ou matériels qui surveillent le trafic réseau lorsqu'il traverse le pare-feu et décident de la manière de traiter la connexion en fonction des règles qui ont été établies. Il vérifie si les paquets réseau individuels sont transmis, abandonnés (dropped) ou bloqués. Ce mécanisme est conçu pour empêcher les connexions indésirables qui pourraient être potentiellement dangereuses.

---

## IDS/IPS

Comme le pare-feu, le système de détection d'intrusion (`IDS`, pour Intrusion Detection System) et le système de prévention d'intrusion (`IPS`, pour Intrusion Prevention System) sont également des composants logiciels. Un `IDS` analyse le réseau à la recherche d'attaques potentielles, les analyse et signale toute attaque détectée. Un `IPS` complète l' `IDS` en prenant des mesures défensives spécifiques si une attaque potentielle a été détectée. L'analyse de telles attaques est basée sur la correspondance de motifs (pattern matching) et les signatures. Si des motifs spécifiques sont détectés, comme un scan de détection de service, l' `IPS` peut empêcher les tentatives de connexion en attente.

---

#### Déterminer les Pare-feu et Leurs Règles

Nous savons déjà que lorsqu'un port est affiché comme filtré (filtered), cela peut avoir plusieurs raisons. Dans la plupart des cas, les pare-feu ont certaines règles définies pour gérer des connexions spécifiques. Les paquets peuvent être soit `abandonnés` (dropped), soit `rejetés` (rejected). Les paquets `abandonnés` sont ignorés, et aucune réponse n'est renvoyée par l'hôte.

C'est différent pour les paquets rejetés, qui suscitent une réponse explicite. Les paquets TCP sont retournés avec un drapeau RST, tandis que les paquets ICMP peuvent contenir différents types de codes d'erreur.

Ces erreurs incluent :

- Net Unreachable (Réseau Inaccessible)
- Net Prohibited (Réseau Interdit)
- Host Unreachable (Hôte Inaccessible)
- Host Prohibited (Hôte Interdit)
- Port Unreachable (Port Inaccessible)
- Proto Unreachable (Protocole Inaccessible)

La méthode de scan TCP ACK (`-sA`) de Nmap est beaucoup plus difficile à filtrer pour les pare-feu et les systèmes IDS/IPS que les scans SYN (`-sS`) ou Connect (`sT`) classiques, car ils n'envoient qu'un paquet TCP avec uniquement le drapeau `ACK`. Lorsqu'un port est fermé ou ouvert, l'hôte doit répondre avec un drapeau `RST`. Contrairement aux connexions sortantes, toutes les tentatives de connexion (avec le drapeau `SYN`) provenant de réseaux externes sont généralement bloquées par les pare-feu. Cependant, les paquets avec le drapeau `ACK` sont souvent laissés passer par le pare-feu car celui-ci ne peut pas déterminer si la connexion a été établie en premier lieu depuis le réseau externe ou le réseau interne.

Si nous examinons ces scans, nous verrons en quoi les résultats diffèrent.

#### Scan SYN

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 21,22,25 -sS -Pn -n --disable-arp-ping --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 14:56 CEST
SENT (0.0278s) TCP 10.10.14.2:57347 > 10.129.2.28:22 S ttl=53 id=22412 iplen=44  seq=4092255222 win=1024 <mss 1460>
SENT (0.0278s) TCP 10.10.14.2:57347 > 10.129.2.28:25 S ttl=50 id=62291 iplen=44  seq=4092255222 win=1024 <mss 1460>
SENT (0.0278s) TCP 10.10.14.2:57347 > 10.129.2.28:21 S ttl=58 id=38696 iplen=44  seq=4092255222 win=1024 <mss 1460>
RCVD (0.0329s) ICMP [10.129.2.28 > 10.10.14.2 Port 21 unreachable (type=3/code=3) ] IP [ttl=64 id=40884 iplen=72 ]
RCVD (0.0341s) TCP 10.129.2.28:22 > 10.10.14.2:57347 SA ttl=64 id=0 iplen=44  seq=1153454414 win=64240 <mss 1460>
RCVD (1.0386s) TCP 10.129.2.28:22 > 10.10.14.2:57347 SA ttl=64 id=0 iplen=44  seq=1153454414 win=64240 <mss 1460>
SENT (1.1366s) TCP 10.10.14.2:57348 > 10.129.2.28:25 S ttl=44 id=6796 iplen=44  seq=4092320759 win=1024 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up (0.0053s latency).

PORT   STATE    SERVICE
21/tcp filtered ftp
22/tcp open     ssh
25/tcp filtered smtp
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.07 seconds
```

#### Scan ACK

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 21,22,25 -sA -Pn -n --disable-arp-ping --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 14:57 CEST
SENT (0.0422s) TCP 10.10.14.2:49343 > 10.129.2.28:21 A ttl=49 id=12381 iplen=40  seq=0 win=1024
SENT (0.0423s) TCP 10.10.14.2:49343 > 10.129.2.28:22 A ttl=41 id=5146 iplen=40  seq=0 win=1024
SENT (0.0423s) TCP 10.10.14.2:49343 > 10.129.2.28:25 A ttl=49 id=5800 iplen=40  seq=0 win=1024
RCVD (0.1252s) ICMP [10.129.2.28 > 10.10.14.2 Port 21 unreachable (type=3/code=3) ] IP [ttl=64 id=55628 iplen=68 ]
RCVD (0.1268s) TCP 10.129.2.28:22 > 10.10.14.2:49343 R ttl=64 id=0 iplen=40  seq=1660784500 win=0
SENT (1.3837s) TCP 10.10.14.2:49344 > 10.129.2.28:25 A ttl=59 id=21915 iplen=40  seq=0 win=1024
Nmap scan report for 10.129.2.28
Host is up (0.083s latency).

PORT   STATE      SERVICE
21/tcp filtered   ftp
22/tcp unfiltered ssh
25/tcp filtered   smtp
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.15 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p 21,22,25`|Scanne uniquement les ports spécifiés.|
|`-sS`|Effectue un scan SYN sur les ports spécifiés.|
|`-sA`|Effectue un scan ACK sur les ports spécifiés.|
|`-Pn`|Désactive les requêtes ICMP Echo.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|

Veuillez prêter attention aux paquets `RCVD` et au drapeau défini que nous recevons de notre cible. Avec le scan SYN (`-sS`), notre cible essaie d'établir la connexion TCP en renvoyant un paquet avec les drapeaux SYN-ACK (`SA`) activés, et avec le scan ACK (`-sA`), nous recevons le drapeau `RST` car le port TCP 22 est ouvert. Pour le port TCP 25, nous ne recevons aucun paquet en retour, ce qui indique que les paquets seront abandonnés.

---

## Détecter les IDS/IPS

Contrairement aux pare-feu et à leurs règles, la détection des systèmes IDS/IPS est beaucoup plus difficile car ce sont des systèmes de surveillance passive du trafic. Les `systèmes IDS` examinent toutes les connexions entre les hôtes. Si l'IDS trouve des paquets contenant des contenus ou des spécifications définis, l'administrateur est averti et prend les mesures appropriées dans le pire des cas.

Les `systèmes IPS` prennent des mesures configurées par l'administrateur de manière indépendante pour prévenir automatiquement les attaques potentielles. Il est essentiel de savoir que les IDS et les IPS sont des applications différentes et que l'IPS sert de complément à l'IDS.

Plusieurs serveurs privés virtuels (`VPS`, pour Virtual Private Server) avec différentes adresses IP sont recommandés pour déterminer si de tels systèmes sont présents sur le réseau cible lors d'un test d'intrusion. Si l'administrateur détecte une telle attaque potentielle sur le réseau cible, la première étape consiste à bloquer l'adresse IP d'où provient l'attaque potentielle. En conséquence, nous ne pourrons plus accéder au réseau en utilisant cette adresse IP, et notre fournisseur d'accès à Internet (`FAI`, ou ISP pour Internet Service Provider) sera contacté et tout accès à Internet sera bloqué.

- Les `systèmes IDS` seuls sont généralement là pour aider les administrateurs à détecter les attaques potentielles sur leur réseau. Ils peuvent ensuite décider comment gérer de telles connexions. Nous pouvons déclencher certaines mesures de sécurité de la part d'un administrateur, par exemple, en scannant agressivement un seul port et son service. En fonction de si des mesures de sécurité spécifiques sont prises, nous pouvons détecter si le réseau dispose d'applications de surveillance ou non.
- Une méthode pour déterminer si un tel `système IPS` est présent sur le réseau cible est de scanner à partir d'un seul hôte (`VPS`). Si à un moment donné cet hôte est bloqué et n'a plus accès au réseau cible, nous savons que l'administrateur a pris des mesures de sécurité. En conséquence, nous pouvons continuer notre test d'intrusion avec un autre `VPS`.

Par conséquent, nous savons que nous devons être plus discrets avec nos scans et, dans le meilleur des cas, masquer toutes les interactions avec le réseau cible et ses services.

---

## Leurres

Il y a des cas où les administrateurs bloquent par principe des sous-réseaux spécifiques de différentes régions. Cela empêche tout accès au réseau cible. Un autre exemple est lorsque l'IPS est censé nous bloquer. Pour cette raison, la méthode de scan par leurres (Decoy) (`-D`) est le bon choix. Avec cette méthode, Nmap génère diverses adresses IP aléatoires qui sont insérées dans l'en-tête IP pour masquer l'origine du paquet envoyé. Avec cette méthode, nous pouvons générer de manière aléatoire (`RND`) un nombre spécifique (par exemple : `5`) d'adresses IP séparées par deux-points (`:`). Notre véritable adresse IP est ensuite placée au hasard parmi les adresses IP générées. Dans l'exemple suivant, notre véritable adresse IP est donc placée en deuxième position. Un autre point critique est que les leurres doivent être actifs. Sinon, le service sur la cible pourrait être inaccessible en raison de mécanismes de sécurité contre les inondations SYN (SYN-flooding).

#### Scan en Utilisant des Leurres

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 80 -sS -Pn -n --disable-arp-ping --packet-trace -D RND:5

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 16:14 CEST
SENT (0.0378s) TCP 102.52.161.59:59289 > 10.129.2.28:80 S ttl=42 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0378s) TCP 10.10.14.2:59289 > 10.129.2.28:80 S ttl=59 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0379s) TCP 210.120.38.29:59289 > 10.129.2.28:80 S ttl=37 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0379s) TCP 191.6.64.171:59289 > 10.129.2.28:80 S ttl=38 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0379s) TCP 184.178.194.209:59289 > 10.129.2.28:80 S ttl=39 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
SENT (0.0379s) TCP 43.21.121.33:59289 > 10.129.2.28:80 S ttl=55 id=29822 iplen=44  seq=3687542010 win=1024 <mss 1460>
RCVD (0.1370s) TCP 10.129.2.28:80 > 10.10.14.2:59289 SA ttl=64 id=0 iplen=44  seq=4056111701 win=64240 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up (0.099s latency).

PORT   STATE SERVICE
80/tcp open  http
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.15 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p 80`|Scanne uniquement les ports spécifiés.|
|`-sS`|Effectue un scan SYN sur les ports spécifiés.|
|`-Pn`|Désactive les requêtes ICMP Echo.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|
|`-D RND:5`|Génère cinq adresses IP aléatoires qui indiquent l'IP source de la connexion.|

Les paquets usurpés (spoofed packets) sont souvent filtrés par les FAI et les routeurs, même s'ils proviennent de la même plage réseau. Par conséquent, nous pouvons également spécifier les adresses IP de nos serveurs VPS et les utiliser en combinaison avec la manipulation de l'« `IP ID` » dans les en-têtes IP pour scanner la cible.

Un autre scénario serait que seuls des sous-réseaux individuels n'auraient pas accès aux services spécifiques du serveur. Nous pouvons donc également spécifier manuellement l'adresse IP source (`-S`) pour tester si nous obtenons de meilleurs résultats avec celle-ci. Les leurres peuvent être utilisés pour les scans SYN, ACK, ICMP et les scans de détection de système d'exploitation. Examinons donc un tel exemple et déterminons de quel système d'exploitation il s'agit le plus probablement.

#### Test d'une Règle de Pare-feu

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -n -Pn -p445 -O

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-22 01:23 CEST
Nmap scan report for 10.129.2.28
Host is up (0.032s latency).

PORT    STATE    SERVICE
445/tcp filtered microsoft-ds
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
Too many fingerprints match this host to give specific OS details
Network Distance: 1 hop

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 3.14 seconds
```

#### Scan en Utilisant une Adresse IP Source Différente

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -n -Pn -p 445 -O -S 10.129.2.200 -e tun0

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-22 01:16 CEST
Nmap scan report for 10.129.2.28
Host is up (0.010s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 2.6.32 (96%), Linux 3.2 - 4.9 (96%), Linux 2.6.32 - 3.10 (96%), Linux 3.4 - 3.10 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Synology DiskStation Manager 5.2-5644 (94%), Linux 2.6.32 - 2.6.35 (94%), Linux 2.6.32 - 3.5 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 4.11 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-n`|Désactive la résolution DNS.|
|`-Pn`|Désactive les requêtes ICMP Echo.|
|`-p 445`|Scanne uniquement les ports spécifiés.|
|`-O`|Effectue un scan de détection de système d'exploitation.|
|`-S`|Scanne la cible en utilisant une adresse IP source différente.|
|`10.129.2.200`|Spécifie l'adresse IP source.|
|`-e tun0`|Envoie toutes les requêtes via l'interface spécifiée.|

---

## Proxy DNS

Par défaut, `Nmap` effectue une résolution DNS inversée (reverse DNS resolution), sauf indication contraire, pour trouver des informations plus importantes sur notre cible. Ces requêtes DNS sont également transmises dans la plupart des cas car le serveur web donné est censé être trouvé et visité. Les requêtes DNS sont effectuées sur le `port UDP 53`. Le `port TCP 53` n'était auparavant utilisé que pour les soi-disant « transferts de zone » (zone transfers) entre les serveurs DNS ou pour le transfert de données de plus de 512 octets. De plus en plus, cela change en raison des extensions IPv6 et DNSSEC. Ces changements font que de nombreuses requêtes DNS sont effectuées via le port TCP 53.

Cependant, `Nmap` nous donne toujours un moyen de spécifier nous-mêmes des serveurs DNS (`--dns-server <ns>,<ns>`). Cette méthode pourrait être fondamentale pour nous si nous nous trouvons dans une zone démilitarisée (`DMZ`). Les serveurs DNS de l'entreprise sont généralement plus fiables que ceux d'Internet. Ainsi, nous pourrions par exemple les utiliser pour interagir avec les hôtes du réseau interne. Comme autre exemple, nous pouvons utiliser le `port TCP 53` comme port source (`--source-port`) pour nos scans. Si l'administrateur utilise le pare-feu pour contrôler ce port et ne filtre pas correctement les IDS/IPS, nos paquets TCP seront considérés comme fiables et autorisés à passer.

#### Scan SYN d'un Port Filtré

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p50000 -sS -Pn -n --disable-arp-ping --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 22:50 CEST
SENT (0.0417s) TCP 10.10.14.2:33436 > 10.129.2.28:50000 S ttl=41 id=21939 iplen=44  seq=736533153 win=1024 <mss 1460>
SENT (1.0481s) TCP 10.10.14.2:33437 > 10.129.2.28:50000 S ttl=46 id=6446 iplen=44  seq=736598688 win=1024 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up.

PORT      STATE    SERVICE
50000/tcp filtered ibm-db2

Nmap done: 1 IP address (1 host up) scanned in 2.06 seconds
```

#### Scan SYN à partir du Port DNS

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p50000 -sS -Pn -n --disable-arp-ping --packet-trace --source-port 53

SENT (0.0482s) TCP 10.10.14.2:53 > 10.129.2.28:50000 S ttl=58 id=27470 iplen=44  seq=4003923435 win=1024 <mss 1460>
RCVD (0.0608s) TCP 10.129.2.28:50000 > 10.10.14.2:53 SA ttl=64 id=0 iplen=44  seq=540635485 win=64240 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up (0.013s latency).

PORT      STATE SERVICE
50000/tcp open  ibm-db2
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 0.08 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p 50000`|Scanne uniquement les ports spécifiés.|
|`-sS`|Effectue un scan SYN sur les ports spécifiés.|
|`-Pn`|Désactive les requêtes ICMP Echo.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|
|`--source-port 53`|Effectue les scans à partir du port source spécifié.|

---

Maintenant que nous avons découvert que le pare-feu accepte le `port TCP 53`, il est très probable que les filtres IDS/IPS soient également configurés de manière beaucoup plus faible que d'autres. Nous pouvons tester cela en essayant de nous connecter à ce port en utilisant `Netcat`.

#### Connexion au Port Filtré

```bash
Hiterof13@htb[/htb]$ ncat -nv --source-port 53 10.129.2.28 50000

Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Connected to 10.129.2.28:50000.
220 ProFTPd
```

---

## Travaux Pratiques sur l'Évasion de Pare-feu et d'IDS/IPS

Dans les trois prochaines sections, nous aurons différents scénarios à pratiquer où nous devrons scanner notre cible. Des règles de pare-feu et des IDS/IPS protègent les systèmes, nous devrons donc utiliser les techniques présentées pour contourner les règles du pare-feu et le faire de la manière la plus discrète possible. Sinon, nous serons bloqués par l'IPS.
---

← [[08 - Performances]] | [[00 - Sommaire Nmap|Sommaire]] | [[10 - Contournement de Pare-feu et d'IDS-IPS - Labo Facile]] →
