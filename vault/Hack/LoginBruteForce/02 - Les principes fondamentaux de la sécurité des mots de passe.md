---
tags:
  - brute-force
ordre: 2
---

# Les principes fondamentaux de la sécurité des mots de passe

L'efficacité des attaques par force brute (brute-force attacks) dépend de la robustesse des mots de passe qu'elles ciblent. Comprendre les principes fondamentaux de la sécurité des mots de passe est crucial pour apprécier l'importance de pratiques de mot de passe robustes et les défis posés par les attaques par force brute.

## L'importance des mots de passe robustes

Les mots de passe constituent la première ligne de défense pour la protection des informations et des systèmes sensibles. Un mot de passe robuste est une barrière redoutable, rendant l'accès non autorisé par force brute ou d'autres techniques beaucoup plus difficile pour les attaquants. Plus un mot de passe est long et complexe, plus un attaquant doit essayer de combinaisons, ce qui augmente de manière exponentielle le temps et les ressources nécessaires pour une attaque réussie.

## L'anatomie d'un mot de passe robuste

Le `National Institute of Standards and Technology` (`NIST`) fournit des directives pour la création de mots de passe robustes. Ces directives mettent l'accent sur les caractéristiques suivantes :

- `Longueur` : Plus le mot de passe est long, mieux c'est. Visez un minimum de 12 caractères, mais plus long est toujours préférable. Le raisonnement est simple : chaque caractère supplémentaire dans un mot de passe augmente considérablement le nombre de combinaisons possibles. Par exemple, un mot de passe de 6 caractères utilisant uniquement des lettres minuscules a 26^6 (environ 300 millions) de combinaisons possibles. En revanche, un mot de passe de 8 caractères a 26^8 (environ 200 milliards) de combinaisons. Cette augmentation exponentielle des possibilités rend les mots de passe plus longs beaucoup plus résistants aux attaques par force brute.
- `Complexité` : Bien que les conseils traditionnels mettaient l'accent sur l'utilisation d'un mélange de lettres majuscules et minuscules, de chiffres et de symboles pour créer des mots de passe complexes, les directives récentes du NIST se sont orientées vers la longueur du mot de passe et l'utilisation de phrases de passe (passphrases). Cependant, la complexité reste une considération importante, surtout dans le contexte des attaques par force brute. L'inclusion de différents types de caractères élargit l'ensemble des caractères potentiels pour chaque position dans le mot de passe. Par exemple, un mot de passe utilisant uniquement des lettres minuscules a 26 possibilités par caractère, tandis qu'un mot de passe utilisant à la fois des lettres majuscules et minuscules en a 52. Cette complexité accrue peut rendre plus difficile pour les attaquants de prédire ou de deviner les mots de passe. Malgré le changement d'orientation, comprendre le rôle de la complexité peut toujours être précieux pour créer des mots de passe robustes.
- `Unicité` : Ne réutilisez pas les mots de passe sur différents comptes. Chaque compte doit avoir son propre mot de passe unique et robuste. Si un compte est compromis, tous les autres comptes utilisant le même mot de passe sont également en danger. En utilisant des mots de passe uniques pour chaque compte, vous compartimentez les dommages potentiels d'une faille de sécurité.
- `Caractère aléatoire` : Évitez d'utiliser des mots du dictionnaire, des informations personnelles ou des phrases courantes. Plus le mot de passe est aléatoire, plus il est difficile à craquer. Les attaquants utilisent souvent des listes de mots (wordlists) contenant des mots de passe courants et des informations personnelles pour accélérer leurs tentatives de force brute. La création d'un mot de passe aléatoire minimise les chances d'être inclus dans de telles listes de mots.

## Faiblesses courantes des mots de passe

Malgré l'importance des mots de passe robustes, de nombreux utilisateurs s'appuient encore sur des mots de passe faibles et faciles à deviner. Les faiblesses courantes incluent :

