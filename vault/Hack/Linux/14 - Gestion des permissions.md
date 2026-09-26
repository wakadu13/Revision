---
tags:
  - linux
ordre: 14
---

# Gestion des permissions

Sous Linux, les permissions sont comme des clés qui contrôlent l'accès aux fichiers et aux répertoires. Ces permissions sont attribuées à la fois aux utilisateurs et aux groupes, un peu comme des clés seraient distribuées à des individus et des équipes spécifiques au sein d'une organisation. Chaque utilisateur peut appartenir à plusieurs groupes, et faire partie d'un groupe accorde des droits d'accès supplémentaires, permettant aux utilisateurs d'effectuer des actions spécifiques sur les fichiers et les répertoires.

Chaque fichier et répertoire a un propriétaire (un utilisateur) et est associé à un groupe. Les permissions pour ces fichiers sont définies à la fois pour le propriétaire et le groupe, déterminant quelles actions — comme la lecture, l'écriture ou l'exécution — sont autorisées. Lorsque vous créez un nouveau fichier ou répertoire, il devient automatiquement « le vôtre » et est associé au groupe auquel vous appartenez, de la même manière qu'un projet au sein d'une entreprise pourrait être placé par défaut sous la supervision de votre équipe.

En substance, les permissions Linux agissent comme un ensemble de règles ou de clés qui dictent qui peut accéder ou modifier certaines ressources, garantissant la sécurité et une collaboration adéquate à travers le système.

Lorsqu'un utilisateur veut accéder au contenu d'un répertoire Linux, c'est comme déverrouiller une porte avant d'entrer. Pour « traverser » ou naviguer dans un répertoire, l'utilisateur doit d'abord avoir la bonne clé — cette clé est la permission d'`exécution` (`execute`) sur le répertoire. Sans elle, même si le contenu du répertoire est visible pour l'utilisateur, il ne pourra pas y entrer ou le parcourir.

En d'autres termes, avoir la permission d'`exécution` sur un répertoire, c'est comme avoir l'autorisation de traverser un couloir pour accéder aux pièces à l'intérieur. Cela ne vous permet pas de voir ou de modifier ce qui se trouve à l'intérieur, mais cela vous accorde la capacité d'entrer et d'explorer la structure du répertoire. Sans cette permission, l'utilisateur ne peut pas accéder au contenu du répertoire et recevra à la place un message d'erreur « `Permission Denied` ».

```bash
cry0l1t3@htb[/htb]$ ls -l
drw-rw-r-- 3 cry0l1t3 cry0l1t3   4096 Jan 12 12:30 scripts
cry0l1t3@htb[/htb]$ ls -al mydirectory/
ls: cannot access 'mydirectory/script.sh': Permission denied
ls: cannot access 'mydirectory/..': Permission denied
ls: cannot access 'mydirectory/subdirectory': Permission denied
ls: cannot access 'mydirectory/.': Permission denied
total 0
d????????? ? ? ? ?            ? .
d????????? ? ? ? ?            ? ..
-????????? ? ? ? ?            ? script.sh
d????????? ? ? ? ?            ? subdirectory
```

Il est important de noter que la permission d'`exécution` est nécessaire pour traverser un répertoire, quel que soit le niveau d'accès de l'utilisateur. De plus, la permission d'`exécution` sur un répertoire ne permet pas à un utilisateur d'exécuter ou de modifier les fichiers ou le contenu à l'intérieur du répertoire, mais seulement de traverser et d'accéder au contenu du répertoire.

Pour exécuter des fichiers à l'intérieur du répertoire, un utilisateur a besoin de la permission d'`exécution` sur le fichier correspondant. Pour modifier le contenu d'un répertoire (créer, supprimer ou renommer des fichiers et des sous-répertoires), l'utilisateur a besoin de la permission d'`écriture` (`write`) sur le répertoire.

L'ensemble du système de permissions sur les systèmes Linux est basé sur le système de numération octal, et fondamentalement, il existe trois types de permissions différents qui peuvent être attribués à un fichier ou à un répertoire :

