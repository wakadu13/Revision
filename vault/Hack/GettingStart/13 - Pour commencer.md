---
tags:
  - getting-started
ordre: 13
---

# Pour commencer

---

En tant que débutant en sécurité de l'information, il peut être extrêmement intimidant de savoir par où commencer. Nous avons vu des personnes de tous horizons, avec peu ou pas de connaissances, réussir sur la plateforme HTB et, par la suite, entamer une carrière technique. Il existe de nombreuses ressources de qualité pour les débutants, notamment des formations gratuites et payantes, des machines et des laboratoires délibérément vulnérables, des sites de tutoriels, des blogs, des chaînes YouTube, etc.

Tout au long de notre parcours, nous rencontrerons continuellement les termes apprentissage `guidé` et apprentissage `par l'exploration`.

HTB Academy suit une approche d'apprentissage `guidé` où les étudiants parcourent un module sur un sujet donné, lisent le contenu et reproduisent les exemples pour renforcer les thèmes présentés. La plupart des sections de module comportent un ou plusieurs exercices pratiques pour tester les connaissances des étudiants sur un sujet donné. De nombreux modules se terminent par une évaluation des compétences en plusieurs étapes pour tester la compréhension par les étudiants du contenu présenté dans les sections du module lorsqu'il est appliqué à un scénario du monde réel.

L'apprentissage guidé a l'avantage de fournir aux étudiants des méthodes structurées pour apprendre diverses techniques d'une manière qui construit correctement leurs connaissances, tout en fournissant du matériel supplémentaire, des connaissances de base et des liens avec le monde réel pour apprendre un sujet en profondeur, tout en les forçant à tester leurs connaissances à différents points de contrôle tout au long du processus d'apprentissage.

La plateforme HTB principale suit une approche d'apprentissage `par l'exploration` pour placer les utilisateurs dans une grande variété de scénarios du monde réel dans lesquels ils doivent utiliser leurs compétences techniques et leurs processus, tels que l'énumération, pour atteindre un objectif souvent inconnu. La plateforme propose des challenges uniques dans des catégories telles que l'ingénierie inverse (reverse engineering), la cryptographie, la stéganographie, le pwn, le web, la forensique (informatique légale), l'OSINT, le mobile, le matériel (hardware), et plus encore, à différents niveaux de difficulté, conçus pour tester les compétences techniques et la pensée critique.

Il y a aussi des machines uniques (boxes) de différents types de systèmes d'exploitation, de petits (et difficiles) mini-laboratoires appelés Endgames, des Fortresses qui sont des machines uniques contenant de nombreux challenges, et des Pro Labs, qui sont de grands réseaux d'entreprise simulés où les utilisateurs peuvent effectuer un test d'intrusion (penetration test) fictif à différents niveaux de difficulté.

Il y a toujours des machines et des challenges « actifs » gratuits que les utilisateurs doivent attaquer avec une approche en boîte noire (black box) ou avec peu ou pas de connaissance préalable de la tâche à accomplir. Les machines, les challenges et les Endgames sont « retirés » et mis à la disposition des utilisateurs VIP avec des solutions détaillées (walkthroughs) officielles pour aider dans le processus d'apprentissage. Lorsque le contenu est retiré de la plateforme, la communauté est invitée à créer des blogs et des vidéos de solutions. Il est utile de lire plusieurs blogs/regarder plusieurs vidéos sur la même machine retirée pour voir les différentes perspectives et les différents styles que les utilisateurs adoptent lorsqu'ils abordent une tâche, afin de commencer à construire l'approche avec laquelle vous êtes le plus à l'aise.

Le principal avantage de l'approche d'apprentissage `par l'exploration` est de nous permettre de nous fier à nos compétences pour pénétrer dans les machines et résoudre les challenges, ce qui nous aide à construire nos méthodologies et techniques et à façonner notre style de test d'intrusion.

**Il est toujours bon de combiner les deux styles d'apprentissage afin de développer nos compétences avec une structure de connaissances appropriée et de nous mettre au défi d'approfondir notre compréhension des compétences que nous avons acquises.**

---

## Ressources

Pour commencer, la quantité de contenu disponible sur le web peut être écrasante. De plus, il n'est pas facile de savoir par où commencer et de juger de la qualité des supports disponibles. Ce qui suit sont quelques ressources en dehors de HTB que nous recommandons à quiconque commence son parcours ou cherche à améliorer ses compétences et à apprendre de nouvelles astuces.

