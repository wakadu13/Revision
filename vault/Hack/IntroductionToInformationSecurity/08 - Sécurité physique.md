---
tags:
  - infosec
ordre: 8
---

# Sécurité physique

---

Imaginez que vous êtes le propriétaire d'une confiserie remplie de délicieuses friandises très demandées. Vous verrouillez la caisse enregistreuse et sécurisez les présentoirs de bonbons, mais si quelqu'un s'introduit dans le magasin après la fermeture, il pourrait tout emporter. La sécurité physique, c'est comme installer des serrures robustes sur vos portes, mettre en place un système d'alarme, et peut-être même engager un agent de sécurité pour protéger votre magasin des cambrioleurs. Il s'agit de tenir les personnes mal intentionnées à l'écart afin que vos friandises (ou, dans le cas de nombreuses entreprises, les informations sensibles) restent en sécurité.

En matière de sécurité de l'information, elle fait référence à la protection du matériel et des installations qui stockent et traitent les données. Cela inclut les ordinateurs, les serveurs, les baies de serveurs, les équipements réseau et même les documents imprimés. L'objectif est d'empêcher les personnes non autorisées d'accéder physiquement à ces ressources, ce qui pourrait entraîner des fuites de données (data breaches), des vols ou des dommages.

![Schéma de réseau montrant les applications, les serveurs, le cloud, Internet et les connexions client. Inclut les employés, les appareils mobiles, l'entreprise et les équipes : Bleue, Rouge et Violette.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

Bien plus que de simples serrures et gardiens, la sécurité physique est une approche globale qui intègre les personnes, les processus et la technologie pour créer une défense robuste contre les menaces physiques. Elle implique un large éventail d'éléments, allant des considérations architecturales dans la conception des bâtiments aux systèmes de contrôle d'accès, en passant par la surveillance, les contrôles environnementaux et les pratiques de sécurité du personnel.

L'objectif principal de la sécurité physique est de créer des couches de mesures de protection qui dissuadent, détectent, retardent et répondent aux menaces physiques potentielles. Cette approche en couches, souvent appelée « défense en profondeur » (defense in depth), garantit que si une mesure de sécurité échoue, d'autres sont en place pour maintenir la protection. Par exemple, une installation sécurisée peut disposer d'une clôture périmétrique pour dissuader les intrus, de systèmes de contrôle d'accès pour détecter les tentatives d'entrée non autorisées, de portes renforcées pour retarder une entrée par effraction et de personnel de sécurité sur site pour répondre aux violations.

Elle est cruciale pour plusieurs raisons :

1. Elle protège les actifs de valeur, y compris les équipements coûteux et les données critiques stockées sur des appareils physiques, contre le vol ou les dommages.
2. Elle protège le personnel, en garantissant la sécurité des employés et des visiteurs au sein d'une installation.
3. Elle aide à maintenir la continuité des opérations en prévenant les interruptions causées par des violations de la sécurité physique.
4. Elle constitue souvent un élément essentiel de la conformité réglementaire, de nombreux secteurs étant tenus de mettre en œuvre des mesures de sécurité physique spécifiques pour protéger les informations sensibles.

---

## Responsabilité

La responsabilité de la sécurité physique relève généralement de la compétence d'une équipe ou d'un service dédié à la sécurité physique. Cette équipe rend souvent compte à un Directeur de la sécurité (CSO) ou à un Directeur de la sécurité de l'information (CISO) dans les organisations où la sécurité physique et la sécurité de l'information sont étroitement intégrées. L'équipe de sécurité physique travaille en étroite collaboration avec les services de gestion des installations, les ressources humaines et les services informatiques pour mettre en œuvre et maintenir les mesures de sécurité.

Cependant, la responsabilité de la sécurité physique implique généralement plusieurs autres rôles au sein d'une organisation :

- `Équipe de gestion des installations` : Elle entretient le bâtiment et s'assure que les mesures de sécurité physique sont en place et fonctionnent.
- `Équipe de sécurité informatique` : Elle se concentre sur la sécurisation du matériel et des équipements réseau, travaillant souvent en étroite collaboration avec les équipes de sécurité physique.
- `Tous les employés` : Chacun a un rôle à jouer dans le respect des protocoles de sécurité, comme ne pas laisser les portes sécurisées ouvertes ou ne pas partager les cartes d'accès.

Le test de la sécurité physique est un domaine spécialisé qui requiert un ensemble unique de compétences et de connaissances. Les testeurs d'intrusion (penetration testers) dont le champ d'action s'étend aux tests physiques, également connus sous le nom de Red Teamers, sont des professionnels qui simulent des attaques réelles pour identifier les vulnérabilités dans les mesures de sécurité physique. Ces vulnérabilités physiques peuvent être :

|**Vulnérabilité**|**Description**|
|---|---|
|`Points d'accès non sécurisés`|Portes, fenêtres ou autres points d'entrée laissés déverrouillés ou facilement contournables|
|`Serrures faibles`|Serrures obsolètes ou de mauvaise qualité qui peuvent être facilement crochetées ou cassées|
|`Sécurité périmétrique inadéquate`|Absence de clôtures, de barrières ou de surveillance autour du périmètre de l'installation|
|`Mauvaise gestion des clés`|Manipulation ou stockage inapproprié des clés, cartes d'accès ou autres identifiants physiques|
|`Éclairage insuffisant`|Zones sombres pouvant dissimuler des intrus ou des activités criminelles|
|`Infrastructure informatique exposée`|Serveurs, équipements réseau ou baies de brassage physiquement accessibles aux personnes non autorisées|
|`Absence de gestion des visiteurs`|Protocoles faibles pour l'identification, l'accompagnement et la surveillance des visiteurs dans les zones sécurisées|
|`Postes de travail laissés sans surveillance`|Ordinateurs ou appareils laissés déverrouillés et accessibles dans des espaces publics ou partagés|

Ces tests peuvent aller de la tentative de contournement des systèmes de contrôle d'accès aux attaques d'ingénierie sociale (social engineering) visant à manipuler le personnel pour qu'il accorde un accès non autorisé. Les tests de sécurité physique comprennent également l'évaluation de l'efficacité des caméras de sécurité, le test des temps de réponse du personnel de sécurité et l'évaluation de la résilience des barrières physiques.

Dans le contexte de la sécurité de l'information, la sécurité physique joue un rôle crucial dans la protection de la confidentialité, de l'intégrité et de la disponibilité des données. Même les mesures de cybersécurité les plus sophistiquées peuvent devenir inefficaces si un attaquant obtient un accès physique aux systèmes ou aux dispositifs de stockage. Par conséquent, une stratégie de sécurité de l'information complète doit inclure des mesures de sécurité physique robustes pour protéger véritablement les actifs informationnels d'une organisation.
---

← [[07 - Sécurité du cloud]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[09 - Sécurité Mobile]] →
