---
tags:
  - networking
ordre: 3
---

# Topologies Réseau

---

Une `topologie réseau` est un agencement typique et une connexion `physique` ou `logique` des appareils d'un réseau. Les ordinateurs sont des `hôtes`, tels que des `clients` et des `serveurs`, qui utilisent activement le réseau. Ils incluent également des `composants réseau` tels que des `commutateurs (switches)`, des `ponts (bridges)` et des `routeurs`, que nous aborderons plus en détail dans les sections suivantes, qui ont une fonction de distribution et garantissent que tous les hôtes du réseau peuvent établir une connexion logique entre eux. La topologie réseau détermine les composants à utiliser et les méthodes d'accès aux supports de transmission.

La `disposition du support de transmission` utilisée pour connecter les appareils est la topologie physique du réseau. Pour les supports conducteurs ou en fibre de verre, cela fait référence au plan de câblage, aux positions des `nœuds` et aux connexions entre les nœuds et le câblage. En revanche, la `topologie logique` décrit la manière dont les signaux agissent sur le support réseau ou dont les données sont transmises d'un appareil à l'autre sur le réseau, indépendamment de leur connexion physique.

---

Nous pouvons diviser l'ensemble du domaine de la topologie réseau en trois zones :

#### 1. Connexions

|`Connexions filaires`|`Connexions sans fil`|
|---|---|
|Câblage coaxial|Wi-Fi|
|Câblage par fibre optique|Cellulaire|
|Câblage à paires torsadées|Satellite|
|et autres|et autres|

---

#### 2. Nœuds - Contrôleur d'Interface Réseau (NIC)

|||||
|---|---|---|---|
|Répéteurs|Concentrateurs (Hubs)|Ponts|Commutateurs|
|Routeur/Modem|Passerelles (Gateways)|Pare-feux (Firewalls)||

Les nœuds de réseau sont les `points de connexion du support de transmission` aux émetteurs et récepteurs de signaux électriques, optiques ou radio dans le support. Un nœud peut être connecté à un ordinateur, mais certains types peuvent n'avoir qu'un seul microcontrôleur sur un nœud ou ne posséder aucun dispositif programmable.

---

#### 3. Classifications

Nous pouvons imaginer une topologie comme une forme virtuelle ou une `structure de réseau`. Cette forme ne correspond pas nécessairement à la disposition physique réelle des appareils sur le réseau. Par conséquent, ces topologies peuvent être `physiques` ou `logiques`. Par exemple, les ordinateurs d'un `LAN` peuvent être disposés en cercle dans une chambre, mais il est très peu probable qu'il s'agisse d'une véritable topologie en anneau.

Les topologies réseau sont divisées en huit types de base suivants :

|||
|---|---|
|Point à point|En bus|
|En étoile|En anneau|
|Maillée|En arbre|
|Hybride|En guirlande (Daisy Chain)|

Des réseaux plus complexes peuvent être construits comme des hybrides de deux ou plusieurs des topologies de base mentionnées ci-dessus.

---

## Point à point

La topologie réseau la plus simple avec une connexion dédiée entre deux hôtes est la topologie `point à point`. Dans cette topologie, une liaison physique directe et simple n'existe qu'entre `deux hôtes`. Ces deux appareils peuvent utiliser ces connexions pour une communication mutuelle.

Les topologies `point à point` sont le modèle de base de la téléphonie traditionnelle et ne doivent pas être confondues avec l'architecture `P2P` (`Peer-to-Peer`).

#### Topologie Point à Point

![image](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/topo_p2p.png)

---

## En bus

Dans la topologie en bus, tous les hôtes sont connectés via un support de transmission. Chaque hôte a accès au support de transmission et aux signaux qui y sont transmis. Il n'y a pas de composant réseau central qui contrôle les processus sur celui-ci. Le support de transmission pour cela peut être, par exemple, un `câble coaxial`.

Étant donné que le support est partagé avec tous les autres, un `seul hôte peut émettre`, et tous les autres ne peuvent que recevoir et évaluer les données pour voir si elles leur sont destinées.

#### Topologie en Bus

![Diagramme montrant une connexion entre l'Hôte A et l'Hôte B.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/topo_bus.png)

---

## En étoile

La topologie en étoile est un composant réseau qui maintient une connexion avec tous les hôtes. Chaque hôte est connecté au `composant réseau central` via une liaison distincte. Il s'agit généralement d'un routeur, d'un concentrateur ou d'un commutateur. Ceux-ci gèrent la `fonction de retransmission` des paquets de données. Pour ce faire, les paquets de données sont reçus et transmis à leur destination. Le trafic de données sur le composant réseau central peut être très élevé puisque toutes les données et connexions passent par lui.

#### Topologie en Étoile

![Diagramme montrant les connexions entre les Hôtes A, B, C, D, E et F.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/topo_star.png)

---

## En anneau

La topologie en anneau `physique` est telle que chaque hôte ou nœud est connecté à l'anneau avec deux câbles :

- Un pour les signaux `entrants` et
- un autre pour les signaux `sortants`.

