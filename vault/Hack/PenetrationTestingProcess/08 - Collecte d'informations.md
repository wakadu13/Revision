---
tags:
  - pentest-process
ordre: 8
---

# Collecte d'informations

---

Une fois la phase de pré-engagement terminée et que toutes les parties ont signé l'ensemble des termes et conditions contractuels, la phase de `collecte d'informations` (information gathering) commence. La collecte d'informations est une partie essentielle de toute évaluation de la sécurité. C'est la phase au cours de laquelle nous recueillons toutes les informations disponibles sur l'entreprise, ses employés et son infrastructure, ainsi que sur la manière dont ils sont organisés. La collecte d'informations est la phase la plus fréquente et la plus vitale tout au long du processus de test de pénétration (penetration testing), sur laquelle nous reviendrons sans cesse.

![Processus de test de pénétration : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-IG.png)

Toutes les étapes que nous entreprenons pour exploiter les vulnérabilités sont basées sur les informations que nous énumérons sur nos cibles. Cette phase peut être considérée comme la pierre angulaire de tout test de pénétration. Nous pouvons obtenir les informations qui nous sont nécessaires de nombreuses manières différentes. Cependant, nous pouvons les diviser en plusieurs catégories :

- Renseignement en Sources Ouvertes (Open-Source Intelligence)
- Énumération de l'infrastructure
- Énumération des services
- Énumération des hôtes

Ces quatre catégories devraient et doivent être réalisées par nous pour chaque test de pénétration. En effet, l'`information` est le composant principal qui nous mène à la réussite des tests de pénétration et à l'identification des vulnérabilités de sécurité. Nous pouvons obtenir ces informations n'importe où, que ce soit sur les réseaux sociaux, les offres d'emploi, les hôtes et serveurs individuels, ou même auprès des employés. L'information est continuellement diffusée et partagée partout.

Après tout, nous, les humains, communiquons en échangeant des informations, et les composants et services réseau communiquent de manière similaire. Tout échange d'informations a toujours un but précis. Pour les réseaux informatiques, l'objectif est toujours de déclencher un processus particulier. Qu'il s'agisse de stocker des données dans une base de données, de s'enregistrer, de générer des valeurs spécifiques ou de transmettre des informations.

---

## Renseignement en Sources Ouvertes (Open-Source Intelligence)

Supposons que notre client veuille que nous voyions quelles informations nous pouvons trouver sur son entreprise sur internet. Pour cela, nous utilisons ce que l'on appelle le `Renseignement en Sources Ouvertes` (`OSINT`). L'OSINT est un processus de recherche d'informations publiquement disponibles sur une entreprise ou des individus cibles, qui permet l'identification d'événements (c.-à-d. des réunions publiques et privées), de dépendances externes et internes, et de connexions. L'OSINT utilise des informations publiques (en sources ouvertes) provenant de sources librement accessibles pour obtenir les résultats souhaités. Nous pouvons souvent trouver des informations sensibles et pertinentes pour la sécurité provenant des entreprises et de leurs employés. Habituellement, les personnes qui partagent de telles informations ne savent pas qu'elles ne sont pas les seules à pouvoir y accéder.

Il est possible de trouver des informations très sensibles telles que des mots de passe, des hashes, des clés, des jetons (tokens), et bien plus encore, qui peuvent nous donner accès au réseau en quelques minutes seulement. Les dépôts sur des sites comme [Github](https://github.com/) ou d'autres plateformes de développement ne sont souvent pas configurés correctement, et des personnes externes peuvent voir ces informations. Si ce type d'information sensible est trouvé au début du test, la section Gestion des Incidents et Rapport des Règles d'Engagement (RoE) doit décrire la procédure de signalement de ces types de vulnérabilités de sécurité critiques. Les mots de passe ou les clés SSH publiés publiquement représentent une faille de sécurité critique s'ils n'ont pas déjà été supprimés ou modifiés. Par conséquent, l'administrateur de notre client doit examiner ces informations avant que nous ne poursuivions.

#### Clés SSH privées et publiques

![Page Searchcode montrant un extrait de code avec des clés privées et publiques OpenSSH expurgées.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/searchcode3.png)

Les développeurs partagent souvent des sections entières de code sur [StackOverflow](https://stackoverflow.com/) pour donner aux autres développeurs un meilleur aperçu du fonctionnement de leur code afin de les aider à résoudre leurs problèmes. Ce type d'information peut également être trouvé très rapidement et utilisé contre l'entreprise. Notre tâche est de trouver de telles failles de sécurité et de les faire corriger. Nous pouvons en apprendre beaucoup plus grâce au module [OSINT: Corporate Recon](https://academy.hackthebox.com/course/preview/osint-corporate-recon). Il présente de nombreuses techniques différentes sur la manière dont nous pouvons trouver de telles informations.

---

## Énumération de l'infrastructure

Pendant l'énumération de l'infrastructure, nous essayons d'obtenir une vue d'ensemble de la position de l'entreprise sur internet et l'intranet. Pour cela, nous utilisons l'OSINT et les premiers scans actifs. Nous utilisons des services tels que le DNS pour créer une carte des serveurs et des hôtes du client et pour comprendre comment leur `infrastructure` est structurée. Cela inclut les serveurs de noms, les serveurs de messagerie, les serveurs web, les instances cloud, et plus encore. Nous dressons une liste précise des hôtes et de leurs adresses IP et les comparons à notre périmètre (scope) pour voir s'ils y sont inclus et répertoriés.

Dans cette phase, nous essayons également de déterminer les mesures de sécurité de l'entreprise. Plus ces informations sont précises, plus il sera facile de dissimuler nos attaques (`tests évasifs` - Evasive Testing). Mais l'identification des pare-feu, tels que les pare-feu applicatifs web (Web Application Firewalls), nous donne également une excellente compréhension des techniques qui pourraient déclencher une alarme chez notre client et des méthodes qui peuvent être utilisées pour éviter cette alarme.

Ici, peu importe « où » nous nous trouvons, que nous essayions d'obtenir une vue d'ensemble de l'infrastructure depuis l'extérieur (`externe`) ou que nous examinions l'infrastructure de l'intérieur (`interne`) du réseau. L'énumération depuis l'intérieur du réseau nous donne un bon aperçu des hôtes et des serveurs que nous pouvons utiliser comme cibles pour une attaque par `pulvérisation de mots de passe` (Password Spraying), dans laquelle nous utilisons un seul mot de passe pour tenter de nous authentifier avec le plus de noms d'utilisateurs différents possible, en espérant qu'une seule tentative d'authentification réussie nous accorde un point d'ancrage dans le réseau. Toutes ces méthodes et techniques utilisées à cette fin seront examinées plus en détail dans les modules individuels.

---

## Énumération des services

Dans l'énumération des services, nous identifions les services qui nous permettent d'interagir avec l'hôte ou le serveur sur le réseau (ou localement, d'un point de vue interne). Il est donc crucial de se renseigner sur le service, sa `version`, les `informations` qu'il nous fournit, et la `raison` pour laquelle il peut être utilisé. Une fois que nous comprenons le contexte pour lequel ce service a été mis en place, certaines conclusions logiques peuvent être tirées pour nous offrir plusieurs options.

De nombreux services ont un historique de versions qui nous permet d'identifier si la version installée sur l'hôte ou le serveur est réellement à jour ou non. Cela nous aidera également à trouver des vulnérabilités de sécurité qui subsistent avec les anciennes versions dans la plupart des cas. De nombreux administrateurs craignent de modifier des applications qui fonctionnent, car cela pourrait nuire à l'ensemble de l'infrastructure. Par conséquent, les administrateurs préfèrent souvent accepter le risque de laisser une ou plusieurs vulnérabilités ouvertes et de maintenir la fonctionnalité plutôt que de combler les failles de sécurité.

---

## Énumération des hôtes

Une fois que nous avons une liste détaillée de l'infrastructure du client, nous examinons chaque hôte listé dans le document de cadrage (scoping document). Nous essayons d'identifier quel `système d'exploitation` fonctionne sur l'hôte ou le serveur, quels `services` il utilise, quelles `versions` des services, et bien plus encore. Encore une fois, en dehors des scans actifs, nous pouvons également utiliser diverses méthodes OSINT pour nous dire comment cet hôte ou ce serveur peut être configuré.

