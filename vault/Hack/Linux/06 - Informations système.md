---
tags:
  - linux
ordre: 6
---

# Informations système

Passons maintenant à la pratique pour nous familiariser avec l'utilisation du terminal et du shell. N'oubliez pas que vous pouvez toujours utiliser les commandes `-h`, `--help` ou `man` pour accéder à l'aide si nécessaire.

Puisque nous allons travailler avec différents systèmes Linux, il est important de comprendre leur structure, y compris les détails du système, les processus, les configurations réseau, les utilisateurs/paramètres utilisateur et les répertoires, ainsi que leurs paramètres associés. Vous trouverez ci-dessous une liste d'outils essentiels pour vous aider à recueillir ces informations. La plupart de ces outils sont préinstallés. Cependant, cette connaissance n'est pas seulement cruciale pour les tâches Linux de routine, mais elle joue également un rôle clé lors de l'évaluation des configurations de sécurité, de l'identification des vulnérabilités ou de la prévention des risques de sécurité potentiels dans les systèmes d'exploitation Linux.

|**Commande**|**Description**|
|---|---|
|`whoami`|Affiche le nom d'utilisateur actuel.|
|`id`|Renvoie l'identité de l'utilisateur|
|`hostname`|Définit ou affiche le nom du système hôte actuel.|
|`uname`|Affiche des informations de base sur le nom du système d'exploitation et le matériel du système.|
|`pwd`|Renvoie le nom du répertoire de travail.|
|`ifconfig`|L'utilitaire ifconfig est utilisé pour attribuer ou afficher une adresse à une interface réseau et/ou configurer les paramètres de l'interface réseau.|
|`ip`|Ip est un utilitaire pour afficher ou manipuler le routage, les périphériques réseau, les interfaces et les tunnels.|
|`netstat`|Affiche l'état du réseau.|
|`ss`|Un autre utilitaire pour examiner les sockets.|
|`ps`|Affiche l'état des processus.|
|`who`|Affiche qui est connecté.|
|`env`|Affiche l'environnement ou définit et exécute une commande.|
|`lsblk`|Liste les périphériques de bloc.|
|`lsusb`|Liste les périphériques USB|
|`lsof`|Liste les fichiers ouverts.|
|`lspci`|Liste les périphériques PCI.|

Faisons défiler la page jusqu'en bas, démarrons la machine cible, puis connectons-nous y en utilisant SSH. Ensuite, essayez de suivre et de reproduire autant d'exemples que possible montrés dans cette section.

---

## Connexion via SSH

`Secure Shell` (`SSH`) fait référence à un protocole qui permet aux clients d'accéder et d'exécuter des commandes ou des actions on des ordinateurs distants. Sur les hôtes et les serveurs basés sur Linux, ainsi que sur d'autres systèmes d'exploitation de type Unix, SSH est l'un des outils standard installés en permanence et constitue le choix privilégié de nombreux administrateurs pour configurer et maintenir un ordinateur via un accès à distance (remote access). C'est un protocole plus ancien et très éprouvé qui ne nécessite ni n'offre d'interface utilisateur graphique (GUI). Pour cette raison, il fonctionne de manière très efficace et occupe très peu de ressources. Nous utilisons ce type de connexion dans les sections suivantes, et dans la plupart des autres exercices de laboratoire du module, pour offrir la possibilité d'essayer les commandes et les actions apprises dans un environnement sûr.

Nous pouvons nous connecter à nos cibles avec la commande suivante :

```bash
Hiterof13@htb[/htb]$ ssh htb-student@[IP address]
```

---

Maintenant, examinons quelques exemples sur la machine à laquelle nous venons de nous connecter.

### Hostname

La commande `hostname` est assez explicite et affichera simplement le nom de l'ordinateur auquel nous sommes connectés.

```bash
Hiterof13@htb[/htb]$ hostname
nixfund
```

### Whoami

Cette commande simple et rapide peut être utilisée sur les systèmes Windows et Linux pour obtenir notre nom d'utilisateur actuel. Lors d'une évaluation de sécurité, lorsque nous obtenons un accès par shell inversé (reverse shell) sur un hôte, l'une des premières choses à faire pour prendre conscience de la situation est de déterminer en tant que quel utilisateur nous opérons. À partir de là, nous pouvons déterminer si l'utilisateur dispose de privilèges/accès spéciaux.

```bash
cry0l1t3@htb[/htb]$ whoami
cry0l1t3
```

### Id

La commande `id` complète la commande `whoami` et affiche notre appartenance effective à des groupes et nos identifiants. Cela peut intéresser les testeurs d'intrusion (penetration testers) qui cherchent à voir les accès qu'un utilisateur peut avoir, et les administrateurs système qui cherchent à auditer les permissions de compte et l'appartenance à des groupes. Dans cette sortie, le groupe `hackthebox` est intéressant car il n'est pas standard, le groupe `adm` signifie que l'utilisateur peut lire les fichiers journaux dans `/var/log` et pourrait potentiellement accéder à des informations sensibles, l'appartenance au groupe `sudo` est particulièrement intéressante car cela signifie que notre utilisateur peut exécuter certaines ou toutes les commandes en tant que super-utilisateur `root`. Les droits sudo pourraient nous aider à réaliser une élévation de privilèges (privilege escalation) ou pourraient être un signe pour un administrateur système qu'il doit peut-être auditer les permissions et les appartenances aux groupes pour supprimer tout accès qui n'est pas nécessaire à un utilisateur donné pour effectuer ses tâches quotidiennes.

