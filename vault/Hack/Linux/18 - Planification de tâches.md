---
tags:
  - linux
ordre: 18
---

# Planification de tâches

La planification de tâches (task scheduling) est une fonctionnalité essentielle des systèmes Linux qui permet aux utilisateurs et aux administrateurs d'automatiser des tâches en les exécutant à des moments précis ou à des intervalles réguliers, éliminant ainsi le besoin d'une intervention manuelle. Disponible dans des distributions comme Ubuntu, Red Hat Linux et Solaris, cette fonctionnalité gère un large éventail de tâches telles que les mises à jour logicielles automatiques, l'exécution de scripts, la maintenance de bases de données et l'automatisation des sauvegardes. En planifiant des tâches régulières et répétitives, elle garantit leur exécution de manière cohérente et fiable. De plus, des alertes peuvent être configurées pour notifier les administrateur ou les utilisateurs lorsque certains événements se produisent. Bien qu'il existe de nombreuses applications pour ce type d'automatisation, ces exemples représentent les cas d'usage les plus courants.

La planification de tâches en général est comparable au réglage d'une machine à café ou à thé pour qu'elle prépare la boisson automatiquement chaque matin. Une fois programmée, elle prépare le café ou le thé à l'heure souhaitée sans autre intervention, garantissant qu'une tasse fraîche soit prête lorsque vous en avez besoin.

Comprendre la planification de tâches dans les systèmes Linux est essentiel pour nous, en tant que spécialistes de la cybersécurité et testeurs d'intrusion (penetration testers), car elle peut servir à la fois d'outil administratif légitime et de vecteur d'activité malveillante. La connaissance de la manière dont les tâches sont automatisées vous permet d'identifier les risques de sécurité potentiels, tels que des tâches Cron non autorisées qui exécutent des scripts malveillants ou maintiennent des portes dérobées (backdoors) persistantes à des intervalles planifiés. En comprenant les subtilités de la planification de tâches, vous pouvez détecter et analyser ces menaces cachées, améliorer les audits de système (system audits) et même utiliser des tâches planifiées pour simuler des scénarios d'attaque lors de tests d'intrusion.

---

## Systemd

Systemd est un service utilisé dans les systèmes Linux tels qu'Ubuntu, Redhat Linux et Solaris pour démarrer des processus et des scripts à un moment précis. Avec lui, nous pouvons configurer des processus et des scripts pour qu'ils s'exécutent à une heure ou un intervalle de temps spécifique, et nous pouvons également spécifier des événements et des déclencheurs particuliers qui lanceront une tâche donnée. Pour ce faire, nous devons suivre quelques étapes et prendre certaines précautions avant que nos scripts ou processus ne soient exécutés automatiquement par le système.

