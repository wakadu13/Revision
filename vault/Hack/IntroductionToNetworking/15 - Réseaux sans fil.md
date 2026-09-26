---
tags:
  - networking
ordre: 15
---

# Réseaux sans fil

---

Les réseaux sans fil sont des réseaux informatiques qui utilisent des connexions de données sans fil entre les nœuds du réseau. Ces réseaux permettent à des appareils tels que des ordinateurs portables, des smartphones et des tablettes de communiquer entre eux et avec Internet sans avoir besoin de connexions physiques telles que des câbles.

Les réseaux sans fil utilisent la technologie de radiofréquence (`RF`, Radio Frequency) pour transmettre des données entre les appareils. Chaque appareil sur un réseau sans fil dispose d'un adaptateur sans fil qui convertit les données en signaux RF et les envoie par voie hertzienne. D'autres appareils sur le réseau reçoivent ces signaux avec leurs propres adaptateurs sans fil, et les données sont alors reconverties dans un format utilisable. Ceux-ci peuvent fonctionner sur différentes portées, en fonction de la technologie utilisée. Par exemple, un réseau local (LAN, Local Area Network) qui couvre une petite zone, comme une maison ou un petit bureau, pourrait utiliser une technologie sans fil appelée `WiFi`, dont la portée est de quelques centaines de pieds. D'un autre côté, un réseau étendu sans fil (`WWAN`, Wireless Wide Area Network) pourrait utiliser une technologie de télécommunication mobile telle que les données cellulaires (`3G`, `4G LTE`, `5G`), qui peut couvrir une zone beaucoup plus vaste, comme une ville ou une région entière.

Par conséquent, pour se connecter à un réseau sans fil, un appareil doit être à portée du réseau et configuré avec les bons paramètres réseau, tels que le nom du réseau et le mot de passe. Une fois connectés, les appareils peuvent communiquer entre eux et avec Internet, permettant aux utilisateurs d'accéder à des ressources en ligne et d'échanger des données.

