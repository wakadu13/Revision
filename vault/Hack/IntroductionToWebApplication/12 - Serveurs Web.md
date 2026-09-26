---
tags:
  - web-applications
ordre: 12
---

# Serveurs Web

---

Un [serveur web (web server)](https://en.wikipedia.org/wiki/Web_server) est une application qui s'exécute sur le serveur backend, qui gère tout le trafic HTTP provenant du navigateur côté client, l'achemine vers les pages demandées, et répond enfin au navigateur côté client. Les serveurs web fonctionnent généralement sur les [ports](https://en.wikipedia.org/wiki/Port_\(computer_networking\)) TCP `80` ou `443`, et sont responsables de la connexion des utilisateurs finaux aux différentes parties de l'application web, en plus de la gestion de leurs diverses réponses.

---

## Flux de travail

Un serveur web typique accepte les requêtes HTTP (HTTP requests) du côté client, et répond avec différentes réponses et codes HTTP, comme une réponse avec le code `200 OK` pour une requête réussie, un code `404 NOT FOUND` lors de la demande de pages qui n'existent pas, un code `403 FORBIDDEN` pour une demande d'accès à des pages restreintes, et ainsi de suite.

![Diagramme montrant un serveur web gérant les requêtes et les réponses de trois clients : smartphone, ordinateur portable et écran.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/web-server-requests.jpg)

Voici quelques-uns des [codes de réponse HTTP (HTTP response codes)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) les plus courants :

|Code|Description|
|---|---|
|**Réponses de succès**||
|`200 OK`|La requête a réussi|
|**Messages de redirection**||
|`301 Moved Permanently`|L'URL de la ressource demandée a été changée de façon permanente|
|`302 Found`|L'URL de la ressource demandée a été changée de façon temporaire|
|**Réponses d'erreur du client**||
|`400 Bad Request`|Le serveur n'a pas pu comprendre la requête en raison d'une syntaxe invalide|
|`401 Unauthorized`|Tentative non authentifiée d'accéder à la page|
|`403 Forbidden`|Le client n'a pas les droits d'accès au contenu|
|`404 Not Found`|Le serveur ne peut pas trouver la ressource demandée|
|`405 Method Not Allowed`|La méthode de la requête est connue du serveur mais a été désactivée et ne peut pas être utilisée|
|`408 Request Timeout`|Cette réponse est envoyée sur une connexion inactive par certains serveurs, même sans aucune requête préalable du client|
|**Réponses d'erreur du serveur**||
|`500 Internal Server Error`|Le serveur a rencontré une situation qu'il ne sait pas comment gérer|
|`502 Bad Gateway`|Le serveur, en agissant comme une passerelle pour obtenir une réponse nécessaire pour traiter la requête, a reçu une réponse invalide|
|`504 Gateway Timeout`|Le serveur agit comme une passerelle et ne peut pas obtenir de réponse à temps|

Les serveurs web acceptent également divers types d'entrées utilisateur (user input) dans les requêtes HTTP, y compris du texte, du [JSON](https://www.w3schools.com/js/js_json_intro.asp), et même des données binaires (binary data) (c'est-à-dire pour les téléchargements de fichiers). Une fois qu'un serveur web reçoit une requête web, il est alors chargé de l'acheminer vers sa destination, d'exécuter tous les processus nécessaires pour cette requête, et de renvoyer la réponse à l'utilisateur du côté client. Les pages et les fichiers vers lesquels le serveur web traite et achemine le trafic sont les fichiers principaux de l'application web.

Ce qui suit montre un exemple de demande d'une page dans un terminal Linux à l'aide de l'utilitaire [cURL](https://en.wikipedia.org/wiki/CURL), et de réception de la réponse du serveur en utilisant l'option `-I`, qui affiche les en-têtes :

```bash
Hiterof13@htb[/htb]$ curl -I https://academy.hackthebox.com  HTTP/2 200 date: Tue, 15 Dec 2020 19:54:29 GMT content-type: text/html; charset=UTF-8 ...SNIP...
```

Tandis que cet exemple de commande `cURL` nous montre le code source de la page web :

```bash
Hiterof13@htb[/htb]$ curl https://academy.hackthebox.com  <!doctype html> <html lang="en"> <head> <meta charset="utf-8" /> <title>Cyber Security Training : HTB Academy</title> <meta name="viewport" content="width=device-width, initial-scale=1.0">
```

