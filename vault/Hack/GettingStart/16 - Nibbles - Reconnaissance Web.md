---
tags:
  - getting-started
ordre: 16
---

# Nibbles - Reconnaissance Web

---

Nous pouvons utiliser `whatweb` pour essayer d'identifier l'application web utilisée.

```bash
Hiterof13@htb[/htb]$ whatweb 10.129.42.190  http://10.129.42.190 [200 OK] Apache[2.4.18], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.18 (Ubuntu)], IP[10.129.42.190]
```

Cet outil n'identifie aucune technologie web standard en cours d'utilisation. En naviguant vers la cible dans `Firefox`, nous voyons un simple message « Hello world! ».

![Texte 'Hello world!' affiché sur un fond blanc.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/nibbles_hello2.png)

La consultation du code source de la page révèle un commentaire intéressant.

![Extrait de code HTML avec 'Hello world!' en gras et un commentaire sur le répertoire /nibbleblog/.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/nibbles_comment1.png)

Nous pouvons également vérifier cela avec cURL.

```bash
Hiterof13@htb[/htb]$ curl http://10.129.42.190  <b>Hello world!</b>  <!-- /nibbleblog/ directory. Nothing interesting here! -->
```

Le commentaire HTML mentionne un répertoire nommé `nibbleblog`. Vérifions cela avec `whatweb`.

```bash
Hiterof13@htb[/htb]$ whatweb http://10.129.42.190/nibbleblog  http://10.129.42.190/nibbleblog [301 Moved Permanently] Apache[2.4.18], Country[RESERVED][ZZ], HTTPServer[Ubuntu Linux][Apache/2.4.18 (Ubuntu)], IP[10.129.42.190], RedirectLocation[http://10.129.42.190/nibbleblog/], Title[301 Moved Permanently] http://10.129.42.190/nibbleblog/ [200 OK] Apache[2.4.18], Cookies[PHPSESSID], Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][Apache/2.4.18 (Ubuntu)], IP[10.129.42.190], JQuery, MetaGenerator[Nibbleblog], PoweredBy[Nibbleblog], Script, Title[Nibbles - Yum yum]
```

