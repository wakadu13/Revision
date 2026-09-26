---
tags:
  - networking
ordre: 20
---

# Connexions TCP/UDP

---

Le [protocole de contrôle de transmission](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) (`TCP`) et le [protocole de datagramme utilisateur](https://en.wikipedia.org/wiki/User_Datagram_Protocol) (`UDP`) sont tous deux des protocoles utilisés pour la transmission d'informations et de données sur Internet. Généralement, les connexions TCP transmettent des données importantes, telles que des pages web et des e-mails. À l'inverse, les connexions UDP transmettent des données en temps réel, comme la vidéo en streaming ou les jeux en ligne.

Le `TCP` est un protocole orienté connexion qui garantit que toutes les données envoyées d'un ordinateur à un autre sont bien reçues. C'est comme une conversation téléphonique où les deux interlocuteurs restent connectés jusqu'à la fin de l'appel. Si une erreur se produit lors de l'envoi des données, le récepteur renvoie un message pour que l'expéditeur puisse renvoyer les données manquantes. Cela rend le `TCP` fiable et plus lent que l'UDP, car la transmission et la récupération des erreurs demandent plus de temps.

L'`UDP`, en revanche, est un protocole sans connexion. Il est utilisé lorsque la vitesse est plus importante que la fiabilité, comme pour le streaming vidéo ou les jeux en ligne. Avec l'`UDP`, il n'y a aucune vérification que les données reçues sont complètes et sans erreur. Si une erreur se produit lors de l'envoi des données, le récepteur ne recevra pas ces données manquantes, et aucun message ne sera renvoyé pour demander leur réexpédition. Certaines données peuvent être perdues avec l'`UDP`, mais la transmission globale est plus rapide.

---

## Paquet IP

Un paquet [protocole Internet](https://en.wikipedia.org/wiki/Internet_Protocol) (`IP`) est la zone de données utilisée par la couche réseau du modèle [d'interconnexion de systèmes ouverts](https://en.wikipedia.org/wiki/OSI_model) (`OSI`) pour transmettre des données d'un ordinateur à un autre. Il se compose d'un en-tête et de la charge utile (payload), qui contient les données utiles réelles.

On peut aussi voir le paquet IP comme une lettre envoyée dans une enveloppe. L'enveloppe contient l'en-tête, qui inclut des informations sur l'expéditeur et le destinataire, ainsi que des instructions pour l'acheminement de la lettre, c'est-à-dire par quels bureaux de poste la lettre doit passer. La lettre elle-même est la charge utile, les données utiles réelles.

#### En-tête IP

L'en-tête d'un paquet IP contient plusieurs champs qui renferment des informations importantes.

|**Champ**|**Description**|
|---|---|
|`Version`|Indique quelle version du protocole IP est utilisée|
|`Internet Header Length`|Indique la taille de l'en-tête en mots de 32 bits|
|`Class of Service`|Signifie l'importance de la transmission des données|
|`Total length`|Spécifie la longueur totale du paquet en octets|
|`Identification (ID)`|Sert à identifier les fragments du paquet lorsqu'il est fragmenté en plus petites parties|
|`Flags`|Utilisés pour indiquer la fragmentation|
|`Fragment Offset`|Indique où le fragment actuel se place dans le paquet|
|`Time to Live`|Spécifie combien de temps le paquet peut rester sur le réseau|
|`Protocol`|Spécifie quel protocole est utilisé pour transmettre les données, comme TCP ou UDP|
|`Checksum`|Sert à détecter les erreurs dans l'en-tête|
|`Source/Destination`|Indiquent d'où le paquet a été envoyé et où il est envoyé|
|`Options`|Contiennent des informations optionnelles pour le routage|
|`Padding`|Complète le paquet pour atteindre une longueur de mot complète|

Il est possible de voir un ordinateur avec plusieurs adresses IP sur différents réseaux. Ici, nous devons prêter attention au champ `IP ID`. Il est utilisé pour identifier les fragments d'un paquet IP lorsqu'il est fragmenté en plus petites parties. C'est un champ de `16 bits` avec un numéro unique allant de `0` à `65535`.

Si un ordinateur a plusieurs adresses IP, le champ `IP ID` sera différent pour chaque paquet envoyé depuis l'ordinateur, mais très similaire. Dans TCPdump, le trafic réseau pourrait ressembler à ceci :

#### Écoute du réseau (Network Sniffing)

```bash
IP 10.129.1.100.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1337
IP 10.129.1.100.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1338
IP 10.129.1.100.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1339
IP 10.129.2.200.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1340
IP 10.129.2.200.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1341
IP 10.129.2.200.5060 > 10.129.1.1.5060: SIP, length: 1329, id 1342
```

La sortie montre que deux adresses IP différentes envoient des paquets à l'adresse IP 10.129.1.1. Cependant, grâce à l'`IP ID`, nous pouvons voir que les paquets sont continus. Cela indique fortement que les deux adresses IP appartiennent au même hôte sur le réseau.

#### Champ Record-Route de l'IP

Le champ `Record-Route` dans l'en-tête IP enregistre également la route vers un appareil de destination. Lorsque l'appareil de destination renvoie le paquet `ICMP Echo Reply`, les adresses IP de tous les appareils par lesquels le paquet est passé sont listées dans le champ `Record-Route` de l'en-tête IP. Cela se produit lorsque nous utilisons la commande suivante, par exemple :

```bash
Hiterof13@htb[/htb]$ ping -c 1 -R 10.129.143.158

PING 10.129.143.158 (10.129.143.158) 56(124) bytes of data.
64 bytes from 10.129.143.158: icmp_seq=1 ttl=63 time=11.7 ms
RR:     10.10.14.38
        10.129.0.1
        10.129.143.158
        10.129.143.158
        10.10.14.1
        10.10.14.38

--- 10.129.143.158 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 11.688/11.688/11.688/0.000 ms
```

La sortie indique qu'une requête `ping` a été envoyée et qu'une réponse a été reçue de l'appareil de destination. Elle montre également le champ `Record-Route` dans l'en-tête IP du paquet `ICMP Echo Request`. Le champ Record-Route contient les adresses IP de tous les appareils par lesquels le paquet `ICMP Echo Request` est passé en route vers l'appareil de destination. Dans ce cas, le champ `Record-Route` contient les adresses IP :

||||
|---|---|---|
|10.10.14.38|10.129.0.1|10.129.143.158|
|10.129.143.158|10.10.14.1|10.10.14.38|

L'outil `traceroute` peut également être utilisé pour tracer plus précisément la route vers une destination, en utilisant la méthode d'expiration TCP pour déterminer quand la route a été entièrement tracée.

1. Nous envoyons un paquet TCP SYN à l'appareil de destination avec un TTL de 1 dans l'en-tête IP.  
    Lorsque le paquet TCP SYN avec un TTL supérieur à 1 atteint un routeur, la valeur du TTL est décrémentée de 1, et le paquet est transmis à l'appareil suivant. Si le paquet TCP SYN avec un TTL de 1 atteint un routeur, le paquet est abandonné (dropped), et le routeur nous renvoie un paquet ICMP Time-Exceeded.
2. Nous recevons le paquet ICMP Time-Exceeded et notons l'adresse IP du routeur qui a envoyé le paquet.
3. Ensuite, nous envoyons un autre paquet TCP SYN à la destination, en augmentant le TTL de 1.

Le processus se répète jusqu'à ce que le paquet TCP SYN atteigne l'hôte de destination et reçoive une réponse `TCP SYN/ACK` ou `TCP RST` de la cible. Une fois que nous recevons une réponse de l'appareil de destination, nous savons que nous avons tracé la route jusqu'à la destination et le processus traceroute se termine.

#### Charge utile IP

La charge utile (payload), également appelée `IP Data`, correspond aux données utiles réelles du paquet. Elle contient les données de divers protocoles, tels que TCP ou UDP, qui sont transmises, tout comme le contenu de la lettre dans l'enveloppe.

---

## TCP

Les paquets TCP, également appelés `segments`, sont divisés en plusieurs sections : les en-têtes et les charges utiles. Les segments TCP sont encapsulés dans le paquet IP envoyé.

L'en-tête contient plusieurs champs qui renferment des informations importantes. Le port source indique l'ordinateur depuis lequel le paquet a été envoyé. Le port de destination indique à quel ordinateur le paquet est envoyé. Le numéro de séquence indique l'ordre dans lequel les données ont été envoyées. Le numéro d'accusé de réception est utilisé pour confirmer que toutes les données ont été reçues avec succès. Les drapeaux de contrôle (control flags) indiquent si le paquet marque la fin d'un message, s'il s'agit d'un accusé de réception de données, ou s'il contient une demande de répétition de données. La taille de la fenêtre (window size) indique la quantité de données que le récepteur peut recevoir. La somme de contrôle (checksum) est utilisée pour détecter des erreurs dans l'en-tête et la charge utile. Le pointeur urgent (Urgent Pointer) alerte le récepteur que des données importantes se trouvent dans la charge utile.

La charge utile correspond aux données utiles réelles du paquet et contient les données qui sont transmises, tout comme le contenu d'une conversation entre deux personnes.

---

## UDP

UDP transfère des `datagrammes` (de petits paquets de données) entre deux hôtes. C'est un protocole sans connexion, ce qui signifie qu'il n'a `pas` besoin d'établir une connexion entre l'expéditeur et le récepteur avant d'envoyer des données. Au lieu de cela, les données sont envoyées directement à l'hôte cible sans aucune connexion préalable.

Lorsque `traceroute` est utilisé avec UDP, nous recevons un message `Destination Unreachable` et `Port Unreachable` lorsque le datagramme UDP atteint l'appareil cible. Généralement, les paquets UDP sont envoyés en utilisant `traceroute` sur les hôtes Unix.

---

## Usurpation à l'aveugle (Blind Spoofing)

L'`usurpation à l'aveugle` (Blind spoofing) est une méthode d'attaque par manipulation de données dans laquelle un attaquant envoie de fausses informations sur un réseau sans voir les réponses réelles renvoyées par les appareils cibles. Elle consiste à manipuler le champ de l'en-tête IP pour indiquer de fausses adresses source et de destination. Par exemple, nous envoyons un paquet TCP à l'hôte cible avec de faux numéros de port source et de destination et un faux `numéro de séquence initial` (`ISN`). L'`ISN` est un champ de l'en-tête TCP utilisé pour spécifier le numéro de séquence du premier paquet TCP d'une connexion. L'ISN est défini par l'expéditeur d'un paquet TCP et envoyé au récepteur dans l'en-tête TCP du premier paquet. Cela peut amener l'hôte cible à établir une connexion avec nous sans que nous ayons à recevoir les paquets de retour.

Cette attaque est couramment utilisée pour perturber l'intégrité des connexions réseau ou pour interrompre les connexions entre les appareils du réseau. Elle peut également être utilisée pour surveiller le trafic réseau ou pour intercepter des informations envoyées par les appareils du réseau.
---

← [[19 - Protocoles d'authentification]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[21 - Cryptographie]] →
