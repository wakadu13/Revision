---
tags:
  - getting-started
ordre: 5
---

# Termes Courants

---

Le test d'intrusion (penetration testing)/hacking est un domaine immense. Nous rencontrerons d'innombrables technologies tout au long de nos carrières. Voici quelques-uns des termes et technologies les plus courants que nous rencontrerons à plusieurs reprises et que nous devons maîtriser. Cette liste n'est pas exhaustive, mais elle est suffisante pour commencer avec les Modules fondamentaux et les box HTB faciles.

---

## Qu'est-ce qu'un Shell ?

`Shell` est un terme très courant que nous entendrons sans cesse au cours de notre parcours. Il a plusieurs significations. Sur un système Linux, le shell est un programme qui prend les entrées de l'utilisateur via le clavier et transmet ces commandes au système d'exploitation pour qu'il exécute une fonction spécifique. Aux débuts de l'informatique, le shell était la seule interface disponible pour interagir avec les systèmes. Depuis lors, de nombreux autres types et versions de systèmes d'exploitation ont vu le jour, ainsi que l'interface utilisateur graphique (GUI) pour compléter les interfaces en ligne de commande (shell), telles que le terminal Linux, la ligne de commande Windows (cmd.exe) et Windows PowerShell.

La plupart des systèmes Linux utilisent un programme appelé [Bash (Bourne Again Shell)](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html) comme programme de shell pour interagir avec le système d'exploitation. Bash est une version améliorée de [sh](https://man7.org/linux/man-pages/man1/sh.1p.html), le programme de shell original des systèmes Unix. Outre `bash`, il existe également d'autres shells, y compris, mais sans s'y limiter, [Zsh](https://en.wikipedia.org/wiki/Z_shell), [Tcsh](https://en.wikipedia.org/wiki/Tcsh), [Ksh](https://en.wikipedia.org/wiki/KornShell), [Fish shell](https://en.wikipedia.org/wiki/Fish_\(Unix_shell\)), etc.

Nous lirons ou entendrons souvent parler d'« obtenir un shell » sur une machine (box/système). Cela signifie que l'hôte cible a été exploité, que nous avons obtenu un accès de niveau shell (généralement `bash` ou `sh`) et que nous pouvons exécuter des commandes de manière interactive comme si nous étions connectés à l'hôte. Un shell peut être obtenu en exploitant une vulnérabilité d'application web ou de réseau/service, ou en obtenant des identifiants et en se connectant à distance à l'hôte cible. Il existe trois principaux types de connexions shell :

|**Type de Shell**|**Description**|
|---|---|
|`Reverse shell`|Initie une connexion en retour vers un « écouteur » (listener) sur notre machine d'attaque.|
|`Bind shell`|Se « lie » (binds) à un port spécifique sur l'hôte cible et attend une connexion depuis notre machine d'attaque.|
|`Web shell`|Exécute des commandes du système d'exploitation via le navigateur web, généralement de manière non interactive ou semi-interactive. Il peut également être utilisé pour exécuter des commandes uniques (par exemple, en exploitant une vulnérabilité de téléversement de fichier et en téléversant un script `PHP` pour exécuter une seule commande).|

Chaque type de shell a son cas d'utilisation, et de la même manière qu'il existe de nombreuses façons d'obtenir un shell, le programme auxiliaire que nous utilisons pour obtenir un shell peut être écrit dans de nombreux langages (`Python`, `Perl`, `Go`, `Bash`, `Java`, `awk`, `PHP`, etc.). Il peut s'agir de petits scripts ou de programmes plus grands et plus complexes pour faciliter une connexion depuis l'hôte cible vers notre système d'attaque et obtenir un accès « shell ». L'accès shell sera abordé en détail dans une section ultérieure.

---

## Qu'est-ce qu'un Port ?

