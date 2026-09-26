---
tags:
  - networking
ordre: 18
---

# Mécanismes d'échange de clés

---

Les méthodes d'échange de clés sont utilisées pour échanger des [clés cryptographiques](https://www.cloudflare.com/learning/ssl/what-is-a-cryptographic-key/) (cryptographic keys) de manière sécurisée entre deux parties. C'est un élément essentiel de nombreux protocoles cryptographiques, car la sécurité du chiffrement utilisé pour protéger la communication repose sur le secret des clés. Il existe de nombreuses méthodes d'échange de clés, chacune avec des caractéristiques et des forces uniques. Certaines méthodes d'échange de clés sont plus sécurisées que d'autres, et la méthode appropriée dépend des circonstances et des exigences spécifiques de la situation.

Ces méthodes fonctionnent généralement en permettant aux deux parties de s'accorder sur une `shared secret key` (clé secrète partagée) via un canal de communication non sécurisé, qui chiffre la communication entre elles. Cela se fait généralement à l'aide d'une forme d'opération mathématique, comme un calcul basé sur les propriétés d'une fonction mathématique ou une série de manipulations simples de la clé.

#### Diffie-Hellman

Une méthode d'échange de clés courante est l'[échange de clés Diffie-Hellman](https://www.comparitech.com/blog/information-security/diffie-hellman-key-exchange/), qui permet à deux parties de s'accorder sur une clé secrète partagée sans aucune communication préalable ou information privée partagée. Il est basé sur le concept de deux parties générant une clé secrète partagée qui peut être utilisée pour chiffrer et déchiffrer les messages entre elles. Il est souvent utilisé comme base pour établir des canaux de communication sécurisés, comme dans le protocole [Sécurité de la couche de transport](https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/) (Transport Layer Security, `TLS`) utilisé pour protéger le trafic web.

L'une des principales limitations de l'échange de clés `Diffie-Hellman` est sa vulnérabilité aux `MITM attacks` (attaques de l'homme du milieu). Dans une attaque MITM, nous interceptons la communication entre les deux parties et prétendons être l'une d'entre elles, générant une clé secrète différente et trompant les deux parties pour qu'elles l'utilisent. Cela permet à l'attaquant de lire et de modifier les messages envoyés entre les parties.

Une autre considération pratique est la performance : le `DH` classique sur corps fini est généralement plus lourd que le DH sur courbe elliptique (`ECDH`) à des niveaux de sécurité comparables, ce qui peut affecter les appareils à faible consommation ou sensibles à la latence.

#### RSA

Un autre algorithme à clé publique (public-key algorithm) largement utilisé est l'algorithme [Rivest–Shamir–Adleman](https://web.archive.org/web/20240302211950/https://venafi.com/blog/how-diffie-hellman-key-exchange-different-rsa/) (`RSA`), qui utilise les propriétés des grands nombres premiers pour générer une clé secrète partagée. Cette méthode repose sur le fait qu'il est relativement facile de multiplier de grands nombres premiers entre eux, mais difficile de factoriser le nombre résultant en ses facteurs premiers. Outre ces deux-là, il en existe quelques autres que nous devons examiner. Il est également largement utilisé dans de nombreuses autres applications et protocoles qui nécessitent une communication et une protection des données sécurisées, y compris, mais sans s'y limiter :

- Chiffrer et signer des messages pour assurer la confidentialité et l'authentification
- Protéger les données en transit sur les réseaux, comme dans les protocoles [Secure Socket Layer](https://www.cloudflare.com/learning/ssl/what-is-ssl/) (`SSL`) et `TLS`
- Générer et vérifier des signatures numériques, qui sont utilisées pour fournir l'authenticité et l'intégrité des documents électroniques et autres données numériques
- Authentifier les utilisateurs et les appareils, comme dans le protocole [Public Key Cryptography for Initial Authentication in Kerberos](https://www.ietf.org/rfc/rfc4556.txt) (`PKINIT`) utilisé par le système d'authentification réseau Kerberos
- Protéger les informations sensibles, comme dans le chiffrement des données personnelles et des documents confidentiels

#### ECDH

Le [Diffie-Hellman sur courbe elliptique](https://medium.com/swlh/understanding-ec-diffie-hellman-9c07be338d4a) (`ECDH`) est une variante de l'échange de clés Diffie-Hellman qui utilise la cryptographie sur courbe elliptique (elliptic curve cryptography, `ECC`) pour générer la clé secrète partagée. Il a l'avantage d'être plus efficace et sécurisé que l'algorithme Diffie-Hellman original, y compris, mais sans s'y limiter :

- Établir des canaux de communication sécurisés, comme dans le protocole `TLS`
- Fournir une confidentialité persistante (forward secrecy), qui garantit que les communications passées ne peuvent pas être révélées même si les clés privées sont compromises
- Authentifier les utilisateurs et les appareils, comme dans le protocole [Internet Key Exchange](https://docs.oracle.com/cd/E19683-01/816-7264/6md9iem1g/index.html) (`IKE`) utilisé dans les VPN (réseaux privés virtuels)

#### ECDSA

L'[algorithme de signature numérique sur courbe elliptique](https://www.hypr.com/security-encyclopedia/elliptic-curve-digital-signature-algorithm) (Elliptic Curve Digital Signature Algorithm, `ECDSA`) utilise la cryptographie sur courbe elliptique (`ECC`) pour générer des signatures numériques qui peuvent authentifier les parties impliquées dans l'échange de clés.

Résumons et comparons ces algorithmes :

|**Algorithme**|**Acronyme**|**Sécurité**|
|---|---|---|
|`Diffie-Hellman`|`DH`|Sécurisé avec des paramètres robustes et une authentification ; plus lent que `ECDH` à sécurité équivalente|
|`Rivest–Shamir–Adleman`|`RSA`|Largement utilisé et considéré comme sécurisé avec des tailles de clé adéquates ; plus coûteux en calcul que `ECC` à des niveaux de sécurité comparables|
|`Elliptic Curve Diffie-Hellman`|`ECDH`|Offre une sécurité et une vitesse améliorées par rapport au `Diffie-Hellman` traditionnel|
|`Elliptic Curve Digital Signature Algorithm`|`ECDSA`|Offre une sécurité et une efficacité améliorées pour la génération de signatures numériques|

---

## Internet Key Exchange

L'[Internet Key Exchange](https://www.hypr.com/security-encyclopedia/internet-key-exchange) (`IKE`) est un protocole utilisé pour établir et maintenir des sessions de communication sécurisées, telles que celles utilisées dans les VPN. Il utilise une combinaison de l'algorithme d'échange de clés `Diffie-Hellman` et d'`autres techniques cryptographiques` pour échanger des clés en toute sécurité et négocier les paramètres de sécurité. De plus, c'est un composant clé de nombreuses solutions VPN, car il permet l'échange sécurisé de clés et d'autres informations de sécurité entre le client et le serveur VPN. Cela permet au VPN d'établir un tunnel chiffré à travers lequel les données peuvent être transmises en toute sécurité.

IKE peut également être utilisé à d'autres fins, comme pour l'authentification des utilisateurs et des appareils. Il est généralement utilisé en conjonction avec d'autres protocoles et algorithmes, tels que l'algorithme RSA pour l'échange de clés et les signatures numériques, et l'[Advanced Encryption Standard](https://www.geeksforgeeks.org/advanced-encryption-standard-aes/) (`AES`) pour le chiffrement des données.

IKE fonctionne soit en `main mode` soit en `aggressive mode`. Ces modes déterminent la séquence et les paramètres du processus d'échange de clés et peuvent affecter la sécurité et les performances de la session IKE.

#### Main Mode

Le `main mode` est le mode par défaut pour `IKE` et est généralement considéré comme `plus sécurisé` que le mode agressif. Le processus d'échange de clés est effectué en `trois phases` dans le mode principal, chacune échangeant un ensemble différent de paramètres de sécurité et de clés. Cela permet une plus grande flexibilité et sécurité, mais peut également entraîner des performances plus lentes par rapport au mode agressif.

#### Aggressive Mode

L'`aggressive mode` est un mode alternatif pour `IKE` qui offre des `performances plus rapides` en réduisant le nombre d'allers-retours et d'échanges de messages requis pour l'échange de clés. Dans ce mode, le processus d'échange de clés est effectué en `deux phases`, avec tous les paramètres de sécurité et les clés échangés dans la première phase. Cependant, bien que cela puisse offrir des performances plus rapides, cela peut également réduire la sécurité de la session IKE par rapport au mode principal, car l'`aggressive mode` ne fournit pas de protection de l'identité.

#### Pre-Shared Keys

Dans IKE, une `Pre-Shared Key` (`PSK`) ou clé pré-partagée est une valeur secrète partagée entre les deux parties impliquées dans l'échange de clés. Cette clé est utilisée pour authentifier les parties et établir un secret partagé qui chiffre la communication ultérieure. L'utilisation d'une PSK est facultative dans IKE, et le choix de l'utiliser ou non dépend des exigences et des contraintes spécifiques de la situation. Cependant, si une `PSK` est utilisée, elle doit être échangée de manière sécurisée entre les deux parties avant le début du processus d'échange de clés. Cela peut être fait via un canal hors-bande (out-of-band) sécurisé, tel qu'un canal de communication séparé, ou en échangeant physiquement la clé.

Le principal avantage de l'utilisation d'une PSK est qu'elle fournit une couche de sécurité supplémentaire en permettant aux parties de s'authentifier mutuellement. Cependant, l'utilisation d'une PSK présente également certaines limitations et inconvénients. Par exemple, il peut être difficile d'échanger la clé de manière sécurisée, et si la clé est compromise par une attaque MITM, la sécurité de la session IKE peut être compromise.
---

← [[17 - Informations Spécifiques au Fournisseur]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[19 - Protocoles d'authentification]] →
