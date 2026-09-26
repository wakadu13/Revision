---
tags:
  - web-applications
ordre: 3
---

# Front-end vs. Back-end

---

Nous avons peut-être entendu les [termes](https://en.wikipedia.org/wiki/Front_end_and_back_end) `front-end` et `back-end` pour le développement web, ou le terme [Full Stack](https://www.w3schools.com/whatis/whatis_fullstack.asp) qui désigne à la fois le développement web `front` et `back-end`. Ces termes deviennent synonymes de développement d'applications web, car ils constituent la majorité du cycle de développement web. Cependant, ces termes sont très différents l'un de l'autre, car chacun se réfère à une facette de l'application web, et chacun fonctionne et communique dans des domaines différents.

---

## Front-end

Le front-end d'une application web contient les composants de l'utilisateur directement via son navigateur web (côté client). Ces composants constituent le code source de la page web que nous voyons lorsque nous visitons une application web et incluent généralement `HTML`, `CSS` et `JavaScript`, qui sont ensuite interprétés en temps réel par nos navigateurs.

![Fenêtre de navigateur affichant des extraits de code HTML, CSS et JS pour la mise en page d'une page web.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/frontend-components.jpg)

Cela inclut tout ce que l'utilisateur voit et avec quoi il interagit, comme les éléments principaux de la page tels que le titre et le texte [HTML](https://www.w3schools.com/html/html_intro.asp), la conception et l'animation de tous les éléments [CSS](https://www.w3schools.com/css/css_intro.asp), et la fonction de chaque partie d'une page [JavaScript](https://www.w3schools.com/js/js_intro.asp).

Dans les applications web modernes, les composants front-end doivent s'adapter à n'importe quelle taille d'écran et fonctionner dans n'importe quel navigateur sur n'importe quel appareil. Cela contraste avec les composants back-end, qui sont généralement écrits pour une plateforme ou un système d'exploitation spécifique. Si le front-end d'une application web n'est pas bien optimisé, il peut rendre l'ensemble de l'application web lente et non réactive. Dans ce cas, certains utilisateurs peuvent penser que le serveur d'hébergement, ou leur connexion internet, est lent, alors que le problème se situe entièrement du côté client, au niveau du navigateur de l'utilisateur. C'est pourquoi le front-end d'une application web doit être optimisé pour la plupart des plateformes, des appareils (y compris les mobiles !) et des tailles d'écran.

Outre le développement de code front-end, voici quelques-unes des autres tâches liées au développement d'applications web front-end :

- Conception visuelle web
- Conception de l'interface utilisateur (UI)
- Conception de l'expérience utilisateur (UX)

Il existe de nombreux sites à notre disposition pour pratiquer le codage front-end. L'un d'eux est [celui-ci](https://html-css-js.com/). Ici, nous pouvons jouer avec l'[éditeur](https://htmlg.com/html-editor/), en tapant et en formatant du texte et en voyant le code `HTML`, `CSS` et `JavaScript` résultant être généré pour nous. Copiez/collez cet exemple TRÈS simple dans la partie droite de l'éditeur :

```html
<p><strong>Welcome to Hack The Box Academy</strong><strong></strong></p> <p></p> <p><em>This is some italic text.</em></p> <p></p> <p><span style="color: #0000ff;">This is some blue text.</span></p> <p></p> <p></p>
```

Regardez le code HTML simple s'afficher à gauche. Amusez-vous avec la mise en forme, les en-têtes, les couleurs, etc., et observez le code changer.

---

## Back-end

Le back-end d'une application web pilote toutes les fonctionnalités principales de l'application web, qui sont toutes exécutées sur le serveur back-end, lequel traite tout ce qui est nécessaire au bon fonctionnement de l'application web. C'est la partie que nous ne voyons ou avec laquelle nous n'interagissons peut-être jamais directement, mais un site web n'est qu'un ensemble de pages web statiques sans un back-end.

Il y a quatre composants principaux du back-end pour les applications web :

|**Composant**|**Description**|
|---|---|
|`Serveurs back-end`|Le matériel et le système d'exploitation qui hébergent tous les autres composants et qui fonctionnent généralement sur des systèmes d'exploitation comme `Linux`, `Windows`, ou en utilisant des `Conteneurs`.|
|`Serveurs Web`|Les serveurs web gèrent les requêtes et les connexions HTTP. Quelques exemples sont `Apache`, `NGINX`, et `IIS`.|
|`Bases de données`|Les bases de données (`DBs`) stockent et récupèrent les données de l'application web. Quelques exemples de bases de données relationnelles sont `MySQL`, `MSSQL`, `Oracle`, `PostgreSQL`, tandis que des exemples de bases de données non relationnelles incluent `NoSQL` et `MongoDB`.|
|`Frameworks de développement`|Les frameworks de développement sont utilisés pour développer le cœur de l'application web. Quelques frameworks bien connus incluent `Laravel` (`PHP`), `ASP.NET` (`C#`), `Spring` (`Java`), `Django` (`Python`), et `Express` (`NodeJS JavaScript`).|

![Diagramme montrant un serveur back-end fonctionnant sous Linux et Windows, connecté à un serveur web (Apache, NGINX, IIS), une application web (PHP, C#, Java) et une base de données (MySQL, MS SQL, Oracle).](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/backend-server.jpg)

Il est également possible d'héberger chaque composant du back-end sur son propre serveur isolé, ou dans des conteneurs isolés, en utilisant des services tels que [Docker](https://www.docker.com/). Pour maintenir une séparation logique et atténuer l'impact des vulnérabilités, différents composants de l'application web, comme la base de données, peuvent être installés dans un conteneur Docker, tandis que l'application web principale est installée dans un autre, isolant ainsi chaque partie des vulnérabilités potentielles qui pourraient affecter le ou les autres conteneurs. Il est également possible de séparer chacun dans son propre serveur dédié, ce qui peut être plus gourmand en ressources et plus long à maintenir. Cependant, cela dépend du cas d'utilisation métier et de la conception/fonctionnalité de l'application web en question.

Voici quelques-unes des tâches principales effectuées par les composants back-end :

- Développer la logique principale et les services du back-end de l'application web
- Développer le code principal et les fonctionnalités de l'application web
- Développer et maintenir la base de données back-end
- Développer et implémenter des bibliothèques à utiliser par l'application web
- Mettre en œuvre les besoins techniques/métiers de l'application web
- Implémenter les `API` principales pour les communications des composants front-end
- Intégrer des serveurs distants et des services cloud dans l'application web

---

## Sécurisation du Front-end/Back-end

Même si dans la plupart des cas, nous n'aurons pas accès au code du back-end pour analyser les fonctions individuelles et la structure du code, cela ne rend pas l'application invulnérable. Elle pourrait tout de même être exploitée par diverses attaques par injection, par exemple.

Supposons qu'une fonction de recherche dans une application web ne traite pas correctement nos requêtes de recherche par erreur. Dans ce cas, nous pourrions utiliser des techniques spécifiques pour manipuler les requêtes de manière à obtenir un accès non autorisé à des données spécifiques de la base de données [injections SQL](https://www.w3schools.com/sql/sql_injection.asp) ou même exécuter des commandes du système d'exploitation via l'application web, ce que l'on appelle également des [injections de commandes (Command Injections)](https://owasp.org/www-community/attacks/Command_Injection).

Nous verrons plus tard comment sécuriser chaque composant utilisé sur le front-end et le back-end. Lorsque nous avons un accès complet au code source des composants front-end, nous pouvons effectuer une revue de code pour trouver des vulnérabilités, ce qui fait partie de ce que l'on appelle le [test d'intrusion en boîte blanche (Whitebox Pentesting)](https://en.wikipedia.org/wiki/White-box_testing).

D'un autre côté, le code source des composants back-end est stocké sur le serveur back-end, nous n'y avons donc pas accès par défaut, ce qui nous oblige à n'effectuer que ce que l'on appelle un [test d'intrusion en boîte noire (Blackbox Pentesting)](https://en.wikipedia.org/wiki/Black-box_testing). Cependant, comme nous le verrons, certaines applications web sont open source, ce qui signifie que nous avons probablement accès à leur code source. De plus, certaines vulnérabilités telles que l'[inclusion de fichiers locaux (Local File Inclusion)](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion) pourraient nous permettre d'obtenir le code source depuis le serveur back-end. Avec ce code source en main, nous pouvons alors effectuer une revue de code sur les composants back-end pour mieux comprendre le fonctionnement de l'application, trouver potentiellement des données sensibles dans le code source (comme des mots de passe), et même trouver des vulnérabilités qui seraient difficiles ou impossibles à trouver sans accès au code source.

Les `20` erreurs les plus courantes que font les développeurs web et qui sont essentielles pour nous en tant que testeurs d'intrusion sont :

|**N°**|**Erreur**|
|---|---|
|`1.`|Autoriser l'entrée de données invalides dans la base de données|
|`2.`|Se concentrer sur le système dans son ensemble|
|`3.`|Établir des méthodes de sécurité développées personnellement|
|`4.`|Considérer la sécurité comme la dernière étape|
|`5.`|Développer un stockage de mots de passe en texte clair|
|`6.`|Créer des mots de passe faibles|
|`7.`|Stocker des données non chiffrées dans la base de données|
|`8.`|Dépendre excessivement du côté client|
|`9.`|Être trop optimiste|
|`10.`|Autoriser les variables via le nom de chemin de l'URL|
|`11.`|Faire confiance au code tiers|
|`12.`|Coder en dur des comptes de porte dérobée|
|`13.`|Injections SQL non vérifiées|
|`14.`|Inclusions de fichiers distants|
|`15.`|Manipulation non sécurisée des données|
|`16.`|Ne pas chiffrer correctement les données|
|`17.`|Ne pas utiliser un système cryptographique sécurisé|
|`18.`|Ignorer la couche 8|
|`19.`|Examen des actions des utilisateurs|
|`20.`|Mauvaises configurations du pare-feu d'application web|

Ces erreurs mènent aux vulnérabilités du [Top 10 de l'OWASP](https://owasp.org/www-project-top-ten/) pour les applications web, que nous aborderons dans d'autres modules :

|**N°**|**Vulnérabilité**|
|---|---|
|`1.`|Rupture du contrôle d'accès|
|`2.`|Défaillances cryptographiques|
|`3.`|Injection|
|`4.`|Conception non sécurisée|
|`5.`|Mauvaise configuration de la sécurité|
|`6.`|Composants vulnérables et obsolètes|
|`7.`|Défaillances d'identification et d'authentification|
|`8.`|Défaillances de l'intégrité des logiciels et des données|
|`9.`|Défaillances de la journalisation et de la surveillance de la sécurité|
|`10.`|Falsification de requête côté serveur (SSRF)|

Il est important de commencer à se familiariser avec ces failles et vulnérabilités car elles constituent la base de nombreux problèmes que nous aborderons dans les futurs modules liés au web et même non liés au web. En tant que pentesters, nous devons avoir la capacité d'identifier, d'exploiter et d'expliquer avec compétence ces vulnérabilités pour nos clients.
---

← [[02 - Structure d'une Application Web]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[04 - HTML]] →
