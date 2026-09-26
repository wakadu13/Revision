---
tags:
  - networking
ordre: 21
---

# Cryptographie

---

Le chiffrement est utilisé sur Internet pour transmettre des données, telles que des informations de paiement, des e-mails ou des données personnelles, de manière confidentielle et protégée contre la manipulation. Les données sont chiffrées à l'aide de divers algorithmes cryptographiques basés sur des opérations mathématiques. À l'aide du chiffrement, les données peuvent être transformées sous une forme que les personnes non autorisées ne peuvent plus lire. Des clés numériques sont utilisées pour le chiffrement dans les processus de chiffrement `symétrique` ou `asymétrique`. Il est plus ou moins facile de forcer les textes chiffrés ou les clés en fonction des méthodes de chiffrement utilisées. Si des méthodes cryptographiques de pointe avec de longues longueurs de clé sont utilisées, elles fonctionnent de manière très sécurisée et sont presque impossibles à compromettre pour le moment. En principe, on peut distinguer les techniques de chiffrement `symétrique` et `asymétrique`. Les méthodes asymétriques ne sont connues que depuis quelques décennies. Néanmoins, ce sont les méthodes les plus fréquemment utilisées dans la communication numérique.

#### Chiffrement symétrique

Le chiffrement symétrique, également connu sous le nom de chiffrement à clé secrète (secret key encryption), est une méthode qui utilise la même clé pour chiffrer et déchiffrer les données. Cela signifie que l'expéditeur et le destinataire doivent avoir la même clé pour déchiffrer correctement les données.

Si la clé secrète est partagée ou perdue, la sécurité des données n'est plus garantie. Les actions critiques pour les méthodes de chiffrement symétrique sont la distribution, le stockage et l'échange des clés. L'[Advanced Encryption Standard](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) (`AES`) et le [Data Encryption Standard](https://en.wikipedia.org/wiki/Data_Encryption_Standard) (`DES`) sont des exemples d'algorithmes de chiffrement symétrique. Ce type de chiffrement est souvent utilisé pour chiffrer de grandes quantités de données, comme des fichiers sur un disque dur ou des données envoyées sur un réseau. `AES` est considéré de nos jours comme l'algorithme de chiffrement le plus sûr.

#### Chiffrement asymétrique

Le chiffrement asymétrique, également connu sous le nom de `chiffrement à clé publique` (public-key encryption), est une méthode de chiffrement qui utilise deux clés différentes :

- une `clé publique` (public key)
- une `clé privée` (private key)

