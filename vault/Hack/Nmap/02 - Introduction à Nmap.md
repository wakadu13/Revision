---
tags:
  - nmap
ordre: 2
---

# Introduction à Nmap

---

Network Mapper (`Nmap`) est un outil open-source d'analyse de réseau et d'audit de sécurité écrit en C, C++, Python et Lua. Il est conçu pour scanner les réseaux et identifier les hôtes disponibles sur le réseau à l'aide de paquets bruts (raw packets), ainsi que les services et les applications, y compris leur nom et leur version, lorsque c'est possible. Il peut également identifier les systèmes d'exploitation et les versions de ces hôtes. En plus d'autres fonctionnalités, Nmap offre également des capacités de scan qui peuvent déterminer si des filtres de paquets, des pare-feux (firewalls), ou des systèmes de détection d'intrusion (IDS) sont configurés comme il se doit.

---

## Cas d'utilisation

Cet outil est l'un des plus utilisés par les administrateurs réseau et les spécialistes de la sécurité informatique. Il est utilisé pour :

- Auditer les aspects de sécurité des réseaux
- Simuler des tests d'intrusion (penetration tests)
- Vérifier les paramètres et les configurations des pare-feux et des IDS
- Types de connexions possibles
- Cartographier le réseau (Network mapping)
- Analyser les réponses
- Identifier les ports ouverts
- Évaluer les vulnérabilités également.

---

## Architecture de Nmap

Nmap propose de nombreux types de scans différents qui peuvent être utilisés pour obtenir divers résultats sur nos cibles. Fondamentalement, Nmap peut être divisé selon les techniques de scan suivantes :

- Découverte d'hôtes (Host discovery)
- Scan de ports (Port scanning)
- Énumération et détection de services
- Détection d'OS
- Interaction scriptable avec le service cible (Nmap Scripting Engine)

---

## Syntaxe

La syntaxe pour Nmap est assez simple et se présente comme suit :

```bash
Hiterof13@htb[/htb]$ nmap <scan types> <options> <target>
```

---

## Techniques de Scan

Nmap propose de nombreuses techniques de scan différentes, établissant différents types de connexions et utilisant des paquets structurés différemment pour l'envoi. Nous pouvons voir ici toutes les techniques de scan que Nmap propose :

```bash
Hiterof13@htb[/htb]$ nmap --help

<SNIP>
SCAN TECHNIQUES:
  -sS/sT/sA/sW/sM: TCP SYN/Connect()/ACK/Window/Maimon scans
  -sU: UDP Scan
  -sN/sF/sX: TCP Null, FIN, and Xmas scans
  --scanflags <flags>: Customize TCP scan flags
  -sI <zombie host[:probeport]>: Idle scan
  -sY/sZ: SCTP INIT/COOKIE-ECHO scans
  -sO: IP protocol scan
  -b <FTP relay host>: FTP bounce scan
<SNIP>
```

Par exemple, le scan TCP-SYN (`-sS`) est l'un des paramètres par défaut, sauf si nous en avons défini un autre, et c'est aussi l'une des méthodes de scan les plus populaires. Cette méthode de scan permet de scanner plusieurs milliers de ports par seconde. Le scan TCP-SYN envoie un paquet avec le drapeau (flag) SYN et, par conséquent, ne termine jamais la poignée de main en trois temps (three-way handshake), ce qui a pour résultat de ne pas établir une connexion TCP complète avec le port scanné.

- Si notre cible nous renvoie un paquet avec le drapeau `SYN-ACK`, Nmap détecte que le port est `open`.
- Si la cible répond avec un paquet avec le drapeau `RST`, c'est un indicateur que le port est `closed`.
- Si Nmap ne reçoit pas de paquet en retour, il l'affichera comme `filtered`. Selon la configuration du pare-feu, certains paquets peuvent être abandonnés (dropped) ou ignorés par le pare-feu.

Prenons un exemple d'un tel scan.

```bash
Hiterof13@htb[/htb]$ sudo nmap -sS localhost

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-11 22:50 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000010s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
5432/tcp open  postgresql
5901/tcp open  vnc-1

Nmap done: 1 IP address (1 host up) scanned in 0.18 seconds
```

Dans cet exemple, nous pouvons voir que nous avons quatre ports TCP différents ouverts. Dans la première colonne, nous voyons le numéro du port. Ensuite, dans la deuxième colonne, nous voyons l'état du service, puis de quel type de service il s'agit.
---

← [[01 - Énumération]] | [[00 - Sommaire Nmap|Sommaire]] | [[03 - Découverte d'Hôtes]] →
