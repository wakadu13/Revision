---
tags:
  - getting-started
ordre: 11
---

# Élévation de privilèges

---

Notre accès initial à un serveur distant se fait généralement dans le contexte d'un utilisateur à faibles privilèges, ce qui ne nous donne pas un accès complet à la machine. Pour obtenir un accès total, nous devrons trouver une vulnérabilité interne/locale qui nous permettra d'élever nos privilèges à l'utilisateur `root` sur `Linux` ou à l'utilisateur `administrator`/`SYSTEM` sur `Windows`. Passons en revue quelques méthodes courantes d'élévation de nos privilèges.

---

## Checklists d'élévation de privilèges

Une fois que nous avons obtenu un accès initial à une machine, nous voulons l'énumérer de manière approfondie pour trouver toute vulnérabilité potentielle que nous pouvons exploiter pour atteindre un niveau de privilège plus élevé. Nous pouvons trouver de nombreuses checklists et aide-mémoires en ligne qui regroupent des vérifications que nous pouvons effectuer et les commandes pour les exécuter. Une excellente ressource est [HackTricks](https://book.hacktricks.xyz/), qui propose une excellente checklist pour l'élévation de privilèges locale sur [Linux](https://book.hacktricks.wiki/en/linux-hardening/linux-privilege-escalation-checklist.html) et sur [Windows](https://book.hacktricks.wiki/en/windows-hardening/checklist-windows-privilege-escalation.html). Un autre excellent dépôt est [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings), qui propose également des checklists pour [Linux](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Linux%20-%20Privilege%20Escalation.md) et [Windows](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Windows%20-%20Privilege%20Escalation.md). Nous devons commencer à expérimenter avec diverses commandes et techniques et nous familiariser avec elles pour comprendre les multiples faiblesses qui peuvent conduire à une élévation de nos privilèges.

---

## Scripts d'énumération

Beaucoup des commandes ci-dessus peuvent être exécutées automatiquement avec un script pour parcourir le rapport et rechercher d'éventuelles faiblesses. Nous pouvons exécuter de nombreux scripts pour énumérer automatiquement le serveur en lançant des commandes courantes qui renvoient des résultats intéressants. Parmi les scripts d'énumération Linux courants, on trouve [LinEnum](https://github.com/rebootuser/LinEnum.git) et [linuxprivchecker](https://github.com/sleventyeleven/linuxprivchecker), et pour Windows, [Seatbelt](https://github.com/GhostPack/Seatbelt) et [JAWS](https://github.com/411Hall/JAWS).

Un autre outil utile que nous pouvons utiliser pour l'énumération de serveurs est la [Privilege Escalation Awesome Scripts SUITE (PEASS)](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite), car elle est bien maintenue pour rester à jour et inclut des scripts pour l'énumération de Linux et de Windows.

Remarque : Ces scripts exécuteront de nombreuses commandes connues pour identifier les vulnérabilités et créeront beaucoup de « bruit » qui pourrait déclencher des logiciels antivirus ou des logiciels de surveillance de sécurité qui recherchent ce type d'événements. Cela peut empêcher les scripts de s'exécuter ou même déclencher une alarme indiquant que le système a été compromis. Dans certains cas, nous pourrions préférer faire une énumération manuelle plutôt que d'exécuter des scripts.

Prenons l'exemple de l'exécution du script Linux de `PEASS` appelé `LinPEAS` :

```bash
Hiterof13@htb[/htb]$ ./linpeas.sh ...SNIP...  Linux Privesc Checklist: https://book.hacktricks.xyz/linux-unix/linux-privilege-escalation-checklist  LEYEND:   RED/YELLOW: 99% a PE vector   RED: You must take a look at it   LightCyan: Users with console   Blue: Users without console & mounted devs   Green: Common things (users, groups, SUID/SGID, mounts, .sh scripts, cronjobs)   LightMangenta: Your username
====================================( Basic information )===================================== OS: Linux version 3.9.0-73-generic User & Groups:
uid=33(www-data) gid=33(www-data) groups=33(www-data) ...SNIP...
```

Comme nous pouvons le voir, une fois que le script s'exécute, il commence à collecter des informations et à les afficher dans un excellent rapport. Discutons de certaines des vulnérabilités que nous devrions rechercher dans la sortie de ces scripts.

---

## Exploits de noyau

Chaque fois que nous rencontrons un serveur exécutant un ancien système d'exploitation, nous devrions commencer par rechercher les vulnérabilités de noyau potentielles qui pourraient exister. Si le serveur n'est pas maintenu avec les dernières mises à jour et correctifs, il est probablement vulnérable à des exploits de noyau spécifiques trouvés sur des versions non patchées de Linux et Windows.

Par exemple, le script ci-dessus nous a montré que la version de Linux était `3.9.0-73-generic`. Si nous cherchons sur Google des exploits pour cette version ou utilisons `searchsploit`, nous trouverions un `CVE-2016-5195`, autrement connu sous le nom de `DirtyCow`. Nous pouvons rechercher et télécharger l'exploit [DirtyCow](https://github.com/dirtycow/dirtycow.github.io/wiki/PoCs) et l'exécuter sur le serveur pour obtenir un accès root.

Le même concept s'applique également à Windows, car il existe de nombreuses vulnérabilités dans les versions non patchées/anciennes de Windows, avec diverses vulnérabilités qui peuvent être utilisées pour l'élévation de privilèges. Nous devons garder à l'esprit que les exploits de noyau peuvent causer une instabilité du système, et nous devons faire très attention avant de les exécuter sur des systèmes de production. Il est préférable de les essayer dans un environnement de laboratoire et de ne les exécuter sur des systèmes de production qu'avec l'approbation explicite et la coordination de notre client.

---

## Logiciels vulnérables

Une autre chose que nous devrions rechercher sont les logiciels installés. Par exemple, nous pouvons utiliser la commande `dpkg -l` sur Linux ou regarder dans `C:\Program Files` sous Windows pour voir quels logiciels sont installés sur le système. Nous devrions rechercher des exploits publics pour tout logiciel installé, surtout si des versions plus anciennes sont utilisées, contenant des vulnérabilités non corrigées.

---

## Privilèges utilisateur

Un autre aspect critique à rechercher après avoir obtenu l'accès à un serveur sont les privilèges disponibles pour l'utilisateur auquel nous avons accès. Si nous sommes autorisés à exécuter certaines commandes en tant que root (ou en tant qu'un autre utilisateur), nous pourrions être en mesure d'élever nos privilèges aux utilisateurs root/système ou d'obtenir un accès en tant qu'un utilisateur différent. Voici quelques moyens courants d'exploiter certains privilèges utilisateur :

1. Sudo
2. SUID
3. Privilèges de jeton Windows (Windows Token Privileges)

La commande `sudo` sous Linux permet à un utilisateur d'exécuter des commandes en tant qu'un autre utilisateur. Elle est généralement utilisée pour permettre à des utilisateurs moins privilégiés d'exécuter des commandes en tant que root sans leur donner accès à l'utilisateur root. Cela se fait généralement car des commandes spécifiques ne peuvent être exécutées qu'en tant que root (comme `tcpdump`) ou pour permettre à l'utilisateur d'accéder à certains répertoires réservés à root. Nous pouvons vérifier quels privilèges `sudo` nous avons avec la commande `sudo -l` :

```bash
Hiterof13@htb[/htb]$ sudo -l
[sudo] password for user1: ...SNIP...  User user1 may run the following commands on ExampleServer:     (ALL : ALL) ALL
```

La sortie ci-dessus indique que nous pouvons exécuter toutes les commandes avec `sudo`, ce qui nous donne un accès complet, et nous pouvons utiliser la commande `su` avec `sudo` pour passer à l'utilisateur root :

```bash
Hiterof13@htb[/htb]$ sudo su -
[sudo] password for user1: whoami root
```

La commande ci-dessus nécessite un mot de passe pour exécuter des commandes avec `sudo`. Il y a certaines occasions où nous pouvons être autorisés à exécuter certaines applications, ou toutes les applications, sans avoir à fournir de mot de passe :

```bash
Hiterof13@htb[/htb]$ sudo -l      (user : user) NOPASSWD: /bin/echo
```

L'entrée `NOPASSWD` montre que la commande `/bin/echo` peut être exécutée sans mot de passe. Cela serait utile si nous avions obtenu l'accès au serveur par une vulnérabilité et n'avions pas le mot de passe de l'utilisateur. Comme il est indiqué `user`, nous pouvons exécuter `sudo` en tant que cet utilisateur et non en tant que root. Pour ce faire, nous pouvons spécifier l'utilisateur avec `-u user` :

```bash
Hiterof13@htb[/htb]$ sudo -u user /bin/echo Hello World!      Hello World!
```

Une fois que nous trouvons une application particulière que nous pouvons exécuter avec `sudo`, nous pouvons chercher des moyens de l'exploiter pour obtenir un shell en tant qu'utilisateur root. [GTFOBins](https://gtfobins.github.io/) contient une liste de commandes et comment elles peuvent être exploitées via `sudo`. Nous pouvons rechercher l'application sur laquelle nous avons un privilège `sudo`, et si elle existe, elle pourrait nous indiquer la commande exacte que nous devrions exécuter pour obtenir un accès root en utilisant le privilège `sudo` que nous avons.

[LOLBAS](https://lolbas-project.github.io/#) contient également une liste d'applications Windows que nous pourrions être en mesure d'utiliser pour effectuer certaines fonctions, comme télécharger des fichiers ou exécuter des commandes dans le contexte d'un utilisateur privilégié.

---

## Tâches planifiées

Tant sous Linux que sous Windows, il existe des méthodes pour faire exécuter des scripts à des intervalles spécifiques pour effectuer une tâche. Quelques exemples sont une analyse antivirus s'exécutant toutes les heures ou un script de sauvegarde s'exécutant toutes les 30 minutes. Il y a généralement deux façons de tirer parti des tâches planifiées (Windows) ou des tâches cron (Linux) pour élever nos privilèges :

1. Ajouter de nouvelles tâches planifiées/tâches cron
2. Les tromper pour qu'elles exécutent un logiciel malveillant

Le moyen le plus simple est de vérifier si nous sommes autorisés à ajouter de nouvelles tâches planifiées. Sous Linux, une forme courante de maintenance des tâches planifiées se fait via les `tâches Cron`. Il existe des répertoires spécifiques que nous pourrions utiliser pour ajouter de nouvelles tâches cron si nous avons les permissions d'`écriture` sur eux. Ceux-ci incluent :

1. `/etc/crontab`
2. `/etc/cron.d`
3. `/var/spool/cron/crontabs/root`

Si nous pouvons écrire dans un répertoire appelé par une tâche cron, nous pouvons écrire un script bash avec une commande de shell inversé (reverse shell), qui devrait nous envoyer un shell inversé lors de son exécution.

---

## Identifiants exposés

Ensuite, nous pouvons rechercher des fichiers que nous pouvons lire et voir s'ils contiennent des identifiants exposés. C'est très courant avec les `fichiers de configuration`, les `fichiers journaux` et les fichiers d'historique utilisateur (`bash_history` sous Linux et `PSReadLine` sous Windows). Les scripts d'énumération que nous avons discutés au début recherchent généralement des mots de passe potentiels dans les fichiers et nous les fournissent, comme ci-dessous :

```bash
...SNIP...
[+] Searching passwords in config PHP files
[+] Finding passwords inside logs (limit 70) ...SNIP... /var/www/html/config.php: $conn = new mysqli(localhost, 'db_user', 'password123');
```

Comme nous pouvons le voir, le mot de passe de la base de données '`password123`' est exposé, ce qui nous permettrait de nous connecter aux bases de données `mysql` locales et de rechercher des informations intéressantes. Nous pouvons également vérifier la `réutilisation de mot de passe`, car l'utilisateur système a peut-être utilisé son mot de passe pour les bases de données, ce qui pourrait nous permettre d'utiliser le même mot de passe pour passer à cet utilisateur, comme suit :

```bash
Hiterof13@htb[/htb]$ su -  Password: password123 whoami  root
```

Nous pouvons également utiliser les identifiants de l'utilisateur pour nous connecter en `ssh` au serveur en tant que cet utilisateur.

---

## Clés SSH

Enfin, parlons des clés SSH. Si nous avons un accès en lecture sur le répertoire `.ssh` d'un utilisateur spécifique, nous pouvons lire ses clés SSH privées qui se trouvent dans `/home/user/.ssh/id_rsa` ou `/root/.ssh/id_rsa`, et les utiliser pour nous connecter au serveur. Si nous pouvons lire le répertoire `/root/.ssh/` et pouvons lire le fichier `id_rsa`, nous pouvons le copier sur notre machine et utiliser le drapeau `-i` pour nous connecter avec :

```bash
Hiterof13@htb[/htb]$ vim id_rsa

Hiterof13@htb[/htb]$ chmod 600 id_rsa

Hiterof13@htb[/htb]$ ssh root@10.10.10.10 -i id_rsa  root@10.10.10.10#
```

Notez que nous avons utilisé la commande 'chmod 600 id_rsa' sur la clé après l'avoir créée sur notre machine pour rendre les permissions du fichier plus restrictives. Si les clés SSH ont des permissions laxistes, c'est-à-dire qu'elles peuvent être lues par d'autres personnes, le serveur ssh les empêchera de fonctionner.

Si nous nous retrouvons avec un accès en écriture au répertoire `/.ssh/` d'un utilisateur, nous pouvons placer notre clé publique dans le répertoire ssh de l'utilisateur à l'emplacement `/home/user/.ssh/authorized_keys`. Cette technique est généralement utilisée pour obtenir un accès ssh après avoir obtenu un shell en tant que cet utilisateur. La configuration SSH actuelle n'acceptera pas les clés écrites par d'autres utilisateurs, donc cela ne fonctionnera que si nous avons déjà pris le contrôle de cet utilisateur. Nous devons d'abord créer une nouvelle clé avec `ssh-keygen` et le drapeau `-f` pour spécifier le fichier de sortie :

```bash
Hiterof13@htb[/htb]$ ssh-keygen -f key  Generating public/private rsa key pair. Enter passphrase (empty for no passphrase): ******* Enter same passphrase again: *******  Your identification has been saved in key Your public key has been saved in key.pub The key fingerprint is: SHA256:...SNIP... user@parrot The key's randomart image is: +---[RSA 3072]----+ |   ..o.++.+      | ...SNIP... |     . ..oo+.    | +----[SHA256]-----+
```

Cela nous donnera deux fichiers : `key` (que nous utiliserons avec `ssh -i`) et `key.pub`, que nous copierons sur la machine distante. Copions `key.pub`, puis sur la machine distante, nous l'ajouterons dans `/root/.ssh/authorized_keys` :

```bash
user@remotehost$ echo "ssh-rsa AAAAB...SNIP...M= user@parrot" >> /root/.ssh/authorized_keys
```

Maintenant, le serveur distant devrait nous permettre de nous connecter en tant que cet utilisateur en utilisant notre clé privée :

```bash
Hiterof13@htb[/htb]$ ssh root@10.10.10.10 -i key  root@remotehost#
```

Comme nous pouvons le voir, nous pouvons maintenant nous connecter en ssh en tant qu'utilisateur `root`. Les modules [Linux Privilege Escalation](https://academy.hackthebox.com/module/details/51) et [Windows Privilege Escalation](https://academy.hackthebox.com/module/details/67) entrent plus en détail sur la façon d'utiliser chacune de ces méthodes pour l'élévation de privilèges, ainsi que de nombreuses autres.
---

← [[09 - Exploits Publics]] | [[00 - Sommaire Getting Started|Sommaire]] | [[12 - Transférer des Fichiers]] →
