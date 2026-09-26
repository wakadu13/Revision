---
tags:
  - nmap
ordre: 5
---

# Sauvegarde des Résultats

---

## Différents Formats

Lorsque nous effectuons divers scans, nous devrions toujours sauvegarder les résultats. Nous pourrons les utiliser ultérieurement pour examiner les différences entre les différentes méthodes de scan que nous avons utilisées. `Nmap` peut sauvegarder les résultats dans 3 formats différents.

- Sortie normale (Normal output) (`-oN`) avec l'extension de fichier `.nmap`
- Sortie compatible avec grep (Grepable output) (`-oG`) avec l'extension de fichier `.gnmap`
- Sortie XML (XML output) (`-oX`) avec l'extension de fichier `.xml`

Nous pouvons également spécifier l'option (`-oA`) pour sauvegarder les résultats dans tous les formats. La commande pourrait ressembler à ceci :

```bash
Hiterof13@htb[/htb]$ sudo nmap 10.129.2.28 -p- -oA target

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-16 12:14 CEST
Nmap scan report for 10.129.2.28
Host is up (0.0091s latency).
Not shown: 65525 closed ports
PORT      STATE SERVICE
22/tcp    open  ssh
25/tcp    open  smtp
80/tcp    open  http
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

Nmap done: 1 IP address (1 host up) scanned in 10.22 seconds
```

|**Options de Scan**|**Description**|
|---|---|
|`10.129.2.28`|Scanne la cible spécifiée.|
|`-p-`|Scanne tous les ports.|
|`-oA target`|Sauvegarde les résultats dans tous les formats, en faisant commencer le nom de chaque fichier par 'target'.|

Si aucun chemin complet n'est fourni, les résultats seront stockés dans le répertoire où nous nous trouvons actuellement. Ensuite, nous allons examiner les différents formats que `Nmap` a créés pour nous.

```bash
Hiterof13@htb[/htb]$ ls

target.gnmap target.xml  target.nmap
```

#### Sortie Normale

```bash
Hiterof13@htb[/htb]$ cat target.nmap

# Nmap 7.80 scan initiated Tue Jun 16 12:14:53 2020 as: nmap -p- -oA target 10.129.2.28
Nmap scan report for 10.129.2.28
Host is up (0.053s latency).
Not shown: 4 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
25/tcp open  smtp
80/tcp open  http
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

# Nmap done at Tue Jun 16 12:15:03 2020 -- 1 IP address (1 host up) scanned in 10.22 seconds
```

#### Sortie Compatible avec grep

```bash
Hiterof13@htb[/htb]$ cat target.gnmap

# Nmap 7.80 scan initiated Tue Jun 16 12:14:53 2020 as: nmap -p- -oA target 10.129.2.28
Host: 10.129.2.28 ()    Status: Up
Host: 10.129.2.28 ()    Ports: 22/open/tcp//ssh///, 25/open/tcp//smtp///, 80/open/tcp//http///  Ignored State: closed (4)
# Nmap done at Tue Jun 16 12:14:53 2020 -- 1 IP address (1 host up) scanned in 10.22 seconds
```

#### Sortie XML

```bash
Hiterof13@htb[/htb]$ cat target.xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE nmaprun>
<?xml-stylesheet href="file:///usr/local/bin/../share/nmap/nmap.xsl" type="text/xsl"?>
<!-- Nmap 7.80 scan initiated Tue Jun 16 12:14:53 2020 as: nmap -p- -oA target 10.129.2.28 -->
<nmaprun scanner="nmap" args="nmap -p- -oA target 10.129.2.28" start="12145301719" startstr="Tue Jun 16 12:15:03 2020" version="7.80" xmloutputversion="1.04">
<scaninfo type="syn" protocol="tcp" numservices="65535" services="1-65535"/>
<verbose level="0"/>
<debugging level="0"/>
<host starttime="12145301719" endtime="12150323493"><status state="up" reason="arp-response" reason_ttl="0"/>
<address addr="10.129.2.28" addrtype="ipv4"/>
<address addr="DE:AD:00:00:BE:EF" addrtype="mac" vendor="Intel Corporate"/>
<hostnames>
</hostnames>
<ports><extraports state="closed" count="4">
<extrareasons reason="resets" count="4"/>
</extraports>
<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="ssh" method="table" conf="3"/></port>
<port protocol="tcp" portid="25"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="smtp" method="table" conf="3"/></port>
<port protocol="tcp" portid="80"><state state="open" reason="syn-ack" reason_ttl="64"/><service name="http" method="table" conf="3"/></port>
</ports>
<times srtt="52614" rttvar="75640" to="355174"/>
</host>
<runstats><finished time="12150323493" timestr="Tue Jun 16 12:14:53 2020" elapsed="10.22" summary="Nmap done at Tue Jun 16 12:15:03 2020; 1 IP address (1 host up) scanned in 10.22 seconds" exit="success"/><hosts up="1" down="0" total="1"/>
</runstats>
</nmaprun>
```

---

## Feuilles de style

Avec la sortie XML, nous pouvons facilement créer des rapports HTML faciles à lire, même pour les personnes non techniques. C'est très utile par la suite pour la documentation, car cela présente nos résultats de manière détaillée et claire. Pour convertir les résultats stockés du format XML au format HTML, nous pouvons utiliser l'outil `xsltproc`.

```bash
Hiterof13@htb[/htb]$ xsltproc target.xml -o target.html
```

Si nous ouvrons maintenant le fichier HTML dans notre navigateur, nous voyons une présentation claire et structurée de nos résultats.

#### Rapport Nmap

![Rapport de scan Nmap pour l'IP 10.10.10.28 montrant les ports ouverts : 22 (SSH), 25 (SMTP), 80 (HTTP). Scanné le 16 juin 2020.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/19/nmap-report.png)

Plus d'informations sur les formats de sortie sont disponibles à l'adresse suivante : [https://nmap.org/book/output.html](https://nmap.org/book/output.html)
---

← [[04 - Scan d'hôtes et de ports]] | [[00 - Sommaire Nmap|Sommaire]] | [[06 - Énumération des services]] →
