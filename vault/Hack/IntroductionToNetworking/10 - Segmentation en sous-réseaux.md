---
tags:
  - networking
ordre: 10
---

# Segmentation en sous-réseaux

---

La division d'une plage d'adresses IPv4 en plusieurs plages d'adresses plus petites est appelée `segmentation en sous-réseaux` (subnetting).

Un `sous-réseau` (subnet) est un segment logique d'un réseau qui utilise des adresses IP avec la même adresse réseau. Nous pouvons considérer un sous-réseau comme une entrée étiquetée dans le couloir d'un grand bâtiment. Par exemple, il pourrait s'agir d'une porte vitrée qui sépare différents départements dans un immeuble de bureaux. Grâce à la segmentation en sous-réseaux, nous pouvons créer nous-mêmes un sous-réseau spécifique ou déterminer les caractéristiques suivantes du réseau respectif :

- `Adresse réseau`
- `Adresse de diffusion`
- `Premier hôte`
- `Dernier hôte`
- `Nombre d'hôtes`

Prenons l'adresse IPv4 et le masque de sous-réseau suivants comme exemple :

- Adresse IPv4 : `192.168.12.160`
- Masque de sous-réseau : `255.255.255.192`
- CIDR : `192.168.12.160/26`

---

Nous savons déjà qu'une adresse IP est divisée en une `partie réseau` (network part) et une `partie hôte` (host part).

#### Partie réseau

|**Détails de**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**Décimal**|
|---|---|---|---|---|---|
|IPv4|`1100 0000`|`1010 1000`|`0000 1100`|`10`10 0000|192.168.12.160`/26`|
|Masque de sous-réseau|`1111 1111`|`1111 1111`|`1111 1111`|`11`00 0000|`255.255.255.192`|
|Bits|/8|/16|/24|/32||

Dans la segmentation en sous-réseaux, nous utilisons le masque de sous-réseau comme modèle pour l'adresse IPv4. À partir des bits à `1` dans le masque de sous-réseau, nous savons quels bits de l'adresse IPv4 `ne peuvent pas` être modifiés. Ceux-ci sont `fixes` et déterminent donc le « réseau principal » dans lequel se trouve le sous-réseau.

#### Partie hôte

|**Détails de**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**Décimal**|
|---|---|---|---|---|---|
|IPv4|1100 0000|1010 1000|0000 1100|10`10 0000`|192.168.12.160/26|
|Masque de sous-réseau|1111 1111|1111 1111|1111 1111|11`00 0000`|255.255.255.192|
|Bits|/8|/16|/24|/32||

Les bits de la `partie hôte` peuvent être modifiés pour obtenir la `première` et la `dernière` adresse. La première adresse est l'`adresse réseau`, et la dernière est l'`adresse de diffusion` (broadcast address) du sous-réseau respectif.

L'`adresse réseau` est essentielle pour la livraison d'un paquet de données. Si l'`adresse réseau` est la même pour l'adresse source et l'adresse de destination, le paquet de données est livré au sein du même sous-réseau. Si les adresses réseau sont différentes, le paquet de données doit être acheminé vers un autre sous-réseau via la `passerelle par défaut` (default gateway).

Le `masque de sous-réseau` détermine où cette séparation se produit.

#### Séparation des parties réseau et hôte

|**Détails de**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**Décimal**|
|---|---|---|---|---|---|
|IPv4|1100 0000|1010 1000|0000 1100|10`\|`10 0000|192.168.12.160/26|
|Masque de sous-réseau|`1111 1111`|`1111 1111`|`1111 1111`|`11\|`00 0000|255.255.255.192|
|Bits|/8|/16|/24|/32||

---

#### Adresse réseau

Ainsi, si nous mettons maintenant tous les bits à `0` dans la `partie hôte` de l'adresse IPv4, nous obtenons l'`adresse réseau` du sous-réseau correspondant.

|**Détails de**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**Décimal**|
|---|---|---|---|---|---|
|IPv4|1100 0000|1010 1000|0000 1100|10`\|00 0000`|`192.168.12.128`/26|
|Masque de sous-réseau|`1111 1111`|`1111 1111`|`1111 1111`|`11\|`00 0000|255.255.255.192|
|Bits|/8|/16|/24|/32||

---

#### Adresse de diffusion

Si nous mettons tous les bits de la `partie hôte` de l'adresse IPv4 à `1`, nous obtenons l'`adresse de diffusion`.

|**Détails de**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**Décimal**|
|---|---|---|---|---|---|
|IPv4|1100 0000|1010 1000|0000 1100|10`\|11 1111`|`192.168.12.191`/26|
|Masque de sous-réseau|`1111 1111`|`1111 1111`|`1111 1111`|`11\|`00 0000|255.255.255.192|
|Bits|/8|/16|/24|/32||

Puisque nous savons maintenant que les adresses IPv4 `192.168.12.128` et `192.168.12.191` sont attribuées, toutes les autres adresses IPv4 se situent donc entre `192.168.12.129-190`. Nous savons maintenant que ce sous-réseau nous offre un total de `64 - 2` (adresse réseau et adresse de diffusion) soit `62` adresses IPv4 que nous pouvons assigner à nos hôtes.

|**Hôtes**|**IPv4**|
|---|---|
|Adresse réseau|`192.168.12.128`|
|Premier hôte|`192.168.12.129`|
|Autres hôtes|`...`|
|Dernier hôte|`192.168.12.190`|
|Adresse de diffusion|`192.168.12.191`|

---

## Segmentation en réseaux plus petits

