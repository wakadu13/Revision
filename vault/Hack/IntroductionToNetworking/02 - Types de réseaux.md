---
tags:
  - networking
ordre: 2
---

# Types de réseaux

---

Chaque réseau est structuré différemment et peut être configuré individuellement. C'est pourquoi des « `types` » et des « `topologies` » ont été développés pour catégoriser ces réseaux. En lisant sur tous les types de réseaux, on peut être submergé par la quantité d'informations, car certains types de réseaux incluent la portée géographique. Nous entendons rarement certaines de ces terminologies en pratique, c'est pourquoi cette section sera divisée en `Termes courants` et `Termes théoriques`. Les termes théoriques sont bons à connaître, car il y a eu un cas documenté d'un serveur de messagerie qui n'a pas réussi à livrer des e-mails à plus de 500 miles, mais ne vous attendez pas à devoir les réciter sur demande, sauf si vous étudiez pour un examen de réseautique.

#### Terminologie courante

|**Type de réseau**|**Définition**|
|---|---|
|Réseau étendu (WAN)|Internet|
|Réseau local (LAN)|Réseaux internes (Ex : Domicile ou Bureau)|
|Réseau local sans fil (WLAN)|Réseaux internes accessibles via Wi-Fi|
|Réseau privé virtuel (VPN)|Connecte plusieurs sites réseau à un `LAN`|

---

## WAN

Le WAN (Wide Area Network ou réseau étendu) est communément appelé `l'Internet`. Lorsque nous traitons avec des équipements réseau, nous aurons souvent une adresse WAN et une adresse LAN. L'adresse WAN est celle qui est généralement accessible par Internet. Cela dit, ce n'est pas exclusif à Internet ; un WAN est simplement un grand nombre de LAN interconnectés. De nombreuses grandes entreprises ou agences gouvernementales auront un « WAN interne » (également appelé Intranet, réseau isolé, etc.). En général, la principale façon d'identifier si le réseau est un WAN est d'utiliser un protocole de routage spécifique au WAN tel que BGP et si le schéma d'adressage IP utilisé n'est pas dans la RFC 1918 (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16).

---

## LAN / WLAN

Les LAN (Local Area Network ou réseau local) et les WLAN (Wireless Local Area Network ou réseau local sans fil) attribuent généralement des adresses IP désignées pour un usage local (RFC 1918, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16). Dans certains cas, comme dans certaines universités ou hôtels, vous pouvez recevoir une adresse IP routable (Internet) en rejoignant leur LAN, mais c'est beaucoup moins courant. Il n'y a rien de différent entre un LAN et un WLAN, si ce n'est que les WLAN introduisent la capacité de transmettre des données sans câbles. C'est principalement une désignation de sécurité.

---

## VPN

Il existe trois principaux types de `Réseaux Privés Virtuels` (`VPN`), mais tous trois ont le même objectif : donner à l'utilisateur l'impression d'être connecté à un réseau différent.

#### VPN de site à site

Le client et le serveur sont tous deux des périphériques réseau, généralement des `routeurs` ou des `pare-feux` (firewalls), et partagent des plages de réseau entières. C'est le plus souvent utilisé pour joindre les réseaux d'entreprise via Internet, permettant à plusieurs sites de communiquer sur Internet comme s'ils étaient locaux.

#### VPN d'accès à distance

Cela implique que l'ordinateur du client crée une interface virtuelle qui se comporte comme si elle était sur le réseau d'un client. Hack The Box utilise `OpenVPN`, qui crée un adaptateur TUN nous permettant d'accéder aux laboratoires. Lors de l'analyse de ces VPN, un élément important à prendre en compte est la table de routage qui est créée lors de la connexion au VPN. Si le VPN ne crée des routes que pour des réseaux spécifiques (ex : 10.10.10.0/24), on parle de `VPN en tunnel scindé` (`Split-Tunnel VPN`), ce qui signifie que la connexion Internet ne passe pas par le VPN. C'est excellent pour Hack The Box car cela donne accès au laboratoire sans le souci de confidentialité lié à la surveillance de votre connexion Internet. Cependant, pour une entreprise, les VPN en `tunnel scindé` ne sont généralement pas idéaux car si la machine est infectée par un logiciel malveillant, les méthodes de détection basées sur le réseau ne fonctionneront probablement pas, car ce trafic sortira par Internet.

#### VPN SSL

Il s'agit essentiellement d'un VPN qui s'exécute dans notre navigateur web et qui devient de plus en plus courant à mesure que les navigateurs web deviennent capables de tout faire. Typiquement, ils diffuseront des applications ou des sessions de bureau entières sur votre navigateur web. Un excellent exemple de cela serait la Pwnbox de HackTheBox.

---

## Termes théoriques

|Type de réseau|Définition|
|---|---|
|Réseau mondial (GAN)|Réseau global (l'Internet)|
|Réseau métropolitain (MAN)|Réseau régional (plusieurs LAN)|
|Réseau personnel sans fil (WPAN)|Réseau personnel (Bluetooth)|

#### GAN

Un réseau mondial tel que `l'Internet` est connu sous le nom de `Réseau Mondial` (`Global Area Network` ou `GAN`). Cependant, l'Internet n'est pas le seul réseau informatique de ce type. Les entreprises actives à l'international maintiennent également des réseaux isolés qui s'étendent sur plusieurs `WAN` et connectent les ordinateurs de l'entreprise dans le monde entier. Les `GAN` utilisent l'infrastructure de fibres optiques des réseaux étendus et les interconnectent par des câbles sous-marins internationaux ou par transmission satellite.

#### MAN

Le `Réseau Métropolitain` (`Metropolitan Area Network` ou `MAN`) est un réseau de télécommunications à large bande qui connecte plusieurs `LAN` à proximité géographique. En règle générale, il s'agit de succursales individuelles d'une entreprise connectées à un `MAN` via des lignes louées. Des routeurs et des connexions haute performance basés sur des fibres optiques sont utilisés, ce qui permet un débit de données nettement supérieur à celui d'Internet. La vitesse de transmission entre deux nœuds distants est comparable à la communication au sein d'un `LAN`.

Les opérateurs de réseaux internationaux fournissent l'infrastructure pour les `MAN`. Les villes câblées en tant que `Réseaux Métropolitains` peuvent être intégrées au niveau supra-régional dans des `Réseaux Étendus` (`WAN`) et au niveau international dans des `Réseaux Mondiaux` (`GAN`).

#### PAN / WPAN

Les appareils modernes tels que les smartphones, les tablettes, les ordinateurs portables ou les ordinateurs de bureau peuvent être connectés de manière ad hoc pour former un réseau afin de permettre l'échange de données. Cela peut se faire par câble sous la forme d'un `Réseau Personnel` (`Personal Area Network` ou `PAN`).

La variante sans fil `Réseau Personnel Sans Fil` (`Wireless Personal Area Network` ou `WPAN`) est basée sur les technologies Bluetooth ou Wireless USB. Un `réseau personnel sans fil` établi via Bluetooth est appelé `Piconet`. Les `PAN` et `WPAN` ne s'étendent généralement que sur quelques mètres et ne sont donc pas adaptés pour connecter des appareils dans des pièces séparées ou même des bâtiments.

Dans le contexte de `l'Internet des Objets` (`Internet of Things` ou `IoT`), les `WPAN` sont utilisés pour communiquer avec des applications de contrôle et de surveillance avec de faibles débits de données. Des protocoles tels que Insteon, Z-Wave et ZigBee ont été explicitement conçus pour les maisons intelligentes et la domotique.
---

← [[01 - Aperçu du Réseautage]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[03 - Topologies Réseau]] →
