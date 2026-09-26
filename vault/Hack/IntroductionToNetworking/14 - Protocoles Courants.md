---
tags:
  - networking
ordre: 14
---

# Protocoles Courants

---

Les protocoles Internet sont des règles et des directives normalisées, définies dans des RFC (Request for Comments), qui spécifient la manière dont les périphériques d'un réseau doivent communiquer entre eux. Ils garantissent que les périphériques d'un réseau peuvent échanger des informations de manière cohérente et fiable, quels que soient le matériel et les logiciels utilisés. Pour que des périphériques puissent communiquer sur un réseau, ils doivent être connectés par un canal de communication, tel qu'une connexion filaire ou sans fil. Les périphériques échangent ensuite des informations à l'aide d'un ensemble de protocoles normalisés qui définissent le format et la structure des données transmises. Les deux principaux types de connexions utilisés sur les réseaux sont le [Protocole de Contrôle de Transmission](https://fr.wikipedia.org/wiki/Transmission_Control_Protocol) (`TCP`) et le [Protocole de Datagramme Utilisateur](https://fr.wikipedia.org/wiki/User_Datagram_Protocol) (`UDP`).

Nous devons connaître et savoir gérer les différents protocoles les plus utilisés. Comme nous l'avons déjà appris, ces protocoles sont à la base de toute communication entre nos appareils et ordinateurs sur les réseaux. Nous avons compilé ci-dessous un grand nombre de ces protocoles, que nous aborderons tout au long des modules. Mieux nous les comprendrons, plus nous pourrons travailler efficacement avec eux.

---

## Protocole de Contrôle de Transmission

