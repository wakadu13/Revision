---
tags:
  - infosec
ordre: 1
---

# Structure de l'InfoSec

---

Dans ce module, notre objectif est de vous fournir une compréhension fondamentale de la sécurité des informations : comment elle est structurée, quels rôles sont assumés par qui, les différents domaines/domaines d'expertise en cybersécurité, et quelles opportunités de carrière sont actuellement disponibles. Ce module est fondamentalement conçu pour les débutants complets, ceux qui ont trouvé la motivation et pris la décision de plonger dans le vaste océan de la cybersécurité.

Pour rendre cette plongée moins intimidante, nous vous donnerons l'aperçu nécessaire de la manière dont la sécurité des informations est largement structurée et organisée. L'objectif ici est de vous doter de suffisamment de connaissances pour vous aider à décider où vous voulez nager, et à développer une idée de la direction que vous devez prendre.

**Note de l'auteur :**  
Puisque nous partons du principe que vous êtes "nouveau" dans ce domaine, nous ne pourrons malheureusement pas vous proposer d'exercices pratiques tout de suite. Imaginez que vous êtes assis dans un avion de chasse, impatient de décoller. Sans savoir ce qu'est chaque élément dans le cockpit ou à quoi il sert, il vous sera extrêmement difficile (et long) de simplement démarrer l'avion, et encore plus de le faire décoller. Par conséquent, ce module est purement "théorique", tout en étant concis et rempli de tous les détails essentiels. Vous rencontrerez et découvrirez tous les autres aspects au cours de votre parcours dans les modules futurs. Notre but est de vous aider à devenir un excellent spécialiste professionnel dans le domaine que vous désirez. Pour cela, nous devons d'abord vous donner une image globale du monde de la sécurité de l'information.

De nos jours, nous dépendons fortement des plateformes numériques pour presque tout : communiquer avec des amis, effectuer des opérations bancaires, faire des achats et gérer des entreprises. Cela signifie qu'il est crucial de protéger nos données contre tout accès ou dommage non autorisé. La sécurité des informations, souvent appelée `InfoSec`, consiste à protéger les informations et les systèmes contre les personnes qui ne doivent pas y avoir accès. Cela inclut la prévention de la consultation, de la modification ou de la destruction non autorisées des données.

Regardez attentivement le graphique suivant et essayez de le mémoriser. Il illustre, de manière très simplifiée, la structure/le paysage approximatif du monde numérique. Nous examinerons cela pièce par pièce dans les sections à venir, et vous comprendrez comment tous ces éléments sont interconnectés.