Un [port](https://en.wikipedia.org/wiki/Port_\(computer_networking\)) peut être considéré comme une fenêtre ou une porte d'une maison (la maison étant un système distant) ; si une fenêtre ou une porte est laissée ouverte ou n'est pas correctement verrouillée, nous pouvons souvent obtenir un accès non autorisé à la maison. C'est similaire en informatique. Les ports sont des points virtuels où les connexions réseau commencent et se terminent. Ils sont basés sur des logiciels et gérés par le système d'exploitation de l'hôte. Les ports sont associés à un processus ou un service spécifique et permettent aux ordinateurs de différencier les différents types de trafic (le trafic SSH est dirigé vers un port différent de celui des requêtes web pour accéder à un site web, même si les requêtes d'accès sont envoyées sur la même connexion réseau).

Chaque port se voit attribuer un numéro, et beaucoup sont standardisés sur tous les appareils connectés au réseau (bien qu'un service puisse être configured pour s'exécuter sur un port non standard). Par exemple, les messages `HTTP` (trafic de site web) sont généralement dirigés vers le port `80`, tandis que les messages `HTTPS` vont vers le port `443`, sauf configuration contraire. Nous rencontrerons des applications web fonctionnant sur des ports non standard, mais nous les trouverons généralement sur les ports 80 et 443. Les numéros de port nous permettent d'accéder à des services ou applications spécifiques s'exécutant sur les appareils cibles. À un niveau très général, les ports aident les ordinateurs à comprendre comment traiter les différents types de données qu'ils reçoivent.

Il existe deux catégories de ports, le [Protocole de Contrôle de Transmission (TCP)](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) et le [Protocole de Datagramme Utilisateur (UDP)](https://en.wikipedia.org/wiki/User_Datagram_Protocol). `TCP` est orienté connexion (connection-oriented), ce qui signifie qu'une connexion entre un client et un serveur doit être établie avant que des données puissent être envoyées. Le serveur doit être en état d'écoute, attendant les demandes de connexion des clients. `UDP` utilise un modèle de communication sans connexion (connectionless). Il n'y a pas de « poignée de main » (handshake) et cela introduit donc une certaine part de non-fiabilité, car il n'y a aucune garantie de livraison des données. `UDP` est utile lorsque la correction/vérification d'erreurs n'est pas nécessaire ou est gérée par l'application elle-même. `UDP` convient aux applications qui exécutent des tâches sensibles au temps, car la perte de paquets est plus rapide que l'attente de paquets retardés en raison de la retransmission, comme c'est le cas avec `TCP`, ce qui peut affecter de manière significative un système en temps réel. Il y a `65 535` ports `TCP` et `65 535` ports `UDP` différents, chacun désigné par un numéro. Certains des ports `TCP` et `UDP` les plus connus sont listés ci-dessous :

|Port(s)|Protocole|
|---|---|
|`20`/`21` (TCP)|`FTP`|
|`22` (TCP)|`SSH`|
|`23` (TCP)|`Telnet`|
|`25` (TCP)|`SMTP`|
|`80` (TCP)|`HTTP`|
|`161` (TCP/UDP)|`SNMP`|
|`389` (TCP/UDP)|`LDAP`|
|`443` (TCP)|`SSL`/`TLS` (`HTTPS`)|
|`445` (TCP)|`SMB`|
|`3389` (TCP)|`RDP`|

En tant que professionnels de la sécurité de l'information, nous devons être capables de nous rappeler rapidement de grandes quantités d'informations sur une grande variété de sujets. Il est essentiel pour nous, en particulier en tant que testeurs d'intrusion (pentesters), de bien maîtriser de nombreux ports `TCP` et `UDP` et d'être capables de les reconnaître rapidement à partir de leur simple numéro (c'est-à-dire savoir que le port `21` est `FTP`, le port `80` est `HTTP`, le port `88` est `Kerberos`) sans avoir à le rechercher. Cela viendra avec la pratique et la répétition et deviendra finalement une seconde nature à mesure que nous attaquerons plus de machines, de laboratoires et de réseaux du monde réel, ce qui nous aidera à travailler plus efficacement et à mieux prioriser nos efforts d'énumération et nos attaques.

Des guides tels que [celui-ci](https://www.stationx.net/common-ports-cheat-sheet/) et [celui-là](https://web.archive.org/web/20240315102711/https://packetlife.net/media/library/23/common-ports.pdf) sont d'excellentes ressources pour apprendre les ports TCP et UDP standard et moins courants. Mettez-vous au défi d'en mémoriser le plus grand nombre possible et faites des recherches sur chacun des protocoles listés dans le tableau ci-dessus. Voici une excellente [référence](https://nullsec.us/top-1-000-tcp-and-udp-ports-nmap-default/) sur les 1 000 principaux ports `TCP` et `UDP` de `nmap` ainsi que les 100 principaux services scannés par `nmap`.

---

## Qu'est-ce qu'un Serveur Web

Un serveur web est une application qui s'exécute sur le serveur back-end, qui gère tout le trafic `HTTP` provenant du navigateur côté client, l'achemine vers les pages de destination des requêtes et répond finalement au navigateur côté client. Les serveurs web fonctionnent généralement sur les ports TCP `80` ou `443` et sont responsables de la connexion des utilisateurs finaux à diverses parties de l'application web, en plus de gérer leurs diverses réponses :

https://www.hackthebox.eu/home/

![Tableau de bord montrant 914 joueurs en ligne, 1020 machines compromises, 618 challenges réussis, et l'activité récente avec les cibles Active, Lame, et Beep.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_main_2.jpg)

Comme les applications web ont tendance à être ouvertes à l'interaction publique et tournées vers Internet, elles peuvent conduire à la compromission du serveur back-end si elles souffrent de vulnérabilités. Les applications web peuvent présenter une vaste surface d'attaque, ce qui en fait une cible de grande valeur pour les attaquants et les pentesters.

De nombreux types de vulnérabilités peuvent affecter les applications web. Nous entendrons souvent parler ou verrons des références au [Top 10 de l'OWASP](https://owasp.org/www-project-top-ten/). Il s'agit d'une liste standardisée des 10 principales vulnérabilités des applications web, maintenue par l'Open Web Application Security Project (OWASP). Cette liste est considérée comme les 10 vulnérabilités les plus dangereuses et n'est pas une liste exhaustive de toutes les vulnérabilités possibles des applications web. Les méthodologies d'évaluation de la sécurité des applications web sont souvent basées sur le top 10 de l'OWASP comme point de départ pour les principales catégories de failles qu'un évaluateur devrait vérifier. Au moment de la rédaction de ce document, la liste du Top 10 de l'OWASP (2021) se compose de :

|Numéro|Catégorie|Description|
|---|---|---|
|1.|[Rupture de Contrôle d'Accès (Broken Access Control)](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)|Les restrictions ne sont pas correctement mises en œuvre pour empêcher les utilisateurs d'accéder aux comptes d'autres utilisateurs, de voir des données sensibles, d'accéder à des fonctionnalités non autorisées, de modifier des données, etc.|
|2.|[Défaillances Cryptographiques (Cryptographic Failures)](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)|Défaillances liées à la cryptographie qui conduisent souvent à l'exposition de données sensibles ou à la compromission du système.|
|3.|[Injection](https://owasp.org/Top10/A03_2021-Injection/)|Les données fournies par l'utilisateur ne sont pas validées, filtrées ou nettoyées par l'application. Quelques exemples d'injections sont l'injection SQL, l'injection de commande, l'injection LDAP, etc.|
|4.|[Conception non Sécurisée (Insecure Design)](https://owasp.org/Top10/A04_2021-Insecure_Design/)|Ces problèmes surviennent lorsque l'application n'est pas conçue en tenant compte de la sécurité.|
|5.|[Mauvaise Configuration de Sécurité (Security Misconfiguration)](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)|Manque de renforcement de la sécurité approprié sur n'importe quelle partie de la pile applicative, configurations par défaut non sécurisées, stockage cloud ouvert, messages d'erreur verbeux qui divulguent trop d'informations.|
|6.|[Composants Vulnérables et Obsolètes (Vulnerable and Outdated Components)](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)|Utilisation de composants (côté client et côté serveur) qui sont vulnérables, non pris en charge ou obsolètes.|
|7.|[Défaillances d'Identification et d'Authentification (Identification and Authentication Failures)](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)|Attaques liées à l'authentification qui ciblent l'identité de l'utilisateur, l'authentification et la gestion de session.|
|8.|[Défaillances d'Intégrité des Logiciels et des Données (Software and Data Integrity Failures)](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)|Les défaillances d'intégrité des logiciels et des données concernent le code et l'infrastructure qui ne protègent pas contre les violations d'intégrité. Un exemple de cela est lorsqu'une application s'appuie sur des plugins, des bibliothèques ou des modules provenant de sources, de dépôts et de réseaux de diffusion de contenu (CDN) non fiables.|
|9.|[Défaillances de Journalisation et de Surveillance de la Sécurité (Security Logging and Monitoring Failures)](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)|Cette catégorie vise à aider à détecter, à remonter et à répondre aux violations actives. Sans journalisation et surveillance, les violations ne peuvent pas être détectées.|
|10.|[Falsification de Requête Côté Serveur (Server-Side Request Forgery - SSRF)](https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/)|Les failles SSRF se produisent chaque fois qu'une application web récupère une ressource distante sans valider l'URL fournie par l'utilisateur. Cela permet à un attaquant de forcer l'application à envoyer une requête forgée vers une destination inattendue, même si elle est protégée par un pare-feu, un VPN ou un autre type de liste de contrôle d'accès réseau (ACL).|

Il est essentiel de se familiariser avec chacune de ces catégories et les diverses vulnérabilités qui correspondent à chacune. Les vulnérabilités des applications web seront traitées en profondeur dans des modules ultérieurs. Pour en savoir plus sur les applications web, consultez le module [Introduction aux Applications Web](https://academy.hackthebox.com/module/details/75).
---

← [[04 - Se Connecter avec un VPN]] | [[00 - Sommaire Getting Started|Sommaire]] | [[06 - Outils de base]] →
