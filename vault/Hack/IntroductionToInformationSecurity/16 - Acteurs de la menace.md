---
tags:
  - infosec
ordre: 16
---

# Acteurs de la menace

---

Une « équipe » d' `Threat Actor` est un groupe organisé d'individus dotés de compétences spécialisées qui collaborent pour mener des cyberattaques. Les Équipes rouges (Red Teams) appliquent les mêmes techniques mais dans l'intention de sécuriser l'entreprise au lieu de lui nuire. Contrairement aux professionnels de la cybersécurité qui protègent les systèmes (comme l'Équipe bleue (Blue Team)), ces équipes sont les adversaires qui cherchent à percer les défenses à des fins malveillantes.

![Schéma de réseau montrant des applications, des serveurs, le cloud, internet et des connexions client. Inclut des employés, des mobiles, l'entreprise et les équipes : Bleue, Rouge et Violette.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

Un Acteur de la menace (ou son équipe) se compose de plusieurs membres clés, chacun possédant des compétences spécialisées cruciales pour l'exécution des cyberattaques. Les programmeurs experts créent des logiciels malveillants personnalisés (custom malware) pour exploiter les vulnérabilités des systèmes, tandis que les spécialistes réseau parcourent des infrastructures numériques complexes pour trouver des points faibles. Les `Social Engineers` utilisent des techniques de manipulation psychologique pour tromper des individus afin qu'ils révèlent des informations sensibles. Les analystes de données traitent les informations volées pour en extraire des renseignements de valeur, tels que des détails financiers ou des secrets commerciaux. La supervision de ces opérations est assurée par des chefs d'équipe, qui coordonnent les activités, fixent les objectifs et élaborent des stratégies pour la réussite des attaques. Cet ensemble de compétences diversifiées permet aux équipes d'acteurs de la menace de mener des cyberopérations sophistiquées de manière efficiente et efficace.

Un acteur de la menace peut également être un individu opérant de manière indépendante. Ces acteurs solitaires, souvent appelés « loups solitaires », possèdent un ensemble de compétences diversifiées qui leur permet d'exécuter des cyberattaques sans le soutien d'une équipe. Ils peuvent être motivés par des intérêts personnels, un gain financier ou des convictions idéologiques. Bien que les acteurs de la menace individuels puissent manquer des ressources des groupes plus importants, leur capacité à travailler de manière autonome peut les rendre tout aussi dangereux et parfois plus difficiles à détecter. Leurs méthodes peuvent aller de simples tentatives d'hameçonnage (phishing) au développement de logiciels malveillants sophistiqués, en fonction de leur expertise et de leurs objectifs.

Imaginez une équipe d'acteurs de la menace en cybersécurité comme un groupe de cambrioleurs hautement qualifiés planifiant le braquage d'une banque de haute sécurité. Chaque membre a un rôle unique, tout comme une équipe de pirates informatiques compte des individus spécialisés. Il y a un `scout`, qui surveille la banque, étudie son agencement, les gardes de sécurité et les horaires des patrouilles, un peu comme un acteur de la menace qui effectue une reconnaissance, recueillant des informations sur les vulnérabilités d'une cible, la configuration de son système ou les habitudes de ses employés. Ensuite, il y a le `lockpicker`, qui se spécialise dans le contournement des serrures physiques, des portes et des alarmes ; dans une équipe de cybersécurité, ce rôle correspond à la personne chargée d'exploiter les vulnérabilités logicielles ou réseau, en utilisant des outils pour infiltrer le système sans déclencher d'alarmes. Le `getaway driver`, quant à lui, planifie l'itinéraire de fuite, s'assurant de ne laisser aucune trace et de ne pas déclencher de poursuite.

Dans le cybermonde, c'est le rôle du `exfiltration specialist`, qui extrait les données en toute sécurité ou déploie un rançongiciel (ransomware) tout en échappant à la détection et en couvrant méticuleusement ses traces. Enfin, il y a le `leader` ou `strategist` qui rassemble tout le monde, coordonne leurs actions et planifie chaque phase en détail, s'assurant que tous les efforts convergent vers la réussite du braquage.

Pour exécuter ce braquage, ils utilisent des outils et des techniques spécifiques conçus pour la précision et la discrétion.

- Le scout peut utiliser des jumelles à haute puissance ou des plans, tout comme un spécialiste de la reconnaissance informatique utilise des outils tels que des scanners de réseau, la collecte de renseignements en sources ouvertes (OSINT) et l'ingénierie sociale (social engineering) pour sonder les points faibles.
- Le lockpicker peut disposer d'outils spécialisés, comme des passe-partout et des décodeurs, similaires aux malwares, rootkits ou scripts personnalisés du pirate informatique utilisés pour obtenir un accès non autorisé.
- Le getaway driver s'appuie sur sa connaissance des routes, allant peut-être même jusqu'à altérer les feux de circulation, ce qui reflète l'utilisation par le spécialiste de l'exfiltration de canaux de communication chiffrés, de techniques d'obfuscation des données et de VPN pour rester intraçable.
- Le leader assure la coordination avec des communications radio sécurisées et peut éviter l'utilisation d'équipements trop complexes qui pourraient ralentir ou compliquer le braquage.

De même, les acteurs de la menace en cybersécurité évitent d'utiliser des tactiques détectables ou à haut risque qui pourraient facilement alerter les équipes de sécurité. Ils s'abstiennent de méthodes de piratage « bruyantes », comme les attaques par force brute (brute-force attacks) qui pourraient déclencher des alarmes, ou les malwares évidents qui sont susceptibles d'être interceptés par les programmes antivirus. Au lieu de cela, ils se concentrent sur des méthodes « lentes et discrètes » (low and slow), prenant leur temps pour éviter la détection, en infiltrant les systèmes de manière subtile plutôt que de façon agressive et tape-à-l'œil.

---

## Objectifs

L'objectif principal des acteurs de la menace est d'infiltrer et d'exploiter des systèmes ou des réseaux cibles, avec des motivations couvrant un large spectre. Le gain financier est un moteur courant, impliquant le vol d'argent par des transactions frauduleuses ou l'acquisition de données de valeur pour les vendre sur le dark web. L'espionnage est un autre motif important, où ces équipes collectent des informations confidentielles auprès de gouvernements ou d'entreprises pour obtenir des avantages stratégiques.

Certains acteurs de la menace se concentrent sur la perturbation, visant à semer le chaos en interrompant des services, en supprimant des données ou en diffusant de la désinformation. Les objectifs idéologiques jouent également un rôle, certaines équipes promouvant des causes politiques, religieuses ou sociales en ciblant des organisations qui s'opposent à leurs croyances. Enfin, la vengeance peut être un puissant facteur de motivation, amenant les acteurs de la menace à attaquer des entités en représailles à des torts perçus. Cette diversité de motifs souligne la nature complexe et multiforme des cybermenaces dans le paysage numérique actuel.
---

← [[15 - Menaces persistantes avancées]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[17 - Équipe Rouge (Red Team)]] →
