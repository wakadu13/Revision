---
tags:
  - networking
ordre: 12
---

# Adresses IPv6

---

`IPv6` est le successeur d'IPv4. Contrairement à IPv4, l'adresse `IPv6` est longue de `128` bits. Le `préfixe` identifie les parties hôte et réseau. L'Internet Assigned Numbers Authority (`IANA`) est responsable de l'attribution des adresses IPv4 et IPv6 et de leurs portions réseau associées. À long terme, `IPv6` devrait remplacer complètement IPv4, qui est encore majoritairement utilisé sur Internet. En principe, cependant, IPv4 et IPv6 peuvent être mis à disposition simultanément (`Dual Stack` ou double pile).

IPv6 suit systématiquement le principe de bout en bout (end-to-end principle) et fournit des adresses IP publiquement accessibles pour tous les terminaux sans avoir besoin de NAT. Par conséquent, une interface peut avoir plusieurs adresses IPv6, et il existe des adresses IPv6 spéciales auxquelles plusieurs interfaces sont assignées.

`IPv6` est un protocole doté de nombreuses nouvelles fonctionnalités, qui présente également de nombreux autres avantages par rapport à IPv4 :

- Espace d'adressage plus grand
- Autoconfiguration d'adresse (SLAAC)
- Plusieurs adresses IPv6 par interface
- Routage plus rapide
- Chiffrement de bout en bout (IPsec)
- Paquets de données jusqu'à 4 GByte

|**Caractéristiques**|**IPv4**|**IPv6**|
|---|---|---|
|Longueur en bits|32 bits|128 bits|
|Couche OSI|Couche réseau|Couche réseau|
|Plage d'adressage|~ 4,3 milliards|~ 340 undécillions|
|Représentation|Décimale|Hexadécimale|
|Notation de préfixe|10.10.10.0/24|fe80::dd80:b1a9:6687:2d3b/64|
|Adressage dynamique|DHCP|SLAAC / DHCPv6|
|IPsec|Optionnel|Obligatoire|

---

Il existe trois différents types d'adresses IPv6 :

|**Type**|**Description**|
|---|---|
|`Unicast`|Adresses pour une seule interface.|
|`Anycast`|Adresses pour plusieurs interfaces, où une seule d'entre elles reçoit le paquet.|
|`Multicast`|Adresses pour plusieurs interfaces, où toutes reçoivent le même paquet.|

Note : Contrairement à IPv4, IPv6 élimine l'adresse de diffusion (broadcast address). À la place, IPv6 utilise des adresses de multidiffusion (multicast) pour prendre en charge la découverte et la communication avec plusieurs nœuds.

---

## Système hexadécimal

Le `système hexadécimal` (`hex`) est utilisé pour rendre la représentation binaire plus lisible et compréhensible. Nous ne pouvons représenter que `10` (`0-9`) états avec le système décimal et `2` (`0` / `1`) avec le système binaire en utilisant un seul caractère. Contrairement aux systèmes binaire et décimal, nous pouvons utiliser le système hexadécimal pour représenter `16` (`0-F`) états avec un seul caractère.

|**Décimal**|**Hex**|**Binaire**|
|---|---|---|
|1|1|0001|
|2|2|0010|
|3|3|0011|
|4|4|0100|
|5|5|0101|
|6|6|0110|
|7|7|0111|
|8|8|1000|
|9|9|1001|
|10|A|1010|
|11|B|1011|
|12|C|1100|
|13|D|1101|
|14|E|1110|
|15|F|1111|

Prenons un exemple avec une adresse IPv4, pour voir à quoi ressemblerait l'adresse IPv4 (`192.168.12.160`) en représentation hexadécimale.

|**Représentation**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|
|---|---|---|---|---|
|Binaire|1100 0000|1010 1000|0000 1100|1010 0000|
|`Hex`|`C0`|`A8`|`0C`|`A0`|
|Décimal|192|168|12|160|

---

Au total, l'adresse IPv6 se compose de `16 octets`. En raison de sa longueur, une adresse `IPv6` est représentée en notation `hexadécimale`. Par conséquent, les `128 bits` sont divisés en `8 blocs` de 16 bits (soit `4` chiffres `hex`adécimaux). Ces blocs sont séparés par un deux-points (`:`) au lieu d'un simple point (`.`) comme en IPv4. Pour simplifier la notation, nous omettons les zéros non significatifs dans les blocs, et nous pouvons remplacer une suite de blocs de zéros par un double deux-points (`::`).

Une adresse IPv6 peut ressembler à ceci :

- IPv6 complète : `fe80:0000:0000:0000:dd80:b1a9:6687:2d3b/64`
- IPv6 courte : `fe80::dd80:b1a9:6687:2d3b/64`

Une adresse IPv6 se compose de deux parties :

- `Préfixe réseau` (partie réseau)
- `Identifiant d'interface` aussi appelé `Suffixe` (partie hôte)

Le `Préfixe réseau` identifie le réseau, le sous-réseau ou la plage d'adresses. L'`Identifiant d'interface` est formé à partir de l'adresse `MAC` de `48 bits` (que nous aborderons plus tard) de l'interface et est converti en une adresse de `64 bits` au cours du processus. La longueur de préfixe par défaut est `/64`. Cependant, d'autres préfixes typiques sont `/32`, `/48` et `/56`. Si nous voulons utiliser nos propres réseaux, nous obtenons de notre fournisseur un préfixe plus court (par ex. `/56`) que `/64`.

Dans la RFC 5952, la notation d'adresse IPv6 susmentionnée a été définie :

- Tous les caractères alphabétiques sont toujours écrits en minuscules.
- Tous les zéros non significatifs d'un bloc sont toujours omis.
- Un ou plusieurs blocs consécutifs de `4 zéros` (hex) sont abrégés par un double deux-points (`::`).
- L'abrègement par un double deux-points (`::`) ne peut être effectué qu'`une seule fois`, en commençant par la gauche.
---

← [[11 - Adresses MAC]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[13 - Terminologie Clé des Réseaux]] →