- (`r`) - Lecture (Read)
- (`w`) - Écriture (Write)
- (`x`) - Exécution (Execute)

Les permissions peuvent être définies pour le `propriétaire` (`owner`), le `groupe` (`group`) et les `autres` (`others`), comme présenté dans l'exemple suivant avec leurs permissions correspondantes.

```bash
cry0l1t3@htb[/htb]$ ls -l /etc/passwd
- rwx rw- r--   1 root root 1641 May  4 23:42 /etc/passwd
- --- --- ---   |  |    |    |   |__________|
|  |   |   |    |  |    |    |        |_ Date
|  |   |   |    |  |    |    |__________ Taille du fichier
|  |   |   |    |  |    |_______________ Groupe
|  |   |   |    |  |____________________ Utilisateur
|  |   |   |    |_______________________ Nombre de liens physiques
|  |   |   |_ Permissions des autres (lecture)
|  |   |_____ Permissions du groupe (lecture, écriture)
|  |_________ Permissions du propriétaire (lecture, écriture, exécution)
|____________ Type de fichier (- = Fichier, d = Répertoire, l = Lien, ... )
```

---

## Modifier les permissions

Nous pouvons modifier les permissions en utilisant la commande `chmod`, les références de groupe de permission (`u` - propriétaire, `g` - Groupe, `o` - autres, `a` - Tous les utilisateurs), et soit un `+` soit un `-` pour ajouter ou supprimer les permissions désignées. Dans l'exemple suivant, supposons que nous ayons un fichier nommé `shell` et que nous voulions en changer les permissions afin que ce script appartienne à cet utilisateur, ne soit pas exécutable, et soit défini avec les permissions de lecture/écriture pour tous les utilisateurs.

```bash
cry0l1t3@htb[/htb]$ ls -l shell
-rwxr-x--x   1 cry0l1t3 htbteam 0 May  4 22:12 shell
```

Nous pouvons alors appliquer la permission de `lecture` pour tous les utilisateurs et voir le résultat.

```bash
cry0l1t3@htb[/htb]$ chmod a+r shell && ls -l shell
-rwxr-xr-x   1 cry0l1t3 htbteam 0 May  4 22:12 shell
```

Nous pouvons également définir les permissions pour tous les autres utilisateurs en `lecture` seule en utilisant l'assignation de valeur octale.

```bash
cry0l1t3@htb[/htb]$ chmod 754 shell && ls -l shell
-rwxr-xr--   1 cry0l1t3 htbteam 0 May  4 22:12 shell
```

Examinons toutes les représentations associées pour mieux comprendre comment l'attribution des permissions est calculée.

```text
Notation binaire :                4 2 1  |  4 2 1  |  4 2 1
----------------------------------------------------------
Représentation binaire :          1 1 1  |  1 0 1  |  1 0 0
----------------------------------------------------------
Valeur octale :                     7    |    5    |    4
----------------------------------------------------------
Représentation des permissions :  r w x  |  r - x  |  r - -
```

Si nous additionnons les bits définis de la `Représentation binaire` assignés aux valeurs de la `Notation binaire`, nous obtenons la `Valeur octale`. La `Représentation des permissions` représente les bits définis dans la `Représentation binaire` en utilisant les trois caractères, ce qui facilite simplement la reconnaissance des permissions définies.

---

## Changer de propriétaire

Pour changer le propriétaire et/ou les attributions de groupe d'un fichier ou d'un répertoire, nous pouvons utiliser la commande `chown`. La syntaxe est la suivante :

### Syntaxe - chown

```bash
cry0l1t3@htb[/htb]$ chown <user>:<group> <file/directory>
```

Dans cet exemple, « shell » peut être remplacé par n'importe quel fichier ou dossier arbitraire.

```bash
cry0l1t3@htb[/htb]$ chown root:root shell && ls -l shell
-rwxr-xr--   1 root root 0 May  4 22:12 shell
```

---

## SUID & SGID