Maintenant, nous commençons à avoir une meilleure idée de la situation. Nous pouvons voir certaines des technologies utilisées telles que [HTML5](https://en.wikipedia.org/wiki/HTML5), [jQuery](https://en.wikipedia.org/wiki/JQuery) et [PHP](https://en.wikipedia.org/wiki/PHP). Nous pouvons également voir que le site exécute [Nibbleblog](https://www.nibbleblog.com/), qui est un moteur de blog gratuit développé en PHP.

---

## Énumération de Répertoires

En naviguant vers le répertoire `/nibbleblog` dans `Firefox`, nous ne voyons rien d'excitant sur la page principale.

![Page de blog intitulée 'Nibbles Yum yum' sans aucun article, ni catégorie, et avec des liens vers 'Home' et 'Powered by Nibbleblog'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/yumyum_.png)

Une recherche rapide sur Google pour « nibbleblog exploit » donne cette [Vulnérabilité de téléversement de fichier de Nibbleblog (Nibbleblog File Upload Vulnerability)](https://www.rapid7.com/db/modules/exploit/multi/http/nibbleblog_file_upload/). La faille permet à un attaquant authentifié de téléverser et d'exécuter du code PHP arbitraire sur le serveur web sous-jacent. Le module `Metasploit` en question fonctionne pour la version `4.0.3`. Nous ne connaissons pas encore la version exacte de `Nibbleblog` utilisée, mais il y a de fortes chances qu'elle soit vulnérable à cela. Si nous examinons le code source du module `Metasploit`, nous pouvons voir que l'exploit utilise des identifiants fournis par l'utilisateur pour s'authentifier sur le portail d'administration à l'adresse `/admin.php`.

Utilisons [Gobuster](https://github.com/OJ/gobuster) pour être exhaustif et vérifier l'existence d'autres pages/répertoires accessibles.

```bash
Hiterof13@htb[/htb]$ gobuster dir -u http://10.129.42.190/nibbleblog/ --wordlist /usr/share/seclists/Discovery/Web-Content/common.txt
===============================================================  Gobuster v3.0.1  by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.129.42.190/nibbleblog/
[+] Threads:        10
[+] Wordlist:       /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/12/17 00:10:47 Starting gobuster
===============================================================
/.hta (Status: 403)
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/admin (Status: 301)
/admin.php (Status: 200)
/content (Status: 301)
/index.php (Status: 200)
/languages (Status: 301)
/plugins (Status: 301)
/README (Status: 200)
/themes (Status: 301)
===============================================================
2020/12/17 00:11:38 Finished
===============================================================
```

`Gobuster` termine très rapidement et confirme la présence de la page `admin.php`. Nous pouvons vérifier la page `README` pour des informations intéressantes, comme le numéro de version.

```bash
Hiterof13@htb[/htb]$ curl http://10.129.42.190/nibbleblog/README
====== Nibbleblog
====== Version: v4.0.3 Codename: Coffee Release date: 2014-04-01  Site: http://www.nibbleblog.com Blog: http://blog.nibbleblog.com Help & Support: http://forum.nibbleblog.com Documentation: http://docs.nibbleblog.com
===== Social
=====  * Twitter: http://twitter.com/nibbleblog * Facebook: http://www.facebook.com/nibbleblog * Google+: http://google.com/+nibbleblog
===== System Requirements
=====  * PHP v5.2 or higher * PHP module - DOM * PHP module - SimpleXML * PHP module - GD * Directory “content” writable by Apache/PHP  <SNIP>
```

Nous validons donc que la version 4.0.3 est utilisée, confirmant que cette version est probablement vulnérable au module `Metasploit` (bien que cela puisse être une ancienne page `README`). Rien d'autre d'intéressant ne saute aux yeux. Allons voir la page de connexion du portail d'administration.

![Formulaire de connexion pour la zone d'administration de Nibbleblog avec des champs pour le nom d'utilisateur, le mot de passe, une case à cocher 'Se souvenir de moi' et un lien 'Retour au blog'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/nibble_admin.png)

Maintenant, pour utiliser l'exploit mentionné ci-dessus, nous aurons besoin d'identifiants administrateur valides. Nous pouvons essayer manuellement quelques techniques de contournement d'autorisation et des paires d'identifiants courantes, comme `admin:admin` et `admin:password`, sans succès. Il existe une fonction de réinitialisation de mot de passe, mais nous recevons une erreur d'e-mail. De plus, trop de tentatives de connexion trop rapides déclenchent un verrouillage avec le message `Nibbleblog security error - Blacklist protection`.

Revenons à nos résultats de force brute de répertoires. Les codes de statut `200` montrent les pages/répertoires qui sont directement accessibles. Les codes de statut `403` dans la sortie indiquent que l'accès à ces ressources est interdit. Enfin, le `301` est une redirection permanente. Explorons chacune d'entre elles. En naviguant vers `nibbleblog/themes/`, nous pouvons voir que le listage de répertoire est activé sur l'application web. Peut-être pourrons-nous trouver quelque chose d'intéressant en fouillant ?

![Listage du répertoire /nibbleblog/themes avec les dossiers : echo, medium, note-2, simpler, techie.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/nibbles_dir_listing.png)

La navigation vers `nibbleblog/content` montre des sous-répertoires intéressants `public`, `private` et `tmp`. En fouillant un peu, nous trouvons un fichier `users.xml` qui semble au moins confirmer que le nom d'utilisateur est bien admin. Il montre également des adresses IP sur liste noire. Nous pouvons demander ce fichier avec `cURL` et embellir la sortie `XML` en utilisant [xmllint](https://linux.die.net/man/1/xmllint).

```bash
Hiterof13@htb[/htb]$ curl -s http://10.129.42.190/nibbleblog/content/private/users.xml
| xmllint  --format -
<?xml version="1.0" encoding="UTF-8" standalone="yes"?> <users>   <user username="admin">     <id type="integer">0</id>     <session_fail_count type="integer">2</session_fail_count>     <session_date type="integer">1608182184</session_date>   </user>   <blacklist type="string" ip="10.10.10.1">     <date type="integer">1512964659</date>     <fail_count type="integer">1</fail_count>   </blacklist>   <blacklist type="string" ip="10.10.14.2">     <date type="integer">1608182171</date>     <fail_count type="integer">5</fail_count>   </blacklist> </users>
```

À ce stade, nous avons un nom d'utilisateur valide mais pas de mot de passe. Les recherches dans la documentation relative à Nibbleblog montrent que le mot de passe est défini lors de l'installation et qu'il n'y a pas de mot de passe par défaut connu. Jusqu'à présent, nous avons les pièces suivantes du puzzle :

- Une installation de Nibbleblog potentiellement vulnérable à une vulnérabilité de téléversement de fichier authentifiée
- Un portail d'administration à `nibbleblog/admin.php`
- Le listage de répertoire qui a confirmé que `admin` est un nom d'utilisateur valide
- La protection contre la force brute des identifiants met notre adresse IP sur liste noire (blacklists) après trop de tentatives de connexion infructueuses. Cela rend impossible l'attaque par force brute sur la connexion avec un outil tel que [Hydra](https://github.com/vanhauser-thc/thc-hydra)

Il n'y a pas d'autres ports ouverts, et nous n'avons pas trouvé d'autres répertoires. Ce que nous pouvons confirmer en effectuant une autre attaque par force brute de répertoires contre la racine de l'application web.

```bash
Hiterof13@htb[/htb]$ gobuster dir -u http://10.129.42.190/ --wordlist /usr/share/seclists/Discovery/Web-Content/common.txt
=============================================================== Gobuster v3.0.1 by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.129.42.190/
[+] Threads:        10
[+] Wordlist:       /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/12/17 00:36:55 Starting gobuster
===============================================================
/.hta (Status: 403)
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/index.html (Status: 200)
/server-status (Status: 403)
===============================================================
2020/12/17 00:37:46 Finished
===============================================================
```

En examinant à nouveau tous les répertoires exposés, nous trouvons un fichier `config.xml`.

```bash
Hiterof13@htb[/htb]$ curl -s http://10.129.42.190/nibbleblog/content/private/config.xml
| xmllint --format -
<?xml version="1.0" encoding="utf-8" standalone="yes"?> <config>   <name type="string">Nibbles</name>   <slogan type="string">Yum yum</slogan>   <footer type="string">Powered by Nibbleblog</footer>   <advanced_post_options type="integer">0</advanced_post_options>   <url type="string">http://10.129.42.190/nibbleblog/</url>   <path type="string">/nibbleblog/</path>   <items_rss type="integer">4</items_rss>   <items_page type="integer">6</items_page>   <language type="string">en_US</language>   <timezone type="string">UTC</timezone>   <timestamp_format type="string">%d %B, %Y</timestamp_format>   <locale type="string">en_US</locale>   <img_resize type="integer">1</img_resize>   <img_resize_width type="integer">1000</img_resize_width>   <img_resize_height type="integer">600</img_resize_height>   <img_resize_quality type="integer">100</img_resize_quality>   <img_resize_option type="string">auto</img_resize_option>   <img_thumbnail type="integer">1</img_thumbnail>   <img_thumbnail_width type="integer">190</img_thumbnail_width>   <img_thumbnail_height type="integer">190</img_thumbnail_height>   <img_thumbnail_quality type="integer">100</img_thumbnail_quality>   <img_thumbnail_option type="string">landscape</img_thumbnail_option>   <theme type="string">simpler</theme>   <notification_comments type="integer">1</notification_comments>   <notification_session_fail type="integer">0</notification_session_fail>   <notification_session_start type="integer">0</notification_session_start>   <notification_email_to type="string">admin@nibbles.com</notification_email_to>   <notification_email_from type="string">noreply@10.10.10.134</notification_email_from>   <seo_site_title type="string">Nibbles - Yum yum</seo_site_title>   <seo_site_description type="string"/>   <seo_keywords type="string"/>   <seo_robots type="string"/>   <seo_google_code type="string"/>   <seo_bing_code type="string"/>   <seo_author type="string"/>   <friendly_urls type="integer">0</friendly_urls>   <default_homepage type="integer">0</default_homepage> </config>
```

En le vérifiant, dans l'espoir de trouver des mots de passe, s'avère infructueux, mais nous voyons deux mentions de `nibbles` dans le titre du site ainsi que dans l'adresse e-mail de notification. C'est aussi le nom de la machine. Serait-ce le mot de passe administrateur ?

Lorsqu'on effectue un cassage de mot de passe hors ligne (offline password cracking) avec un outil comme `Hashcat` ou qu'on essaie de deviner un mot de passe, il est important de prendre en compte toutes les informations dont nous disposons. Il n'est pas rare de réussir à casser un hash de mot de passe (comme la phrase de passe d'un réseau sans fil d'entreprise) en utilisant une liste de mots (`wordlist`) générée en parcourant leur site web à l'aide d'un outil tel que [CeWL](https://github.com/digininja/CeWL).

![Tableau de bord de Nibbleblog avec des options pour publier, gérer et des paramètres. Les notifications montrent les démarrages de session et les tentatives de connexion.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/nibbles_loggedin.png)

Cela nous montre à quel point une énumération approfondie est cruciale. Récapitulons ce que nous avons trouvé jusqu'à présent :

- Nous avons commencé par un simple scan `nmap` montrant deux ports ouverts
- Découvert une instance de `Nibbleblog`
- Analysé les technologies utilisées avec `whatweb`
- Trouvé la page du portail de connexion administrateur à `admin.php`
- Découvert que le listage de répertoire est activé et parcouru plusieurs répertoires
- Confirmé que `admin` était le nom d'utilisateur valide
- Découvert à nos dépens que la mise sur liste noire (IP blacklisting) est activée pour empêcher les tentatives de connexion par force brute
- Découvert des indices qui nous ont menés au mot de passe administrateur valide nibbles

Cela prouve que nous avons besoin d'un processus clair et reproductible que nous utiliserons encore et encore, que nous attaquions une seule machine sur HTB, que nous effectuions un test d'intrusion d'application web pour un client, ou que nous attaquions un grand environnement Active Directory. Gardez à l'esprit que l'énumération itérative, ainsi qu'une prise de notes détaillée, est l'une des clés du succès dans ce domaine. Au fur et à mesure que vous progresserez dans votre carrière, vous vous étonnerez souvent de voir à quel point le périmètre initial d'un test d'intrusion semblait extrêmement petit et « ennuyeux », mais une fois que vous creusez et effectuez des cycles d'énumération successifs, en creusant couche après couche, vous pourriez trouver un service exposé sur un port élevé ou une page ou un répertoire oublié qui peut conduire à une exposition de données sensibles ou même à un premier accès (foothold).
---

← [[15 - Nibbles - Énumération]] | [[00 - Sommaire Getting Started|Sommaire]] | [[17 - Nibbles - Prise de contrôle initiale]] →