Nous pouvons trouver de nombreux services différents, comme un serveur FTP que l'entreprise utilise pour échanger des données entre les employés et qui autorise même un accès anonyme. Aujourd'hui encore, il existe de nombreux hôtes et serveurs qui ne sont plus pris en charge par les fabricants. Cependant, des vulnérabilités sont toujours trouvées pour ces anciennes versions de systèmes d'exploitation et de services, qui subsistent et mettent en danger toute l'infrastructure de notre client.

Peu importe ici que nous examinions chaque hôte ou serveur de l'extérieur ou de l'intérieur. Cependant, d'un point de vue interne, nous trouverons des services qui ne sont souvent pas accessibles de l'extérieur. Par conséquent, de nombreux administrateurs deviennent négligents et considèrent souvent ces services comme « sûrs » car ils ne sont pas directement accessibles depuis internet. Ainsi, de nombreuses erreurs de configuration sont souvent découvertes ici en raison de ces hypothèses ou de pratiques laxistes. Lors de l'énumération des hôtes, nous essayons de déterminer quel rôle cet hôte ou ce serveur joue et avec quels composants réseau il communique. De plus, nous devons également identifier quels `services` il utilise à cette fin et sur quels `ports` ils se trouvent.

Pendant l'énumération interne des hôtes, qui dans la plupart des cas a lieu après l'`Exploitation` réussie d'une ou plusieurs vulnérabilités, nous examinons également l'hôte ou le serveur de l'intérieur. Cela signifie que nous recherchons des `fichiers` sensibles, des `services` locaux, des `scripts`, des `applications`, des `informations` et d'autres éléments qui pourraient être stockés sur l'hôte. C'est également une partie essentielle de la phase de `Post-Exploitation`, où nous essayons d'exploiter et d'élever les privilèges.

