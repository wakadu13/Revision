---
tags:
  - bash-scripting
ordre: 2
---

# Exécution conditionnelle

---

L'exécution conditionnelle nous permet de contrôler le flux de notre script en fonction de différentes conditions. Cette fonctionnalité est l'un des composants essentiels. Sans elle, nous ne pourrions exécuter qu'une commande après l'autre.

Lorsque nous définissons diverses conditions, nous spécifions quelles fonctions ou sections de code doivent être exécutées pour une valeur spécifique. Si nous atteignons une condition spécifique, seul le code correspondant à cette condition est exécuté, et les autres sont ignorés. Dès que la section de code est terminée, les commandes suivantes seront exécutées en dehors de l'exécution conditionnelle. Revenons sur la première partie du script et analysons-la.

#### Script.sh

```bash
#!/bin/bash

# Vérifier l'argument fourni
if [ $# -eq 0 ]
then
    echo -e "You need to specify the target domain.\n"
    echo -e "Usage:"
    echo -e "\t$0 <domain>"
    exit 1
else
    domain=$1
fi

<SNIP>
```

En résumé, cette section de code fonctionne avec les composants suivants :

- `#!/bin/bash` - Shebang.
- `if-else-fi` - Exécution conditionnelle.
- `echo` - Affiche une sortie spécifique.
- `$#` / `$0` / `$1` - Variables spéciales.
- `domain` - Variables.

Les conditions des exécutions conditionnelles peuvent être définies à l'aide de variables (`$#`, `$0`, `$1`, `domain`), de valeurs (`0`) et de chaînes de caractères (strings), comme nous le verrons dans les exemples suivants. Ces valeurs sont comparées avec les `opérateurs de comparaison` (comparison operators) (`-eq`) que nous examinerons dans la section suivante.

---

## Shebang

La ligne shebang se trouve toujours en haut de chaque script et commence toujours par « `#!` ». Cette ligne contient le chemin vers l'interpréteur spécifié (`/bin/bash`) avec lequel le script est exécuté. Nous pouvons également utiliser le Shebang pour définir d'autres interpréteurs comme Python, Perl, et autres.

```python
#!/usr/bin/env python
```

```perl
#!/usr/bin/env perl
```

---

## If-Else-Fi

L'une des tâches les plus fondamentales en programmation est de vérifier différentes conditions pour les gérer. La vérification des conditions prend généralement deux formes différentes dans les langages de programmation et de script, la `condition if-else` et les `instructions case` (case statements). En pseudo-code, la condition if signifie ce qui suit :

#### Pseudo-Code

```bash
si [ le nombre d'arguments fournis est égal à 0 ]
alors
    Afficher : "You need to specify the target domain."
    Afficher : "<ligne vide>"
    Afficher : "Usage:"
    Afficher : "   <nom du script> <domaine>"
    Quitter le script avec une erreur
sinon
    La variable "domain" sert d'alias pour l'argument fourni

terminer la condition if
```

Par défaut, une condition `If-Else` peut ne contenir qu'un seul « `If` », comme le montre l'exemple suivant.

#### If-Only.sh

```bash
#!/bin/bash

value=$1

if [ $value -gt "10" ]
then
        echo "Given argument is greater than 10."
fi
```

#### If-Only.sh - Execution

```bash
Hiterof13@htb[/htb]$ bash if-only.sh 5
```

```bash
Hiterof13@htb[/htb]$ bash if-only.sh 12

Given argument is greater than 10.
```

---

En ajoutant `Elif` ou `Else`, nous ajoutons des alternatives pour traiter des valeurs ou des états spécifiques. Si une valeur particulière ne correspond pas au premier cas, elle sera traitée par les autres.

#### If-Elif-Else.sh

```bash
#!/bin/bash

value=$1

if [ $value -gt "10" ]
then
    echo "Given argument is greater than 10."
elif [ $value -lt "10" ]
then
    echo "Given argument is less than 10."
else
    echo "Given argument is not a number."
fi
```

#### If-Elif-Else.sh - Execution

```bash
Hiterof13@htb[/htb]$ bash if-elif-else.sh 5

Given argument is less than 10.
```

```bash
Hiterof13@htb[/htb]$ bash if-elif-else.sh 12

Given argument is greater than 10.
```

```bash
Hiterof13@htb[/htb]$ bash if-elif-else.sh HTB

if-elif-else.sh: line 5: [: HTB: integer expression expected
if-elif-else.sh: line 8: [: HTB: integer expression expected
Given argument is not a number.
```

---

Nous pourrions étendre notre script et spécifier plusieurs conditions. Cela pourrait ressembler à quelque chose comme ceci :

#### Plusieurs Conditions - Script.sh

```bash
#!/bin/bash

# Vérifier l'argument fourni
if [ $# -eq 0 ]
then
    echo -e "You need to specify the target domain.\n"
    echo -e "Usage:"
    echo -e "\t$0 <domain>"
    exit 1
elif [ $# -eq 1 ]
then
    domain=$1
else
    echo -e "Too many arguments given."
    exit 1
fi

<SNIP>
```

Ici, nous définissons une autre condition (`elif [<condition>];then`) qui affiche une ligne nous indiquant (`echo -e "..."`) que nous avons fourni plus d'un argument et quitte le programme avec une erreur (`exit 1`).

---

---

## Script d'exercice

```bash
#!/bin/bash
# Compter le nombre de caractères dans une variable :
#     echo $variable | wc -m

# Variable à encoder
var="nef892na9s1p9asn2aJs71nIsm"

for counter in {1..40}
do
        var=$(echo $var | base64)
done
```

---

← [[01 - Shell Bourne-Again]] | [[00 - Sommaire Bash Scripting|Sommaire]] | [[03 - Arguments, Variables et Tableaux]] →
