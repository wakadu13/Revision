---
tags:
  - networking
ordre: 19
---

# Protocoles d'authentification

---

De nombreux protocoles d'authentification différents sont utilisés en réseau pour vérifier l'identité des appareils et des utilisateurs. Ces protocoles sont essentiels car ils fournissent un moyen sécurisé et normalisé de `vérifier l'identité` des utilisateurs, des appareils et d'autres entités sur un réseau. Sans protocoles d'authentification, il serait difficile d'identifier de manière sûre et fiable les entités sur un réseau, ce qui permettrait aux attaquants d'obtenir facilement un accès non autorisé et de compromettre potentiellement le réseau.

Les protocoles d'authentification fournissent également un moyen d'`échanger des informations de manière sécurisée` entre les entités d'un réseau, ce que nous aborderons brièvement. Ceci est important pour garantir la confidentialité et l'intégrité des données sensibles et pour empêcher les accès non autorisés et autres menaces de sécurité. Examinons quelques-uns des protocoles d'authentification les plus couramment utilisés :

|**Protocole**|**Description**|
|---|---|
|`Kerberos`|Protocole d'authentification basé sur un Centre de Distribution de Clés (KDC - Key Distribution Center) qui utilise des tickets dans les environnements de domaine.|
|`SRP`|C'est un protocole d'authentification basé sur un mot de passe qui utilise la cryptographie pour se protéger contre l'écoute clandestine (eavesdropping) et les attaques de l'homme du milieu (man-in-the-middle).|
|`SSL`|Un protocole cryptographique utilisé pour la communication sécurisée sur un réseau informatique.|
|`TLS`|TLS est un protocole cryptographique qui assure la sécurité des communications sur Internet. C'est le successeur du SSL.|
|`OAuth`|Une norme ouverte pour l'autorisation qui permet aux utilisateurs d'accorder un accès tiers à leurs ressources web sans partager leurs mots de passe.|
|`OpenID`|OpenID est un protocole d'authentification décentralisé qui permet aux utilisateurs d'utiliser une seule identité pour se connecter à plusieurs sites web.|
|`SAML`|Le Security Assertion Markup Language est une norme basée sur XML pour échanger en toute sécurité des données d'authentification et d'autorisation entre les parties.|
|`2FA`|Une méthode d'authentification qui utilise une combinaison de deux facteurs différents pour vérifier l'identité d'un utilisateur.|
|`FIDO`|L'alliance FIDO (Fast IDentity Online) est un consortium d'entreprises qui travaillent au développement de normes ouvertes pour l'authentification forte.|
|`PKI`|L'Infrastructure à Clé Publique (PKI - Public Key Infrastructure) est un système d'échange sécurisé d'informations basé sur l'utilisation de clés publiques et privées pour le chiffrement et les signatures numériques.|
|`SSO`|Une méthode d'authentification, dite d'authentification unique (SSO - Single Sign-On), qui permet à un utilisateur d'utiliser un seul jeu d'identifiants pour accéder à plusieurs applications.|
|`MFA`|L'authentification multifacteur (MFA - Multi-Factor Authentication) est une méthode d'authentification qui utilise plusieurs facteurs, comme quelque chose que l'utilisateur connaît (un mot de passe), quelque chose que l'utilisateur possède (un téléphone), ou quelque chose que l'utilisateur est (données biométriques), pour vérifier son identité.|
|`PAP`|Un protocole d'authentification simple qui envoie le mot de passe d'un utilisateur en clair sur le réseau.|
|`CHAP`|Un protocole d'authentification qui utilise une poignée de main à trois voies (three-way handshake) pour vérifier l'identité d'un utilisateur.|
|`EAP`|Un framework (cadre) permettant de prendre en charge plusieurs méthodes d'authentification, autorisant l'utilisation de diverses technologies pour vérifier l'identité d'un utilisateur.|
|`SSH`|C'est un protocole réseau pour la communication sécurisée entre un client et un serveur. On peut l'utiliser pour l'accès en ligne de commande à distance et l'exécution de commandes à distance, ainsi que pour le transfert de fichiers sécurisé. SSH utilise le chiffrement pour se protéger contre l'écoute clandestine et d'autres attaques et peut également être utilisé pour l'authentification.|
|`HTTPS`|C'est une version sécurisée du protocole HTTP utilisée pour la communication sur Internet. HTTPS utilise SSL/TLS pour chiffrer la communication et fournir une authentification, garantissant que des tiers ne peuvent pas intercepter et lire les données transmises. Il est largement utilisé pour la communication sécurisée sur Internet, en particulier pour la navigation web.|
|`LEAP`|LEAP est un protocole d'authentification sans fil développé par Cisco. Il utilise EAP pour fournir une authentification mutuelle entre un client sans fil et un serveur et utilise l'algorithme de chiffrement RC4 pour chiffrer la communication entre les deux. Malheureusement, LEAP est vulnérable aux attaques par dictionnaire et à d'autres failles de sécurité et a été largement remplacé par des protocoles plus sécurisés tels que EAP-TLS et PEAP.|
|`PEAP`|PEAP, d'un autre côté, est un protocole de tunnellisation (tunneling) sécurisé utilisé pour les réseaux sans fil et filaires. Il est basé sur EAP et utilise TLS pour chiffrer la communication entre un client et un serveur. PEAP utilise un certificat côté serveur pour authentifier le serveur et peut également être utilisé pour authentifier le client à l'aide de diverses méthodes, telles que des mots de passe, des certificats ou des données biométriques. PEAP est largement utilisé dans les réseaux d'entreprise pour une authentification sécurisée.|

Par exemple, LEAP et PEAP peuvent être utilisés pour authentifier les clients sans fil lorsqu'ils accèdent au réseau sans fil ou pour authentifier les employés distants se connectant au réseau via un VPN. Dans ces cas, l'utilisation de SSH ou HTTPS serait difficile à mettre en œuvre, car ils sont conçus pour des objectifs différents. En termes de sécurité, `PEAP` est généralement plus sûr que LEAP car il utilise un certificat de clé publique côté serveur pour authentifier le serveur et chiffrer le hachage `MSCHAPv2`, tandis que `LEAP` repose sur un secret partagé qui est négocié entre le client et le serveur et ne chiffre `pas` les hachages `MSCHAPv2`. PEAP prend également en charge l'utilisation d'algorithmes de chiffrement plus forts, tels que AES et 3DES, pour chiffrer les informations d'authentification, alors que LEAP utilise l'algorithme RC4, plus faible.

Cependant, les deux protocoles sont vulnérables à des attaques spécifiques et ont été largement remplacés par des protocoles plus sécurisés tels que EAP-TLS.

Pour les connexions physiques, les protocoles avec `SSL` ou `TLS` sont utilisés par défaut, tels que `SSH` ou `HTTPS`. Ces deux protocoles utilisent des algorithmes de chiffrement robustes pour protéger les informations d'authentification transmises entre le client et le serveur. Cela aide à empêcher l'interception ou l'altération des données d'authentification, ce qui est essentiel pour maintenir la sécurité du processus d'authentification. De plus, ils prennent en charge l'utilisation de certificats numériques et de la `PKI` pour authentifier le serveur auprès du client. Cela garantit que le client peut vérifier l'identité du serveur et aide à prévenir les attaques MITM. SSH et HTTPS sont des protocoles largement utilisés et bien pris en charge, avec des implémentations disponibles pour divers systèmes d'exploitation et appareils, ce qui les rend faciles à utiliser et à déployer dans une variété d'environnements.
---

← [[18 - Mécanismes d'échange de clés]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[20 - Connexions TCP-UDP]] →
