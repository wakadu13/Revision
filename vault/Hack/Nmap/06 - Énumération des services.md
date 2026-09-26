---
tags:
  - nmap
ordre: 6
---

# Énumération des services

---

Pour nous, il est essentiel de déterminer l'application et sa version aussi précisément que possible. Nous pouvons utiliser ces informations pour rechercher des vulnérabilités connues et analyser le code source de cette version si nous le trouvons. Un numéro de version exact nous permet de rechercher un exploit plus précis qui correspond au service et au système d'exploitation de notre cible.

---

## Détection de la version des services

Il est recommandé d'effectuer d'abord un scan de ports rapide, ce qui nous donne un petit aperçu des ports disponibles. Cela génère beaucoup moins de trafic, ce qui est avantageux pour nous car nous risquons sinon d'être découverts et bloqués par les mécanismes de sécurité. Nous pouvons nous occuper de ceux-ci en premier lieu et lancer un scan de ports en arrière-plan, qui affichera tous les ports ouverts (`-p-`). Nous pouvons utiliser le scan de version pour scanner les ports spécifiques à la recherche des services et de leurs versions (`-sV`).

Un scan de ports complet prend un temps considérable. Pour voir l'état du scan, nous pouvons appuyer sur la `[Barre d'espace]` pendant le scan, ce qui amènera `Nmap` à nous montrer l'état du scan.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p- -sV

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 19:44 CEST
[Space Bar]
Stats: 0:00:03 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 3.64% done; ETC: 19:45 (0:00:53 remaining)
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p-`|Scanne tous les ports.|
|`-sV`|Effectue une détection de version des services sur les ports spécifiés.|

---

Une autre option (`--stats-every=5s`) que nous pouvons utiliser est de définir la fréquence à laquelle l'état doit être affiché. Ici, nous pouvons spécifier le nombre de secondes (`s`) ou de minutes (`m`) après lesquelles nous voulons obtenir l'état.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p- -sV --stats-every=5s

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 19:46 CEST
Stats: 0:00:05 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 13.91% done; ETC: 19:49 (0:00:31 remaining)
Stats: 0:00:10 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 39.57% done; ETC: 19:48 (0:00:15 remaining)
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p-`|Scanne tous les ports.|
|`-sV`|Effectue une détection de version des services sur les ports spécifiés.|
|`--stats-every=5s`|Affiche la progression du scan toutes les 5 secondes.|

---

Nous pouvons également augmenter le `niveau de verbosité` (`-v` / `-vv`), ce qui nous montrera les ports ouverts directement lorsque `Nmap` les détecte.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p- -sV -v

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 20:03 CEST
NSE: Loaded 45 scripts for scanning.
Initiating ARP Ping Scan at 20:03
Scanning 10.129.2.28 [1 port]
Completed ARP Ping Scan at 20:03, 0.03s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 20:03
Completed Parallel DNS resolution of 1 host. at 20:03, 0.02s elapsed
Initiating SYN Stealth Scan at 20:03
Scanning 10.129.2.28 [65535 ports]
Discovered open port 995/tcp on 10.129.2.28
Discovered open port 80/tcp on 10.129.2.28
Discovered open port 993/tcp on 10.129.2.28
Discovered open port 143/tcp on 10.129.2.28
Discovered open port 25/tcp on 10.129.2.28
Discovered open port 110/tcp on 10.129.2.28
Discovered open port 22/tcp on 10.129.2.28
<SNIP>
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p-`|Scanne tous les ports.|
|`-sV`|Effectue une détection de version des services sur les ports spécifiés.|
|`-v`|Augmente la verbosité du scan, ce qui affiche des informations plus détaillées.|

---

## Capture de bannière

Une fois le scan terminé, nous verrons tous les ports TCP avec le service correspondant et leurs versions qui sont actifs sur le système.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p- -sV

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 20:00 CEST
Nmap scan report for 10.129.2.28
Host is up (0.013s latency).
Not shown: 65525 closed ports
PORT      STATE    SERVICE      VERSION
22/tcp    open     ssh          OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
25/tcp    open     smtp         Postfix smtpd
80/tcp    open     http         Apache httpd 2.4.29 ((Ubuntu))
110/tcp   open     pop3         Dovecot pop3d
139/tcp   filtered netbios-ssn
143/tcp   open     imap         Dovecot imapd (Ubuntu)
445/tcp   filtered microsoft-ds
993/tcp   open     ssl/imap     Dovecot imapd (Ubuntu)
995/tcp   open     ssl/pop3     Dovecot pop3d
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
Service Info: Host:  inlane; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 91.73 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p-`|Scanne tous les ports.|
|`-sV`|Effectue une détection de version des services sur les ports spécifiés.|

---

Principalement, `Nmap` examine les bannières des ports scannés et les affiche. S'il ne peut pas identifier les versions à travers les bannières, `Nmap` tente de les identifier via un système de correspondance basé sur les signatures, mais cela augmente considérablement la durée du scan. Un inconvénient des résultats présentés par `Nmap` est que le scan automatique peut manquer certaines informations car `Nmap` ne sait parfois pas comment les gérer. Regardons un exemple de ceci.

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p- -sV -Pn -n --disable-arp-ping --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-16 20:10 CEST
<SNIP>
NSOCK INFO [0.4200s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 18 [10.129.2.28:25] (35 bytes): 220 inlane ESMTP Postfix (Ubuntu)..
Service scan match (Probe NULL matched with NULL line 3104): 10.129.2.28:25 is smtp.  Version: |Postfix smtpd|||
NSOCK INFO [0.4200s] nsock_iod_delete(): nsock_iod_delete (IOD #1)
Nmap scan report for 10.129.2.28
Host is up (0.076s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
Service Info: Host:  inlane

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.47 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p-`|Scanne tous les ports.|
|`-sV`|Effectue une détection de version des services sur les ports spécifiés.|
|`-Pn`|Désactive les requêtes ICMP Echo.|
|`-n`|Désactive la résolution DNS.|
|`--disable-arp-ping`|Désactive le ping ARP.|
|`--packet-trace`|Affiche tous les paquets envoyés et reçus.|

