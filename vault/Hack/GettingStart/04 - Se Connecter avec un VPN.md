---
tags:
  - getting-started
ordre: 4
---

# Se Connecter avec un VPN

---

Un [réseau privé virtuel (VPN)](https://fr.wikipedia.org/wiki/R%C3%A9seau_priv%C3%A9_virtuel) nous permet de nous connecter à un réseau privé (interne) et d'accéder à des hôtes et des ressources comme si nous étions directement connectés au réseau privé cible. Il s'agit d'un canal de communication sécurisé sur des réseaux publics partagés pour se connecter à un réseau privé (par exemple, un employé se connectant à distance au réseau d'entreprise de sa société depuis son domicile). Les VPN offrent un certain degré de confidentialité et de sécurité en chiffrant les communications sur le canal pour empêcher l'écoute clandestine (eavesdropping) et l'accès aux données qui y transitent.

![Schéma réseau montrant Internet, un Pare-feu, un Serveur VPN, un LAN d'entreprise, des Serveurs d'entreprise, des Ordinateurs de bureau et un Utilisateur à distance.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/GettingStarted.png)

À un niveau général, un VPN fonctionne en acheminant la connexion Internet de notre appareil via le serveur privé du VPN cible plutôt que par notre fournisseur d'accès à Internet (FAI). Lorsque l'on est connecté à un VPN, les données proviennent du serveur VPN plutôt que de notre ordinateur et sembleront provenir d'une adresse IP publique autre que la nôtre.

Il existe deux principaux types de VPN d'accès à distance : le VPN basé sur un client et le VPN SSL. Le VPN SSL utilise le navigateur web comme client VPN. La connexion est établie entre le navigateur et une passerelle VPN SSL qui peut être configurée pour n'autoriser l'accès qu'à des applications web telles que la messagerie électronique et les sites intranet, ou même au réseau interne, mais sans que l'utilisateur final n'ait besoin d'installer ou d'utiliser un logiciel spécialisé. Le VPN basé sur un client nécessite l'utilisation d'un logiciel client pour établir la connexion VPN. Une fois connecté, l'hôte de l'utilisateur fonctionnera presque comme s'il était directement connecté au réseau de l'entreprise et pourra accéder à toutes les ressources (applications, hôtes, sous-réseaux, etc.) autorisées par la configuration du serveur. Certains VPN d'entreprise fourniront aux employés un accès complet au réseau interne de l'entreprise, tandis que d'autres placeront les utilisateurs sur un segment spécifique réservé aux travailleurs à distance.

---

## Pourquoi Utiliser un VPN ?

Nous pouvons utiliser un service VPN tel que `NordVPN` ou `Private Internet Access` et nous connecter à un serveur VPN dans une autre partie de notre pays ou une autre région du monde pour masquer notre trafic de navigation ou déguiser notre adresse IP publique. Cela peut nous fournir un certain niveau de sécurité et de confidentialité. Cependant, comme nous nous connectons au serveur d'une entreprise, il y a toujours un risque que les données soient enregistrées ou que le service VPN ne suive pas les meilleures pratiques de sécurité ou les fonctionnalités de sécurité qu'il annonce. L'utilisation d'un service VPN comporte le risque que le fournisseur ne fasse pas ce qu'il prétend et enregistre toutes les données. L'utilisation d'un service VPN **ne garantit pas** l'anonymat ou la confidentialité, mais elle est utile pour contourner certaines restrictions de réseau/pare-feu ou lorsqu'on est connecté à un réseau potentiellement hostile (par exemple, un réseau sans fil public d'un aéroport). Un service VPN ne doit jamais être utilisé en pensant qu'il nous protégera des conséquences d'activités malveillantes.

---

## Se Connecter au VPN HTB

