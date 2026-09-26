---
tags:
  - web-applications
ordre: 14
---

# Frameworks de Développement & APIs

---

En plus des serveurs web qui peuvent héberger des applications web dans divers langages, il existe de nombreux frameworks de développement web courants qui aident à développer les fichiers et les fonctionnalités de base des applications web. Avec la complexité croissante des applications web, il peut être difficile de créer une application web moderne et sophistiquée à partir de zéro. Par conséquent, la plupart des applications web populaires sont développées à l'aide de frameworks web.

Comme la plupart des applications web partagent des fonctionnalités communes -telles que l'inscription des utilisateurs-, les frameworks de développement web facilitent la mise en œuvre rapide de ces fonctionnalités et leur liaison avec les composants front-end, créant ainsi une application web entièrement fonctionnelle. Parmi les frameworks de développement web les plus courants, on peut citer :

- [Laravel](https://laravel.com/) (`PHP`) : généralement utilisé par les startups et les petites entreprises, car il est puissant mais facile à développer.
- [Express](https://expressjs.com/) (`Node.JS`) : utilisé par `PayPal`, `Yahoo`, `Uber`, `IBM`, et `MySpace`.
- [Django](https://www.djangoproject.com/) (`Python`) : utilisé par `Google`, `YouTube`, `Instagram`, `Mozilla`, et `Pinterest`.
- [Rails](https://rubyonrails.org/) (`Ruby`) : utilisé par `GitHub`, `Hulu`, `Twitch`, `Airbnb`, et même `Twitter` par le passé.

Il convient de noter que les sites web populaires utilisent généralement une variété de frameworks et de serveurs web, plutôt qu'un seul.

---

## APIs

Un aspect important du développement d'applications web back-end est l'utilisation d'[APIs](https://en.wikipedia.org/wiki/API) web et de paramètres de requête HTTP pour connecter le front-end et le back-end afin de pouvoir envoyer des données dans les deux sens entre les composants front-end et back-end et d'exécuter diverses fonctions au sein de l'application web.

Pour que le composant front-end interagisse avec le back-end et demande l'exécution de certaines tâches, il utilise des APIs pour demander au composant back-end une tâche spécifique avec une entrée spécifique. Les composants back-end traitent ces requêtes, exécutent les fonctions nécessaires et renvoient une certaine réponse aux composants front-end, qui effectuent finalement le rendu de la sortie pour l'utilisateur final du côté client.

---

#### Paramètres de Requête

La méthode par défaut pour envoyer des arguments spécifiques à une page web passe par les paramètres de requête `GET` et `POST`. Cela permet aux composants front-end de spécifier des valeurs pour certains paramètres utilisés dans la page afin que les composants back-end les traitent et y répondent en conséquence.

Par exemple, une page `/search.php` prendrait un paramètre `item`, qui peut être utilisé pour spécifier l'élément de recherche. La transmission d'un paramètre via une requête `GET` se fait par l'URL '`/search.php?item=apples`', tandis que les paramètres `POST` sont transmis via les données `POST` au bas de la requête `HTTP` `POST` :

```http
POST /search.php HTTP/1.1 ...SNIP...  item=apples
```

Les paramètres de requête permettent à une seule page de recevoir différents types d'entrées, chacune pouvant être traitée différemment. Pour certains autres scénarios, les APIs Web peuvent être beaucoup plus rapides et plus efficaces à utiliser. Le module [Requêtes Web](https://academy.hackthebox.com/course/preview/web-requests) approfondit les requêtes `HTTP`.

---

## APIs Web

Une API ([Application Programming Interface](https://en.wikipedia.org/wiki/API) ou interface de programmation d'application) est une interface au sein d'une application qui spécifie comment l'application peut interagir avec d'autres applications. Pour les applications Web, c'est ce qui permet un accès à distance aux fonctionnalités des composants back-end. Les APIs ne sont pas exclusives aux applications web et sont utilisées pour les applications logicielles en général. Les APIs Web sont généralement accessibles via le protocole `HTTP` et sont habituellement gérées et traduites par les serveurs web.

![Schéma d'une API avec des connexions à des icônes de cloud, d'utilisateur, de shopping, de vidéo, d'audio et de clé](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/api_examples.jpg)

Une application web météo, par exemple, peut avoir une certaine API pour récupérer la météo actuelle d'une ville donnée. Nous pouvons interroger l'URL de l'API et passer le nom ou l'ID de la ville, et elle renverra la météo actuelle dans un objet `JSON`. Un autre exemple est l'API de Twitter, qui nous permet de récupérer les derniers Tweets d'un certain compte aux formats `XML` ou `JSON`, et nous permet même d'envoyer un Tweet 'si authentifié', etc.

Pour permettre l'utilisation d'APIs au sein d'une application web, les développeurs doivent développer cette fonctionnalité sur le back-end de l'application web en utilisant les standards d'API comme `SOAP` ou `REST`.

---

## SOAP

Le standard `SOAP` ([Simple Objects Access](https://en.wikipedia.org/wiki/SOAP)) partage des données via `XML`, où la requête est faite en `XML` à travers une requête HTTP, et la réponse est également renvoyée en `XML`. Les composants front-end sont conçus pour analyser (parser) correctement cette sortie `XML`. Voici un exemple de message `SOAP` :

```xml
<?xml version="1.0"?>  <soap:Envelope xmlns:soap="http://www.example.com/soap/soap/" soap:encodingStyle="http://www.w3.org/soap/soap-encoding">  <soap:Header> </soap:Header>  <soap:Body>   <soap:Fault>   </soap:Fault> </soap:Body>  </soap:Envelope>
```

`SOAP` est très utile pour transférer des données structurées (c'est-à-dire un objet de classe entier), ou même des données binaires, et est souvent utilisé avec des objets sérialisés, tout cela permettant de partager des données complexes entre les composants front-end et back-end et de les analyser correctement. Il est également très utile pour partager des objets _stateful_ (avec état) - c'est-à-dire partager/modifier l'état actuel d'une page web -, ce qui devient de plus en plus courant avec les applications web et mobiles modernes.

Cependant, `SOAP` peut être difficile à utiliser pour les débutants ou nécessiter des requêtes longues et compliquées même pour des requêtes plus petites, comme des requêtes de base de `recherche` (`search`) ou de `filtre` (`filter`). C'est là que le standard d'API `REST` est plus utile.

---

## REST

Le standard `REST` ([Representational State Transfer](https://en.wikipedia.org/wiki/Representational_state_transfer)) partage des données via le chemin de l'URL (par ex. `search/users/1`), et renvoie généralement la sortie au format `JSON` (par ex. userid `1`).

Contrairement aux paramètres de requête, les APIs `REST` se concentrent généralement sur des pages qui attendent un type d'entrée passé directement via le chemin de l'URL, sans spécifier son nom ou son type. Ceci est généralement utile pour des requêtes comme la `recherche` (`search`), le `tri` (`sort`), ou le `filtre` (`filter`). C'est pourquoi les APIs `REST` décomposent généralement la fonctionnalité de l'application web en APIs plus petites et utilisent ces requêtes d'API plus petites pour permettre à l'application web d'effectuer des actions plus avancées, rendant l'application web plus modulaire et évolutive (scalable).

Les réponses aux requêtes d'API `REST` sont généralement au format `JSON`, et les composants front-end sont ensuite développés pour gérer cette réponse et en faire le rendu correctement. D'autres formats de sortie pour `REST` incluent `XML`, `x-www-form-urlencoded`, ou même des données brutes (raw data). Comme vu précédemment dans la section `database`, voici un exemple de réponse `JSON` à la requête API `GET /category/posts/` :

```json
{   "100001": {     "date": "01-01-2021",     "content": "Welcome to this web application."   },   "100002": {     "date": "02-01-2021",     "content": "This is the first post on this web app."   },   "100003": {     "date": "02-01-2021",     "content": "Reminder: Tomorrow is the ..."   } }
```

`REST` utilise diverses méthodes HTTP pour effectuer différentes actions sur l'application web :

- Requête `GET` pour récupérer des données
- Requête `POST` pour créer des données (non-idempotent)
- Requête `PUT` pour créer ou remplacer des données existantes (idempotent)
- Requête `DELETE` pour supprimer des données
---

← [[13 - Bases de données]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[15 - Vulnérabilités Web Courantes]] →
