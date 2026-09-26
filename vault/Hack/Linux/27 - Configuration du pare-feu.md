---
tags:
  - linux
ordre: 27
---

# Configuration du pare-feu

L'objectif principal des pare-feux est de fournir un mécanisme de sécurité pour contrôler et surveiller le trafic réseau entre différents segments de réseau, tels que les réseaux internes et externes ou différentes zones de réseau. Les pare-feux jouent un rôle crucial dans la protection des réseaux informatiques contre les accès non autorisés, le trafic malveillant et d'autres menaces de sécurité. Linux, étant un système d'exploitation populaire utilisé sur les serveurs et autres périphériques réseau, fournit des fonctionnalités de pare-feu intégrées qui peuvent être utilisées pour contrôler le trafic réseau. En d'autres termes, ils peuvent filtrer le trafic entrant et sortant en fonction de règles prédéfinies, de protocoles, de ports et d'autres critères pour empêcher les accès non autorisés et atténuer les menaces de sécurité. L'objectif spécifique d'une implémentation de pare-feu peut varier en fonction des besoins spécifiques de l'organisation, comme assurer la confidentialité, l'intégrité et la disponibilité des ressources réseau.

Un exemple de l'histoire des pare-feux Linux est le développement de l'outil iptables, qui a remplacé les anciens outils ipchains et ipfwadm. L'utilitaire iptables a été introduit pour la première fois dans le noyau Linux 2.4 en 2000 et a fourni un mécanisme flexible et efficace pour filtrer le trafic réseau. iptables est devenu la solution de pare-feu standard de facto pour les systèmes Linux, et il a été largement adopté par de nombreuses organisations et utilisateurs.

L'utilitaire iptables offrait une interface en ligne de commande simple mais puissante pour configurer les règles de pare-feu, qui pouvait être utilisée pour filtrer le trafic en fonction de divers critères tels que les adresses IP, les ports, les protocoles, etc. iptables a été conçu pour être hautement personnalisable et pouvait être utilisé pour créer des ensembles de règles de pare-feu complexes capables de protéger contre diverses menaces de sécurité telles que les attaques par déni de service (DoS), les scans de ports et les tentatives d'intrusion réseau.

Sous Linux, la fonctionnalité de pare-feu est généralement implémentée à l'aide du framework Netfilter, qui fait partie intégrante du noyau. Netfilter fournit un ensemble de points d'accroche (hooks) qui peuvent être utilisés pour intercepter et modifier le trafic réseau lorsqu'il traverse le système. L'utilitaire iptables est couramment utilisé pour configurer les règles de pare-feu sur les systèmes Linux.

---

## Iptables

L'utilitaire iptables fournit un ensemble flexible de règles pour filtrer le trafic réseau en fonction de divers critères tels que les adresses IP source et de destination, les numéros de port, les protocoles, etc. Il existe également d'autres solutions comme nftables, ufw et firewalld. `Nftables` offre une syntaxe plus moderne et des performances améliorées par rapport à iptables. Cependant, la syntaxe des règles nftables n'est pas compatible avec iptables, donc la migration vers nftables nécessite un certain effort. `UFW` signifie « Uncomplicated Firewall » (Pare-feu simple) et fournit une interface simple et conviviale pour configurer les règles de pare-feu. UFW est construit sur le framework iptables, tout comme nftables, et offre un moyen plus simple de gérer les règles de pare-feu. Enfin, FirewallD fournit une solution de pare-feu dynamique et flexible qui peut être utilisée pour gérer des configurations de pare-feu complexes. Il prend en charge un ensemble riche de règles pour filtrer le trafic réseau et peut être utilisé pour créer des zones et des services de pare-feu personnalisés. Il se compose de plusieurs éléments qui fonctionnent ensemble pour fournir une solution de pare-feu flexible et puissante. Les principaux composants d'iptables sont :

|**Composant**|**Description**|
|---|---|
|`Tables`|Les tables sont utilisées pour organiser et catégoriser les règles de pare-feu.|
|`Chains`|Les chaînes sont utilisées pour regrouper un ensemble de règles de pare-feu appliquées à un type spécifique de trafic réseau.|
|`Rules`|Les règles définissent les critères de filtrage du trafic réseau et les actions à entreprendre pour les paquets qui correspondent à ces critères.|
|`Matches`|Les correspondances (matches) sont utilisées pour faire correspondre des critères spécifiques pour le filtrage du trafic réseau, tels que les adresses IP source ou de destination, les ports, les protocoles, etc.|
|`Targets`|Les cibles (targets) spécifient l'action à entreprendre pour les paquets qui correspondent à une règle spécifique. Par exemple, les cibles peuvent être utilisées pour accepter, abandonner (drop) ou rejeter (reject) des paquets, ou pour les modifier d'une autre manière.|

