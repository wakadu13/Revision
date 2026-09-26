---
tags:
  - bash-scripting
ordre: 7
---

# Contrôle de flux - Boucles

---

Le contrôle du flux de nos scripts est essentiel. Nous avons déjà abordé les conditions `if-else`, qui font également partie du contrôle de flux. Après tout, nous voulons que notre script fonctionne rapidement et efficacement. Pour cela, nous pouvons utiliser d'autres composants pour augmenter l'efficacité et permettre un traitement sans erreur. Chaque structure de contrôle est soit une `branche` (branch), soit une `boucle` (loop). Les expressions logiques de valeurs booléennes contrôlent généralement l'exécution d'une structure de contrôle. Ces structures de contrôle incluent :

- Branches :
    - Conditions `If-Else`
    - Instructions `Case`
- Boucles :
    - Boucles `For`
    - Boucles `While`
    - Boucles `Until`

---

## Boucles For

Commençons par les boucles `For`. La boucle `For` est exécutée à chaque passage pour précisément un paramètre, que le shell prend dans une liste, calcule à partir d'un incrément, ou récupère d'une autre source de données. La boucle for s'exécute tant qu'elle trouve des données correspondantes. Ce type de boucle peut être structuré et défini de différentes manières. Par exemple, les boucles `for` sont souvent utilisées lorsque nous devons travailler avec de nombreuses valeurs différentes provenant d'un `tableau` (array). Cela peut être utilisé pour scanner différents hôtes ou ports. Nous pouvons également l'utiliser pour exécuter des commandes spécifiques sur des ports et services connus afin d'accélérer notre processus d'énumération. La syntaxe peut être la suivante :

#### Syntaxe - Exemples

```bash
for variable in 1 2 3 4
do
    echo $variable
done
```

```bash
for variable in file1 file2 file3
do
    echo $variable
done
```

```bash
for ip in 10.10.10.170 10.10.10.174 10.10.10.175
do
    ping -c 1 $ip
done
```

Bien sûr, nous pouvons aussi écrire ces commandes sur une seule ligne. Une telle commande ressemblerait à ceci :

```bash
Hiterof13@htb[/htb]$ for ip in 10.10.10.170 10.10.10.174;do ping -c 1 $ip;done

PING 10.10.10.170 (10.10.10.170): 56 data bytes
64 bytes from 10.10.10.170: icmp_seq=0 ttl=63 time=42.106 ms

--- 10.10.10.170 ping statistics ---
1 packets transmitted, 1 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 42.106/42.106/42.106/0.000 ms
PING 10.10.10.174 (10.10.10.174): 56 data bytes
64 bytes from 10.10.10.174: icmp_seq=0 ttl=63 time=45.700 ms

--- 10.10.10.174 ping statistics ---
1 packets transmitted, 1 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 45.700/45.700/45.700/0.000 ms
```

---

Jetons un autre coup d'œil à notre script `CIDR.sh`. Nous avons ajouté plusieurs boucles `for` au script, mais concentrons-nous sur cette petite section de code.

#### CIDR.sh

```bash
<SNIP>

# Identify Network range for the specified IP address(es)
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

Comme dans l'exemple précédent, pour chaque adresse IP du tableau "`ipaddr`", nous effectuons une requête "`whois`", dont la sortie est filtrée sur "`NetRange`" et "`CIDR`". Cela nous aide à déterminer dans quelle plage d'adresses se trouve notre cible. Nous pouvons utiliser ces informations pour rechercher des hôtes supplémentaires lors d'un test d'intrusion (penetration test), `si le client l'a approuvé`. Les résultats que nous recevons sont affichés en conséquence et stockés dans le fichier "`CIDR.txt`".

---

## Boucles While

La boucle `while` est conceptuellement simple et suit le principe suivant :

- Une instruction est exécutée tant qu'une condition est remplie (`true`).

Nous pouvons également combiner des boucles et fusionner leur exécution avec différentes valeurs. Il est important de noter que la combinaison excessive de plusieurs boucles imbriquées peut rendre le code très peu clair et entraîner des erreurs difficiles à trouver et à suivre. Une telle combinaison peut ressembler à celle de notre script `CIDR.sh`.

#### CIDR.sh

```bash
<SNIP>
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
<SNIP>
```

