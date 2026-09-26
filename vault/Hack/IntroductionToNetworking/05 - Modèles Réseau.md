---
tags:
  - networking
ordre: 5
---

# Modèles Réseau

---

Deux modèles réseau décrivent la communication et le transfert de données d'un hôte à un autre, appelés le `modèle ISO/OSI` et le `modèle TCP/IP`. Il s'agit d'une représentation simplifiée des soi-disant `couches` qui transforment les `Bits` transférés en contenu lisible pour nous.

![Comparaison des modèles OSI et TCP/IP : Le modèle OSI a 7 couches, dont Application, Présentation, Session, Transport, Réseau, Liaison de données et Physique. Le modèle TCP/IP a 4 couches : Application, Transport, Internet et Liaison.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/net_models4_updated.png)

---

## Le Modèle OSI

Le modèle `OSI`, souvent appelé modèle en couches `ISO/OSI`, est un modèle de référence qui peut être utilisé pour décrire et définir la communication entre les systèmes. Le modèle de référence comporte `sept` couches individuelles, chacune ayant des tâches clairement distinctes.

Le terme `OSI` signifie modèle d'« `Open Systems Interconnection` » (Interconnexion de Systèmes Ouverts), publié par l'« `International Telecommunication Union` » (`ITU`) (Union Internationale des Télécommunications - UIT) et l'« `International Organization for Standardization` » (`ISO`) (Organisation Internationale de Normalisation). Par conséquent, le modèle `OSI` est souvent appelé le modèle en couches `ISO/OSI`.

---

## Le Modèle TCP/IP

`TCP/IP` (`Transmission Control Protocol`/`Internet Protocol`) est un terme générique désignant de nombreux protocoles réseau. Ces protocoles sont responsables de la commutation (switching) et du transport des paquets de données sur Internet. Internet est entièrement basé sur la famille de protocoles `TCP/IP`. Cependant, `TCP/IP` ne fait pas seulement référence à ces deux protocoles, mais est généralement utilisé comme un terme générique pour toute une famille de protocoles.

Par exemple, `ICMP` (`Internet Control Message Protocol`) ou `UDP` (`User Datagram Protocol`) appartiennent à la famille de protocoles. La famille de protocoles fournit les fonctions nécessaires au transport et à la commutation des paquets de données dans un réseau privé ou public.

---

## ISO/OSI vs. TCP/IP

`TCP/IP` est un protocole de communication qui permet aux hôtes de se connecter à Internet. Il fait référence au `Transmission Control Protocol` utilisé dans et par les applications sur Internet. Contrairement au modèle `OSI`, il permet un allègement des règles à suivre, à condition que des directives générales soient respectées.

Le modèle `OSI`, quant à lui, est une passerelle de communication (communication gateway) entre le réseau et les utilisateurs finaux. Le modèle OSI est généralement appelé le modèle de référence car il est plus récent и plus largement utilisé. Il est également connu pour son protocole strict et ses limitations.

---

## Transferts de Paquets

Dans un système en couches, les appareils d'une couche échangent des données dans un format différent appelé `unité de données de protocole` (`PDU` - protocol data unit). Par exemple, lorsque nous voulons naviguer sur un site web sur l'ordinateur, le logiciel du serveur distant transmet d'abord les données demandées à la couche application. Elles sont traitées couche par couche, chaque couche remplissant les fonctions qui lui sont assignées. Les données sont ensuite transférées via la couche physique du réseau jusqu'à ce que le serveur de destination ou un autre appareil les reçoive. Les données sont à nouveau acheminées à travers les couches, chaque couche effectuant les opérations qui lui sont assignées jusqu'à ce que le logiciel récepteur utilise les données.

![Comparaison des modèles OSI et TCP/IP avec les PDU : Le modèle OSI a 7 couches, dont Application, Présentation, Session, Transport, Réseau, Liaison de données et Physique. Le modèle TCP/IP a 4 couches : Application, Transport, Internet et Liaison. Les PDU sont les Données, le Segment/Datagramme, le Paquet, la Trame et le Bit.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/net_models_pdu2_updated.png)

Pendant la transmission, chaque couche ajoute un `en-tête` (`header`) à la `PDU` de la couche supérieure, qui contrôle et identifie le paquet. Ce processus est appelé `encapsulation`. L'en-tête et les données forment ensemble la PDU pour la couche suivante. Le processus se poursuit jusqu'à la `Couche Physique` (`Physical Layer`) ou la `Couche Réseau` (`Network Layer`), où les données sont transmises au récepteur. Le récepteur inverse le processus et dépaquette les données à chaque couche avec les informations de l'en-tête. Ensuite, l'application utilise finalement les données. Ce processus se poursuit jusqu'à ce que toutes les données aient été envoyées et reçues.

![Schéma du transfert de paquets montrant l'encapsulation des données de l'expéditeur au destinataire à travers les couches : Données, TCP, IP, MAC et Transmission Binaire, avec les en-têtes et la séquence correspondants.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/packet_transfer.png)

Pour nous, en tant que testeurs d'intrusion (penetration testers), les deux modèles de référence sont utiles. Avec le `TCP/IP`, nous pouvons rapidement comprendre comment l'ensemble de la connexion est établi, et avec le modèle `ISO/OSI`, nous pouvons le démonter pièce par pièce et l'analyser en détail. Cela se produit souvent lorsque nous pouvons écouter et intercepter un trafic réseau spécifique. Nous devons alors analyser ce trafic en conséquence, ce que nous détaillerons dans le module `Analyse du Trafic Réseau` (`Network Traffic Analysis`). Par conséquent, nous devrions nous familiariser avec les deux modèles de référence, les comprendre et les assimiler de la meilleure façon possible.
---

← [[04 - Proxys]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[06 - Le modèle OSI]] →