![Schéma de réseau montrant les applications, les serveurs, le cloud, internet et les connexions des clients. Inclut les employés, les appareils mobiles, l'entreprise et les équipes : Bleue, Rouge et Violette.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

- `Client` : C'est un PC/ordinateur portable à travers lequel vous accédez à des ressources et des services « sur Internet ».
- `Internet` : C'est un vaste réseau interconnecté de serveurs qui offrent différents services et applications, comme Hack The Box.
- `Serveurs` : Les serveurs fournissent divers services et applications conçus pour effectuer des tâches spécifiques. Par exemple, un type de serveur pourrait être un « serveur web », vous permettant, ainsi qu'à d'autres, de visualiser le contenu d'un site web (comme cette section que vous lisez actuellement) sur votre ordinateur ou votre smartphone.
- `Réseau` : Lorsque plusieurs serveurs ou ordinateurs sont connectés et peuvent communiquer entre eux, on parle de réseau.
- `Cloud` : Le cloud fait référence à des centres de données qui offrent des serveurs interconnectés que les entreprises et les particuliers peuvent utiliser.
- `Équipe bleue (Blue Team)` : Cette équipe est responsable de la sécurité interne de l'entreprise et se défend contre les cyberattaques.
- `Équipe rouge (Red Team)` : Cette équipe simule un adversaire/une attaque réelle contre l'entreprise.
- `Équipe violette (Purple Team)` : Cette équipe est composée de membres des équipes bleue et rouge qui travaillent ensemble pour améliorer la sécurité de l'entreprise.

Nous approfondirons ces équipes et d'autres aspects dans des sections individuelles.

Si vous cherchez à devenir un testeur d'intrusion (pentester) - un professionnel qui trouve et corrige les faiblesses de sécurité dans les systèmes - la compréhension de l'InfoSec est essentielle. Votre travail consiste à identifier les vulnérabilités potentielles avant que les pirates malveillants ne puissent les exploiter. En apprenant les mesures de sécurité robustes, vous pouvez aider les organisations à protéger leurs informations précieuses et à empêcher les accès non autorisés.

De plus en plus de services et de systèmes sont mis en ligne dans une tendance connue sous le nom de transformation numérique. Bien que ce changement offre de nombreux avantages comme la commodité et l'efficacité, il crée également plus d'opportunités pour les cyberattaques. Les pirates informatiques deviennent plus intelligents et plus agressifs, visant à voler des données sensibles ou à perturber des services. Ces cyberattaques peuvent entraîner des pertes financières importantes et nuire à la réputation d'une entreprise ainsi qu'à la confiance de ses clients.

Imaginez que vos informations sont comme un trésor stocké dans un château. Les murs du château, les ponts-levis et les gardes sont les mesures de sécurité protégeant votre trésor des voleurs.

- `Le trésor` : Vos données et informations précieuses.
- `Les murs du château` : Les pare-feux (Firewalls), les mécanismes de défense et le chiffrement qui empêchent les étrangers d'entrer.
- `Les gardes` : Les protocoles de sécurité et les contrôles d'accès qui surveillent qui entre et qui sort.
- `Les testeurs d'intrusion` : Des chevaliers qui testent les défenses du château en simulant des attaques pour trouver les points faibles.
- `La transformation numérique` : Agrandir le château pour y stocker plus de trésors, ce qui attire plus de voleurs.
- `Les cybermenaces` : Des voleurs qui cherchent constamment des moyens de percer les défenses du château.

Tout comme un château doit renforcer ses défenses à mesure qu'il grandit et devient une cible plus précieuse, les entreprises doivent améliorer leurs mesures d'InfoSec à mesure qu'elles déplacent plus de services en ligne. En considérant l'InfoSec comme un bâtiment ou une forteresse à protéger, il devient plus facile de comprendre l'importance d'une sécurité robuste à l'ère numérique.

La nécessité de l'InfoSec découle de la valeur de l'information à l'ère numérique. Les données personnelles, la propriété intellectuelle, les informations financières et les secrets d'État ne sont que quelques exemples des données critiques qui nécessitent une protection. Une violation peut entraîner de graves conséquences, notamment des pertes financières, une atteinte à la réputation, des ramifications juridiques et des menaces pour la sécurité nationale.

---

## Domaines de la sécurité de l'information

L'InfoSec joue un rôle essentiel dans la protection des données d'une organisation contre diverses menaces, en garantissant la `confidentialité (confidentiality)`, l'`intégrité (integrity)` et la `disponibilité (availability)` des données. Ce vaste domaine englobe une variété de domaines, et la liste fournie ici ne reprend que certains des actifs les plus généraux. Cependant, il est essentiel de noter que ces exemples ne font qu'effleurer la surface du large spectre que couvre l'InfoSec.

La gamme réelle d'actifs qui relèvent de l'InfoSec est beaucoup plus étendue et continue d'évoluer parallèlement aux avancées technologiques et au paysage en constante évolution des cybermenaces, comprenant, sans s'y limiter :

1. Sécurité des réseaux
2. Sécurité des applications
3. Sécurité opérationnelle
4. Reprise après sinistre et continuité des activités
5. Sécurité du cloud
6. Sécurité physique
7. Sécurité mobile
8. Sécurité de l'Internet des objets (IdO)

Plus tard, nous explorerons également certaines des `cybermenaces` les plus répandues, telles que les attaques par déni de service distribué (DDoS), les rançongiciels (ransomware), les menaces persistantes avancées (APT) et les menaces internes. De plus, nous examinerons la structure et la fonction des `équipes de cybersécurité`, en acquérant une compréhension de leurs domaines de spécialisation et des rôles clés au sein de ces équipes. Cet aperçu complet fournira des informations précieuses sur la manière dont les professionnels de la cybersécurité collaborent pour atténuer ces menaces en évolution et y répondre.

#### Concepts de sécurité

Un risque (risk) dans le contexte de la sécurité de l'information fait référence à la possibilité qu'un événement malveillant se produise, ce qui pourrait causer des dommages aux actifs d'une organisation, tels que ses données ou son infrastructure. Ce potentiel de dommage est généralement quantifié en termes de probabilité et de gravité de son impact. Le risque est un concept plus large qui englobe à la fois les menaces et les vulnérabilités, et la gestion des risques implique d'identifier et d'appliquer des mesures appropriées pour atténuer les menaces et minimiser les vulnérabilités.

Une menace (threat), d'autre part, est une cause potentielle d'un incident qui pourrait entraîner un préjudice pour un système ou une organisation. Il peut s'agir d'une personne, comme un cybercriminel ou un pirate, ou d'un événement naturel, comme un incendie ou une inondation. Les menaces exploitent les vulnérabilités pour compromettre la sécurité d'un système.

Une vulnérabilité (vulnerability) est une faiblesse dans un système qui pourrait être exploitée par une menace. Les vulnérabilités peuvent exister sous diverses formes, telles que des bogues logiciels, des erreurs de configuration ou des mots de passe faibles. La présence d'une vulnérabilité ne signifie pas nécessairement qu'un système sera compromis ; il doit également y avoir une menace capable d'exploiter cette vulnérabilité, et le dommage potentiel qui pourrait en résulter constitue le risque.

En substance, un risque représente le potentiel de dommage, une menace est ce qui peut causer ce dommage, et une vulnérabilité est la faiblesse qui permet à la menace de causer des dommages. Ces trois concepts sont interconnectés, et comprendre la différence entre eux est essentiel pour une gestion efficace de la sécurité de l'information.

#### Rôles dans la sécurité de l'information

Dans le vaste monde de la sécurité de l'information (InfoSec), il existe une pléthore de rôles différents, chacun ayant son propre ensemble de responsabilités. Ces rôles font partie intégrante d'une infrastructure InfoSec robuste, contribuant aux opérations sécurisées d'une organisation :

|**Rôle**|**Description**|**Pertinence pour les tests d'intrusion**|
|---|---|---|
|`Responsable de la sécurité des systèmes d'information` (`RSSI` / `CISO`)|Supervise l'ensemble du programme de sécurité de l'information|Définit la stratégie de sécurité globale que les testeurs d'intrusion évalueront|
|`Architecte en sécurité`|Conçoit des systèmes et des réseaux sécurisés|Crée les systèmes que les testeurs d'intrusion tenteront de pénétrer|
|`Testeur d'intrusion`|Identifie les vulnérabilités par le biais d'attaques simulées|Recherche et exploite activement les vulnérabilités au sein d'un système, de manière légale et éthique. C'est probablement le rôle que vous visez.|
|`Spécialiste de la réponse aux incidents`|Gère les incidents de sécurité et y répond|Travaille souvent en tandem avec les testeurs d'intrusion en répondant à leurs attaques, et en partageant/collaborant avec eux par la suite pour discuter des leçons apprises.|
|`Analyste en sécurité`|Surveille les systèmes à la recherche de menaces et analyse les données de sécurité|Peut utiliser les résultats des tests d'intrusion pour améliorer la surveillance|
|`Spécialiste de la conformité`|Assure le respect des normes et réglementations de sécurité|Les rapports de tests d'intrusion soutiennent souvent les efforts de conformité|
---

[[00 - Sommaire Introduction to Information Security|Sommaire]] | [[02 - Principes de la sécurité de l'information]] →