---

## Pillaging

Une autre étape essentielle est le `Pillaging`. Après avoir atteint la phase de `Post-Exploitation`, le pillaging est effectué pour collecter des informations sensibles localement sur l'hôte déjà exploité, telles que les noms d'employés, les données clients, et bien plus encore. Cependant, cette collecte d'informations n'a lieu qu'après avoir exploité l'hôte cible et y avoir obtenu un accès.

Les informations que nous pouvons obtenir sur les hôtes exploités peuvent être divisées en de nombreuses catégories différentes et varient considérablement. Cela dépend de l'objectif de l'hôte et de son positionnement dans le réseau de l'entreprise. Les administrateurs qui prennent les mesures de sécurité pour ces hôtes jouent également un rôle important. Néanmoins, de telles informations peuvent montrer l'`impact` d'une attaque potentielle sur notre client et être utilisées pour des étapes ultérieures afin d'`élever nos privilèges` (escalate our privileges) ou de nous `déplacer latéralement` (move laterally) plus loin dans le réseau.

- Notez que `HTB Academy` n'a pas de module spécifiquement axé sur le pillaging.

Ceci est intentionnel pour des raisons que nous allons clarifier ici. Le pillaging en soi n'est pas une étape ou une sous-catégorie comme beaucoup le décrivent souvent, mais une partie intégrante des étapes de collecte d'informations et d'élévation de privilèges qui est inévitablement effectuée localement sur les systèmes cibles.

- `Le pillaging est expliqué séparément dans d'autres modules, où nous considérons les étapes correspondantes comme utiles et nécessaires.`

Voici une petite liste de modules où le `Pillaging` est abordé, mais ce sujet sera également traité dans de nombreux autres modules :

||||
|---|---|---|
|`Network Enumeration with Nmap`|`Getting Started`|`Password Attacks`|
|`Active Directory Enumeration & Attacks`|`Linux Privilege Escalation`|`Windows Privilege Escalation`|
|`Attacking Common Services`|`Attacking Common Applications`|`Attacking Enterprise Networks`|

Nous interagirons avec plus de `150 cibles` au cours du parcours professionnel de Testeur de Pénétration (Penetration Tester Job Role Path) et effectuerons neuf mini-tests de pénétration simulés, ce qui nous donnera de nombreuses occasions de travailler et de pratiquer ce sujet. De plus, les modules spécifiques aux systèmes d'exploitation doivent être considérés du point de vue du pillaging, car une grande partie de ce qui est montré dans ces modules peut être utilisée pour la récupération d'informations ou l'élévation de privilèges sur les systèmes cibles.
---

← [[07 - Pré-engagement]] | [[00 - Sommaire Penetration Testing Process|Sommaire]] | [[09 - Évaluation des vulnérabilités]] →
