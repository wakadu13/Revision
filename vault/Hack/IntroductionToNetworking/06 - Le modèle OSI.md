---
tags:
  - networking
ordre: 6
---

# Le modèle OSI

---

L'objectif de la définition de la norme `ISO/OSI` était de créer un modèle de référence permettant la communication de différents systèmes techniques via divers appareils et technologies et d'assurer la compatibilité. Le modèle `OSI` utilise `seven` couches différentes, qui sont basées hiérarchiquement les unes sur les autres pour atteindre cet objectif. Ces couches représentent les phases de l'établissement de chaque connexion, par lesquelles transitent les paquets envoyés. De cette manière, la norme a été créée pour tracer visuellement la manière dont une connexion est structurée et établie.

|**Couche**|**Fonction**|
|---|---|
|`7.Application`|Entre autres, cette couche contrôle l'entrée et la sortie des données et fournit les fonctions d'application.|
|`6.Presentation`|La tâche de la couche de présentation est de transférer la présentation des données, qui dépend du système, dans une forme indépendante de l'application.|
|`5.Session`|La couche de session contrôle la connexion logique entre deux systèmes et prévient, par exemple, les ruptures de connexion ou d'autres problèmes.|
|`4.Transport`|La couche 4 est utilisée pour le contrôle de bout en bout des données transférées. La couche de transport peut détecter et éviter les situations de congestion et segmenter les flux de données.|
|`3.Network`|Sur la couche réseau, les connexions sont établies dans les réseaux à commutation de circuits, et les paquets de données sont acheminés dans les réseaux à commutation de paquets. Les données sont transmises sur l'ensemble du réseau, de l'émetteur au récepteur.|
|`2.Data Link`|La tâche centrale de la couche 2 est de permettre des transmissions fiables et sans erreur sur le support respectif. À cette fin, les flux de bits de la couche 1 sont divisés en blocs ou en trames.|
|`1.Physical`|Les techniques de transmission utilisées sont, par exemple, les signaux électriques, les signaux optiques ou les ondes électromagnétiques. Via la couche 1, la transmission s'effectue sur des lignes de transmission filaires ou sans fil.|

---

Les couches `2-4` sont des couches `transport oriented`, et les couches `5-7` sont des couches `application oriented`. Dans chaque couche, des tâches précisément définies sont exécutées, et les interfaces avec les couches voisines sont décrites avec précision. Chaque couche offre ses services à la couche située directement au-dessus d'elle. Pour rendre ces services disponibles, la couche utilise les services de la couche inférieure et exécute les tâches de sa propre couche.

Si deux systèmes communiquent, les sept couches du modèle `OSI` sont parcourues au moins `twice`, car l'émetteur et le récepteur doivent tous deux prendre en compte le modèle en couches. Par conséquent, un grand nombre de tâches différentes doivent être effectuées dans les différentes couches pour garantir la sécurité, la fiabilité et la performance de la communication.

Lorsqu'une application envoie un paquet à l'autre système, le système parcourt les couches présentées ci-dessus de la couche `7` à la couche `1`, et le système récepteur dépaquette le paquet reçu de la couche `1` à la couche `7`.
---

← [[05 - Modèles Réseau]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[07 - Le modèle TCP-IP]] →
