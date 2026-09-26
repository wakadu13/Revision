---
tags:
  - nmap
ordre: 3
---

# Découverte d'Hôtes

---

Lorsque nous devons effectuer un test d'intrusion (penetration test) interne sur l'ensemble du réseau d'une entreprise, par exemple, nous devons avant tout obtenir un aperçu des systèmes qui sont en ligne et avec lesquels nous pouvons travailler. Pour découvrir activement de tels systèmes sur le réseau, nous pouvons utiliser diverses options de découverte d'hôtes de `Nmap`. `Nmap` fournit de nombreuses options pour déterminer si notre cible est active ou non. La méthode de découverte d'hôtes la plus efficace consiste à utiliser des **requêtes d'écho ICMP (ICMP echo requests)**, que nous allons examiner.

Il est toujours recommandé de sauvegarder chaque scan. Cela pourra être utilisé plus tard pour la comparaison, la documentation et la création de rapports. Après tout, différents outils peuvent produire des résultats différents. Il peut donc être utile de distinguer quel outil produit quel résultat.

#### Scanner une Plage Réseau

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.0/24 -sn -oA tnet | grep for | cut -d" " -f5

10.129.2.4
10.129.2.10
10.129.2.11
10.129.2.18
10.129.2.19
10.129.2.20
10.129.2.28
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.0/24`|Plage réseau cible.|
|`-sn`|Désactive le scan de ports.|
|`-oA tnet`|Stocke les résultats dans tous les formats en commençant par le nom 'tnet'.|

Cette méthode de scan ne fonctionne que si les pare-feu (firewalls) des hôtes l'autorisent. Sinon, nous pouvons utiliser d'autres techniques de scan pour savoir si les hôtes sont actifs ou non. Nous examinerons ces techniques de plus près dans la section « Contournement de Pare-feu et d'IDS ».

---

## Scanner une Liste d'IP

Lors d'un test d'intrusion interne, il n'est pas rare qu'on nous fournisse une liste d'adresses IP avec les hôtes que nous devons tester. `Nmap` nous donne également la possibilité de travailler avec des listes et de lire les hôtes à partir de cette liste au lieu de les définir ou de les taper manuellement.

Une telle liste pourrait ressembler à ceci :

```bash
Hiterof13@htb[/htb]$ cat hosts.lst

10.129.2.4
10.129.2.10
10.129.2.11
10.129.2.18
10.129.2.19
10.129.2.20
10.129.2.28
```

Si nous utilisons la même technique de scan sur la liste prédéfinie, la commande ressemblera à ceci :

```bash
Hiterof13@htb[/htb]$ sudo nmap -sn -oA tnet -iL hosts.lst | grep for | cut -d" " -f5

10.129.2.18
10.129.2.19
10.129.2.20
```

|**Options de Scan**|**Description**|
|---|---|
|`-sn`|Désactive le scan de ports.|
|`-oA tnet`|Stocke les résultats dans tous les formats en commençant par le nom 'tnet'.|
|`-iL`|Effectue les scans définis sur les cibles de la liste 'hosts.lst' fournie.|

Dans cet exemple, nous voyons que seuls 3 des 7 hôtes sont actifs. N'oubliez pas que cela peut signifier que les autres hôtes ignorent les **requêtes d'écho ICMP** par défaut en raison des configurations de leur pare-feu. Comme `Nmap` ne reçoit pas de réponse, il marque ces hôtes comme inactifs.

---

## Scanner Plusieurs IP

Il peut également arriver que nous n'ayons besoin de scanner qu'une petite partie d'un réseau. Une alternative à la méthode que nous avons utilisée la dernière fois consiste à spécifier plusieurs adresses IP.

```bash
Hiterof13@htb[/htb]$ sudo nmap -sn -oA tnet 10.129.2.18 10.129.2.19 10.129.2.20| grep for | cut -d" " -f5

10.129.2.18
10.129.2.19
10.129.2.20
```

Si ces adresses IP sont adjacentes, nous pouvons également définir la plage dans l'octet correspondant.

```bash
Hiterof13@htb[/htb]$ sudo nmap -sn -oA tnet 10.129.2.18-20| grep for | cut -d" " -f5

10.129.2.18
10.129.2.19
10.129.2.20
```

---

## Scanner une Seule IP

Avant de scanner un seul hôte pour les ports ouverts et ses services, nous devons d'abord déterminer s'il est actif ou non. Pour cela, nous pouvons utiliser la même méthode que précédemment.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.18 -sn -oA host

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-14 23:59 CEST
Nmap scan report for 10.129.2.18
Host is up (0.087s latency).
MAC Address: DE:AD:00:00:BE:EF
Nmap done: 1 IP address (1 host up) scanned in 0.11 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.18`|Effectue les scans définis sur la cible.|
|`-sn`|Désactive le scan de ports.|
|`-oA host`|Stocke les résultats dans tous les formats en commençant par le nom 'host'.|

