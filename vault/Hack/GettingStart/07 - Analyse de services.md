---
tags:
  - getting-started
ordre: 7
---

# Analyse de services

---

Nous sommes prêts à aller plus loin et à commencer à explorer une machine ! La première chose à faire est d'identifier le système d'exploitation et tous les services disponibles qui pourraient être en cours d'exécution. Un service est une application s'exécutant sur un ordinateur qui remplit une fonction utile pour d'autres utilisateurs ou ordinateurs. Nous appelons ces machines spécialisées qui hébergent ces services utiles des « serveurs » plutôt que des postes de travail, permettant aux utilisateurs d'interagir avec ces divers services et de les consommer. Ce qui nous intéresse, ce sont les services qui ont été mal configurés ou qui présentent une vulnérabilité. Au lieu d'effectuer les actions attendues dans le cadre du service, nous voulons voir si nous pouvons forcer le service à effectuer une action non intentionnelle qui soutient nos objectifs, comme l'exécution d'une commande de notre choix.

Les ordinateurs se voient attribuer une adresse IP, ce qui leur permet d'être identifiés de manière unique et d'être accessibles sur un réseau. Les services fonctionnant sur ces ordinateurs peuvent se voir attribuer un numéro de port pour rendre le service accessible. Comme nous l'avons vu précédemment, les numéros de port vont de 1 à 65 535, la plage des ports bien connus (well-known ports) allant de 1 à 1 023 étant réservée aux services privilégiés. Le port 0 est un port réservé dans le réseautage TCP/IP et n'est pas utilisé dans les messages TCP ou UDP. Si quelque chose tente de se lier au port 0 (comme un service), il se liera au prochain port disponible au-dessus du port 1 024, car le port 0 est traité comme un port « joker » (wild card).

Pour accéder à un service à distance, nous devons nous connecter en utilisant la bonne adresse IP et le bon numéro de port et utiliser un langage que le service comprend. L'examen manuel de l'ensemble des 65 535 ports pour tout service disponible serait laborieux. Des outils ont donc été créés pour automatiser ce processus et analyser la plage de ports pour nous. L'un des outils d'analyse (scanning tools) les plus couramment utilisés est Nmap (Network Mapper).

---

## Nmap

Commençons par l'analyse la plus basique. Supposons que nous voulions effectuer une analyse de base sur une cible située à l'adresse `10.129.42.253`. Pour ce faire, nous devons taper `nmap 10.129.42.253` et appuyer sur Entrée. Nous voyons que l'analyse `Nmap` s'est terminée très rapidement. C'est parce que si nous ne spécifions aucune option supplémentaire, Nmap n'analysera par défaut que les 1 000 ports les plus courants. Le résultat de l'analyse révèle que les ports 21, 22, 80, 139 et 445 sont disponibles.

```bash
Hiterof13@htb[/htb]$ nmap 10.129.42.253
Starting Nmap 7.80 ( https://nmap.org ) at 2021-02-25 16:07 EST
Nmap scan report for 10.129.42.253
Host is up (0.11s latency).
Not shown: 995 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds
Nmap done: 1 IP address (1 host up) scanned in 2.19 seconds
```

Sous l'en-tête `PORT`, il nous est également indiqué qu'il s'agit de ports TCP. Par défaut, `Nmap` effectuera une analyse TCP (TCP scan) à moins qu'il ne lui soit spécifiquement demandé d'effectuer une analyse UDP (UDP scan). L'en-tête `STATE` confirme que ces ports sont ouverts. Parfois, nous verrons d'autres ports listés qui ont un état différent, tel que `filtered`. Cela peut se produire si un pare-feu (firewall) n'autorise l'accès aux ports qu'à partir d'adresses spécifiques. L'en-tête `SERVICE` nous indique le nom du service généralement associé au numéro de port spécifique. Cependant, l'analyse par défaut ne nous dira pas ce qui est à l'écoute sur ce port. Tant que nous n'aurons pas demandé à `Nmap` d'interagir avec le service et de tenter d'en extraire des informations d'identification, il pourrait s'agir d'un tout autre service.

En nous familiarisant, nous remarquerons que plusieurs ports sont couramment associés à Windows ou Linux. Par exemple, le port 3389 est le port par défaut pour les Services de Bureau à Distance (Remote Desktop Services) et constitue une excellente indication que la cible est une machine Windows. Dans notre scénario actuel, la disponibilité du port 22 (SSH) indique que la cible exécute Linux/Unix, mais ce service peut également être configuré sur Windows. Lançons une analyse `Nmap` plus avancée et recueillons plus d'informations sur le périphérique cible.