Les boucles `while` fonctionnent également avec des conditions comme `if-else`. Une boucle `while` a besoin d'une sorte de compteur pour savoir quand elle doit arrêter d'exécuter les commandes qu'elle contient. Sinon, cela conduit à une boucle infinie. Un tel compteur peut être une variable que nous avons déclarée avec une valeur spécifique ou une valeur booléenne. Les boucles `While` s'exécutent tant que la valeur booléenne est "`True`". Outre le compteur, nous pouvons également utiliser la commande "`break`", qui interrompt la boucle lorsqu'elle est atteinte, comme dans l'exemple suivant :

#### WhileBreaker.sh

```bash
#!/bin/bash

counter=0

while [ $counter -lt 10 ]
do
  # Increase $counter by 1
  ((counter++))
  echo "Counter: $counter"

  if [ $counter == 2 ]
  then
    continue
  elif [ $counter == 4 ]
  then
    break
  fi
done
```

#### WhileBreaker.sh

```bash
Hiterof13@htb[/htb]$ ./WhileBreaker.sh

Counter: 1
Counter: 2
Counter: 3
Counter: 4
```

---

## Boucles Until

Il existe aussi la boucle `until`, qui est relativement rare. Néanmoins, la boucle `until` fonctionne exactement comme la boucle `while`, mais avec la différence suivante :

- Le code à l'intérieur d'une boucle `until` est exécuté tant que la condition particulière est `false`.

L'autre manière est de laisser la boucle s'exécuter jusqu'à ce que la valeur souhaitée soit atteinte. Les boucles "`until`" sont très bien adaptées à cela. Ce type de boucle fonctionne de manière similaire à la boucle "`while`" mais, comme déjà mentionné, avec la différence qu'elle s'exécute jusqu'à ce que la valeur booléenne soit "`False`".

#### Until.sh

```bash
#!/bin/bash

counter=0

until [ $counter -eq 10 ]
do
  # Increase $counter by 1
  ((counter++))
  echo "Counter: $counter"
done
```

#### Until.sh

```bash
Hiterof13@htb[/htb]$ ./Until.sh

Counter: 1
Counter: 2
Counter: 3
Counter: 4
Counter: 5
Counter: 6
Counter: 7
Counter: 8
Counter: 9
Counter: 10
```

---

---

## Script d'exercice

```bash
#!/bin/bash

# Decrypt function
function decrypt {
    MzSaas7k=$(echo $hash | sed 's/988sn1/83unasa/g')
    Mzns7293sk=$(echo $MzSaas7k | sed 's/4d298d/9999/g')
    MzSaas7k=$(echo $Mzns7293sk | sed 's/3i8dqos82/873h4d/g')
    Mzns7293sk=$(echo $MzSaas7k | sed 's/4n9Ls/20X/g')
    MzSaas7k=$(echo $Mzns7293sk | sed 's/912oijs01/i7gg/g')
    Mzns7293sk=$(echo $MzSaas7k | sed 's/k32jx0aa/n391s/g')
    MzSaas7k=$(echo $Mzns7293sk | sed 's/nI72n/YzF1/g')
    Mzns7293sk=$(echo $MzSaas7k | sed 's/82ns71n/2d49/g')
    MzSaas7k=$(echo $Mzns7293sk | sed 's/JGcms1a/zIm12/g')
    Mzns7293sk=$(echo $MzSaas7k | sed 's/MS9/4SIs/g')
    MzSaas7k=$(echo $Mzns7293sk | sed 's/Ymxj00Ims/Uso18/g')
    Mzns7293sk=$(echo $MzSaas7k | sed 's/sSi8Lm/Mit/g')
    MzSaas7k=$(echo $Mzns7293sk | sed 's/9su2n/43n92ka/g')
    Mzns7293sk=$(echo $MzSaas7k | sed 's/ggf3iunds/dn3i8/g')
    MzSaas7k=$(echo $Mzns7293sk | sed 's/uBz/TT0K/g')

    flag=$(echo $MzSaas7k | base64 -d | openssl enc -aes-128-cbc -a -d -salt -pass pass:$salt)
}

# Variables
var="9M"
salt=""
hash="VTJGc2RHVmtYMTl2ZnYyNTdUeERVRnBtQWVGNmFWWVUySG1wTXNmRi9rQT0K"

# Base64 Encoding Example:
#        user@htb$ echo "Some Text" | base64

# <- For-Loop here

# Check if $salt is empty
if [[ ! -z "$salt" ]]
then
    decrypt
    echo $flag
else
    exit 1
fi
```

---

← [[06 - Entrées et Sorties]] | [[00 - Sommaire Bash Scripting|Sommaire]] | [[08 - Contrôle de flux - Branchements]] →
