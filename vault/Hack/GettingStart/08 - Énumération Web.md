---
tags:
  - getting-started
ordre: 8
---

# Énumération Web

---

Lors d'un scan de services, nous tomberons souvent sur des serveurs web fonctionnant sur les ports 80 et 443. Les serveurs web hébergent des applications web (parfois plus d'une) qui offrent souvent une surface d'attaque considérable et une cible de très grande valeur lors d'un test d'intrusion (penetration test). Une énumération web appropriée est essentielle, surtout lorsqu'une organisation n'expose pas beaucoup de services ou que ces services sont correctement patchés.

---

## Gobuster

Après avoir découvert une application web, il est toujours utile de vérifier si nous pouvons découvrir des fichiers ou des répertoires cachés sur le serveur web qui ne sont pas destinés à un accès public. Nous pouvons utiliser un outil tel que [ffuf](https://github.com/ffuf/ffuf) ou [GoBuster](https://github.com/OJ/gobuster) pour effectuer cette énumération de répertoires. Parfois, nous trouverons des fonctionnalités cachées ou des pages/répertoires exposant des données sensibles qui peuvent être exploitées pour accéder à l'application web ou même obtenir une exécution de code à distance (remote code execution) sur le serveur web lui-même.

#### Énumération de Répertoires/Fichiers

GoBuster est un outil polyvalent qui permet d'effectuer du brute-force de DNS, de vhost et de répertoires. L'outil dispose de fonctionnalités supplémentaires, telles que l'énumération de buckets S3 publics d'AWS. Pour les besoins de ce module, nous nous intéressons aux modes de brute-force de répertoires (et de fichiers) spécifiés avec l'option `dir`. Lançons un scan simple en utilisant la liste de mots (wordlist) `common.txt` de `dirb`.

```bash
Hiterof13@htb[/htb]$ gobuster dir -u http://10.10.10.121/ -w /usr/share/seclists/Discovery/Web-Content/common.txt
=============================================================== Gobuster v3.0.1 by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.10.121/
[+] Threads:        10
[+] Wordlist:       /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/12/11 21:47:25 Starting gobuster
===============================================================
/.hta (Status: 403)
/.htpasswd (Status: 403)
/.htaccess (Status: 403)
/index.php (Status: 200)
/server-status (Status: 403)
/wordpress (Status: 301)
===============================================================
2020/12/11 21:47:46 Finished
===============================================================
```

Un code de statut HTTP `200` révèle que la requête de la ressource a réussi, tandis qu'un code de statut HTTP 403 indique que nous n'avons pas l'autorisation d'accéder à la ressource. Un code de statut 301 indique que nous sommes redirigés, ce qui n'est pas un cas d'échec. Il est utile de se familiariser avec les différents codes de statut HTTP, que l'on peut trouver [ici](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). Le module de l'Académie `Web Requests` couvre également les codes de statut HTTP de manière plus approfondie.

Le scan s'est terminé avec succès et identifie une installation WordPress sur `/wordpress`. WordPress est le CMS (Système de Gestion de Contenu) le plus utilisé et possède une surface d'attaque potentielle énorme. Dans ce cas, visiter `http://10.10.10.121/wordpress` dans un navigateur révèle que WordPress est encore en mode de configuration, ce qui nous permettra d'obtenir une exécution de code à distance (RCE) sur le serveur.

![Écran de sélection de la langue de WordPress avec une liste de langues et un bouton 'Continuer'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/wordpress.png)

#### Énumération de Sous-domaines DNS

Il peut également y avoir des ressources essentielles hébergées sur des sous-domaines, comme des panneaux d'administration ou des applications avec des fonctionnalités supplémentaires qui pourraient être exploitées. Nous pouvons utiliser `GoBuster` pour énumérer les sous-domaines disponibles d'un domaine donné en utilisant l'option `dns` pour spécifier le mode DNS. D'abord, clonons le [dépôt](https://github.com/danielmiessler/SecLists) GitHub de SecLists, qui contient de nombreuses listes utiles pour le fuzzing et l'exploitation :

#### Installer SecLists

```bash
Hiterof13@htb[/htb]$ git clone https://github.com/danielmiessler/SecLists
```

```bash
Hiterof13@htb[/htb]$ sudo apt install seclists -y
```

Ensuite, ajoutez un serveur DNS tel que 1.1.1.1 au fichier `/etc/resolv.conf`. Nous ciblerons le domaine `inlanefreight.com`, le site web d'une entreprise fictive de fret et de logistique.

```bash
Hiterof13@htb[/htb]$ gobuster dns -d inlanefreight.com -w /usr/share/SecLists/Discovery/DNS/namelist.txt
=============================================================== Gobuster v3.0.1 by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Domain:     inlanefreight.com
[+] Threads:    10
[+] Timeout:    1s
[+] Wordlist:   /usr/share/SecLists/Discovery/DNS/namelist.txt
===============================================================
2020/12/17 23:08:55 Starting gobuster
===============================================================
Found: blog.inlanefreight.com
Found: customer.inlanefreight.com
Found: my.inlanefreight.com
Found: ns1.inlanefreight.com
Found: ns2.inlanefreight.com
Found: ns3.inlanefreight.com
===============================================================
2020/12/17 23:10:34 Finished
===============================================================
```

Ce scan révèle plusieurs sous-domaines intéressants que nous pourrions examiner plus en détail. Le module [Attacking Web Applications with Ffuf](https://academy.hackthebox.com/module/details/54) approfondit l'énumération web et le fuzzing.

---

## Astuces pour l'Énumération Web

Passons en revue quelques astuces supplémentaires pour l'énumération web qui vous aideront à terminer des machines sur HTB et dans le monde réel.

#### Capture de Bannière / En-têtes de Serveur Web

Dans la section précédente, nous avons parlé de la capture de bannière (banner grabbing) à des fins générales. Les en-têtes de serveur web donnent une bonne image de ce qui est hébergé sur un serveur web. Ils peuvent révéler le framework d'application spécifique utilisé, les options d'authentification, et si le serveur manque d'options de sécurité essentielles ou a été mal configuré. Nous pouvons utiliser `cURL` pour récupérer les informations d'en-tête du serveur depuis la ligne de commande. `cURL` est un autre ajout essentiel à notre boîte à outils de test d'intrusion, et il est recommandé de se familiariser avec ses nombreuses options.

```bash
Hiterof13@htb[/htb]$ curl -IL https://www.inlanefreight.com  HTTP/1.1 200 OK Date: Fri, 18 Dec 2020 22:24:05 GMT Server: Apache/2.4.29 (Ubuntu) Link: <https://www.inlanefreight.com/index.php/wp-json/>; rel="https://api.w.org/" Link: <https://www.inlanefreight.com/>; rel=shortlink Content-Type: text/html; charset=UTF-8
```

Un autre outil pratique est [EyeWitness](https://github.com/FortyNorthSecurity/EyeWitness), qui peut être utilisé pour prendre des captures d'écran des applications web cibles, prendre leur empreinte (fingerprint) et identifier d'éventuels identifiants par défaut.

#### Whatweb

Nous pouvons extraire la version des serveurs web, des frameworks et des applications pris en charge à l'aide de l'outil en ligne de commande `whatweb`. Ces informations peuvent nous aider à identifier les technologies utilisées et à commencer à rechercher des vulnérabilités potentielles.

```bash
Hiterof13@htb[/htb]$ whatweb 10.10.10.121  http://10.10.10.121 [200 OK] Apache[2.4.41], Country[RESERVED][ZZ], Email[license@php.net], HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.10.10.121], Title[PHP 7.4.3 - phpinfo()]
```

`Whatweb` est un outil pratique qui contient de nombreuses fonctionnalités pour automatiser l'énumération d'applications web sur un réseau.

```bash
Hiterof13@htb[/htb]$ whatweb --no-errors 10.10.10.0/24  http://10.10.10.11 [200 OK] Country[RESERVED][ZZ], HTTPServer[nginx/1.14.1], IP[10.10.10.11], PoweredBy[Red,nginx], Title[Test Page for the Nginx HTTP Server on Red Hat Enterprise Linux], nginx[1.14.1] http://10.10.10.100 [200 OK] Apache[2.4.41], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.10.10.100], Title[File Sharing Service] http://10.10.10.121 [200 OK] Apache[2.4.41], Country[RESERVED][ZZ], Email[license@php.net], HTTPServer[Ubuntu Linux][Apache/2.4.41 (Ubuntu)], IP[10.10.10.121], Title[PHP 7.4.3 - phpinfo()] http://10.10.10.247 [200 OK] Bootstrap, Country[RESERVED][ZZ], Email[contact@cross-fit.htb], Frame, HTML5, HTTPServer[OpenBSD httpd], IP[10.10.10.247], JQuery[3.3.1], PHP[7.4.12], Script, Title[Fine Wines], X-Powered-By[PHP/7.4.12], X-UA-Compatible[ie=edge]
```

#### Certificats

Les certificats SSL/TLS sont une autre source d'informations potentiellement précieuse si HTTPS est utilisé. En naviguant vers `https://10.10.10.121/` et en consultant le certificat, on découvre les détails ci-dessous, y compris l'adresse e-mail et le nom de l'entreprise. Ceux-ci pourraient potentiellement être utilisés pour mener une attaque d'hameçonnage (phishing) si cela entre dans le cadre d'une évaluation.

![Détails du certificat pour Megabank Limited, incluant les informations sur le sujet et l'émetteur avec le pays, l'état, la localité, l'organisation et l'adresse e-mail.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/cert.png)

#### Robots.txt

Il est courant que les sites web contiennent un fichier `robots.txt`, dont le but est d'indiquer aux robots d'indexation des moteurs de recherche, comme Googlebot, quelles ressources peuvent ou ne peuvent pas être consultées pour l'indexation. Le fichier `robots.txt` peut fournir des informations précieuses telles que l'emplacement de fichiers privés et de pages d'administration. Dans ce cas, nous voyons que le fichier `robots.txt` contient deux entrées non autorisées (disallowed).

![Fichier Robots.txt interdisant l'accès à /private et /uploaded_files pour tous les user agents.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/robots.png)

Naviguer vers `http://10.10.10.121/private` dans un navigateur révèle une page de connexion administrateur HTB.

![Formulaire de connexion avec des champs pour le nom d'utilisateur et le mot de passe, et un bouton de connexion.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/academy.png)

#### Code Source

Il est également utile de vérifier le code source de toutes les pages web que nous rencontrons. Nous pouvons appuyer sur `[CTRL + U]` pour afficher la fenêtre du code source dans un navigateur. Cet exemple révèle un commentaire de développeur contenant des identifiants pour un compte de test, qui pourraient être utilisés pour se connecter au site web.

![Extrait HTML avec des identifiants de compte de test, des balises meta et un titre de connexion administrateur.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/source.png)
---

← [[07 - Analyse de services]] | [[00 - Sommaire Getting Started|Sommaire]] | [[09 - Exploits Publics]] →
