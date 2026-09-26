---
tags:
  - bash-scripting
ordre: 9
---

# Fonctions

---

Plus nos scripts s'allongent, plus ils deviennent chaotiques. Si nous utilisons plusieurs fois les mêmes routines dans le script, la taille du script augmentera en conséquence. Dans de tels cas, les `fonctions` sont la solution qui améliore considérablement à la fois la taille et la clarté du script. Nous regroupons plusieurs commandes dans un bloc entre accolades (`{` ... `}`), puis nous les appelons via un nom de fonction que nous définissons. Une fois qu'une fonction a été définie, elle peut être appelée et réutilisée tout au long du script.

Les `fonctions` sont une partie essentielle des scripts et des programmes, car elles servent à exécuter des commandes récurrentes pour différentes valeurs et phases du script ou du programme. Ainsi, nous n'avons pas à répéter la même section de code encore et encore, mais nous pouvons créer une seule fonction qui exécute les commandes spécifiques. La définition de telles fonctions rend le code plus facile à lire et aide à le garder aussi court que possible. Il est important de noter que les fonctions doivent toujours être définies logiquement `avant` leur premier appel, car un script est également traité de haut en bas. Par conséquent, la définition d'une fonction se trouve toujours `au début` du script. Il existe deux méthodes pour définir les fonctions :

#### Méthode 1 - Fonctions

```bash
function name {
    <commands>
}
```

#### Méthode 2 - Fonctions

```bash
name() {
    <commands>
}
```

Nous pouvons choisir la méthode de définition de fonction avec laquelle nous sommes le plus à l'aise. Dans notre script `CIDR.sh`, nous avons utilisé la première méthode car elle est plus facile à lire avec le mot-clé « `function` ».

#### CIDR.sh

```bash
<SNIP>
# Identifie la plage réseau pour la ou les adresses IP spécifiées
function network_range {
    for ip in $ipaddr
    do
        netrange=$(whois $ip | grep "NetRange\|CIDR" | tee -a CIDR.txt)
        cidr=$(whois $ip | grep "CIDR" | awk '{print $2}')
        cidr_ips=$(prips $cidr)
        echo -e "\nNetRange for $ip:"
        echo -e "$netrange"
    done
}
<SNIP>
```

La fonction est appelée simplement en invoquant son nom, comme nous l'avons vu dans l'instruction `case`.

#### Exécution de la fonction - CIDR.sh

```bash
<SNIP>
case $opt in
    "1") network_range ;;
    "2") ping_host ;;
    "3") network_range && ping_host ;;
    "*") exit 0 ;;
esac
```

---

## Passage de paramètres

De telles fonctions doivent être conçues de manière à pouvoir être utilisées avec une structure de valeurs fixe ou, du moins, uniquement avec un format fixe. Comme nous l'avons déjà vu dans notre script `CIDR.sh`, nous avons utilisé le format d'une adresse IP pour la fonction « `network_range` ». Les paramètres sont facultatifs, et nous pouvons donc appeler la fonction sans paramètres. En principe, la même chose s'applique aux paramètres passés à une fonction qu'aux paramètres passés à un script shell. Il s'agit de `$1` à `$9` (`${n}`), ou de `$variable` comme nous l'avons déjà vu. Chaque fonction possède son propre jeu de paramètres. Ainsi, ils n'entrent pas en conflit avec ceux d'autres fonctions ou avec les paramètres du script shell.

Une différence importante entre les scripts bash et d'autres langages de programmation est que toutes les variables définies sont toujours traitées de manière `globale`, sauf si elles sont déclarées autrement avec « [local](https://www.tldp.org/LDP/abs/html/localvar.html) ». Cela signifie qu'une variable définie dans une fonction peut être appelée dans le script principal (en dehors de la fonction). Le passage des paramètres aux fonctions se fait de la même manière que le passage des arguments à notre script et se présente comme suit :

#### PrintPars.sh

```bash
#!/bin/bash

function print_pars {
    echo $1 $2 $3
}

one="First parameter"
two="Second parameter"
three="Third parameter"

print_pars "$one" "$two" "$three"
```

```bash
Hiterof13@htb[/htb]$ ./PrintPars.sh

First parameter Second parameter Third parameter
```

---

## Valeurs de retour

Lorsque nous démarrons un nouveau processus, chaque `processus enfant` (par exemple, une `fonction` dans le script exécuté) renvoie un `code de retour` (return code) au `processus parent` (le `shell bash` via lequel nous avons exécuté le script) à la fin de son exécution, l'informant de son statut. Cette information est utilisée pour déterminer si le processus s'est déroulé avec succès ou si des erreurs spécifiques se sont produites. Sur la base de cette information, le `processus parent` peut décider de la suite du déroulement du programme.

|**Code de retour**|**Description**|
|---|---|
|`1`|Erreurs générales|
|`2`|Mauvaise utilisation des commandes intégrées (builtins) du shell|
|`126`|La commande invoquée ne peut pas être exécutée|
|`127`|Commande non trouvée|
|`128`|Argument invalide pour exit|
|`128+n`|Signal d'erreur fatale « `n` »|
|`130`|Script terminé par Contrôle-C|
|`255\*`|Statut de sortie hors plage|

---

Pour récupérer la valeur d'une fonction, nous pouvons utiliser plusieurs méthodes comme `return`, `echo` ou une `variable`. Dans l'exemple suivant, nous verrons comment utiliser « `$?` » pour lire le « `code de retour` », comment passer les arguments à la fonction et comment assigner le résultat à une variable.

#### Return.sh

```bash
#!/bin/bash

function given_args {

        if [ $# -lt 1 ]
        then
                echo -e "Number of arguments: $#"
                return 1
        else
                echo -e "Number of arguments: $#"
                return 0
        fi
}

# Aucun argument n'est fourni
given_args
echo -e "Function status code: $?\n"

# Un argument est fourni
given_args "argument"
echo -e "Function status code: $?\n"

# Stocke le résultat de la fonction dans une variable
content=$(given_args "argument")

echo -e "Content of the variable: \n\t$content"
```

#### Return.sh - Exécution

```bash
Hiterof13@htb[/htb]$ ./Return.sh

Number of arguments: 0
Function status code: 1

Number of arguments: 1
Function status code: 0

Content of the variable:
    Number of arguments: 1
```

---

← [[08 - Contrôle de flux - Branchements]] | [[00 - Sommaire Bash Scripting|Sommaire]] | [[10 - Débogage]] →