Dans un réseau WiFi, la communication entre les appareils s'effectue par RF dans les bandes de `2.4 GHz` ou `5 GHz`. Lorsqu'un appareil, comme un ordinateur portable, veut envoyer des données sur le réseau, il communique d'abord avec le [point d'accès sans fil](https://en.wikipedia.org/wiki/Wireless_access_point) (`WAP`, Wireless Access Point) pour demander la permission de transmettre. Le WAP est un appareil central, comme un routeur, qui connecte le réseau sans fil à un réseau filaire et contrôle l'accès au réseau. Une fois que le WAP accorde la permission, l'appareil émetteur envoie les données sous forme de signaux RF, qui sont reçus par les adaptateurs sans fil des autres appareils sur le réseau. Les données sont ensuite reconverties dans un format utilisable et transmises à l'application ou au système approprié.

L'intensité du signal RF et la distance qu'il peut parcourir sont influencées par des facteurs tels que la puissance de l'émetteur, la présence d'obstacles et la densité du bruit RF dans l'environnement. Ainsi, pour garantir une communication fiable, les réseaux WiFi utilisent des techniques telles que la transmission à étalement de spectre et la correction d'erreurs pour surmonter ces défis.

---

## Connexion WiFi

L'appareil doit également être configuré avec les bons paramètres réseau, tels que le nom du réseau / [identifiant de l'ensemble de services](https://www.geeksforgeeks.org/service-set-identifier-ssid-in-computer-network/) (`SSID`, Service Set Identifier) et le `password`. Ainsi, pour se connecter au routeur, l'ordinateur portable utilise un protocole de réseau sans fil appelé [IEEE 802.11](https://en.wikipedia.org/wiki/IEEE_802.11). Ce protocole définit les détails techniques de la manière dont les appareils sans fil communiquent entre eux et avec les WAP. Lorsqu'un appareil souhaite rejoindre un réseau WiFi, il envoie une requête au WAP pour lancer le processus de connexion. Cette requête est connue sous le nom de `connection request frame` ou `association request` et est envoyée en utilisant le protocole de réseau sans fil `IEEE 802.11`. La trame de demande de connexion contient divers champs d'information, incluant, mais sans s'y limiter :

|||
|---|---|
|`MAC address`|Un identifiant unique pour l'adaptateur sans fil de l'appareil.|
|`SSID`|Le nom du réseau, également connu sous le nom de `Service Set Identifier` du réseau WiFi.|
|`Supported data rates`|Une liste des débits de données avec lesquels l'appareil peut communiquer.|
|`Supported channels`|Une liste des `channels` (canaux) sur lesquels l'appareil peut communiquer.|
|`Supported security protocols`|Une liste des protocoles de sécurité que l'appareil est capable d'utiliser, tels que `WPA2`/`WPA3`.|

L'appareil utilise ensuite ces informations pour configurer son adaptateur sans fil et se connecter au WAP. Une fois la connexion établie, l'appareil peut communiquer avec le WAP et d'autres appareils du réseau. Il peut également accéder à Internet et à d'autres ressources en ligne via le WAP, qui agit comme une passerelle vers le réseau filaire. Cependant, le `SSID` peut être masqué en désactivant sa diffusion. Cela signifie que les appareils qui recherchent ce WAP spécifique ne pourront pas identifier son `SSID`. Néanmoins, le `SSID` peut toujours être trouvé dans le paquet d'authentification.

En plus du protocole `IEEE 802.11`, d'autres protocoles et technologies réseau peuvent également être utilisés, comme TCP/IP, DHCP et WPA2, dans un réseau WiFi pour effectuer des tâches telles que l'attribution d'adresses IP aux appareils, le routage du trafic entre les appareils et la fourniture de la sécurité.

#### Échange défi-réponse WEP

L'échange défi-réponse est un processus visant à établir une connexion sécurisée entre un WAP et un appareil client dans un réseau sans fil qui utilise le protocole de sécurité WEP. Cela implique l'échange de paquets entre le WAP et l'appareil client pour authentifier l'appareil et établir une connexion sécurisée.

|**Étape**|**Qui**|**Description**|
|---|---|---|
|1|`Client`|Envoie un paquet de demande d'association au WAP pour demander l'accès.|
|2|`WAP`|Répond au client avec un paquet de réponse d'association, qui inclut une chaîne de défi.|
|3|`Client`|Calcule une réponse à la chaîne de défi à l'aide d'une clé secrète partagée et la renvoie au WAP.|
|4|`WAP`|Calcule la réponse attendue au défi avec la même clé secrète partagée et envoie un paquet de réponse d'authentification au client.|

Néanmoins, certains paquets peuvent se perdre, c'est pourquoi la somme de contrôle `CRC` a été intégrée. Le [contrôle de redondance cyclique](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) (`CRC`, Cyclic Redundancy Check) est un mécanisme de détection d'erreurs utilisé dans le protocole WEP pour protéger contre la corruption de données dans les communications sans fil. Une valeur CRC est calculée pour chaque paquet transmis sur le réseau sans fil en fonction des données du paquet. Elle est utilisée pour vérifier l'intégrité des données. Lorsque l'appareil de destination reçoit le paquet, la valeur CRC est recalculée et comparée à la valeur originale. Si les valeurs correspondent, les données ont été transmises avec succès sans aucune erreur. Cependant, si les valeurs ne correspondent pas, les données ont été corrompues et doivent être retransmises.

La conception du mécanisme `CRC` présente une faille qui nous permet de déchiffrer un paquet unique `without` connaître la `encryption key`. Cela est dû au fait que la valeur `CRC` est calculée en utilisant les données en `plaintext` dans le paquet plutôt que les données chiffrées. En WEP, la valeur CRC est incluse dans l'en-tête du paquet avec les données chiffrées. Lorsque l'appareil de destination reçoit le paquet, la valeur `CRC` est recalculée et comparée à l'originale pour s'assurer que les données ont été transmises avec succès sans aucune erreur. Cependant, nous pouvons utiliser le `CRC` pour déterminer les données en `plaintext` dans le paquet, même si les données sont chiffrées.

---

## Fonctionnalités de sécurité

Les réseaux WiFi disposent de plusieurs fonctionnalités de sécurité pour se protéger contre les accès non autorisés et garantir la confidentialité et l'intégrité des données transmises sur le réseau. Parmi les principales fonctionnalités de sécurité, on trouve, sans s'y limiter :

- Chiffrement
- Contrôle d'accès
- Pare-feu

#### Chiffrement

Nous pouvons utiliser divers algorithmes de chiffrement pour protéger la confidentialité des données transmises sur les réseaux sans fil. Les algorithmes de chiffrement les plus courants dans les réseaux WiFi sont la [confidentialité équivalente au filaire](https://en.wikipedia.org/wiki/Wired_Equivalent_Privacy) (`WEP`, Wired Equivalent Privacy), [l'accès protégé Wi-Fi 2](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access#WPA2) (`WPA2`, WiFi Protected Access 2) et [l'accès protégé Wi-Fi 3](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access#WPA3) (`WPA3`, WiFi Protected Access 3).

#### Contrôle d'accès

Les réseaux WiFi sont configurés par défaut pour autoriser les appareils autorisés à rejoindre le réseau en utilisant des méthodes d'authentification spécifiques. Cependant, ces méthodes peuvent être modifiées en exigeant un mot de passe ou un identifiant unique (comme une adresse MAC) pour identifier les appareils autorisés.

#### Pare-feu

Un pare-feu est un système de sécurité qui contrôle le trafic réseau entrant et sortant en fonction de règles de sécurité prédéterminées. Par exemple, les routeurs WiFi ont souvent des pare-feu intégrés qui peuvent bloquer le trafic entrant depuis Internet et protéger contre divers types de cybermenaces.

---

## Protocoles de chiffrement

La [confidentialité équivalente au filaire](https://en.wikipedia.org/wiki/Wired_Equivalent_Privacy) (`WEP`) et [l'accès protégé Wi-Fi](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Access) (`WPA`, WiFi Protected Access) sont des protocoles de chiffrement qui sécurisent les données transmises sur un réseau WiFi. Le WPA peut utiliser différents algorithmes de chiffrement, y compris la [norme de chiffrement avancée](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) (`AES`, Advanced Encryption Standard).

#### WEP

`WEP` utilise une clé de `40-bit` ou `104-bit` pour chiffrer les données, tandis que `WPA using AES` utilise une clé de `128-bit`. Des clés plus longues offrent un chiffrement plus robuste et sont plus résistantes aux attaques. Cependant, il est vulnérable à diverses attaques qui peuvent permettre à un attaquant de déchiffrer les données transmises sur le réseau. De plus, le WEP n'est pas compatible avec les appareils et systèmes d'exploitation plus récents et n'est généralement plus considéré comme sécurisé. Enfin, `WEP` utilise l'algorithme de chiffrement `RC4 cipher`, ce qui le rend vulnérable aux attaques.

Cependant, WEP utilise une `shared key` pour l'authentification, ce qui signifie que la même clé est utilisée pour le chiffrement et l'authentification. Il existe deux versions du protocole WEP :

- `WEP-40`/`WEP-64`
- `WEP-104`

Le `WEP-40`, également connu sous le nom de `WEP-64`, utilise une clé (secrète) de `40-bit`, tandis que le `WEP-104` utilise une clé de `104-bit`. La clé est divisée en un [vecteur d'initialisation](https://en.wikipedia.org/wiki/Initialization_vector) (`IV`, Initialization Vector) et une `secret key`.

L'`IV` est une petite valeur incluse dans l'en-tête du paquet avec les données chiffrées et est utilisé pour créer la clé pour `WEP-40` et `WEP-104` et est inclus pour garantir que chaque clé est unique. La `secret key` est une série de bits aléatoires utilisée pour chiffrer les données. Cependant, le `WEP-104` a une `secret key` de `80-bits`. Regardons le tableau suivant pour voir clairement les différences :

|**Protocole**|**IV**|**Secret Key**|
|---|---|---|
|`WEP-40`/`WEP-64`|24-bit|40-bit|
|`WEP-104`|24-bit|80-bit|

Cependant, comme l'IV en WEP est relativement petit, nous pouvons le forcer par attaque brute (brute force), c'est-à-dire essayer toutes les combinaisons de caractères possibles pour lui, et déterminer la bonne valeur. Ensuite, nous pouvons l'utiliser pour déchiffrer les données dans le paquet. Cela nous permet d'accéder aux données transmises sur le réseau sans fil et de compromettre potentiellement la sécurité du réseau.

#### WPA

`WPA` offre le plus haut niveau de sécurité et n'est pas susceptible aux mêmes types d'attaques que le WEP. De plus, le WPA utilise des méthodes d'authentification plus sûres, telles qu'une [clé pré-partagée](https://en.wikipedia.org/wiki/Pre-shared_key) (`PSK`, Pre-Shared Key) ou un serveur d'authentification 802.1X, qui offrent une meilleure protection contre les accès non autorisés. Bien que les appareils plus anciens puissent ne pas prendre en charge le WPA, il est compatible avec la plupart des appareils et systèmes d'exploitation. Tous les réseaux sans fil, en particulier dans les infrastructures critiques comme les bureaux, devraient généralement implémenter au moins le chiffrement `WPA2` ou même `WPA3`.

---

## Protocoles d'authentification

Le [protocole d'authentification extensible léger](https://en.wikipedia.org/wiki/Lightweight_Extensible_Authentication_Protocol) (`LEAP`, Lightweight Extensible Authentication Protocol) et le [protocole d'authentification extensible protégé](https://en.wikipedia.org/wiki/Protected_Extensible_Authentication_Protocol) (`PEAP`, Protected Extensible Authentication Protocol) sont des protocoles d'authentification utilisés pour sécuriser les réseaux sans fil afin de fournir une méthode sécurisée pour authentifier les appareils sur un réseau sans fil et sont souvent utilisés en conjonction avec WEP ou WPA pour fournir une couche de sécurité supplémentaire.

LEAP et PEAP sont tous deux basés sur le [protocole d'authentification extensible](https://en.wikipedia.org/wiki/Extensible_Authentication_Protocol) (`EAP`, Extensible Authentication Protocol), un cadre d'authentification utilisé dans divers contextes de réseautage. Cependant, une différence clé entre `LEAP` et `PEAP` est la manière dont ils sécurisent le processus d'authentification.

- `LEAP` utilise une `shared key` pour l'authentification, ce qui signifie que la `same key` est utilisée pour le `encryption and authentication`.

Cela peut nous permettre d'accéder assez facilement au réseau si la clé est compromise.

Cependant, `PEAP` utilise une méthode d'authentification plus sécurisée appelée [sécurité de la couche de transport](https://en.wikipedia.org/wiki/Transport_Layer_Security) (`TLS`, Transport Layer Security) en tunnel. Cette méthode établit une connexion sécurisée entre l'appareil et le WAP en utilisant un `digital certificate`, et un tunnel chiffré protège le processus d'authentification. Cela offre une protection plus robuste contre les accès non autorisés et est plus résistant aux attaques.

---

## TACACS+

Dans un réseau sans fil, lorsqu'un point d'accès sans fil (WAP) envoie une demande d'authentification à un serveur [Terminal Access Controller Access-Control System Plus](https://web.archive.org/web/20250423051356/https://www.ciscopress.com/articles/article.asp?p=422947&seqNum=4) (`TACACS+`), il est probable que l'`entire request packet` sera chiffré pour protéger la confidentialité et l'intégrité de la demande.

`TACACS+` est un protocole utilisé pour authentifier et autoriser les utilisateurs accédant à des périphériques réseau, tels que des routeurs et des commutateurs. Lorsqu'un WAP envoie une demande d'authentification à un serveur `TACACS+`, la demande inclut généralement les informations d'identification de l'utilisateur et d'autres informations sur la session.

Le chiffrement de la demande d'authentification aide à garantir que ces informations sensibles ne sont pas visibles pour des tiers non autorisés qui pourraient intercepter la demande. En même temps, elle est transmise sur le réseau. Cela aide également à empêcher la falsification de la demande ou son remplacement par une demande malveillante.

Plusieurs méthodes de chiffrement peuvent être utilisées pour chiffrer la demande d'authentification, telles que `SSL`/`TLS` ou `IPSec`. La méthode de chiffrement spécifique utilisée peut dépendre de la configuration du serveur `TACACS+` et des capacités du WAP.

---

## Attaque de désassociation

Une [attaque de désassociation](https://www.makeuseof.com/what-are-disassociation-attacks/) est un type d'attaque de réseau sans fil `all` qui vise à perturber la communication entre un WAP et ses clients en envoyant des trames de désassociation à un ou plusieurs clients.

Le WAP utilise des trames de désassociation pour déconnecter un client du réseau. Lorsqu'un WAP envoie une trame de désassociation à un client, le client se déconnectera du réseau et devra se reconnecter pour continuer à utiliser le réseau.

Nous pouvons lancer l'attaque depuis l'`within` ou l'`outside` du réseau en fonction de notre emplacement et des mesures de sécurité du réseau. Le but de cette attaque est de perturber la communication entre le WAP et ses clients, provoquant la déconnexion des clients et pouvant causer des désagréments ou des perturbations pour les utilisateurs. Elle peut également être utilisée comme un précurseur à d'autres attaques, telles qu'une attaque de l'homme du milieu (MITM), en forçant les clients à se reconnecter au réseau et en les exposant potentiellement à d'autres attaques.

---

## Renforcement de la sécurité sans fil

Il existe de nombreuses façons de protéger les réseaux sans fil. Cependant, quelques exemples doivent être considérés pour augmenter considérablement la sécurité des réseaux sans fil. Ce sont les suivants, mais sans s'y limiter :

- Désactivation de la diffusion
- Accès protégé Wi-Fi (WiFi Protected Access)
- Filtrage MAC
- Déploiement de l'EAP-TLS

#### Désactivation de la diffusion

La désactivation de la diffusion du SSID est une mesure de sécurité qui peut aider à renforcer un WAP en rendant plus difficile la découverte et la connexion au réseau. Lorsque le SSID est diffusé, il est inclus dans les trames de balise (beacon frames) régulièrement transmises par le WAP pour annoncer la disponibilité du réseau. En désactivant la diffusion du SSID, le WAP ne transmettra pas de trames de balise, et le réseau ne sera pas visible pour les appareils qui ne sont pas déjà connectés au réseau.

#### WPA

Encore une fois, le WPA fournit un chiffrement et une authentification forts pour les communications sans fil, aidant à protéger contre les accès non autorisés au réseau et l'interception de données sensibles. Le WPA comprend deux versions principales :

1. WPA-Personnel
2. WPA-Entreprise

WPA-Personnel (WPA-Personal), conçu pour les réseaux domestiques et de petites entreprises, et WPA-Entreprise (WPA-Enterprise), conçu pour les grandes organisations et qui utilise un serveur d'authentification centralisé (par ex., RADIUS ou TACACS+) pour vérifier l'identité des clients.

#### Filtrage MAC

Le filtrage MAC est une mesure de sécurité qui permet à un WAP d'accepter ou de rejeter des connexions de périphériques spécifiques en fonction de leurs adresses MAC. En configurant le WAP pour n'accepter que les connexions des périphériques avec des adresses MAC approuvées, il est possible d'empêcher les périphériques non autorisés de se connecter au réseau.

#### Déploiement de l'EAP-TLS

L'EAP-TLS est un protocole de sécurité utilisé pour authentifier et chiffrer les communications sans fil. Il utilise des certificats numériques et une infrastructure à clé publique (IGC, PKI) pour vérifier l'identité des clients et établir des connexions sécurisées. Le déploiement de l'EAP-TLS peut aider à renforcer un WAP en fournissant une authentification et un chiffrement forts pour les communications sans fil, ce qui peut protéger contre les accès non autorisés au réseau et l'interception de données sensibles.
---

← [[14 - Protocoles Courants]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[16 - Réseaux Privés Virtuels]] →