Supposons maintenant que, en tant qu'administrateurs, nous ayons reçu la tâche de diviser le sous-réseau qui nous a été attribué en 4 sous-réseaux supplémentaires. Ainsi, il est essentiel de savoir que nous ne pouvons diviser les sous-réseaux qu'en nous basant sur le système binaire.

|**Exposant**|**Valeur**|
|---|---|
|2`^0`|= 1|
|2`^1`|= 2|
|2`^2`|= 4|
|2`^3`|= 8|
|2`^4`|= 16|
|2`^5`|= 32|
|2`^6`|= 64|
|2`^7`|= 128|
|2`^8`|= 256|

---

Par conséquent, nous pouvons diviser les `64 hôtes` que nous connaissons par `4`. Le `4` est égal à l'exposant 2`^2` dans le système binaire, nous découvrons ainsi le nombre de bits par lequel nous devons étendre le masque de sous-réseau. Nous connaissons donc les paramètres suivants :

- Sous-réseau : `192.168.12.128/26`
- Sous-réseaux requis : `4`

Nous augmentons/étendons maintenant notre masque de sous-réseau de `2 bits`, passant de `/26` à `/28`, et cela ressemble à ceci :

|**Détails de**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**Décimal**|
|---|---|---|---|---|---|
|IPv4|1100 0000|1010 1000|0000 1100|1000`\|` 0000|192.168.12.128`/28`|
|Masque de sous-réseau|`1111 1111`|`1111 1111`|`1111 1111`|`1111\|` 0000|`255.255.255.240`|
|Bits|/8|/16|/24|/32||

Ensuite, nous pouvons diviser les `64` adresses IPv4 dont nous disposons en `4 parties` :

|**Hôtes**|**Calcul**|**Sous-réseaux**|**Plage d'hôtes pour chaque sous-réseau**|
|---|---|---|---|
|64|/|4|= `16`|

Nous savons donc quelle sera la taille de chaque sous-réseau. À partir de maintenant, nous partons de l'adresse réseau qui nous a été donnée (192.168.12.128) et nous ajoutons les `16` hôtes `4` fois :

|**N° de sous-réseau**|**Adresse réseau**|**Premier hôte**|**Dernier hôte**|**Adresse de diffusion**|**CIDR**|
|---|---|---|---|---|---|
|1|`192.168.12.128`|192.168.12.129|192.168.12.142|`192.168.12.143`|192.168.12.128/28|
|2|`192.168.12.144`|192.168.12.145|192.168.12.158|`192.168.12.159`|192.168.12.144/28|
|3|`192.168.12.160`|192.168.12.161|192.168.12.174|`192.168.12.175`|192.168.12.160/28|
|4|`192.168.12.176`|192.168.12.177|192.168.12.190|`192.168.12.191`|192.168.12.176/28|

---

## Calcul mental de sous-réseaux

La segmentation en sous-réseaux peut sembler impliquer beaucoup de calculs, mais chaque octet se répète et tout est une puissance de deux, il n'y a donc pas besoin de beaucoup mémoriser. La première chose à faire est d'identifier quel octet change.

|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|
|---|---|---|---|
|/8|/16|/24|/32|

Il est possible d'identifier quel octet de l'adresse IP peut changer en se souvenant de ces quatre nombres. Étant donné l'adresse réseau : `192.168.1.1/25`, il est immédiatement évident que 192.168.2.4 ne serait pas dans le même réseau car le sous-réseau en `/25` signifie que seul le quatrième octet peut changer.

La partie suivante identifie la taille de chaque sous-réseau en utilisant le `reste` de la division du préfixe réseau par huit. Ceci est également appelé `Opération Modulo (%)` (Modulo Operation) et est largement utilisé en cryptologie. Avec notre exemple précédent de `/25`, `(25 % 8)` donnerait 1. C'est parce que huit entre trois fois dans 25 (8 * 3 = 24). Il reste 1, qui est le bit réseau réservé pour le masque de réseau. Il y a un total de huit bits dans chaque octet d'une adresse IP. Si un bit est utilisé pour le masque de réseau, l'équation devient 2^(8-1) ou 2^7, soit 128. Le tableau ci-dessous contient tous les nombres.

|**Reste**|**Nombre**|**Forme exponentielle**|**Forme de division**|
|---|---|---|---|
|0|256|2^8|256|
|1|128|2^7|256/2|
|2|64|2^6|256/2/2|
|3|32|2^5|256/2/2/2|
|4|16|2^4|256/2/2/2/2|
|5|8|2^3|256/2/2/2/2/2|
|6|4|2^2|256/2/2/2/2/2/2|
|7|2|2^1|256/2/2/2/2/2/2/2|

En mémorisant les puissances de deux jusqu'à huit, le calcul peut devenir instantané. Cependant, si on les oublie, il peut être plus rapide de se souvenir de diviser 256 par deux autant de fois que la valeur du reste.

La partie délicate consiste à obtenir la plage d'adresses IP réelle, car 0 est un nombre et n'est pas nul en réseau. Ainsi, dans notre `/25` avec 128 adresses IP, la première plage est `192.168.1.0-127`. La première adresse est l'adresse réseau et la dernière est l'adresse de diffusion, ce qui signifie que l'`espace IP utilisable` (usable IP space) devient `192.168.1.1-126`. Si notre adresse IP tombait au-dessus de 128, alors l'`espace IP utilisable` serait 192.168.1.129-254 (128 est l'adresse réseau et 255 est l'adresse de diffusion).
---

← [[09 - Adresses IP]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[11 - Adresses MAC]] →
