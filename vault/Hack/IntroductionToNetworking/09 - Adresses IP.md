---
tags:
  - networking
ordre: 9
---

# Adresses IP

---

Chaque hôte situé dans le réseau peut être identifié par ce qu'on appelle l'adresse `Media Access Control` (`MAC`). Cela permettrait l'échange de données au sein de ce même réseau. Si l'hôte distant est situé dans un autre réseau, la connaissance de l'adresse `MAC` ne suffit pas à établir une connexion. L'adressage sur Internet se fait via l'adresse `IPv4` et/ou `IPv6`, qui se compose de l'`adresse réseau` (network address) et de l'`adresse d'hôte` (host address).

Peu importe qu'il s'agisse d'un petit réseau, comme un réseau informatique domestique, ou de l'Internet dans son ensemble. L'adresse IP assure la livraison des données au bon destinataire. On peut se représenter les adresses `MAC` et `IPv4` / `IPv6` de la manière suivante :

- `IPv4` / `IPv6` - décrit l'adresse postale unique et le quartier du bâtiment du destinataire.
- `MAC` - décrit l'étage et l'appartement exacts du destinataire.

Il est possible qu'une seule adresse IP s'adresse à plusieurs destinataires (diffusion ou broadcasting) ou qu'un appareil réponde à plusieurs adresses IP. Cependant, il faut s'assurer que chaque adresse IP n'est attribuée qu'une seule fois au sein du réseau.

---

## Structure IPv4

La méthode la plus courante d'attribution d'adresses IP est l'`IPv4`, qui consiste en un nombre binaire de `32` bits regroupé en `4 octets` (bytes) de `8` bits chacun (`octets`) allant de `0` à `255`. Ceux-ci sont convertis en nombres décimaux plus faciles à lire, séparés par des points et représentés en notation décimale pointée (dotted-decimal notation).

Une adresse IPv4 peut donc ressembler à ceci :

|**Notation**|**Présentation**|
|---|---|
|Binaire|0111 1111.0000 0000.0000 0000.0000 0001|
|Décimal|127.0.0.1|

Chaque interface réseau (cartes réseau, imprimantes réseau ou routeurs) se voit attribuer une adresse IP unique.

Le format `IPv4` permet 4 294 967 296 adresses uniques. L'adresse IP est divisée en une `partie hôte` (host part) et une `partie réseau` (network part). Le `routeur` attribue la `partie hôte` de l'adresse IP à la maison ou par un administrateur. L'`administrateur réseau` respectif attribue la `partie réseau`. Sur Internet, c'est l'`IANA` qui alloue et gère les adresses IP uniques.

Par le passé, une classification plus poussée était effectuée. Les blocs de réseaux IP étaient divisés en `classes A à E`. Les différentes classes se distinguaient par la longueur respective des parties hôte et réseau.

|**`Classe`**|**Adresse Réseau**|**Première Adresse**|**Dernière Adresse**|**Masque de sous-réseau**|**CIDR**|**Sous-réseaux**|**IPs**|
|---|---|---|---|---|---|---|---|
|`A`|1.0.0.0|1.0.0.1|127.255.255.255|255.0.0.0|/8|127|16,777,214 + 2|
|`B`|128.0.0.0|128.0.0.1|191.255.255.255|255.255.0.0|/16|16,384|65,534 + 2|
|`C`|192.0.0.0|192.0.0.1|223.255.255.255|255.255.255.0|/24|2,097,152|254 + 2|
|`D`|224.0.0.0|224.0.0.1|239.255.255.255|Multidiffusion|Multidiffusion|Multidiffusion|Multidiffusion|
|`E`|240.0.0.0|240.0.0.1|255.255.255.255|réservé|réservé|réservé|réservé|

---

## Masque de sous-réseau

Une séparation plus poussée de ces classes en plus petits réseaux est réalisée à l'aide du `découpage en sous-réseaux` (subnetting). Cette séparation se fait à l'aide des `masques de réseau` (netmasks), qui ont la même longueur qu'une adresse IPv4. Comme pour les classes, il décrit quelles positions de bits dans l'adresse IP agissent comme `partie réseau` ou `partie hôte`.

|**Classe**|**Adresse Réseau**|**Première Adresse**|**Dernière Adresse**|**`Masque de sous-réseau`**|**CIDR**|**Sous-réseaux**|**IPs**|
|---|---|---|---|---|---|---|---|
|**A**|1.0.0.0|1.0.0.1|127.255.255.255|`255.0.0.0`|/8|127|16,777,214 + 2|
|**B**|128.0.0.0|128.0.0.1|191.255.255.255|`255.255.0.0`|/16|16,384|65,534 + 2|
|**C**|192.0.0.0|192.0.0.1|223.255.255.255|`255.255.255.0`|/24|2,097,152|254 + 2|
|**D**|224.0.0.0|224.0.0.1|239.255.255.255|`Multidiffusion`|Multidiffusion|Multidiffusion|Multidiffusion|
|**E**|240.0.0.0|240.0.0.1|255.255.255.255|`réservé`|réservé|réservé|réservé|

---

## Adresses de réseau et de passerelle

Les `deux` `IPs` supplémentaires ajoutées dans la `colonne IPs` sont réservées à ce que l'on appelle l'`adresse réseau` et l'`adresse de diffusion` (broadcast address). Un autre rôle important est joué par la `passerelle par défaut` (default gateway), qui est le nom de l'adresse IPv4 du `routeur` qui relie les réseaux et les systèmes avec des protocoles différents et gère les adresses et les méthodes de transmission. Il est courant que la `passerelle par défaut` se voie attribuer la première ou la dernière adresse IPv4 assignable dans un sous-réseau. Il ne s'agit pas d'une exigence technique, mais c'est devenu une norme de facto dans les environnements réseau de toutes tailles.

|**Classe**|**Adresse Réseau**|**`Première Adresse`**|**Dernière Adresse**|**Masque de sous-réseau**|**CIDR**|**Sous-réseaux**|**`IPs`**|
|---|---|---|---|---|---|---|---|
|A|1.0.0.0|`1.0.0.1`|127.255.255.255|255.0.0.0|/8|127|16,777,214 `+ 2`|
|B|128.0.0.0|`128.0.0.1`|191.255.255.255|255.255.0.0|/16|16,384|65,534 `+ 2`|
|C|192.0.0.0|`192.0.0.1`|223.255.255.255|255.255.255.0|/24|2,097,152|254 `+ 2`|
|D|224.0.0.0|`224.0.0.1`|239.255.255.255|Multidiffusion|Multidiffusion|Multidiffusion|Multidiffusion|
|E|240.0.0.0|`240.0.0.1`|255.255.255.255|réservé|réservé|réservé|réservé|

---

## Adresse de diffusion

La tâche de l'adresse IP de `diffusion` (broadcast) est de connecter tous les appareils d'un réseau entre eux. Une `diffusion` dans un réseau est un message qui est transmis à tous les participants d'un réseau et qui ne nécessite aucune réponse. De cette manière, un hôte envoie un paquet de données à tous les autres participants du réseau simultanément et, ce faisant, communique son `adresse IP`, que les destinataires peuvent utiliser pour le contacter. C'est la `dernière adresse IPv4` qui est utilisée pour la `diffusion`.

|**Classe**|**Adresse Réseau**|**Première Adresse**|**`Dernière Adresse`**|**Masque de sous-réseau**|**CIDR**|**Sous-réseaux**|**IPs**|
|---|---|---|---|---|---|---|---|
|A|1.0.0.0|1.0.0.1|`127.255.255.255`|255.0.0.0|/8|127|16,777,214 + 2|
|B|128.0.0.0|128.0.0.1|`191.255.255.255`|255.255.0.0|/16|16,384|65,534 + 2|
|C|192.0.0.0|192.0.0.1|`223.255.255.255`|255.255.255.0|/24|2,097,152|254 + 2|
|D|224.0.0.0|224.0.0.1|`239.255.255.255`|Multidiffusion|Multidiffusion|Multidiffusion|Multidiffusion|
|E|240.0.0.0|240.0.0.1|`255.255.255.255`|réservé|réservé|réservé|réservé|

---

## Système binaire

Le système binaire est un système de numération qui n'utilise que deux états différents, représentés par deux chiffres (`0` et `1`), contrairement au système décimal (0 à 9).

Une adresse IPv4 est divisée en 4 octets, comme nous l'avons déjà vu. Chaque `octet` se compose de `8 bits`. Chaque position d'un bit dans un octet a une valeur décimale spécifique. Prenons l'adresse IPv4 suivante comme exemple :

- Adresse IPv4 : `192.168.10.39`

Voici un exemple de ce à quoi ressemble le `premier octet` :

#### 1er Octet - Valeur : 192

```bash
Valeurs:        128  64  32  16  8  4  2  1
Binaire:          1   1   0   0  0  0  0  0
```

Si nous calculons la somme de toutes ces valeurs pour chaque octet où le bit est à `1`, nous obtenons la somme :

|**Octet**|**Valeurs**|**Somme**|
|---|---|---|
|1er|128 + 64 + 0 + 0 + 0 + 0 + 0 + 0|= `192`|
|2e|128 + 0 + 32 + 0 + 8 + 0 + 0 + 0|= `168`|
|3e|0 + 0 + 0 + 0 + 8 + 0 + 2 + 0|= `10`|
|4e|0 + 0 + 32 + 0 + 0 + 4 + 2 + 1|= `39`|

La représentation complète du binaire au décimal ressemblerait à ceci :

#### IPv4 - Notation Binaire

```bash
Octet:             1er         2e          3e          4e
Binaire:        1100 0000 . 1010 1000 . 0000 1010 . 0010 0111
Décimal:           192    .    168    .     10    .     39
```

- Adresse IPv4 : `192.168.10.39`

Cette addition a lieu pour chaque octet, ce qui donne une représentation décimale de l'`adresse IPv4`. Le masque de sous-réseau est calculé de la même manière.

#### IPv4 - Décimal vers Binaire

```bash
Valeurs:        128  64  32  16  8  4  2  1
Binaire:          1   1   1   1  1  1  1  1
```

|**Octet**|**Valeurs**|**Somme**|
|---|---|---|
|1er|128 + 64 + 32 + 16 + 8 + 4 + 2 + 1|= `255`|
|2e|128 + 64 + 32 + 16 + 8 + 4 + 2 + 1|= `255`|
|3e|128 + 64 + 32 + 16 + 8 + 4 + 2 + 1|= `255`|
|4e|0 + 0 + 0 + 0 + 0 + 0 + 0 + 0|= `0`|

#### Masque de sous-réseau

```bash
Octet:             1er         2e          3e          4e
Binaire:        1111 1111 . 1111 1111 . 1111 1111 . 0000 0000
Décimal:           255    .    255    .    255    .     0
```

- Adresse IPv4 : `192.168.10.39`
- Masque de sous-réseau : `255.255.255.0`

---

## CIDR

Le `routage inter-domaine sans classe` (`Classless Inter-Domain Routing` ou `CIDR`) est une méthode de représentation qui remplace l'assignation fixe entre l'adresse IPv4 et les classes de réseau (A, B, C, D, E). La division est basée sur le masque de sous-réseau ou ce que l'on appelle le `suffixe CIDR`, qui permet la division au niveau du bit de l'espace d'adressage IPv4 et donc en `sous-réseaux` de n'importe quelle taille. Le `suffixe CIDR` indique combien de bits au début de l'adresse IPv4 appartiennent au réseau. C'est une notation qui représente le `masque de sous-réseau` en spécifiant le nombre de bits à `1` dans le masque de sous-réseau.

Reprenons l'adresse IPv4 et le masque de sous-réseau suivants comme exemple :

- Adresse IPv4 : `192.168.10.39`
- Masque de sous-réseau : `255.255.255.0`

La représentation complète de l'adresse IPv4 et du masque de sous-réseau ressemblerait alors à ceci :

- CIDR : `192.168.10.39/24`

Le suffixe CIDR est donc la somme de tous les uns dans le masque de sous-réseau.

```bash
Octet:             1er         2e          3e          4e
Binaire:        1111 1111 . 1111 1111 . 1111 1111 . 0000 0000 (/24)
Décimal:           255    .    255    .    255    .     0
```

---

← [[08 - Couche Réseau]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[10 - Segmentation en sous-réseaux]] →
