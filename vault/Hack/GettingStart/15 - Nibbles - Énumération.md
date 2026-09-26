---
tags:
  - getting-started
ordre: 15
---

# Nibbles - Énumération

---

Au moment de la rédaction de ce document, 201 machines autonomes de divers systèmes d'exploitation et niveaux de difficulté sont à notre disposition sur la plateforme HTB avec un abonnement VIP. Cet abonnement inclut un walkthrough officiel (solution pas à pas) créé par HTB pour chaque machine retirée. Nous pouvons également trouver des walkthroughs sous forme de blogs et de vidéos pour la plupart des machines avec une recherche rapide sur Google.

Pour nos besoins, nous allons parcourir la machine `Nibbles`, une machine Linux de niveau facile qui présente des tactiques d'énumération courantes, l'exploitation basique d'une application web, et une mauvaise configuration liée à un fichier pour escalader les privilèges.

![Détails de la machine Nibbles : OS Linux, difficulté Facile, 20 points, publiée le 13 janv. 2018, IP 10.10.10.75.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/nibbles_card.png)

Examinons d'abord quelques statistiques de la machine :

|Nom de la machine|Nibbles|
|---|---|
|Créateur|mrb3n|
|Système d'exploitation|Linux|
|Difficulté|Facile|
|Chemin d'accès utilisateur|Web|
|Escalade de privilèges|Fichier inscriptible par tous / Mauvaise configuration de Sudoers|
|Vidéo Ippsec|[https://www.youtube.com/watch?v=s_0GcRGv6Ds](https://www.youtube.com/watch?v=s_0GcRGv6Ds)|
|Walkthrough|[https://0xdf.gitlab.io/2018/06/30/htb-nibbles.html](https://0xdf.gitlab.io/2018/06/30/htb-nibbles.html)|

Notre première étape lorsque nous abordons une machine est d'effectuer une énumération de base. Commençons d'abord par ce que nous savons de la cible. Nous connaissons déjà l'adresse IP de la cible, qu'il s'agit de Linux, et qu'elle a un vecteur d'attaque lié au web. Nous appelons cela une approche en boîte grise (grey-box) car nous avons quelques informations sur la cible. Sur la plateforme HTB, les 20 machines « actives » publiées chaque semaine sont toutes abordées depuis une perspective de boîte noire (black-box). Les utilisateurs reçoivent l'adresse IP et le type de système d'exploitation à l'avance, mais aucune information supplémentaire sur la cible pour formuler leurs attaques. C'est pourquoi une énumération approfondie est essentielle et constitue souvent un processus itératif.

Avant de continuer, prenons un peu de recul et examinons les différentes approches des actions de test d'intrusion (penetration testing). Il en existe trois types principaux, `black-box`, `grey-box` et `white-box`, et chacun diffère par son objectif et son approche.

|**Type d'engagement**|**Description**|
|---|---|
|`Black-Box`|Connaissance faible ou nulle d'une cible. Le testeur d'intrusion doit effectuer une reconnaissance approfondie pour en savoir plus sur la cible. Il peut s'agir d'un test d'intrusion externe où le testeur ne reçoit que le nom de l'entreprise et aucune autre information telle que les adresses IP cibles, ou d'un test d'intrusion interne où le testeur doit soit contourner les contrôles pour obtenir un accès initial au réseau, soit peut se connecter au réseau interne mais n'a aucune information sur les réseaux/hôtes internes. Ce type de test d'intrusion simule le mieux une attaque réelle mais n'est pas aussi complet que d'autres types d'évaluation et pourrait laisser des mauvaises configurations/vulnérabilités non découvertes.|
|`Grey-Box`|Dans un test en boîte grise, le testeur reçoit une certaine quantité d'informations à l'avance. Il peut s'agir d'une liste d'adresses/plages IP dans le périmètre, d'identifiants de bas niveau pour une application web ou Active Directory, ou de certains diagrammes d'application/réseau. Ce type de test d'intrusion peut simuler un initié malveillant ou voir ce qu'un attaquant peut faire avec un faible niveau d'accès. Dans ce scénario, le testeur passera généralement moins de temps en reconnaissance et plus de temps à rechercher des mauvaises configurations et à tenter une exploitation.|
|`White-Box`|Dans ce type de test, le testeur reçoit un accès complet. Dans un test d'application web, il peut recevoir des identifiants de niveau administrateur, un accès au code source, des schémas de construction, etc., pour rechercher des vulnérabilités logiques et d'autres failles difficiles à découvrir. Dans un test de réseau, il peut recevoir des identifiants de niveau administrateur pour fouiller dans Active Directory ou d'autres systèmes à la recherche de mauvaises configurations qui pourraient autrement passer inaperçues. Ce type d'évaluation est très complet car le testeur aura accès aux deux côtés d'une cible et effectuera une analyse exhaustive.|

---

## Nmap

Commençons par un scan `nmap` rapide pour rechercher les ports ouverts en utilisant la commande `nmap -sV --open -oA nibbles_initial_scan <ip address>`. Cela exécutera un scan d'énumération de service (`-sV`) sur les 1 000 ports les plus courants par défaut et ne retournera que les ports ouverts (`--open`). Nous pouvons vérifier quels ports `nmap` scanne pour un type de scan donné en exécutant un scan sans cible spécifiée, en utilisant la commande `nmap -v -oG -`. Ici, nous afficherons le format « greppable » sur la sortie standard avec `-oG -` et `-v` pour une sortie verbeuse. Comme aucune cible n'est spécifiée, le scan échouera mais affichera les ports scannés.

```bash
Hiterof13@htb[/htb]$ nmap -v -oG -
# Nmap 7.80 scan initiated Wed Dec 16 23:22:26 2020 as: nmap -v -oG -  # Ports scanned: TCP(1000;1,3-4,6-7,9,13,17,19-26,30,32-33,37,42-43,49,53,70,79-85,88-90,99-100,106,109-111,113,119,125,135,139,143-144,146,161,163,179,199,211-212,222,254-256,259,264,280,301,306,311,340,366,389,406-407,416-417,425,427,443-445,458,464-465,481,497,500,512-515,524,541,543-545,548,554-555,563,587,593,616-617,625,631,636,646,648,666-668,683,687,691,700,705,711,714,720,722,726,749,765,777,783,787,800-801,808,843,873,880,888,898,900-903,911-912,981,987,990,992-993,995,999-1002,1007,1009-1011,1021-1100,1102,1104-1108,1110-1114,1117,1119,1121-1124,1126,1130-1132,1137-1138,1141,1145,1147-1149,1151-1152,1154,1163-1166,1169,1174-1175,1183,1185-1187,1192,1198-1199,1201,1213,1216-1218,1233-1234,1236,1244,1247-1248,1259,1271-1272,1277,1287,1296,1300-1301,1309-1311,1322,1328,1334,1352,1417,1433-1434,1443,1455,1461,1494,1500-1501,1503,1521,1524,1533,1556,1580,1583,1594,1600,1641,1658,1666,1687-1688,1700,1717-1721,1723,1755,1761,1782-1783,1801,1805,1812,1839-1840,1862-1864,1875,1900,1914,1935,1947,1971-1972,1974,1984,1998-2010,2013,2020-2022,2030,2033-2035,2038,2040-2043,2045-2049,2065,2068,2099-2100,2103,2105-2107,2111,2119,2121,2126,2135,2144,2160-2161,2170,2179,2190-2191,2196,2200,2222,2251,2260,2288,2301,2323,2366,2381-2383,2393-2394,2399,2401,2492,2500,2522,2525,2557,2601-2602,2604-2605,2607-2608,2638,2701-2702,2710,2717-2718,2725,2800,2809,2811,2869,2875,2909-2910,2920,2967-2968,2998,3000-3001,3003,3005-3007,3011,3013,3017,3030-3031,3052,3071,3077,3128,3168,3211,3221,3260-3261,3268-3269,3283,3300-3301,3306,3322-3325,3333,3351,3367,3369-3372,3389-3390,3404,3476,3493,3517,3527,3546,3551,3580,3659,3689-3690,3703,3737,3766,3784,3800-3801,3809,3814,3826-3828,3851,3869,3871,3878,3880,3889,3905,3914,3918,3920,3945,3971,3986,3995,3998,4000-4006,4045,4111,4125-4126,4129,4224,4242,4279,4321,4343,4443-4446,4449,4550,4567,4662,4848,4899-4900,4998,5000-5004,5009,5030,5033,5050-5051,5054,5060-5061,5080,5087,5100-5102,5120,5190,5200,5214,5221-5222,5225-5226,5269,5280,5298,5357,5405,5414,5431-5432,5440,5500,5510,5544,5550,5555,5560,5566,5631,5633,5666,5678-5679,5718,5730,5800-5802,5810-5811,5815,5822,5825,5850,5859,5862,5877,5900-5904,5906-5907,5910-5911,5915,5922,5925,5950,5952,5959-5963,5987-5989,5998-6007,6009,6025,6059,6100-6101,6106,6112,6123,6129,6156,6346,6389,6502,6510,6543,6547,6565-6567,6580,6646,6666-6669,6689,6692,6699,6779,6788-6789,6792,6839,6881,6901,6969,7000-7002,7004,7007,7019,7025,7070,7100,7103,7106,7200-7201,7402,7435,7443,7496,7512,7625,7627,7676,7741,7777-7778,7800,7911,7920-7921,7937-7938,7999-8002,8007-8011,8021-8022,8031,8042,8045,8080-8090,8093,8099-8100,8180-8181,8192-8194,8200,8222,8254,8290-8292,8300,8333,8383,8400,8402,8443,8500,8600,8649,8651-8652,8654,8701,8800,8873,8888,8899,8994,9000-9003,9009-9011,9040,9050,9071,9080-9081,9090-9091,9099-9103,9110-9111,9200,9207,9220,9290,9415,9418,9485,9500,9502-9503,9535,9575,9593-9595,9618,9666,9876-9878,9898,9900,9917,9929,9943-9944,9968,9998-10004,10009-10010,10012,10024-10025,10082,10180,10215,10243,10566,10616-10617,10621,10626,10628-10629,10778,11110-11111,11967,12000,12174,12265,12345,13456,13722,13782-13783,14000,14238,14441-14442,15000,15002-15004,15660,15742,16000-16001,16012,16016,16018,16080,16113,16992-16993,17877,17988,18040,18101,18988,19101,19283,19315,19350,19780,19801,19842,20000,20005,20031,20221-20222,20828,21571,22939,23502,24444,24800,25734-25735,26214,27000,27352-27353,27355-27356,27715,28201,30000,30718,30951,31038,31337,32768-32785,33354,33899,34571-34573,35500,38292,40193,40911,41511,42510,44176,44442-44443,44501,45100,48080,49152-49161,49163,49165,49167,49175-49176,49400,49999-50003,50006,50300,50389,50500,50636,50800,51103,51493,52673,52822,52848,52869,54045,54328,55055-55056,55555,55600,56737-56738,57294,57797,58080,60020,60443,61532,61900,62078,63331,64623,64680,65000,65129,65389) UDP(0;) SCTP(0;) PROTOCOLS(0;)  WARNING: No targets were specified, so 0 hosts scanned.
# Nmap done at Wed Dec 16 23:22:26 2020 -- 0 IP addresses (0 hosts up) scanned in 0.04 seconds
```

Enfin, nous allons générer tous les formats de scan en utilisant `-oA`. Cela inclut une sortie XML, une sortie au format « greppable » et une sortie texte qui pourraient nous être utiles plus tard. Il est essentiel de prendre l'habitude de prendre des notes détaillées et de sauvegarder toutes les sorties de console dès le début. Mieux nous maîtriserons cette pratique, plus elle deviendra une seconde nature lors d'engagements réels. Une prise de notes appropriée est cruciale pour nous en tant que testeurs d'intrusion et accélérera considérablement le processus de rédaction de rapports tout en garantissant qu'aucune preuve n'est perdue. Il est également essentiel de conserver des journaux horodatés détaillés des tentatives de scan et d'exploitation en cas de panne ou d'incident pour lequel le client a besoin d'informations sur nos activités.

```bash
Hiterof13@htb[/htb]$ nmap -sV --open -oA nibbles_initial_scan 10.129.42.190
Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-16 23:18 EST
Nmap scan report for 10.129.42.190
Host is up (0.11s latency).
Not shown: 991 closed ports, 7 filtered ports Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd <REDACTED> ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 11.82 seconds
```

D'après la sortie du scan initial, nous pouvons voir que l'hôte est probablement un Linux Ubuntu et expose un serveur web Apache sur le port 80 et un serveur OpenSSH sur le port 22. SSH, ou [Secure Shell](https://en.wikipedia.org/wiki/SSH_\(Secure_Shell\)), est un protocole généralement utilisé pour l'accès à distance aux hôtes Linux/Unix. SSH peut également être utilisé pour accéder aux hôtes Windows et est maintenant natif de Windows 10 depuis la version 1809. Nous pouvons également voir que les trois types de sortie de scan ont été créés dans notre répertoire de travail.

```bash
Hiterof13@htb[/htb]$ ls  nibbles_initial_scan.gnmap  nibbles_initial_scan.nmap  nibbles_initial_scan.xml
```

Avant de commencer à fouiller les ports ouverts, nous pouvons lancer un scan complet des ports TCP en utilisant la commande `nmap -p- --open -oA nibbles_full_tcp_scan 10.129.42.190`. Cela vérifiera la présence de services fonctionnant sur des ports non standard que notre scan initial aurait pu manquer. Comme cela scanne les 65 535 ports TCP, cela peut prendre beaucoup de temps en fonction du réseau. Nous pouvons laisser cela tourner en arrière-plan et continuer notre énumération. L'utilisation de `nc` pour faire de la capture de bannière (banner grabbing) confirme ce que `nmap` nous a dit ; la cible exécute un serveur web Apache et un serveur OpenSSH.

```bash
Hiterof13@htb[/htb]$ nc -nv 10.129.42.190 22  (UNKNOWN) [10.129.42.190] 22 (ssh) open SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.8
```

`nc` nous indique que le port 80 exécute un serveur HTTP (web) mais n'affiche pas la bannière.

```bash
Hiterof13@htb[/htb]$ nc -nv 10.129.42.190 80  (UNKNOWN) [10.129.42.190] 80 (http) open
```

En vérifiant notre autre fenêtre de terminal, nous pouvons voir que le scan complet des ports (`-p-`) est terminé et n'a trouvé aucun port supplémentaire. Effectuons un scan par [script](https://nmap.org/book/man-nse.html) `nmap` en utilisant l'indicateur `-sC`. Cet indicateur utilise les scripts par défaut, qui sont listés [ici](https://nmap.org/nsedoc/categories/default.html). Ces scripts peuvent être intrusifs, il est donc toujours important de comprendre exactement comment fonctionnent nos outils. Nous exécutons la commande `nmap -sC -p 22,80 -oA nibbles_script_scan 10.129.42.190`. Comme nous savons déjà quels ports sont ouverts, nous pouvons gagner du temps et limiter le trafic de scan inutile en spécifiant les ports cibles avec `-p`.

```bash
Hiterof13@htb[/htb]$ nmap -sC -p 22,80 -oA nibbles_script_scan 10.129.42.190
Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-16 23:39 EST
Nmap scan report for 10.129.42.190
Host is up (0.11s latency).
PORT   STATE SERVICE
22/tcp open  ssh
| ssh-hostkey:  |   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA) |   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
|_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
80/tcp open  http
|_http-title: Site doesn't have a title (text/html).
Nmap done: 1 IP address (1 host up) scanned in 4.42 seconds
```

Le scan par script ne nous a rien donné d'utile. Complétons notre énumération `nmap` en utilisant le script [http-enum](https://nmap.org/nsedoc/scripts/http-enum.html), qui peut être utilisé pour énumérer les répertoires courants d'applications web. Ce scan n'a rien révélé d'utile non plus.

```bash
Hiterof13@htb[/htb]$ nmap -sV --script=http-enum -oA nibbles_nmap_http_enum 10.129.42.190
Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-16 23:41 EST
Nmap scan report for 10.129.42.190
Host is up (0.11s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd <REDACTED> ((Ubuntu))
|_http-server-header: Apache/<REDACTED> (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.23 seconds
```

---

← [[14 - Naviguer sur HTB]] | [[00 - Sommaire Getting Started|Sommaire]] | [[16 - Nibbles - Reconnaissance Web]] →
