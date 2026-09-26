---
tags:
  - brute-force
ordre: 9
---

# Medusa

---

Medusa, un outil de premier plan dans l'arsenal de la cybersécurité, est conçu pour être un outil de brute-force de connexion rapide, massivement parallèle et modulaire. Son objectif principal est de prendre en charge un large éventail de services qui permettent l'authentification à distance, permettant aux testeurs d'intrusion (penetration testers) et aux professionnels de la sécurité d'évaluer la résilience des systèmes de connexion contre les attaques par force brute.

## Installation

Medusa est souvent préinstallé sur les distributions populaires de tests d'intrusion. Vous pouvez vérifier sa présence en exécutant :

```bash
Hiterof13@htb[/htb]$ medusa -h
```

L'installation de Medusa sur un système Linux est simple.

```bash
Hiterof13@htb[/htb]$ sudo apt-get -y update

Hiterof13@htb[/htb]$ sudo apt-get -y install medusa
```

## Syntaxe des commandes et tableau des paramètres

L'interface en ligne de commande de Medusa est simple. Elle permet aux utilisateurs de spécifier des hôtes, des utilisateurs, des mots de passe et des modules avec diverses options pour affiner le processus d'attaque.

```bash
Hiterof13@htb[/htb]$ medusa [target_options] [credential_options] -M module [module_options]
```

|Paramètre|Explication|Exemple d'utilisation|
|---|---|---|
|`-h HOST` ou `-H FILE`|Options de cible : Spécifiez un nom d'hôte ou une adresse IP cible unique (`-h`) ou un fichier contenant une liste de cibles (`-H`).|`medusa -h 192.168.1.10 ...` ou `medusa -H targets.txt ...`|
|`-u USERNAME` ou `-U FILE`|Options de nom d'utilisateur : Fournissez un nom d'utilisateur unique (`-u`) ou un fichier contenant une liste de noms d'utilisateur (`-U`).|`medusa -u admin ...` ou `medusa -U usernames.txt ...`|
|`-p PASSWORD` ou `-P FILE`|Options de mot de passe : Spécifiez un mot de passe unique (`-p`) ou un fichier contenant une liste de mots de passe (`-P`).|`medusa -p password123 ...` ou `medusa -P passwords.txt ...`|
|`-M MODULE`|Module : Définissez le module spécifique à utiliser pour l'attaque (par ex., `ssh`, `ftp`, `http`).|`medusa -M ssh ...`|
|`-m "MODULE_OPTION"`|Options de module : Fournissez des paramètres supplémentaires requis par le module choisi, entre guillemets.|`medusa -M http -m "POST /login.php HTTP/1.1\r\nContent-Length: 30\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\nusername=^USER^&password=^PASS^" ...`|
|`-t TASKS`|Tâches : Définissez le nombre de tentatives de connexion parallèles à exécuter, ce qui peut accélérer l'attaque.|`medusa -t 4 ...`|
|`-f` ou `-F`|Mode rapide : Arrête l'attaque après la découverte de la première connexion réussie, soit sur l'hôte actuel (`-f`), soit sur n'importe quel hôte (`-F`).|`medusa -f ...` ou `medusa -F ...`|
|`-n PORT`|Port : Spécifiez un port non standard pour le service cible.|`medusa -n 2222 ...`|
|`-v LEVEL`|Sortie verbeuse : Affiche des informations détaillées sur la progression de l'attaque. Plus le `LEVEL` (niveau) est élevé (jusqu'à 6), plus la sortie est verbeuse.|`medusa -v 4 ...`|

### Modules Medusa

Chaque module de Medusa est conçu pour interagir avec des mécanismes d'authentification spécifiques, ce qui lui permet d'envoyer les requêtes appropriées et d'interpréter les réponses pour réussir les attaques. Vous trouverez ci-dessous un tableau des modules couramment utilisés :