La clé publique est utilisée pour chiffrer les données, tandis que la clé privée est utilisée pour les déchiffrer. Cela signifie que n'importe qui peut utiliser une clé publique pour chiffrer des données pour quelqu'un, mais seul le destinataire possédant la clé privée associée peut déchiffrer les données. Les exemples de méthodes de chiffrement asymétrique incluent [Rivest–Shamir–Adleman](https://en.wikipedia.org/wiki/RSA_\(cryptosystem\)) (`RSA`), [Pretty Good Privacy](https://en.wikipedia.org/wiki/Pretty_Good_Privacy) (`PGP`) et [Elliptic Curve Cryptography](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography) (`ECC`). Le chiffrement asymétrique est utilisé dans une variété d'applications, dont certaines incluent :

||||
|---|---|---|
|Signatures électroniques|SSL/TLS|VPN|
|SSH|PKI|Cloud|

---

## Chiffrement à clé publique

Un avantage du chiffrement asymétrique est sa `sécurité`. Étant donné que la sécurité est basée sur des problèmes mathématiques très difficiles à résoudre, les attaques simples ne peuvent pas le forcer. De plus, le problème de l'échange de clés est contourné. C'est un problème important avec les méthodes de chiffrement symétrique. Cependant, comme la clé publique peut être accessible à tous, il n'est pas nécessaire d'échanger les clés secrètement. De plus, les méthodes asymétriques ouvrent la possibilité d'une authentification avec des signatures numériques.

---

## Data Encryption Standard

DES est un chiffrement par bloc à clé symétrique (symmetric-key block cipher), et son chiffrement fonctionne comme une combinaison du masque jetable (one-time pad), de la permutation et des chiffrements par substitution appliqués à des séquences de bits. Il utilise la `même clé` pour `chiffrer et déchiffrer` les données.

La clé est composée de `64 bits`, dont `8 bits` sont utilisés comme somme de contrôle (checksum). Par conséquent, la longueur réelle de la clé de DES n'est que de `56 bits`. Et c'est pourquoi on parle toujours d'une longueur de clé de 56 bits en référence à DES. Pour éviter le danger de l'analyse fréquentielle, ce ne sont pas des lettres uniques, mais chaque bloc de 64 bits de texte en clair qui est chiffré en un bloc de 64 bits de texte chiffré.

Une extension de DES est le [Triple DES / 3DES](https://en.wikipedia.org/wiki/Triple_DES), qui chiffre les données de manière plus sécurisée. La procédure pour cela consiste généralement en trois clés, la première clé étant utilisée pour chiffrer les données, la deuxième pour déchiffrer les données et la troisième pour chiffrer à nouveau les données.

`3DES` était considéré comme plus sûr que le DES original car il offre une plus grande sécurité en utilisant trois tours de chiffrement, bien que l'utilisation d'une clé de 56 bits le limite encore. `AES`, le successeur de DES, offre une sécurité supérieure en utilisant des longueurs de clé plus longues et est maintenant la technologie de chiffrement symétrique la plus utilisée.

---

## Advanced Encryption Standard

Comparé à DES, AES utilise des clés de 128 bits (`AES-128`), 192 bits (`AES-192`) ou 256 bits (`AES-256`) pour chiffrer et déchiffrer les données. De plus, AES est plus rapide que DES car sa structure d'algorithme est plus efficace. En effet, il peut être appliqué à plusieurs blocs de données à la fois, ce qui le rend plus rapide. Cela signifie que le chiffrement et le déchiffrement AES peuvent être effectués plus rapidement que DES, ce qui est particulièrement important lorsque de grandes quantités de données doivent être chiffrées.

Par exemple, nous pouvons trouver AES dans de nombreuses applications et protocoles différents, sans s'y limiter :

||||
|---|---|---|
|WLAN IEEE 802.11i|IPsec|SSH|
|VoIP|PGP|OpenSSL|

---

## Modes de chiffrement

Un mode de chiffrement (cipher mode) fait référence à la manière dont un algorithme de chiffrement par bloc (block cipher) chiffre un message en clair. Un algorithme de chiffrement par bloc chiffre les données, chacune utilisant des blocs de données de taille fixe (généralement 64 ou 128 bits). Un mode de chiffrement définit comment ces blocs sont traités et combinés pour chiffrer un message de n'importe quelle longueur. Il existe plusieurs modes de chiffrement courants, notamment :

|**Mode de chiffrement**|**Description**|
|---|---|
|Mode [Electronic Code Book](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation) (`ECB`)|Le mode ECB n'est généralement pas recommandé en raison de sa vulnérabilité à certains types d'attaques. De plus, il ne masque pas efficacement les motifs de données. Par conséquent, une analyse statistique peut révéler des éléments de messages en clair, par exemple dans les applications web.|
|Mode [Cipher Block Chaining](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CBC) (`CBC`)|Le mode CBC est généralement utilisé pour chiffrer des messages comme le chiffrement de disque et la communication par e-mail. C'est le mode par défaut pour AES et est également utilisé dans des logiciels comme TrueCrypt, VeraCrypt, TLS et SSL.|
|Mode [Cipher Feedback](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_feedback_\(CFB\)) (`CFB`)|Le mode CFB est bien adapté au chiffrement en temps réel d'un flux de données, par ex. le chiffrement des communications réseau ou le chiffrement/déchiffrement de fichiers en transit comme les Public-Key Cryptography Standards (PKCS) et BitLocker de Microsoft.|
|Mode [Output Feedback](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#OFB) (`OFB`)|Le mode OFB est également utilisé pour chiffrer un flux de données, par ex. pour chiffrer la communication en temps réel. Cependant, ce mode est considéré comme meilleur pour le flux de données en raison de la manière dont le flux de clés est généré. On peut trouver ce mode dans PKCS mais aussi dans le protocole SSH.|
|Mode [Counter](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CTR) (`CTR`)|Le mode CTR chiffre les flux de données en temps réel qu'AES utilise, par ex. la communication réseau, le chiffrement de disque et d'autres scénarios en temps réel où les données sont traitées. Un exemple de cela serait IPsec ou BitLocker de Microsoft.|
|Mode [Galois/Counter](https://en.wikipedia.org/wiki/Galois/Counter_Mode) (`GCM`)|GCM est utilisé dans les cas où la confidentialité et l'intégrité doivent être protégées ensemble, comme les communications sans fil, les VPN et autres protocoles de communication sécurisés.|

Chaque mode a ses propres caractéristiques et est plus adapté à certains cas d'utilisation. Le choix du mode de chiffrement dépend des exigences de l'application et des objectifs de sécurité à atteindre.
---

← [[20 - Connexions TCP-UDP]] | [[00 - Sommaire Introduction to Networking|Sommaire]]
