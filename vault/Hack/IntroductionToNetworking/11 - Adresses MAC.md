---
tags:
  - networking
ordre: 11
---

# Adresses MAC

---

Chaque hôte d'un réseau possède sa propre adresse de `Contrôle d'Accès au Média` (`Media Access Control` ou `MAC`) de `48`-bits (`6 octets`), représentée au format hexadécimal. L'adresse `MAC` est l'`adresse physique` (« physical address ») de nos interfaces réseau. Il existe plusieurs normes différentes pour l'adresse MAC :

- Ethernet (IEEE 802.3)
- Bluetooth (IEEE 802.15)
- WLAN (IEEE 802.11)

Ceci est dû au fait que l'adresse `MAC` concerne la connexion physique (carte réseau, adaptateur Bluetooth ou WLAN) d'un hôte. Chaque carte réseau a sa propre adresse MAC, qui est configurée une seule fois au niveau matériel par le fabricant, mais qui peut toujours être modifiée, au moins temporairement.

Jetons un œil à un exemple d'une telle adresse MAC :

Adresse MAC :

- `DE:AD:BE:EF:13:37`
- `DE-AD-BE-EF-13-37`
- `DEAD.BEEF.1337`

|**Représentation**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**5e Octet**|**6e Octet**|
|---|---|---|---|---|---|---|
|Binaire|1101 1110|1010 1101|1011 1110|1110 1111|0001 0011|0011 0111|
|Hex|DE|AD|BE|EF|13|37|

---

Lorsqu'un paquet IP est livré, il doit être adressé sur la `couche 2` à l'adresse physique de l'hôte de destination ou au routeur / NAT, qui est responsable du routage. Chaque paquet a une `adresse d'expéditeur` et une `adresse de destination`.

L'adresse MAC se compose d'un total de `6 octets`. La première moitié (`3 octets` / `24 bits`) est ce qu'on appelle l'`Identifiant Unique d'Organisation` (`Organization Unique Identifier` ou `OUI`), défini par l'`Institute of Electrical and Electronics Engineers` (`IEEE`) pour les fabricants respectifs.

|**Représentation**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**5e Octet**|**6e Octet**|
|---|---|---|---|---|---|---|
|Binaire|`1101 1110`|`1010 1101`|`1011 1110`|1110 1111|0001 0011|0011 0111|
|Hex|`DE`|`AD`|`BE`|EF|13|37|

---

La dernière moitié de l'adresse MAC est appelée la `Partie d'Adresse Individuelle` (`Individual Address Part`) ou `Contrôleur d'Interface Réseau` (`Network Interface Controller` ou `NIC`), que les fabricants attribuent. Le fabricant ne définit cette séquence de bits qu'une seule fois et garantit ainsi que l'adresse complète est unique.

|**Représentation**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**5e Octet**|**6e Octet**|
|---|---|---|---|---|---|---|
|Binaire|1101 1110|1010 1101|1011 1110|`1110 1111`|`0001 0011`|`0011 0111`|
|Hex|DE|AD|BE|`EF`|`13`|`37`|