|Module Medusa|Service/Protocole|Description|Exemple d'utilisation|
|---|---|---|---|
|FTP|Protocole de transfert de fichiers|Forçage brut des identifiants de connexion FTP, utilisés pour les transferts de fichiers sur un réseau.|`medusa -M ftp -h 192.168.1.100 -u admin -P passwords.txt`|
|HTTP|Protocole de transfert hypertexte|Forçage brut des formulaires de connexion sur les applications web via HTTP (GET/POST).|`medusa -M http -h www.example.com -U users.txt -P passwords.txt -m DIR:/login.php -m FORM:username=^USER^&password=^PASS^`|
|IMAP|Internet Message Access Protocol|Forçage brut des connexions IMAP, souvent utilisées pour accéder aux serveurs de messagerie.|`medusa -M imap -h mail.example.com -U users.txt -P passwords.txt`|
|MySQL|Base de données MySQL|Forçage brut des identifiants de base de données MySQL, couramment utilisés pour les applications web et les bases de données.|`medusa -M mysql -h 192.168.1.100 -u root -P passwords.txt`|
|POP3|Post Office Protocol 3|Forçage brut des connexions POP3, généralement utilisées pour récupérer des e-mails depuis un serveur de messagerie.|`medusa -M pop3 -h mail.example.com -U users.txt -P passwords.txt`|
|RDP|Protocole de bureau à distance|Forçage brut des connexions RDP, couramment utilisées pour l'accès au bureau à distance des systèmes Windows.|`medusa -M rdp -h 192.168.1.100 -u admin -P passwords.txt`|
|SSHv2|Secure Shell (SSH)|Forçage brut des connexions SSH, couramment utilisées pour l'accès à distance sécurisé.|`medusa -M ssh -h 192.168.1.100 -u root -P passwords.txt`|
|Subversion (SVN)|Système de contrôle de version|Forçage brut des dépôts Subversion (SVN) pour le contrôle de version.|`medusa -M svn -h 192.168.1.100 -u admin -P passwords.txt`|
|Telnet|Protocole Telnet|Forçage brut des services Telnet pour l'exécution de commandes à distance sur des systèmes plus anciens.|`medusa -M telnet -h 192.168.1.100 -u admin -P passwords.txt`|
|VNC|Virtual Network Computing|Forçage brut des identifiants de connexion VNC pour l'accès au bureau à distance.|`medusa -M vnc -h 192.168.1.100 -P passwords.txt`|
|Web Form|Forçage brut des formulaires de connexion Web|Forçage brut des formulaires de connexion sur les sites web à l'aide de requêtes HTTP POST.|`medusa -M web-form -h www.example.com -U users.txt -P passwords.txt -m FORM:"username=^USER^&password=^PASS^:F=Invalid"`|

### Cibler un serveur SSH

Imaginez un scénario où vous devez tester la sécurité d'un serveur SSH à l'adresse `192.168.0.100`. Vous disposez d'une liste de noms d'utilisateur potentiels dans `usernames.txt` et de mots de passe courants dans `passwords.txt`. Pour lancer une attaque par force brute contre le service SSH sur ce serveur, utilisez la commande Medusa suivante :

```bash
Hiterof13@htb[/htb]$ medusa -h 192.168.0.100 -U usernames.txt -P passwords.txt -M ssh
```

Cette commande demande à Medusa de :

- Cibler l'hôte à l'adresse `192.168.0.100`.
- Utiliser les noms d'utilisateur du fichier `usernames.txt`.
- Tester les mots de passe listés dans le fichier `passwords.txt`.
- Employer le module `ssh` pour l'attaque.

Medusa essaiera systématiquement chaque combinaison nom d'utilisateur-mot de passe contre le service SSH pour tenter d'obtenir un accès non autorisé.

### Cibler plusieurs serveurs Web avec une authentification HTTP de base

Supposons que vous ayez une liste de serveurs web qui utilisent l'authentification HTTP de base. Les adresses de ces serveurs sont stockées dans `web_servers.txt`, et vous disposez également de listes de noms d'utilisateur et de mots de passe courants dans `usernames.txt` et `passwords.txt`, respectivement. Pour tester ces serveurs simultanément, exécutez :

```bash
Hiterof13@htb[/htb]$ medusa -H web_servers.txt -U usernames.txt -P passwords.txt -M http -m GET
```

Dans ce cas, Medusa va :

- Parcourir la liste des serveurs web dans `web_servers.txt`.
- Utiliser les noms d'utilisateur et les mots de passe fournis.
- Employer le module `http` avec la méthode `GET` pour tenter les connexions.

En exécutant plusieurs threads, Medusa vérifie efficacement chaque serveur à la recherche d'identifiants faibles.

### Tester les mots de passe vides ou par défaut

Si vous voulez évaluer si des comptes sur un hôte spécifique (`10.0.0.5`) ont des mots de passe vides ou par défaut (où le mot de passe correspond au nom d'utilisateur), vous pouvez utiliser :

```bash
Hiterof13@htb[/htb]$ medusa -h 10.0.0.5 -U usernames.txt -e ns -M service_name
```

Cette commande demande à Medusa de :

- Cibler l'hôte à l'adresse `10.0.0.5`.
- Utiliser les noms d'utilisateur de `usernames.txt`.
- Effectuer des vérifications supplémentaires pour les mots de passe vides (`-e n`) et les mots de passe correspondant au nom d'utilisateur (`-e s`).
- Utiliser le module de service approprié (remplacez `service_name` par le nom de module correct).

Medusa essaiera chaque nom d'utilisateur avec un mot de passe vide, puis avec le mot de passe correspondant au nom d'utilisateur, révélant potentiellement des comptes avec des configurations faibles ou par défaut.
---

← [[08 - Formulaires de connexion]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[10 - Services Web]] →
