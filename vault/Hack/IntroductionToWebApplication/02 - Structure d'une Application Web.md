---
tags:
  - web-applications
ordre: 2
---

# Structure d'une Application Web

---

Il n'y a pas deux applications web identiques. Les entreprises créent des applications web pour une multitude d'utilisations et de publics. Les applications web sont conçues et programmées différemment, et l'infrastructure back-end peut être configurée de nombreuses manières. Il est important de comprendre les différentes façons dont les applications web peuvent fonctionner en coulisses, la structure d'une application web, ses composants, et comment ils peuvent être mis en place au sein de l'infrastructure d'une entreprise.

Les structures d'applications web se composent de nombreuses couches différentes qui peuvent être résumées dans les trois catégories principales suivantes :

|**Catégorie**|**Description**|
|---|---|
|`Infrastructure de l'application web`|Décrit la structure des composants requis, tels que la base de données, nécessaires au bon fonctionnement de l'application web. Étant donné que l'application web peut être configurée pour s'exécuter sur un serveur distinct, il est essentiel de savoir à quel serveur de base de données elle doit accéder.|
|`Composants de l'application web`|Les composants qui constituent une application web représentent tous les éléments avec lesquels l'application interagit. Ils sont répartis dans les trois domaines suivants : les composants `UI/UX`, `Client` et `Serveur`.|
|`Architecture de l'application web`|L'architecture comprend toutes les relations entre les différents composants de l'application web.|

---

## Infrastructure de l'Application Web

Les applications web peuvent utiliser de nombreuses configurations d'infrastructure différentes. Celles-ci sont également appelées `modèles`. Les plus courantes peuvent être regroupées dans les quatre types suivants :

- `Client-Serveur`
- `Un Seul Serveur`
- `Plusieurs Serveurs - Une Base de Données`
- `Plusieurs Serveurs - Plusieurs Bases de Données`

---

#### Client-Serveur

Les applications web adoptent souvent le modèle `client-serveur`. Dans un modèle client-serveur, un serveur héberge l'application web et la distribue à tous les clients qui tentent d'y accéder.

![Schéma montrant un serveur connecté à quatre clients : ordinateur de bureau, ordinateur portable, smartphone et écran.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/client-server-model.jpg)

Dans ce modèle, les applications web ont deux types de composants : ceux du front-end, qui sont généralement interprétés et exécutés côté client (navigateur), et les composants du back-end, généralement compilés, interprétés et exécutés par le serveur d'hébergement.

