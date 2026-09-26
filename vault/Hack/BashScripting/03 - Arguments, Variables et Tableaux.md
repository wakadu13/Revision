---
tags:
  - bash-scripting
ordre: 3
---

# Arguments, Variables et Tableaux

---

## Arguments

L'avantage des scripts bash est que nous pouvons toujours passer jusqu'à 9 arguments (`$0`-`$9`) au script sans les assigner à des variables ou définir les exigences correspondantes pour ceux-ci. `9 arguments` car le premier argument `$0` est réservé pour le script. Comme nous pouvons le voir ici, nous avons besoin du signe dollar (`$`) avant le nom de la variable pour l'utiliser à la position spécifiée. En comparaison, l'assignation ressemblerait à ceci :

```bash
Hiterof13@htb[/htb]$ ./script.sh ARG1 ARG2 ARG3 ... ARG9
       ASSIGNMENTS:       $0      $1   $2   $3 ...   $9
```

Cela signifie que nous avons automatiquement assigné les arguments correspondants aux variables prédéfinies à cet endroit. Ces variables sont appelées variables spéciales. Ces variables spéciales servent d'espaces réservés. Si nous regardons à nouveau la section de code, nous verrons où et quels arguments ont été utilisés.

#### CIDR.sh

```bash
#!/bin/bash

# Check for given argument
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

Il y a plusieurs manières d'exécuter notre script. Cependant, nous devons d'abord définir les droits d'exécution du script avant de l'exécuter avec l'interpréteur qui y est défini.

#### CIDR.sh - Définir les droits d'exécution

```bash
Hiterof13@htb[/htb]$ chmod +x cidr.sh
```

#### CIDR.sh - Exécution sans arguments

```bash
Hiterof13@htb[/htb]$ ./cidr.sh

You need to specify the target domain.

Usage:
    cidr.sh <domain>
```

#### CIDR.sh - Exécution sans droits d'exécution

```bash
Hiterof13@htb[/htb]$ bash cidr.sh

You need to specify the target domain.

Usage:
    cidr.sh <domain>
```

---

## Variables spéciales

Les variables spéciales utilisent le [séparateur de champ interne (Internal Field Separator)](https://bash.cyberciti.biz/guide/$IFS) (`IFS`) pour identifier où un argument se termine et où le suivant commence. Bash fournit diverses variables spéciales qui aident lors de la création de scripts. Certaines de ces variables sont :

|**Variable spéciale**|**Description**|
|---|---|
|`$#`|Cette variable contient le nombre d'arguments passés au script.|
|`$@`|Cette variable peut être utilisée pour récupérer la liste des arguments de la ligne de commande.|
|`$n`|Chaque argument de la ligne de commande peut être récupéré sélectivement en utilisant sa position. Par exemple, le premier argument se trouve à `$1`.|
|`$$`|L'ID de processus du processus en cours d'exécution.|
|`$?`|Le statut de sortie du script. Cette variable est utile pour déterminer si une commande a réussi. La valeur 0 représente une exécution réussie, tandis que 1 est le résultat d'un échec.|

Parmi celles présentées ci-dessus, nous avons 3 de ces variables spéciales dans notre condition `if-else`.

|**Variable spéciale**|**Description**|
|---|---|
|`$#`|Dans ce cas, nous n'avons besoin que d'une seule variable qui doit être assignée à la variable `domain`. Cette variable est utilisée pour spécifier la cible avec laquelle nous voulons travailler. Si nous fournissons juste un FQDN comme argument, la variable `$#` aura la valeur `1`.|
|`$0`|Cette variable spéciale se voit assigner le nom du script exécuté, qui est ensuite affiché dans l'exemple « `Usage:` ».|
|`$1`|Séparé par un espace, le premier argument est assigné à cette variable spéciale.|

---

## Variables

Nous voyons également à la fin de la boucle if-else que nous assignons la valeur du premier argument à la variable appelée « `domain` ». L'assignation des variables se fait sans le signe dollar (`$`). Le signe dollar est uniquement destiné à permettre l'utilisation de la valeur correspondante de cette variable dans d'autres sections de code. Lors de l'assignation de variables, il ne doit y avoir aucun espace entre les noms et les valeurs.

```bash
<SNIP>
else
    domain=$1
fi
<SNIP>
```

Contrairement à d'autres langages de programmation, il n'y a pas de différenciation et de reconnaissance directes entre les types de variables en Bash comme les « `strings` » (chaînes de caractères), les « `integers` » (entiers) et les « `boolean` » (booléens). Tout le contenu des variables est traité comme des chaînes de caractères. Bash active des fonctions arithmétiques selon que seuls des nombres sont assignés ou non. Il est important de noter lors de la déclaration de variables qu'elles ne contiennent `pas` d'`espace`. Sinon, le nom réel de la variable sera interprété comme une fonction interne ou une commande.

#### Déclaration d'une variable - Erreur

```bash
Hiterof13@htb[/htb]$ variable = "this will result with an error."

command not found: variable
```

#### Déclaration d'une variable - Sans erreur

```bash
Hiterof13@htb[/htb]$ variable="Declared without an error."
Hiterof13@htb[/htb]$ echo $variable

Declared without an error.
```

---

## Tableaux

En Bash, il est également possible d'assigner plusieurs valeurs à une seule variable. Cela peut être avantageux si nous voulons analyser plusieurs domaines ou adresses IP. Ces variables sont appelées `tableaux` (`arrays`) que nous pouvons utiliser pour stocker et traiter une séquence ordonnée de valeurs d'un type spécifique. Les `tableaux` identifient chaque entrée stockée par un `index` commençant à `0`. Lorsque nous voulons assigner une valeur à un composant d'un tableau, nous procédons de la même manière qu'avec les variables shell standard. Il suffit de spécifier l'index du champ entre crochets. La déclaration des `tableaux` ressemble à ceci en Bash :

#### Arrays.sh

```bash
#!/bin/bash

domains=(www.inlanefreight.com ftp.inlanefreight.com vpn.inlanefreight.com www2.inlanefreight.com)

echo ${domains[0]}
```

Nous pouvons également les récupérer individuellement en utilisant l'index avec la variable et l'index correspondant entre accolades. Les accolades sont utilisées pour l'expansion de variable.

```bash
Hiterof13@htb[/htb]$ ./Arrays.sh

www.inlanefreight.com
```

Il est important de noter que les guillemets simples (`'` ... `'`) et les guillemets doubles (`"` ... `"`) empêchent la séparation par un espace des valeurs individuelles dans le tableau. Cela signifie que tous les espaces entre les guillemets simples et doubles sont ignorés et traités comme une seule valeur assignée au tableau.

#### Arrays.sh

```bash
#!/bin/bash

domains=("www.inlanefreight.com ftp.inlanefreight.com vpn.inlanefreight.com" www2.inlanefreight.com)
echo ${domains[0]}
```

```bash
Hiterof13@htb[/htb]$ ./Arrays.sh

www.inlanefreight.com ftp.inlanefreight.com vpn.inlanefreight.com
```

---

← [[02 - Exécution conditionnelle]] | [[00 - Sommaire Bash Scripting|Sommaire]] | [[04 - Opérateurs de comparaison]] →
