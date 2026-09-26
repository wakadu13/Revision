---
tags:
  - linux
ordre: 28
---

# Journaux système

Les journaux système (system logs) sur Linux sont un ensemble de fichiers qui contiennent des informations sur le système et les activités qui s'y déroulent. Ces journaux sont importants pour surveiller et dépanner le système, car ils peuvent fournir des informations sur le comportement du système, l'activité des applications et les événements de sécurité. Ces journaux système peuvent également être une source précieuse d'informations pour identifier les faiblesses et les vulnérabilités de sécurité potentielles au sein d'un système Linux. En analysant les journaux sur nos systèmes cibles, nous pouvons obtenir des informations sur le comportement du système, l'activité réseau et l'activité des utilisateurs, et nous pouvons utiliser ces informations pour identifier toute activité anormale, telle que des connexions non autorisées, des tentatives d'attaques, des identifiants en texte clair ou des accès inhabituels à des fichiers, ce qui pourrait indiquer une potentielle faille de sécurité (security breach).

En tant que testeurs d'intrusion (penetration testers), nous pouvons également utiliser les journaux système pour surveiller l'efficacité de nos activités de tests de sécurité. En examinant les journaux après avoir effectué des tests de sécurité, nous pouvons déterminer si nos activités ont déclenché des événements de sécurité, tels que des alertes de détection d'intrusion ou des avertissements système. Ces informations peuvent nous aider à affiner nos stratégies de test et à améliorer la sécurité globale du système.

Afin d'assurer la sécurité d'un système Linux, il est important de configurer correctement les journaux système. Cela inclut le réglage des niveaux de journalisation appropriés, la configuration de la rotation des journaux pour éviter que les fichiers journaux ne deviennent trop volumineux, et s'assurer que les journaux sont stockés en toute sécurité et protégés contre tout accès non autorisé. De plus, il est important d'examiner et d'analyser régulièrement les journaux pour identifier les risques de sécurité potentiels et répondre à tout événement de sécurité en temps opportun. Il existe plusieurs types de journaux système sur Linux, notamment :

- Journaux du noyau
- Journaux système
- Journaux d'authentification
- Journaux d'application
- Journaux de sécurité

## Journaux du noyau

Ces journaux contiennent des informations sur le noyau du système, y compris les pilotes matériels, les appels système et les événements du noyau. Ils sont stockés dans le fichier `/var/log/kern.log`. Par exemple, les journaux du noyau peuvent révéler la présence de pilotes vulnérables ou obsolètes qui pourraient être ciblés par des attaquants pour accéder au système. Ils peuvent également fournir des informations sur les plantages du système, les limitations de ressources et d'autres événements qui pourraient conduire à un déni de service (denial of service) ou à d'autres problèmes de sécurité. De plus, les journaux du noyau peuvent nous aider à identifier des appels système suspects ou d'autres activités qui pourraient indiquer la présence de logiciels malveillants (malware) ou d'autres logiciels malicieux sur le système. En surveillant le fichier `/var/log/kern.log`, nous pouvons détecter tout comportement inhabituel et prendre les mesures appropriées pour éviter d'autres dommages au système.

## Journaux système

Ces journaux contiennent des informations sur les événements au niveau du système, tels que les démarrages et arrêts de services, les tentatives de connexion et les redémarrages du système. Ils sont stockés dans le fichier `/var/log/syslog`. En analysant les tentatives de connexion, les démarrages et arrêts de services et d'autres événements au niveau du système, nous pouvons détecter tout accès ou activité possible sur le système. Cela peut nous aider à identifier les vulnérabilités qui pourraient être exploitées et à recommander des mesures de sécurité pour atténuer ces risques. De plus, nous pouvons utiliser le `syslog` pour identifier les problèmes potentiels qui pourraient impacter la disponibilité ou les performances du système, tels que des échecs de démarrage de service ou des redémarrages du système. Voici un exemple de ce à quoi un tel fichier `syslog` pourrait ressembler :

## Syslog