Si nous désactivons le scan de ports (port scanning) (`-sn`), Nmap effectue automatiquement un scan par ping avec des `requêtes d'écho ICMP` (`-PE`). Une fois qu'une telle requête est envoyée, nous nous attendons généralement à une `réponse ICMP` si l'hôte contacté est actif. Le fait le plus intéressant est que nos scans précédents n'ont pas fait cela, car avant que Nmap ne puisse envoyer une requête d'écho ICMP, il envoyait un `ping ARP` qui résultait en une `réponse ARP`. Nous pouvons le confirmer avec l'option « `--packet-trace` ». Pour garantir que des requêtes d'écho ICMP sont bien envoyées, nous définissons également l'option (`-PE`) pour cela.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.18 -sn -oA host -PE --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 00:08 CEST
SENT (0.0074s) ARP who-has 10.129.2.18 tell 10.10.14.2
RCVD (0.0309s) ARP reply 10.129.2.18 is-at DE:AD:00:00:BE:EF
Nmap scan report for 10.129.2.18
Host is up (0.023s latency).
MAC Address: DE:AD:00:00:BE:EF
Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.18`|Effectue les scans définis sur la cible.|
|`-sn`|Désactive le scan de ports.|
|`-oA host`|Stocke les résultats dans tous les formats en commençant par le nom 'host'.|
|`-PE`|Effectue le scan par ping en utilisant des 'requêtes d'écho ICMP' sur la cible.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus|

---

Une autre façon de déterminer pourquoi Nmap a marqué notre cible comme « active » est avec l'option « `--reason` ».

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.18 -sn -oA host -PE --reason

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 00:10 CEST
SENT (0.0074s) ARP who-has 10.129.2.18 tell 10.10.14.2
RCVD (0.0309s) ARP reply 10.129.2.18 is-at DE:AD:00:00:BE:EF
Nmap scan report for 10.129.2.18
Host is up, received arp-response (0.028s latency).
MAC Address: DE:AD:00:00:BE:EF
Nmap done: 1 IP address (1 host up) scanned in 0.03 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.18`|Effectue les scans définis sur la cible.|
|`-sn`|Désactive le scan de ports.|
|`-oA host`|Stocke les résultats dans tous les formats en commençant par le nom 'host'.|
|`-PE`|Effectue le scan par ping en utilisant des 'requêtes d'écho ICMP' sur la cible.|
|`--reason`|Affiche la raison d'un résultat spécifique.|

---

Nous voyons ici que `Nmap` détecte bien si l'hôte est actif ou non uniquement grâce à la `requête ARP` et à la `réponse ARP`. Pour désactiver les requêtes ARP et scanner notre cible avec les `requêtes d'écho ICMP` souhaitées, nous pouvons désactiver les pings ARP en utilisant l'option « `--disable-arp-ping` ». Ensuite, nous pouvons scanner notre cible à nouveau et examiner les paquets envoyés et reçus.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.18 -sn -oA host -PE --packet-trace --disable-arp-ping

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 00:12 CEST
SENT (0.0107s) ICMP [10.10.14.2 > 10.129.2.18 Echo request (type=8/code=0) id=13607 seq=0] IP [ttl=255 id=23541 iplen=28 ]
RCVD (0.0152s) ICMP [10.129.2.18 > 10.10.14.2 Echo reply (type=0/code=0) id=13607 seq=0] IP [ttl=128 id=40622 iplen=28 ]
Nmap scan report for 10.129.2.18
Host is up (0.086s latency).
MAC Address: DE:AD:00:00:BE:EF
Nmap done: 1 IP address (1 host up) scanned in 0.11 seconds
```

Nous l'avons déjà mentionné dans le « Processus d'Apprentissage » et au début de ce module, il est essentiel de prêter attention aux détails. Une `requête d'écho ICMP` peut nous aider à déterminer si notre cible est active et à identifier son système. Vous trouverez plus de stratégies sur la découverte d'hôtes à l'adresse suivante :

[https://nmap.org/book/host-discovery-strategies.html](https://nmap.org/book/host-discovery-strategies.html)
---

← [[02 - Introduction à Nmap]] | [[00 - Sommaire Nmap|Sommaire]] | [[04 - Scan d'hôtes et de ports]] →