Cela signifie qu'un câble arrive à chaque hôte et qu'un câble en part. La topologie en anneau ne nécessite généralement pas de composant réseau actif. Le contrôle et l'accès au support de transmission sont régulés par un protocole auquel toutes les stations adhèrent.

Une topologie en anneau `logique` est basée sur une topologie physique en étoile, où un distributeur au niveau du nœud simule l'anneau en retransmettant d'un port à l'autre.

Les informations sont transmises dans une direction de transmission prédéterminée. Généralement, l'accès au support de transmission se fait séquentiellement de station en station en utilisant un système de scrutation depuis la station centrale ou un `jeton (token)`. Un jeton est une séquence de bits qui passe continuellement à travers un réseau en anneau dans une direction, qui fonctionne selon le `processus de revendication de jeton`.

#### Topologie en Anneau

![Diagramme montrant un routeur connectant les Hôtes A, B, C et D.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/topo_ring.png)

---

## Maillée

De nombreux nœuds décident des connexions au niveau `physique` et du routage au niveau `logique` dans les réseaux maillés. Par conséquent, les structures maillées n'ont pas de topologie fixe. Il existe deux structures de base à partir du concept de base : la structure `entièrement maillée` et la structure `partiellement maillée`.

Chaque hôte est connecté à tous les autres hôtes du réseau dans une `structure entièrement maillée`. Cela signifie que les hôtes sont maillés les uns avec les autres. Cette technique est principalement utilisée dans les `WAN` ou les `MAN` pour garantir une haute fiabilité et une large bande passante.

Dans cette configuration, les nœuds réseau importants tels que les routeurs pourraient être mis en réseau ensemble. Si un routeur tombe en panne, les autres peuvent continuer à fonctionner sans problème, et le réseau peut absorber la défaillance grâce aux nombreuses connexions.

Chaque nœud d'une topologie entièrement maillée possède les mêmes fonctions de routage et connaît les nœuds voisins avec lesquels il peut communiquer, leur proximité avec la passerelle réseau et les charges de trafic.

Dans la `structure partiellement maillée`, les points d'extrémité ne sont connectés que par une seule connexion. Dans ce type de topologie réseau, des nœuds spécifiques sont connectés à un seul autre nœud, et d'autres nœuds sont connectés à deux ou plusieurs autres nœuds avec une connexion point à point.

#### Topologie Maillée

![Diagramme réseau montrant les Hôtes A, B, C et D connectés via les Routeurs A, B, C et D.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/topo_mesh.png)

---

## En arbre

La topologie en arbre est une topologie en étoile étendue que l'on retrouve dans les réseaux locaux plus vastes. Ceci est particulièrement utile lorsque plusieurs topologies sont combinées. Cette topologie est souvent utilisée, par exemple, dans les grands immeubles d'entreprise.

Il existe à la fois des structures en arbre logiques selon l'`arbre recouvrant (spanning tree)` et des structures physiques. Les réseaux modernes modulaires, basés sur un câblage structuré avec une hiérarchie de concentrateurs, ont également une structure en arbre. Les topologies en arbre sont également utilisées pour les `réseaux à large bande` et les `réseaux métropolitains` (`MAN`).

#### Topologie en Arbre

![Diagramme réseau montrant un serveur connecté à deux commutateurs Ethernet, chacun reliant les Hôtes A, B, C, D, E et F.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/topo_tree.png)

---

## Hybride

Les réseaux hybrides combinent deux ou plusieurs topologies de sorte que le réseau qui en résulte ne présente aucune des topologies standards. Par exemple, un réseau en arbre peut représenter une topologie hybride dans laquelle des réseaux en étoile sont connectés via des réseaux en bus interconnectés. Cependant, un réseau en arbre qui est lié à un autre réseau en arbre reste topologiquement un réseau en arbre. Une topologie hybride est toujours créée lorsque `deux` topologies de réseau de base `différentes` sont interconnectées.

#### Topologie Hybride

![Diagramme réseau montrant les Hôtes A, B, C, D, E et F connectés via les Routeurs A, B et C.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/topo_hybrid.png)

---

## En guirlande (Daisy Chain)

Dans la topologie en guirlande, plusieurs hôtes sont connectés en reliant un câble d'un nœud à un autre.

Comme cela crée une chaîne de connexions, elle est également connue sous le nom de configuration en guirlande dans laquelle plusieurs composants matériels sont connectés en série. Ce type de mise en réseau se trouve souvent dans les technologies d'automatisation (`CAN`).

La connexion en guirlande est basée sur la disposition physique des nœuds, contrairement aux procédures à jeton, qui sont structurelles mais peuvent être rendues indépendantes de la disposition physique. Le signal est envoyé vers et depuis un composant via ses nœuds précédents jusqu'au système informatique.

#### Topologie en Guirlande

![Diagramme réseau montrant les Hôtes A, B, D et E connectés à l'Hôte C.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/topo_daisy-chain.png)
---

← [[02 - Types de réseaux]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[04 - Proxys]] →
