---
tags:
  - getting-started
ordre: 1
---

# Aperçu de l'Infosec

---

La [sécurité de l'information](https://en.wikipedia.org/wiki/Information_security) (infosec) est un domaine très vaste. Ce domaine s'est considérablement développé et a beaucoup évolué au cours des dernières années. Il offre de nombreuses spécialisations, y compris, mais sans s'y limiter :

- Sécurité des réseaux et des infrastructures
- Sécurité des applications
- Tests de sécurité
- Audit des systèmes
- Planification de la continuité des activités
- Informatique légale (digital forensics)
- Détection et réponse aux incidents

En résumé, l'infosec est la pratique qui consiste à protéger les données contre l'accès non autorisé, les modifications, l'utilisation illicite, la perturbation, etc. Les professionnels de l'infosec prennent également des mesures pour réduire l'impact global de tels incidents.

Les données peuvent être électroniques ou physiques, tangibles (par ex., des plans de conception) ou intangibles (des connaissances). Une phrase courante qui reviendra souvent dans notre carrière en infosec est la protection de la « confidentialité, intégrité et disponibilité des données », ou la `CIA triad`.

---

## Processus de gestion des risques

La protection des données doit se concentrer sur la mise en œuvre de politiques efficaces et efficientes sans affecter négativement les opérations commerciales et la productivité d'une organisation. Pour ce faire, les organisations doivent suivre un processus appelé le `risk management process`. Ce processus comprend les cinq étapes suivantes :

|Étape|Explication|
|---|---|
|`Identifying the Risk`|Identifier les risques auxquels l'entreprise est exposée, tels que les risques juridiques, environnementaux, de marché, réglementaires et autres.|
|`Analyze the Risk`|Analyser les risques pour déterminer leur impact et leur probabilité. Les risques doivent être mis en correspondance avec les diverses politiques, procédures et processus métier de l'organisation.|
|`Evaluate the Risk`|Évaluer, classer et hiérarchiser les risques. Ensuite, l'organisation doit décider d'accepter (inévitable), d'éviter (changer les plans), de contrôler (atténuer) ou de transférer le risque (assurer).|
|`Dealing with Risk`|Éliminer ou contenir les risques du mieux possible. Cela se fait en interagissant directement avec les parties prenantes du système ou du processus auquel le risque est associé.|
|`Monitoring Risk`|Tous les risques doivent être surveillés en permanence. Les risques doivent être constamment surveillés pour déceler tout changement de situation qui pourrait modifier leur score d'impact, `i.e., from low to medium or high impact`.|

Comme mentionné précédemment, le principe fondamental de l'infosec est l'assurance de l'information, c'est-à-dire le maintien de la `CIA` des données et la garantie qu'elles ne sont compromises d'aucune manière, forme ou façon lorsqu'un incident se produit. Un incident peut être une catastrophe naturelle, un dysfonctionnement du système ou un incident de sécurité.

---

## Red Team vs. Blue Team

En infosec, on entend souvent les termes `red team` et `blue team`. Pour simplifier, la `red team` joue le rôle des attaquants, tandis que la `blue team` joue le rôle des défenseurs.

Les membres de la red team (red teamers) jouent généralement un rôle d'adversaire en s'introduisant dans l'organisation pour identifier les faiblesses potentielles que de vrais attaquants pourraient utiliser pour percer les défenses de l'organisation. La tâche la plus courante du côté du red teaming est le test d'intrusion (penetration testing), l'ingénierie sociale (social engineering) et d'autres techniques offensives similaires.

D'un autre côté, la blue team constitue la majorité des emplois en infosec. Elle est responsable du renforcement des défenses de l'organisation en analysant les risques, en élaborant des politiques, en répondant aux menaces et aux incidents, et en utilisant efficacement les outils de sécurité et d'autres tâches similaires.

---

## Rôle des testeurs d'intrusion

Un évaluateur de sécurité (testeur d'intrusion réseau, testeur d'intrusion d'applications web, red teamer, etc.) aide une organisation à identifier les risques sur ses réseaux externes et internes. Ces risques peuvent inclure des vulnérabilités de réseau ou d'application web, l'exposition de données sensibles, des erreurs de configuration ou des problèmes pouvant porter atteinte à la réputation. Un bon testeur peut travailler avec un client pour identifier les risques pour son organisation, fournir des informations sur la manière de reproduire ces risques, et des conseils sur l'atténuation ou la remédiation des problèmes identifiés pendant les tests.

Les évaluations peuvent prendre de nombreuses formes, d'un test d'intrusion en boîte blanche (white-box penetration test) sur tous les systèmes et applications concernés pour identifier autant de vulnérabilités que possible, à une évaluation de hameçonnage (phishing) pour évaluer le risque ou la sensibilisation à la sécurité des employés, jusqu'à une évaluation red team ciblée construite autour d'un scénario pour émuler un acteur malveillant (threat actor) du monde réel.

Nous devons comprendre la situation globale des risques auxquels une organisation est confrontée et son environnement pour évaluer et noter avec précision les vulnérabilités découvertes lors des tests. Une compréhension approfondie du processus de gestion des risques est essentielle pour quiconque débute dans la sécurité de l'information.

Ce module se concentrera sur la manière de débuter en infosec et en test d'intrusion d'un point de vue pratique, en particulier sur la sélection et la navigation dans une distribution pour pentest (pentest distro), l'apprentissage des technologies courantes et des outils essentiels, l'apprentissage des niveaux et des bases du test d'intrusion, le "crackage" de notre première machine sur HTB, comment trouver et demander de l'aide le plus efficacement possible, les problèmes potentiels courants, et comment naviguer sur la plateforme Hack the Box.

Bien que ce module utilise la plateforme Hack The Box et des machines volontairement vulnérables comme exemples, les compétences fondamentales présentées s'appliquent à n'importe quel environnement.
---

[[00 - Sommaire Getting Started|Sommaire]] | [[02 - Démarrer avec une Distribution de Pentest]] →
