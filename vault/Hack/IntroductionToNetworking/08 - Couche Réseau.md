---
tags:
  - networking
ordre: 8
---

# Couche Réseau

---

La `couche réseau (network layer)` (`Couche 3`) du modèle `OSI` contrôle l'échange de paquets de données, car ceux-ci ne peuvent pas être directement acheminés vers le destinataire et doivent donc passer par des nœuds de routage. Les paquets de données sont ensuite transférés de nœud en nœud jusqu'à ce qu'ils atteignent leur cible. Pour ce faire, la `couche réseau` identifie les nœuds individuels du réseau, établit et ferme les canaux de connexion, et s'occupe du routage et du contrôle du flux de données. Lors de l'envoi des paquets, les adresses sont évaluées, et les données sont acheminées à travers le réseau de nœud en nœud. Généralement, il n'y a pas de traitement des données dans les couches supérieures à la `L3` au niveau des nœuds. Le routage et la construction des tables de routage se font sur la base des adresses.

En bref, elle est responsable des fonctions suivantes :

- `Adressage logique (Logical Addressing)`
- `Routage (Routing)`

Des protocoles sont définis dans chaque couche du modèle `OSI`, et ces protocoles représentent un ensemble de règles pour la communication dans la couche respective. Ils sont transparents pour les protocoles des couches supérieures ou inférieures. Certains protocoles remplissent des tâches de plusieurs couches et s'étendent sur deux couches ou plus. Les protocoles les plus utilisés sur cette couche sont :

- `IPv4` / `IPv6`
- `IPsec`
- `ICMP`
- `IGMP`
- `RIP`
- `OSPF`

Elle assure le routage des paquets de la source à la destination à l'intérieur ou à l'extérieur d'un sous-réseau. Ces deux sous-réseaux peuvent avoir des schémas d'adressage différents ou des types d'adressage incompatibles. Dans les deux cas, la transmission des données passe par l'ensemble du réseau de communication et inclut le routage entre les nœuds du réseau. Étant donné qu'une communication directe entre l'expéditeur et le destinataire n'est pas toujours possible en raison des différents sous-réseaux, les paquets doivent être transférés par des nœuds (routeurs) qui se trouvent sur le chemin. Les paquets transférés n'atteignent pas les couches supérieures, mais se voient attribuer une nouvelle destination intermédiaire et sont envoyés au nœud suivant.
---

← [[07 - Le modèle TCP-IP]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[09 - Adresses IP]] →
