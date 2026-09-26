---
tags:
  - bash-scripting
ordre: 5
---

# Arithmétique

---

En Bash, nous disposons de sept `opérateurs arithmétiques` différents avec lesquels nous pouvons travailler. Ils sont utilisés pour effectuer différentes opérations mathématiques ou pour modifier certains nombres entiers.

#### Opérateurs Arithmétiques

|**Opérateur**|**Description**|
|---|---|
|`+`|Addition|
|`-`|Soustraction|
|`*`|Multiplication|
|`/`|Division|
|`%`|Modulo|
|`variable++`|Augmente la valeur de la variable de 1|
|`variable--`|Diminue la valeur de la variable de 1|

Nous pouvons résumer tous ces opérateurs dans un petit script :

#### Arithmetic.sh

```bash
#!/bin/bash

increase=1
decrease=1

echo "Addition: 10 + 10 = $((10 + 10))"
echo "Subtraction: 10 - 10 = $((10 - 10))"
echo "Multiplication: 10 * 10 = $((10 * 10))"
echo "Division: 10 / 10 = $((10 / 10))"
echo "Modulus: 10 % 4 = $((10 % 4))"

((increase++))
echo "Increase Variable: $increase"

((decrease--))
echo "Decrease Variable: $decrease"
```

La sortie de ce script ressemble à ceci :

#### Arithmetic.sh - Exécution

```bash
Hiterof13@htb[/htb]$ ./Arithmetic.sh

Addition: 10 + 10 = 20
Subtraction: 10 - 10 = 0
Multiplication: 10 * 10 = 100
Division: 10 / 10 = 1
Modulus: 10 % 4 = 2
Increase Variable: 2
Decrease Variable: 0
```

---

Nous pouvons également calculer la longueur de la variable. En utilisant la fonction `${#variable}`, chaque caractère est compté, et nous obtenons le nombre total de caractères dans la variable.

#### VarLength.sh

```bash
#!/bin/bash

htb="HackTheBox"

echo ${#htb}
```

#### VarLength.sh

```bash
Hiterof13@htb[/htb]$ ./VarLength.sh

10
```

---

Si nous examinons notre script `CIDR.sh`, nous verrons que nous avons utilisé les opérateurs d'incrémentation et de décrémentation à plusieurs reprises. Cela garantit que la boucle `while`, que nous aborderons plus tard, s'exécute et envoie des pings aux hôtes tant que la variable « `stat` » a la valeur `1`. Si la commande `ping` se termine avec le code `0` (succès), nous recevons un message indiquant que l'hôte est actif (`host is up`) et la variable « `stat` », ainsi que les variables « `hosts_up` » et « `hosts_total` », sont modifiées.

#### CIDR.sh

```bash
<SNIP>
    echo -e "\nPinging host(s):"
    for host in $cidr_ips
    do
        stat=1
        while [ $stat -eq 1 ]
        do
            ping -c 2 $host > /dev/null 2>&1
            if [ $? -eq 0 ]
            then
                echo "$host is up."
                ((stat--))
                ((hosts_up++))
                ((hosts_total++))
            else
                echo "$host is down."
                ((stat--))
                ((hosts_total++))
            fi
        done
    done
<SNIP>
```

---

← [[04 - Opérateurs de comparaison]] | [[00 - Sommaire Bash Scripting|Sommaire]] | [[06 - Entrées et Sorties]] →