---

Si nous regardons les résultats de `Nmap`, nous pouvons voir l'état du port, le nom du service et le nom d'hôte. Néanmoins, regardons cette ligne ici :

- `NSOCK INFO [0.4200s] nsock_trace_handler_callback(): Callback: READ SUCCESS for EID 18 [10.129.2.28:25] (35 bytes): 220 inlane ESMTP Postfix (Ubuntu)..`

Nous voyons alors que le serveur SMTP sur notre cible nous a donné plus d'informations que ce que `Nmap` nous a montré. Car ici, nous voyons qu'il s'agit de la distribution Linux `Ubuntu`. Cela se produit car, après un établissement de liaison en trois temps (three-way handshake) réussi, le serveur envoie souvent une bannière pour identification. Cela sert à faire savoir au client avec quel service il travaille. Au niveau du réseau, cela se produit avec un drapeau `PSH` dans l'en-tête TCP. Cependant, il peut arriver que certains services ne fournissent pas immédiatement de telles informations. Il est également possible de supprimer ou de manipuler les bannières des services respectifs. Si nous nous connectons `manuellement` au serveur SMTP en utilisant `nc`, que nous capturons la bannière et que nous interceptons le trafic réseau avec `tcpdump`, nous pouvons voir ce que `Nmap` ne nous a pas montré.

#### Tcpdump

```bash
Hiterof13@htb[/htb]$ sudo tcpdump -i eth0 host 10.10.14.2 and 10.129.2.28

tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
```

#### Nc

```bash
Hiterof13@htb[/htb]$  nc -nv 10.129.2.28 25

Connection to 10.129.2.28 port 25 [tcp/*] succeeded!
220 inlane ESMTP Postfix (Ubuntu)
```

#### Tcpdump - Trafic intercepté

```bash
18:28:07.128564 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [S], seq 1798872233, win 65535, options [mss 1460,nop,wscale 6,nop,nop,TS val 331260178 ecr 0,sackOK,eol], length 0
18:28:07.255151 IP 10.129.2.28.smtp > 10.10.14.2.59618: Flags [S.], seq 1130574379, ack 1798872234, win 65160, options [mss 1460,sackOK,TS val 1800383922 ecr 331260178,nop,wscale 7], length 0
18:28:07.255281 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [.], ack 1, win 2058, options [nop,nop,TS val 331260304 ecr 1800383922], length 0
18:28:07.319306 IP 10.129.2.28.smtp > 10.10.14.2.59618: Flags [P.], seq 1:36, ack 1, win 510, options [nop,nop,TS val 1800383985 ecr 331260304], length 35: SMTP: 220 inlane ESMTP Postfix (Ubuntu)
18:28:07.319426 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [.], ack 36, win 2058, options [nop,nop,TS val 331260368 ecr 1800383985], length 0
```

Les trois premières lignes nous montrent l'établissement de liaison en trois temps.

||||
|---|---|---|
|1.|`[SYN]`|`18:28:07.128564 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [S], <SNIP>`|
|2.|`[SYN-ACK]`|`18:28:07.255151 IP 10.129.2.28.smtp > 10.10.14.2.59618: Flags [S.], <SNIP>`|
|3.|`[ACK]`|`18:28:07.255281 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [.], <SNIP>`|

Après cela, le serveur SMTP cible nous envoie un paquet TCP avec les drapeaux `PSH` et `ACK`, où `PSH` indique que le serveur cible nous envoie des données et `ACK` nous informe simultanément que toutes les données requises ont été envoyées.

||||
|---|---|---|
|4.|`[PSH-ACK]`|`18:28:07.319306 IP 10.129.2.28.smtp > 10.10.14.2.59618: Flags [P.], <SNIP>`|

Le dernier paquet TCP que nous avons envoyé confirme la réception des données avec un `ACK`.

||||
|---|---|---|
|5.|`[ACK]`|`18:28:07.319426 IP 10.10.14.2.59618 > 10.129.2.28.smtp: Flags [.], <SNIP>`|
---

← [[05 - Sauvegarde des Résultats]] | [[00 - Sommaire Nmap|Sommaire]] | [[07 - Moteur de Scripts de Nmap]] →