Nous pouvons utiliser le paramètre `-sC` pour spécifier que les scripts `Nmap` doivent être utilisés pour essayer d'obtenir des informations plus détaillées. Le paramètre `-sV` demande à `Nmap` d'effectuer une analyse de version (version scan). Dans cette analyse, Nmap prendra l'empreinte (fingerprint) des services sur le système cible et identifiera le protocole du service, le nom de l'application et sa version. L'analyse de version s'appuie sur une base de données complète de plus de 1 000 signatures de service (service signatures). Enfin, `-p-` indique à Nmap que nous voulons analyser les 65 535 ports TCP.

```bash
Hiterof13@htb[/htb]$ nmap -sV -sC -p- 10.129.42.253
Starting Nmap 7.80 ( https://nmap.org ) at 2021-02-25 16:18 EST
Nmap scan report for 10.129.42.253
Host is up (0.11s latency).
Not shown: 65530 closed ports
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 ftp      ftp          4096 Feb 25 19:25 pub
| ftp-syst:  |   STAT:
| FTP server status: |      Connected to ::ffff:10.10.14.2 |      Logged in as ftp |      TYPE: ASCII |      No session bandwidth limit |      Session timeout in seconds is 300 |      Control connection is plain text |      Data connections will be plain text |      At session startup, client count was 2 |      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
80/tcp  open  http        Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: PHP 7.4.3 - phpinfo()
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
Host script results:
|_nbstat: NetBIOS name: GS-SVCSCAN, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode:  |   2.02:
|_    Message signing enabled but not required
| smb2-time:  |   date: 2021-02-25T21:21:51
|_  start_date: N/A
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 233.68 seconds
```

Cela renvoie beaucoup plus d'informations. Nous voyons qu'il a fallu beaucoup plus de temps pour analyser 65 535 ports que 1 000. Les options `-sC` et `-sV` augmentent également la durée d'une analyse, car au lieu d'effectuer une simple poignée de main TCP, elles effectuent beaucoup plus de vérifications. Nous remarquons que cette fois, il y a un en-tête VERSION, qui rapporte la version du service et le système d'exploitation si cela est possible à identifier.

