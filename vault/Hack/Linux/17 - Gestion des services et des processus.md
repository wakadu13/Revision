---
tags:
  - linux
ordre: 17
---

# Gestion des services et des processus

Les services, également connus sous le nom de démons (daemons), sont des composants fondamentaux d'un système Linux qui s'exécutent silencieusement en arrière-plan « sans interaction directe de l'utilisateur ». Ils effectuent des tâches cruciales qui maintiennent le système opérationnel et fournissent des fonctionnalités supplémentaires. En général, les services peuvent être classés en deux catégories :

### Services système

Ce sont des services internes requis lors du démarrage du système. Ils effectuent des tâches essentielles liées au matériel et initialisent les composants système nécessaires au bon fonctionnement du système d'exploitation. Ils sont comme le moteur et la boîte de vitesses d'une voiture. Ils démarrent lorsque vous tournez la clé de contact et sont essentiels au fonctionnement de la voiture. Sans eux, la voiture n'avancerait pas.

### Services installés par l'utilisateur

Ces services sont ajoutés par les utilisateurs et incluent généralement des applications serveur et d'autres processus d'arrière-plan qui fournissent des fonctionnalités ou des capacités spécifiques. Ces types de services sont comme la climatisation ou le système de navigation GPS d'une voiture. Bien qu'ils ne soient pas indispensables au fonctionnement de la voiture, ils améliorent les fonctionnalités et offrent des options supplémentaires selon les préférences du conducteur.

Les démons sont souvent identifiés par la lettre `d` à la fin du nom de leur programme, comme `sshd` (démon SSH) ou `systemd`. Tout comme une voiture dépend à la fois de ses composants principaux et de ses options pour offrir une expérience complète, un système Linux utilise à la fois les services système et les services installés par l'utilisateur pour fonctionner efficacement et répondre aux besoins de l'utilisateur.

En général, nous avons seulement quelques objectifs lorsque nous traitons un service ou un processus :

1. Démarrer/Redémarrer un service/processus
2. Arrêter un service/processus
3. Voir ce qui se passe/s'est passé avec un service/processus
4. Activer/Désactiver un service/processus au démarrage
5. Trouver un service/processus

La plupart des distributions Linux modernes ont adopté `systemd` comme système d'initialisation (init system). C'est le premier processus qui démarre lors du processus de démarrage (boot process) et se voit attribuer un identifiant de processus (Process ID ou `PID`). Tous les processus d'un système Linux se voient attribuer un `PID` et peuvent être consultés dans le répertoire `/proc/`, qui contient des informations sur chaque processus. Les processus peuvent également avoir un identifiant de processus parent (Parent Process ID ou `PPID`), indiquant qu'ils ont été démarrés par un autre processus (le parent), ce qui en fait des processus enfants (child processes).

---

## Systemctl

Après avoir installé `OpenSSH` sur notre VM, nous pouvons démarrer le service avec la commande suivante.

```bash
Hiterof13@htb[/htb]$ systemctl start ssh
```

Une fois le service démarré, nous pouvons maintenant vérifier s'il s'exécute sans erreur.

```bash
Hiterof13@htb[/htb]$ systemctl status ssh
● ssh.service - OpenBSD Secure Shell server
   Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2020-05-14 15:08:23 CEST; 24h ago
   Main PID: 846 (sshd)
   Tasks: 1 (limit: 4681)
   CGroup: /system.slice/ssh.service
           └─846 /usr/sbin/sshd -D

Mai 14 15:08:22 inlane systemd[1]: Starting OpenBSD Secure Shell server...
Mai 14 15:08:23 inlane sshd[846]: Server listening on 0.0.0.0 port 22.
Mai 14 15:08:23 inlane sshd[846]: Server listening on :: port 22.
Mai 14 15:08:23 inlane systemd[1]: Started OpenBSD Secure Shell server.
Mai 14 15:08:30 inlane systemd[1]: Reloading OpenBSD Secure Shell server.
Mai 14 15:08:31 inlane sshd[846]: Received SIGHUP; restarting.
Mai 14 15:08:31 inlane sshd[846]: Server listening on 0.0.0.0 port 22.
Mai 14 15:08:31 inlane sshd[846]: Server listening on :: port 22.
```

Pour ajouter OpenSSH au script SysV afin d'indiquer au système d'exécuter ce service après le démarrage, nous pouvons le lier avec la commande suivante :

```bash
Hiterof13@htb[/htb]$ systemctl enable ssh
Synchronizing state of ssh.service with SysV service script with /lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable ssh
```

Une fois le système redémarré, le serveur OpenSSH s'exécutera automatiquement. Nous pouvons le vérifier avec un outil appelé `ps`.

```bash
Hiterof13@htb[/htb]$ ps -aux | grep ssh
root       846  0.0  0.1  72300  5660 ?        Ss   Mai14   0:00 /usr/sbin/sshd -D
```

Nous pouvons également utiliser `systemctl` pour lister tous les services.

