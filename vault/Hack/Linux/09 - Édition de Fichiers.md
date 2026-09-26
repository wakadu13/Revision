---
tags:
  - linux
ordre: 9
---

# Édition de Fichiers

Après avoir appris à créer des fichiers et des répertoires, passons à la manipulation de ces fichiers. Il existe plusieurs façons d'éditer un fichier sous Linux, les éditeurs de texte les plus courants étant `Vi` et `Vim`. Cependant, nous commencerons par l'éditeur `Nano`, qui est moins utilisé mais plus facile à comprendre.

Pour créer et éditer un fichier avec Nano, vous pouvez spécifier le nom du fichier directement comme premier paramètre lors du lancement de l'éditeur. Par exemple, pour créer et ouvrir un nouveau fichier nommé `notes.txt`, vous utiliseriez la commande suivante :

```bash
Hiterof13@htb[/htb]$ nano notes.txt
```

Cette commande ouvrira l'éditeur `Nano`, vous permettant de commencer à éditer le fichier `notes.txt` immédiatement. L'interface simple de Nano (aussi appelée « `pager` ») en fait un excellent choix pour éditer rapidement des fichiers texte, surtout lorsque vous débutez.

### L'éditeur Nano

```text
  GNU nano 2.9.3                    notes.txt

Here we can type everything we want and make our notes.▓

^G Get Help    ^O Write Out   ^W Where Is    ^K Cut Text    ^J Justify     ^C Cur Pos     M-U Undo
^X Exit        ^R Read File   ^\ Replace     ^U Uncut Text  ^T To Spell    ^_ Go To Line  M-E Redo
```

Ci-dessous, nous voyons deux lignes avec de courtes descriptions. L'accent circonflexe (`^`) représente notre touche « `[CTRL]` ». Par exemple, si nous appuyons sur `[CTRL + W]`, une ligne « `Search:` » apparaît en bas de l'éditeur, où nous pouvons saisir le ou les mots que nous recherchons. Si nous cherchons maintenant le mot « `we` » et que nous appuyons sur `[ENTRÉE]`, le curseur se déplacera vers le premier mot qui correspond.

```text
  GNU nano 2.9.3                    notes.txt

Here ▓we can type everything we want and make our notes.

Search:   notes
^G Get Help    M-C Case Sens  M-B Backwards  M-J FullJstify ^W Beg of Par  ^Y First Line  ^P PrevHstory
^C Cancel      M-R Regexp     ^R Replace     ^T Go To Line  ^O End of Par  ^V Last Line   ^N NextHstory
```

Pour sauter à la prochaine correspondance avec le curseur, nous appuyons de nouveau sur `[CTRL + W]` et confirmons avec `[ENTRÉE]` sans aucune information supplémentaire.

```text
  GNU nano 2.9.3                    notes.txt

Here we can type everything ▓we want and make our notes.

Search [we]:
^G Get Help    M-C Case Sens  M-B Backwards  M-J FullJstify ^W Beg of Par  ^Y First Line  ^P PrevHstory
^C Cancel      M-R Regexp     ^R Replace     ^T Go To Line  ^O End of Par  ^V Last Line   ^N NextHstory
```

Nous pouvons maintenant enregistrer le fichier en appuyant sur `[CTRL + O]` et confirmer le nom du fichier avec `[ENTRÉE]`.

```text
  GNU nano 2.9.3                    notes.txt

Here we can type everything we want and make our notes.

File Name to Write: notes.txt▓
^G Get Help    M-C Case Sens  M-B Backwards  M-J FullJstify ^W Beg of Par  ^Y First Line  ^P PrevHstory
^C Cancel      M-R Regexp     ^R Replace     ^T Go To Line  ^O End of Par  ^V Last Line   ^N NextHstory
```

Après avoir enregistré le fichier, nous pouvons quitter l'éditeur avec `[CTRL + X]`.

### De retour sur le shell

Pour afficher le contenu du fichier, nous pouvons utiliser la commande `cat`.

```bash
Hiterof13@htb[/htb]$ cat notes.txt
Here we can type everything we want and make our notes.
```

Sur les systèmes Linux, plusieurs fichiers peuvent être extrêmement utiles pour les testeurs d'intrusion (penetration testers), en raison de permissions mal configurées ou de paramètres de sécurité insuffisants de la part des administrateurs. L'un de ces fichiers importants est le fichier `/etc/passwd`. Ce fichier contient des informations essentielles sur les utilisateurs du système, telles que leurs noms d'utilisateur, leurs identifiants d'utilisateur (`UID`), leurs identifiants de groupe (`GID`) et leurs répertoires personnels.

Historiquement, le fichier `/etc/passwd` stockait également les hachages de mot de passe (password hashes), mais aujourd'hui, ces hachages sont généralement stockés dans `/etc/shadow`, qui a des permissions plus strictes. Cependant, si les permissions sur `/etc/passwd` ou d'autres fichiers critiques ne sont pas correctement définies, cela peut exposer des informations sensibles ou conduire à des opportunités d'escalade de privilèges (privilege escalation).

En tant que testeurs d'intrusion, l'identification de fichiers avec des droits ou des permissions incorrects peut fournir des informations clés sur des vulnérabilités potentielles qui pourraient être exploitées, comme des comptes utilisateurs faibles ou un accès aux fichiers mal configuré qui devrait normalement être restreint. La compréhension de ces fichiers est essentielle lors de l'évaluation de la posture de sécurité d'un système.

---

## VIM

