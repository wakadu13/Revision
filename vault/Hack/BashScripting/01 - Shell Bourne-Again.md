---
tags:
  - bash-scripting
ordre: 1
---

# Shell Bourne-Again

---

[Bash](https://en.wikipedia.org/wiki/Bash_\(Unix_shell\)) est le langage de script que nous utilisons pour communiquer avec les systèmes d'exploitation basés sur Unix et pour donner des commandes au système. Depuis mai 2019, Windows fournit un [Sous-système Windows pour Linux (Windows Subsystem for Linux)](https://docs.microsoft.com/en-us/windows/wsl/about) qui nous permet d'utiliser `Bash` dans un environnement Windows. Il est essentiel de maîtriser ce langage pour travailler efficacement avec. La principale différence entre les langages de script et les langages de programmation est que nous n'avons pas besoin de compiler le code pour exécuter le langage de script, contrairement aux langages de programmation.

En tant que testeurs d'intrusion (penetration testers), nous devons être capables de travailler avec n'importe quel système d'exploitation, qu'il soit basé sur Windows ou Unix. L'efficacité dépend principalement de la connaissance des systèmes, en particulier dans le domaine de l'escalade de privilèges (privilege escalation). Sur les systèmes basés sur Unix, il est essentiel d'apprendre à utiliser le terminal, à filtrer les données et à automatiser ces processus. Surtout dans les grands réseaux d'entreprise basés sur Unix, nous aurons à traiter de grandes quantités de données. Nous devons trier et filtrer en conséquence pour déterminer les failles et informations potentielles le plus rapidement possible.

Il est également essentiel d'apprendre à combiner plusieurs commandes et à travailler avec des résultats individuels. C'est là que le scripting entre en jeu, augmentant notre vitesse et notre efficacité. Comme un langage de programmation, un langage de script a presque la même structure, qui peut être divisée en :

- `Entrées` & `Sorties`
- `Arguments`, `Variables` & `Tableaux`
- `Exécution conditionnelle`
- `Arithmétique`
- `Boucles`
- `Opérateurs de comparaison`
- `Fonctions`

Il est souvent courant d'automatiser certains processus pour ne pas les répéter tout le temps ou pour traiter et filtrer une grande quantité d'informations. En général, un script ne crée pas de processus, mais il est exécuté par l'interpréteur qui exécute le script, dans ce cas, `Bash`. Pour exécuter un script, nous devons spécifier l'interpréteur и lui indiquer quel script il doit traiter. Un tel appel ressemble à ceci :

#### Exécution de Script - Exemples

```bash
Hiterof13@htb[/htb]$ bash script.sh <optional arguments>
```

```bash
Hiterof13@htb[/htb]$ sh script.sh <optional arguments>
```

```bash
Hiterof13@htb[/htb]$ ./script.sh <optional arguments>
```

Regardons un tel script et voyons comment il peut être créé pour obtenir des résultats spécifiques. Si nous exécutons ce script et spécifions un domaine, nous voyons quelles informations ce script fournit.

#### CIDR.sh

```bash
Hiterof13@htb[/htb]$ ./CIDR.sh inlanefreight.com

Discovered IP address(es):
165.22.119.202

Additional options available:
    1) Identify the corresponding network range of target domain.
    2) Ping discovered hosts.
    3) All checks.
    *) Exit.

Select your option: 3

NetRange for 165.22.119.202:
NetRange:       165.22.0.0 - 165.22.255.255
CIDR:           165.22.0.0/16

Pinging host(s):
165.22.119.202 is up.

1 out of 1 hosts are up.
```

Maintenant, examinons ce script en détail et lisons-le ligne par ligne de la meilleure façon possible. Dans les sections suivantes, nous examinerons et analyserons toutes les parties de ce script.

#### CIDR.sh

```bash
#!/bin/bash

# Check for given arguments
if [ $# -eq 0 ]
then
    echo -e "You need to specify the target domain.\n"
    echo -e "Usage:"
    echo -e "\t$0 <domain>"
    exit 1
else
    domain=$1
fi

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

# Ping discovered IP address(es)
function ping_host {
    hosts_up=0
    hosts_total=0

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

    echo -e "\n$hosts_up out of $hosts_total hosts are up."
}

# Identify IP address of the specified domain
hosts=$(host $domain | grep "has address" | cut -d" " -f4 | tee discovered_hosts.txt)

echo -e "Discovered IP address:\n$hosts\n"
ipaddr=$(host $domain | grep "has address" | cut -d" " -f4 | tr "\n" " ")

# Available options
echo -e "Additional options available:"
echo -e "\t1) Identify the corresponding network range of target domain."
echo -e "\t2) Ping discovered hosts."
echo -e "\t3) All checks."
echo -e "\t*) Exit.\n"

read -p "Select your option: " opt

case $opt in
    "1") network_range ;;
    "2") ping_host ;;
    "3") network_range && ping_host ;;
    "*") exit 0 ;;
esac
```

---

Comme nous pouvons le voir, nous avons commenté ici plusieurs parties du script en lesquelles nous pouvons le diviser.

1. Vérification des arguments fournis
2. Identification de la plage réseau pour la ou les adresses IP spécifiées
3. Ping des adresses IP découvertes
4. Identification de la ou des adresses IP du domaine spécifié
5. Options disponibles

---

#### 1. Vérification des arguments fournis

Dans la première partie du script, nous avons une instruction if-else qui vérifie si nous avons spécifié un domaine représentant l'entreprise cible.

---

#### 2. Identification de la plage réseau pour la ou les adresses IP spécifiées

Ici, nous avons créé une fonction qui effectue une requête « whois » pour chaque adresse IP, affiche la ligne correspondant à la plage réseau réservée et la stocke dans le fichier CIDR.txt.

---

#### 3. Ping des adresses IP découvertes

Cette fonction supplémentaire est utilisée pour vérifier si les hôtes trouvés sont joignables avec leurs adresses IP respectives. Avec la boucle For (For-Loop), nous envoyons un ping à chaque adresse IP de la plage réseau et comptons les résultats.

---

#### 4. Identification de la ou des adresses IP du domaine spécifié

Comme première étape de ce script, nous identifions l'adresse IPv4 du domaine qui nous est retournée.

---

#### 5. Options disponibles

Ensuite, nous décidons quelles fonctions nous voulons utiliser pour obtenir plus d'informations sur l'infrastructure.
---

[[00 - Sommaire Bash Scripting|Sommaire]] | [[02 - Exécution conditionnelle]] →