```bash
Hiterof13@htb[/htb]$ systemctl list-units --type=service
UNIT                                                       LOAD   ACTIVE SUB     DESCRIPTION
accounts-daemon.service                                    loaded active running Accounts Service
acpid.service                                              loaded active running ACPI event daemon
apache2.service                                            loaded active running The Apache HTTP Server
apparmor.service                                           loaded active exited  AppArmor initialization
apport.service                                             loaded active exited  LSB: automatic crash repor
avahi-daemon.service                                       loaded active running Avahi mDNS/DNS-SD Stack
bolt.service                                               loaded active running Thunderbolt system service
```

Il est tout à fait possible que les services ne démarrent pas en raison d'une erreur. Pour voir le problème, nous pouvons utiliser l'outil `journalctl` pour consulter les journaux (logs).

```bash
Hiterof13@htb[/htb]$ journalctl -u ssh.service --no-pager
-- Logs begin at Wed 2020-05-13 17:30:52 CEST, end at Fri 2020-05-15 16:00:14 CEST. --
Mai 13 20:38:44 inlane systemd[1]: Starting OpenBSD Secure Shell server...
Mai 13 20:38:44 inlane sshd[2722]: Server listening on 0.0.0.0 port 22.
Mai 13 20:38:44 inlane sshd[2722]: Server listening on :: port 22.
Mai 13 20:38:44 inlane systemd[1]: Started OpenBSD Secure Shell server.
Mai 13 20:39:06 inlane sshd[3939]: Connection closed by 10.22.2.1 port 36444 [preauth]
Mai 13 20:39:27 inlane sshd[3942]: Accepted password for master from 10.22.2.1 port 36452 ssh2
Mai 13 20:39:27 inlane sshd[3942]: pam_unix(sshd:session): session opened for user master by (uid=0)
Mai 13 20:39:28 inlane sshd[3942]: pam_unix(sshd:session): session closed for user master
Mai 14 02:04:49 inlane sshd[2722]: Received signal 15; terminating.
Mai 14 02:04:49 inlane systemd[1]: Stopping OpenBSD Secure Shell server...
Mai 14 02:04:49 inlane systemd[1]: Stopped OpenBSD Secure Shell server.
-- Reboot --
```

---

## Tuer un processus

Un processus peut se trouver dans les états suivants :

- En cours d'exécution
- En attente (attend un événement ou une ressource système)
- Arrêté
- Zombie (arrêté mais ayant toujours une entrée dans la table des processus).

Les processus peuvent être contrôlés à l'aide de `kill`, `pkill`, `pgrep` et `killall`. Pour interagir avec un processus, nous devons lui envoyer un signal. Nous pouvons afficher tous les signaux avec la commande suivante :

```bash
Hiterof13@htb[/htb]$ kill -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL       5) SIGTRAP
 6) SIGABRT      7) SIGBUS       8) SIGFPE       9) SIGKILL     10) SIGUSR1
11) SIGSEGV     12) SIGUSR2     13) SIGPIPE     14) SIGALRM     15) SIGTERM
16) SIGSTKFLT   17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
21) SIGTTIN     22) SIGTTOU     23) SIGURG      24) SIGXCPU     25) SIGXFSZ
26) SIGVTALRM   27) SIGPROF     28) SIGWINCH    29) SIGIO       30) SIGPWR
31) SIGSYS      34) SIGRTMIN    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3
38) SIGRTMIN+4  39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12 47) SIGRTMIN+13
48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14 51) SIGRTMAX-13 52) SIGRTMAX-12
53) SIGRTMAX-11 54) SIGRTMAX-10 55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7
58) SIGRTMAX-6  59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
63) SIGRTMAX-1  64) SIGRTMAX
```

Les signaux les plus couramment utilisés sont :

|**Signal**|**Description**|
|---|---|
|`1`|`SIGHUP` - Envoyé à un processus lorsque le terminal qui le contrôle est fermé.|
|`2`|`SIGINT` - Envoyé lorsqu'un utilisateur appuie sur `[Ctrl] + C` dans le terminal de contrôle pour interrompre un processus.|
|`3`|`SIGQUIT` - Envoyé lorsqu'un utilisateur appuie sur `[Ctrl] + D` pour quitter.|
|`9`|`SIGKILL` - Tue immédiatement un processus sans opération de nettoyage.|
|`15`|`SIGTERM` - Terminaison du programme.|
|`19`|`SIGSTOP` - Arrête le programme. Il ne peut plus être géré.|
|`20`|`SIGTSTP` - Envoyé lorsqu'un utilisateur appuie sur `[Ctrl] + Z` pour demander la suspension d'un service. L'utilisateur peut le gérer par la suite.|

Par exemple, si un programme se figeait, nous pourrions forcer sa fermeture avec la commande suivante :

```bash
Hiterof13@htb[/htb]$ kill 9 <PID>
```

---

## Mettre un processus en arrière-plan

