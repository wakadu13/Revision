---
tags:
  - networking
ordre: 17
---

# Informations Spécifiques au Fournisseur

---

[Cisco IOS](https://www.cisco.com/c/en/us/products/ios-nx-os-software/ios-technologies/index.html) est le système d'exploitation des équipements réseau Cisco tels que les routeurs et les commutateurs. Il fournit les fonctionnalités et les services nécessaires pour gérer et exploiter les équipements réseau. Ce système d'exploitation existe en différentes versions et éditions qui varient en termes de fonctionnalités, de support et de performance. Il offre plusieurs fonctionnalités requises pour le fonctionnement des réseaux modernes, telles que, mais sans s'y limiter :

- Le support de l'IPv6
- La Qualité de Service (QoS)
- Des fonctionnalités de sécurité telles que le chiffrement et l'authentification
- Des fonctionnalités de virtualisation telles que le Virtual Private LAN Service (VPLS)
- Le Virtual Routing and Forwarding (VRF)

Cisco IOS peut être géré de plusieurs manières, en fonction de l'équipement réseau et du matériel utilisé. La méthode la plus couramment utilisée est l'interface de ligne de commande (`CLI`), qui peut également être gérée via l'interface utilisateur graphique (`GUI`). De plus, il prend en charge divers protocoles et services réseau requis pour les opérations réseau. Ceux-ci incluent :

|**Type de Protocole**|**Description**|
|---|---|
|`Protocoles de routage`|Tels que [OSPF](https://en.wikipedia.org/wiki/Open_Shortest_Path_First) et [BGP](https://en.wikipedia.org/wiki/Border_Gateway_Protocol) sont utilisés pour router les paquets de données sur un réseau.|
|`Protocoles de commutation`|Tels que le [VLAN Trunking Protocol](https://en.wikipedia.org/wiki/VLAN_Trunking_Protocol) (`VTP`) et le [Spanning Tree Protocol](https://en.wikipedia.org/wiki/Spanning_Tree_Protocol) (`STP`) sont utilisés pour configurer et gérer les commutateurs sur un réseau.|
|`Services réseau`|Tels que le [Dynamic Host Configuration Protocol](https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol) (`DHCP`) sont utilisés pour fournir automatiquement aux clients du réseau des adresses IP et d'autres configurations réseau.|
|`Fonctionnalités de sécurité`|Telles que les [listes de contrôle d'accès](https://en.wikipedia.org/wiki/Access-control_list) (`ACL`), qui sont utilisées pour contrôler l'accès aux ressources du réseau et prévenir les menaces de sécurité.|

---

Dans Cisco IOS, différents types de mots de passe sont utilisés à des fins diverses, par exemple :

|**Type de Mot de Passe**|**Description**|
|---|---|
|`User`|Le mot de passe [utilisateur](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/s1/sec-s1-cr-book/sec-cr-t2.html#wp2992613898) est utilisé pour se connecter à Cisco IOS. Il sert à restreindre l'accès à l'équipement réseau et à ses fonctionnalités.|
|`Enable Password`|Le mot de passe [d'activation](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/d1/sec-d1-cr-book/sec-cr-e1.html#wp3884449514) est utilisé pour entrer en mode « enable ». Le mode « enable » est le mode où vous avez accès aux fonctions et paramètres avancés.|
|`Secret`|Le [secret](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/s1/sec-s1-cr-book/sec-cr-s1.html#wp2622423174) est un mot de passe pour sécuriser l'accès à certaines fonctions et services. Il est souvent utilisé pour restreindre l'accès aux outils et services de gestion à distance.|
|`Enable Secret`|Le [secret d'activation](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/d1/sec-d1-cr-book/sec-cr-e1.html#wp3438133060) est un mot de passe ultra-sécurisé utilisé pour sécuriser l'accès au mode « enable », et ils sont stockés de manière chiffrée pour fournir une protection supplémentaire.|

Nous vous recommandons vivement de consulter les ressources externes fournies pour comprendre les mécanismes de chiffrement de Cisco IOS et la manière dont ils sont utilisés.

Les équipements Cisco IOS peuvent être configurés pour SSH ou Telnet. Ils peuvent donc être accessibles à distance. Nous pouvons déterminer à partir de la réponse que nous recevons qu'il s'agit bien d'un Cisco IOS, car il répond avec le message `User Access Verification`.

#### Cisco IOS

```bash
Hiterof13@htb[/htb]$ telnet 10.129.10.2

Trying 10.129.10.2...
Connected to 10.129.10.2.
Escape character is '^]'.


User Access Verification

Password:
```

---

# VLANs

Imaginons le scénario suivant : une startup nommée XQ a engagé un administrateur réseau pour créer un réseau pour son entreprise à bureau unique, et en raison de limitations budgétaires, ils ne peuvent s'offrir qu'un seul commutateur et un seul routeur. L'administrateur système de XQ a déclaré qu'en plus d'héberger les serveurs web et de base de données sur le réseau, le personnel de différents départements l'utilisera. En tant que spécialiste expérimenté de la sécurité réseau, l'administrateur réseau a immédiatement pensé aux attaques de sécurité qu'un initié pourrait perpétrer, en particulier celles abusant du trafic de diffusion (broadcast traffic), comme les `tempêtes de diffusion` (broadcast storms). Par conséquent, pour résoudre ce problème, l'administrateur réseau a décidé de segmenter logiquement le réseau avec des `Réseaux Locaux Virtuels` (`VLAN`), décomposant conceptuellement un commutateur en de plus petits mini-commutateurs.

Un `VLAN` est un regroupement logique de points de terminaison réseau connectés à des ports définis sur un commutateur, permettant la segmentation des réseaux en créant des domaines de diffusion logiques qui peuvent s'étendre sur plusieurs segments de réseau local physique. Avec les `VLAN`, les administrateurs réseau peuvent segmenter les réseaux en fonction de facteurs tels que l'équipe, la fonction, le département ou l'application, sans se soucier de l'emplacement physique des points de terminaison et des utilisateurs. Un paquet de diffusion envoyé sur un `VLAN` n'atteint aucun autre point de terminaison membre d'un autre `VLAN`. Parce que chaque `VLAN` est considéré comme un domaine de diffusion, il doit avoir son propre `sous-réseau` ; par exemple, l'administrateur réseau engagé par XQ peut segmenter le réseau par départements :

|**Département**|**ID de VLAN**|**Sous-réseau**|
|:-:|:-:|:-:|
|`Servers`|`VLAN 10`|`192.168.1.0/24`|
|`C-Level`|`VLAN 20`|`192.168.2.0/24`|
|`Finance`|`VLAN 30`|`192.168.3.0/24`|
|`HR`|`VLAN 40`|`192.168.4.0/24`|
|`Marketing`|`VLAN 50`|`192.168.5.0/24`|
|`Support`|`VLAN 60`|`192.168.6.0/24`|

Une myriade d'avantages est obtenue lors de l'utilisation des `VLAN`, notamment :

- `Meilleure Organisation` : Les administrateurs réseau peuvent regrouper les points de terminaison en fonction de n'importe quel attribut commun qu'ils partagent.
- `Sécurité Accrue` : La segmentation du réseau empêche les membres non autorisés d'écouter les paquets réseau dans d'autres `VLAN`.
- `Administration Simplifiée` : Les administrateurs réseau n'ont pas à se soucier de l'emplacement physique d'un point de terminaison.
- `Performance Accrue` : Avec un trafic de diffusion réduit pour tous les points de terminaison, plus de bande passante est disponible pour être utilisée par le réseau.

Les commutateurs Cisco fournissent les ID/numéros de `VLAN` 1 à 4094 (`0` et `4095` sont des ID réservés et ne peuvent pas être utilisés) ; les ID 1 à 1005 (le `VLAN 1` est connu comme le `VLAN par défaut` et ne peut/doit pas être modifié ni supprimé) sont connus comme des `VLAN` de `plage normale`, les ID 1002 à 1005 étant réservés pour les `VLAN` `Token Ring` et `Fiber Distributed Data Interface` (`FDDI`), tandis que les ID 1006 à 4094 sont connus comme des `VLAN` de `plage étendue`. Par défaut, toute personnalisation appliquée aux `VLAN` de `plage normale` est enregistrée dans la base de données `VLAN` (le fichier `vlan.dat`), contrairement aux `VLAN` de `plage étendue`, dont les personnalisations ne sont pas enregistrées. Les `VLAN` 2 à 1001 stockés dans `vlan.dat` peuvent avoir des paramètres incluant le nom, le type, l'état et l'unité de transmission maximale (`MTU`).

## Appartenances aux VLAN

Les administrateurs réseau peuvent assigner les ports d'un commutateur à des `VLAN` de manière statique ou dynamique. L'assignation statique de `VLAN`, qui est la méthode la plus simple et la plus courante, consiste à assigner manuellement chaque port à un `VLAN` à l'aide du `système d'exploitation réseau` du commutateur ; cela doit être fait séparément pour tous les commutateurs (il est essentiel de garder à l'esprit que les points de terminaison se connectant à ces ports ne sont pas conscients de l'existence des `VLAN`). En revanche, l'assignation dynamique de `VLAN` détermine automatiquement l'appartenance d'un point de terminaison à un `VLAN` en fonction des adresses `MAC` ou des protocoles. L'administrateur système peut enregistrer les adresses `MAC` dans un service/base de données centralisé de gestion de `VLAN`, tel que le service `VLAN Membership Policy Server` (`VMPS`), puis le commutateur interroge la base de données du `VMPS` pour déterminer le `VLAN` du point de terminaison avec cette adresse `MAC` spécifique. Indépendamment de leur flexibilité et de leur mobilité, les `VLAN` dynamiques augmentent la charge administrative.

Du point de vue de la sécurité, les `VLAN` statiques sont l'option la plus sûre car un port sera toujours lié à un ID de `VLAN` spécifique, à moins d'être modifié manuellement par la suite. Pour les `VLAN` dynamiques, un attaquant pourrait potentiellement utiliser des outils tels que [macchanger](https://github.com/alobbs/macchanger) pour usurper l'adresse MAC de points de terminaison légitimes et obtenir l'appartenance à leurs `VLAN`, et ainsi écouter tout le trafic réseau qui y transite.

## Ports d'Accès et Ports de Trunk

Tout port sur un commutateur compatible `VLAN` doit être soit un `port d'accès`, soit un `port de trunk`. Les `ports d'accès` appartiennent et ne peuvent transporter que le trafic d'un seul `VLAN` (ou dans certains cas deux, le second étant pour le `trafic voix`) ; tout trafic arrivant sur un `port d'accès` est supposé appartenir au `VLAN` auquel le port a été assigné. D'autre part, les `ports de trunk` peuvent transporter plusieurs `VLAN` en même temps ; les `liaisons trunk` connectent deux `ports de trunk` sur deux commutateurs (ou un commutateur et un routeur) pour permettre aux informations de plusieurs `VLAN` d'être transportées à travers les commutateurs.

## Identification des VLAN

Les trames `Ethernet` `802.3` standard ne contiennent pas d'informations de `VLAN` ; par conséquent, les commutateurs et autres périphériques compatibles `VLAN` ont besoin d'un mécanisme pour suivre toutes les informations de `VLAN` associées à un paquet lorsqu'il traverse des périphériques compatibles `VLAN`. Deux principales `méthodes de trunking` sont utilisées pour y parvenir, `ISL` et `IEEE 802.1Q`.

#### Inter-Switch Link (ISL)

`Inter-Switch Link` (`ISL`) est un protocole propriétaire de Cisco utilisé pour le trunking entre des périphériques compatibles `VLAN`. Bien que `ISL` soit l'une des premières `méthodes de trunking` (antérieure à `802.1Q`), il est obsolète et n'est plus aussi largement utilisé dans les commutateurs (et routeurs) Cisco modernes. Au lieu de cela, la plupart ne prennent en charge que la norme `802.1Q` largement adoptée. `ISL` encapsulait l'ensemble de la trame `Ethernet`, y compris l'en-tête `Ethernet` original et l'étiquette `VLAN`, en y ajoutant son propre en-tête de 26 octets et une remorque de 4 octets.

#### IEEE 802.1Q

Pour garantir l'interopérabilité des technologies `VLAN` des différents fournisseurs d'équipements réseau, l'`Institute of Electrical and Electronics Engineers` (`IEEE`) a développé la spécification [802.1Q](https://ieeexplore.ieee.org/document/10004498) en 1998. Le comité `IEEE 802` a dû modifier le format de la trame `Ethernet` `802.3` en ajoutant une paire de champs de 2 octets, `TPID` et `TCI` (qui se compose de trois sous-champs, `PCP`, `DEI` et `VID`), ce qui donne une trame `Ethernet` `802.1Q` compatible `VLAN`.

![Schéma montrant la conversion d'une trame Ethernet 802.3 en une trame Ethernet 802.1Q par l'insertion d'un en-tête 802.1Q entre les champs d'adresse source et de longueur. L'en-tête 802.1Q inclut TPID, PCP, DEI et VID.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/8023_Legacy_8021Q_Ethernet_Frames.png)

Le `Tag protocol identifier` (`TPID`) est un champ de 16 bits toujours défini sur `0x8100` pour identifier la trame `Ethernet` comme une trame étiquetée `802.1Q`. Le `Tag Control Information` (`TCI`) est un champ de 16 bits contenant le `Priority code point` (`PCP`), le `Drop eligible indicator` (`DEI`) (précédemment connu sous le nom de `Canonical format indicator` (`CFI`)), et le `VLAN identifier` (`VID`). Le champ principal concernant les `VLAN` est le `VID`, qui occupe les 12 bits de poids faible du `TCI`. Comme il est de 12 bits, il y a 2^12 = 4096 valeurs possibles, mais comme `0` et `4095` sont réservés, vous pouvez en fait utiliser `4094` ID de `VLAN`. Par conséquent, une trame étiquetée `802.1Q` peut contenir des informations pour 4094 `VLAN` ; la pratique d'insérer plusieurs étiquettes `802.1Q` dans un seul paquet est connue sous le nom de `Double étiquetage` (Double Tagging), introduit par [802.1ad](https://standards.ieee.org/ieee/802.1Q/10323/). L'`étiquetage de VLAN` (VLAN tagging) est le processus d'insertion d'informations de `VLAN` dans un en-tête `Ethernet` `802.1Q`, tandis que le `désétiquetage de VLAN` (VLAN untagging) est le processus de suppression des informations de `VLAN` d'une trame `Ethernet` étiquetée `802.1Q` et de transmission du paquet aux ports de destination.

## Cartes réseau compatibles VLAN

Certaines `cartes d'interface réseau` (`NIC`) connectées à des ordinateurs/serveurs prennent en charge l'`étiquetage de VLAN` (VLAN tagging). Voyons comment nous pouvons assigner un ID de `VLAN` à une `NIC` en utilisant Linux et Windows.

#### Assigner une carte réseau à un VLAN sous Linux

Sous Linux, la création d'un `VLAN` se fait en créant une interface au-dessus d'une autre, appelée interface `parente`. Cette interface `VLAN` étiquettera les paquets avec l'ID de `VLAN` assigné tandis que les paquets de retour seront désétiquetés.

Pour assigner une carte réseau à un `VLAN` sous Linux, de nombreux outils peuvent être utilisés, tels que [ip](https://man7.org/linux/man-pages/man8/ip.8.html), [nmcli](https://linux.die.net/man/1/nmcli), et [vconfig](https://linux.die.net/man/8/vconfig) (obsolète). Cependant, nous devons d'abord nous assurer que le noyau a chargé le module [802.1Q](https://elixir.bootlin.com/linux/v6.4.7/source/net/8021q/vlan.c) :

```bash
Hiterof13@htb[/htb]$ sudo modprobe 8021q
```

Ensuite, nous pouvons utiliser `lsmod` pour nous assurer que `8021q` a été chargé avec succès :

```bash
Hiterof13@htb[/htb]$ lsmod | grep 8021

8021q                  40960  0
garp                   16384  1 8021q
mrp                    20480  1 8021q
```

Maintenant, nous devons trouver le nom de l'interface `Ethernet` physique sur laquelle nous allons créer l'interface `VLAN`, qui est `eth0` :

```bash
Hiterof13@htb[/htb]$ ip a

<SNIP>
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether a6:ba:3b:08:3a:36 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    altname ens3
    inet 94.2X.5X.72/22 brd 94.237.51.255 scope global dynamic eth0
       valid_lft 83489sec preferred_lft 83489sec
    inet6 fe80::a4ba:3bff:fe08:3a36/64 scope link
        valid_lft forever preferred_lft forever
```

Ensuite, nous utiliserons `vconfig` pour créer une nouvelle interface qui est membre du `VLAN` souhaité, `20` par exemple, au-dessus de `eth0` :

```bash
Hiterof13@htb[/htb]$ sudo vconfig add eth0 20

Warning: vconfig is deprecated and might be removed in the future, please migrate to ip(route2) as soon as possible!
```

Pour utiliser `ip` à la place :

```bash
sudo ip link add link eth0 name eth0.20 type vlan id 20
```

L'une ou l'autre de ces commandes créera une nouvelle interface appelée `eth0.20@eth0` :

```bash
Hiterof13@htb[/htb]$ ip a

<SNIP>
4: eth0.20@eth0: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether a6:ba:3b:08:3a:36 brd ff:ff:ff:ff:ff:ff
```

Ensuite, en fonction du `sous-réseau` assigné aux adresses avec le `VLAN 20` au sein du réseau local, nous devons assigner une adresse IP à l'interface puis la démarrer :

```bash
Hiterof13@htb[/htb]$ sudo ip addr add 192.168.1.1/24 dev eth0.20
Hiterof13@htb[/htb]$ sudo ip link set up eth0.20
```

Enfin, nous pouvons vérifier si l'état de l'interface est passé à `up` :

```bash
Hiterof13@htb[/htb]$ ip a | grep eth0.20

4: eth0.20@eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    inet 192.168.1.1/24 scope global eth0.20
```

#### Assigner une carte réseau à un VLAN sous Windows

Sous Windows, pour assigner un `VLAN` à un adaptateur réseau physique qui prend en charge l'`étiquetage de VLAN`, nous devons d'abord ouvrir le `Gestionnaire de périphériques` :

![Interface de recherche Windows montrant 'Gestionnaire de périphériques' comme meilleur résultat sous Panneau de configuration.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/Windows_Device_Manager.png)

Ensuite, nous devons cliquer sur `Propriétés` pour l' `interface Ethernet` que nous voulons assigner à un `VLAN` :

![Fenêtre du Gestionnaire de périphériques montrant un menu contextuel pour l'adaptateur ASIX AX88772B USB2.0 to Fast Ethernet avec 'Propriétés' en surbrillance.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/Windows_Device_Manager_Adapter_Properties.png)

Dans `Avancé`, il y aura une propriété `VLAN ID` à laquelle nous pouvons assigner une valeur. Après avoir cliqué sur `OK`, si l'adaptateur prend en charge l'assignation d'un `VLAN`, il sera défini ; sinon, la fenêtre se fermera, et aucune étiquette `VLAN` ne sera ajoutée aux paquets provenant de cet hôte :

![Fenêtre du Gestionnaire de périphériques montrant les propriétés de l'adaptateur ASIX AX88772B USB2.0 to Fast Ethernet. L'ID de VLAN est sélectionné avec une valeur de 10.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/Windows_Device_Manager_Adapter_Properties_VLAN_ID.png)

Au lieu de se fier à l'interface graphique, nous pouvons utiliser `PowerShell`. D'abord, obtenons les noms de tous les adaptateurs réseau physiques disponibles en utilisant le Cmdlet [Get-NetAdapter](https://learn.microsoft.com/en-us/powershell/module/netadapter/get-netadapter?view=windowsserver2022-ps) :

```powershell
PS C:\> Get-NetAdapter | Format-Table -AutoSize

Name                                           InterfaceDescription                                                          ifIndex Status             MacAddress              LinkSpeed
----                                           --------------------                                                          ------- ------             ----------              ---------
VirtualBox Host-Only Network  VirtualBox Host-Only Ethernet Adapter                                        20 Up                    0A-00-27-10-42-15       1 Gbps
Ethernet 2                                 ASIX AX88772B USB2.0 to Fast Ethernet Adapter                            55 Up                    90-EB-78-14-21-7F    100 Mbps
Bluetooth Network Connection  Bluetooth Device (Personal Area Network)                                   18 Disconnected   38-41-25-E8-DE-2D        3 Mbps
Wi-Fi                                         Intel(R) Wireless-AC 9560 160MHz                                                12 Disconnected   8E-36-6A-7A-BA-6A 866.7 Mbps
```

Précédemment, nous avons utilisé le `Gestionnaire de périphériques` pour assigner `Ethernet 2` au `VLAN 10` ; pour récupérer l'ID de `VLAN` de l'interface, nous pouvons utiliser le Cmdlet [Get-NetAdapterAdvancedProperty](https://learn.microsoft.com/en-us/powershell/module/netadapter/get-netadapteradvancedproperty?view=windowsserver2022-ps) avec le drapeau `-DisplayName` avec `vlan id` :

```powershell
PS C:\> Get-NetAdapterAdvancedProperty -DisplayName "vlan id"

Name                      DisplayName                    DisplayValue                   RegistryKeyword RegistryValue
----                      -----------                    ------------                   --------------- -------------
Ethernet 2                VLAN ID                        10                                     VLAN_ID               {10}
```

Nous pouvons également définir l'ID de `VLAN` d'une adresse réseau physique en utilisant le Cmdlet [Set-NetAdapter](https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadapter?view=windowsserver2022-ps) avec le drapeau [VlanID](https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadapter?view=windowsserver2022-ps#-vlanid) ; ce puissant Cmdlet peut également être utilisé pour personnaliser d'autres propriétés des interfaces telles que les [adresses MAC](https://learn.microsoft.com/en-us/powershell/module/netadapter/set-netadapter?view=windowsserver2022-ps#-macaddress) :

```powershell
PS C:\> Set-NetAdapter -Name "Ethernet 2" -VlanID 10
```

Cependant, rappelez-vous que cette opération ne réussit que si l'interface réseau prend en charge cette fonctionnalité ; sinon, `PowerShell` lèvera une erreur indiquant que l'interface ne la prend pas en charge.

## Analyser le Trafic Étiqueté VLAN

Nous pouvons identifier et analyser le trafic étiqueté `VLAN` sur un réseau avec `Wireshark` en utilisant le filtre [vlan](https://www.wireshark.org/docs/dfref/v/vlan.html). Par exemple, lors de l'analyse d'une capture de paquets réseau, nous pouvons inspecter les paquets avec un étiquetage `802.1Q` en utilisant le filtre `vlan` :

![Interface de Wireshark montrant une capture de paquets avec un paquet de réponse RIP v2 en surbrillance, et les détails Ethernet II, 802.1Q VLAN et Protocole Internet.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/Wireshark_VLAN_Filter.png)

De plus, nous pouvons rechercher des paquets avec un ID de `VLAN` spécifique ; par exemple, pour rechercher des paquets ayant le `VLAN 10`, nous pouvons utiliser le filtre `vlan.id == 10` :

![Interface de Wireshark montrant une capture de paquets avec un paquet de réponse RIP v2 en surbrillance, et les détails Ethernet II, 802.1Q VLAN et Protocole Internet.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/Wireshark_VLAN_ID_Filter.png)

De plus, pour énumérer les ID de `VLAN` utilisés à partir d'une capture de paquets, nous pouvons utiliser [tshark](https://www.wireshark.org/docs/man-pages/tshark.html) :

```bash
Hiterof13@htb[/htb]$ tshark -r "The Ultimate PCAP v20221220.pcapng" -T fields -e vlan.id | sort -n -u

1
2
3
7
10
20
30
40
50
60
70
80
90
121
125
224
```

---

## Implications de Sécurité et Attaques de VLAN

Malgré l'amélioration de la posture de sécurité d'un réseau, les adversaires peuvent toujours contourner les mécanismes de défense mis en place par les `VLAN`. Bien que dans les réseaux commutés modernes, l'utilisation des `VLAN` apporte de nombreux avantages (tels que la maintenance simplifiée du réseau et l'amélioration des performances), elle introduit également des risques de sécurité potentiels, menant à diverses attaques de `VLAN`. Il est essentiel de comprendre les méthodologies sous-jacentes de ces attaques et de mettre en œuvre des approches d'atténuation pratiques pour protéger les réseaux.

#### Saut de VLAN (VLAN Hopping)

Les attaques de `saut de VLAN` (VLAN hopping) permettent au trafic d'un `VLAN` d'être vu par un autre `VLAN` sans l'aide d'un routeur. Elles exploitent le `Dynamic Trunking Protocol` (`DTP`) de Cisco, un protocole utilisé pour négocier automatiquement la formation d'une `liaison trunk` entre deux appareils Cisco. Un adversaire doit configurer un hôte pour imiter/agir comme un commutateur afin de tirer parti de la fonctionnalité de port de trunking automatique activée par défaut sur la plupart des ports de commutateur. Pour exploiter le `saut de VLAN`, un adversaire doit pouvoir se connecter physiquement à un port de commutateur sur lequel le `DTP` est activé. L'adversaire peut abuser de cette connexion en configurant un hôte connecté au commutateur sur ce port spécifique pour usurper la signalisation `802.1Q` et les paquets `DTP`. En cas de succès, le commutateur établira finalement une `liaison trunk` avec l'hôte de l'adversaire, exposant les paquets réseau, et pas seulement pour un `VLAN` spécifique.

Nous pouvons utiliser des outils tels que [Yersinia](https://linux.die.net/man/8/yersinia) pour effectuer des attaques de `saut de VLAN` :

![Interface de Yersinia montrant les options d'attaque de protocole avec 'enabling trunking' sélectionné pour le Dynamic Trunking Protocol (DTP).](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/Yersinia_DTP_Attack.png)

#### Saut de VLAN par double étiquetage

L'`attaque par saut de VLAN avec double étiquetage` (double-tagging VLAN hopping attack) est une attaque de plus en plus sophistiquée contre les `VLAN`. Bien que le `double étiquetage de VLAN` soit une pratique légitime que des entités telles que les `Fournisseurs de Services Internet` (`FAI`) utilisent (ils peuvent utiliser leurs `VLAN` en interne tout en transportant le trafic de clients déjà `étiqueté VLAN`), les adversaires peuvent également tenter d'en abuser. Dans une `attaque par saut de VLAN avec double étiquetage`, un adversaire intègre une étiquette `802.1Q` cachée à l'intérieur d'une trame `Ethernet` qui a déjà une étiquette `802.1Q`, permettant à la trame d'aller vers un `VLAN` différent, que l'étiquette `802.1Q` originale ne spécifiait pas.

Un adversaire peut mener cette attaque en suivant trois étapes. Gardez à l'esprit que cette attaque ne fonctionne que si l'adversaire est connecté à un port résidant dans le même `VLAN` que le `VLAN natif` du port de trunk :

1. L'adversaire envoie une trame `Ethernet` `802.1Q` `doublement étiquetée` au commutateur avec l'en-tête externe ayant l'ID de `VLAN` de l'adversaire, qui est le même que le `VLAN natif` du port de trunk. Supposons que le `VLAN natif` est le `VLAN 10` et que le `VLAN 30` est le `VLAN` que l'adversaire veut atteindre, où réside la victime.
2. L'étiquette externe `802.1Q` de 4 octets arrive sur le commutateur, et il est vu qu'elle est destinée au `VLAN 10`, le `VLAN natif`. Après avoir retiré l'étiquette `VLAN 10`, la trame est transmise sur tous les ports du `VLAN 10`. Sur le port de trunk, l'étiquette `VLAN 10` est retirée (supprimée), et le paquet n'est pas ré-étiqueté car il fait partie du `VLAN natif`. Cependant, l'étiquette `VLAN 30` est toujours intacte (non retirée), et le premier commutateur ne l'a pas inspectée.
3. Par la suite, le commutateur ne regardera que l'étiquette `802.1Q` interne que l'adversaire a envoyée, et il décide que la trame doit être transmise pour le `VLAN 30`, qui est le `VLAN` choisi par l'adversaire. Maintenant, le deuxième commutateur enverra la trame directement au port de la victime ou l'inondera, selon qu'il existe ou non une entrée dans la table d'adresses MAC pour l'hôte victime.

[Scapy](https://scapy.readthedocs.io/en/latest/usage.html#vlan-hopping) permet de réaliser l'`attaque par saut de VLAN avec double étiquetage`, en plus de `Yersinia` :

![Interface de Yersinia montrant les options d'attaque de protocole avec 'sending 802.1Q double enc. packet' sélectionné.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/34/Yersinia_Double_Tagging_VLAN_Hopping_Attack.png)

---

## VXLAN

Nous avons mentionné précédemment que le champ `VID` dans l'en-tête `802.1Q` à l'intérieur d'une trame `Ethernet` n'est que de 12 bits, ce qui permet 4094 VLAN. Bien que ce nombre de VLAN puisse être suffisant pour les petits réseaux, il en faut plus pour les centres de données et les fournisseurs de services cloud, qui nécessitent une segmentation étendue. De plus, les réseaux de couche 2 actuels utilisent le `Protocole Spanning Tree` (`STP`) `IEEE 802.1D` pour éviter les boucles réseau causées par des chemins redondants. Cependant, certains opérateurs de centres de données rencontrent des limitations avec le `STP`, telles que le blocage de liens, ce qui réduit les ports disponibles et empêche la résilience par le multi-chemin. Ces défis entravent l'efficacité du réseau dans les environnements virtualisés qui reposent sur une infrastructure physique de couche 2. Une exigence essentielle dans de tels environnements est l'évolutivité transparente du réseau de couche 2 à travers l'ensemble du centre de données et même entre les centres de données pour allouer efficacement les ressources de calcul, de réseau et de stockage. Néanmoins, les approches traditionnelles comme le `STP`, tout en assurant une topologie sans boucle, peuvent désactiver de nombreux liens, exacerbant davantage le problème.

La [RFC7348](https://datatracker.ietf.org/doc/html/rfc7348) offre une solution à ces problèmes et limitations dans les réseaux de couche 2 en introduisant le `Virtual eXtensible Local Area Network` (`VXLAN`), qui est essentiellement un « schéma de superposition de couche 2 sur un réseau de couche 3 ». Le `VXLAN` est spécifiquement conçu pour répondre aux limitations des réseaux de couche 2 traditionnels et aux exigences des infrastructures réseau de centre de données de couche 2 et 3 dans un environnement multi-locataire (multi-tenant) avec des machines virtuelles (VM). Fonctionnant sur l'infrastructure réseau existante, `VXLAN` fournit un moyen innovant d'étendre de manière transparente un réseau de couche 2. Son objectif principal est de faciliter la mise à l'échelle des réseaux de couche 2 à travers de vastes paysages de centres de données, s'étendant même sur plusieurs emplacements de données physiques. Chaque superposition `VXLAN` est appelée un `segment VXLAN`, garantissant que seules les VM au sein du même segment VXLAN peuvent communiquer entre elles, maintenant ainsi l'isolement et la sécurité du réseau. Un ID de segment de 24 bits, connu sous le nom de `VXLAN Network Identifier` (`VNI`), identifie de manière unique chaque segment VXLAN. L'adoption de VXLAN permet la coexistence de 16 millions de segments `VXLAN` au sein du même domaine administratif, offrant une évolutivité et une flexibilité pour les centres de données modernes et les environnements virtualisés.

---

## Protocole de Découverte Cisco

Le Protocole de Découverte Cisco (CDP) est un protocole réseau de couche 2 de Cisco qui est utilisé par les appareils Cisco tels que les routeurs, les commutateurs et les ponts pour recueillir des informations sur d'autres appareils Cisco directement connectés. Ces informations peuvent être utilisées pour découvrir et suivre la topologie du réseau et aider à gérer et dépanner le réseau. Ce protocole est généralement activé dans les appareils Cisco, mais il peut être désactivé s'il n'est pas nécessaire ou s'il doit être désactivé pour des raisons de sécurité.

#### Trafic Réseau CDP

```bash
22:14:11.563654 CDPv2, ttl: 180s, checksum: 0xebc1 (incorrect -> 0x8b71), length: 180
        Device-ID (0x01), length: 14 bytes: 'router.inlanefreight.loc'
        Addresses (0x02), length: 8 bytes:
                IPv4 (0x01), length: 4: 10.129.100.1
        Port-ID (0x03), length: 9 bytes: 'Ethernet0/0'
        Capability (0x04), length: 4: (0x00000010): Router
        Version String (0x05), length: 27 bytes: 'Cisco IOS Software, C880 Software'
        Platform (0x06), length: 26 bytes: 'Cisco 881 (MPC8300) processor'
```

Le message affiché contient des informations sur l'appareil lui-même, telles que le nom de l'appareil, l'adresse IP, le nom du port et la fonctionnalité du routeur, ainsi que des informations sur le système d'exploitation et la plate-forme matérielle de l'appareil. De plus, nous pouvons voir à la première ligne, avec `CDPv2`, que nous avons affaire au `Protocole de Découverte Cisco`.

À des fins de comparaison, nous pouvons examiner un autre protocole appelé Spanning Tree Protocol (`STP`). Le `STP` est un protocole réseau qui garantit l'absence de boucles dans un réseau avec plusieurs connexions entre les commutateurs. Il n'y a pas de boucles, et il empêche les paquets de données de circuler en boucle et de congestionner le réseau.

#### Trafic Réseau STP

```bash
22:14:11.563654 STP 802.1w, Rapid STP, Flags [Learn, Forward], bridge-id 8001.00:11:22:33:44:55.8000, length 43
        root-id 8001.AA:AA:AA:AA:AA:AA, cost 0, port-id 8001, message-age 0.00s, max-age 20.00s, hello-time 2.00s, forward-delay 15.00s
```

Dans cet exemple, nous voyons qu'un message `STP` a été envoyé, contenant des informations sur le commutateur racine, l'adresse MAC du commutateur racine, l'ID du port sur lequel le message a été envoyé, et d'autres paramètres de configuration tels que le temps de vieillissement maximum, le temps de salutation et le délai de transmission.
---

← [[16 - Réseaux Privés Virtuels]] | [[00 - Sommaire Introduction to Networking|Sommaire]] | [[18 - Mécanismes d'échange de clés]] →