Jusqu'à présent, nous savons que le système d'exploitation est Ubuntu Linux. Les versions des applications peuvent également aider à révéler la version de l'OS cible. Prenez OpenSSH, par exemple. Nous voyons que la version rapportée est `OpenSSH 8.2p1 Ubuntu 4ubuntu0.1`. En inspectant d'autres journaux de modifications (changelogs) de paquets SSH Ubuntu ([changelogs](https://launchpad.net/ubuntu/yakkety/+source/openssh/+changelog)), nous voyons que la version de la publication prend le format `1:7.3p1-1ubuntu0.1`. En adaptant notre version à ce format, nous obtenons `1:8.2p1-4ubuntu0.1`. Une recherche rapide de cette version en ligne révèle qu'elle est incluse dans Ubuntu Linux Focal Fossa 20.04.

![Résultats de recherche Google pour '1:8.2p1-4ubuntu0.1 release' montrant des liens vers le paquet OpenSSH sur Launchpad.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/google1.png)

Une autre recherche rapide révèle que la date de sortie de cet OS est le 23 avril 2020.

![Résultats de recherche Google pour 'Ubuntu focal 20.04 release date' montrant le 23 avril 2020 comme date de sortie.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/google2.png)

Cependant, il convient de noter que cette technique de recoupement n'est pas entièrement fiable, car il est possible d'installer des paquets d'applications plus récents sur une version d'OS plus ancienne. L'option d'analyse de script `-sC` fait que `Nmap` rapporte les en-têtes de serveur (server headers) `http-server-header` et le titre de la page (page title) `http-title` pour toute page web hébergée sur le serveur web. Le titre de la page web `PHP 7.4.3 - phpinfo()` indique qu'il s'agit d'un fichier PHPInfo, qui est souvent créé manuellement pour confirmer que PHP a été installé avec succès. Le titre (et la page PHPInfo) révèle également la version de PHP, ce qui est à noter si elle est vulnérable.

http://10.129.42.253/index.php

![Tableau d'informations de la version 7.4.3 de PHP montrant les détails du système, la date de compilation, l'API du serveur et les chemins de configuration.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/phpinfo.png)

#### Scripts Nmap

Spécifier `-sC` exécutera de nombreux scripts par défaut utiles contre une cible, mais il y a des cas où l'exécution d'un script spécifique est requise. Par exemple, dans le périmètre d'une évaluation (assessment scope), on peut nous demander d'auditer une grande installation Citrix. Nous pourrions utiliser [ce](https://raw.githubusercontent.com/cyberstruggle/DeltaGroup/master/CVE-2019-19781/CVE-2019-19781.nse) script `Nmap` pour auditer la vulnérabilité sévère de Citrix NetScaler ([CVE-2019–19781](https://blog.rapid7.com/2020/01/17/active-exploitation-of-citrix-netscaler-cve-2019-19781-what-you-need-to-know/)), tandis que `Nmap` dispose également d'autres scripts pour auditer une installation Citrix.

```bash
Hiterof13@htb[/htb]$ locate scripts/citrix  /usr/share/nmap/scripts/citrix-brute-xml.nse /usr/share/nmap/scripts/citrix-enum-apps-xml.nse /usr/share/nmap/scripts/citrix-enum-apps.nse /usr/share/nmap/scripts/citrix-enum-servers-xml.nse /usr/share/nmap/scripts/citrix-enum-servers.nse
```

La syntaxe pour exécuter un script Nmap est `nmap --script <nom du script> -p<port> <hôte>`.

Les scripts `Nmap` sont un excellent moyen d'améliorer la fonctionnalité de nos analyses, et l'inspection des options disponibles sera payante. Consultez le module [Énumération de réseau avec Nmap](https://academy.hackthebox.com/module/details/19) pour une étude plus détaillée de l'outil `Nmap`.

---

## Attaquer les services réseau

#### Capture de bannière (Banner Grabbing)

Comme discuté précédemment, la capture de bannière (Banner grabbing) est une technique utile pour prendre rapidement l'empreinte d'un service. Souvent, un service cherchera à s'identifier en affichant une bannière une fois la connexion initiée. Nmap tentera de capturer les bannières si la syntaxe `nmap -sV --script=banner <target>` est spécifiée. Nous pouvons également tenter cela manuellement en utilisant `Netcat`. Prenons un autre exemple, en utilisant la version `nc` de `Netcat` :

```bash
Hiterof13@htb[/htb]$ nc -nv 10.129.42.253 21  (UNKNOWN) [10.129.42.253] 21 (ftp) open 220 (vsFTPd 3.0.3)
```

Cela révèle que la version de `vsFTPd` sur le serveur est `3.0.3`. Nous pouvons également automatiser ce processus en utilisant le puissant moteur de script de `Nmap` : `nmap -sV --script=banner -p21 10.10.10.0/24`.

#### FTP

Il est utile de se familiariser avec FTP, car c'est un protocole standard, et ce service peut souvent contenir des données intéressantes. Une analyse `Nmap` du port par défaut pour FTP (21) révèle l'installation de vsftpd 3.0.3 que nous avons identifiée précédemment. De plus, elle rapporte également que l'authentification anonyme est activée et qu'un répertoire `pub` est disponible.

```bash
Hiterof13@htb[/htb]$ nmap -sC -sV -p21 10.129.42.253
Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-20 00:54 GMT
Nmap scan report for 10.129.42.253
Host is up (0.081s latency).
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    2 ftp      ftp          4096 Dec 19 23:50 pub
| ftp-syst:  |   STAT:
| FTP server status: |      Connected to ::ffff:10.10.14.2 |      Logged in as ftp |      TYPE: ASCII |      No session bandwidth limit |      Session timeout in seconds is 300 |      Control connection is plain text |      Data connections will be plain text |      At session startup, client count was 3 |      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
Service Info: OS: Unix
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.78 seconds
```

Connectons-nous au service en utilisant l'utilitaire en ligne de commande `ftp`.

```bash
Hiterof13@htb[/htb]$ ftp -p 10.129.42.253  Connected to 10.129.42.253. 220 (vsFTPd 3.0.3) Name (10.129.42.253:user): anonymous 230 Login successful. Remote system type is UNIX. Using binary mode to transfer files.

ftp> ls 227 Entering Passive Mode (10,129,42,253,158,60). 150 Here comes the directory listing. drwxr-xr-x    2 ftp      ftp          4096 Feb 25 19:25 pub 226 Directory send OK.

ftp> cd pub 250 Directory successfully changed.

ftp> ls 227 Entering Passive Mode (10,129,42,253,182,129). 150 Here comes the directory listing. -rw-r--r--    1 ftp      ftp            18 Feb 25 19:25 login.txt 226 Directory send OK.

ftp> get login.txt local: login.txt remote: login.txt 227 Entering Passive Mode (10,129,42,253,181,53). 150 Opening BINARY mode data connection for login.txt (18 bytes). 226 Transfer complete. 18 bytes received in 0.00 secs (165.8314 kB/s)

ftp> exit 221 Goodbye.
```

Dans le shell ci-dessus, nous voyons que FTP prend en charge des commandes courantes telles que `cd` et `ls` et nous permet de télécharger des fichiers en utilisant la commande `get`. L'inspection du fichier `login.txt` téléchargé révèle des identifiants que nous pourrions utiliser pour approfondir notre accès au système.

```bash
Hiterof13@htb[/htb]$ cat login.txt   admin:ftp@dmin123
```

---

#### SMB

SMB (Server Message Block) est un protocole très répandu sur les machines Windows qui offre de nombreux vecteurs pour le mouvement vertical et latéral. Des données sensibles, y compris des identifiants, peuvent se trouver dans des partages de fichiers réseau, et certaines versions de SMB peuvent être vulnérables à des exploits RCE (Remote Code Execution) tels que [EternalBlue](https://www.avast.com/c-eternalblue). Il est crucial d'énumérer soigneusement cette surface d'attaque potentielle considérable. `Nmap` dispose de nombreux scripts pour l'énumération de SMB, tels que [smb-os-discovery.nse](https://nmap.org/nsedoc/scripts/smb-os-discovery.html), qui interagira avec le service SMB pour extraire la version du système d'exploitation rapportée.

```bash
Hiterof13@htb[/htb]$ nmap --script smb-os-discovery.nse -p445 10.10.10.40
Starting Nmap 7.91 ( https://nmap.org ) at 2020-12-27 00:59 GMT
Nmap scan report for doctors.htb (10.10.10.40)
Host is up (0.022s latency).
PORT    STATE SERVICE
445/tcp open  microsoft-ds
Host script results:
| smb-os-discovery:  |   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1) |   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional |   Computer name: CEO-PC |   NetBIOS computer name: CEO-PC\x00 |   Workgroup: WORKGROUP\x00
|_  System time: 2020-12-27T00:59:46+00:00
Nmap done: 1 IP address (1 host up) scanned in 2.71 seconds
```

Dans ce cas, l'hôte exécute un OS Windows 7 hérité, et nous pourrions effectuer une énumération plus poussée pour confirmer s'il est vulnérable à EternalBlue. Le Metasploit Framework dispose de plusieurs [modules](https://www.rapid7.com/db/modules/exploit/windows/smb/ms17_010_eternalblue/) pour EternalBlue qui peuvent être utilisés pour valider la vulnérabilité et l'exploiter, comme nous le verrons dans une prochaine section. Nous pouvons lancer une analyse contre notre cible pour cette section du module afin de recueillir des informations du service SMB. Nous pouvons déterminer que l'hôte exécute un noyau Linux, la version 4.6.2 de Samba, et que le nom d'hôte est GS-SVCSCAN.

```bash
Hiterof13@htb[/htb]$ nmap -A -p445 10.129.42.253
Starting Nmap 7.80 ( https://nmap.org ) at 2021-02-25 16:29 EST
Nmap scan report for 10.129.42.253
Host is up (0.11s latency).
PORT    STATE SERVICE     VERSION
445/tcp open  netbios-ssn Samba smbd 4.6.2
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 2.6.32 (95%), Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Adtran 424RG FTTH gateway (92%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%), Linux 3.2 - 4.9 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Host script results:
|_nbstat: NetBIOS name: GS-SVCSCAN, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb2-security-mode:  |   2.02:
|_    Message signing enabled but not required
| smb2-time:  |   date: 2021-02-25T21:30:06
|_  start_date: N/A
TRACEROUTE (using port 445/tcp) HOP RTT       ADDRESS 1   111.62 ms 10.10.14.1 2   111.89 ms 10.129.42.253  OS and
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.72 seconds
```

---

#### Partages

SMB permet aux utilisateurs et aux administrateurs de partager des dossiers et de les rendre accessibles à distance par d'autres utilisateurs. Souvent, ces partages contiennent des fichiers avec des informations sensibles telles que des mots de passe. Un outil qui peut énumérer et interagir avec les partages SMB est [smbclient](https://www.samba.org/samba/docs/current/man-html/smbclient.1.html). L'option `-L` spécifie que nous voulons récupérer une liste des partages disponibles sur l'hôte distant, tandis que `-N` supprime la demande de mot de passe.

```bash
Hiterof13@htb[/htb]$ smbclient -N -L \\\\10.129.42.253      Sharename       Type      Comment     ---------       ----      -------     print$          Disk      Printer Drivers     users           Disk           IPC$            IPC       IPC Service (gs-svcscan server (Samba, Ubuntu)) SMB1 disabled -- no workgroup available
```

Cela révèle le partage non standard `users`. Essayons de nous connecter en tant qu'utilisateur invité (guest user).

```bash
Hiterof13@htb[/htb]$ smbclient \\\\10.129.42.253\\users  Enter WORKGROUP\users's password:  Try "help" to get a list of possible commands.

smb: \> ls NT_STATUS_ACCESS_DENIED listing \*

smb: \> exit
```

La commande `ls` a entraîné un message d'accès refusé, indiquant que l'accès invité n'est pas autorisé. Réessayons en utilisant les identifiants de l'utilisateur bob (`bob:Welcome1`).

```bash
Hiterof13@htb[/htb]$ smbclient -U bob \\\\10.129.42.253\\users  Enter WORKGROUP\bob's password:  Try "help" to get a list of possible commands.

smb: \> ls   .                                   D        0  Thu Feb 25 16:42:23 2021   ..                                  D        0  Thu Feb 25 15:05:31 2021   bob                                 D        0  Thu Feb 25 16:42:23 2021          4062912 blocks of size 1024. 1332480 blocks available

smb: \> cd bob

smb: \bob\> ls   .                                   D        0  Thu Feb 25 16:42:23 2021   ..                                  D        0  Thu Feb 25 16:42:23 2021   passwords.txt                       N      156  Thu Feb 25 16:42:23 2021          4062912 blocks of size 1024. 1332480 blocks available

smb: \bob\> get passwords.txt  getting file \bob\passwords.txt of size 156 as passwords.txt (0.3 KiloBytes/sec) (average 0.3 KiloBytes/sec)
```

Nous avons réussi à accéder au partage `users` en utilisant des identifiants et avons obtenu l'accès au fichier intéressant `passwords.txt`, qui peut être téléchargé avec la commande `get`.

---

#### SNMP

Les chaînes de communauté SNMP (SNMP Community strings) fournissent des informations et des statistiques sur un routeur ou un appareil, nous aidant à y accéder. Les chaînes de communauté par défaut du fabricant, `public` et `private`, sont souvent inchangées. Dans les versions 1 et 2c de SNMP, l'accès est contrôlé à l'aide d'une chaîne de communauté en clair (plaintext), et si nous connaissons le nom, nous pouvons y accéder. Le chiffrement et l'authentification n'ont été ajoutés qu'à partir de la version 3 de SNMP. De nombreuses informations peuvent être obtenues à partir de SNMP. L'examen des paramètres de processus peut révéler des identifiants passés en ligne de commande, qu'il pourrait être possible de réutiliser pour d'autres services accessibles de l'extérieur, étant donné la prévalence de la réutilisation des mots de passe dans les environnements d'entreprise. Des informations de routage, des services liés à des interfaces supplémentaires et la version des logiciels installés peuvent également être révélés.

```bash
Hiterof13@htb[/htb]$ snmpwalk -v 2c -c public 10.129.42.253 1.3.6.1.2.1.1.5.0  iso.3.6.1.2.1.1.5.0 = STRING: "gs-svcscan"
```

```bash
Hiterof13@htb[/htb]$ snmpwalk -v 2c -c private  10.129.42.253   Timeout: No Response from 10.129.42.253
```

Un outil tel que [onesixtyone](https://github.com/trailofbits/onesixtyone) peut être utilisé pour forcer par la force brute (brute force) les noms des chaînes de communauté en utilisant un fichier de dictionnaire (dictionary file) de chaînes de communauté courantes, comme le fichier `dict.txt` inclus dans le dépôt GitHub de l'outil.

```bash
Hiterof13@htb[/htb]$ onesixtyone -c dict.txt 10.129.42.254  Scanning 1 hosts, 51 communities 10.129.42.254 [public] Linux gs-svcscan 5.4.0-66-generic #74-Ubuntu SMP Wed Jan 27 22:54:38 UTC 2021 x86_64
```

---

## Conclusion

L'analyse et l'énumération de services est un vaste sujet que nous approfondirons au fur et à mesure. Les aspects que nous avons abordés ici s'appliquent à de nombreux réseaux, y compris les machines HTB.
---

← [[06 - Outils de base]] | [[00 - Sommaire Getting Started|Sommaire]] | [[08 - Énumération Web]] →
