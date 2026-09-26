---
tags:
  - linux
ordre: 20
---

# Travailler avec les services web

Un autre élément crucial du développement web est la communication entre les navigateurs et les serveurs web. La configuration d'un serveur web sur un système d'exploitation Linux peut se faire de plusieurs manières, avec des options populaires comme Nginx, IIS et Apache. Parmi celles-ci, Apache est l'un des serveurs web les plus utilisés. Considérez Apache comme le moteur qui alimente votre site web, assurant une communication fluide entre votre site et ses visiteurs.

Nous pouvons également comparer Apache aux fondations et à la structure d'une maison. Tout comme vous pouvez ajouter différentes pièces ou personnaliser des fonctionnalités dans une maison, Apache peut être étendu avec des modules, chacun conçu pour un objectif spécifique, que ce soit pour sécuriser la communication, rediriger le trafic ou façonner dynamiquement le contenu, à la manière d'un architecte d'intérieur qui réaménage les pièces pour répondre à vos besoins.

La véritable force d'Apache réside dans sa modularité : il peut être personnalisé et étendu avec divers modules pour effectuer des tâches spécifiques. Par exemple, `mod_ssl` agit comme un coffre-fort, sécurisant la communication entre le navigateur et le serveur web en chiffrant les données. Le module `mod_proxy` est comme un contrôleur de trafic, dirigeant les requêtes vers la bonne destination, ce qui est particulièrement utile lors de la configuration de serveurs proxy. D'autres modules tels que `mod_headers` et `mod_rewrite` vous donnent un contrôle précis sur les données qui transitent entre le navigateur et le serveur, vous permettant de modifier les en-têtes HTTP et les URL à la volée, comme si vous ajustiez le cours d'un ruisseau.

En plus de gérer le contenu web statique, Apache prend également en charge la création de pages web dynamiques grâce à des langages de script côté serveur. Les langages couramment utilisés incluent PHP, Perl et Ruby, mais vous pouvez également en utiliser d'autres comme Python, JavaScript, Lua, ou même .NET. Ces langages de script servent d'outils créatifs en coulisses, générant dynamiquement du contenu et garantissant que le site web est interactif et réactif.

Si ce n'est pas déjà fait, installons Apache :

```bash
Hiterof13@htb[/htb]$ sudo apt install apache2 -y
Reading package lists... Done
Building dependency tree
Reading state information... Done
Suggested packages:
  apache2-doc apache2-suexec-pristine | apache2-suexec-custom
The following NEW packages will be installed:
  apache2
0 upgraded, 1 newly installed, 0 to remove and 17 not upgraded.
Need to get 95,1 kB of archives.
After this operation, 535 kB of additional disk space will be used.
Get:1 http://de.archive.ubuntu.com/ubuntu bionic-updates/main amd64 apache2 amd64 2.4.29-1ubuntu4.13 [95,1 kB]
Fetched 95,1 kB in 0s (270 kB/s)

<SNIP>
```

Maintenant, nous pouvons démarrer le serveur en utilisant les commandes `apache2ctl`, `systemctl` ou `service`. Il existe également un binaire `apache2`, mais il n'est généralement pas utilisé pour démarrer directement le serveur (cela est dû à l'utilisation de variables d'environnement dans la configuration par défaut.)

```bash
Hiterof13@htb[/htb]$ sudo systemctl start apache2
```