Si un hôte avec l'adresse IP cible est situé dans le même sous-réseau, la livraison est effectuée directement à l'adresse physique de l'ordinateur cible. Cependant, si cet hôte appartient à un sous-réseau différent, la trame Ethernet est adressée à l'`adresse MAC` du routeur responsable (`passerelle par défaut` ou « default gateway »). Si l'adresse de destination de la trame Ethernet correspond à sa propre `adresse de couche 2`, le routeur transmettra la trame aux couches supérieures. Le `Protocole de Résolution d'Adresse` (`Address Resolution Protocol` ou `ARP`) est utilisé en IPv4 pour déterminer les adresses MAC associées aux adresses IP.

Comme pour les adresses IPv4, il existe également certaines plages réservées pour l'adresse MAC. Celles-ci incluent, par exemple, la plage locale pour la MAC.

|**Plage Locale**|
|---|
|0`2`:00:00:00:00:00|
|0`6`:00:00:00:00:00|
|0`A`:00:00:00:00:00|
|0`E`:00:00:00:00:00|

De plus, les deux derniers bits du premier octet peuvent jouer un autre rôle essentiel. Le dernier bit peut avoir deux états, 0 et 1, comme nous le savons déjà. Le dernier bit identifie l'adresse MAC comme étant `Unicast` (`0`) ou `Multicast` (`1`). Avec l'`unicast`, cela signifie que le paquet envoyé n'atteindra qu'un seul hôte spécifique.

#### MAC Unicast

|**Représentation**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**5e Octet**|**6e Octet**|
|---|---|---|---|---|---|---|
|Binaire|1101 111`0`|1010 1101|1011 1110|1110 1111|0001 0011|0011 0111|
|Hex|D`E`|AD|BE|EF|13|37|

---

Avec le `multicast`, le paquet est envoyé une seule fois à tous les hôtes du réseau local, qui décident ensuite d'accepter ou non le paquet en fonction de leur configuration. L'adresse `multicast` est une adresse unique, tout comme l'adresse de `broadcast`, qui a des valeurs d'octets fixes. Le `Broadcast` (diffusion générale) dans un réseau représente un appel diffusé, où les paquets de données sont transmis simultanément d'un point à tous les membres d'un réseau. Il est principalement utilisé si l'adresse du destinataire du paquet n'est pas encore connue. Un exemple est les protocoles `ARP` (pour les adresses MAC) et DHCP (pour les adresses IPv4).

Les valeurs définies de chaque octet sont marquées en `vert`.

#### MAC Multicast

|**Représentation**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**5e Octet**|**6e Octet**|
|---|---|---|---|---|---|---|
|Binaire|`0000 0001`|`0000 0000`|`0101 1110`|1110 1111|0001 0011|0011 0111|
|Hex|`01`|`00`|`5E`|EF|13|37|

#### MAC Broadcast

|**Représentation**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**5e Octet**|**6e Octet**|
|---|---|---|---|---|---|---|
|Binaire|`1111 1111`|`1111 1111`|`1111 1111`|`1111 1111`|`1111 1111`|`1111 1111`|
|Hex|`FF`|`FF`|`FF`|`FF`|`FF`|`FF`|

---

L'avant-dernier bit du premier octet identifie s'il s'agit d'un `OUI global`, défini par l'IEEE, ou d'une adresse MAC `administrée localement`.

#### OUI Global

|**Représentation**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**5e Octet**|**6e Octet**|
|---|---|---|---|---|---|---|
|Binaire|1101 11`0`0|1010 1101|1011 1110|1110 1111|0001 0011|0011 0111|
|Hex|D`C`|AD|BE|EF|13|37|

#### Administrée Localement

|**Représentation**|**1er Octet**|**2e Octet**|**3e Octet**|**4e Octet**|**5e Octet**|**6e Octet**|
|---|---|---|---|---|---|---|
|Binaire|1101 11`1`0|1010 1101|1011 1110|1110 1111|0001 0011|0011 0111|
|Hex|D`E`|AD|BE|EF|13|37|

---

## Vecteurs d'Attaque des Adresses MAC

Les adresses MAC peuvent être modifiées/manipulées ou usurpées, et en tant que telles, elles ne doivent pas être considérées comme le seul moyen de sécurité ou d'identification. Les administrateurs réseau devraient mettre en œuvre des mesures de sécurité supplémentaires, telles que la segmentation du réseau et des protocoles d'authentification forts, pour se protéger contre les attaques potentielles.

Il existe plusieurs vecteurs d'attaque qui peuvent potentiellement être exploités par l'utilisation d'adresses MAC :

- `Usurpation d'adresse MAC` (`MAC spoofing`) : Cela consiste à modifier l'adresse MAC d'un appareil pour qu'elle corresponde à celle d'un autre appareil, généralement pour obtenir un accès non autorisé à un réseau.
- `Inondation MAC` (`MAC flooding`) : Cela consiste à envoyer de nombreux paquets avec différentes adresses MAC à un commutateur réseau, ce qui provoque l'atteinte de la capacité de sa table d'adresses MAC et l'empêche de fonctionner correctement.
- `Filtrage d'adresses MAC` (`MAC address filtering`) : Certains réseaux peuvent être configurés pour n'autoriser l'accès qu'aux appareils ayant des adresses MAC spécifiques, ce que nous pourrions potentiellement exploiter en tentant d'accéder au réseau en utilisant une adresse MAC usurpée.

---

## Protocole de Résolution d'Adresse