#### Machines/Applications Vulnérables

Il existe de nombreuses ressources pour s'exercer aux vulnérabilités web et réseau courantes dans un environnement sûr et contrôlé. Voici quelques exemples d'applications web délibérément vulnérables et de machines vulnérables que nous pouvons mettre en place dans un environnement de laboratoire pour une pratique supplémentaire.

|||
|---|---|
|[OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)|Est une application web moderne et vulnérable écrite en Node.js, Express et Angular qui présente l'ensemble du [Top 10 OWASP](https://owasp.org/www-project-top-ten) ainsi que de nombreuses autres failles de sécurité d'applications du monde réel.|
|[Metasploitable 2](https://docs.rapid7.com/metasploit/metasploitable-2-exploitability-guide/)|Est une VM Linux Ubuntu délibérément vulnérable qui peut être utilisée pour pratiquer l'énumération, l'exploitation automatisée et manuelle.|
|[Metasploitable 3](https://github.com/rapid7/metasploitable3)|Est un modèle pour construire une VM Windows vulnérable configurée avec un large éventail de [vulnérabilités](https://github.com/rapid7/metasploitable3/wiki/Vulnerabilities).|
|[DVWA](https://github.com/digininja/DVWA)|Il s'agit d'une application web PHP/MySQL vulnérable présentant de nombreuses vulnérabilités courantes des applications web avec différents degrés de difficulté.|

Il est utile d'apprendre à les configurer dans votre environnement de laboratoire pour acquérir une pratique supplémentaire dans la mise en place de VM et le travail avec des configurations courantes telles que la mise en place d'un serveur web. En plus de ces machines/applications vulnérables, nous pouvons également mettre en place de nombreuses machines et applications dans un environnement de laboratoire pour pratiquer la configuration, l'énumération/exploitation et la remédiation.

---

#### Chaînes YouTube

Il existe de nombreuses chaînes YouTube qui présentent des techniques de test d'intrusion/hacking. En voici quelques-unes qui méritent d'être ajoutées à vos favoris :

|||
|---|---|
|[IppSec](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA)|Fournit une solution détaillée extrêmement approfondie de chaque machine HTB retirée, pleine de perspectives tirées de sa propre expérience, ainsi que des vidéos sur diverses techniques.|
|[VbScrub](https://www.youtube.com/channel/UCpoyhjwNIWZmsiKNKpsMAQQ)|Propose des vidéos sur HTB ainsi que des vidéos sur des techniques, se concentrant principalement sur l'exploitation d'Active Directory.|
|[STÖK](https://www.youtube.com/channel/UCQN2DsjnYH60SFBIA6IkNwg)|Propose des vidéos sur divers sujets liés à la sécurité de l'information, se concentrant principalement sur les bug bounties et les tests d'intrusion d'applications web.|
|[LiveOverflow](https://www.youtube.com/channel/UClcE-kVhqyiHCcjYwcpfj9w)|Propose des vidéos sur une grande variété de sujets techniques liés à la sécurité de l'information.|

---

#### Blogs

Il y a trop de blogs pour pouvoir tous les lister. Si vous faites une recherche Google pour une solution détaillée de n'importe quelle machine HTB retirée, vous tomberez généralement sur les mêmes blogs à maintes reprises. Ceux-ci peuvent être excellents pour voir le point de vue d'une autre personne sur le même sujet, surtout si leurs articles contiennent des informations « supplémentaires » sur la cible que d'autres blogs ne couvrent pas. Un excellent blog à consulter est [0xdf hacks stuff](https://0xdf.gitlab.io/). Ce blog propose des solutions détaillées fantastiques pour la plupart des machines HTB retirées, chacune avec une section « Beyond Root » couvrant un aspect unique de la machine que l'auteur a remarqué. Le blog propose également des articles sur diverses techniques, l'analyse de malwares et des comptes-rendus (write-ups) d'événements CTF passés.

À n'importe quelle étape du processus d'apprentissage, il est utile de lire autant de matériel que possible pour mieux comprendre un sujet et obtenir différentes perspectives. Outre les blogs liés aux machines HTB retirées, il est également utile de rechercher des comptes-rendus de blogs sur des exploits/attaques récents, des techniques d'exploitation d'Active Directory, des comptes-rendus d'événements CTF et des rapports de bug bounty. Tous ces éléments peuvent contenir une mine d'informations qui peuvent aider à relier certains points de notre apprentissage ou même nous apprendre quelque chose de nouveau qui peut s'avérer utile lors d'une évaluation.

---

#### Sites de tutoriels

Il existe de nombreux sites de tutoriels pour pratiquer les compétences informatiques fondamentales, comme le scripting. Deux excellents sites de tutoriels sont [Under The Wire](https://underthewire.tech/wargames) et [Over The Wire](https://overthewire.org/wargames/). Ces sites web sont conçus pour aider les utilisateurs à s'entraîner à utiliser `PowerShell` sous Windows et la ligne de commande Linux, respectivement, à travers divers scénarios sous un format de « wargames ». Ils guident l'utilisateur à travers différents niveaux, composés de tâches ou de défis pour les former à l'utilisation fondamentale et avancée de la ligne de commande Windows et Linux, ainsi qu'au scripting en `Bash` et `PowerShell`. Ces compétences sont primordiales pour quiconque cherche à réussir dans cette industrie.

---

#### Point de départ HTB

[Starting Point](https://app.hackthebox.com/starting-point) est une introduction aux laboratoires HTB et aux machines/challenges de base. Après avoir suivi un tutoriel couvrant la connexion au VPN, l'énumération, l'obtention d'un premier accès (foothold) et l'escalade de privilèges sur une seule cible, plusieurs machines de niveau facile nous sont présentées, qui peuvent être attaquées avant d'accéder au reste de la plateforme HTB.

---

#### Parcours HTB

Sur la plateforme HTB principale, les [Parcours (Tracks)](https://app.hackthebox.com/tracks) sont des « sélections de machines et de challenges liés entre eux pour que les utilisateurs puissent progresser, en maîtrisant un sujet particulier ». Les parcours couvrent une variété de sujets et sont continuellement ajoutés à la plateforme. Leur but est d'aider les étudiants à rester concentrés sur un objectif spécifique de manière structurée tout en suivant une approche d'apprentissage par l'exploration.

---

#### Machines HTB pour débutants

Il existe de nombreuses machines pour débutants sur la plateforme HTB principale. En voici quelques-unes recommandées :

|[Lame](https://app.hackthebox.com/machines/1)|[Blue](https://app.hackthebox.com/machines/51)|[Nibbles](https://app.hackthebox.com/machines/121)|[Shocker](https://app.hackthebox.com/machines/108)|[Jerry](https://app.hackthebox.com/machines/144)|
|---|---|---|---|---|

Si vous préférez regarder une solution vidéo tout en travaillant sur une machine facile, les playlists ci-dessous de la chaîne d'IppSec contiennent des solutions pour diverses machines HTB faciles sous Linux/Windows :

|**<br><br>Machines Linux Faciles<br><br>**|**<br><br>Machines Windows Faciles<br><br>**|
|---|---|

---

#### Challenges HTB pour débutants

La plateforme HTB contient des challenges uniques dans diverses catégories. Voici quelques challenges pour débutants :

|[Find The Easy Pass](https://app.hackthebox.com/challenges/5)|[Weak RSA](https://app.hackthebox.com/challenges/6)|[You know 0xDiablos](https://app.hackthebox.com/challenges/106)|
|---|---|---|

---

#### Prolab Dante

La plateforme HTB propose divers Pro Labs qui sont des réseaux d'entreprise simulés avec de nombreux hôtes interconnectés que les joueurs peuvent utiliser pour pratiquer leurs compétences dans un réseau contenant plusieurs cibles. L'exploitation réussie d'hôtes spécifiques donnera des informations qui aideront les joueurs lorsqu'ils attaqueront des hôtes rencontrés plus tard dans le laboratoire.

Le [Pro Lab Dante](https://app.hackthebox.com/prolabs/overview/dante) est le laboratoire le plus adapté aux débutants proposé à ce jour. Ce laboratoire s'adresse aux joueurs ayant une certaine expérience des attaques de réseaux et d'applications web, ainsi qu'une compréhension des concepts de réseau et des bases des méthodologies de test d'intrusion telles que l'analyse/énumération, le mouvement latéral (lateral movement), l'escalade de privilèges, la post-exploitation, etc.

---

## Pour la suite

Maintenant que nous avons abordé la terminologie et les techniques de base ainsi que l'analyse/énumération, assemblons les pièces du puzzle en parcourant pas à pas une machine HTB de niveau facile.
---

← [[12 - Transférer des Fichiers]] | [[00 - Sommaire Getting Started|Sommaire]] | [[14 - Naviguer sur HTB]] →
