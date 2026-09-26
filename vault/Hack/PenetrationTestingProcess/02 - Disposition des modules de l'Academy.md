---
tags:
  - pentest-process
ordre: 2
---

# Disposition des modules de l'Academy

---

Hack The Box a été initialement créé pour offrir aux professionnels de la tech un endroit sûr pour pratiquer et développer leurs compétences en hacking, et n'était pas idéalement adapté aux débutants qui commençaient leur parcours en TI/Sécurité. Hack The Box a commencé comme une plateforme de CTF (Capture The Flag) compétitive avec un mélange de machines et de challenges, chacun attribuant un nombre de points variable en fonction de la difficulté, à résoudre selon une approche en « boîte noire » (black box), sans solution pas à pas, ni guide, ni même d'indices. Au fur et à mesure de l'évolution de la plateforme, nous avons constaté le besoin de contenu plus adapté aux débutants et d'une approche d'apprentissage guidée pour compléter le côté compétitif de la plateforme. C'est avec cet objectif en tête que HTB Academy est née. Nous visons à fournir du contenu adapté aux débutants tout en aidant les praticiens de niveau intermédiaire et avancé à monter en compétences dans divers domaines. Nous proposons également Starting Point sur la plateforme HTB principale, qui vise à aider les utilisateurs à se familiariser avec l'attaque de cibles individuelles en utilisant une approche guidée, pour finalement passer à la résolution de machines de manière autonome et même à participer aux machines compétitives. Chaque personne a probablement sa propre opinion sur HTB, et cela peut ne pas convenir à tout le monde. Cependant, nous aimerions prendre le temps d'expliquer notre point de vue en tant que spécialistes expérimentés en TI issus de divers domaines, avec de nombreuses années d'expérience combinée et des parcours différents, de débutants à là où nous en sommes aujourd'hui.