```text
Feb 28 2023 15:00:01 server CRON[2715]: (root) CMD (/usr/local/bin/backup.sh)
Feb 28 2023 15:04:22 server sshd[3010]: Failed password for htb-student from 10.14.15.2 port 50223 ssh2
Feb 28 2023 15:05:02 server kernel: [  138.303596] ata3.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x6 frozen
Feb 28 2023 15:06:43 server apache2[2904]: 127.0.0.1 - - [28/Feb/2023:15:06:43 +0000] "GET /index.html HTTP/1.1" 200 13484 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
Feb 28 2023 15:07:19 server sshd[3010]: Accepted password for htb-student from 10.14.15.2 port 50223 ssh2
Feb 28 2023 15:09:54 server kernel: [  367.543975] EXT4-fs (sda1): re-mounted. Opts: errors=remount-ro
Feb 28 2023 15:12:07 server systemd[1]: Started Clean PHP session files.
```

## Journaux d'authentification

Ces journaux contiennent des informations sur les tentatives d'authentification des utilisateurs, y compris les tentatives réussies et échouées. Ils sont stockés dans le fichier `/var/log/auth.log`. Il est important de noter que bien que le fichier `/var/log/syslog` puisse contenir des informations de connexion similaires, le fichier `/var/log/auth.log` se concentre spécifiquement sur les tentatives d'authentification des utilisateurs, ce qui en fait une ressource plus précieuse pour identifier les menaces de sécurité potentielles. Par conséquent, il est essentiel pour les testeurs d'intrusion d'examiner les journaux stockés dans le fichier `/var/log/auth.log` pour s'assurer que le système est sécurisé et n'a pas été compromis.

## Auth.log

```text
Feb 28 2023 18:15:01 sshd[5678]: Accepted publickey for admin from 10.14.15.2 port 43210 ssh2: RSA SHA256:+KjEzN2cVhIW/5uJpVX9n5OB5zVJ92FtCZxVzzcKjw
Feb 28 2023 18:15:03 sudo:   admin : TTY=pts/1 ; PWD=/home/admin ; USER=root ; COMMAND=/bin/bash
Feb 28 2023 18:15:05 sudo:   admin : TTY=pts/1 ; PWD=/home/admin ; USER=root ; COMMAND=/usr/bin/apt-get install netcat-traditional
Feb 28 2023 18:15:08 sshd[5678]: Disconnected from 10.14.15.2 port 43210 [preauth]
Feb 28 2023 18:15:12 kernel: [  778.941871] firewall: unexpected traffic allowed on port 22
Feb 28 2023 18:15:15 auditd[9876]: Audit daemon started successfully
Feb 28 2023 18:15:18 systemd-logind[1234]: New session 4321 of user admin.
Feb 28 2023 18:15:21 CRON[2345]: pam_unix(cron:session): session opened for user root by (uid=0)
Feb 28 2023 18:15:24 CRON[2345]: pam_unix(cron:session): session closed for user root
```

Dans cet exemple, nous pouvons voir à la première ligne qu'une clé publique (public key) a été utilisée avec succès pour l'authentification de l'utilisateur `admin`. De plus, nous pouvons voir que cet utilisateur fait partie du groupe `sudoers` car il peut exécuter des commandes en utilisant `sudo`. Le message du noyau indique que du trafic inattendu a été autorisé sur le port 22, ce qui pourrait indiquer une faille de sécurité potentielle. Après cela, nous voyons qu'une nouvelle session a été créée pour l'utilisateur "admin" par `systemd-logind` et qu'une session `cron` a été ouverte et fermée pour l'utilisateur `root`.

## Journaux d'application

Ces journaux contiennent des informations sur les activités d'applications spécifiques s'exécutant sur le système. Ils sont souvent stockés dans leurs propres fichiers, tels que `/var/log/apache2/error.log` pour le serveur web Apache ou `/var/log/mysql/error.log` pour le serveur de base de données MySQL. Ces journaux sont particulièrement importants lorsque nous ciblons des applications spécifiques, telles que des serveurs web ou des bases de données, car ils peuvent fournir des informations sur la manière dont ces applications traitent et gèrent les données. En examinant ces journaux, nous pouvons identifier des vulnérabilités ou des mauvaises configurations potentielles. Par exemple, les journaux d'accès (access logs) peuvent être utilisés pour suivre les requêtes adressées à un serveur web, tandis que les journaux d'audit (audit logs) peuvent être utilisés pour suivre les modifications apportées au système ou à des fichiers spécifiques. Ces journaux peuvent être utilisés pour identifier les tentatives d'accès non autorisé, l'exfiltration de données (data exfiltration) ou toute autre activité suspecte.