HTB et d'autres services offrant des VM/réseaux volontairement vulnérables exigent que les joueurs se connectent au réseau cible via un VPN pour accéder au réseau du laboratoire privé. Les hôtes au sein des réseaux HTB ne peuvent pas se connecter directement à Internet. Lorsque l'on est connecté au VPN HTB (ou à tout laboratoire axé sur les tests d'intrusion/le hacking), nous devrions toujours considérer le réseau comme « hostile ». Nous ne devrions nous connecter qu'à partir d'une machine virtuelle, refuser l'authentification par mot de passe si SSH est activé sur notre VM d'attaque, verrouiller tous les serveurs web et ne pas laisser d'informations sensibles sur notre VM d'attaque (c'est-à-dire ne pas jouer sur HTB ou d'autres réseaux vulnérables avec la même VM que nous utilisons pour effectuer des évaluations pour des clients). Pour se connecter à un VPN (que ce soit sur HTB Academy ou la plateforme principale de HTB), nous utilisons la commande suivante :

```bash
Hiterof13@htb[/htb]$ sudo openvpn user.ovpn  Thu Dec 10 18:42:41 2020 OpenVPN 2.4.9 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Apr 21 2020 Thu Dec 10 18:42:41 2020 library versions: OpenSSL 1.1.1g  21 Apr 2020, LZO 2.10 Thu Dec 10 18:42:41 2020 Outgoing Control Channel Authentication: Using 256 bit message hash 'SHA256' for HMAC authentication Thu Dec 10 18:42:41 2020 Incoming Control Channel Authentication: Using 256 bit message hash 'SHA256' for HMAC authentication Thu Dec 10 18:42:41 2020 TCP/UDP: Preserving recently used remote address: [AF_INET] Thu Dec 10 18:42:41 2020 Socket Buffers: R=[212992->212992] S=[212992->212992] Thu Dec 10 18:42:41 2020 UDP link local: (not bound) <SNIP> Thu Dec 10 18:42:41 2020 Initialization Sequence Completed
```

La dernière ligne `Initialization Sequence Completed` nous indique que nous nous sommes connectés avec succès au VPN.

Où `sudo` indique à notre hôte d'exécuter la commande en tant qu'utilisateur root avec des privilèges élevés, `openvpn` est le client VPN, et le fichier `user.ovpn` est la clé VPN que nous téléchargeons depuis la section du module Academy ou depuis la plateforme principale de HTB. Si nous tapons `ifconfig` dans une autre fenêtre de terminal, nous verrons un adaptateur `tun` si nous nous sommes connectés avec succès au VPN.

```bash
Hiterof13@htb[/htb]$ ifconfig  <SNIP>  tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500         inet 10.10.x.2  netmask 255.255.254.0  destination 10.10.x.2         inet6 dead:beef:1::2000  prefixlen 64  scopeid 0x0<global>         inet6 fe80::d82f:301a:a94a:8723  prefixlen 64  scopeid 0x20<link>         unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen
```

Taper `netstat -rn` nous montrera les réseaux accessibles via le VPN.

```bash
Hiterof13@htb[/htb]$ netstat -rn  Kernel IP routing table Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface 0.0.0.0         192.168.1.2     0.0.0.0         UG        0 0          0 eth0 10.10.14.0      0.0.0.0         255.255.254.0   U         0 0          0 tun0 10.129.0.0      10.10.14.1      255.255.0.0     UG        0 0          0 tun0 192.168.1.0     0.0.0.0         255.255.255.0   U         0 0          0 eth0
```

Ici, nous pouvons voir que le réseau 10.129.0.0/16 utilisé pour les machines de HTB Academy est accessible via l'adaptateur `tun0` par le biais du réseau 10.10.14.0/23.

---

## Aide avec le VPN

Si c'est la première fois que vous utilisez un VPN, les ressources suivantes sur le portail d'assistance de Hack The Box vous seront utiles :

- [Introduction à l'Accès au Lab](https://help.hackthebox.com/en/articles/5185687-gs-introduction-to-lab-access)
- [Dépannage de la Connexion](https://help.hackthebox.com/en/articles/5185536-t-connection-troubleshooting)
---

← [[03 - Rester Organisé]] | [[00 - Sommaire Getting Started|Sommaire]] | [[05 - Termes Courants]] →
