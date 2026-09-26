---
tags:
  - pentest-process
ordre: 6
---

# Processus de test d'intrusion

---

Dans les sciences sociales, un processus est considéré comme un terme désignant une séquence dirigée d'événements. Dans un contexte opérationnel et organisationnel, les processus sont désignés plus précisément comme des processus de travail, d'affaires, de production ou de création de valeur. Les processus sont un autre nom pour les programmes s'exécutant dans les systèmes informatiques, qui sont généralement des parties du logiciel système.

Il est également essentiel de faire la distinction entre les processus `déterministes` et `stochastiques`. Un processus déterministe est un processus dans lequel chaque état est causalement dépendant et déterminé par d'autres états et événements antérieurs. Un processus stochastique est un processus dans lequel un état ne découle d'autres états qu'avec une certaine probabilité. Ici, seules des conditions statistiques peuvent être supposées. Pour nous, plusieurs des définitions ci-dessus se chevauchent. Nous utilisons la définition du processus de test d'intrusion (penetration testing process) issue des sciences sociales pour représenter `un enchaînement d'événements connectés` avec des `processus déterministes`. En effet, toutes nos étapes sont basées sur les événements et les résultats que nous pouvons découvrir ou provoquer.

`Un processus de test d'intrusion est défini par des étapes et des événements successifs réalisés par le testeur d'intrusion pour trouver un chemin vers l'objectif prédéfini.`

Les processus décrivent une séquence spécifique d'opérations dans un laps de temps particulier qui mène au résultat souhaité. Il est également essentiel de noter que les processus ne représentent pas une recette figée et ne sont pas un guide pas à pas. Nos processus de test d'intrusion doivent donc être généraux et flexibles. Après tout, chaque client a une infrastructure, des désirs et des attentes uniques.

---

## Étapes d'un test d'intrusion

La manière la plus efficace de les représenter et de les définir est à travers des `étapes` interdépendantes. Nous constatons souvent dans nos recherches que ces processus sont présentés sous la forme d'un processus circulaire. Si nous regardons cela de plus près et imaginons qu'un seul composant du processus circulaire ne s'applique pas, l'ensemble du processus est perturbé. Strictement défini, tout le processus échoue. Si nous supposons que nous recommençons ce processus depuis le début, mais déjà avec les informations nouvellement acquises, il s'agit déjà d'une nouvelle approche de processus qui n'annule pas la précédente.

Le problème est qu'avec ces représentations et approches, il n'y a souvent rien sur quoi se replier pour étendre notre processus de test d'intrusion. Comme nous l'avons vu, il n'y a pas de guide pas à pas que nous pouvons suivre, mais des `étapes` qui permettent de varier et d'adapter de manière flexible les démarches et approches individuelles aux résultats et informations que nous recevons. Nous pouvons développer notre propre playbook pour diverses choses que nous essayons à différentes étapes d'un test d'intrusion, mais chaque environnement est différent, et nous devons donc nous adapter constamment.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Analyse de vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process.png)

Nous détaillerons chacune de ces étapes et aborderons les spécificités de chacune dans les sections ultérieures et examinerons un `plan d'étude optionnel` sur la manière de procéder pour apprendre les nombreuses Tactiques, Techniques et Procédures (TTP), en utilisant une structure pour montrer comment chaque étape s'appuie sur la précédente et peut également être de nature itérative. Tout d'abord, examinons les grandes composantes du processus de test d'intrusion et discutons des modules individuels et de la raison pour laquelle ils sont si importants.

Ce plan d'étude optionnel est basé sur des ensembles de modules pour chaque étape que nous recommandons de parcourir avant de passer à l'étape suivante. Nous travaillerons à travers différentes phases dans presque tous les modules, effectuant des étapes telles que la `Collecte d'informations`, le `Mouvement latéral` et le `Pillage` à plusieurs reprises. La séparation des modules est conçue pour se concentrer sur le sujet, ce qui nécessite des connaissances spécifiques qui ne doivent pas être ignorées. Des lacunes dans l'une de ces connaissances, même si nous pensons les maîtriser, peuvent entraîner des malentendus ou des difficultés au cours de l'étude. En conséquence, le processus de test d'intrusion avec ses étapes se présente comme suit :