Les TI (Technologies de l'Information) sont une fonction commerciale majeure de la plupart des organisations, axée sur la création, l'administration et le support de la technologie informatique utilisée par les organisations pour accomplir leur mission. Le terme TI est souvent utilisé pour englober de nombreuses sous-disciplines spécialisées comme la Cybersécurité, la Sécurité de l'Information, le Développement Logiciel, l'Administration de Bases de Données, l'Administration Réseau, et plus encore. Pour devenir « bon » dans ce domaine, il faut une pratique et des efforts considérables. La cybersécurité peut être une discipline très exigeante car elle requiert les connaissances de base nécessaires à un spécialiste en TI typique, ainsi qu'une compréhension beaucoup plus approfondie de tous les domaines (réseautique, administration des systèmes Linux et Windows, scripting, bases de données, etc.). Nous n'avons pas besoin d'être des experts dans chaque domaine des TI. Cependant, plus nous avons d'expérience et de connaissances, plus notre travail en tant que spécialiste de la sécurité informatique ou testeur d'intrusion (penetration tester) deviendra facile. Nous ne pouvons pas travailler en toute confiance en tant que testeurs d'intrusion si nous n'avons pas une compréhension approfondie des technologies que nous évaluons. Par exemple, un développeur web se concentre uniquement sur le développement d'applications et de sites web. Cela nécessite généralement des connaissances en HTML, JavaScript, CSS, SQL et des langages de programmation côté serveur, tels que PHP. Même si le développeur a plus de dix ans d'expérience dans son domaine, il suffit d'une seule erreur pour que tout le serveur web devienne inutilisable ou que des données soient volées. En tant qu'attaquant, l'astuce consiste à trouver un moyen d'identifier et d'exploiter ces erreurs.

Dans cette optique, nous avons posé des bases pour nos étudiants car, d'après notre expérience, il est difficile de savoir par où commencer. Nous avons structuré et construit notre matériel d'apprentissage de manière à ce qu'il puisse paraître difficile `au début`, mais avec le temps, vous réaliserez que c'est le moyen le plus simple et le plus efficace d'enseigner une matière aussi complexe de manière efficiente. Nous voulons rendre le processus d'apprentissage aussi simple et efficace que possible tout en insistant sur les fondamentaux et en y revenant à plusieurs reprises. Par exemple, beaucoup de nos tâches sont conçues pour vous amener à penser d'une certaine manière. Nous faisons cela pour vous aider à développer les compétences analytiques essentielles qui sont impératives pour réussir dans un domaine qui peut comporter tant d'incertitude. Nous voulons aider à former des professionnels qui voient les choses différemment et qui remettent tout en question, ce qui peut finalement aider à apporter plus de valeur aux clients si vous êtes capable de trouver des problèmes subtils que d'autres testeurs manquent. Nous ne pouvons pas enseigner les compétences analytiques et la capacité à creuser plus profondément et à « tout remettre en question » en un seul module ou parcours. Cela peut être comparé à jouer d'un instrument de musique. On ne peut pas apprendre à bien jouer de la guitare sans une pratique considérable. On peut tout apprendre sur une guitare, l'histoire des guitares, le nom de chaque composant, etc., mais si on en prend une sans pratique, on ne sera pas capable de produire une musique équivalente à notre connaissance des guitares. C'est la même chose dans le domaine des tests d'intrusion. Nous pouvons tout savoir sur l'histoire des ordinateurs et être capables de décrire chaque composant, mais sans une expérience pratique approfondie, nous ne serons pas en mesure d'effectuer des tests d'intrusion à un haut niveau.

Le reste de cette section expliquera comment nous avons structuré les modules de la manière dont nous l'avons fait pour vous donner un aperçu de notre processus de pensée et de notre philosophie d'enseignement. Notre objectif principal est de créer des ressources de formation engageantes et responsabilisantes qui profitent aux individus de `TOUS` les niveaux de compétence.

La liste des modules présentée correspond à la séquence que nous recommandons de suivre pour les débutants ou les utilisateurs avancés qui sont « bloqués », afin de s'améliorer dans des domaines spécifiques à chaque étape du processus de test d'intrusion.

![Diagramme du processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process.png)

---

## Pré-engagement

L'étape de pré-engagement est celle où les principaux engagements, tâches, périmètres, limitations et accords connexes sont documentés par écrit. Au cours de cette étape, les documents contractuels sont rédigés et les informations essentielles sont échangées, celles-ci étant pertinentes pour les testeurs d'intrusion et le client, en fonction du type d'évaluation.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-PRE.png)

Il n'y a qu'un seul chemin que nous pouvons emprunter à partir d'ici :

|**Parcours**|**Description**|
|---|---|
|`Collecte d'informations`|Ensuite, nous passons à l'étape de `Collecte d'informations`. Avant que les systèmes cibles puissent être examinés et attaqués, nous devons d'abord les identifier. Il se peut que le client ne nous donne aucune information sur son réseau et ses composants, à l'exception d'un nom de domaine ou simplement d'une liste d'adresses IP/plages réseau dans le périmètre. Par conséquent, nous devons obtenir une vue d'ensemble de la ou des applications web cibles ou du réseau avant de poursuivre.|

À cette étape du processus, nous devrions avoir une base solide qui peut être construite grâce aux modules fondamentaux suivants :

#### 1. Learning Process

|||
|---|---|
|[![Logo du module pour le module Learning Process.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b1-fa22-4873-b302-f256190a590c.png)](https://academy.hackthebox.com/module/details/9)|Pour acquérir ces connaissances aussi rapidement et aussi bien que possible, nous devons savoir comment fonctionne le `Processus d'Apprentissage` (Learning Process) d'un être humain et comment éviter les obstacles durant le processus. Dans ce module, nous apprenons l'art du fonctionnement de notre cerveau et comment nous pouvons utiliser ces connaissances pour augmenter considérablement notre efficacité d'apprentissage.<br><br>Niveau 0FondamentalGénéral12 Sections+103 heures|

De plus, nous avons besoin de connaissances fondamentales sur les systèmes d'exploitation les plus utilisés au monde. Cela inclut les systèmes d'exploitation `Linux` et `Windows`. Avant d'attaquer ces systèmes, nous devons d'abord savoir comment ils fonctionnent, afin de pouvoir ensuite apprendre comment les exploiter au mieux.

#### 2. Linux Fundamentals

|||
|---|---|
|[![Logo du module pour le module Linux Fundamentals.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-0cdb-4d14-8327-32b04a235731.png)](https://academy.hackthebox.com/module/details/18)|Linux est l'un des systèmes d'exploitation les plus stables aujourd'hui, et omniprésent dans les réseaux d'entreprise. `Linux Fundamentals` est essentiel pour que nous apprenions sa structure et puissions prendre les mesures appropriées pour atteindre nos objectifs.<br><br>Niveau 0FondamentalGénéral18 Sections+106 heures|

#### 3. Windows Fundamentals

|||
|---|---|
|[![Logo du module pour le module Windows Fundamentals.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-8a54-4ce5-ba30-40a8d77966dd.png)](https://academy.hackthebox.com/module/details/49)|D'un autre côté, Windows est l'un des systèmes d'exploitation les plus conviviaux que la plupart des entreprises trouvent dans leur infrastructure informatique. Il est essentiel de comprendre les `Windows Fundamentals` pour pouvoir manipuler le système d'exploitation de la meilleure façon possible et atteindre les résultats souhaités.<br><br>Niveau 0FondamentalGénéral14 Sections+106 heures|

Tous les systèmes connectés communiquent via différents réseaux, routes et protocoles sur Internet ou sur le réseau interne. Pour comprendre comment les systèmes interconnectés fonctionnent et communiquent, nous devons travailler sur certains composants théoriques pour comprendre les fonctionnalités clés et les termes spécifiques.

#### 4. Introduction to Networking

|||
|---|---|
|[![Logo du module pour le module Introduction to Networking.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-57e7-4393-8bac-c0a5ef21369e.png)](https://academy.hackthebox.com/module/details/34)|La majeure partie du monde de l'information est interconnectée, et comprendre comment les hôtes communiquent et se trouvent sur Internet et au sein des réseaux internes est un autre élément fondamental que nous devons maîtriser. Sans une compréhension approfondie de la `Réseautique` (Networking), nous ne serons pas efficaces dans l'évaluation des systèmes interconnectés.<br><br>Niveau 0FondamentalGénéral12 Sections+103 heures|

Les applications web représentent une catégorie distincte. Nous sommes à l'aise avec l'utilisation d'un navigateur web et la navigation sur des sites web. Mais que se passe-t-il en coulisses lorsque nous interagissons avec une application web ? Avant d'attaquer les applications web, nous devons nous concentrer sur leur fonctionnement et les processus qui se déroulent en arrière-plan lors de l'utilisation d'une application web.

#### 5. Introduction to Web Applications

|||
|---|---|
|[![Logo du module pour le module Introduction to Web Applications.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-0b41-4144-a53a-406c73ac8f7d.png)](https://academy.hackthebox.com/module/details/75)|La réseautique informatique sur Internet est standardisée sur de nombreuses couches et protocoles. Le type d'applications le plus utilisé sont les `Applications Web`. Celles-ci sont conçues pour que tout utilisateur disposant d'un navigateur et d'une connexion Internet puisse accéder aux pages web sur Internet.<br><br>Niveau 0FondamentalGénéral17 Sections+103 heures|

#### 6. Web Requests

|||
|---|---|
|[![Logo du module pour le module Web Requests.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-5c15-42c4-a555-bf54bfbe2585.png)](https://academy.hackthebox.com/module/details/35)|La communication se fait par différents types de `Requêtes Web` (Web Requests), que l'application web traite avec des fonctions spécifiques. Nous couvrirons différents types de requêtes web et comment les navigateurs web les utilisent en arrière-plan. Certaines mauvaises configurations du serveur web peuvent même nous donner accès au système sans avoir à exploiter directement une application web.<br><br>Niveau 0FondamentalGénéral8 Sections+104 heures|

#### 7. JavaScript Deobfuscation

|||
|---|---|
|[![Logo du module pour le module JavaScript Deobfuscation.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-6be9-4730-aabf-503b8fbefe2b.png)](https://academy.hackthebox.com/module/details/41)|La plupart des applications web de nos jours sont dynamiques et incluent `JavaScript`, avec lequel nous devons également être familiers pour gérer correctement la dynamique de la page web. JavaScript est un langage de programmation très populaire et est souvent obfusqué pour rendre difficile pour les attaquants (et les défenseurs) de comprendre la fonctionnalité exacte du code.<br><br>Niveau 0FondamentalDéfensif11 Sections+104 heures|

Comme nous le savons, les grands réseaux informatiques doivent être gérés et sécurisés de près. La plupart des entreprises ont une structure de gestion, car la gestion de centaines ou de milliers de systèmes à distance ou physiquement, un par un, serait déraisonnable. Pour cette raison, diverses technologies existent pour faciliter et accélérer la gestion à distance des utilisateurs, des systèmes et d'autres ressources.

#### 8. Introduction to Active Directory

|||
|---|---|
|[![Logo du module pour le module Introduction to Active Directory.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-05a4-4a27-88a3-188f4c4e02aa.png)](https://academy.hackthebox.com/module/details/74)|De nos jours, la plupart des entreprises utilisent une méthode structurée pour gérer des centaines ou des milliers d'ordinateurs et d'utilisateurs. `Active Directory` est utilisé pour simplifier et accélérer la gestion pour les administrateurs.<br><br>Niveau 0FondamentalGénéral16 Sections+107 heures|

#### 9. Getting Started

|||
|---|---|
|[![Logo du module pour le module Getting Started.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-168c-489f-a560-b1e406f8acfa.png)](https://academy.hackthebox.com/module/details/77)|Qu'est-ce qui cause la plus grande difficulté pour la plupart des gens au début ? La réponse à cette question est beaucoup plus simple que la plupart ne l'imaginent, car tout ce que nous avons à faire est de `Commencer` (Get Started). Ce module comprend de nombreux conseils et astuces pour ceux qui débutent, des exemples des technologies que nous verrons et des méthodes d'attaque que nous utiliserons, ainsi qu'une solution guidée pour résoudre une machine vulnérable, aboutissant à la résolution (pour certains d'entre nous) de notre première machine sans assistance.<br><br>Niveau 0FondamentalOffensif23 Sections+108 heures|

---

## Collecte d'informations

La collecte d'informations est une partie essentielle de toute évaluation. Parce que l'information, la connaissance qui en découle, les conclusions que nous tirons et les mesures que nous prenons sont basées sur les informations disponibles. Ces informations doivent être obtenues de quelque part, il est donc essentiel de savoir comment les récupérer et les exploiter au mieux en fonction de nos objectifs d'évaluation.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-IG.png)

À partir de cette étape, la suite de notre parcours est claire :

|**Parcours**|**Description**|
|---|---|
|`Évaluation des vulnérabilités`|La prochaine étape de notre voyage est l'`Évaluation des vulnérabilités`, où nous utilisons les informations trouvées pour identifier les faiblesses potentielles. Nous pouvons utiliser des scanners de vulnérabilités qui analyseront les systèmes cibles à la recherche de vulnérabilités connues, ainsi qu'une analyse manuelle où nous essayons de regarder en coulisses pour découvrir où les vulnérabilités potentielles pourraient se trouver.|

Les informations que nous recueillons à l'avance influenceront les résultats de l'étape d'`Exploitation`. À partir de là, nous pouvons voir si nous en avons collecté assez ou si nous avons creusé assez profondément. Le temps, la patience et l'engagement personnel jouent tous un rôle important dans la collecte d'informations. C'est à ce moment que de nombreux testeurs d'intrusion ont tendance à se lancer directement dans l'exploitation d'une vulnérabilité potentielle. Cela échoue souvent et peut entraîner, entre autres, une perte de temps considérable. Avant de tenter d'exploiter quoi que ce soit, nous devrions avoir terminé une collecte d'informations approfondie, en prenant des notes détaillées en cours de route, en nous concentrant sur les éléments à approfondir une fois que nous arriverons à l'étape de l'exploitation. La plupart des évaluations sont basées sur le temps, nous ne voulons donc pas perdre de temps à nous éparpiller, ce qui pourrait nous faire manquer quelque chose de critique. L'organisation et la patience sont essentielles, tout en étant aussi minutieux que possible.

#### 10. Network Enumeration with Nmap

|||
|---|---|
|[![Logo du module pour le module Network Enumeration with Nmap.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-10b4-4bad-8327-7ab3f1c27e46.png)](https://academy.hackthebox.com/module/details/19)|Si nous limitons notre périmètre à l'infrastructure réseau de l'entreprise, nous devrions savoir comment effectuer l'`Énumération réseau avec Nmap` (Network Enumeration with Nmap), identifier les cibles potentielles et contourner les mesures de sécurité comme les pare-feu, les systèmes de prévention et de détection d'intrusion (IPS/IDS).<br><br>Niveau IFacileOffensif12 Sections+107 heures|

#### 11. Footprinting

|||
|---|---|
|[![Logo du module pour le module Footprinting.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-94ef-464c-a139-d250c792f69d.png)](https://academy.hackthebox.com/module/details/112)|Une fois que nous avons identifié les cibles potentielles, nous devons savoir comment les services individuels de ces hôtes peuvent être examinés. Il est essentiel de comprendre à quoi servent ces services, comment ils peuvent être mal configurés et comment nous, en tant qu'attaquants, pouvons les exploiter à nos fins. Parce que chaque service qui communique via le réseau laisse sa propre `empreinte` (Footprint) que nous devons découvrir. Connaître ces empreintes nous donnera une image plus précise des prochaines étapes que nous pourrons entreprendre alors que nous nous dirigeons vers la phase d'exploitation.<br><br>Niveau IIMoyenOffensif20 Sections+202 jours|

#### 12. Information Gathering - Web Edition

|||
|---|---|
|[![Logo du module pour le module Information Gathering - Web Edition.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-ec50-4c29-9823-f0be48c20cb2.png)](https://academy.hackthebox.com/module/details/144)|Dans la plupart des cas, les serveurs web et les applications web contiennent une grande quantité d'informations qui peuvent être utilisées contre eux. Étant donné que le web est un vaste domaine technique à part entière, il sera traité séparément. Un serveur web peut exécuter de nombreuses applications web, et certaines de ces applications peuvent être uniquement destinées aux développeurs et aux administrateurs. Par conséquent, les trouver est une partie essentielle de notre `Information Gathering - Web Edition`. Nous voulons également découvrir autant d'applications web que possible et recueillir des informations détaillées sur leur structure et leur fonction, ce qui aidera à informer nos attaques.<br><br>Niveau IIFacileOffensif10 Sections+207 heures|

Les choses peuvent devenir assez complexes lorsque nous voulons trouver des informations sur une entreprise cible sur Internet. Après tout, passer au crible diverses sources et plateformes de médias sociaux prend du temps et nécessite beaucoup d'attention et de patience.

#### 13. OSINT: Corporate Recon

|||
|---|---|
|[![Logo du module pour le module OSINT: Corporate Recon.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-3f6d-46fd-979b-c8d8fdaf5ce2.png)](https://academy.hackthebox.com/module/details/28)|Ce type de recherche est appelé renseignement en sources ouvertes (OSINT) et comporte de nombreuses sous-catégories. En résumé, ce processus consiste à recueillir des informations à partir de toutes les sources publiquement disponibles. `OSINT: Corporate Recon`, nous donne une approche claire et structurée qui nous permettra de travailler à travers de nombreux types de données et de sources d'information. Un exemple simple serait de trouver une clé SSH privée qui nous permet de nous connecter au réseau de l'entreprise en tant qu'administrateur.<br><br>Niveau IVDifficileOffensif23 Sections+2002 jours|

---

## Évaluation des vulnérabilités

L'étape de l'évaluation des vulnérabilités est divisée en deux domaines. D'une part, c'est une approche pour scanner les vulnérabilités connues à l'aide d'outils automatisés. D'autre part, c'est une analyse des vulnérabilités potentielles à travers les informations trouvées. De nombreuses entreprises effectuent régulièrement des audits d'évaluation des vulnérabilités pour vérifier leur infrastructure à la recherche de nouvelles vulnérabilités connues et les comparer avec les dernières entrées dans les bases de données de ces outils.

Une analyse consiste davantage à `penser hors des sentiers battus`. Nous essayons de découvrir des lacunes et des opportunités pour tromper les systèmes et les applications à notre avantage et obtenir un accès ou des privilèges non intentionnels. Cela nécessite de la créativité et une compréhension technique approfondie. Nous devons relier les différents points d'information que nous obtenons et comprendre ses processus.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-VA.png)

À partir de cette étape, il y a quatre chemins que nous pouvons emprunter, en fonction de notre avancement :

|**Parcours**|**Description**|
|---|---|
|`Exploitation`|Le premier dans lequel nous pouvons nous lancer est l'étape d'`Exploitation`. Cela se produit lorsque nous n'avons pas encore accès à un système ou à une application. Bien sûr, cela suppose que nous ayons déjà identifié au moins une lacune et préparé tout le nécessaire pour tenter de l'exploiter.|
|`Post-exploitation`|Le deuxième chemin mène à l'étape de `Post-exploitation`, où nous effectuons une escalade de privilèges sur le système cible. Cela suppose que nous sommes déjà sur le système cible et que nous pouvons interagir avec lui.|
|`Mouvement latéral`|Notre troisième option est l'étape du `Mouvement latéral`, où nous nous déplaçons du système déjà exploité à travers le réseau et attaquons d'autres systèmes. Encore une fois, cela suppose que nous soyons déjà sur un système cible et que nous puissions interagir avec lui. Cependant, l'escalade de privilèges n'est pas strictement nécessaire car l'interaction avec le système nous permet déjà de nous déplacer plus loin dans le réseau dans certaines circonstances. D'autres fois, nous devrons effectuer une escalade de privilèges avant de nous déplacer latéralement. Chaque évaluation est différente.|
|`Collecte d'informations`|La dernière option est de retourner à l'étape de `Collecte d'informations` lorsque nous n'avons pas assez d'informations à disposition. Ici, nous pouvons creuser plus profondément pour trouver plus d'informations qui nous donneront une vue plus précise.|

La capacité d'analyse vient avec le temps et l'expérience. Cependant, elle doit également être entraînée car une analyse correcte établit des liens entre différents points et informations. Connecter ces informations sur le réseau cible ou le système cible et notre expérience nous permettra souvent de reconnaître des schémas spécifiques. Nous pouvons comparer cela à la lecture. Une fois que nous avons lu certains mots assez souvent, nous connaîtrons ce mot à un moment donné et comprendrons ce qu'il signifie simplement en regardant les lettres.

#### 14. Vulnerability Assessment

|||
|---|---|
|[![Logo du module pour le module Vulnerability Assessment.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-8105-4d45-921b-ba91d6392842.png)](https://academy.hackthebox.com/module/details/108)|Après avoir résumé les informations, nous pouvons utiliser des outils automatisés pour scanner les cibles définies afin de détecter les vulnérabilités connues dans les systèmes. Cependant, nous devons d'abord connaître les systèmes de notation et apprendre à configurer et à utiliser ces outils efficacement. L'`Évaluation des vulnérabilités` (Vulnerability Assessment) effectuée par ces outils peut nous donner un meilleur aperçu des vulnérabilités potentielles et de la configuration du système cible. À partir de là, de nouvelles voies et opportunités peuvent nous être révélées pour nous aider à trouver un autre chemin vers le système.<br><br>Niveau 0FacileOffensif17 Sections+102 heures|

#### 15. File Transfers

|||
|---|---|
|[![Logo du module pour le module File Transfers.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-2d86-459b-b86a-ab1e879880c1.png)](https://academy.hackthebox.com/module/details/24)|Avant de pouvoir exploiter efficacement les vulnérabilités potentielles, nous devons être familiers avec les techniques et méthodes pour transférer les données requises vers les systèmes cibles. C'est parce que des ajustements manuels sont souvent nécessaires pour contourner des restrictions spécifiques. Connaître les moyens et les méthodes pour effectuer des `Transferts de fichiers` (File Transfers) est un composant essentiel que nous devons maîtriser et il existe de nombreuses façons de transférer des fichiers vers et depuis des hôtes Windows et Linux. Si nous avons trouvé une faille potentielle et ne savons pas comment transférer les données correspondantes vers le système cible, cela nous mènera à une impasse.<br><br>Niveau 0MoyenOffensif8 Sections+103 heures|

#### 16. Shells & Payloads

|||
|---|---|
|[![Logo du module pour le module Shells & Payloads.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-9deb-4da0-9951-ae99f8c703c5.png)](https://academy.hackthebox.com/module/details/115)|Nous devons également savoir quels fichiers nous devons transférer pour obtenir un accès initial ou supplémentaire aux systèmes. Pour cela, il est nécessaire de savoir ce que sont les `Shells & Payloads` (charges utiles). À l'aide des charges utiles transmises, nous obtenons un accès à la ligne de commande du système cible. De nombreuses choses doivent être prises en considération car ces shells et charges utiles doivent être adaptés à l'environnement et au système ciblé.<br><br>Niveau IMoyenOffensif17 Sections+102 jours|

#### 17. Using the Metasploit-Framework

|||
|---|---|
|[![Logo du module pour le module Using the Metasploit-Framework.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-63e9-457e-b924-710dbe278ef7.png)](https://academy.hackthebox.com/module/details/39)|De plus, il existe un framework très pratique appelé `Metasploit-Framework` qui couvre de nombreuses attaques, méthodes d'énumération et d'escalade de privilèges et nous permet de configurer et d'exécuter plus rapidement. Il peut nous aider à accélérer nos processus et à pénétrer les systèmes cibles de manière semi-automatisée. Cependant, avant de pouvoir faire cela, nous devons comprendre ce dont cet outil est capable et ses limitations.<br><br>Niveau 0FacileOffensif15 Sections+105 heures|

---

## Exploitation

L'exploitation est l'attaque effectuée contre un système ou une application basée sur la vulnérabilité potentielle découverte lors de notre collecte d'informations et de notre énumération. Nous utilisons les informations de l'étape de `Collecte d'informations`, les analysons dans l'étape d'`Évaluation des vulnérabilités` et préparons les attaques potentielles. Souvent, de nombreuses entreprises et systèmes utilisent les mêmes applications mais prennent des décisions différentes concernant leur configuration. C'est parce que la même application peut souvent être utilisée à des fins diverses, et chaque organisation aura des objectifs différents.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-EX.png)

À partir de cette étape, il y a quatre chemins que nous pouvons emprunter, en fonction de notre avancement :

|**Parcours**|**Description**|
|---|---|
|`Collecte d'informations`|Une fois que nous avons un accès initial au système cible, quel que soit le niveau de nos privilèges à ce moment-là, nous devons recueillir des informations sur le système local. Peu importe que nous utilisions ces nouvelles informations pour une escalade de privilèges, un mouvement latéral ou une exfiltration de données. Par conséquent, avant de pouvoir prendre d'autres mesures, nous devons découvrir à quoi nous avons affaire. Cela nous amène inévitablement à l'étape de l'évaluation des vulnérabilités, où nous analysons et évaluons les informations que nous trouvons.|
|`Post-exploitation`|La `Post-exploitation` consiste principalement à effectuer une escalade de privilèges si nous n'avons pas encore atteint les droits les plus élevés possibles sur l'hôte cible. Comme nous le savons, plus d'opportunités s'offrent à nous avec des privilèges plus élevés. Ce parcours inclut en fait les étapes `Collecte d'informations`, `Évaluation des vulnérabilités`, `Exploitation` et `Mouvement latéral`, mais d'un point de vue interne sur le système cible. Le saut direct vers la post-exploitation est moins fréquent, mais il arrive. Car grâce à l'étape d'exploitation, nous avons peut-être déjà obtenu les privilèges les plus élevés, et à partir de là, nous recommençons à la `Collecte d'informations`.|
|`Mouvement latéral`|À partir d'ici, nous pouvons également passer directement au `Mouvement latéral`. Cela peut se produire dans différentes conditions. Si nous avons atteint les privilèges les plus élevés sur un système à double interface réseau (dual-homed) utilisé pour connecter deux réseaux, nous pouvons probablement utiliser cet hôte pour commencer à énumérer des hôtes qui n'étaient pas disponibles auparavant.|
|`Preuve de concept`|Nous pouvons emprunter le dernier chemin après avoir obtenu les privilèges les plus élevés en exploitant un système interne. Bien sûr, nous n'avons pas nécessairement à avoir pris le contrôle de tous les systèmes. Cependant, si nous avons obtenu les privilèges d'Administrateur de Domaine dans un environnement Active Directory, nous pouvons probablement nous déplacer librement sur l'ensemble du réseau et effectuer toutes les actions que nous pouvons imaginer. Nous pouvons donc créer la `Preuve de concept` (Proof-of-Concept) à partir de nos notes pour détailler et potentiellement automatiser les chemins et les activités et les mettre à la disposition du service technique.|

Cette étape est si complète qu'elle a été divisée en deux domaines distincts. La première catégorie concerne les protocoles réseau généraux souvent utilisés et présents dans presque tous les réseaux. L'exploitation réelle des vulnérabilités potentielles et existantes est basée sur l'adaptabilité et la connaissance des différents protocoles réseau auxquels nous serons confrontés. De plus, nous devons être capables de créer une vue d'ensemble du réseau existant pour comprendre les objectifs de ses composants individuels. Dans la plupart des cas, les serveurs et applications web contiennent une grande quantité d'informations qui peuvent être utilisées contre eux. Comme indiqué précédemment, étant donné que le web est un vaste domaine technique à part entière, il sera traité séparément. Nous nous intéressons également aux services exposés à distance fonctionnant sur les hôtes cibles, car ceux-ci peuvent présenter des mauvaises configurations ou des vulnérabilités publiques connues que nous pouvons exploiter pour un accès initial. Enfin, les utilisateurs existants jouent également un rôle important dans le réseau global.

#### 18. Password Attacks

|||
|---|---|
|[![Logo du module pour le module Password Attacks.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b5-1d5c-40e5-8fe8-08850d03139f.png)](https://academy.hackthebox.com/module/details/147)|Si des noms d'utilisateur ou des mots de passe potentiels ont été trouvés lors de notre collecte d'informations, nous pourrons peut-être les utiliser spécifiquement pour effectuer des `Attaques de mots de passe` (Password Attacks) sur les systèmes et les applications et nous authentifier. Ce module couvre diverses méthodes pour obtenir des informations d'identification à distance et localement sur les systèmes Windows et Linux.<br><br>Niveau IMoyenOffensif18 Sections+108 heures|

#### 19. Attacking Common Services

|||
|---|---|
|[![Logo du module pour le module Attacking Common services.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-a220-42dd-82a0-4e1a81e1a739.png)](https://academy.hackthebox.com/module/details/116)|En raison de la variété des attaques qui peuvent être menées, les attaques sur des services réseau spécifiques et des applications web diffèrent. Par conséquent, elles sont séparées en différents modules, car de nombreuses attaques spécifiques ne peuvent être menées que contre des applications web. Cependant, il existe de nombreux services réseau essentiels que l'on peut presque toujours trouver dans n'importe quel réseau d'entreprise. Par conséquent, savoir comment `attaquer les services courants` (Attacking Common Services) est un autre concept majeur qui doit être couvert en détail.<br><br>Niveau IIMoyenOffensif19 Sections+208 heures|

#### 20. Pivoting, Tunneling & Port Forwarding

|||
|---|---|
|[![Logo du module pour le module Pivoting, Tunneling & Port Forwarding.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b5-44c9-456a-9bab-10b3e9696565.png)](https://academy.hackthebox.com/module/details/158)|Lors du `Pivotage` (Pivoting), le système exploité est utilisé comme un nœud entre les réseaux externes et internes ou entre différents réseaux internes. Ceci est utilisé pour communiquer avec les systèmes internes auxquels nous ne pouvons généralement pas établir de connexion directe depuis Internet ou un autre hôte du réseau interne. Peu importe que ceux-ci soient hébergés sur site (on-premise) ou dans le cloud. L'accès au réseau et les restrictions peuvent être configurés vers et depuis des hôtes spécifiques, même dans le cloud. Des `Tunnels` (Tunneling) doivent également être créés pour pouvoir transférer des données en toute sécurité. La `Redirection de port` (Port forwarding) est souvent utilisée pour transférer un port local vers le port d'un système exploité.<br><br>Niveau IIMoyenOffensif18 Sections+202 jours|

#### 21. Active Directory Enumeration & Attacks

|||
|---|---|
|[![Logo du module pour le module Active Directory Enumeration & Attacks.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-e6cf-404a-a2f6-baaf06305f78.png)](https://academy.hackthebox.com/module/details/143)|Comme nous le savons déjà, la plupart des réseaux d'entreprise sont gérés par des administrateurs utilisant Active Directory. Par conséquent, il est crucial de se familiariser avec cette technologie et la manière dont l'`Énumération et les attaques sur Active Directory` (Active Directory Enumeration & Attacks) peuvent l'affecter. Sa complexité peut souvent conduire à diverses vulnérabilités. Surtout lorsque les administrateurs sont négligents ou imprécis, des vulnérabilités apparaissent souvent qui peuvent conduire à une prise de contrôle complète du domaine.<br><br>Niveau IIMoyenOffensif36 Sections+207 jours|

#### Exploitation Web

L'exploitation web est la deuxième partie de l'étape d'exploitation. De nombreuses technologies, améliorations, fonctionnalités et perfectionnements différents ont été développés dans ce domaine au cours des dernières années, et les choses évoluent constamment. En conséquence, de nombreux composants différents entrent en jeu lorsqu'il s'agit d'applications web. Cela inclut de nombreux types de bases de données qui nécessitent une syntaxe de commande différente pour interagir avec elles. En raison de la diversité des applications web disponibles pour les entreprises et de leur prévalence dans le monde entier, nous devons traiter ce domaine séparément et nous y concentrer intensément. Les applications web présentent une vaste surface d'attaque et sont souvent les principales cibles accessibles lors des missions de tests d'intrusion externes, donc de solides compétences en énumération et en exploitation web sont primordiales.

#### 22. Using Web Proxies

|||
|---|---|
|[![Logo du module pour le module Using Web Proxies.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-8aed-4f16-b465-5b522e9f98ed.png)](https://academy.hackthebox.com/module/details/110)|Les serveurs web et les applications web fonctionnent sur la base du protocole HTTP/HTTPS. Comme d'autres protocoles, ce protocole a une structure fixe pour les requêtes et les réponses. Nous nous concentrerons sur l'`Utilisation des Proxies Web` (Using Web Proxies) pour analyser et manipuler ces requêtes. La manière dont ces requêtes et leurs en-têtes HTTP peuvent être manipulés joue un rôle important dans les résultats que nous pouvons en obtenir. Même l'absence de certains en-têtes HTTP ou un trop grand nombre de méthodes HTTP autorisées peuvent être très dangereux pour le serveur web ou l'application web rapidement et facilement.<br><br>Niveau IIFacileOffensif15 Sections+208 heures|

#### 23. Attacking Web Applications with Ffuf

|||
|---|---|
|[![Logo du module pour le module Attacking Web Applications with Ffuf.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-9c0c-44e5-8d29-1178c068584c.png)](https://academy.hackthebox.com/module/details/54)|Après avoir appris à quelles méthodes d'attaque ces applications web peuvent être soumises, nous pouvons utiliser beaucoup de ces méthodes d'attaque et commencer à `Attaquer les applications Web avec Ffuf`. Étant donné que chaque serveur web et chaque application fonctionne avec de nombreux paramètres différents en raison de son lien avec la base de données, ces paramètres peuvent être découverts manuellement et automatiquement. À cette fin, il existe des procédures et différentes possibilités qui nous permettent de trouver ces paramètres pour exploiter d'autres vulnérabilités possibles.<br><br>Niveau 0FacileOffensif13 Sections+105 heures|

#### 24. Login Brute Forcing

|||
|---|---|
|[![Logo du module pour le module Login Brute Forcing.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-a535-4269-bdfa-95905700f90d.png)](https://academy.hackthebox.com/module/details/57)|Les mécanismes d'authentification sont une cible vitale. En les utilisant, nous pouvons obtenir l'accès à différents comptes d'utilisateurs à l'aide de vulnérabilités spécifiques. L'un des moyens les plus efficaces d'obtenir un accès est par `l'attaque par force brute sur les identifiants` (Login Brute Forcing). Presque toutes les applications web qui offrent des fonctions spécifiques à l'utilisateur fonctionnent à l'aide d'une sorte de mécanisme d'authentification.<br><br>Niveau IIFacileOffensif11 Sections+206 heures|

#### 25. SQL Injection Fundamentals

|||
|---|---|
|[![Logo du module pour le module SQL Injection Fundamentals.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-5147-4fd3-951a-4e751aa69a17.png)](https://academy.hackthebox.com/module/details/33)|Qu'elle gère des produits ou des utilisateurs, la plupart des applications web fonctionnent avec au moins une base de données. Cette base de données est liée à l'application web d'une manière ou d'une autre et peut ouvrir une autre catégorie d'attaque appelée injection SQL (SQL Injection). Avec une compréhension des `SQL Injection Fundamentals`, nous pouvons manipuler ou exploiter la base de données à nos fins en abusant des fonctionnalités contenues dans l'application web.<br><br>Niveau 0MoyenOffensif17 Sections+108 heures|

#### 26. SQLMap Essentials

|||
|---|---|
|[![Logo du module pour le module SQLMap Essentials.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-ab83-4db1-bb4a-ad1a8a3f462b.png)](https://academy.hackthebox.com/module/details/58)|Beaucoup d'attaques contre les bases de données d'applications web sont résumées dans un outil appelé SQLMap et devraient donc également être apprises pour accélérer notre processus après une inspection manuelle. `SQLMap Essentials` doit être appris pour appliquer l'outil de manière appropriée et l'adapter à l'application web.<br><br>Niveau IIFacileOffensif11 Sections+208 heures|

#### 27. Cross-Site Scripting (XSS)

|||
|---|---|
|[![Logo du module pour le module Cross-Site Scripting (XSS).](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-6de7-42c9-9c76-9fca0c085540.png)](https://academy.hackthebox.com/module/details/103)|Le `script inter-sites (Cross-Site Scripting - XSS)` est une autre des catégories d'attaques les plus courantes. Ces vulnérabilités peuvent être exploitées pour lancer diverses attaques, telles que le phishing, le détournement de session, et autres. Entre autres choses, nous pouvons également potentiellement prendre le contrôle des sessions web d'autres utilisateurs ou même d'administrateurs.<br><br>Niveau IIFacileOffensif10 Sections+206 heures|

#### 28. File Inclusion

|||
|---|---|
|[![Logo du module pour le module File Inclusion.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-2948-4715-ab75-14d0a411f4d4.png)](https://academy.hackthebox.com/module/details/23)|Selon la configuration du serveur web et l'application web, certaines vulnérabilités nous permettent un certain type d'`Inclusion de Fichiers` (File Inclusion). Par exemple, nous pourrions être en mesure d'accéder à des fichiers sur le système cible ou d'utiliser les nôtres pour exécuter du code sans que l'accès ne soit fourni par les développeurs ou les administrateurs.<br><br>Niveau 0MoyenOffensif11 Sections+108 heures|

#### 29. Command Injections

|||
|---|---|
|[![Logo du module pour le module Command Injections.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-86a4-4345-a83f-3337284d8805.png)](https://academy.hackthebox.com/module/details/109)|Nous n'avons pas toujours besoin d'attaquer la base de données en utilisant des injections SQL ou XSS. Souvent, des `injections de commandes` (Command Injections) directes peuvent être utilisées pour exécuter des commandes système. Certaines injections de commandes sont plus faciles à repérer que d'autres, qui peuvent nécessiter des connaissances avancées pour identifier et contourner les filtres en place.<br><br>Niveau IIMoyenOffensif12 Sections+206 heures|

#### 30. Web Attacks

|||
|---|---|
|[![Logo du module pour le module Web Attacks.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-cad0-4181-9590-687917d4a7d1.png)](https://academy.hackthebox.com/module/details/134)|Les autres vulnérabilités du top 10 des plus critiques incluent la falsification de verbe HTTP (HTTP Verb Tampering), la référence directe non sécurisée à un objet (IDOR) et l'entité externe XML (XXE). Ce sont des `attaques Web` (Web Attacks) plus avancées, car elles nécessitent le contournement de certains filtres de sécurité et encodages.<br><br>Niveau IIMoyenOffensif18 Sections+202 jours|

#### 31. Attacking Common Applications

|||
|---|---|
|[![Logo du module pour le module Attacking Common Applications.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-9947-447f-b838-69bb9e5bbf35.png)](https://academy.hackthebox.com/module/details/113)|Les applications web courantes peuvent être personnalisées par les administrateurs mais sont néanmoins utilisées dans le monde entier. Par conséquent, il est également essentiel de savoir comment `Attaquer les applications courantes` (Attacking Common Applications).<br><br>Niveau IIMoyenOffensif22 Sections+202 jours|

---

## Post-exploitation

Dans la plupart des cas, lorsque nous exploitons certains services à nos fins pour obtenir l'accès au système, nous n'obtenons généralement pas les privilèges les plus élevés possibles. Parce que les services sont généralement configurés d'une certaine manière « isolée » pour arrêter les attaquants potentiels, contourner ces restrictions est la prochaine étape que nous franchissons à ce stade. Cependant, il n'est pas toujours facile d'effectuer une escalade de privilèges. Après avoir acquis une connaissance approfondie du fonctionnement de ces systèmes d'exploitation, nous devons adapter nos techniques au système d'exploitation particulier et étudier attentivement comment fonctionnent l'`escalade de privilèges sur Linux` (Linux Privilege Escalation) et l'`escalade de privilèges sur Windows` (Windows Privilege Escalation).

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-POEX.png)

À partir de cette étape, il y a quatre chemins que nous pouvons emprunter, en fonction de notre avancement :

|**Parcours**|**Description**|
|---|---|
|`Collecte d'informations / Pillage`|Avant de pouvoir commencer l'escalade de privilèges, nous devons d'abord obtenir une vue d'ensemble du fonctionnement interne du système exploité. Après tout, nous ne savons pas quels utilisateurs se trouvent sur le système et quelles options s'offrent à nous jusqu'à ce point. Cette étape est également connue sous le nom de `Pillage` (Pillaging). Ce chemin n'est pas facultatif, comme les autres, mais essentiel. Encore une fois, entrer dans l'étape de `Collecte d'informations` nous met dans cette perspective. Cela nous amène inévitablement à l'étape de l'évaluation des vulnérabilités, où nous analysons et évaluons les informations que nous trouvons.|
|`Exploitation`|Si nous avons trouvé des informations sensibles sur le système et son contenu, nous pouvons les utiliser pour exploiter des applications ou des services locaux avec des privilèges plus élevés afin d'exécuter des commandes avec ces privilèges.|
|`Mouvement latéral`|À partir d'ici, nous pouvons également passer directement au `Mouvement latéral`. Cela peut se produire dans différentes conditions. Si nous avons atteint les privilèges les plus élevés sur un système à double interface réseau utilisé pour connecter deux réseaux, nous pouvons probablement utiliser cet hôte pour commencer à énumérer des hôtes qui n'étaient pas disponibles auparavant.|
|`Preuve de concept`|Nous pouvons emprunter le dernier chemin après avoir obtenu les privilèges les plus élevés en exploitant un système interne. Bien sûr, nous n'avons pas nécessairement à avoir pris le contrôle de tous les systèmes. Cependant, si nous avons obtenu les privilèges d'Administrateur de Domaine dans un environnement Active Directory, nous pouvons probablement nous déplacer librement sur l'ensemble du réseau et effectuer toutes les actions que nous pouvons imaginer. Nous pouvons donc créer la `Preuve de concept` à partir de nos notes pour détailler et potentiellement automatiser les chemins et les activités et les mettre à la disposition du service technique.|

Après avoir obtenu l'accès à un système, nous devons être en mesure de prendre d'autres mesures depuis l'intérieur du système. Lors d'un test d'intrusion, les clients veulent souvent savoir jusqu'où un attaquant pourrait aller dans leur réseau. Il existe de nombreuses versions différentes de systèmes d'exploitation. Par exemple, nous pouvons rencontrer Windows XP, Windows 7, 8, 10, 11, et Windows Server 2008, 2012, 2016 et 2019. Il existe également différentes distributions pour les systèmes d'exploitation basés sur Linux, telles que Ubuntu, Debian, Parrot OS, Arch, Deepin, Redhat, Pop!_OS, et bien d'autres. Peu importe dans lequel de ces systèmes nous entrons, nous devons nous y retrouver et comprendre les points faibles individuels qu'un système peut avoir de l'intérieur.

#### 32. Linux Privilege Escalation

|||
|---|---|
|[![Logo du module pour le module Linux Privilege Escalation.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-94e8-4086-958c-a752065a7aac.png)](https://academy.hackthebox.com/module/details/51)|La grande majorité des serveurs web qui composent le World Wide Web fonctionnent sous Linux. De plus, nous trouverons de nombreux serveurs basés sur Linux hébergeant des services d'infrastructure critiques que les individus et les organisations utilisent pour être plus productifs et efficaces dans leur travail quotidien. En raison de cette utilisation répandue de Linux, nous devons comprendre les fondamentaux. Il existe de nombreuses façons de mal configurer les systèmes Linux. La découverte de ces failles et leur exploitation pour effectuer une escalade de privilèges sont couvertes dans `Linux Privilege Escalation`.<br><br>Niveau IIFacileOffensif28 Sections+208 heures|

#### 33. Windows Privilege Escalation

|||
|---|---|
|[![Logo du module pour le module Windows Privilege Escalation.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b2-df3c-4972-97f1-8c6902a5aeeb.png)](https://academy.hackthebox.com/module/details/67)|Les systèmes Windows modernes ont maintenant des précautions de sécurité plus fortes (si une organisation est diligente avec les correctifs), mais les erreurs d'administrateur sont possibles dans n'importe quel environnement. Il existe de nombreuses façons de trouver les mauvaises configurations dans les systèmes basés sur Windows, et nous en avons besoin pour l'`escalade de privilèges sur Windows` (Windows Privilege Escalation).<br><br>Niveau IIMoyenOffensif33 Sections+204 jours|

---

## Mouvement latéral

Le mouvement latéral est l'un des composants essentiels pour se déplacer à travers un réseau d'entreprise. Nous pouvons l'utiliser pour atteindre d'autres hôtes internes et escalader davantage nos privilèges dans le sous-réseau actuel ou une autre partie du réseau. Cependant, tout comme le `Pillage`, l'étape du `Mouvement latéral` (Lateral Movement) nécessite l'accès à au moins un des systèmes du réseau de l'entreprise. Dans l'étape d'Exploitation, les privilèges obtenus ne jouent pas un rôle critique dans un premier temps, car nous pouvons également nous déplacer à travers le réseau sans droits d'administrateur.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-LA.png)

Il y a trois chemins que nous pouvons emprunter à partir de cette étape :

|**Parcours**|**Description**|
|---|---|
|`Évaluation des vulnérabilités`|Si le test d'intrusion n'est pas encore terminé, nous pouvons passer d'ici à l'étape d'`Évaluation des vulnérabilités`. Ici, les informations déjà obtenues du pillage sont utilisées et analysées pour évaluer où se trouvent les services réseau ou les applications utilisant un mécanisme d'authentification que nous pourrions être en mesure d'exploiter.|
|`Collecte d'informations / Pillage`|Après un mouvement latéral réussi, nous pouvons nous lancer à nouveau dans le `Pillage`. Il s'agit de la collecte d'informations locales sur le système cible auquel nous avons accédé.|
|`Preuve de concept`|Une fois que nous avons effectué le dernier mouvement latéral possible et terminé notre attaque sur le réseau de l'entreprise, nous pouvons résumer les informations et les étapes que nous avons collectées et peut-être même automatiser certaines sections qui démontrent la vulnérabilité aux failles que nous avons trouvées.|

Puisque le `Mouvement latéral` et le `Pillage` nécessitent tous deux l'accès à un système déjà exploité, ces techniques et méthodes sont couvertes dans différents modules, tels que `Getting Started`, `Linux Privilege Escalation`, et `Windows Privilege Escalation`, et bien d'autres.

---

## Preuve de concept (Proof-of-Concept)

La `Preuve de concept` (`POC` - Proof-Of-Concept) est simplement une preuve qu'une vulnérabilité trouvée existe. Dès que les administrateurs recevront notre rapport, ils essaieront de confirmer les vulnérabilités trouvées en les reproduisant. Après tout, aucun administrateur ne changera des processus critiques pour l'entreprise sans confirmer l'existence d'une vulnérabilité donnée. Un grand réseau peut avoir de nombreux systèmes interopérables et des dépendances qui doivent être vérifiées après avoir effectué un changement, ce qui peut prendre un temps et un argent considérables. Ce n'est pas parce qu'un pentester a trouvé une faille donnée que l'organisation peut facilement y remédier en changeant simplement un système, car cela pourrait avoir un impact négatif sur l'entreprise. Les administrateurs doivent tester soigneusement les correctifs pour s'assurer qu'aucun autre système n'est affecté négativement lorsqu'un changement est introduit. Les PoC sont envoyés avec la documentation dans le cadre d'un test d'intrusion de haute qualité, permettant aux administrateurs de les utiliser pour confirmer les problèmes eux-mêmes.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-POC.png)

À partir de cette étape, il n'y a qu'un seul chemin que nous pouvons emprunter :

|**Parcours**|**Description**|
|---|---|
|`Post-engagement`|À ce stade, nous ne pouvons que passer à l'étape de post-engagement, où nous optimisons et améliorons la documentation et l'envoyons au client après un examen intensif.|

Lorsque nous avons déjà toutes les informations que nous avons collectées et que nous avons utilisé la vulnérabilité à notre avantage, il ne faut pas beaucoup d'efforts pour automatiser les étapes individuelles pour cela.

#### 34. Introduction to Python 3

|||
|---|---|
|[![Logo du module pour le module Introduction to Python 3.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b3-51a5-4e85-8ec4-25582dbcde7d.png)](https://academy.hackthebox.com/module/details/88)|Python est l'un des langages de programmation les plus faciles à apprendre, et il est également assez puissant. Cela facilite l'automatisation de nombreuses étapes et, avec l'aide de commentaires dans notre code, de comprendre exactement comment la vulnérabilité est exploitée étape par étape. Par conséquent, `Introduction to Python 3` sera suffisant pour la plupart des aspects de l'automatisation une fois que nous aurons compris la structure de ce langage de programmation.<br><br>Niveau IFacileGénéral14 Sections+105 heures|

---

## Post-engagement

L'étape de `Post-Engagement` comprend également le nettoyage des systèmes que nous exploitons afin qu'aucun de ces systèmes ne puisse être exploité à l'aide de nos outils. Par exemple, laisser un bind shell sur un serveur web qui ne nécessite pas d'authentification et qui est facile à trouver fera le contraire de ce que nous essayons de faire. De cette manière, nous mettons le réseau en danger par notre négligence. Par conséquent, il est essentiel de supprimer tout le contenu que nous avons transféré sur les systèmes lors de notre test d'intrusion afin que le réseau de l'entreprise soit laissé dans le même état qu'avant notre test d'intrusion. Nous devons également noter tout changement de système, toute tentative d'exploitation réussie, les informations d'identification capturées et les fichiers téléchargés dans les annexes de notre rapport afin que nos clients puissent vérifier cela par rapport à toutes les alertes qu'ils reçoivent pour prouver qu'elles résultent de nos actions de test et non d'un véritable attaquant sur le réseau.

De plus, nous devons concilier toutes nos notes avec la documentation que nous avons rédigée entre-temps pour nous assurer que nous n'avons sauté aucune étape et que nous pouvons fournir un rapport complet, bien formaté et soigné à nos clients.

#### 35. Documentation & Reporting

|||
|---|---|
|[![Logo du module pour le module Documentation & Reporting.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b5-5743-44e9-a282-b7069880a627.png)](https://academy.hackthebox.com/module/details/162)|Nous devons comprendre la `Documentation et la rédaction de rapports` (Documentation and Reporting), comment rester organisé et prendre des notes détaillées, et comment rédiger efficacement et fournir des livrables client de haute qualité. La pratique dans ce domaine simplifiera la préparation de nos rapports et nous fera gagner un temps considérable. Ce module nous aide également à optimiser notre prise de notes et notre organisation, que nous devons adapter à nos besoins pour travailler le plus efficacement possible.<br><br>Niveau IIFacileGénéral8 Sections+202 jours|

#### 36. Attacking Enterprise Networks

|||
|---|---|
|[![Logo du module pour le module Attacking Enterprise Networks.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/logo/9e65e8b5-5ae3-4039-8006-1126596f1930.png)](https://academy.hackthebox.com/module/details/163)|Il est essentiel d'obtenir et de conserver une vue d'ensemble de toutes ces étapes, de leur contenu et des défis possibles. `Attaquer les réseaux d'entreprise` (Attacking Enterprise Networks) peut être une tâche intimidante, et nous pouvons nous perdre dans la diversité de nos options et négliger certains des éléments essentiels. Au lieu de cela, nous devons nous familiariser avec la manière d'attaquer de si grands réseaux et les vulnérabilités qui peuvent exister avec un grand nombre de systèmes dans un réseau.<br><br>Niveau IIMoyenOffensif14 Sections+202 jours|

Maintenant que nous avons couvert la disposition générale des modules de l'Academy concernant le processus de test d'intrusion, nous discuterons brièvement de la manière dont les exercices et les questions sont présentés dans HTB Academy.
---

← [[01 - Introduction au parcours de Testeur d'Intrusion]] | [[00 - Sommaire Penetration Testing Process|Sommaire]] | [[03 - Exercices et questions de l'Academy]] →