Il sera parfois nécessaire de mettre le scan ou le processus que nous venons de démarrer en arrière-plan pour continuer à utiliser la session en cours afin d'interagir avec le système ou de démarrer d'autres processus. Comme nous l'avons déjà vu, nous pouvons le faire avec le raccourci `[Ctrl + Z]`. Comme mentionné ci-dessus, nous envoyons le signal `SIGTSTP` au noyau (kernel), qui suspend le processus.

```bash
Hiterof13@htb[/htb]$ ping -c 10 www.hackthebox.eu
PING www.hackthebox.eu (104.20.55.68) 56(84) bytes of data.
[Ctrl + Z]
[1]+  Stopped                 ping -c 10 www.hackthebox.eu
Hiterof13@htb[/htb]$ vim tmpfile
[Ctrl + Z]
[2]+  Stopped                 vim tmpfile
```

Maintenant, tous les processus en arrière-plan peuvent être affichés avec la commande suivante.

```bash
Hiterof13@htb[/htb]$ jobs
[1]+  Stopped                 ping -c 10 www.hackthebox.eu
[2]+  Stopped                 vim tmpfile
```

Le raccourci `[Ctrl] + Z` suspend les processus, et ils ne seront plus exécutés. Pour qu'il continue de s'exécuter en arrière-plan, nous devons entrer la commande `bg` pour mettre le processus en arrière-plan.

```bash
Hiterof13@htb[/htb]$ bg
[1]+ ping -c 10 www.hackthebox.eu &
Hiterof13@htb[/htb]$
--- www.hackthebox.eu ping statistics ---
10 packets transmitted, 0 received, 100% packet loss, time 113482ms

[ENTER]
[1]+  Exit 1                  ping -c 10 www.hackthebox.eu
```

Une autre option consiste à lancer automatiquement le processus en arrière-plan en ajoutant une esperluette (`&`) à la fin de la commande.

```bash
Hiterof13@htb[/htb]$ ping -c 10 www.hackthebox.eu &
[1] 10825
PING www.hackthebox.eu (172.67.1.1) 56(84) bytes of data.
```

Une fois le processus terminé, nous verrons les résultats.

```bash
Hiterof13@htb[/htb]$
--- www.hackthebox.eu ping statistics ---
10 packets transmitted, 0 received, 100% packet loss, time 9210ms

[ENTER]
[1]+  Exit 1                  ping -c 10 www.hackthebox.eu
```

---

## Mettre un processus au premier plan

Après cela, nous pouvons utiliser la commande `jobs` pour lister tous les processus en arrière-plan. Les processus en arrière-plan ne nécessitent pas d'interaction de l'utilisateur, et nous pouvons utiliser la même session shell sans attendre que le processus se termine. Une fois que le scan ou le processus a terminé son travail, le terminal nous informera que le processus est terminé.

```bash
Hiterof13@htb[/htb]$ jobs
[1]+  Running                 ping -c 10 www.hackthebox.eu &
```

Si nous voulons ramener le processus d'arrière-plan au premier plan et interagir à nouveau avec lui, nous pouvons utiliser la commande `fg <ID>`.

```bash
Hiterof13@htb[/htb]$ fg 1
ping -c 10 www.hackthebox.eu

--- www.hackthebox.eu ping statistics ---
10 packets transmitted, 0 received, 100% packet loss, time 9206ms
```

---

## Exécuter plusieurs commandes

Il existe trois possibilités pour exécuter plusieurs commandes, l'une après l'autre. Celles-ci sont séparées par :

- Un point-virgule (`;`)
- Une double esperluette (`&&`)
- Des barres verticales (pipes) (`|`)

La différence entre eux réside dans le traitement des processus précédents et dépend si le processus précédent s'est terminé avec succès ou avec des erreurs. Le point-virgule (`;`) est un séparateur de commandes et exécute les commandes en ignorant les résultats et les erreurs des commandes précédentes.

```bash
Hiterof13@htb[/htb]$ echo '1'; echo '2'; echo '3'
1
2
3
```

Par exemple, si nous exécutons la même commande mais remplaçons la deuxième commande, `ls`, par un fichier qui n'existe pas, nous obtenons une erreur, et la troisième commande sera néanmoins exécutée.

```bash
Hiterof13@htb[/htb]$ echo '1'; ls MISSING_FILE; echo '3'
1
ls: cannot access 'MISSING_FILE': No such file or directory
3
```

Cependant, la situation est différente si nous utilisons la double esperluette (`&&`) pour exécuter les commandes l'une après l'autre. S'il y a une erreur dans l'une des commandes, les suivantes ne seront plus exécutées et l'ensemble du processus sera arrêté.

```bash
Hiterof13@htb[/htb]$ echo '1' && ls MISSING_FILE && echo '3'
1
ls: cannot access 'MISSING_FILE': No such file or directory
```

Les barres verticales (pipes) (`|`) ne dépendent pas seulement du fonctionnement correct et sans erreur des processus précédents, mais aussi des résultats des processus précédents.

---

← [[16 - Gestion de paquets]] | [[00 - Sommaire Linux|Sommaire]] | [[18 - Planification de tâches]] →