`Vim` est un éditeur open-source pour toutes sortes de textes ASCII, tout comme Nano. C'est un clone amélioré du précédent Vi. C'est un éditeur extrêmement puissant qui se concentre sur l'essentiel, à savoir l'édition de texte. Pour les tâches qui vont au-delà, Vim fournit une interface avec des programmes externes, tels que `grep`, `awk`, `sed`, etc., qui peuvent gérer leurs tâches spécifiques bien mieux qu'une fonction correspondante directement implémentée dans un éditeur ne le peut habituellement. Cela rend l'éditeur petit et compact, rapide, puissant, flexible et moins sujet aux erreurs.

Vim suit ici le principe d'Unix : de nombreux petits programmes spécialisés, bien testés et éprouvés, qui, lorsqu'ils sont combinés et communiquent entre eux, aboutissent à un système flexible et puissant.

### Vim

```bash
Hiterof13@htb[/htb]$ vim
```

```text
1 $
~
~                              VIM - Vi IMproved
~
~                               version 8.0.1453
~                           by Bram Moolenaar et al.
~           Modified by pkg-vim-maintainers@lists.alioth.debian.org
~                 Vim is open source and freely distributable
~
~                           Sponsor Vim development!
~                type  :help sponsor<Enter>    for information
~
~                type  :q<Enter>               to exit
~                type  :help<Enter>  or  <F1>  for on-line help
~                type  :help version8<Enter>   for version info
~
                                                              0,0-1         All
```

Contrairement à Nano, `Vim` est un éditeur modal qui peut distinguer la saisie de texte de la saisie de commandes. Vim offre un total de six modes fondamentaux qui facilitent notre travail et rendent cet éditeur si puissant :

|**Mode**|**Description**|
|---|---|
|`Normal`|En mode normal, toutes les saisies sont considérées comme des commandes de l'éditeur. Il n'y a donc pas d'insertion des caractères saisis dans le tampon (buffer) de l'éditeur, comme c'est le cas avec la plupart des autres éditeurs. Après avoir démarré l'éditeur, nous sommes généralement en mode normal.|
|`Insert`|À quelques exceptions près, tous les caractères saisis sont insérés dans le tampon.|
|`Visual`|Le mode visuel est utilisé pour marquer une partie contiguë du texte, qui sera surlignée visuellement. En positionnant le curseur, nous modifions la zone sélectionnée. La zone surlignée peut ensuite être éditée de diverses manières, par exemple en la supprimant, la copiant ou la remplaçant.|
|`Command`|Il nous permet de saisir des commandes d'une seule ligne en bas de l'éditeur. Cela peut être utilisé pour trier, remplacer des sections de texte ou les supprimer, par exemple.|
|`Replace`|En mode remplacement, le nouveau texte saisi écrasera les caractères de texte existants, sauf s'il n'y a plus d'anciens caractères à la position actuelle du curseur. Dans ce cas, le nouveau texte saisi sera ajouté.|
|`Ex`|Émule le comportement de l'éditeur de texte [Ex](https://man7.org/linux/man-pages/man1/ex.1p.html), l'un des prédécesseurs de `Vim`. Fournit un mode où nous pouvons exécuter plusieurs commandes séquentiellement sans retourner en mode Normal après chaque commande.|

Lorsque l'éditeur Vim est ouvert, nous pouvons passer en mode commande en tapant « `:` », puis en tapant « `q` » pour fermer Vim.

```text
1 $
~
~                              VIM - Vi IMproved
~
~                               version 8.0.1453
~                           by Bram Moolenaar et al.
~           Modified by pkg-vim-maintainers@lists.alioth.debian.org
~                 Vim is open source and freely distributable
~
~                           Sponsor Vim development!
~                type  :help sponsor<Enter>    for information
~
~                type  :q<Enter>               to exit
~                type  :help<Enter>  or  <F1>  for on-line help
~                type  :help version8<Enter>   for version info
~
:q▓
```

Vim offre une excellente opportunité appelée `vimtutor` pour s'entraîner et se familiariser avec l'éditeur. Il peut sembler très difficile et compliqué au début, mais cette impression ne durera que peu de temps. L'efficacité que nous gagnons avec Vim une fois que nous nous y sommes habitués est énorme. L'entrée dans le mode tuteur de l'éditeur `vim` peut se faire en utilisant le mode `Commande` `:Tutor` ou en utilisant la commande `vimtutor` dans le shell.

### VimTutor

```bash
Hiterof13@htb[/htb]$ vimtutor
```

```text
===============================================================================
=    W e l c o m e   t o   t h e   V I M   T u t o r    -    Version 1.7      =
===============================================================================

     Vim is a very powerful editor that has many commands, too many to
     explain in a tutor such as this.  This tutor is designed to describe
     enough of the commands that you will be able to easily use Vim as
     an all-purpose editor.

     The approximate time required to complete the tutor is 25-30 minutes,
     depending upon how much time is spent with experimentation.

     ATTENTION:
     The commands in the lessons will modify the text.  Make a copy of this
     file to practice on (if you started "vimtutor" this is already a copy).

     It is important to remember that this tutor is set up to teach by
     use.  That means that you need to execute the commands to learn them
     properly.  If you only read the text, you will forget the commands!

     Now, make sure that your Caps-Lock key is NOT depressed and press
     the   j   key enough times to move the cursor so that lesson 1.1
     completely fills the screen.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

---

← [[08 - Travailler avec les Fichiers et les Répertoires]] | [[00 - Sommaire Linux|Sommaire]] | [[10 - Rechercher des Fichiers et des Dossiers]] →
