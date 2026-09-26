---
tags:
  - infosec
ordre: 9
---

# Sécurité Mobile

---

Imaginez que vous transportez partout avec vous un véritable coffre au trésor, rempli de vos biens les plus précieux comme des lettres personnelles, une pièce d'identité, des contacts, des clés, de l'argent, des photos de famille, des documents financiers, des contrats et même des fichiers de travail confidentiels. Ce coffre au trésor est votre appareil mobile, un smartphone ou une tablette qui contient une grande quantité d'informations sensibles. Tout comme vous protégeriez un vrai coffre au trésor contre les voleurs et les curieux, il est crucial de protéger votre appareil mobile contre diverses menaces numériques. C'est là que la sécurité mobile entre en jeu.

La sécurité mobile est un aspect essentiel de la sécurité de l'information qui se concentre sur la protection des appareils mobiles, des données qu'ils stockent et des réseaux auxquels ils se connectent contre un large éventail de menaces. Ces menaces peuvent inclure des hackers essayant de voler des informations personnelles, des applications malveillantes visant à corrompre votre appareil, ou des réseaux non sécurisés exposant vos données à des regards indiscrets. À mesure que les appareils mobiles deviennent une partie intégrante de notre vie quotidienne, assurer leur sécurité est plus important que jamais.

![Schéma de réseau montrant des applications, des serveurs, le cloud, Internet et des connexions client. Inclut des employés, des appareils mobiles, une entreprise et des équipes : Bleue, Rouge et Violette.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

L'objectif principal de la sécurité mobile est de protéger les informations sensibles stockées et transmises par les appareils mobiles. Cela inclut des données personnelles comme les contacts et les messages, des informations financières telles que les coordonnées bancaires et les numéros de carte de crédit, et des données d'entreprise comme les e-mails confidentiels et les documents professionnels. Les appareils mobiles servent souvent de passerelles vers nos vies personnelles et professionnelles, ce qui en fait des cibles attrayantes pour les cybercriminels.

---

## Protection de l'appareil

Protéger les appareils mobiles implique plusieurs couches de mesures de sécurité, chacune traitant différents aspects des vulnérabilités potentielles.

|Sécurité de l'appareil|Sécurité des données|Sécurité du réseau|Sécurité des applications|
|---|---|---|---|

Pour garder votre coffre au trésor en sécurité, vous avez besoin de serrures solides qui empêchent tout accès non autorisé (`device security`). Ceci est réalisé grâce à des codes d'accès, qui agissent comme des clés que vous seul possédez. L'authentification biométrique ajoute une couche supplémentaire en utilisant des caractéristiques physiques uniques comme les empreintes digitales ou la reconnaissance faciale, rendant encore plus difficile pour quelqu'un d'autre de déverrouiller votre appareil. De plus, des fonctionnalités comme les capacités d'effacement à distance vous permettent d'effacer toutes les données de votre appareil s'il est perdu ou volé, garantissant que vos informations ne tombent pas entre de mauvaises mains.

À l'intérieur de votre coffre au trésor se trouvent vos objets de valeur, les données. Même si quelqu'un parvient à forcer le coffre, vous pouvez toujours protéger vos trésors en les plaçant dans un coffre-fort à l'intérieur du coffre (`data security`). Dans le monde numérique, cela se fait par le chiffrement, qui brouille vos données afin qu'elles ne puissent être lues qu'avec la bonne clé de déchiffrement. Les sauvegardes sécurisées agissent comme des doubles de vos trésors stockés en lieu sûr ailleurs, afin que vous ne perdiez pas tout si quelque chose arrive à votre appareil. Les stratégies de prévention de la perte de données (Data Loss Prevention) garantissent que les informations sensibles ne sont pas partagées ou divulguées accidentellement.

Lorsque vous utilisez votre appareil mobile pour vous connecter à Internet, c'est comme si vous envoyiez vos trésors à travers un réseau de routes (`network security`). Les réseaux Wi-Fi publics sont comme des routes non surveillées où des bandits (hackers) peuvent facilement intercepter vos biens. Protéger votre appareil sur ces réseaux est crucial. Les réseaux privés virtuels (VPN) agissent comme des tunnels privés et sécurisés qui protègent vos données pendant leur transit, empêchant les autres d'écouter. Les protocoles de communication sécurisés garantissent que les données échangées entre votre appareil et d'autres services restent confidentielles et à l'abri de toute falsification.

Les applications sont comme les outils et les gadgets que vous placez dans votre coffre au trésor. Cependant, tous les outils ne sont pas sûrs et certains peuvent être défectueux ou même délibérément nuisibles (`application security`). La vérification des applications consiste à sélectionner soigneusement les applications à installer, un peu comme on inspecte des outils avant de les utiliser. La gestion des autorisations vous permet de contrôler ce à quoi chaque application peut accéder sur votre appareil, en veillant à ce qu'elles n'outrepassent pas leurs droits et n'accèdent pas à plus d'informations que nécessaire. Les pratiques de développement sécurisé par les créateurs d'applications aident à garantir que les applications sont conçues en tenant compte de la sécurité dès le départ.

---

## Responsabilité

Protéger les appareils mobiles au sein d'une organisation est un effort collaboratif impliquant plusieurs rôles clés :

1. Les `IT departments` mettent en œuvre et gèrent des solutions de sécurité comme les réseaux sécurisés et le chiffrement des appareils
2. Les responsables de la sécurité des systèmes d'information (Chief Information Security Officers) (`CISOs`) élaborent des stratégies de sécurité globales, évaluent les risques liés à l'utilisation des appareils mobiles et garantissent la conformité avec les exigences légales et réglementaires
3. Les `Security teams` se spécialisent dans le test et l'évaluation des mesures de sécurité, en réalisant des tests d'intrusion (penetration testing) pour identifier et corriger les vulnérabilités
4. Les `IT security managers` supervisent les opérations quotidiennes, s'assurant que les politiques sont respectées, que les outils de sécurité fonctionnent correctement et en adaptant les mesures pour contrer les nouvelles menaces.

De nos jours, la sécurité mobile est essentielle. Les appareils mobiles sont des extensions de nous-mêmes, détenant les clés de nos vies personnelles et de nos responsabilités professionnelles. Protéger ces appareils ne consiste pas seulement à préserver le matériel, mais aussi à sécuriser les grandes quantités de données sensibles qu'ils transportent et les réseaux auxquels ils se connectent.
---

← [[08 - Sécurité physique]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[10 - Sécurité de l'Internet des objets]] →