`TCP` est un protocole `orienté connexion` qui établit une connexion virtuelle entre deux périphériques avant de transmettre des données en utilisant un [établissement de connexion en trois temps (Three-Way-Handshake)](https://fr.wikipedia.org/wiki/Transmission_Control_Protocol#%C3%89tablissement_d'une_connexion). Cette connexion est maintenue jusqu'à ce que le transfert de données soit terminé, et les périphériques peuvent continuer à échanger des données tant que la connexion est active.

Par exemple, lorsque nous saisissons une URL dans notre navigateur web, celui-ci envoie une requête HTTP au serveur hébergeant le site web en utilisant `TCP`. Le serveur répond en renvoyant le code HTML du site web au navigateur, toujours via `TCP`. Le navigateur utilise ensuite ce code pour afficher le site web sur notre écran. Ce processus repose sur l'établissement d'une connexion `TCP` entre le navigateur et le serveur web, qui est maintenue jusqu'à la fin du transfert de données. Par conséquent, `TCP` est fiable mais plus lent que l'UDP, car il nécessite une surcharge (overhead) supplémentaire pour établir et maintenir la connexion.

|**Protocole**|**Acronyme**|**Port**|**Description**|
|---|---|---|---|
|Telnet|`Telnet`|`23`|Service de connexion à distance|
|Secure Shell|`SSH`|`22`|Service de connexion sécurisée à distance|
|Protocole Simple de Gestion de Réseau|`SNMP`|`161-162`|Gérer les périphériques réseau|
|Protocole de Transfert Hypertexte|`HTTP`|`80`|Utilisé pour transférer des pages web|
|Protocole de Transfert Hypertexte Sécurisé|`HTTPS`|`443`|Utilisé pour transférer des pages web sécurisées|
|Système de Noms de Domaine|`DNS`|`53`|Résoudre les noms de domaine|
|Protocole de Transfert de Fichiers|`FTP`|`20-21`|Utilisé pour transférer des fichiers|
|Protocole Trivial de Transfert de Fichiers|`TFTP`|`69`|Utilisé pour transférer des fichiers|
|Protocole d'Heure Réseau|`NTP`|`123`|Synchroniser les horloges des ordinateurs|
|Protocole Simple de Transfert de Courrier|`SMTP`|`25`|Utilisé pour le transfert d'e-mails|
|Protocole Bureau de Poste|`POP3`|`110`|Utilisé pour récupérer les e-mails|
|Protocole d'Accès aux Messages Internet|`IMAP`|`143`|Utilisé pour accéder aux e-mails|
|Bloc de Message Serveur|`SMB`|`445`|Utilisé pour transférer des fichiers|
|Système de Fichiers en Réseau|`NFS`|`111`, `2049`|Utilisé pour monter des systèmes distants|
|Protocole d'Amorçage|`BOOTP`|`67`, `68`|Utilisé pour démarrer les ordinateurs|
|Kerberos|`Kerberos`|`88`|Utilisé pour l'authentification et l'autorisation|
|Protocole d'Accès aux Annuaires Léger|`LDAP`|`389`|Utilisé pour les services d'annuaire|
|Service d'Authentification à Accès Distant|`RADIUS`|`1812`, `1813`|Utilisé pour l'authentification et l'autorisation|
|Protocole de Configuration Dynamique des Hôtes|`DHCP`|`67`, `68`|Utilisé pour configurer les adresses IP|
|Protocole de Bureau à Distance|`RDP`|`3389`|Utilisé pour l'accès au bureau à distance|
|Protocole de Transfert de Nouvelles sur le Réseau|`NNTP`|`119`|Utilisé pour accéder aux groupes de discussion|
|Appel de Procédure à Distance|`RPC`|`135`, `137-139`|Utilisé pour appeler des procédures à distance|
|Protocole d'Identification|`Ident`|`113`|Utilisé pour identifier les processus utilisateur|
|Protocole de Messages de Contrôle Internet|`ICMP`|`0-255`|Utilisé pour diagnostiquer les problèmes réseau|
|Protocole de Gestion de Groupes Internet|`IGMP`|`0-255`|Utilisé pour la multidiffusion (multicasting)|
|Écouteur Oracle DB (par défaut/alternatif)|`oracle-tns`|`1521`/`1526`|L'écouteur par défaut/alternatif de la base de données Oracle est un service qui s'exécute sur l'hôte de la base de données et reçoit les requêtes des clients Oracle.|
|Verrou Ingres|`ingreslock`|`1524`|La base de données Ingres est couramment utilisée pour de grandes applications commerciales et comme porte dérobée (backdoor) pouvant exécuter des commandes à distance via RPC.|
|Proxy Web Squid|`http-proxy`|`3128`|Le proxy web Squid est un proxy web HTTP de mise en cache et de redirection utilisé pour accélérer un serveur web en mettant en cache les requêtes répétées.|
|Protocole de Copie Sécurisée|`SCP`|`22`|Copier des fichiers de manière sécurisée entre systèmes|
|Protocole d'Initiation de Session|`SIP`|`5060`|Utilisé pour les sessions VoIP|
|Protocole d'Accès aux Objets Simple|`SOAP`|`80`, `443`|Utilisé pour les services web|
|Couche de Sockets Sécurisée|`SSL`|`443`|Transférer des fichiers de manière sécurisée|
|TCP Wrappers|`TCPW`|`113`|Utilisé pour le contrôle d'accès|
|Protocole de Gestion de Clés et d'Association de Sécurité Internet|`ISAKMP`|`500`|Utilisé pour les connexions VPN|
|Microsoft SQL Server|`ms-sql-s`|`1433`|Utilisé pour les connexions client au Microsoft SQL Server.|
|Négociation de Clés Internet Kerberisée|`KINK`|`892`|Utilisé pour l'authentification et l'autorisation|
|Chemin le plus Court d'Abord|`OSPF`|`89`|Utilisé pour le routage|
|Protocole de Tunnelisation Point à Point|`PPTP`|`1723`|Est utilisé pour créer des VPN|
|Exécution à Distance|`REXEC`|`512`|Ce protocole est utilisé pour exécuter des commandes sur des ordinateurs distants et renvoyer le résultat des commandes à l'ordinateur local.|
|Connexion à Distance|`RLOGIN`|`513`|Ce protocole démarre une session shell interactive sur un ordinateur distant.|
|Système de Fenêtrage X|`X11`|`6000`|C'est un système logiciel et un protocole réseau qui fournit une interface utilisateur graphique (GUI) pour les ordinateurs en réseau.|
|Système de Gestion de Base de Données Relationnelle|`DB2`|`50000`|Un SGBDR est conçu pour stocker, récupérer et gérer des données dans un format structuré pour des applications d'entreprise telles que les systèmes financiers, les systèmes de gestion de la relation client (CRM).|

---

## Protocole de Datagramme Utilisateur

D'un autre côté, `UDP` est un protocole `sans connexion`, ce qui signifie qu'il n'établit pas de connexion virtuelle avant de transmettre des données. Au lieu de cela, il envoie les paquets de données à la destination sans vérifier s'ils ont été reçus.

Par exemple, lorsque nous diffusons (stream) ou regardons une vidéo sur une plateforme comme YouTube, les données vidéo sont transmises à notre appareil via `UDP`. La raison est que la vidéo peut tolérer une certaine perte de données, et que la vitesse de transmission est plus importante que la fiabilité. Si quelques paquets de données vidéo sont perdus en cours de route, cela n'aura pas d'impact significatif sur la qualité globale de la vidéo. Cela rend `UDP` plus rapide que TCP mais moins fiable, car il n'y a aucune garantie que les paquets atteindront leur destination.

|**Protocole**|**Acronyme**|**Port**|**Description**|
|---|---|---|---|
|Système de Noms de Domaine|`DNS`|`53`|C'est un protocole pour résoudre les noms de domaine en adresses IP.|
|Protocole Trivial de Transfert de Fichiers|`TFTP`|`69`|Il est utilisé pour transférer des fichiers entre systèmes.|
|Protocole d'Heure Réseau|`NTP`|`123`|Il synchronise les horloges des ordinateurs sur un réseau.|
|Protocole Simple de Gestion de Réseau|`SNMP`|`161`|Il surveille et gère les périphériques réseau à distance.|
|Protocole d'Information de Routage|`RIP`|`520`|Il est utilisé pour échanger des informations de routage entre les routeurs.|
|Échange de Clés Internet|`IKE`|`500`|Échange de Clés Internet|
|Protocole d'Amorçage|`BOOTP`|`68`|Il est utilisé pour démarrer des hôtes sur un réseau.|
|Protocole de Configuration Dynamique des Hôtes|`DHCP`|`67`|Il est utilisé pour attribuer dynamiquement des adresses IP aux périphériques d'un réseau.|
|Telnet|`TELNET`|`23`|C'est un protocole de communication d'accès à distance en mode texte.|
|MySQL|`MySQL`|`3306`|C'est un système de gestion de base de données open-source.|
|Serveur Terminal|`TS`|`3389`|C'est un protocole d'accès à distance utilisé par défaut pour les Services Terminal Server de Microsoft Windows.|
|Nom NetBIOS|`netbios-ns`|`137`|Il est utilisé dans les systèmes d'exploitation Windows pour résoudre les noms NetBIOS en adresses IP sur un réseau local (LAN).|
|Microsoft SQL Server|`ms-sql-m`|`1434`|Utilisé pour le service SQL Server Browser de Microsoft.|
|Universal Plug and Play|`UPnP`|`1900`|C'est un protocole permettant aux périphériques de se découvrir et de communiquer sur le réseau.|
|PostgreSQL|`PGSQL`|`5432`|C'est un système de gestion de base de données objet-relationnel.|
|Virtual Network Computing|`VNC`|`5900`|C'est un système de partage de bureau graphique.|
|Système de Fenêtrage X|`X11`|`6000-6063`|C'est un système logiciel et un protocole réseau qui fournit une interface graphique (GUI) sur les systèmes de type Unix.|
|Syslog|`SYSLOG`|`514`|C'est un protocole standard pour collecter et stocker les messages de journalisation sur un système informatique.|
|Internet Relay Chat|`IRC`|`194`|C'est un protocole de messagerie texte Internet en temps réel (chat) ou de communication synchrone.|
|OpenPGP|`OpenPGP`|`11371`|C'est un protocole pour chiffrer et signer les données et les communications.|
|Sécurité du Protocole Internet|`IPsec`|`500`|IPsec est également un protocole qui fournit une communication sécurisée et chiffrée. Il est couramment utilisé dans les VPN pour créer un tunnel sécurisé entre deux appareils.|
|Échange de Clés Internet|`IKE`|`11371`|C'est un protocole pour chiffrer et signer les données et les communications.|
|Protocole de Contrôle du Gestionnaire d'Affichage X|`XDMCP`|`177`|XDMCP est un protocole réseau qui permet à un utilisateur de se connecter à distance à un ordinateur exécutant X11.|

---

## ICMP

Le [Protocole de Messages de Contrôle Internet](https://fr.wikipedia.org/wiki/Internet_Control_Message_Protocol) (`ICMP`) est un protocole utilisé par les périphériques pour communiquer entre eux sur Internet à diverses fins, notamment pour le rapport d'erreurs (error reporting) et les informations d'état. Il envoie des requêtes et des messages entre les périphériques, qui peuvent être utilisés pour signaler des erreurs ou fournir des informations d'état.

#### Requêtes ICMP

Une requête est un message envoyé par un périphérique à un autre pour demander une information ou effectuer une action spécifique. Un exemple de requête dans ICMP est la `requête ping`, qui teste la connectivité entre deux périphériques. Lorsqu'un périphérique envoie une requête ping à un autre, le second périphérique répond avec un message de `réponse ping`.

#### Messages ICMP

Un message en ICMP peut être soit une requête, soit une réponse. En plus des requêtes et réponses ping, ICMP prend en charge d'autres types de messages, tels que les messages d'erreur, `destination inaccessible` et `délai dépassé`. Ces messages sont utilisés pour communiquer divers types d'informations et d'erreurs entre les périphériques du réseau.

Par exemple, si un périphérique essaie d'envoyer un paquet à un autre et que le paquet ne peut pas être livré, le périphérique peut utiliser ICMP pour renvoyer un message d'erreur à l'expéditeur. ICMP a deux versions différentes :

- `ICMPv4` : Pour IPv4 uniquement
- `ICMPv6` : Pour IPv6 uniquement

ICMPv4 est la version originale d'`ICMP`, développée pour être utilisée avec IPv4. Elle est encore largement utilisée et constitue la version la plus courante d'ICMP. D'autre part, ICMPv6 a été développé pour IPv6. Il inclut des fonctionnalités supplémentaires et est conçu pour remédier à certaines des limitations d'ICMPv4.

|**Type de Requête**|**Description**|
|---|---|
|`Requête d'écho`|Ce message teste si un périphérique est joignable sur le réseau. Lorsqu'un périphérique envoie une requête d'écho, il s'attend à recevoir un message de réponse d'écho. Par exemple, les outils `tracert` (Windows) ou `traceroute` (Linux) envoient toujours des requêtes d'écho ICMP.|
|`Requête d'horodatage`|Ce message détermine l'heure sur un périphérique distant.|
|`Requête de masque d'adresse`|Ce message est utilisé pour demander le masque de sous-réseau d'un périphérique.|

|**Type de Message**|**Description**|
|---|---|
|`Réponse d'écho`|Ce message est envoyé en réponse à un message de requête d'écho.|
|`Destination inaccessible`|Ce message est envoyé lorsqu'un périphérique ne peut pas livrer un paquet à sa destination.|
|`Redirection`|Un routeur envoie ce message pour informer un périphérique qu'il doit envoyer ses paquets à un autre routeur.|
|`Délai dépassé`|Ce message est envoyé lorsqu'un paquet a mis trop de temps pour atteindre sa destination.|
|`Problème de paramètre`|Ce message est envoyé lorsqu'il y a un problème avec l'en-tête d'un paquet.|
|`Extinction de la source`|Ce message est envoyé lorsqu'un périphérique reçoit des paquets trop rapidement et ne peut pas suivre. Il est utilisé pour ralentir le flux de paquets.|

Une autre partie cruciale d'ICMP pour nous est le champ [Durée de vie (Time-To-Live)](https://fr.wikipedia.org/wiki/Time_to_live) (`TTL`) dans l'en-tête du paquet ICMP, qui limite la durée de vie du paquet lorsqu'il voyage à travers le réseau. Il empêche les paquets de circuler indéfiniment sur le réseau en cas de boucles de routage (routing loops). Chaque fois qu'un paquet passe par un routeur, celui-ci décrémente la `valeur TTL de 1`. Lorsque la valeur TTL atteint `0`, le routeur rejette le paquet et envoie un message ICMP `Time Exceeded` (Délai dépassé) à l'expéditeur.

Nous pouvons également utiliser le `TTL` pour déterminer le nombre de sauts (hops) qu'un paquet a effectués et la distance approximative jusqu'à la destination. Par exemple, si un paquet a un `TTL` de 10 et qu'il faut 5 sauts pour atteindre sa destination, on peut en déduire que la destination est à environ 5 sauts de distance. Par exemple, si nous voyons un ping avec une valeur `TTL` de `122`, cela pourrait signifier que nous avons affaire à un système Windows (`TTL 128` par défaut) qui se trouve à 6 sauts de distance.

Cependant, il est également possible de deviner le système d'exploitation en se basant sur la valeur `TTL` par défaut utilisée par le périphérique. Chaque système d'exploitation a généralement une valeur `TTL` par défaut lors de l'envoi de paquets. Cette valeur est définie dans l'en-tête du paquet et est décrémentée de 1 chaque fois que le paquet passe par un routeur. Par conséquent, en examinant la valeur `TTL` par défaut d'un périphérique, il est possible de déduire quel système d'exploitation le périphérique utilise. Par exemple : Les systèmes Windows (`2000/XP/2003/Vista/10`) ont généralement une valeur `TTL` par défaut de 128, tandis que les systèmes macOS et Linux ont généralement une valeur `TTL` par défaut de 64 et Solaris une valeur `TTL` par défaut de 255. Cependant, il est important de noter que l'utilisateur peut modifier ces valeurs, elles ne doivent donc pas être considérées comme un moyen définitif de déterminer le système d'exploitation d'un périphérique.

---

## VoIP

La [Voix sur IP (Voice over Internet Protocol)](https://www.arcep.fr/la-regulation/grands-dossiers-thematiques-transverses/la-voix-sur-ip.html) (`VoIP`) est une méthode de transmission de communications vocales et multimédias. Par exemple, elle nous permet de passer des appels téléphoniques en utilisant une connexion Internet à haut débit au lieu d'une ligne téléphonique traditionnelle, comme avec Skype, Whatsapp, Google Hangouts, Slack, Zoom, et d'autres.

Les ports VoIP les plus courants sont `TCP/5060` et `TCP/5061`, qui sont utilisés pour le [Protocole d'Initiation de Session (Session Initiation Protocol)](https://fr.wikipedia.org/wiki/Session_Initiation_Protocol) (SIP). Cependant, le port `TCP/1720` peut également être utilisé par certains systèmes VoIP pour le [protocole H.323](https://fr.wikipedia.org/wiki/H.323), un ensemble de normes pour la communication multimédia sur les réseaux à commutation de paquets. Néanmoins, SIP est plus largement utilisé que H.323 dans les systèmes VoIP.

SIP est un protocole de signalisation pour initier, maintenir, modifier et terminer des sessions en temps réel impliquant de la vidéo, de la voix, de la messagerie et d'autres applications et services de communication entre deux ou plusieurs points d'extrémité sur Internet. Par conséquent, il utilise des requêtes et des méthodes entre les points d'extrémité. Les requêtes et méthodes SIP les plus courantes sont :

|**Méthode**|**Description**|
|---|---|
|`INVITE`|Initie une session ou invite un autre point d'extrémité à y participer.|
|`ACK`|Confirme la réception d'une requête INVITE.|
|`BYE`|Met fin à une session.|
|`CANCEL`|Annule une requête INVITE en attente.|
|`REGISTER`|Enregistre un agent utilisateur (user agent ou UA) SIP auprès d'un serveur SIP.|
|`OPTIONS`|Demande des informations sur les capacités d'un serveur ou d'un agent utilisateur SIP, comme les types de médias qu'il prend en charge.|

#### Divulgation d'Informations

Cependant, SIP nous permet d'énumérer les utilisateurs existants pour des attaques potentielles. Cela peut être fait à diverses fins, comme déterminer la disponibilité d'un utilisateur, trouver des informations sur les capacités ou les services de l'utilisateur, ou pour effectuer ultérieurement des attaques par force brute (brute-force attacks) sur les comptes utilisateurs.

L'un des moyens possibles pour énumérer les utilisateurs est la requête SIP `OPTIONS`. C'est une méthode utilisée pour demander des informations sur les capacités d'un serveur ou d'agents utilisateurs SIP, comme les types de médias qu'il prend en charge, les codecs qu'il peut décoder, et d'autres détails. La requête `OPTIONS` peut sonder un serveur ou un agent utilisateur SIP pour obtenir des informations ou pour tester sa connectivité et sa disponibilité.

Lors de notre analyse, il est possible de découvrir un fichier `SEPxxxx.cnf`, où `xxxx` est un identifiant unique. Il s'agit d'un fichier de configuration utilisé par Cisco Unified Communications Manager, anciennement connu sous le nom de Cisco CallManager, pour définir les paramètres d'un téléphone IP Cisco Unified. Le fichier spécifie le modèle de téléphone, la version du firmware, les paramètres réseau et d'autres détails.
---

← [[13 - Terminologie Clé des Réseaux]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[15 - Réseaux sans fil]] →
