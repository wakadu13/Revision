---
tags:
  - pentest-process
ordre: 9
---

# Évaluation des vulnérabilités

---

Pendant la phase de `vulnerability assessment`, nous examinons et analysons les informations collectées durant la phase de collecte d'informations. La phase d'évaluation des vulnérabilités (vulnerability assessment) est un processus analytique basé sur les résultats.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-VA.png)

`Une analyse est un examen détaillé d'un événement ou d'un processus, décrivant son origine et son impact, qui, à l'aide de certaines précautions et actions, peut être déclenché pour soutenir ou empêcher des occurrences futures.`

Toute analyse peut être très compliquée, car de nombreux facteurs différents et leurs interdépendances jouent un rôle important. Outre le fait que nous travaillons avec les trois temporalités (passé, présent et futur) lors de chaque analyse, l'origine et la destination jouent un rôle important. Il existe quatre types d'analyse différents :

|**Type d'analyse**|**Description**|
|---|---|
|`Descriptive`|L'analyse descriptive est essentielle dans toute analyse de données. D'une part, elle décrit un ensemble de données sur la base de caractéristiques individuelles. Elle aide à détecter d'éventuelles erreurs dans la collecte des données ou des valeurs aberrantes dans l'ensemble de données.|
|`Diagnostique`|L'analyse diagnostique clarifie les causes, les effets et les interactions des conditions. Cela fournit des informations obtenues par des corrélations et des interprétations. Nous devons adopter une vision rétrospective, similaire à l'analyse descriptive, avec la subtile différence que nous essayons de trouver les raisons des événements et des évolutions.|
|`Prédictive`|En évaluant les données historiques et actuelles, l'analyse prédictive crée un modèle prédictif pour les probabilités futures. Basée sur les résultats des analyses descriptive et diagnostique, cette méthode d'analyse de données permet d'identifier les tendances, de détecter les écarts par rapport aux valeurs attendues à un stade précoce et de prédire les occurrences futures avec la plus grande précision possible.|
|`Prescriptive`|L'analyse prescriptive vise à définir les actions à entreprendre pour éliminer ou prévenir un problème futur ou pour déclencher une activité ou un processus spécifique.|

Nous utilisons nos résultats et les informations obtenues jusqu'à présent et les analysons pour en tirer des conclusions. La formation de conclusions peut être étendue très loin, mais nous devons ensuite les confirmer ou les infirmer. Supposons que nous ayons trouvé un port TCP 2121 ouvert sur un hôte pendant la phase de collecte d'informations.

À part le fait que ce port est ouvert, Nmap ne nous a rien montré d'autre. Nous devons maintenant nous demander quelles conclusions peuvent être tirées de ce résultat. Par conséquent, peu importe la question par laquelle nous commençons pour tirer nos conclusions. Cependant, il est essentiel de poser des `questions précises` et de se souvenir de ce que nous `savons` et de ce que nous `ne savons pas`. À ce stade, nous devons d'abord nous demander ce que nous `voyons` et ce que nous `avons` réellement, car ce que nous voyons n'est pas la même chose que ce que nous avons :

