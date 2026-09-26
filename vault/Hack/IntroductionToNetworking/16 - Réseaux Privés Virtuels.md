---
tags:
  - networking
ordre: 16
---

# Réseaux Privés Virtuels

---

Un `Réseau Privé Virtuel` (`VPN`, de l'anglais Virtual Private Network) est une technologie qui permet une connexion sécurisée et chiffrée entre un réseau privé et un appareil distant. Cela permet à la machine distante d'accéder directement au réseau privé, offrant un accès sécurisé et confidentiel aux ressources et services du réseau. Par exemple, un administrateur depuis un autre emplacement doit gérer les serveurs internes pour que les employés puissent continuer à utiliser les services internes. De nombreuses entreprises limitent l'accès aux serveurs, de sorte que les clients ne peuvent atteindre ces serveurs qu'à partir du réseau local. C'est là que le VPN entre en jeu : l'administrateur se connecte au serveur VPN via internet, s'authentifie, et crée ainsi un tunnel chiffré afin que d'autres ne puissent pas lire le transfert de données. De plus, l'ordinateur de l'administrateur se voit également attribuer une adresse IP locale (interne) grâce à laquelle il peut accéder aux serveurs internes et les gérer. Les administrateurs utilisent couramment les VPN pour fournir un accès distant sécurisé et économique au réseau d'une entreprise. Un VPN utilise généralement les ports `TCP/1723` pour les connexions VPN `PPTP` ([Point-to-Point Tunneling Protocol](https://www.paloaltonetworks.com/cyberpedia/what-is-pptp)) et `UDP/500` pour les connexions VPN [IKEv1](https://www.cisco.com/c/en/us/support/docs/security-vpn/ipsec-negotiation-ike-protocols/217432-understand-ipsec-ikev1-protocol.html) et [IKEv2](https://nordvpn.com/blog/ikev2ipsec/).

Cela permet aux employés d'accéder au réseau et à ses ressources, comme les serveurs de messagerie et de fichiers, depuis des emplacements distants, tels que leur domicile ou lors de déplacements. Les administrateurs utilisent les VPN pour plusieurs raisons. Les VPN chiffrent la connexion entre l'appareil distant et le réseau privé, ce qui rend beaucoup plus difficile pour les attaquants d'intercepter et de voler des informations sensibles. Grâce à cela, l'ensemble de la communication est plus sécurisé.

Une autre raison est que les VPN permettent aux employés d'accéder au réseau privé et à ses ressources à distance, de n'importe où, tant qu'ils disposent d'une connexion internet. C'est particulièrement utile pour les employés qui doivent travailler à distance, comme ceux qui sont en déplacement ou en télétravail. De plus, les VPN peuvent être plus économiques que d'autres solutions d'accès à distance, telles que les lignes louées ou les connexions dédiées, car ils utilisent l'internet public pour connecter les utilisateurs distants au réseau privé.

De plus, nous pouvons utiliser les VPN pour connecter plusieurs sites distants, comme des succursales, en un seul réseau privé, ce qui facilite la gestion et l'accès aux ressources du réseau. Cependant, plusieurs composants et prérequis sont nécessaires pour qu'un VPN fonctionne :

|**Prérequis**|**Description**|
|---|---|
|`Client VPN`|Ce logiciel est installé sur l'appareil distant et est utilisé pour établir et maintenir une connexion VPN avec le serveur VPN. Par exemple, il peut s'agir d'un client OpenVPN.|
|`Serveur VPN`|Il s'agit d'un ordinateur ou d'un équipement réseau chargé d'accepter les connexions VPN des clients VPN et d'acheminer le trafic entre les clients VPN et le réseau privé.|
|`Chiffrement`|Les connexions VPN sont chiffrées à l'aide de divers algorithmes et protocoles de chiffrement, tels que l'AES et l'IPsec, pour sécuriser la connexion et protéger les données transmises.|
|`Authentification`|Le serveur et le client VPN doivent s'authentifier mutuellement à l'aide d'un secret partagé, d'un certificat ou d'une autre méthode d'authentification pour établir une connexion sécurisée.|

Le client et le serveur VPN utilisent ces ports pour établir et maintenir la connexion VPN. Au niveau de la couche TCP/IP, une connexion VPN utilise généralement le protocole `ESP` ([Encapsulating Security Payload](https://www.ibm.com/docs/en/i/7.4?topic=protocols-encapsulating-security-payload), ou Charge Utile de Sécurité Encapsulée) pour chiffrer et authentifier le trafic VPN. Cela permet au client et au serveur VPN d'échanger des données de manière sécurisée sur l'internet public.

---

## IPsec

La [Sécurité du Protocole Internet](https://www.cloudflare.com/learning/network-layer/what-is-ipsec/) (`IPsec`, de l'anglais Internet Protocol Security) est un protocole de sécurité réseau qui fournit le chiffrement et l'authentification pour les communications sur internet. C'est un protocole de sécurité puissant et largement utilisé qui fournit le chiffrement et l'authentification pour les communications sur internet et qui fonctionne en chiffrant la charge utile de données de chaque paquet IP et en ajoutant un `en-tête d'authentification` (`AH`, de l'anglais authentication header), qui est utilisé pour vérifier l'intégrité et l'authenticité du paquet. L'IPsec utilise une combinaison de deux protocoles pour fournir le chiffrement et l'authentification :

1. [En-tête d'authentification](https://www.ibm.com/docs/en/i/7.1?topic=protocols-authentication-header) (`AH`) : Ce protocole assure l'intégrité et l'authenticité des paquets IP, mais ne fournit pas de chiffrement. Il ajoute un en-tête d'authentification à chaque paquet IP, qui contient une somme de contrôle cryptographique pouvant être utilisée pour vérifier que le paquet n'a pas été altéré.
2. [Charge Utile de Sécurité Encapsulée](https://www.ibm.com/docs/en/i/7.4?topic=protocols-encapsulating-security-payload) (`ESP`) : Ce protocole fournit le chiffrement et, en option, l'authentification des paquets IP. Il chiffre la charge utile de données de chaque paquet IP et ajoute éventuellement un en-tête d'authentification, similaire à l'AH.

L'IPsec peut être utilisé dans deux modes.

|**Mode**|**Description**|
|---|---|
|`Mode transport`|Dans ce mode, l'IPsec chiffre et authentifie la charge utile de données de chaque paquet IP, mais ne chiffre pas l'en-tête IP. Il est généralement utilisé pour sécuriser la communication de bout en bout entre deux hôtes.|
|`Mode tunnel`|Avec ce mode, l'IPsec chiffre et authentifie l'ensemble du paquet IP, y compris l'en-tête IP. Il est généralement utilisé pour créer un tunnel VPN entre deux réseaux.|

Par exemple, un administrateur pourrait placer un pare-feu entre les deux. Afin de faciliter le trafic VPN IPsec d'un client VPN situé à l'extérieur d'un pare-feu vers un serveur VPN situé à l'intérieur, le pare-feu devrait autoriser les protocoles suivants :

|**Protocole**|**Port**|**Description**|
|---|---|---|
|`Protocole Internet` (`IP`)|Numéros de protocole IP `50–51` (`ESP`, `AH`)|C'est le protocole principal qui constitue la base de toutes les communications sur internet. Il est utilisé pour router les paquets de données entre le client VPN et le serveur VPN. Dans le contexte de l'IPsec, les numéros de protocole 50 (ESP) et 51 (AH) identifient les en-têtes liés au VPN utilisés entre le client VPN et le serveur VPN.|
|`Internet Key Exchange` (`IKE`)|`UDP/500`|L'IKE est un protocole utilisé pour établir et maintenir une communication sécurisée entre le client VPN et le serveur VPN. Il est basé sur l'algorithme d'échange de clés Diffie-Hellman et sert à négocier et à établir des clés secrètes partagées qui peuvent être utilisées pour chiffrer et déchiffrer le trafic VPN.|
|`Encapsulating Security Payload` (`ESP`)|Protocole IP `50` _(NAT-T : `UDP/4500`)_|L'ESP est également un protocole qui assure le chiffrement et l'authentification des datagrammes IP. Il est utilisé pour chiffrer le trafic VPN between the VPN client and the VPN server, en utilisant les clés qui ont été négociées avec l'IKE, soit directement en tant que protocole IP 50, soit encapsulé dans l'UDP/4500 lorsque la traversée NAT (NAT traversal) est utilisée.|

Ces protocoles sont nécessaires pour faciliter le trafic VPN IPsec car ils fournissent la sécurité et le chiffrement requis pour une communication sécurisée sur l'internet public. Sans ces protocoles, le trafic VPN serait vulnérable à l'interception et à l'altération.

---

## PPTP

Le [Point-to-Point Tunneling Protocol](https://www.vpnranks.com/blog/pptp-vs-l2tp/) (`PPTP`) est un protocole réseau qui permet la création de VPN en établissant un tunnel sécurisé entre le client et le serveur VPN, et en encapsulant les données transmises dans ce tunnel. Initialement une extension du protocole Point-to-Point (PPP), le PPTP est pris en charge par de nombreux systèmes d'exploitation.

Cependant, en raison de ses vulnérabilités connues, le PPTP n'est plus considéré comme sécurisé. Il peut tunneler des protocoles tels que IP, IPX ou NetBEUI via IP, mais a été largement remplacé par des protocoles VPN plus sécurisés comme L2TP/IPsec, IPsec/IKEv2 et OpenVPN. Depuis 2012, l'utilisation du PPTP a diminué car sa méthode d'authentification, MSCHAPv2, emploie le chiffrement obsolète DES, qui peut être facilement cassé avec du matériel spécialisé.
---

← [[15 - Réseaux sans fil]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[17 - Informations Spécifiques au Fournisseur]] →
