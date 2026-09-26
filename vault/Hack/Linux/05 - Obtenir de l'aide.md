---
tags:
  - linux
ordre: 5
---

# Obtenir de l'aide

Après avoir établi une base solide sur la structure de Linux, ses différentes distributions et le rôle du shell, nous sommes maintenant prêts à mettre ces connaissances en pratique. Il est temps de se lancer, en utilisant des commandes directement dans le terminal, et d'apprendre à chercher de l'aide lorsque nous en rencontrons des inconnues.

Nous tomberons toujours sur des outils dont nous ne connaissons pas les paramètres optionnels par cœur ou sur des outils que nous n'avons jamais vus auparavant. Il est donc essentiel de savoir comment nous pouvons nous débrouiller pour nous familiariser avec ces outils. Les deux premières méthodes sont les pages de manuel (man pages) et les fonctions d'aide. C'est toujours une bonne idée de se familiariser d'abord avec l'outil que nous voulons essayer. Nous apprendrons également quelques astuces possibles avec certains outils que nous pensions impossibles. Dans les pages de manuel, nous trouverons les manuels détaillés avec des explications approfondies.

## Première commande :

```bash
Hiterof13@htb[/htb]$ ls
cacert.der  Documents  Music     Public     Videos
Desktop     Downloads  Pictures  Templates
```

La commande `ls` dans les systèmes Linux et Unix est utilisée pour lister les fichiers et les répertoires dans le dossier courant ou tout autre répertoire spécifié, vous permettant de voir ce qu'il y a à l'intérieur et de gérer les fichiers plus efficacement. Comme la plupart des commandes Linux, `ls` est fournie avec des options et des fonctionnalités supplémentaires qui vous aident à filtrer ou à formater la sortie pour afficher exactement ce que vous voulez. Pour découvrir les options qu'un outil ou une commande propose, il existe plusieurs façons d'obtenir de l'aide. L'une de ces méthodes consiste à utiliser la commande `man`, qui affiche les pages de manuel des commandes et fournit des informations détaillées sur leur utilisation.

## Syntaxe :

```bash
Hiterof13@htb[/htb]$ man <tool>
```

Jetons un œil à un exemple et obtenons de l'aide pour la commande `ls` :

## Exemple :

```bash
Hiterof13@htb[/htb]$ man ls
```

```text
LS(1)                            User Commands                           LS(1)

NAME
       ls - list directory contents

SYNOPSIS
       ls [OPTION]... [FILE]...

DESCRIPTION
       List  information  about  the FILEs (the current directory by default).
       Sort entries alphabetically if none of -cftuvSUX nor --sort  is  speci‐
       fied.

       Mandatory  arguments  to  long  options are mandatory for short options
       too.

       -a, --all
              do not ignore entries starting with .

       -A, --almost-all
              do not list implied . and ..

       --author
 Manual page ls(1) line 1 (press h for help or q to quit)
```

Après avoir examiné quelques exemples, nous pouvons également consulter rapidement les paramètres optionnels sans parcourir la documentation complète. Nous disposons de plusieurs manières de le faire.

## Syntaxe :

```bash
Hiterof13@htb[/htb]$ <tool> --help
```

## Exemple :

```bash
Hiterof13@htb[/htb]$ ls --help
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

Mandatory arguments to long options are mandatory for short options too.
  -a, --all                  do not ignore entries starting with .
  -A, --almost-all           do not list implied . and ..
      --author               with -l, print the author of each file
  -b, --escape               print C-style escapes for nongraphic characters
      --block-size=SIZE      with -l, scale sizes by SIZE when printing them;
                             e.g., '--block-size=M'; see SIZE format below
  -B, --ignore-backups       do not list implied entries ending with ~
  -c                         with -lt: sort by, and show, ctime (time of last
                             modification of file status information);
                             with -l: show ctime and sort by name;
                             otherwise: sort by ctime, newest first
  -C                         list entries by columns

<SNIP>
```

Certains outils ou commandes comme `curl` fournissent une version courte de l'aide en utilisant `-h` au lieu de `--help` :

## Syntaxe :

```bash
Hiterof13@htb[/htb]$ <tool> -h
```

## Exemple :

```bash
Hiterof13@htb[/htb]$ curl -h
Usage: curl [options...] <url>
     --abstract-unix-socket <path> Connect via abstract Unix domain socket
     --anyauth       Pick any authentication method
 -a, --append        Append to target file when uploading
     --basic         Use HTTP Basic Authentication
     --cacert <file> CA certificate to verify peer against
     --capath <dir>  CA directory to verify peer against
 -E, --cert <certificate[:password]> Client certificate file and password
<SNIP>
```

Comme nous pouvons le voir, les résultats ne diffèrent pas l'un de l'autre dans cet exemple. Un autre outil qui peut être utile au début est `apropos`. Chaque page de manuel contient une courte description. Cet outil recherche les occurrences d'un mot-clé donné dans ces descriptions.

## Syntaxe :

```bash
Hiterof13@htb[/htb]$ apropos <keyword>
```

## Exemple :

```bash
Hiterof13@htb[/htb]$ apropos sudo
sudo (8)             - execute a command as another user
sudo.conf (5)        - configuration for sudo front end
sudo_plugin (8)      - Sudo Plugin API
sudo_root (8)        - How to run administrative commands
sudoedit (8)         - execute a command as another user
sudoers (5)          - default sudo security policy plugin
sudoreplay (8)       - replay sudo session logs
visudo (8)           - edit the sudoers file
```

Une autre ressource utile pour obtenir de l'aide si nous avons du mal à comprendre une commande longue est : [https://explainshell.com/](https://explainshell.com/)

Ensuite, nous aborderons un grand nombre de commandes, dont beaucoup seront peut-être nouvelles pour vous. Cependant, vous savez maintenant comment chercher de l'aide pour toute commande que vous ne connaissez pas, ou dont vous n'êtes pas sûr des options. De plus, nous vous encourageons vivement à explorer votre curiosité, en prenant tout le temps nécessaire pour bricoler et expérimenter avec les outils présentés. Ce sera toujours du temps bien employé.

---

← [[04 - Description de l'invite]] | [[00 - Sommaire Linux|Sommaire]] | [[06 - Informations système]] →
