---
tags:
  - web-applications
ordre: 11
---

# Serveurs Back-End

---

Un serveur back-end est le matériel et le système d'exploitation du back-end qui héberge toutes les applications nécessaires au fonctionnement de l'application web. C'est le système réel qui exécute tous les processus et effectue toutes les tâches qui constituent l'ensemble de l'application web. Le serveur back-end s'intègre dans la [couche d'accès aux données (Data access layer)](https://en.wikipedia.org/wiki/Data_access_layer).

---

## Logiciels

Le serveur back-end contient les 3 autres composants back-end :

- `Serveur Web`
- `Base de données`
- `Framework de développement`

![Diagramme montrant un serveur back-end exécutant Linux et Windows, connecté à un serveur web (Apache, NGINX, IIS), une application web (PHP, C#, Java) et une base de données (MySQL, MS SQL, Oracle).](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/backend-server.jpg)

D'autres composants logiciels sur le serveur back-end peuvent inclure des [hyperviseurs (hypervisors)](https://en.wikipedia.org/wiki/Hypervisor), des conteneurs (containers), et des WAFs.

Il existe de nombreuses combinaisons populaires de « stacks » pour les serveurs back-end, qui contiennent un ensemble spécifique de composants back-end. Voici quelques exemples courants :

|Combinaisons|Composants|
|---|---|
|[LAMP](https://en.wikipedia.org/wiki/LAMP_\(software_bundle\))|`Linux`, `Apache`, `MySQL`, et `PHP`.|
|[WAMP](https://en.wikipedia.org/wiki/LAMP_\(software_bundle\)#WAMP)|`Windows`, `Apache`, `MySQL`, et `PHP`.|
|[WINS](https://en.wikipedia.org/wiki/Solution_stack)|`Windows`, `IIS`, `.NET`, et `SQL Server`|
|[MAMP](https://en.wikipedia.org/wiki/MAMP)|`macOS`, `Apache`, `MySQL`, et `PHP`.|
|[XAMPP](https://en.wikipedia.org/wiki/XAMPP)|Multiplateforme, `Apache`, `MySQL`, et `PHP/PERL`.|

Une liste complète des Web Solution Stacks est disponible dans cet [article](https://en.wikipedia.org/wiki/Solution_stack).

---

## Matériel

Le serveur back-end contient tout le matériel nécessaire. La puissance et les capacités de performance de ce matériel déterminent la stabilité et la réactivité de l'application web. Comme abordé précédemment dans la section `Architecture`, de nombreuses architectures, en particulier pour les très grandes applications web, sont conçues pour répartir leur charge sur de nombreux serveurs back-end qui travaillent collectivement pour effectuer les mêmes tâches et fournir l'application web à l'utilisateur final. Les applications web n'ont pas à s'exécuter directement sur un seul serveur back-end, mais peuvent utiliser des centres de données et des services d'hébergement cloud qui fournissent des hôtes virtuels pour l'application web.
---

← [[10 - Falsification de requête inter-site (Cross-Site Request Forgery - CSRF)]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[12 - Serveurs Web]] →
