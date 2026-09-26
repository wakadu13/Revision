---
tags:
  - nmap
ordre: 7
---

# Moteur de Scripts de Nmap

---

Le Moteur de Scripts de Nmap (`NSE` pour Nmap Scripting Engine) est une autre fonctionnalité pratique de `Nmap`. Il nous offre la possibilité de créer des scripts en Lua pour interagir avec certains services. Il y a un total de 14 catégories dans lesquelles ces scripts peuvent être divisés :

|**Catégorie**|**Description**|
|---|---|
|`auth`|Détermination des identifiants d'authentification.|
|`broadcast`|Scripts utilisés pour la découverte d'hôtes par diffusion (broadcasting) ; les hôtes découverts peuvent être automatiquement ajoutés aux scans restants.|
|`brute`|Exécute des scripts qui tentent de se connecter au service respectif par force brute (brute-forcing) avec des identifiants.|
|`default`|Scripts par défaut exécutés en utilisant l'option `-sC`.|
|`discovery`|Évaluation des services accessibles.|
|`dos`|Ces scripts sont utilisés pour vérifier les vulnérabilités de déni de service (denial of service) des services et sont moins utilisés car ils endommagent les services.|
|`exploit`|Cette catégorie de scripts tente d'exploiter les vulnérabilités connues pour le port scanné.|
|`external`|Scripts qui utilisent des services externes pour un traitement ultérieur.|
|`fuzzer`|Utilise des scripts pour identifier les vulnérabilités et la gestion inattendue de paquets en envoyant différents champs, ce qui peut prendre beaucoup de temps.|
|`intrusive`|Scripts intrusifs qui pourraient affecter négativement le système cible.|
|`malware`|Vérifie si un logiciel malveillant (malware) infecte le système cible.|
|`safe`|Scripts défensifs qui n'effectuent pas d'accès intrusif ou destructeur.|
|`version`|Extension pour la détection de service.|
|`vuln`|Identification de vulnérabilités spécifiques.|

Nous avons plusieurs façons de définir les scripts souhaités dans `Nmap`.

#### Scripts par défaut

```bash
Hiterof13@htb[/htb]$ sudo nmap <target> -sC
```

#### Catégorie de scripts spécifique

```bash
Hiterof13@htb[/htb]$ sudo nmap <target> --script <category>
```

#### Scripts définis

```bash
Hiterof13@htb[/htb]$ sudo nmap <target> --script <script-name>,<script-name>,...
```

Par exemple, continuons à travailler avec le port SMTP cible et voyons les résultats que nous obtenons avec deux scripts définis.

#### Nmap - Spécifier des scripts

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 25 --script banner,smtp-commands

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-16 23:21 CEST
Nmap scan report for 10.129.2.28
Host is up (0.050s latency).

PORT   STATE SERVICE
25/tcp open  smtp
|_banner: 220 inlane ESMTP Postfix (Ubuntu)
|_smtp-commands: inlane, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8,
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p 25`|Scanne uniquement le port spécifié.|
|`--script banner,smtp-commands`|Utilise les scripts NSE spécifiés.|

Nous voyons que nous pouvons reconnaître la distribution Linux **Ubuntu** en utilisant le script `banner`. Le script `smtp-commands` nous montre quelles commandes nous pouvons utiliser en interagissant avec le serveur SMTP cible. Dans cet exemple, de telles informations peuvent nous aider à trouver des utilisateurs existants sur la cible. `Nmap` nous donne également la possibilité de scanner notre cible avec l'option agressive (`-A`). Cela scanne la cible avec plusieurs options comme la détection de service (`-sV`), la détection d'OS (`-O`), le traceroute (`--traceroute`), et avec les scripts NSE par défaut (`-sC`).

#### Nmap - Scan agressif

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 80 -A
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-17 01:38 CEST
Nmap scan report for 10.129.2.28
Host is up (0.012s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-generator: WordPress 5.3.4
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: blog.inlanefreight.com
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 2.6.32 (96%), Linux 3.2 - 4.9 (96%), Linux 2.6.32 - 3.10 (96%), Linux 3.4 - 3.10 (95%), Linux 3.1 (95%), Linux 3.2 (95%),
AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), Synology DiskStation Manager 5.2-5644 (94%), Netgear RAIDiator 4.2.28 (94%),
Linux 2.6.32 - 2.6.35 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop

TRACEROUTE
HOP RTT      ADDRESS
1   11.91 ms 10.129.2.28

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.36 seconds
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p 80`|Scanne uniquement le port spécifié.|
|`-A`|Effectue la détection de service, la détection d'OS, un traceroute et utilise les scripts par défaut pour scanner la cible.|

Avec l'aide de l'option de scan utilisée (`-A`), nous avons découvert quel type de serveur web (`Apache 2.4.29`) est en cours d'exécution sur le système, quelle application web (`WordPress 5.3.4`) est utilisée, et le titre (`blog.inlanefreight.com`) de la page web. De plus, `Nmap` montre qu'il s'agit probablement d'un système d'exploitation `Linux` (`96%`).

---

## Évaluation des vulnérabilités

Passons maintenant au port HTTP 80 et voyons quelles informations et vulnérabilités nous pouvons trouver en utilisant la catégorie `vuln` du `NSE`.

#### Nmap - Catégorie Vuln

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p 80 -sV --script vuln

Nmap scan report for 10.129.2.28
Host is up (0.036s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-enum:
|   /wp-login.php: Possible admin folder
|   /readme.html: Wordpress version: 2
|   /: WordPress version: 5.3.4
|   /wp-includes/images/rss.png: Wordpress version 2.2 found.
|   /wp-includes/js/jquery/suggest.js: Wordpress version 2.5 found.
|   /wp-includes/images/blank.gif: Wordpress version 2.6 found.
|   /wp-includes/js/comment-reply.js: Wordpress version 2.7 found.
|   /wp-login.php: Wordpress login page.
|   /wp-admin/upgrade.php: Wordpress login page.
|_  /readme.html: Interesting, a readme.
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| http-wordpress-users:
| Username found: admin
|_Search stopped at ID #25. Increase the upper limit if necessary with 'http-wordpress-users.limit'
| vulners:
|   cpe:/a:apache:http_server:2.4.29:
|       CVE-2019-0211   7.2 https://vulners.com/cve/CVE-2019-0211
|       CVE-2018-1312   6.8 https://vulners.com/cve/CVE-2018-1312
|       CVE-2017-15715  6.8 https://vulners.com/cve/CVE-2017-15715
<SNIP>
```

|**Options de scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p 80`|Scanne uniquement le port spécifié.|
|`-sV`|Effectue la détection de version de service sur les ports spécifiés.|
|`--script vuln`|Utilise tous les scripts associés de la catégorie spécifiée.|

Les scripts utilisés pour le dernier scan interagissent avec le serveur web et son application web pour trouver plus d'informations sur leurs versions et vérifier diverses bases de données pour voir s'il existe des vulnérabilités connues. Plus d'informations sur les scripts NSE et les catégories correspondantes peuvent être trouvées à l'adresse suivante : [https://nmap.org/nsedoc/index.html](https://nmap.org/nsedoc/index.html)
---

← [[06 - Énumération des services]] | [[00 - Sommaire Nmap|Sommaire]] | [[08 - Performances]] →