#### Pré-engagement

Le `pré-engagement (pre-engagement)` consiste à éduquer le client et à ajuster le contrat. Tous les tests nécessaires et leurs composants sont strictement définis et enregistrés contractuellement. Lors d'une réunion en personne ou d'une conférence téléphonique, de nombreux arrangements sont pris, tels que :

- `Accord de non-divulgation (Non-Disclosure Agreement)`
- `Objectifs (Goals)`
- `Périmètre (Scope)`
- `Estimation du temps (Time Estimation)`
- `Règles d'engagement (Rules of Engagement)`

#### Collecte d'informations

La `collecte d'informations (information gathering)` décrit comment nous obtenons des informations sur les composants nécessaires de diverses manières. Nous recherchons des informations sur l'entreprise cible ainsi que sur les logiciels et le matériel utilisés pour trouver des failles de sécurité potentielles que nous pourrions exploiter pour obtenir un point d'ancrage.

#### Analyse de vulnérabilités

Une fois que nous arrivons à l'étape d'`analyse de vulnérabilités (Vulnerability Assessment)`, nous analysons les résultats de notre étape de `collecte d'informations`, à la recherche de vulnérabilités connues dans les systèmes, les applications et leurs différentes versions pour découvrir de possibles vecteurs d'attaque. L'analyse de vulnérabilités est l'évaluation des vulnérabilités potentielles, à la fois manuellement et par des moyens automatisés. Elle est utilisée pour déterminer le niveau de menace et la susceptibilité de l'infrastructure réseau d'une entreprise aux cyberattaques.

#### Exploitation

À l'étape d'`exploitation (Exploitation)`, nous utilisons les résultats pour tester nos attaques contre les vecteurs potentiels et les exécuter contre les systèmes cibles pour obtenir un accès initial à ces systèmes.

#### Post-exploitation

À cette étape du test d'intrusion, nous avons déjà accès à la machine exploitée et nous nous assurons de conserver cet accès même si des modifications et des changements sont effectués. Durant cette phase, nous pouvons essayer d'élever nos privilèges pour obtenir les droits les plus élevés possible et rechercher des données sensibles telles que des identifiants ou d'autres données que le client cherche à protéger (pillage). Parfois, nous effectuons la post-exploitation pour démontrer à un client l'impact de notre accès. D'autres fois, nous effectuons la post-exploitation comme une entrée pour le processus de mouvement latéral décrit ci-après.

#### Mouvement latéral

Le `mouvement latéral (lateral movement)` décrit le déplacement au sein du réseau interne de notre entreprise cible pour accéder à des hôtes supplémentaires avec un niveau de privilège identique ou supérieur. C'est souvent un processus itératif combiné avec des activités de post-exploitation jusqu'à ce que nous atteignions notre objectif. Par exemple, nous obtenons un point d'ancrage sur un serveur web, élevons nos privilèges et trouvons un mot de passe dans le registre. Nous effectuons une énumération plus poussée et voyons que ce mot de passe fonctionne pour accéder à un serveur de base de données en tant qu'utilisateur administrateur local. À partir de là, nous pouvons piller des données sensibles de la base de données et trouver d'autres identifiants pour approfondir notre accès dans le réseau. À cette étape, nous utiliserons généralement de nombreuses techniques basées sur les informations trouvées sur l'hôte ou le serveur exploité.

#### Preuve de concept