De plus, les journaux d'accès et d'audit sont des journaux critiques qui enregistrent des informations sur les actions des utilisateurs et des processus sur le système. Ils sont cruciaux à des fins de sécurité et de conformité, et nous pouvons les utiliser pour identifier des problèmes de sécurité potentiels et des vecteurs d'attaque (attack vectors).

Par exemple, les `access logs` conservent un enregistrement de l'activité des utilisateurs et des processus sur le système, y compris les tentatives de connexion, les accès aux fichiers et les connexions réseau. Les `Audit logs` enregistrent des informations sur les événements pertinents pour la sécurité sur le système, tels que les modifications des fichiers de configuration du système ou les tentatives de modification des fichiers ou des paramètres du système. Ces journaux aident à suivre les attaques et activités potentielles ou à identifier les failles de sécurité ou d'autres problèmes. Une entrée d'exemple dans un fichier journal d'accès peut ressembler à ce qui suit :

## Access Log Entry

```text
2023-03-07T10:15:23+00:00 servername privileged.sh: htb-student accessed /root/hidden/api-keys.txt
```

Dans cette entrée de journal, nous pouvons voir que l'utilisateur `htb-student` a utilisé le script `privileged.sh` pour accéder au fichier `api-keys.txt` dans le répertoire `/root/hidden/`. Sur les systèmes Linux, la plupart des services courants ont des emplacements par défaut pour les journaux d'accès :

|**Service**|**Description**|
|---|---|
|`Apache`|Les journaux d'accès sont stockés dans le fichier /var/log/apache2/access.log (ou similaire, selon la distribution).|
|`Nginx`|Les journaux d'accès sont stockés dans le fichier /var/log/nginx/access.log (ou similaire).|
|`OpenSSH`|Les journaux d'accès sont stockés dans le fichier /var/log/auth.log sur Ubuntu et dans /var/log/secure sur CentOS/RHEL.|
|`MySQL`|Les journaux d'accès sont stockés dans le fichier /var/log/mysql/mysql.log.|
|`PostgreSQL`|Les journaux d'accès sont stockés dans le fichier /var/log/postgresql/postgresql-version-main.log.|
|`Systemd`|Les journaux d'accès sont stockés dans le répertoire /var/log/journal/.|

## Journaux de sécurité

Ces journaux de sécurité et leurs événements sont souvent enregistrés dans divers fichiers journaux, en fonction de l'application ou de l'outil de sécurité spécifique utilisé. Par exemple, l'application Fail2ban enregistre les tentatives de connexion échouées dans le fichier `/var/log/fail2ban.log`, tandis que le pare-feu UFW enregistre l'activité dans le fichier `/var/log/ufw.log`. D'autres événements liés à la sécurité, tels que les modifications des fichiers ou des paramètres du système, peuvent être enregistrés dans des journaux système plus généraux tels que `/var/log/syslog` ou `/var/log/auth.log`. En tant que testeurs d'intrusion, nous pouvons utiliser des outils et des techniques d'analyse de journaux pour rechercher des événements spécifiques ou des schémas d'activité qui peuvent indiquer un problème de sécurité et utiliser ces informations pour tester plus en profondeur le système à la recherche de vulnérabilités ou de vecteurs d'attaque potentiels.

Il est important de connaître les emplacements par défaut des journaux d'accès et autres fichiers journaux sur les systèmes Linux, car ces informations peuvent être utiles lors de la réalisation d'une évaluation de la sécurité ou d'un test d'intrusion. En comprenant comment les événements liés à la sécurité sont enregistrés et stockés, nous pouvons analyser plus efficacement les données des journaux et identifier les problèmes de sécurité potentiels.

Tous ces journaux peuvent être consultés et analysés à l'aide de divers outils, y compris les visionneuses de fichiers journaux intégrées à la plupart des environnements de bureau Linux, ainsi que des outils en ligne de commande tels que les commandes `tail`, `grep` et `sed`. Une analyse appropriée des journaux système peut aider à identifier et à résoudre les problèmes du système, ainsi qu'à détecter les failles de sécurité et autres événements d'intérêt.

---

← [[27 - Configuration du pare-feu]] | [[00 - Sommaire Linux|Sommaire]] | [[29 - Solaris]] →