- `Mots de passe courts` : Les mots de passe de moins de huit caractères sont particulièrement vulnérables aux attaques par force brute, car le nombre de combinaisons possibles est relativement faible.
- `Mots et phrases courants` : L'utilisation de mots du dictionnaire, de noms ou de phrases courantes comme mots de passe les rend vulnérables aux attaques par dictionnaire (dictionary attacks), où les attaquants essaient une liste prédéfinie de mots de passe courants.
- `Informations personnelles` : L'intégration d'informations personnelles comme les dates de naissance, les noms d'animaux de compagnie ou les adresses dans les mots de passe les rend plus faciles à deviner, surtout si ces informations sont publiquement disponibles sur les réseaux sociaux ou d'autres plateformes en ligne.
- `Réutilisation des mots de passe` : L'utilisation du même mot de passe sur plusieurs comptes est risquée. Si un compte est compromis, tous les autres comptes utilisant le même mot de passe sont également en danger.
- `Motifs prévisibles` : L'utilisation de motifs comme "azerty" ou "123456" ou de substitutions simples comme "m0tdep@sse" rend les mots de passe faciles à deviner, car ces motifs sont bien connus des attaquants.

## Politiques de mot de passe

Les organisations mettent souvent en œuvre des politiques de mot de passe pour imposer l'utilisation de mots de passe robustes. Ces politiques incluent généralement des exigences pour :

- `Longueur minimale` : Le nombre minimum de caractères qu'un mot de passe doit avoir.
- `Complexité` : Les types de caractères qui doivent être inclus dans un mot de passe (par ex., majuscules, minuscules, chiffres, symboles).
- `Expiration du mot de passe` : La fréquence à laquelle les mots de passe doivent être changés.
- `Historique des mots de passe` : Le nombre de mots de passe précédents qui ne peuvent pas être réutilisés.

Bien que les politiques de mot de passe puissent aider à améliorer la sécurité des mots de passe, elles peuvent également entraîner la frustration des utilisateurs et l'adoption de mauvaises pratiques, comme noter les mots de passe ou utiliser de légères variantes du même mot de passe. Lors de la conception des politiques de mot de passe, il est important d'équilibrer la sécurité et l'utilisabilité.

## Les dangers des identifiants par défaut

Un aspect critique de la sécurité des mots de passe souvent négligé est le danger posé par les `mots de passe par défaut`. Ces mots de passe prédéfinis sont fournis avec divers appareils, logiciels ou services en ligne. Ils sont souvent simples et faciles à deviner, ce qui en fait une cible de choix pour les attaquants.

Les mots de passe par défaut augmentent considérablement le taux de réussite des attaques par force brute. Les attaquants peuvent exploiter des listes de mots de passe par défaut courants, réduisant considérablement l'espace de recherche et accélérant le processus de craquage. Dans certains cas, les attaquants n'ont même pas besoin de lancer une attaque par force brute ; ils peuvent essayer quelques mots de passe par défaut courants et obtenir un accès avec un minimum d'effort.

La prévalence des mots de passe par défaut en fait une proie facile pour les attaquants. Ils fournissent un point d'entrée simple dans les systèmes et les réseaux, pouvant potentiellement conduire à des fuites de données, des accès non autorisés et d'autres activités malveillantes.

|Appareil/Fabricant|Nom d'utilisateur par défaut|Mot de passe par défaut|Type d'appareil|
|---|---|---|---|
|Routeur Linksys|admin|admin|Routeur sans fil|
|Routeur D-Link|admin|admin|Routeur sans fil|
|Routeur Netgear|admin|password|Routeur sans fil|
|Routeur TP-Link|admin|admin|Routeur sans fil|
|Routeur Cisco|cisco|cisco|Routeur réseau|
|Routeur Asus|admin|admin|Routeur sans fil|
|Routeur Belkin|admin|password|Routeur sans fil|
|Routeur Zyxel|admin|1234|Routeur sans fil|
|Samsung SmartCam|admin|4321|Caméra IP|
|Hikvision DVR|admin|12345|Enregistreur vidéo numérique (DVR)|
|Caméra IP Axis|root|pass|Caméra IP|
|Ubiquiti UniFi AP|ubnt|ubnt|Point d'accès sans fil|
|Imprimante Canon|admin|admin|Imprimante réseau|
|Thermostat Honeywell|admin|1234|Thermostat intelligent|
|Panasonic DVR|admin|12345|Enregistreur vidéo numérique (DVR)|