- un port `TCP` `2121`. - `TCP` signifie déjà que ce service est `orienté connexion`.
- Est-ce un port `standard` ? - `Non`, car ceux-ci se situent entre `0-1023`, également appelés ports bien connus ou [ports système](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
- Y a-t-il des chiffres dans ce `numéro de port` qui semblent `familiers` ? - `Oui`, le port `TCP` `21` (`FTP`). Avec l'expérience, nous apprendrons à connaître de nombreux ports standard et leurs services, que les administrateurs tentent souvent de déguiser, mais en utilisant souvent des alternatives « faciles à retenir ».

Sur la base de notre supposition, nous pouvons essayer de nous connecter au service en utilisant `Netcat` ou un client `FTP` et tenter d'établir une connexion pour confirmer ou infirmer notre hypothèse.

En nous connectant au service, nous avons remarqué que la connexion a pris plus de temps que d'habitude (environ 15 secondes). Il existe certains services dont la vitesse de connexion, ou le temps de réponse, peut être configurée. Maintenant que nous savons qu'un serveur FTP fonctionne sur ce port, nous pouvons déduire l'origine de notre analyse « échouée ». Nous pourrions le confirmer à nouveau en spécifiant le `temps d'aller-retour minimum de la sonde` (`--min-rtt-timeout`) dans Nmap à 15 ou 20 secondes et en relançant l'analyse.

---

## Recherche et analyse de vulnérabilités

La `Information Gathering` et la `Vulnerability Research` peuvent être considérées comme faisant partie de l'analyse descriptive. C'est là que nous identifions les composants individuels du réseau ou du système que nous étudions. Dans la `Vulnerability Research`, nous recherchons les vulnérabilités, exploits et failles de sécurité connus qui ont déjà été découverts et signalés. Par conséquent, si nous avons identifié une version d'un service ou d'une application grâce à la collecte d'informations et que nous avons trouvé une [Vulnérabilité et Exposition Commune (Common Vulnerabilities and Exposures - CVE)](https://www.cve.org/ResourcesSupport/FAQs), il est très probable que cette vulnérabilité soit toujours présente.

Nous pouvons trouver des divulgations de vulnérabilités pour chaque composant en utilisant de nombreuses sources différentes. Celles-ci incluent, sans s'y limiter :

||||
|---|---|---|
|[CVEdetails](https://www.cvedetails.com/)|[Exploit DB](https://www.exploit-db.com/)|[Vulners](https://vulners.com/)|
|[Packet Storm Security](https://packetstormsecurity.com/)|[NIST](https://nvd.nist.gov/vuln/search?execution=e2s1)||

C'est là que l'`Analyse diagnostique` et l'`Analyse prédictive` sont utilisées. Une fois que nous avons trouvé une vulnérabilité publiée comme celle-ci, nous pouvons la diagnostiquer pour déterminer ce qui cause ou a causé la vulnérabilité. Ici, nous devons comprendre au mieux la fonctionnalité du code de la `Preuve de concept` (`POC`) ou de l'application ou du service lui-même, car de nombreuses configurations manuelles par les administrateurs nécessiteront une certaine personnalisation du POC. Chaque POC est adapté à un cas spécifique que nous devrons également, dans la plupart des cas, adapter au nôtre.

---

## Évaluation des vecteurs d'attaque possibles

La `Vulnerability Assessment` inclut également les tests réels, qui font partie de l'`Analyse prédictive`. Ce faisant, nous analysons les informations historiques et les combinons avec les informations actuelles que nous avons pu découvrir. Que nous ayons reçu ou non des exigences spécifiques de niveau d'évasion de la part de notre client, nous testons les services et applications trouvés `localement` ou `sur le système cible`. Si nous devons tester de manière discrète et éviter les alertes, nous devrions refléter le système cible localement aussi précisément que possible. Cela signifie que nous utilisons les informations obtenues lors de notre phase de collecte d'informations pour répliquer le système cible, puis nous recherchons des vulnérabilités dans le système déployé localement.

---

## Le retour

Si nous ne parvenons pas à détecter ou à identifier des vulnérabilités potentielles à partir de notre analyse, nous reviendrons à l'étape de `Information Gathering` et chercherons des informations plus approfondies que celles que nous avons recueillies jusqu'à présent. Il est important de noter que ces deux étapes (`Information Gathering` et `Vulnerability Assessment`) se chevauchent souvent, ce qui entraîne des allers-retours réguliers entre elles. Nous le verrons dans de nombreuses vidéos où l'auteur résout une box HTB ou un défi CTF. Nous devons nous rappeler que ces défis sont souvent résolus le plus rapidement possible, et que la vitesse est donc plus importante que la qualité. Dans un CTF, l'objectif est d'accéder à la machine cible et de `capturer les drapeaux` avec les privilèges les plus élevés le plus rapidement possible, au lieu d'exposer toutes les faiblesses potentielles du système.

|**`Un (vrai) test d'intrusion n'est pas un CTF.`**|
|---|

Ici, la `qualité` et l'`intensité` de notre test d'intrusion et de son analyse ont la plus haute priorité, car rien n'est pire que de voir notre client se faire pirater avec succès via un vecteur relativement simple que nous aurions dû découvrir lors de notre test d'intrusion.
---

← [[08 - Collecte d'informations]] | [[00 - Sommaire Penetration Testing Process|Sommaire]] | [[10 - Exploitation]] →
