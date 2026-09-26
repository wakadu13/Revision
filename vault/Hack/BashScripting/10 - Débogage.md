---
tags:
  - bash-scripting
ordre: 10
---

# Débogage

---

Bash nous offre une excellente occasion de trouver, de suivre et de corriger les erreurs dans notre code. Le terme `debugging` (débogage) peut avoir de nombreuses significations différentes. Néanmoins, le [débogage Bash](https://tldp.org/LDP/Bash-Beginners-Guide/html/sect_02_03.html) est le processus qui consiste à supprimer les erreurs (bogues) de notre code. Le débogage peut être effectué de plusieurs manières. Par exemple, nous pouvons utiliser notre code pour le débogage afin de vérifier les fautes de frappe, ou nous pouvons l'utiliser pour l'analyse de code afin de les suivre et de déterminer pourquoi des erreurs spécifiques se produisent.

Ce processus est également utilisé pour trouver des vulnérabilités dans les programmes. Par exemple, nous pouvons essayer de provoquer des erreurs en utilisant différents types d'entrées et suivre leur traitement dans le processeur (CPU) via l'assembleur, ce qui peut fournir un moyen de manipuler le traitement de ces erreurs pour insérer notre propre code et forcer le système à l'exécuter. Ce sujet sera traité et discuté en détail dans d'autres modules. Bash nous permet de déboguer notre code en utilisant les options « `-x` » (`xtrace`) et « `-v` ». Voyons maintenant un exemple avec notre script `CIDR.sh`.

#### CIDR.sh - Débogage

```bash
Hiterof13@htb[/htb]$ bash -x CIDR.sh

+ '[' 0 -eq 0 ']'
+ echo -e 'You need to specify the target domain.\n'
You need to specify the target domain.

+ echo -e Usage:
Usage:
+ echo -e '\tCIDR.sh <domain>'
    CIDR.sh <domain>
+ exit 1
```

Ici, Bash nous montre précisément quelle fonction ou commande a été exécutée et avec quelles valeurs. Ceci est indiqué par le signe plus (`+`) au début de la ligne. Si nous voulons voir tout le code d'une fonction particulière, nous pouvons définir l'option « `-v` » qui affiche la sortie de manière plus détaillée.

#### CIDR.sh - Débogage verbeux

```bash
Hiterof13@htb[/htb]$ bash -x -v CIDR.sh

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
+ '[' 0 -eq 0 ']'
+ echo -e 'You need to specify the target domain.\n'
You need to specify the target domain.

+ echo -e Usage:
Usage:
+ echo -e '\tCIDR.sh <domain>'
    CIDR.sh <domain>
+ exit 1
```

Par rapport au débogage normal, nous voyons toute la section de code qui a été traitée jusqu'à présent, puis les étapes individuelles qui ont été suivies.

## Connect to HTB
---

← [[09 - Fonctions]] | [[00 - Sommaire Bash Scripting|Sommaire]]
