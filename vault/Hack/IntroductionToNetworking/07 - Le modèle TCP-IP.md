---
tags:
  - networking
ordre: 7
---

# Le modèle TCP/IP

---

Le modèle `TCP/IP` est également un modèle de référence en couches, souvent désigné sous le nom de suite de protocoles Internet (Internet Protocol Suite). Le terme `TCP/IP` correspond aux deux protocoles que sont le Protocole de Contrôle de Transmission (Transmission Control Protocol) (`TCP`) et le Protocole Internet (Internet Protocol) (`IP`). L'`IP` se situe dans la couche réseau (couche 3) (network layer) et le `TCP` se situe dans la couche transport (couche 4) (transport layer) du modèle en couches `OSI`.

|**Couche**|**Fonction**|
|---|---|
|`4.Application`|La Couche Application permet aux applications d'accéder aux services des autres couches et définit les protocoles que les applications utilisent pour échanger des données.|
|`3.Transport`|La Couche Transport est responsable de la fourniture de services de session (`TCP`) et de datagramme (`UDP`) pour la Couche Application.|
|`2.Internet`|La Couche Internet est responsable des fonctions d'adressage des hôtes, d'empaquetage et de routage.|
|`1.Liaison`|La Couche Liaison est responsable du placement des paquets `TCP/IP` sur le support réseau et de la réception des paquets correspondants depuis le support réseau. `TCP/IP` est conçu pour fonctionner indépendamment de la méthode d'accès au réseau, du format de la trame et du support.|

---

Avec `TCP/IP`, chaque application peut transférer et échanger des données sur n'importe quel réseau, et ce, peu importe où se trouve le destinataire. L'`IP` garantit que le paquet de données (data packet) atteint sa destination, et le `TCP` contrôle le transfert de données et assure la connexion entre le flux de données (data stream) et l'application. La principale différence entre `TCP/IP` et `OSI` est le nombre de couches, dont certaines ont été fusionnées.

![Comparaison des modèles OSI et TCP/IP : OSI a 7 couches, dont Application, Présentation, Session, Transport, Réseau, Liaison de Données et Physique. TCP/IP a 4 couches : Application, Transport, Internet et Liaison.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/redesigned/net_models4.png)

Les tâches les plus importantes de `TCP/IP` sont :

|**Tâche**|**Protocole**|**Description**|
|---|---|---|
|`Adressage Logique (Logical Addressing)`|`IP`|En raison du grand nombre d'hôtes sur différents réseaux, il est nécessaire de structurer la topologie du réseau et l'adressage logique. Au sein de `TCP/IP`, l'`IP` prend en charge l'adressage logique des réseaux et des nœuds. Les paquets de données n'atteignent que le réseau auquel ils sont destinés. Les méthodes pour y parvenir sont les classes de réseau (network classes), le sous-réseautage (subnetting) et le `CIDR`.|
|`Routage (Routing)`|`IP`|Pour chaque paquet de données, le nœud suivant est déterminé dans chaque nœud sur le chemin de l'expéditeur au destinataire. De cette manière, un paquet de données est acheminé vers son destinataire, même si son emplacement est inconnu de l'expéditeur.|
|`Contrôle d'Erreur et de Flux (Error & Control Flow)`|`TCP`|L'expéditeur et le destinataire sont fréquemment en contact l'un avec l'autre via une connexion virtuelle. Par conséquent, des messages de contrôle sont envoyés en continu pour vérifier si la connexion est toujours établie.|
|`Support Applicatif (Application Support)`|`TCP`|Les ports `TCP` et `UDP` forment une abstraction logicielle pour distinguer les applications spécifiques et leurs liens de communication.|
|`Résolution de Noms (Name Resolution)`|`DNS`|Le `DNS` assure la résolution de noms par le biais des Noms de Domaine Pleinement Qualifiés (Fully Qualified Domain Names) (`FQDN`) en adresses `IP`, ce qui nous permet d'atteindre l'hôte souhaité avec le nom spécifié sur Internet.|
---

← [[06 - Le modèle OSI]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[08 - Couche Réseau]] →
