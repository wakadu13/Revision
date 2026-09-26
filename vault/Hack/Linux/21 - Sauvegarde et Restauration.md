---
tags:
  - linux
ordre: 21
---

# Sauvegarde et Restauration

Les systèmes Linux fournissent une gamme d'outils puissants pour la sauvegarde (backup) et la restauration (restore) de données, conçus pour être à la fois efficaces et sécurisés. Ces outils permettent de s'assurer que nos données sont non seulement protégées contre la perte ou la corruption, mais aussi facilement accessibles lorsque nous en avons besoin.

Lors de la sauvegarde de données sur un système Ubuntu, nous avons plusieurs options, notamment :

- Rsync
- Deja Dup
- Duplicity

Rsync est un outil open-source qui permet des sauvegardes rapides et sécurisées, que ce soit localement ou vers un emplacement distant. L'un de ses principaux avantages est qu'il ne transfère que les portions de fichiers qui ont été modifiées, ce qui le rend très efficace pour traiter de grandes quantités de données. Rsync est particulièrement utile pour les transferts réseau, comme la synchronisation de fichiers entre serveurs ou la création de sauvegardes incrémentielles (incremental backups) sur Internet.

Duplicity est un autre outil puissant qui s'appuie sur Rsync, mais qui ajoute des fonctionnalités de chiffrement (encryption) pour protéger les sauvegardes. Il vous permet de chiffrer vos copies de sauvegarde, garantissant que les données sensibles restent sécurisées même si elles sont stockées sur des serveurs distants, des sites FTP ou des services cloud comme Amazon S3. Duplicity offre une couche de sécurité supplémentaire tout en conservant les capacités de transfert de données efficaces de Rsync.

Considérez vos données comme des trésors de grande valeur stockés dans une maison. Les outils de sauvegarde sur Linux, tels que Rsync, Duplicity et Deja Dup, agissent comme différents types de coffres-forts. Rsync est comme un transporteur rapide qui ne déplace que ce qui est nouveau ou a changé, ce qui en fait le moyen idéal pour envoyer des mises à jour vers une chambre forte distante. Duplicity est un coffre-fort de haute sécurité qui non seulement stocke le trésor, mais le verrouille également avec un code complexe, garantissant que personne d'autre ne peut y accéder. Deja Dup est un coffre-fort simple et accessible que tout le monde peut utiliser, tout en offrant le même niveau de protection. Chiffrer vos sauvegardes ajoute un verrou supplémentaire à votre coffre-fort, garantissant que même si quelqu'un le trouve, il ne pourra pas l'ouvrir.

Pour les utilisateurs qui préfèrent une option plus simple et conviviale, Deja Dup offre une interface graphique qui rend le processus de sauvegarde simple. En arrière-plan, il utilise également Rsync et, comme Duplicity, il prend en charge les sauvegardes chiffrées (encrypted backups). Deja Dup est idéal pour les utilisateurs qui souhaitent un accès rapide et facile aux options de sauvegarde et de restauration sans avoir à se plonger dans la ligne de commande.

Assurer la sécurité de vos sauvegardes est tout aussi important que de les créer. Le chiffrement de vos données de sauvegarde aide à les protéger contre les accès non autorisés, offrant la tranquillité d'esprit que les informations sensibles restent protégées. Sur les systèmes Ubuntu, vous pouvez utiliser des outils de chiffrement supplémentaires comme GnuPG, eCryptfs ou LUKS pour ajouter une autre couche de protection à vos sauvegardes.

La sauvegarde et la restauration des données sont une pratique essentielle pour quiconque travaille avec Ubuntu. En utilisant des outils comme Rsync, Duplicity et Deja Dup, vous pouvez vous assurer que vos données sont stockées en toute sécurité et facilement récupérables, vous donnant l'assurance qu'en cas de perte de données inattendue, vos informations pourront être restaurées rapidement et de manière fiable.

Pour installer Rsync sur Ubuntu, nous pouvons utiliser le gestionnaire de paquets (package manager) `apt` :

### Installer Rsync