### Tables

Lorsque l'on travaille avec des pare-feux sur des systèmes Linux, il est important de comprendre comment les tables fonctionnent dans iptables. Dans iptables, les tables sont utilisées pour catégoriser et organiser les règles de pare-feu en fonction du type de trafic qu'elles sont conçues pour gérer. Ces tables sont utilisées pour organiser et catégoriser les règles de pare-feu. Chaque table est responsable de l'exécution d'un ensemble de tâches spécifiques.

|**Nom de la table**|**Description**|**Chaînes intégrées**|
|---|---|---|
|`filter`|Utilisée pour filtrer le trafic réseau en fonction des adresses IP, des ports et des protocoles.|INPUT, OUTPUT, FORWARD|
|`nat`|Utilisée pour modifier les adresses IP source ou de destination des paquets réseau.|PREROUTING, POSTROUTING|
|`mangle`|Utilisée pour modifier les champs d'en-tête des paquets réseau.|PREROUTING, OUTPUT, INPUT, FORWARD, POSTROUTING|

En plus des tables intégrées, iptables fournit une quatrième table appelée la table raw, qui est utilisée pour configurer des options spéciales de traitement des paquets. La table raw contient deux chaînes intégrées : PREROUTING et OUTPUT.

### Chaînes

Dans iptables, les chaînes organisent les règles qui définissent comment le trafic réseau doit être filtré ou modifié. Il existe deux types de chaînes dans iptables :

- Chaînes intégrées
- Chaînes définies par l'utilisateur

Les chaînes intégrées sont prédéfinies et automatiquement créées lors de la création d'une table. Chaque table dispose d'un ensemble différent de chaînes intégrées. Par exemple, la table filter a trois chaînes intégrées :

- INPUT
- OUTPUT
- FORWARD

Ces chaînes sont utilisées pour filtrer le trafic réseau entrant et sortant, ainsi que le trafic qui est transféré entre différentes interfaces réseau. La table nat a deux chaînes intégrées :

- PREROUTING
- POSTROUTING

La chaîne PREROUTING est utilisée pour modifier l'adresse IP de destination des paquets entrants avant que la table de routage ne les traite. La chaîne POSTROUTING est utilisée pour modifier l'adresse IP source des paquets sortants après que la table de routage les a traités. La table mangle a cinq chaînes intégrées :

- PREROUTING
- OUTPUT
- INPUT
- FORWARD
- POSTROUTING

Ces chaînes sont utilisées pour modifier les champs d'en-tête des paquets entrants et sortants et des paquets traités par les chaînes correspondantes.

Les `chaînes définies par l'utilisateur` peuvent simplifier la gestion des règles en regroupant les règles de pare-feu selon des critères spécifiques, tels que l'adresse IP source, le port de destination ou le protocole. Elles peuvent être ajoutées à n'importe laquelle des trois tables principales. Par exemple, si une organisation a plusieurs serveurs web qui nécessitent tous des règles de pare-feu similaires, les règles pour chaque serveur pourraient être regroupées dans une chaîne définie par l'utilisateur. Un autre exemple serait une chaîne définie par l'utilisateur qui pourrait filtrer le trafic destiné à un port spécifique, comme le port 80 (HTTP). L'utilisateur pourrait alors ajouter des règles à cette chaîne qui filtrent spécifiquement le trafic destiné au port 80.

### Règles et cibles

Les règles iptables sont utilisées pour définir les critères de filtrage du trafic réseau et les actions à entreprendre pour les paquets qui correspondent à ces critères. Les règles sont ajoutées aux chaînes à l'aide de l'option `-A` suivie du nom de la chaîne, et elles peuvent être modifiées ou supprimées à l'aide de diverses autres options.

Chaque règle se compose d'un ensemble de critères ou de correspondances (matches) et d'une cible (target) spécifiant l'action à entreprendre pour les paquets qui correspondent aux critères. Les critères ou correspondances font correspondre des champs spécifiques dans l'en-tête IP, tels que l'adresse IP source ou de destination, le protocole, le port source, le port de destination, etc. La cible spécifie l'action pour les paquets qui correspondent aux critères. Elles spécifient l'action à entreprendre pour les paquets qui correspondent à une règle spécifique. Par exemple, les cibles peuvent accepter, abandonner, rejeter ou modifier les paquets. Voici quelques-unes des cibles courantes utilisées dans les règles iptables :

