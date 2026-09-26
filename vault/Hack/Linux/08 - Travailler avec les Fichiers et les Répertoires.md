---
tags:
  - linux
ordre: 8
---

# Travailler avec les Fichiers et les Répertoires

La principale différence entre la manipulation des fichiers sous Linux et sous Windows réside dans la manière dont nous accédons à ces fichiers et les gérons. Sous Windows, nous utilisons généralement des outils graphiques comme l'Explorateur pour trouver, ouvrir et modifier des fichiers. Cependant, sous Linux, le terminal offre une alternative puissante où les fichiers peuvent être consultés et modifiés directement à l'aide de commandes. Cette méthode est non seulement plus rapide, mais aussi plus efficace, car elle vous permet de modifier des fichiers de manière interactive sans même avoir besoin d'éditeurs comme `vim` ou `nano`.

L'efficacité du terminal provient de sa capacité à accéder aux fichiers avec seulement quelques commandes, et il vous permet de modifier des fichiers de manière sélective en utilisant des expressions régulières (`regex`). De plus, vous pouvez exécuter plusieurs commandes à la fois, rediriger la sortie vers des fichiers et automatiser les tâches d'édition par lots, ce qui représente un gain de temps considérable lorsque vous travaillez avec de nombreux fichiers simultanément. Cette approche en ligne de commande rationalise le flux de travail (workflow), ce qui en fait un outil inestimable pour des tâches qui seraient plus longues à réaliser via une interface graphique.

Ensuite, nous explorerons le travail avec les fichiers et les répertoires pour gérer efficacement le contenu de notre système d'exploitation.

---

## Créer, Déplacer et Copier

Commençons par apprendre à effectuer des opérations clés comme la création, le renommage, le déplacement, la copie et la suppression de fichiers. Avant d'exécuter les commandes suivantes, nous devons d'abord nous connecter en SSH à la cible (en utilisant les instructions de connexion en bas de la section). Maintenant, disons que nous voulons créer un nouveau fichier ou un nouveau répertoire. La syntaxe pour cela est la suivante :

### Syntaxe - touch

```bash
Hiterof13@htb[/htb]$ touch <nom>
```

### Syntaxe - mkdir

```bash
Hiterof13@htb[/htb]$ mkdir <nom>
```

Dans l'exemple suivant, nous allons créer un fichier nommé `info.txt` et un répertoire nommé `Storage`. Pour les créer, nous suivons les commandes et leur syntaxe comme indiqué ci-dessus.

### Créer un Fichier Vide

```bash
Hiterof13@htb[/htb]$ touch info.txt
```

### Créer un Répertoire

```bash
Hiterof13@htb[/htb]$ mkdir Storage
```

Lorsque vous organisez votre système, vous pourriez avoir besoin de créer plusieurs répertoires à l'intérieur d'autres répertoires. Exécuter manuellement la commande `mkdir` pour chacun d'eux serait fastidieux. Heureusement, la commande mkdir dispose de l'option `-p` (parents), qui vous permet de créer automatiquement les répertoires parents.

```bash
Hiterof13@htb[/htb]$ mkdir -p Storage/local/user/documents
```

Nous pouvons examiner toute la structure après avoir créé les répertoires parents avec l'outil `tree`.

```bash
Hiterof13@htb[/htb]$ tree .
.
├── info.txt
└── Storage
    └── local
        └── user
            └── documents

4 directories, 1 file
```

Vous pouvez créer des fichiers directement dans des répertoires spécifiques en précisant le chemin où le fichier doit être stocké, et vous pouvez utiliser le point simple (`.`) pour indiquer que vous voulez partir du répertoire courant. C'est un moyen pratique de travailler depuis votre emplacement actuel, sans avoir à taper le chemin complet. Par conséquent, la commande pour créer un autre fichier vide ressemble à ceci :

### Créer userinfo.txt

```bash
Hiterof13@htb[/htb]$ touch ./Storage/local/user/userinfo.txt
```

```bash
Hiterof13@htb[/htb]$ tree .
.
├── info.txt
└── Storage
    └── local
        └── user
            ├── documents
            └── userinfo.txt

4 directories, 2 files
```

Avec la commande `mv`, nous pouvons déplacer mais aussi renommer des fichiers et des répertoires. La syntaxe pour cela est la suivante :

### Syntaxe - mv

```bash
Hiterof13@htb[/htb]$ mv <fichier/répertoire> <fichier/répertoire renommé>
```

D'abord, renommons le fichier `info.txt` en `information.txt`, puis déplaçons-le dans le répertoire `Storage`.

### Renommer le Fichier

```bash
Hiterof13@htb[/htb]$ mv info.txt information.txt
```

Maintenant, créons un fichier nommé `readme.txt` dans le répertoire courant, puis déplaçons les fichiers `information.txt` et `readme.txt` dans le répertoire `Storage/`.

### Créer readme.txt

```bash
Hiterof13@htb[/htb]$ touch readme.txt
```

### Déplacer des Fichiers vers un Répertoire Spécifique

```bash
Hiterof13@htb[/htb]$ mv information.txt readme.txt Storage/
```

```bash
Hiterof13@htb[/htb]$ tree .
.
└── Storage
    ├── information.txt
    ├── local
    │   └── user
    │       ├── documents
    │       └── userinfo.txt
    └── readme.txt

4 directories, 3 files
```

Supposons que nous voulions avoir le fichier `readme.txt` dans le répertoire `local/`. Nous pouvons alors l'y copier en spécifiant les chemins.

### Copier readme.txt

```bash
Hiterof13@htb[/htb]$ cp Storage/readme.txt Storage/local/
```

Nous pouvons maintenant vérifier si le fichier s'y trouve en utilisant à nouveau l'outil `tree`.

```bash
Hiterof13@htb[/htb]$ tree .
.
└── Storage
    ├── information.txt
    ├── local
    │   ├── readme.txt
    │   └── user
    │       ├── documents
    │       └── userinfo.txt
    └── readme.txt

4 directories, 4 files
```

En plus des commandes de base de gestion de fichiers, il existe de nombreuses autres manières puissantes de travailler avec les fichiers sous Linux, comme l'utilisation de la redirection et des éditeurs de texte. La redirection vous permet de manipuler le flux d'entrée et de sortie entre les commandes et les fichiers, rendant des tâches comme la création ou la modification de fichiers plus rapides et plus efficaces. Vous pouvez également utiliser des éditeurs de texte populaires comme vim et nano pour une édition plus interactive.

Nous explorerons et discuterons de ces méthodes plus en détail dans les sections ultérieures. À mesure que vous vous familiariserez avec ces techniques, vous gagnerez en flexibilité dans la manière de créer, modifier et gérer les fichiers sur votre système.

> [!tip] Exercice facultatif
> Utilisez les outils que nous avons déjà appris pour découvrir comment supprimer des fichiers et des répertoires. Gardez à l'esprit que la recherche en ligne est une partie précieuse du processus d'apprentissage — ce n'est pas de la triche. Vous n'êtes pas en train d'être évalué en ce moment, mais plutôt de construire vos connaissances. Rechercher des solutions en ligne peut vous exposer à différentes approches et méthodes alternatives, vous donnant une compréhension plus large du fonctionnement des choses et vous aidant à découvrir les moyens les plus efficaces de résoudre les problèmes.

---

← [[07 - Navigation]] | [[00 - Sommaire Linux|Sommaire]] | [[09 - Édition de Fichiers]] →