```bash
Hiterof13@htb[/htb]$ sudo apt install rsync -y
```

Cela installera la dernière version de Rsync sur le système. Une fois l'installation terminée, nous pouvons commencer à utiliser l'outil pour sauvegarder et restaurer des données. Pour sauvegarder un répertoire entier avec `rsync`, nous pouvons utiliser la commande suivante :

### Rsync - Sauvegarder un répertoire local sur notre serveur de sauvegarde

```bash
Hiterof13@htb[/htb]$ rsync -av /path/to/mydirectory user@backup_server:/path/to/backup/directory
```

Cette commande copiera l'intégralité du répertoire (`/path/to/mydirectory`) vers un hôte distant (`backup_server`), dans le répertoire `/path/to/backup/directory`. L'option `archive` (`-a`) est utilisée pour préserver les attributs originaux des fichiers, tels que les permissions, les horodatages, etc., et l'utilisation de l'option `verbose` (`-v`) fournit une sortie détaillée de la progression de l'opération `rsync`.

Nous pouvons également ajouter des options supplémentaires pour personnaliser le processus de sauvegarde, comme l'utilisation de la compression et des sauvegardes incrémentielles. Nous pouvons le faire comme suit :

```bash
Hiterof13@htb[/htb]$ rsync -avz --backup --backup-dir=/path/to/backup/folder --delete /path/to/mydirectory user@backup_server:/path/to/backup/directory
```

Avec cette commande, nous sauvegardons le répertoire `mydirectory` sur le serveur distant `backup_server`, en préservant les attributs, horodatages et permissions d'origine des fichiers, et en activant la compression (`-z`) pour des transferts plus rapides. L'option `--backup` crée des sauvegardes incrémentielles dans le répertoire `/path/to/backup/folder`, et l'option `--delete` supprime de l'hôte distant les fichiers qui ne sont plus présents dans le répertoire source.

Si nous voulons restaurer notre répertoire depuis notre serveur de sauvegarde vers notre répertoire local, nous pouvons utiliser la commande suivante :

### Rsync - Restaurer notre sauvegarde

```bash
Hiterof13@htb[/htb]$ rsync -av user@remote_host:/path/to/backup/directory /path/to/mydirectory
```

---

## Rsync chiffré

Pour garantir la sécurité de notre transfert de fichiers `rsync` entre notre hôte local et notre serveur de sauvegarde, nous pouvons combiner l'utilisation de SSH et d'autres mesures de sécurité. En utilisant SSH, nous sommes en mesure de chiffrer nos données pendant leur transfert, ce qui rend leur accès beaucoup plus difficile pour toute personne non autorisée. De plus, nous pouvons également utiliser des pare-feux et d'autres protocoles de sécurité pour garantir que nos données restent sûres et sécurisées pendant le transfert. En prenant ces mesures, nous pouvons être sûrs que nos données sont protégées et que notre transfert de fichiers est sécurisé. Par conséquent, nous indiquons à `rsync` d'utiliser SSH comme suit :

### Transfert sécurisé de notre sauvegarde

```bash
Hiterof13@htb[/htb]$ rsync -avz -e ssh /path/to/mydirectory user@backup_server:/path/to/backup/directory
```

Le transfert de données entre notre hôte local et le serveur de sauvegarde s'effectue via la connexion SSH chiffrée, qui assure la confidentialité et la protection de l'intégrité des données transférées. Ce processus de chiffrement garantit que les données sont protégées contre tout acteur malveillant potentiel qui pourrait autrement y accéder et les modifier sans autorisation. La clé de chiffrement elle-même est également protégée par un ensemble complet de protocoles de sécurité, ce qui rend encore plus difficile pour toute personne non autorisée d'accéder aux données. De plus, la connexion chiffrée est conçue pour être très résistante à toute tentative de violation de la sécurité, ce qui nous permet d'avoir confiance dans la protection des données transférées.

---

## Synchronisation automatique

