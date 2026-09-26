---
tags:
  - bash-scripting
ordre: 4
---

# Opérateurs de comparaison

---

Pour comparer des valeurs spécifiques entre elles, nous avons besoin d'éléments appelés [opérateurs de comparaison](https://www.tldp.org/LDP/abs/html/comparison-ops.html). Les `opérateurs de comparaison` sont utilisés pour déterminer comment les valeurs définies seront comparées. Pour ces opérateurs, on distingue :

- les opérateurs de `chaîne de caractères` (string)
- les opérateurs de `nombre entier` (integer)
- les opérateurs de `fichier` (file)
- les opérateurs `booléens` (boolean)

---

## Opérateurs de chaîne de caractères

Si nous comparons des chaînes de caractères, nous savons ce que nous aimerions trouver dans la valeur correspondante.

|**Opérateur**|**Description**|
|---|---|
|`==`|est égal à|
|`!=`|n'est pas égal à|
|`<`|est inférieur selon l'ordre alphabétique ASCII|
|`>`|est supérieur selon l'ordre alphabétique ASCII|
|`-z`|si la chaîne est vide (nulle)|
|`-n`|si la chaîne n'est pas nulle|

Il est important de noter ici que nous mettons la variable pour l'argument donné (`$1`) entre guillemets doubles (`"$1"`). Cela indique à Bash que le contenu de la variable doit être traité comme une chaîne de caractères. Sinon, nous obtiendrions une erreur.

```bash
#!/bin/bash

# Check the given argument
if [ "$1" != "HackTheBox" ]
then
    echo -e "You need to give 'HackTheBox' as argument."
    exit 1

elif [ $# -gt 1 ]
then
    echo -e "Too many arguments given."
    exit 1

else
    domain=$1
    echo -e "Success!"
fi
```

Les opérateurs de comparaison de chaînes de caractères « `<` / `>` » ne fonctionnent qu'à l'intérieur des doubles crochets `[[ <condition> ]]`. Nous pouvons trouver la table ASCII sur Internet ou en utilisant la commande suivante dans le terminal. Nous verrons un exemple plus tard.

```bash
Hiterof13@htb[/htb]$ man ascii
```

#### Table ASCII

|**Décimal**|**Hexadécimal**|**Caractère**|**Description**|
|---|---|---|---|
|0|00|NUL|Fin d'une chaîne|
|...|...|...|...|
|65|41|A|A majuscule|
|66|42|B|B majuscule|
|67|43|C|C majuscule|
|68|44|D|D majuscule|
|...|...|...|...|
|127|7F|DEL|Supprimer|

`ASCII` est l'acronyme de `American Standard Code for Information Interchange` et représente un codage de caractères sur 7 bits. Comme chaque bit peut prendre deux valeurs, il y a `128` combinaisons de bits différentes, qui peuvent aussi être interprétées comme les nombres entiers décimaux de `0` à `127` ou en valeurs hexadécimales de `00` à `7F`. Les 32 premiers codes de caractères ASCII sont réservés en tant que [caractères de contrôle](https://fr.wikipedia.org/wiki/Caract%C3%A8re_de_contr%C3%B4le).

---

## Opérateurs de nombre entier

La comparaison de nombres entiers peut nous être très utile si nous savons quelles valeurs nous voulons comparer. En conséquence, nous définissons les étapes et commandes suivantes sur la manière dont le script doit traiter la valeur correspondante.

|**Opérateur**|**Description**|
|---|---|
|`-eq`|est égal à|
|`-ne`|n'est pas égal à|
|`-lt`|est inférieur à|
|`-le`|est inférieur ou égal à|
|`-gt`|est supérieur à|
|`-ge`|est supérieur ou égal à|

---

```bash
#!/bin/bash

# Check the given argument
if [ $# -lt 1 ]
then
    echo -e "Number of given arguments is less than 1"
    exit 1

elif [ $# -gt 1 ]
then
    echo -e "Number of given arguments is greater than 1"
    exit 1

else
    domain=$1
    echo -e "Number of given arguments equals 1"
fi
```

---

## Opérateurs de fichier

Les opérateurs de fichier sont utiles si nous voulons connaître des permissions spécifiques ou si les fichiers existent.

|**Opérateur**|**Description**|
|---|---|
|`-e`|si le fichier existe|
|`-f`|teste si c'est un fichier|
|`-d`|teste si c'est un répertoire|
|`-L`|teste si c'est un lien symbolique|
|`-N`|vérifie si le fichier a été modifié depuis sa dernière lecture|
|`-O`|si l'utilisateur actuel est propriétaire du fichier|
|`-G`|si l'ID de groupe du fichier correspond à celui de l'utilisateur actuel|
|`-s`|teste si la taille du fichier est supérieure à 0|
|`-r`|teste si le fichier a la permission de lecture|
|`-w`|teste si le fichier a la permission d'écriture|
|`-x`|teste si le fichier a la permission d'exécution|

```bash
#!/bin/bash

# Check if the specified file exists
if [ -e "$1" ]
then
    echo -e "The file exists."
    exit 0

else
    echo -e "The file does not exist."
    exit 2
fi
```

---

## Opérateurs booléens et logiques

Nous obtenons une valeur booléenne `faux` (false) ou `vrai` (true) comme résultat avec les opérateurs logiques. Bash nous donne la possibilité de comparer des chaînes de caractères en utilisant des doubles crochets `[[ <condition> ]]`. Pour obtenir ces valeurs booléennes, nous pouvons utiliser les opérateurs de chaîne de caractères. Que la comparaison corresponde ou non, nous obtenons la valeur booléenne `faux` ou `vrai`.

```bash
#!/bin/bash

# Check the boolean value
if [[ -z $1 ]]
then
    echo -e "Boolean value: True (is null)"
    exit 1

elif [[ $# > 1 ]]
then
    echo -e "Boolean value: True (is greater than)"
    exit 1

else
    domain=$1
    echo -e "Boolean value: False (is equal to)"
fi
```

---

## Opérateurs logiques

Avec les opérateurs logiques, nous pouvons définir plusieurs conditions au sein d'une seule. Cela signifie que toutes les conditions que nous définissons doivent être remplies avant que le code correspondant puisse être exécuté.

|**Opérateur**|**Description**|
|---|---|
|`!`|négation logique NON|
|`&&`|ET logique|
|`\|`|OU logique|

```bash
#!/bin/bash

# Check if the specified file exists and if we have read permissions
if [[ -e "$1" && -r "$1" ]]
then
    echo -e "We can read the file that has been specified."
    exit 0

elif [[ ! -e "$1" ]]
then
    echo -e "The specified file does not exist."
    exit 2

elif [[ -e "$1" && ! -r "$1" ]]
then
    echo -e "We don't have read permission for this file."
    exit 1

else
    echo -e "Error occured."
    exit 5
fi
```

---

## Script d'exercice

```bash
#!/bin/bash

var="8dm7KsjU28B7v621Jls"
value="ERmFRMVZ0U2paTlJYTkxDZz09Cg"

for i in {1..40}
do
        var=$(echo $var | base64)

        #<---- If condition here:
done
```

---

← [[03 - Arguments, Variables et Tableaux]] | [[00 - Sommaire Bash Scripting|Sommaire]] | [[05 - Arithmétique]] →
