---
tags:
  - linux
ordre: 26
---

# Sécurité Linux

Tous les systèmes informatiques présentent un risque d'intrusion inhérent. Certains présentent un risque plus élevé que d'autres, comme un serveur web exposé sur Internet hébergeant de multiples applications web complexes. Les systèmes Linux sont également moins sujets aux virus qui affectent les systèmes d'exploitation Windows et ne présentent pas une surface d'attaque (attack surface) aussi grande que les hôtes joints à un domaine Active Directory. Quoi qu'il en soit, il est essentiel de mettre en place certains principes fondamentaux pour sécuriser n'importe quel système Linux.

L'une des mesures de sécurité les plus importantes pour les systèmes d'exploitation Linux est de maintenir le système d'exploitation et les paquets installés à jour. Cela peut être réalisé avec une commande telle que :

```bash
Hiterof13@htb[/htb]$ apt update && apt dist-upgrade
```

Si les règles de pare-feu (firewall) ne sont pas correctement définies au niveau du réseau, nous pouvons utiliser le pare-feu Linux et/ou `iptables` pour restreindre le trafic entrant/sortant de l'hôte.

Si le SSH est ouvert sur le serveur, la configuration doit être paramétrée pour interdire la connexion par mot de passe et empêcher l'utilisateur root de se connecter via SSH. Il est également important d'éviter de se connecter et d'administrer le système en tant qu'utilisateur root autant que possible et de gérer adéquatement le contrôle d'accès. L'accès des utilisateurs doit être déterminé sur la base du principe de moindre privilège (principle of least privilege). Par exemple, si un utilisateur a besoin d'exécuter une commande en tant que root, cette commande doit être spécifiée dans la configuration `sudoers` au lieu de lui donner des droits sudo complets. Un autre mécanisme de protection courant qui peut être utilisé est `fail2ban`. Cet outil compte le nombre de tentatives de connexion échouées, et si un utilisateur a atteint le nombre maximum, l'hôte qui a tenté de se connecter sera traité comme configuré.

Il est également important d'auditer périodiquement le système pour s'assurer qu'il n'existe pas de problèmes qui pourraient faciliter une escalade de privilèges (privilege escalation), tels qu'un noyau (kernel) obsolète, des problèmes de permissions utilisateur, des fichiers inscriptibles par tous (world-writable files), des tâches cron mal configurées ou des services mal configurés. De nombreux administrateurs oublient la possibilité que certaines versions du noyau doivent être mises à jour manuellement.

Une option pour renforcer davantage la sécurité des systèmes Linux est `Security-Enhanced Linux` (`SELinux`) ou `AppArmor`. Il s'agit d'un module de sécurité du noyau qui peut être utilisé pour des politiques de contrôle d'accès. Dans SELinux, chaque processus, fichier, répertoire et objet système reçoit une étiquette. Des règles de politique sont créées pour contrôler l'accès entre ces processus et objets étiquetés et sont appliquées par le noyau. Cela signifie que l'accès peut être configuré pour contrôler quels utilisateurs et applications peuvent accéder à quelles ressources. SELinux fournit des contrôles d'accès très granulaires, comme la spécification de qui peut ajouter du contenu à un fichier ou le déplacer.

En outre, il existe différentes applications et services tels que [Snort](https://www.snort.org/), [chkrootkit](http://www.chkrootkit.org/), [rkhunter](https://packages.debian.org/sid/rkhunter), [Lynis](https://cisofy.com/lynis/), et d'autres qui peuvent contribuer à la sécurité de Linux. De plus, certains paramètres de sécurité doivent être appliqués, tels que :

- Supprimer ou désactiver tous les services et logiciels non nécessaires
- Supprimer tous les services qui reposent sur des mécanismes d'authentification non chiffrés
- S'assurer que NTP est activé et que Syslog est en cours d'exécution
- S'assurer que chaque utilisateur a son propre compte
- Imposer l'utilisation de mots de passe forts
- Configurer le vieillissement des mots de passe (password aging) et restreindre l'utilisation des mots de passe précédents
- Verrouiller les comptes utilisateurs après des échecs de connexion
- Désactiver tous les binaires SUID/SGID non désirés

Cette liste est incomplète, car la sécurité n'est pas un produit mais un processus. Cela signifie que des mesures spécifiques doivent toujours être prises pour mieux protéger les systèmes, et cela dépend de la connaissance qu'ont les administrateurs de leurs systèmes d'exploitation. Mieux les administrateurs connaissent le système, et plus ils sont formés, meilleures et plus sûres seront leurs précautions et mesures de sécurité.

---

## TCP Wrappers

TCP wrapper est un mécanisme de sécurité utilisé dans les systèmes Linux qui permet à l'administrateur système de contrôler quels services sont autorisés à accéder au système. Il fonctionne en restreignant l'accès à certains services en fonction du nom d'hôte (hostname) ou de l'adresse IP de l'utilisateur qui demande l'accès. Lorsqu'un client tente de se connecter à un service, le système consultera d'abord les règles définies dans les fichiers de configuration des TCP wrappers pour déterminer l'adresse IP du client. Si l'adresse IP correspond aux critères spécifiés dans les fichiers de configuration, le système accordera alors au client l'accès au service. Cependant, si les critères ne sont pas remplis, la connexion sera refusée, fournissant une couche de sécurité supplémentaire pour le service. Les TCP wrappers utilisent les fichiers de configuration suivants :

- `/etc/hosts.allow`
- `/etc/hosts.deny`

En bref, le fichier `/etc/hosts.allow` spécifie quels services et hôtes sont autorisés à accéder au système, tandis que le fichier `/etc/hosts.deny` spécifie quels services et hôtes ne sont pas autorisés à y accéder. Ces fichiers peuvent être configurés en y ajoutant des règles spécifiques.

### /etc/hosts.allow

```bash
Hiterof13@htb[/htb]$ cat /etc/hosts.allow
# Autoriser l'accès à SSH depuis le réseau local
sshd : 10.129.14.0/24

# Autoriser l'accès à FTP depuis un hôte spécifique
ftpd : 10.129.14.10

# Autoriser l'accès à Telnet depuis n'importe quel hôte du domaine inlanefreight.local
telnetd : .inlanefreight.local
```

### /etc/hosts.deny

```bash
Hiterof13@htb[/htb]$ cat /etc/hosts.deny
# Refuser l'accès à tous les services depuis n'importe quel hôte du domaine inlanefreight.com
ALL : .inlanefreight.com

# Refuser l'accès à SSH depuis un hôte spécifique
sshd : 10.129.22.22

# Refuser l'accès à FTP aux hôtes avec des adresses IP dans la plage de 10.129.22.0 à 10.129.22.255
ftpd : 10.129.22.0/24
```

Il est important de se rappeler que l'ordre des règles dans les fichiers est important. La première règle qui correspond au service et à l'hôte demandés est celle qui sera appliquée. Il est également important de noter que les TCP wrappers ne remplacent pas un pare-feu, car ils sont limités par le fait qu'ils ne peuvent contrôler que l'accès aux services et non aux ports.

---

← [[25 - Protocoles de bureau à distance sous Linux]] | [[00 - Sommaire Linux|Sommaire]] | [[27 - Configuration du pare-feu]] →