En plus des permissions standards d'utilisateur et de groupe, Linux nous permet de configurer des permissions spéciales sur les fichiers via les bits `SUID (Set User ID)` et `SGID (Set Group ID)`. Ces bits fonctionnent comme des laissez-passer temporaires, permettant aux utilisateurs d'exécuter certains programmes avec les privilèges d'un autre utilisateur ou groupe. Par exemple, les administrateurs peuvent utiliser `SUID` ou `SGID` pour accorder aux utilisateurs des droits élevés pour des applications spécifiques, permettant d'effectuer des tâches avec les permissions nécessaires, même si l'utilisateur lui-même ne les possède pas normalement.

La présence de ces permissions est indiquée par un `s` à la place du `x` habituel dans l'ensemble des permissions du fichier. Lorsqu'un programme avec le bit SUID ou SGID est exécuté, il s'exécute avec les permissions du propriétaire ou du groupe du fichier, plutôt que celles de l'utilisateur qui l'a lancé. Cela peut être utile pour certaines tâches système mais introduit également des risques de sécurité potentiels s'il n'est pas utilisé avec précaution.

Un risque courant survient lorsque les administrateurs, peu familiers avec toutes les fonctionnalités d'une application, attribuent les bits `SUID` ou `SGID` de manière indiscriminée. Par exemple, si le bit `SUID` est appliqué à un programme comme `journalctl`, qui inclut une fonction pour lancer un shell depuis son interface, tout utilisateur exécutant ce programme pourrait lancer un shell en tant que root. Cela leur confère un contrôle total sur le système, présentant une vulnérabilité de sécurité importante. Plus d'informations à ce sujet et sur d'autres applications de ce type peuvent être trouvées sur [GTFObins](https://gtfobins.github.io/gtfobins/journalctl/).

---

## Sticky Bit

Les sticky bits sous Linux sont comme des verrous sur des fichiers dans des espaces partagés. Lorsqu'il est défini sur un répertoire, le sticky bit ajoute une couche de sécurité supplémentaire, garantissant que seules certaines personnes peuvent modifier ou supprimer des fichiers, même si d'autres ont accès au répertoire.

Imaginez un espace de travail commun où de nombreuses personnes peuvent entrer et utiliser les mêmes outils, mais où chaque personne a son propre tiroir que seule elle (ou le responsable) peut ouvrir. Le sticky bit agit comme une serrure sur ces tiroirs, empêchant quiconque de toucher à leur contenu. Dans un répertoire partagé, cela signifie que seul le propriétaire du fichier, le propriétaire du répertoire ou l'utilisateur root (l'administrateur système) peut supprimer ou renommer des fichiers. Les autres utilisateurs peuvent toujours accéder au répertoire mais ne peuvent pas modifier les fichiers qui ne leur appartiennent pas.

Cette fonctionnalité est particulièrement utile dans les environnements partagés, comme les répertoires publics, où plusieurs utilisateurs travaillent ensemble. En définissant le sticky bit, vous vous assurez que les fichiers importants ne sont pas modifiés accidentellement ou malicieusement par quelqu'un qui ne devrait pas avoir l'autorité de le faire, ajoutant ainsi une protection importante aux espaces de travail collaboratifs.

```bash
cry0l1t3@htb[/htb]$ ls -l
drw-rw-r-t 3 cry0l1t3 cry0l1t3   4096 Jan 12 12:30 scripts
drw-rw-r-T 3 cry0l1t3 cry0l1t3   4096 Jan 12 12:32 reports
```

Dans cet exemple, nous voyons que les deux répertoires ont le sticky bit de défini. Cependant, le dossier `reports` a un `T` majuscule, et le dossier `scripts` a un `t` minuscule.

Si le sticky bit est en majuscule (`T`), cela signifie que tous les autres utilisateurs n'ont pas la permission d'`exécution` (`x`) et, par conséquent, ne peuvent ni voir le contenu du dossier ni y exécuter de programmes. Le sticky bit en minuscule (`t`) est le sticky bit pour lequel la permission d'`exécution` (`x`) a été définie.

---

← [[13 - Expressions régulières]] | [[00 - Sommaire Linux|Sommaire]] | [[15 - Gestion des utilisateurs]] →