De nombreux types de serveurs web peuvent être utilisés pour exécuter des applications web. La plupart d'entre eux peuvent gérer tous les types de requêtes HTTP complexes, et ils sont généralement gratuits. Nous pouvons même développer notre propre serveur web de base en utilisant des langages tels que `Python`, `JavaScript` et `PHP`. Cependant, pour chaque langage, il existe une application web populaire qui est optimisée pour gérer de grandes quantités de trafic web, ce qui nous fait gagner du temps en nous évitant de créer notre propre serveur web.

---

## Apache

![Logo Apache avec une plume.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/apache.png)

[Apache](https://www.apache.org/) (ou `httpd`) est le serveur web le plus courant sur internet, hébergeant plus de `40 %` de tous les sites web. `Apache` est généralement pré-installé dans la plupart des distributions `Linux` et peut également être installé sur les serveurs Windows et macOS.

`Apache` est habituellement utilisé avec `PHP` pour le développement d'applications web, mais il prend également en charge d'autres langages comme `.Net`, `Python`, `Perl`, et même des langages de système d'exploitation comme `Bash` via `CGI`. Les utilisateurs peuvent installer une grande variété de modules `Apache` pour étendre ses fonctionnalités et prendre en charge plus de langages. Par exemple, pour prendre en charge le service de fichiers `PHP`, les utilisateurs doivent installer `PHP` sur le serveur backend, en plus d'installer le module `mod_php` pour `Apache`.

`Apache` est un projet open-source, et les utilisateurs de la communauté peuvent accéder à son code source pour corriger des problèmes et rechercher des vulnérabilités. Il est bien maintenu et régulièrement corrigé contre les vulnérabilités pour le protéger contre l'exploitation. De plus, il est très bien documenté, ce qui rend l'utilisation et la configuration des différentes parties du serveur web relativement faciles. `Apache` est couramment utilisé par les startups et les petites entreprises, car il est simple de développer pour lui. Néanmoins, certaines grandes entreprises utilisent Apache, notamment :

|`Apple`|`Adobe`|`Baidu`|
|---|---|---|

---

## NGINX

![Logo NGINX.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/nginx.png)

[NGINX](https://www.nginx.com/) est le deuxième serveur web le plus courant sur internet, hébergeant environ `30 %` de tous les sites web. `NGINX` se concentre sur le service de nombreuses requêtes web simultanées (concurrent web requests) avec une charge mémoire et CPU relativement faible en utilisant une architecture asynchrone pour ce faire. Cela fait de `NGINX` un serveur web très fiable pour les applications web populaires et les grandes entreprises du monde entier, c'est pourquoi il est le serveur web le plus populaire parmi les sites web à fort trafic, avec environ 60 % des 100 000 sites web les plus importants utilisant `NGINX`.

`NGINX` est également gratuit et open-source, ce qui lui confère tous les mêmes avantages mentionnés précédemment, comme la sécurité et la fiabilité. Certains sites web populaires qui utilisent `NGINX` incluent :

|`Google`|`Facebook`|`Twitter`|`Cisco`|`Intel`|`Netflix`|`HackTheBox`|
|---|---|---|---|---|---|---|

---

## IIS

![Logo Microsoft IIS.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/iis.png)

[IIS (Internet Information Services)](https://en.wikipedia.org/wiki/Internet_Information_Services) est le troisième serveur web le plus courant sur internet, hébergeant environ `15 %` de tous les sites web. `IIS` est développé et maintenu par Microsoft et fonctionne principalement sur les serveurs Microsoft Windows. `IIS` est généralement utilisé pour héberger des applications web développées pour le framework .NET de Microsoft, mais peut également être utilisé pour héberger des applications web développées dans d'autres langages comme `PHP`, ou pour héberger d'autres types de services comme `FTP`. De plus, `IIS` est très bien optimisé pour l'intégration Active Directory et inclut des fonctionnalités comme l'authentification `Windows Auth` pour authentifier les utilisateurs via Active Directory, leur permettant de se connecter automatiquement aux applications web.

Bien qu'il ne soit pas le serveur web le plus populaire, de nombreuses grandes organisations utilisent `IIS` comme serveur web. Beaucoup d'entre elles utilisent Windows Server sur leur backend ou s'appuient fortement sur Active Directory au sein de leur organisation. Certains sites web populaires qui utilisent IIS incluent :

|`Microsoft`|`Office365`|`Skype`|`Stack Overflow`|`Dell`|
|---|---|---|---|---|

Outre ces 3 serveurs web, il existe de nombreux autres serveurs web couramment utilisés, comme [Apache Tomcat](https://tomcat.apache.org/) pour les applications web `Java`, et [Node.JS](https://nodejs.org/en/) pour les applications web développées en `JavaScript` sur le backend.
---

← [[11 - Serveurs Back-End]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[13 - Bases de données]] →