Ce ne sont là que quelques exemples de mots de passe par défaut bien connus. Les attaquants compilent souvent des listes exhaustives de tels mots de passe et les utilisent dans des attaques automatisées.

Outre les mots de passe par défaut, les noms d'utilisateur par défaut constituent une autre préoccupation majeure en matière de sécurité. Les fabricants livrent souvent des appareils avec des noms d'utilisateur prédéfinis, tels que `admin`, `root` ou `user`. Vous avez peut-être remarqué dans le tableau ci-dessus combien d'entre eux utilisent des noms d'utilisateur courants. Ces noms d'utilisateur sont largement connus et souvent publiés dans la documentation ou facilement accessibles en ligne. SecLists maintient une liste de noms d'utilisateur courants à l'adresse [top-usernames-shortlist.txt](https://github.com/danielmiessler/SecLists/blob/master/Usernames/top-usernames-shortlist.txt)

Les noms d'utilisateur par défaut représentent une vulnérabilité importante car ils donnent aux attaquants un point de départ prévisible. Dans de nombreuses attaques par force brute, connaître le nom d'utilisateur est la moitié du travail. Une fois le nom d'utilisateur établi, l'attaquant n'a plus qu'à craquer le mot de passe, et si l'appareil utilise toujours un mot de passe par défaut, l'attaque peut être menée à bien avec un minimum d'effort.

Même lorsque les mots de passe par défaut sont modifiés, le fait de conserver le nom d'utilisateur par défaut laisse les systèmes vulnérables aux attaques. Cela réduit considérablement la surface d'attaque, car le pirate peut sauter le processus de devinette des noms d'utilisateur et se concentrer uniquement sur le mot de passe.

### Attaques par force brute et sécurité des mots de passe

Dans un scénario de force brute, la robustesse des mots de passe ciblés devient le principal obstacle de l'attaquant. Un mot de passe faible s'apparente à une serrure fragile sur une porte – facile à crocheter avec un minimum d'effort. À l'inverse, un mot de passe robuste agit comme un coffre-fort, exigeant beaucoup plus de temps et de ressources pour être forcé.

Pour un pentester, cela se traduit par une compréhension plus approfondie de la posture de sécurité de la cible :

- `Évaluation de la vulnérabilité du système :` Les politiques de mot de passe, ou leur absence, et la probabilité que les utilisateurs emploient des mots de passe faibles renseignent directement sur le succès potentiel d'une attaque par force brute.
- `Sélection stratégique des outils :` La complexité des mots de passe dicte les outils et les méthodologies qu'un pentester déploiera. Une simple attaque par dictionnaire pourrait suffire pour des mots de passe faibles, tandis qu'une approche hybride plus sophistiquée pourrait être nécessaire pour craquer les plus robustes.
- `Allocation des ressources :` Le temps estimé et la puissance de calcul nécessaires pour une attaque par force brute sont intrinsèquement liés à la complexité des mots de passe. Cette connaissance est essentielle pour une planification et une gestion des ressources efficaces.
- `Exploitation des points faibles :` Les mots de passe par défaut sont souvent le talon d'Achille d'un système. La capacité d'un pentester à identifier et à exploiter ces identifiants faciles à deviner peut fournir un point d'entrée rapide dans le réseau cible.

En substance, une compréhension approfondie de la sécurité des mots de passe est une feuille de route pour un pentester naviguant dans les complexités d'une attaque par force brute. Elle révèle les points faibles potentiels, éclaire les choix stratégiques et prédit l'effort requis pour une intrusion réussie. Cette connaissance, cependant, est une arme à double tranchant. Elle souligne également l'importance cruciale de pratiques de mot de passe robustes pour toute organisation cherchant à se défendre contre de telles attaques, mettant en évidence le rôle central de chaque utilisateur dans la protection des informations sensibles.
---

← [[01 - Introduction]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[03 - Attaques par force brute]] →
