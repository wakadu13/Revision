---
tags:
  - web-applications
ordre: 1
---

# Introduction

---

Les [applications web](https://en.wikipedia.org/wiki/Web_application) sont des applications interactives qui s'exécutent sur des navigateurs web. Les applications web adoptent généralement une [architecture client-serveur](https://cio-wiki.org/wiki/Client_Server_Architecture) pour s'exécuter et gérer les interactions. Elles ont généralement des composants front-end (c'est-à-dire l'interface du site web, ou "ce que l'utilisateur voit") qui s'exécutent côté client (navigateur) et d'autres composants back-end (code source de l'application web) qui s'exécutent côté serveur (serveur back-end/bases de données).

Cela permet aux organisations d'héberger des applications puissantes avec un contrôle quasi total en temps réel sur leur conception et leurs fonctionnalités, tout en étant accessibles dans le monde entier. Quelques exemples d'applications web typiques incluent les services de messagerie en ligne comme `Gmail`, les détaillants en ligne comme `Amazon`, et les traitements de texte en ligne comme `Google Docs`.

https://www.hackthebox.eu/home/

![Tableau de bord affichant 932 joueurs en ligne, 1032 machines compromises, 622 défis réussis, et l'activité récente avec les cibles Lame, Emdee five for life, et Delivery.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/htb-web-app_1.jpg)

Les applications web ne sont pas exclusives aux fournisseurs géants comme Google ou Microsoft, mais peuvent être développées par n'importe quel développeur web et hébergées en ligne sur n'importe quel service d'hébergement courant, pour être utilisées par n'importe qui sur Internet. C'est pourquoi nous avons aujourd'hui des millions d'applications web sur Internet, avec des milliards d'utilisateurs qui interagissent avec elles chaque jour.

---

## Applications Web vs. Sites Web

Dans le passé, nous interagissions avec des sites web qui étaient statiques et ne pouvaient pas être modifiés en temps réel. Cela signifie que les sites web traditionnels étaient créés de manière statique pour représenter des informations spécifiques, et ces informations ne changeaient pas avec notre interaction. Pour modifier le contenu du site web, la page correspondante devait être éditée manuellement par les développeurs. Ces types de pages statiques ne contiennent pas de fonctions et, par conséquent, ne produisent pas de changements en temps réel. Ce type de site web est également connu sous le nom de [Web 1.0](https://en.wikipedia.org/wiki/Web_2.0#Web_1.0).

![Comparaison entre un site web et une application web : Le site web a des pages statiques, identiques pour tout le monde ; L'application web a des pages dynamiques et interactives, différentes pour chaque utilisateur.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/website_vs_webapps.jpg)

D'un autre côté, la plupart des sites web exécutent des applications web, ou [Web 2.0](https://en.wikipedia.org/wiki/Web_2.0), présentant un contenu dynamique basé sur l'interaction de l'utilisateur. Une autre différence significative est que les applications web sont entièrement fonctionnelles et peuvent exécuter diverses fonctionnalités pour l'utilisateur final, tandis que les sites web sont dépourvus de ce type de fonctionnalité. D'autres différences clés entre les sites web traditionnels et les applications web incluent :

- Être modulaires
- S'exécuter sur n'importe quelle taille d'écran
- S'exécuter sur n'importe quelle plateforme sans être optimisées

---

## Applications Web vs. Applications de Système d'Exploitation Natif

Contrairement aux applications de système d'exploitation natif (OS natif), les applications web sont indépendantes de la plateforme et peuvent s'exécuter dans un navigateur sur n'importe quel système d'exploitation. Ces applications web n'ont pas besoin d'être installées sur le système d'un utilisateur car ces applications web et leurs fonctionnalités sont exécutées à distance sur le serveur distant et ne consomment donc aucun espace sur le disque dur de l'utilisateur final.

Un autre avantage des applications web par rapport aux applications d'OS natif est l'unité de version. Tous les utilisateurs accédant à une application web utilisent la même version et la même application web, qui peut être continuellement mise à jour et modifiée sans avoir à pousser des mises à jour à chaque utilisateur. Les applications web peuvent être mises à jour à un seul endroit (le serveur web) sans développer différentes versions (builds) pour chaque plateforme, ce qui réduit considérablement les coûts de maintenance et de support en supprimant la nécessité de communiquer les changements à tous les utilisateurs individuellement.

D'un autre côté, les applications d'OS natif ont certains avantages par rapport aux applications web, principalement leur vitesse de fonctionnement et la capacité d'utiliser les bibliothèques du système d'exploitation natif et le matériel local. Comme les applications natives sont conçues pour utiliser les bibliothèques de l'OS natif, elles sont beaucoup plus rapides à charger et à interagir avec. De plus, les applications natives sont généralement plus capables que les applications web, car elles ont une intégration plus profonde avec le système d'exploitation et ne sont pas limitées aux seules capacités du navigateur.

Plus récemment, cependant, les applications web hybrides et progressives deviennent de plus en plus courantes. Elles utilisent des frameworks modernes pour exécuter des applications web en utilisant les capacités et les ressources de l'OS natif, ce qui les rend plus rapides que les applications web classiques et plus capables.

---

## Distribution des Applications Web

Il existe de nombreuses applications web open-source utilisées par des organisations du monde entier qui peuvent être personnalisées pour répondre aux besoins de chaque organisation. Parmi les applications web open-source courantes, on trouve :

- [WordPress](https://wordpress.com/)
- [OpenCart](https://www.opencart.com/)
- [Joomla](https://www.joomla.org/)

Il existe également des applications web propriétaires 'closed source', qui sont généralement développées par une organisation donnée puis vendues à une autre organisation ou utilisées par des organisations via un modèle d'abonnement. Parmi les applications web closed source courantes, on trouve :

- [Wix](https://www.wix.com/)
- [Shopify](https://www.shopify.com/)
- [DotNetNuke](https://www.dnnsoftware.com/)

---

## Risques de Sécurité des Applications Web

Les attaques d'applications web sont courantes et représentent un défi pour la plupart des organisations ayant une présence sur le web, quelle que soit leur taille. Après tout, elles sont généralement accessibles depuis n'importe quel pays par toute personne disposant d'une connexion Internet et d'un navigateur web, et offrent généralement une vaste surface d'attaque. Il existe de nombreux outils automatisés pour scanner et attaquer les applications web qui, entre de mauvaises mains, peuvent causer des dommages importants. À mesure que les applications web deviennent plus complexes et avancées, la possibilité que des vulnérabilités critiques soient intégrées dans leur conception augmente également.

Une attaque réussie contre une application web peut entraîner des pertes importantes et des interruptions d'activité massives. Étant donné que les applications web s'exécutent sur des serveurs qui peuvent héberger d'autres informations sensibles et sont souvent liées à des bases de données contenant des données utilisateur ou d'entreprise sensibles, toutes ces données pourraient être compromises si un site web est attaqué avec succès. C'est pourquoi il est essentiel pour toute entreprise qui utilise des applications web de tester correctement ces applications à la recherche de vulnérabilités et de les corriger rapidement, tout en vérifiant que le correctif résout la faille et n'introduit pas par inadvertance de nouvelles failles.

Le test de pénétration (penetration testing) d'applications web est une compétence de plus en plus essentielle à acquérir. Toute organisation cherchant à sécuriser ses applications web exposées sur Internet (et internes) devrait effectuer des tests d'applications web fréquents et mettre en œuvre des pratiques de codage sécurisé à chaque étape du cycle de vie du développement. Pour effectuer correctement des tests de pénétration sur des applications web, nous devons comprendre comment elles fonctionnent, comment elles sont développées, et quel type de risque se trouve à chaque couche et composant de l'application en fonction des technologies utilisées.

Nous rencontrerons toujours diverses applications web conçues et configurées différemment. L'une des méthodes les plus actuelles et largement utilisées pour tester les applications web est le [Guide de test de sécurité web de l'OWASP (OWASP Web Security Testing Guide)](https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing).

L'une des procédures les plus courantes consiste à commencer par examiner les composants front-end d'une application web, tels que `HTML`, `CSS` et `JavaScript` (également connus sous le nom de trinité front-end), et à tenter de trouver des vulnérabilités telles que l'exposition de données sensibles ([Sensitive Data Exposure](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure)) et le Cross-Site Scripting (XSS) ([Cross-Site Scripting (XSS)](https://owasp.org/www-project-top-ten/2017/A7_2017-Cross-Site_Scripting_\(XSS\))). Une fois que tous les composants front-end ont été testés de manière approfondie, nous examinons généralement les fonctionnalités de base de l'application web et l'interaction entre le navigateur et le serveur web pour énumérer les technologies utilisées par le serveur web et rechercher des failles exploitables. Nous évaluons généralement les applications web d'un point de vue non authentifié et authentifié (si l'application dispose d'une fonctionnalité de connexion) pour maximiser la couverture et examiner tous les scénarios d'attaque possibles.

---

## Attaquer les Applications Web

De nos jours, presque toutes les entreprises, quelle que soit leur taille, ont une ou plusieurs applications web dans leur périmètre externe. Ces applications peuvent aller de simples sites web statiques à des blogs alimentés par des systèmes de gestion de contenu (CMS) tels que `WordPress`, en passant par des applications complexes avec des fonctionnalités d'inscription/connexion prenant en charge divers rôles d'utilisateur, des utilisateurs de base aux super administrateurs. De nos jours, il n'est pas très courant de trouver un hôte exposé sur Internet directement exploitable via un exploit public connu (comme un service vulnérable ou une vulnérabilité d'exécution de code à distance (RCE) sur Windows), bien que cela arrive. Les applications web offrent une vaste surface d'attaque, et leur nature dynamique signifie qu'elles sont en constante évolution (et souvent négligées !). Une modification de code relativement simple peut introduire une vulnérabilité catastrophique ou une série de vulnérabilités qui peuvent être enchaînées pour obtenir un accès à des données sensibles ou une exécution de code à distance sur le serveur web ou d'autres hôtes de l'environnement, tels que les serveurs de base de données.

Il n'est pas rare de trouver des failles qui peuvent mener directement à l'exécution de code, comme un formulaire de téléversement de fichiers qui permet le téléversement de code malveillant ou une vulnérabilité d'inclusion de fichier (file inclusion) qui peut être exploitée pour obtenir une exécution de code à distance. Une vulnérabilité bien connue qui est encore assez répandue dans divers types d'applications web est l'injection SQL (SQL injection). Ce type de vulnérabilité provient de la gestion non sécurisée des entrées fournies par l'utilisateur. Elle peut entraîner l'accès à des données sensibles, la lecture/écriture de fichiers sur le serveur de base de données, et même l'exécution de code à distance.

Nous trouvons souvent des vulnérabilités d'injection SQL sur les applications web qui utilisent Active Directory pour l'authentification. Bien que nous ne puissions généralement pas exploiter cela pour extraire les mots de passe (puisqu'ils sont administrés par Active Directory), nous pouvons souvent récupérer la plupart ou la totalité des adresses e-mail des utilisateurs d'Active Directory, qui sont souvent les mêmes que leurs noms d'utilisateur. Ces données peuvent ensuite être utilisées pour effectuer une attaque par pulvérisation de mots de passe ([password spraying](https://us-cert.cisa.gov/ncas/current-activity/2019/08/08/acsc-releases-advisory-password-spraying-attacks)) contre les portails web qui utilisent Active Directory pour l'authentification, tels que le VPN ou Microsoft Outlook Web Access/Microsoft O365. Une pulvérisation de mots de passe réussie peut souvent aboutir à un accès à des données sensibles telles que des e-mails ou même à un point d'ancrage (foothold) directement dans l'environnement du réseau d'entreprise.

Cet exemple montre les dommages qui peuvent découler d'une seule vulnérabilité d'application web, en particulier lorsqu'elle est "enchaînée" pour extraire des données d'une application qui peuvent être utilisées pour attaquer d'autres parties de l'infrastructure externe d'une entreprise. Un professionnel de la sécurité de l'information (infosec) complet doit avoir une compréhension approfondie des applications web et être aussi à l'aise pour attaquer les applications web que pour effectuer des tests de pénétration de réseau et des attaques sur Active Directory. Un testeur de pénétration avec une base solide en applications web peut souvent se distinguer de ses pairs et trouver des failles que d'autres pourraient négliger. Voici quelques autres exemples concrets d'attaques d'applications web et leur impact :

|Faille|Scénario concret|
|---|---|
|[Injection SQL](https://owasp.org/www-community/attacks/SQL_Injection)|Obtention de noms d'utilisateur Active Directory et réalisation d'une attaque par pulvérisation de mots de passe contre un portail VPN ou de messagerie.|
|[Inclusion de fichier](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion)|Lecture du code source pour trouver une page ou un répertoire caché qui expose des fonctionnalités supplémentaires pouvant être utilisées pour obtenir une exécution de code à distance.|
|[Téléversement de fichier sans restriction (Unrestricted File Upload)](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)|Une application web qui permet à un utilisateur de téléverser une photo de profil mais autorise le téléversement de n'importe quel type de fichier (pas seulement des images). Cela peut être exploité pour obtenir le contrôle total du serveur de l'application web en téléversant du code malveillant.|
|[Référence directe non sécurisée à un objet (IDOR)](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)|Lorsqu'elle est combinée avec une faille telle qu'un contrôle d'accès défaillant, elle peut souvent être utilisée pour accéder aux fichiers ou aux fonctionnalités d'un autre utilisateur. Un exemple serait de modifier votre profil utilisateur en naviguant vers une page telle que /user/701/edit-profile. Si nous pouvons changer le `701` en `702`, nous pourrions modifier le profil d'un autre utilisateur !|
|[Contrôle d'accès défaillant (Broken Access Control)](https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control)|Un autre exemple est une application qui permet à un utilisateur de créer un nouveau compte. Si la fonctionnalité d'enregistrement de compte est mal conçue, un utilisateur peut effectuer une élévation de privilèges (privilege escalation) lors de l'inscription. Considérez la requête `POST` lors de l'enregistrement d'un nouvel utilisateur, qui soumet les données `username=bjones&password=Welcome1&email=bjones@inlanefreight.local&roleid=3`. Et si nous pouvions manipuler le paramètre `roleid` et le changer en `0` ou `1`. Nous avons vu des applications réelles où c'était le cas, et il était possible d'enregistrer rapidement un utilisateur administrateur et d'accéder à de nombreuses fonctionnalités non prévues de l'application web.|

Commencez à vous familiariser avec les attaques courantes d'applications web et leurs implications. Ne vous inquiétez pas si certains de ces termes vous semblent étrangers à ce stade ; ils deviendront plus clairs au fur et à mesure de votre progression et de l'application d'une approche itérative de l'apprentissage.

	Il est impératif d'étudier les applications web en profondeur et de se familiariser avec leur fonctionnement et les nombreuses piles applicatives différentes. Nous verrons des attaques d'applications web à plusieurs reprises au cours de notre parcours dans l'Académie, sur la plateforme principale de HTB, et lors d'évaluations en conditions réelles. Plongeons dans le sujet et apprenons la structure/fonction des applications web pour devenir des attaquants mieux informés, nous distinguer de nos pairs et trouver des failles que d'autres pourraient négliger.
---

[[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[02 - Structure d'une Application Web]] →