```bash
cry0l1t3@htb[/htb]$ id
uid=1000(cry0l1t3) gid=1000(cry0l1t3) groups=1000(cry0l1t3),1337(hackthebox),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare)
```

### Uname

Approfondissons un peu la commande `uname`. Si nous tapons `man uname` dans notre terminal, nous afficherons la page de manuel de la commande, qui montrera les options possibles que nous pouvons exécuter avec la commande et les résultats.

```text
UNAME(1)                         User Commands                        UNAME(1)

NAME
       uname - print system information

SYNOPSIS
       uname [OPTION]...

DESCRIPTION
       Print certain system information.  With no OPTION, same as -s.

       -a, --all
              print all information, in the following order, except omit -p and -i if unknown:

       -s, --kernel-name
              print the kernel name

       -n, --nodename
              print the network node hostname

       -r, --kernel-release
              print the kernel release

       -v, --kernel-version
              print the kernel version

       -m, --machine
              print the machine hardware name

       -p, --processor
              print the processor type (non-portable)

       -i, --hardware-platform
              print the hardware platform (non-portable)

       -o, --operating-system
```

L'exécution de `uname -a` affichera toutes les informations sur la machine dans un ordre spécifique : nom du noyau, nom d'hôte, la publication du noyau (kernel release), la version du noyau (kernel version), le nom du matériel de la machine et le système d'exploitation. L'option `-a` omettra `-p` (type de processeur) et `-i` (plate-forme matérielle) s'ils sont inconnus.

```bash
cry0l1t3@htb[/htb]$ uname -a
Linux box 4.15.0-99-generic #100-Ubuntu SMP Wed Apr 22 20:32:56 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
```

À partir de la commande ci-dessus, nous pouvons voir que le nom du noyau est `Linux`, le nom d'hôte est `box`, la publication du noyau est `4.15.0-99-generic`, la version du noyau est `#100-Ubuntu SMP Wed Apr 22 20:32:56 UTC 2020`, et ainsi de suite. Exécuter l'une de ces options seule nous donnera la sortie spécifique qui nous intéresse.

### Uname pour obtenir la version du noyau

Supposons que nous voulions afficher la publication du noyau pour rechercher rapidement des exploits de noyau potentiels. Nous pouvons taper `uname -r` pour obtenir cette information.

```bash
cry0l1t3@htb[/htb]$ uname -r
4.15.0-99-generic
```

Avec cette information, nous pourrions aller chercher « 4.15.0-99-generic exploit », et le premier [résultat](https://www.exploit-db.com/exploits/47163) semble immédiatement utile.

Il est fortement recommandé d'étudier les commandes et de comprendre à quoi elles servent et quelles informations elles peuvent fournir. Bien que cela puisse être un peu fastidieux, nous pouvons beaucoup apprendre en étudiant les pages de manuel des commandes courantes. Nous pourrions même découvrir des choses que nous ne savions pas possibles avec une commande donnée. Ces informations ne sont pas seulement utilisées pour travailler avec Linux. Cependant, elles seront également utilisées plus tard pour découvrir des vulnérabilités et des erreurs de configuration sur le système Linux qui pourraient contribuer à une élévation de privilèges. Voici quelques exercices facultatifs que nous pouvons résoudre pour nous entraîner, ce qui nous aidera à nous familiariser avec certaines des commandes.

---

## À propos des exercices Linux

Les exercices fournis pour étudier le système d'exploitation Linux et ses commandes peuvent ne pas toujours être immédiatement clairs sur ce que vous devez faire, et c'est tout à fait normal, c'est même inévitable. Comme vous l'avez appris dans le module sur le processus d'apprentissage, apprendre quelque chose de nouveau peut être inconfortable et peut causer du stress. Vous pouvez le comparer à la première fois où vous vous êtes assis au volant d'une voiture et avez dû conduire seul. C'était stressant car il y avait beaucoup de choses sur lesquelles vous deviez vous concentrer en même temps. Mais maintenant, avec l'expérience, conduire est plus facile, bien que vous n'appreniez plus autant. De même, dans ce module, vous pourriez vous retrouver dans des situations où vous n'êtes pas sûr de ce qu'il faut faire, mais ce n'est pas grave. Dans votre parcours en cybersécurité, vous ferez souvent face à de tels moments, et ils sont un indicateur positif que vous apprenez quelque chose de nouveau. Surmonter ces défis vous aide à vous améliorer, même si vous n'avez pas encore entièrement résolu l'exercice. C'est l'objectif final : progresser par l'apprentissage.

Les exercices sont intentionnellement conçus pour vous pousser progressivement hors de vos connaissances actuelles et vers un territoire inconnu. Cette progression est délibérée et garantit qu'à mesure que vous continuez à pratiquer, votre expérience et vos connaissances s'étendront naturellement. Bien que cela puisse parfois être inconfortable, ce processus est essentiel à la croissance. À chaque nouveau défi, vous irez au-delà de ce que vous savez déjà, et avec un effort constant, vous constaterez que votre compréhension et vos compétences se développent presque automatiquement. Continuez à pratiquer, et vous deviendrez progressivement plus confiant et capable de naviguer dans l'inconnu.

---

← [[05 - Obtenir de l'aide]] | [[00 - Sommaire Linux|Sommaire]] | [[07 - Navigation]] →