À cette étape, nous documentons, pas à pas, les démarches que nous avons suivies pour parvenir à la compromission du réseau ou à un certain niveau d'accès. Notre objectif est de brosser un tableau de la manière dont nous avons pu enchaîner plusieurs faiblesses pour atteindre notre but, afin qu'ils puissent avoir une image claire de la place de chaque vulnérabilité et de la manière de prioriser leurs efforts de remédiation. Si nous ne documentons pas bien nos étapes, il est difficile pour le client de comprendre ce que nous avons pu faire, ce qui rend leurs efforts de remédiation plus difficiles. Si possible, nous pourrions créer un ou plusieurs scripts pour automatiser les étapes que nous avons suivies afin d'aider notre client à reproduire nos découvertes. Nous couvrons cela en profondeur dans le module `Documentation et rapports (Documentation & Reporting)`.

#### Post-engagement

Pendant le `post-engagement`, une documentation détaillée est préparée à la fois pour les administrateurs et la direction de l'entreprise cliente afin de comprendre la gravité des vulnérabilités découvertes. À ce stade, nous nettoyons également toutes les traces de nos actions sur tous les hôtes et serveurs. Durant cette étape, nous créons les livrables pour notre client, tenons une réunion de présentation du rapport, et parfois nous faisons une présentation exécutive aux dirigeants de l'entreprise cible ou à leur conseil d'administration. Enfin, nous archiverons nos données de test conformément à nos obligations contractuelles et à la politique de l'entreprise. Nous conserverons généralement ces données pendant une période définie ou jusqu'à ce que nous effectuions une évaluation post-remédiation (re-test) pour tester les correctifs du client.

---

## Importance

Nous devons intérioriser cette procédure et l'utiliser comme base pour tous nos engagements techniques. Les composants de chaque étape nous permettent de comprendre précisément les domaines que nous devons améliorer et où se situent la plupart de nos difficultés et de nos lacunes en matière de connaissances. Par exemple, nous pouvons penser à un site web comme une cible que nous devons étudier.

|**Étape**|**Description**|
|---|---|
|`1. Pré-engagement`|La première étape consiste à créer tous les documents nécessaires dans la phase de pré-engagement, à discuter des objectifs de l'évaluation et à clarifier toutes les questions.|
|`2. Collecte d'informations`|Une fois les activités de pré-engagement terminées, nous enquêtons sur le site web existant de l'entreprise que nous avons été chargés d'évaluer. Nous identifions les technologies utilisées et apprenons comment fonctionne l'application web.|
|`3. Analyse de vulnérabilités`|Avec ces informations, nous pouvons rechercher des vulnérabilités connues et examiner les fonctionnalités douteuses qui pourraient permettre des actions non intentionnelles.|
|`4. Exploitation`|Une fois que nous avons trouvé des vulnérabilités potentielles, nous préparons notre code d'exploitation, nos outils et notre environnement, et nous testons le serveur web pour ces vulnérabilités potentielles.|
|`5. Post-exploitation`|Une fois que nous avons exploité avec succès la cible, nous passons à la collecte d'informations et examinons le serveur web de l'intérieur. Si nous trouvons des informations sensibles à ce stade, nous essayons d'élever nos privilèges (selon le système et les configurations).|
|`6. Mouvement latéral`|Si d'autres serveurs et hôtes du réseau interne sont dans le périmètre, nous essayons alors de nous déplacer à travers le réseau et d'accéder à d'autres hôtes et serveurs en utilisant les informations que nous avons recueillies.|
|`7. Preuve de concept`|Nous créons une `preuve de concept (proof-of-concept)` qui prouve que ces vulnérabilités existent et nous automatisons potentiellement même les étapes individuelles qui déclenchent ces vulnérabilités.|
|`8. Post-engagement`|Enfin, la documentation est finalisée et présentée à notre client sous forme de rapport formel. Ensuite, nous pouvons organiser une réunion de présentation du rapport pour clarifier tout ce qui concerne nos tests ou nos résultats et fournir tout le soutien nécessaire au personnel chargé de remédier à nos découvertes.|
---

← [[05 - Lois et réglementations]] | [[00 - Sommaire Penetration Testing Process|Sommaire]] | [[07 - Pré-engagement]] →