Une fois Apache démarré, naviguons avec notre navigateur vers la page par défaut ([http://localhost](http://localhost/)). Par défaut, Apache servira sur le port HTTP 80, et votre navigateur utilisera également ce port par défaut chaque fois que vous entrerez une [URI](https://clouddocs.f5.com/api/irules/HTTP__uri.html) HTTP (sauf indication contraire.)

![Page par défaut d'Apache2 sur Ubuntu avec le message 'It works!', indiquant une configuration réussie du serveur. Les instructions suggèrent de remplacer le fichier par défaut avant d'utiliser le serveur.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/apache-default.png)

C'est la page par défaut après l'installation, elle sert à confirmer que le serveur web fonctionne correctement.

Si vous utilisez la Pwnbox, vous pourriez rencontrer une erreur en essayant de démarrer Apache ; cela est dû au fait que le port 80 est occupé par un autre service. Pour définir un port alternatif pour notre serveur web, nous pouvons modifier le fichier `/etc/apache2/ports.conf`. Ici, nous l'avons configuré sur le port 8080.

```text
  GNU nano 2.9.3                    /etc/apache2/ports.conf

# If you just change the port or add more ports here, you will likely also
# have to change the VirtualHost statement in
# /etc/apache2/sites-enabled/000-default.conf

Listen 8080

<IfModule ssl_module>
        Listen 443
</IfModule>

<IfModule mod_gnutls.c>
        Listen 443
</IfModule>

^G Get Help    ^O Write Out   ^W Where Is    ^K Cut Text    ^J Justify     ^C Cur Pos     M-U Undo
^X Exit        ^R Read File   ^\ Replace     ^U Uncut Text  ^T To Spell    ^_ Go To Line  M-E Redo
```

Nous pouvons maintenant redémarrer Apache et naviguer vers `http://localhost:8080`, ou utiliser un outil en ligne de commande tel que `curl` pour vérifier :

```bash
Hiterof13@htb[/htb]$ curl -I http://localhost:8080
HTTP/1.1 200 OK
Date: Mon, 04 Nov 2024 21:18:50 GMT
Server: Apache/2.4.62 (Debian)
Last-Modified: Mon, 07 Oct 2024 06:39:39 GMT
ETag: "29cd-623dd48f6dd5a"
Accept-Ranges: bytes
Content-Length: 10701
Vary: Accept-Encoding
Content-Type: text/html
```

Un autre aspect important du travail avec les serveurs web est d'apprendre à communiquer avec eux en utilisant des outils en ligne de commande comme curl et wget. Ces outils sont incroyablement utiles lorsque nous voulons analyser systématiquement le contenu d'une page hébergée sur un serveur web. Considérez-les comme vos navigateurs web personnels dans le terminal, vous permettant de récupérer et d'interagir avec le contenu web directement depuis la ligne de commande.

Par exemple, nous pourrions écrire un simple script bash qui télécharge une page web et en extrait toutes les URL qu'elle contient. C'est comme jeter un filet dans un océan d'informations et en retirer les liens spécifiques dont nous avons besoin. De tels scripts sont puissants pour des tâches comme le web scraping (aspiration de site web), les tests automatisés ou la surveillance des changements sur un site web.

Cependant, puisque notre objectif principal pour l'instant est de nous familiariser avec Linux, vous aurez l'occasion de voir, construire et utiliser de tels scripts dans d'autres modules. Pour l'instant, concentrons-nous sur la manière dont nous pouvons interagir et communiquer avec un serveur web en utilisant curl et wget.

---

## CURL

`cURL` est un outil qui nous permet de transférer des fichiers depuis le shell via des protocoles comme `HTTP`, `HTTPS`, `FTP`, `SFTP`, `FTPS` ou `SCP`, et de manière générale, nous donne la possibilité de contrôler et de tester des sites web à distance via la ligne de commande. Outre le contenu des serveurs distants, nous pouvons également visualiser des requêtes individuelles pour examiner la communication entre le client et le serveur. Habituellement, `cURL` est déjà installé sur la plupart des systèmes Linux. C'est une autre raison essentielle de se familiariser avec cet outil, car il peut faciliter grandement certains processus par la suite.

```bash
Hiterof13@htb[/htb]$ curl http://localhost
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <!--
    Modified from the Debian original for Ubuntu
    Last updated: 2016-11-16
    See: https://launchpad.net/bugs/1288690
  -->
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Apache2 Ubuntu Default Page: It works</title>
    <style type="text/css" media="screen">
...SNIP...
```

Dans la balise title, nous pouvons voir que c'est le même texte que celui de notre navigateur. Cela nous permet d'inspecter le code source du site web et d'en extraire des informations. Plus précisément, `curl` retourne le code source de la page du site web en tant que STDOUT (sortie standard). Contrairement à la consultation d'un site web avec un navigateur, qui interprète le HTML, le CSS et le Javascript pour créer des sites web visuels et esthétiques. Néanmoins, nous reviendrons sur ce point dans un autre module.

---

## Wget

Une alternative à curl est l'outil `wget`. Avec cet outil, nous pouvons télécharger des fichiers depuis des serveurs FTP ou HTTP directement depuis le terminal, et il sert de gestionnaire de téléchargement solide. Si nous utilisons wget de la même manière, la différence avec curl est que le contenu du site web est téléchargé et stocké localement, comme le montre l'exemple suivant.

```bash
Hiterof13@htb[/htb]$ wget http://localhost
--2020-05-15 17:43:52--  http://localhost/
Resolving localhost (localhost)... 127.0.0.1
Connecting to localhost (localhost)|127.0.0.1|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 10918 (11K) [text/html]
Saving to: 'index.html'

index.html                 100%[=======================================>]  10,66K  --.-KB/s    in 0s

2020-05-15 17:43:52 (33,0 MB/s) - ‘index.html’ saved [10918/10918]
```

---

## Python 3

Une autre option souvent utilisée pour le transfert de données est l'utilisation de Python 3. Dans ce cas, le répertoire racine du serveur web est l'endroit où la commande est exécutée pour démarrer le serveur. Pour cet exemple, nous nous trouvons dans un répertoire où WordPress est installé et qui contient un fichier "readme.html". Maintenant, démarrons le serveur web Python 3 et voyons si nous pouvons y accéder avec le navigateur.

```bash
Hiterof13@htb[/htb]$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

![Page d'accueil de WordPress avec logo, intitulée 'Semantic Personal Publishing Platform'. Comprend un message de Matt Mullenweg sur l'importance de WordPress et une section sur 'Installation : La fameuse installation en 5 minutes'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/python3-browser.png)

Nous pouvons voir quelles requêtes ont été faites si nous regardons maintenant les événements de notre serveur web Python 3.

```bash
Hiterof13@htb[/htb]$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
127.0.0.1 - - [15/May/2020 17:56:29] "GET /readme.html HTTP/1.1" 200 -
127.0.0.1 - - [15/May/2020 17:56:29] "GET /wp-admin/css/install.css?ver=20100228 HTTP/1.1" 200 -
127.0.0.1 - - [15/May/2020 17:56:29] "GET /wp-admin/images/wordpress-logo.png HTTP/1.1" 200 -
127.0.0.1 - - [15/May/2020 17:56:29] "GET /wp-admin/images/wordpress-logo.svg?ver=20131107 HTTP/1.1" 200 -
```

En test d'intrusion (penetration testing), nous sommes souvent confrontés à des défis qui exigent une résolution de problèmes créative et une pensée non conventionnelle. Vous rencontrerez des scénarios que vous n'avez jamais traités auparavant, ce qui signifie non seulement apprendre quelque chose de nouveau, mais aussi trouver des solutions par vous-même grâce à la recherche et à une pensée innovante.

N'oubliez pas, il s'agit d'un processus d'apprentissage, pas d'un examen. Faire vos propres recherches et explorer différentes approches est essentiel pour élargir votre éventail de compétences. En fait, ces efforts seront essentiels pour développer votre expertise et votre capacité d'adaptation dans le domaine. À partir de maintenant, les exercices que vous rencontrerez vous pousseront intentionnellement hors de votre zone de confort. C'est intentionnel, pour accélérer votre apprentissage et vous aider à progresser plus rapidement.

En relevant ces défis, vous développerez les compétences nécessaires pour faire face à des situations réelles, où il n'y a souvent pas de solution universelle. Adoptez ce processus d'exploration et de découverte, car c'est la meilleure façon de progresser.

---

← [[19 - Services Réseau]] | [[00 - Sommaire Linux|Sommaire]] | [[21 - Sauvegarde et Restauration]] →
