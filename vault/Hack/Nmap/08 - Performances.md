---
tags:
  - nmap
ordre: 8
---

# Performances

---

Les performances de scan jouent un rôle important lorsque nous devons scanner un réseau étendu ou lorsque nous avons affaire à une faible bande passante réseau. Nous pouvons utiliser diverses options pour indiquer à `Nmap` à quelle vitesse (`-T <0-5>`), avec quelle fréquence (`--min-parallelism <number>`), quels timeouts (`--max-rtt-timeout <time>`) les paquets de test doivent avoir, combien de paquets doivent être envoyés simultanément (`--min-rate <number>`), et avec quel nombre de réessais (`--max-retries <number>`) pour les ports scannés les cibles doivent être scannées.

---

## Timeouts

Lorsque Nmap envoie un paquet, il faut un certain temps (`temps d'aller-retour (Round-Trip-Time)` - `RTT`) pour recevoir une réponse du port scanné. Généralement, `Nmap` démarre avec un timeout élevé (`--min-RTT-timeout`) de 100ms. Voyons un exemple en scannant l'ensemble du réseau avec 256 hôtes, y compris les 100 ports les plus courants.

#### Scan par Défaut

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.0/24 -F

<SNIP>
Nmap done: 256 IP addresses (10 hosts up) scanned in 39.44 seconds
```

#### RTT Optimisé

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.0/24 -F --initial-rtt-timeout 50ms --max-rtt-timeout 100ms

<SNIP>
Nmap done: 256 IP addresses (8 hosts up) scanned in 12.29 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.0/24`|Scanne le réseau cible spécifié.|
|`-F`|Scanne les 100 ports les plus courants.|
|`--initial-rtt-timeout 50ms`|Définit la valeur de temps spécifiée comme timeout RTT initial.|
|`--max-rtt-timeout 100ms`|Définit la valeur de temps spécifiée comme timeout RTT maximum.|

En comparant les deux scans, nous pouvons voir que nous avons trouvé deux hôtes de moins avec le scan optimisé, mais que le scan n'a pris qu'un quart du temps. Nous pouvons en conclure que définir le timeout RTT initial (`--initial-rtt-timeout`) sur une période trop courte peut nous faire manquer des hôtes.

---

## Nombre Maximum de Réessais

Une autre façon d'augmenter la vitesse du scan est de spécifier le nombre de réessais pour les paquets envoyés (`--max-retries`). La valeur par défaut est `10`, mais nous pouvons la réduire à `0`. Cela signifie que si Nmap ne reçoit pas de réponse pour un port, il n'enverra plus de paquets à ce port et le passera.

#### Scan par Défaut

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.0/24 -F | grep "/tcp" | wc -l

23
```

#### Réessais Réduits

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.0/24 -F --max-retries 0 | grep "/tcp" | wc -l

21
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.0/24`|Scanne le réseau cible spécifié.|
|`-F`|Scanne les 100 ports les plus courants.|
|`--max-retries 0`|Définit le nombre de réessais qui seront effectués pendant le scan.|

Encore une fois, nous constatons que l'accélération peut également avoir un effet négatif sur nos résultats, ce qui signifie que nous pouvons passer à côté d'informations importantes.

---

## Débits

Lors d'un test d'intrusion en boîte blanche (white-box penetration test), il se peut que nous soyons mis sur liste blanche (whitelisted) par les systèmes de sécurité pour vérifier les vulnérabilités des systèmes du réseau et pas seulement pour tester les mesures de protection. Si nous connaissons la bande passante du réseau, nous pouvons jouer sur le débit des paquets envoyés, ce qui accélère considérablement nos scans avec `Nmap`. En définissant le débit minimum (`--min-rate <number>`) pour l'envoi de paquets, nous demandons à `Nmap` d'envoyer simultanément le nombre de paquets spécifié. Il essaiera de maintenir ce débit en conséquence.

#### Scan par Défaut

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.0/24 -F -oN tnet.default

<SNIP>
Nmap done: 256 IP addresses (10 hosts up) scanned in 29.83 seconds
```

#### Scan Optimisé

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.0/24 -F -oN tnet.minrate300 --min-rate 300

<SNIP>
Nmap done: 256 IP addresses (10 hosts up) scanned in 8.67 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.0/24`|Scanne le réseau cible spécifié.|
|`-F`|Scanne les 100 ports les plus courants.|
|`-oN tnet.minrate300`|Sauvegarde les résultats au format normal, dans le fichier du nom spécifié.|
|`--min-rate 300`|Définit le nombre minimum de paquets à envoyer par seconde.|

---

#### Scan par Défaut - Ports Ouverts Trouvés

```bash
Hiterof13@htb[/htb]$ cat tnet.default | grep "/tcp" | wc -l

23
```

#### Scan Optimisé - Ports Ouverts Trouvés

```bash
Hiterof13@htb[/htb]$ cat tnet.minrate300 | grep "/tcp" | wc -l

23
```

---

## Temporisation

Comme de tels réglages ne peuvent pas toujours être optimisés manuellement, comme dans le cas d'un test d'intrusion en boîte noire (black-box penetration test), `Nmap` nous propose six modèles de temporisation (`-T <0-5>`) différents. Ces valeurs (`0-5`) déterminent l'agressivité de nos scans. Cela peut également avoir des effets négatifs si le scan est trop agressif, et les systèmes de sécurité peuvent nous bloquer en raison du trafic réseau produit. Le modèle de temporisation par défaut utilisé lorsque nous n'avons rien défini d'autre est le normal (`-T 3`).

- `-T 0` / `-T paranoid`
- `-T 1` / `-T sneaky`
- `-T 2` / `-T polite`
- `-T 3` / `-T normal`
- `-T 4` / `-T aggressive`
- `-T 5` / `-T insane`

Ces modèles contiennent des options que nous pouvons également définir manuellement, et nous en avons déjà vu certaines. Les développeurs ont déterminé les valeurs définies pour ces modèles en fonction de leurs meilleurs résultats, ce qui nous facilite l'adaptation de nos scans à l'environnement réseau correspondant. Nous pouvons trouver les options exactes utilisées avec leurs valeurs ici : [https://nmap.org/book/performance-timing-templates.html](https://nmap.org/book/performance-timing-templates.html)

#### Scan par Défaut

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.0/24 -F -oN tnet.default

<SNIP>
Nmap done: 256 IP addresses (10 hosts up) scanned in 32.44 seconds
```

#### Scan Insane

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.0/24 -F -oN tnet.T5 -T 5

<SNIP>
Nmap done: 256 IP addresses (10 hosts up) scanned in 18.07 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.0/24`|Scanne le réseau cible spécifié.|
|`-F`|Scanne les 100 ports les plus courants.|
|`-oN tnet.T5`|Sauvegarde les résultats au format normal, dans le fichier du nom spécifié.|
|`-T 5`|Spécifie le modèle de temporisation insane.|

---

#### Scan par Défaut - Ports Ouverts Trouvés

```bash
Hiterof13@htb[/htb]$ cat tnet.default | grep "/tcp" | wc -l

23
```

#### Scan Insane - Ports Ouverts Trouvés

```bash
Hiterof13@htb[/htb]$ cat tnet.T5 | grep "/tcp" | wc -l

23
```

---

Vous trouverez plus d'informations sur les performances des scans à l'adresse [https://nmap.org/book/man-performance.html](https://nmap.org/book/man-performance.html)
---

← [[07 - Moteur de Scripts de Nmap]] | [[00 - Sommaire Nmap|Sommaire]] | [[09 - Évasion de Pare-feu et d'IDS-IPS]] →
