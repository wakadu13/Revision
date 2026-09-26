---
tags:
  - bash-scripting
ordre: 6
---

# Entrées et Sorties

---

## Contrôle des Entrées

Il se peut que nous obtenions des résultats de nos requêtes envoyées et des commandes exécutées, pour lesquels nous devons décider manuellement de la marche à suivre. Un autre exemple serait d'avoir défini plusieurs fonctions dans notre script, conçues pour différents scénarios. Nous devons décider lesquelles d'entre elles doivent être exécutées après une vérification manuelle et en fonction des résultats. Il est également tout à fait possible que des scans ou des activités spécifiques ne soient pas autorisés. Par conséquent, nous devons savoir comment faire en sorte qu'un script en cours d'exécution attende nos instructions. Si nous examinons à nouveau notre script `CIDR.sh`, nous voyons que nous avons ajouté un tel appel pour décider des étapes suivantes.

#### CIDR.sh

```bash
# Options disponibles
<SNIP>
echo -e "Options supplémentaires disponibles :"
echo -e "\t1) Identifier la plage réseau correspondante du domaine cible."
echo -e "\t2) Pinger les hôtes découverts."
echo -e "\t3) Toutes les vérifications."
echo -e "\t*) Quitter.\n"

read -p "Sélectionnez votre option : " opt

case $opt in
    "1") network_range ;;
    "2") ping_host ;;
    "3") network_range && ping_host ;;
    "*") exit 0 ;;
esac
```

Les premières lignes `echo` servent de menu d'affichage pour les options qui s'offrent à nous. Avec la commande `read`, la ligne « `Select your option:` » s'affiche, et l'option supplémentaire `-p` garantit que notre saisie reste sur la même ligne. Notre saisie est stockée dans la variable `opt`, que nous utilisons ensuite pour exécuter les fonctions correspondantes avec l'instruction `case`, que nous examinerons plus tard. Selon le numéro que nous saisissons, l'instruction `case` détermine quelles fonctions sont exécutées.

---

## Contrôle des Sorties

Nous avons déjà étudié les redirections de sortie dans le module `Principes de base de Linux`. Néanmoins, le problème avec les redirections est que nous n'obtenons aucune sortie de la commande respective. Elle sera redirigée vers le fichier approprié. Si nos scripts deviennent plus compliqués par la suite, ils peuvent prendre beaucoup plus de temps que quelques secondes. Pour éviter de rester inactif à attendre les résultats de notre script, nous pouvons utiliser l'utilitaire [tee](https://man7.org/linux/man-pages/man1/tee.1.html). Il garantit que nous voyons les résultats que nous obtenons immédiatement et qu'ils sont stockés dans les fichiers correspondants. Dans notre script `CIDR.sh`, nous avons utilisé cet utilitaire deux fois de différentes manières.

#### CIDR.sh

```bash
<SNIP>

# Identifier la plage réseau pour la ou les adresses IP spécifiées
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

# Identifier l'adresse IP du domaine spécifié
hosts=$(host $domain | grep "has address" | cut -d" " -f4 | tee discovered_hosts.txt)

<SNIP>
```

Lorsque nous utilisons `tee`, nous transférons la sortie reçue et utilisons le pipe (`|`) pour la transmettre à `tee`. Le paramètre « `-a` / `--append` » garantit que le fichier spécifié n'est pas écrasé, mais complété par les nouveaux résultats. En même temps, il nous montre les résultats tels qu'ils se trouveront dans le fichier.

```bash
Hiterof13@htb[/htb]$ cat discovered_hosts.txt CIDR.txt

165.22.119.202
NetRange:       165.22.0.0 - 165.22.255.255
CIDR:           165.22.0.0/16
```

---

← [[05 - Arithmétique]] | [[00 - Sommaire Bash Scripting|Sommaire]] | [[07 - Contrôle de flux - Boucles]] →
