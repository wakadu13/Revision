---
tags:
  - infosec
ordre: 15
---

# Menaces persistantes avancées

---

Une `menace persistante avancée` (`APT` pour Advanced Persistent Threat) est une cyberattaque sophistiquée et continue au cours de laquelle un intrus obtient un accès non autorisé au réseau d'une entreprise et reste non détecté pendant une longue période. Contrairement aux cyberattaques classiques qui sont rapides et visent un gain immédiat, les APT sont des opérations à long terme qui exigent des ressources et une planification considérables. Elles sont souvent menées par des groupes bien financés, parfois parrainés par des États-nations ou des organisations criminelles.

![Schéma de réseau montrant des applications, des serveurs, le cloud, internet et des connexions client. Inclut les employés, les appareils mobiles, l'entreprise et les équipes : Blue, Red et Purple.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

Imaginez que vous possédez un grand musée rempli d'artefacts et de trésors inestimables. Vous avez installé des systèmes de sécurité de pointe comme des alarmes, des caméras et des gardes à chaque entrée. Ces mesures protègent contre les voleurs typiques qui pourraient tenter de s'introduire rapidement pour voler ce qu'ils peuvent. Cependant, un groupe de voleurs d'art hautement qualifiés décide de cibler votre musée. Au lieu d'un vol à l'arraché, ils planifient méticuleusement. Ils étudient vos protocoles de sécurité, se lient d'amitié avec votre personnel et, au fil du temps, s'infiltrent dans votre musée déguisés en employés ou en sous-traitants. Une fois à l'intérieur, ils se déplacent avec précaution, évitant d'être détectés tout en volant des pièces de valeur une par une. Ce cambriolage prolongé et furtif est similaire à ce qui se passe lors d'une **APT** dans le monde de la cybersécurité.

L'objectif principal d'une APT va au-delà du gain financier immédiat, se concentrant plutôt sur l'établissement d'un `accès à long terme` à des informations sensibles ou à des systèmes critiques. Les attaquants APT poursuivent une variété de cibles de grande valeur, chacune ayant des conséquences potentiellement considérables. Ces objectifs peuvent inclure le vol de propriété intellectuelle, comme des secrets commerciaux, des données de recherche de pointe ou des technologies propriétaires, qui peuvent fournir des avantages concurrentiels significatifs.

Les informations gouvernementales, y compris les documents classifiés et les rapports de renseignement, constituent une autre cible de choix, pouvant potentiellement compromettre la sécurité nationale. Les APT visent également à obtenir des avantages stratégiques en accédant à des informations qui procurent des bénéfices économiques, politiques ou militaires aux attaquants ou à leurs sponsors. Peut-être plus alarmant encore, certaines APT sont conçues pour la perturbation, avec la capacité de saboter des infrastructures critiques comme les réseaux électriques, les réseaux de communication ou les systèmes financiers, provoquant potentiellement un chaos généralisé et des dommages économiques. La nature diverse et les enjeux élevés de ces objectifs soulignent la menace sérieuse que les APT représentent pour les organisations comme pour les nations.

---

## Comment ça fonctionne

Une attaque APT se déroule en une série d'étapes soigneusement orchestrées, un peu comme un cambriolage complexe dans une installation de haute sécurité. Elle commence par la reconnaissance, où les attaquants collectent méticuleusement des informations sur leur cible, à la manière de voleurs étudiant des plans et des protocoles de sécurité. Vient ensuite l'infiltration initiale, souvent par des courriels d'hameçonnage ciblé (spear-phishing) personnalisés ou l'exploitation de vulnérabilités, comparable à des voleurs utilisant des déguisements ou trouvant des entrées cachées. Une fois à l'intérieur, les attaquants établissent une tête de pont en installant des logiciels malveillants et en créant des portes dérobées (backdoors), de la même manière que des voleurs installeraient des cachettes secrètes dans l'installation.

Ils se livrent ensuite à un mouvement latéral (lateral movement), en procédant à une escalade de privilèges et en compromettant d'autres systèmes, comme des voleurs désactivant méthodiquement les alarmes et accédant à des zones restreintes. L'étape critique de l'exfiltration de données (data exfiltration) consiste à transférer furtivement des informations de valeur hors du réseau, un peu comme des voleurs feraient sortir clandestinement des biens de grande valeur. Enfin, les attaquants maintiennent la persistance, s'assurant de pouvoir revenir même s'ils sont partiellement découverts, ce qui est analogue à des voleurs établissant de multiples voies de fuite et planques. Cette approche multicouche permet aux APT de rester non détectées pendant de longues périodes, ce qui en fait une menace redoutable dans le paysage de la cybersécurité.

En 2020, l'un des incidents APT les plus significatifs s'est produit lors de l'`attaque SolarWinds`. Des attaquants, que l'on pense être parrainés par un État, ont infiltré SolarWinds, une entreprise fournissant des logiciels de gestion de réseau utilisés par des milliers d'organisations, y compris des agences gouvernementales américaines et des entreprises du Fortune 500. Les attaquants ont inséré du code malveillant dans une mise à jour logicielle de routine. Lorsque les clients ont installé la mise à jour, ils ont sans le savoir introduit le logiciel malveillant dans leurs propres systèmes. Cette attaque de la chaîne d'approvisionnement (supply chain attack) a permis aux attaquants d'espionner un grand nombre d'organisations, de voler des données sensibles et de rester non détectés pendant de nombreux mois.

---

## Impact

Les APT comptent parmi les cybermenaces les plus dangereuses et les plus dommageables auxquelles les organisations sont confrontées aujourd'hui. Leur impact est profond, affectant non seulement la sécurité immédiate des données, mais aussi la viabilité à long terme et la réputation des organisations.

De telles attaques APT peuvent avoir des impacts dévastateurs sur les organisations, allant de pertes financières importantes à des dommages de réputation à long terme. Le coût financier d'une attaque APT peut être considérable, englobant les coûts directs liés au vol d'informations sensibles, les processus de récupération coûteux et les temps d'arrêt opérationnel. Au-delà des pertes monétaires, les APT peuvent gravement nuire à la réputation d'une organisation, érodant la confiance des clients et attirant une publicité négative.

Des conséquences juridiques et réglementaires s'ensuivent souvent, notamment des violations de conformité, de lourdes amendes et des poursuites judiciaires potentielles. La perte de propriété intellectuelle peut saper l'avantage concurrentiel d'une entreprise, tandis que les attaques contre les infrastructures critiques posent de graves risques pour la sécurité nationale. Les APT entraînent également des perturbations opérationnelles, une augmentation des coûts de sécurité et des impacts psychologiques sur les employés. La nature persistante de ces menaces signifie que les organisations doivent rester vigilantes face aux portes dérobées cachées et aux attaques récurrentes. À plus grande échelle, les APT peuvent avoir des implications économiques et politiques mondiales significatives, pouvant tendre les relations internationales et modifier les équilibres de pouvoir économique par le biais de l'espionnage industriel.
---

← [[14 - Menace interne]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[16 - Acteurs de la menace]] →