1. Créer un timer (planifie quand votre `mytimer.service` doit s'exécuter)
2. Créer un service (exécute les commandes ou le script)
3. Activer le timer

### Créer un timer

Pour créer un timer pour systemd, nous devons créer un répertoire où le script du timer sera stocké.

```bash
Hiterof13@htb[/htb]$ sudo mkdir /etc/systemd/system/mytimer.timer.d
Hiterof13@htb[/htb]$ sudo vim /etc/systemd/system/mytimer.timer
```

Ensuite, nous devons créer un script qui configure le timer. Le script doit contenir les options suivantes : « Unit », « Timer » et « Install ». L'option « Unit » spécifie une description pour le timer. L'option « Timer » spécifie quand démarrer le timer et quand l'activer. Enfin, l'option « Install » spécifie où installer le timer.

### Mytimer.timer

```ini
[Unit]
Description=My Timer

[Timer]
OnBootSec=3min
OnUnitActiveSec=1hour

[Install]
WantedBy=timers.target
```

Ici, cela dépend de la manière dont nous voulons utiliser notre script. Par exemple, si nous voulons exécuter notre script une seule fois après le démarrage du système, nous devrions utiliser le paramètre `OnBootSec` dans `Timer`. Cependant, si nous voulons que notre script s'exécute régulièrement, nous devrions alors utiliser `OnUnitActiveSec` pour que le système exécute le script à des intervalles réguliers. Ensuite, nous devons créer notre `service`.

### Créer un service

```bash
Hiterof13@htb[/htb]$ sudo vim /etc/systemd/system/mytimer.service
```

Ici, nous définissons une description et spécifions le chemin complet vers le script que nous voulons exécuter. Le « multi-user.target » est l'unité système qui est activée lors du démarrage en mode multi-utilisateur normal. Il définit les services qui doivent être démarrés lors d'un démarrage normal du système.

```ini
[Unit]
Description=My Service

[Service]
ExecStart=/full/path/to/my/script.sh

[Install]
WantedBy=multi-user.target
```

Après cela, nous devons demander à `systemd` de relire les dossiers pour inclure les changements.

### Recharger Systemd

```bash
Hiterof13@htb[/htb]$ sudo systemctl daemon-reload
```

Après cela, nous pouvons utiliser `systemctl` pour `start` le service manuellement et `enable` le démarrage automatique.

### Démarrer le timer & le service

```bash
Hiterof13@htb[/htb]$ sudo systemctl start mytimer.timer
Hiterof13@htb[/htb]$ sudo systemctl enable mytimer.timer
```

De cette façon, `mytimer.service` sera lancé automatiquement selon les intervalles (ou délais) que vous avez définis dans `mytimer.timer`.

---

## Cron

Cron est un autre outil qui peut être utilisé dans les systèmes Linux pour planifier et automatiser des processus. Il permet aux utilisateurs et aux administrateurs d'exécuter des tâches à une heure spécifique ou à des intervalles spécifiques. Pour les exemples ci-dessus, nous pouvons également utiliser Cron pour automatiser les mêmes tâches. Nous avons juste besoin de créer un script, puis de dire au démon cron de l'appeler à un moment précis.

Avec Cron, nous pouvons automatiser les mêmes tâches, mais le processus de configuration du démon Cron est un peu différent de celui de Systemd. Pour configurer le démon cron, nous devons stocker les tâches dans un fichier appelé `crontab`, puis indiquer au démon quand exécuter les tâches. Ensuite, nous pouvons planifier et automatiser les tâches en configurant le démon cron en conséquence. La structure de Cron se compose des éléments suivants :

|**Échelle de temps**|**Description**|
|---|---|
|Minutes (0-59)|Spécifie la minute à laquelle la tâche doit être exécutée.|
|Heures (0-23)|Spécifie l'heure à laquelle la tâche doit être exécutée.|
|Jours du mois (1-31)|Spécifie le jour du mois où la tâche doit être exécutée.|
|Mois (1-12)|Spécifie le mois au cours duquel la tâche doit être exécutée.|
|Jours de la semaine (0-7)|Spécifie le jour de la semaine où la tâche doit être exécutée.|

Par exemple, un tel crontab pourrait ressembler à ceci :

```text
# System Update
0 */6 * * * /path/to/update_software.sh

# Execute Scripts
0 0 1 * * /path/to/scripts/run_scripts.sh

# Cleanup DB
0 0 * * 0 /path/to/scripts/clean_database.sh

# Backups
0 0 * * 7 /path/to/scripts/backup.sh
```

La première tâche, `System Update`, doit être exécutée toutes les six heures. Ceci est indiqué par l'entrée `0 */6` dans la colonne des heures. La tâche est exécutée par le script `update_software.sh`, dont le chemin est indiqué dans la dernière colonne.

La deuxième tâche, `Execute Scripts`, doit être exécutée chaque premier jour du mois à minuit. Ceci est indiqué par les entrées `0` et `0` dans les colonnes des minutes et des heures et `1` dans la colonne des jours du mois. La tâche est exécutée par le script `run_scripts.sh`, dont le chemin est indiqué dans la dernière colonne.

La troisième tâche, `Cleanup DB`, doit être exécutée tous les dimanches à minuit. Ceci est spécifié par les entrées `0` et `0` dans les colonnes des minutes et des heures et `0` dans la colonne des jours de la semaine. La tâche est exécutée par le script `clean_database.sh`, dont le chemin est indiqué dans la dernière colonne.

La quatrième tâche, `Backups`, doit être exécutée tous les dimanches à minuit. Ceci est indiqué par les entrées `0` et `0` dans les colonnes des minutes et des heures et `7` dans la colonne des jours de la semaine. La tâche est exécutée par le script `backup.sh`, dont le chemin est indiqué dans la dernière colonne.

Il est également possible de recevoir des notifications lorsqu'une tâche est exécutée avec succès ou non. De plus, nous pouvons créer des journaux (logs) pour surveiller l'exécution des tâches.

---

## Systemd vs. Cron

Systemd et Cron sont deux outils qui peuvent être utilisés dans les systèmes Linux pour planifier et automatiser des processus. La principale différence entre ces deux outils réside dans leur configuration. Avec Systemd, vous devez créer un script de timer et de service qui indique au système d'exploitation quand exécuter les tâches. D'un autre côté, avec Cron, vous devez créer un fichier `crontab` qui indique au démon cron quand exécuter les tâches.

---

← [[17 - Gestion des services et des processus]] | [[00 - Sommaire Linux|Sommaire]] | [[19 - Services Réseau]] →