Pour activer la synchronisation automatique avec `rsync`, vous pouvez utiliser une combinaison de `cron` et `rsync` pour automatiser le processus de synchronisation. La planification de la tâche cron (cron job) pour qu'elle s'exécute à intervalles réguliers garantit que le contenu des deux systèmes reste synchronisé. Cela peut être particulièrement bénéfique pour les organisations qui ont besoin de maintenir leurs données synchronisées sur plusieurs machines. De plus, la mise en place d'une synchronisation automatique avec `rsync` peut être un excellent moyen d'économiser du temps et des efforts, car elle élimine le besoin de synchronisation manuelle. Elle aide également à garantir que les fichiers et les données stockés dans les systèmes sont maintenus à jour et cohérents, ce qui contribue à réduire les erreurs et à améliorer l'efficacité.

Par conséquent, nous créons un nouveau script appelé `RSYNC_Backup.sh`, qui déclenchera la commande `rsync` pour synchroniser notre répertoire local avec le répertoire distant. Cependant, comme nous utilisons un script pour effectuer la connexion SSH pour rsync, nous devons configurer une authentification par clé (key-based authentication). Cela permet d'éviter d'avoir à saisir notre mot de passe lors de la connexion avec SSH.

Tout d'abord, nous générons une paire de clés pour notre utilisateur.

```bash
Hiterof13@htb[/htb]$ ssh-keygen -t rsa -b 2048
```

Suivez les invites pour spécifier l'emplacement (par défaut `~/.ssh/id_rsa`) et fournir éventuellement une phrase de passe (laissez-la vide pour ne pas en avoir). Ensuite, nous devons copier notre clé publique (public key) sur le serveur distant.

```bash
Hiterof13@htb[/htb]$ ssh-copy-id user@backup_server
```

Maintenant, nous pouvons créer notre script pour automatiser la sauvegarde rsync.

### RSYNC_Backup.sh

```bash
#!/bin/bash

rsync -avz -e ssh /path/to/mydirectory user@backup_server:/path/to/backup/directory
```

Ensuite, afin de s'assurer que le script puisse s'exécuter correctement, nous devons lui donner les permissions nécessaires. De plus, il est également important de s'assurer que le script appartient au bon utilisateur, car cela garantira que seul le bon utilisateur a accès au script et que le script n'est pas modifié par un autre utilisateur.

```bash
Hiterof13@htb[/htb]$ chmod +x RSYNC_Backup.sh
```

Après cela, nous pouvons créer un crontab qui indique à `cron` d'exécuter le script toutes les heures à la minute 0.

```bash
Hiterof13@htb[/htb]$ crontab -e
```

Nous pouvons ajuster la planification en fonction de nos besoins. Pour ce faire, le crontab doit avoir le contenu suivant :

### Synchronisation automatique - Crontab

```bash
0 * * * * /path/to/RSYNC_Backup.sh
```

Avec cette configuration, `cron` sera responsable de l'exécution du script à l'intervalle souhaité, garantissant que la commande `rsync` est exécutée et que le contenu du répertoire local est synchronisé avec l'hôte distant.

Nous vous encourageons à essayer rsync en utilisant Pwnbox. Au lieu de synchroniser des fichiers avec un serveur distant, vous pouvez utiliser Pwnbox à la fois comme source et comme destination, ce qui simplifie les tests. Pour ce faire, créez deux répertoires sur Pwnbox :

1. `to_backup` (où vos données originales sont stockées) et un autre appelé
2. `synced_backup` (où les données synchronisées seront copiées)

Vous transférerez ensuite les données du répertoire `to_backup` vers le répertoire `synced_backup` à l'aide de `rsync`. Pour automatiser ce processus, configurez une tâche `cron` qui s'exécute chaque minute pour assurer une synchronisation continue. N'oubliez pas, comme nous testons cela localement, nous pouvons utiliser l'adresse IP de boucle locale (loopback IP address) 127.0.0.1 comme adresse pour l'hôte « distant »

---

← [[20 - Travailler avec les services web]] | [[00 - Sommaire Linux|Sommaire]] | [[22 - Gestion des systèmes de fichiers]] →