Le [Protocole de Résolution d'Adresse](https://fr.wikipedia.org/wiki/Address_Resolution_Protocol) (`Address Resolution Protocol` ou `ARP`) est un protocole réseau. C'est un élément important de la communication réseau utilisé pour résoudre une adresse IP de couche réseau (couche 3) en une adresse MAC de couche de liaison de données (couche 2). Il fait correspondre l'adresse IP d'un hôte à son adresse MAC correspondante pour faciliter la communication entre les appareils sur un [Réseau Local](https://fr.wikipedia.org/wiki/R%C3%A9seau_local) (`Local Area Network` ou `LAN`). Lorsqu'un appareil sur un LAN veut communiquer avec un autre appareil, il envoie un message de broadcast contenant l'adresse IP de destination et sa propre adresse MAC. L'appareil avec l'adresse IP correspondante répond avec sa propre adresse MAC, et les deux appareils peuvent alors communiquer directement en utilisant leurs adresses MAC. Ce processus est connu sous le nom de résolution ARP.

L'ARP est un élément important du processus de communication réseau car il permet aux appareils d'envoyer et de recevoir des données en utilisant des adresses MAC plutôt que des adresses IP, ce qui peut être plus efficace. Deux types de messages de requête peuvent être utilisés :

#### Requête ARP

Lorsqu'un appareil veut communiquer avec un autre appareil sur un LAN, il envoie une requête ARP pour résoudre l'adresse IP de l'appareil de destination en son adresse MAC. La requête est diffusée (broadcast) à tous les appareils sur le LAN et contient l'adresse IP de l'appareil de destination. L'appareil avec l'adresse IP correspondante répond avec son adresse MAC.

#### Réponse ARP

Lorsqu'un appareil reçoit une requête ARP, il envoie une réponse ARP à l'appareil demandeur avec son adresse MAC. Le message de réponse contient les adresses IP et MAC de l'appareil demandeur et de l'appareil qui répond.

#### Capture Tshark de Requêtes ARP

```bash
1   0.000000 10.129.12.100 -> 10.129.12.255 ARP 60  Who has 10.129.12.101?  Tell 10.129.12.100
2   0.000015 10.129.12.101 -> 10.129.12.100 ARP 60  10.129.12.101 is at AA:AA:AA:AA:AA:AA

3   0.000030 10.129.12.102 -> 10.129.12.255 ARP 60  Who has 10.129.12.103?  Tell 10.129.12.102
4   0.000045 10.129.12.103 -> 10.129.12.102 ARP 60  10.129.12.103 is at BB:BB:BB:BB:BB:BB
```

Le message « `who has` » dans la première et la troisième ligne indique qu'un appareil demande l'adresse MAC pour l'adresse IP spécifiée, tandis que la deuxième et la quatrième ligne montrent la réponse ARP avec l'adresse MAC de l'appareil de destination.

Cependant, il est également vulnérable aux attaques, telles que l'[usurpation ARP](https://fr.wikipedia.org/wiki/ARP_spoofing) (`ARP Spoofing`), qui peuvent être utilisées pour intercepter ou manipuler le trafic sur le réseau. Cependant, pour se protéger contre de telles attaques, il est important de mettre en œuvre des mesures de sécurité telles que des pare-feu et des systèmes de détection d'intrusion.

L'`usurpation ARP` (`ARP spoofing`), également connue sous le nom d'`empoisonnement du cache ARP` (`ARP cache poisoning`) ou de `routage empoisonné par ARP` (`ARP poison routing`), est une attaque qui peut être réalisée à l'aide d'outils comme [Ettercap](https://github.com/Ettercap/ettercap) ou [Cain & Abel](https://github.com/xchwarze/Cain) dans laquelle nous envoyons des messages ARP falsifiés sur un LAN. L'objectif est d'associer notre adresse MAC à l'adresse IP d'un appareil légitime sur le réseau de l'entreprise, nous permettant ainsi d'intercepter le trafic destiné à l'appareil légitime. Par exemple, cela pourrait ressembler à ce qui suit :

```bash
1   0.000000 10.129.12.100 -> 10.129.12.101 ARP 60 10.129.12.255 is at CC:CC:CC:CC:CC:CC  (ARP reply from attacker claiming gateway IP)
2   0.000015 10.129.12.101 -> Broadcast ARP 60 Who has 10.129.12.100? Tell 10.129.12.101
3   0.000030 10.129.12.100 -> 10.129.12.101 ARP 60 10.129.12.100 is at CC:CC:CC:CC:CC:CC
4   0.000045 10.129.12.101 -> 10.129.12.100 ARP 60 Who has 10.129.12.255? Tell 10.129.12.101 (Victim querying gateway after poisoning)
```

La première ligne nous montre (l'attaquant à `10.129.12.100`) envoyant une réponse ARP gratuite falsifiée à la cible (`10.129.12.101`), associant notre adresse MAC (`CC:CC:CC:CC:CC:CC`) à l'adresse IP de la passerelle (`10.129.12.255`). La deuxième et la quatrième ligne montrent la cible envoyant des requêtes ARP, et la troisième montre notre réponse. Cela indique que nous avons empoisonné le cache ARP de la cible et que le trafic destiné à la passerelle sera désormais envoyé à notre adresse MAC.

Nous pouvons utiliser l'empoisonnement ARP pour effectuer diverses activités, telles que le vol d'informations sensibles, la redirection de trafic ou le lancement d'attaques de l'homme du milieu (`MITM attacks`). Cependant, pour se protéger contre l'usurpation ARP, il est important d'utiliser des protocoles réseau sécurisés, tels que IPSec ou SSL, et de mettre en œuvre des mesures de sécurité, telles que des pare-feu et des systèmes de détection d'intrusion.
---

← [[10 - Segmentation en sous-réseaux]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[12 - Adresses IPv6]] →