Lorsqu'un client visite l'URL (adresse web, par ex. [https://www.acme.local](https://www.acme.local/)) de l'application web, le serveur utilise l'interface principale de l'application web (`UI`). Une fois que l'utilisateur clique sur un bouton ou demande une fonction spécifique, le navigateur envoie une requête web HTTP au serveur, qui interprète cette requête et effectue la ou les tâches nécessaires pour la compléter (par ex. connecter l'utilisateur, ajouter un article au panier, naviguer vers une autre page, etc.). Une fois que le serveur dispose des données requises, il renvoie le résultat au navigateur du client, qui l'affiche de manière lisible par un humain.

`Ce site web avec lequel nous interagissons actuellement est également une application web, développée et hébergée par Hack The Box (serveur web), et nous y accédons et interagissons avec elle en utilisant notre navigateur web (client).`

Cependant, même si la plupart des applications web utilisent une architecture client-serveur front-back-end, il existe de nombreuses implémentations de conception.

---

#### Un Seul Serveur

Dans cette architecture, l'ensemble de l'application web, voire plusieurs applications web et leurs composants, y compris la base de données, sont hébergés sur un seul serveur. Bien que cette conception soit simple et facile à mettre en œuvre, c'est aussi la plus risquée.

![Schéma montrant un serveur connecté à trois clients : smartphone, ordinateur portable et écran.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/one-server-arch.jpg)

Si une application web hébergée sur ce serveur est compromise dans cette architecture, alors les données de toutes les applications web seront compromises. Cette conception représente une approche du type « `tous ses œufs dans le même panier` », car si l'une des applications web hébergées est vulnérable, l'ensemble du serveur web le devient.

De plus, si le serveur web tombe en panne pour une raison quelconque, toutes les applications web hébergées deviennent entièrement inaccessibles jusqu'à ce que le problème soit résolu.

---

#### Plusieurs Serveurs - Une Base de Données

Ce modèle sépare la base de données sur son propre serveur de base de données et permet au serveur hébergeant les applications web d'accéder au serveur de base de données pour stocker et récupérer des données. Il peut s'agir d'une relation de plusieurs serveurs vers une base de données ou d'un serveur vers une base de données, tant que la base de données est séparée sur son propre serveur.

![Schéma montrant une base de données connectée à trois serveurs, chacun lié à un client smartphone, ordinateur portable et écran.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/many-server-one-db-arch.jpg)

Ce modèle peut permettre à plusieurs applications web d'accéder à une seule base de données pour avoir accès aux mêmes données sans avoir à les synchroniser entre elles. Les applications web peuvent être des réplications d'une application principale (par ex., principale/sauvegarde), ou elles peuvent être des applications web distinctes qui partagent des données communes.

L'avantage principal de ce modèle (`d'un point de vue sécurité`) est la segmentation, où chacun des principaux composants d'une application web est situé et hébergé séparément. Si un serveur web est compromis, les autres serveurs web ne sont pas directement affectés. De même, si la base de données est compromise (par ex., via une vulnérabilité d'injection SQL), l'application web elle-même n'est pas directement affectée. Il reste des mesures de contrôle d'accès qui doivent être mises en œuvre après la segmentation des actifs, comme limiter l'accès de l'application web aux seules données nécessaires à son fonctionnement.

---

#### Plusieurs Serveurs - Plusieurs Bases de Données

Ce modèle s'appuie sur le modèle `Plusieurs Serveurs, Une Base de Données`. Cependant, au sein du serveur de base de données, les données de chaque application web sont hébergées dans une base de données distincte. L'application web ne peut accéder qu'à ses données privées et aux données communes partagées entre les applications web. Il est également possible d'héberger la base de données de chaque application web sur son propre serveur de base de données.

![Schéma montrant trois bases de données connectées à trois serveurs, chacun lié à un client smartphone, ordinateur portable et écran.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/many-server-many-db-arch.jpg)

Cette conception est également largement utilisée à des fins de redondance, de sorte que si un serveur web ou une base de données tombe en panne, une sauvegarde prendra le relais pour réduire au maximum les temps d'arrêt. Bien que cela puisse être plus difficile à mettre en œuvre et puisse nécessiter des outils comme des [répartiteurs de charge (load balancers)](https://en.wikipedia.org/wiki/Load_balancing_\(computing\)) pour fonctionner correctement, cette architecture est l'un des meilleurs choix en termes de sécurité en raison de ses mesures de contrôle d'accès appropriées et de la segmentation adéquate des actifs.

Outre ces modèles, il existe d'autres modèles d'applications web, tels que les applications web [sans serveur (serverless)](https://aws.amazon.com/lambda/serverless-architectures-learn-more) ou les applications web qui utilisent des [microservices](https://aws.amazon.com/microservices).

---

## Composants d'une Application Web

Chaque application web peut avoir un nombre différent de composants. Néanmoins, tous les composants des modèles mentionnés précédemment peuvent être décomposés en :

1. `Client`
2. `Serveur`
    - Serveur web
    - Logique de l'application web
    - Base de données
3. `Services` (Microservices)
    - Intégrations tierces
    - Intégrations d'applications web
4. `Fonctions` (Serverless)

---

## Architecture d'une Application Web

Les composants d'une application web sont divisés en trois couches différentes (AKA architecture à trois niveaux (Three Tier Architecture)).

|**Couche**|**Description**|
|---|---|
|`Couche de présentation`|Se compose des composants de processus d'interface utilisateur qui permettent la communication avec l'application et le système. Ceux-ci sont accessibles par le client via le navigateur web et sont retournés sous forme de HTML, JavaScript et CSS.|
|`Couche applicative`|Cette couche garantit que toutes les requêtes client (requêtes web) sont correctement traitées. Divers critères sont vérifiés, tels que l'autorisation, les privilèges et les données transmises au client.|
|`Couche de données`|La couche de données travaille en étroite collaboration avec la couche applicative pour déterminer précisément où les données requises sont stockées et accessibles.|

Un exemple d'architecture d'application web pourrait ressembler à ceci :

![Schéma de l'architecture ASP.NET Core montrant le client, le proxy inverse IIS, l'application web ASP.NET Core avec des filtres et des services, connectée à des sources de données, des fournisseurs d'identité et des services tiers.](https://docs.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/media/image5-12.png)Source : [Documentation Microsoft](https://docs.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures)

De plus, certains serveurs web peuvent exécuter des appels au système d'exploitation et des programmes, comme [IIS ISAPI](https://learn.microsoft.com/en-us/previous-versions/iis/6.0-sdk/ms525172\(v=vs.90\)) ou [PHP-CGI](https://www.php.net/manual/en/install.unix.commandline.php).

---

#### Microservices

Nous pouvons considérer les microservices comme des composants indépendants de l'application web, qui dans la plupart des cas ne sont programmés que pour une seule tâche. Par exemple, pour une boutique en ligne, nous pouvons décomposer les tâches principales en les composants suivants :

- Inscription
- Recherche
- Paiements
- Évaluations
- Avis

Ces composants communiquent avec le client et entre eux. La communication entre ces microservices est `sans état (stateless)`, ce qui signifie que la requête et la réponse sont indépendantes. C'est parce que les données sont `stockées séparément` des microservices respectifs. L'utilisation de microservices est considérée comme une [architecture orientée services (SOA)](https://en.wikipedia.org/wiki/Service-oriented_architecture), construite comme une collection de différentes fonctions automatisées axées sur un seul objectif commercial. Néanmoins, ces microservices dépendent les uns des autres.

Un autre composant essentiel et efficace des microservices est qu'ils peuvent être écrits dans différents langages de programmation et continuer à interagir. Les microservices bénéficient d'une mise à l'échelle plus facile et d'un développement plus rapide des applications, ce qui encourage l'innovation et accélère la mise sur le marché de nouvelles fonctionnalités. Certains avantages des microservices incluent :

- Agilité
- Mise à l'échelle flexible
- Déploiement facile
- Code réutilisable
- Résilience

Ce [livre blanc](https://d1.awsstatic.com/whitepapers/microservices-on-aws.pdf) d'AWS offre un excellent aperçu de la mise en œuvre des microservices.

---

#### Sans serveur (Serverless)

Les fournisseurs de cloud tels qu'AWS, GCP, Azure, entre autres, proposent des architectures sans serveur. Ces plateformes fournissent des frameworks applicatifs pour construire de telles applications web sans avoir à se soucier des serveurs eux-mêmes. Ces applications web s'exécutent alors dans des conteneurs de calcul sans état (Docker, par exemple). Ce type d'architecture donne à une entreprise la flexibilité de créer et de déployer des applications et des services sans avoir à gérer l'infrastructure ; toute la gestion des serveurs est effectuée par le fournisseur de cloud, ce qui élimine le besoin de provisionner, de mettre à l'échelle et de maintenir les serveurs nécessaires pour faire fonctionner les applications et les bases de données.

Vous pouvez en lire plus sur le calcul sans serveur et ses divers cas d'utilisation [ici](https://aws.amazon.com/serverless).

---

## Sécurité de l'Architecture

Comprendre l'architecture générale des applications web et la conception spécifique de chaque application web est important lors de la réalisation d'un test d'intrusion (penetration test) sur n'importe quelle application web. Dans de nombreux cas, la vulnérabilité d'une application web individuelle peut ne pas être causée par une erreur de programmation mais par une erreur de conception dans son architecture.

Par exemple, une application web individuelle peut avoir toutes ses fonctionnalités de base implémentées de manière sécurisée. Cependant, en raison d'un manque de mesures de contrôle d'accès appropriées dans sa conception, par exemple l'utilisation du [contrôle d'accès basé sur les rôles (RBAC)](https://en.wikipedia.org/wiki/Role-based_access_control), les utilisateurs peuvent être en mesure d'accéder à certaines fonctionnalités d'administration qui ne sont pas destinées à leur être directement accessibles ou même d'accéder aux informations privées d'autres utilisateurs sans en avoir les privilèges. Pour résoudre ce type de problème, un changement de conception important devrait être mis en œuvre, ce qui serait probablement à la fois coûteux et long.

Un autre exemple serait si nous ne parvenons pas à trouver la base de données après avoir exploité une vulnérabilité et pris le contrôle du serveur back-end, ce qui peut signifier que la base de données est hébergée sur un serveur distinct. Nous pourrions ne trouver qu'une partie des données de la base de données, ce qui peut signifier que plusieurs bases de données sont utilisées. C'est pourquoi la sécurité doit être prise en compte à chaque phase du développement d'une application web, et des tests d'intrusion doivent être effectués tout au long du cycle de vie du développement de l'application web.
---

← [[01 - Introduction]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[03 - Front-end vs. Back-end]] →