|**Nom de la cible**|**Description**|
|---|---|
|`ACCEPT`|Autorise le paquet à traverser le pare-feu et à poursuivre vers sa destination|
|`DROP`|Abandonne le paquet, l'empêchant de fait de traverser le pare-feu|
|`REJECT`|Rejette le paquet et envoie un message d'erreur à l'adresse source, l'informant que le paquet a été bloqué|
|`LOG`|Journalise les informations du paquet dans le journal système|
|`SNAT`|Modifie l'adresse IP source du paquet, généralement utilisé pour la traduction d'adresses réseau (NAT) afin de traduire des adresses IP privées en adresses IP publiques|
|`DNAT`|Modifie l'adresse IP de destination du paquet, généralement utilisé pour la NAT afin de transférer le trafic d'une adresse IP à une autre|
|`MASQUERADE`|Similaire à SNAT mais utilisé lorsque l'adresse IP source n'est pas fixe, comme dans un scénario d'adresse IP dynamique|
|`REDIRECT`|Redirige les paquets vers un autre port ou une autre adresse IP|
|`MARK`|Ajoute ou modifie la valeur de marque Netfilter du paquet, qui peut être utilisée pour un routage avancé ou à d'autres fins|

Illustrons une règle et considérons que nous voulons ajouter une nouvelle entrée à la chaîne INPUT qui autorise l'acceptation du trafic TCP entrant sur le port 22 (SSH). La commande pour cela ressemblerait à ce qui suit :

```bash
Hiterof13@htb[/htb]$ sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
```

### Correspondances (Matches)

Les `correspondances (Matches)` sont utilisées pour spécifier les critères qui déterminent si une règle de pare-feu doit être appliquée à un paquet ou à une connexion particulière. Les correspondances sont utilisées pour faire correspondre des caractéristiques spécifiques du trafic réseau, telles que l'adresse IP source ou de destination, le protocole, le numéro de port, etc.

|**Nom de la correspondance**|**Description**|
|---|---|
|`-p` ou `--protocol`|Spécifie le protocole à faire correspondre (p. ex. tcp, udp, icmp)|
|`--dport`|Spécifie le port de destination à faire correspondre|
|`--sport`|Spécifie le port source à faire correspondre|
|`-s` ou `--source`|Spécifie l'adresse IP source à faire correspondre|
|`-d` ou `--destination`|Spécifie l'adresse IP de destination à faire correspondre|
|`-m state`|Correspond à l'état d'une connexion (p. ex. NEW, ESTABLISHED, RELATED)|
|`-m multiport`|Correspond à plusieurs ports ou plages de ports|
|`-m tcp`|Correspond aux paquets TCP et inclut des options supplémentaires spécifiques à TCP|
|`-m udp`|Correspond aux paquets UDP et inclut des options supplémentaires spécifiques à UDP|
|`-m string`|Correspond aux paquets qui contiennent une chaîne de caractères spécifique|
|`-m limit`|Correspond aux paquets à une limite de débit spécifiée|
|`-m conntrack`|Correspond aux paquets en fonction de leurs informations de suivi de connexion|
|`-m mark`|Correspond aux paquets en fonction de leur valeur de marque Netfilter|
|`-m mac`|Correspond aux paquets en fonction de leur adresse MAC|
|`-m iprange`|Correspond aux paquets en fonction d'une plage d'adresses IP|

En général, les correspondances sont spécifiées à l'aide de l'option '-m' dans iptables. Par exemple, la commande suivante ajoute une règle à la chaîne 'INPUT' dans la table 'filter' qui correspond au trafic TCP entrant sur le port 80 :

```bash
Hiterof13@htb[/htb]$ sudo iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
```

Cette règle d'exemple correspond au trafic TCP entrant (`-p tcp`) sur le port 80 (`--dport 80`) et saute vers la cible d'acceptation (`-j ACCEPT`) si la correspondance est réussie.

|||
|---|---|
|1.|Lancez un serveur web sur le port TCP/8080 de votre cible et utilisez iptables pour bloquer le trafic entrant sur ce port.|
|2.|Modifiez les règles iptables pour autoriser le trafic entrant sur le port TCP/8080.|
|3.|Bloquez le trafic provenant d'une adresse IP spécifique.|
|4.|Autorisez le trafic provenant d'une adresse IP spécifique.|
|5.|Bloquez le trafic en fonction du protocole.|
|6.|Autorisez le trafic en fonction du protocole.|
|7.|Créez une nouvelle chaîne.|
|8.|Transférez le trafic vers une chaîne spécifique.|
|9.|Supprimez une règle spécifique.|
|10.|Listez toutes les règles existantes.|

---

← [[26 - Sécurité Linux]] | [[00 - Sommaire Linux|Sommaire]] | [[28 - Journaux système]] →
