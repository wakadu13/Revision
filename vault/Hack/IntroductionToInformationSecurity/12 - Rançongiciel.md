---
tags:
  - infosec
ordre: 12
---

# Rançongiciel

---

Un rançongiciel (ransomware) est un type de logiciel malveillant (ou maliciel) qui infiltre les serveurs, les ordinateurs et les réseaux, chiffrant les fichiers de valeur pour les rendre inaccessibles. Les attaquants exigent ensuite le paiement d'une rançon, souvent en cryptomonnaie comme le Bitcoin, en échange d'une clé de déchiffrement qui promet de restaurer l'accès aux données verrouillées. C'est une situation similaire à une prise d'otages numérique, où vos fichiers importants sont retenus captifs.

![Diagramme de réseau montrant les applications, les serveurs, le cloud, internet et les connexions client. Inclut les employés, les appareils mobiles, l'entreprise et les équipes : Bleue, Rouge et Violette.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

L'objectif principal d'un rançongiciel est, généralement, assez simple. Pour les cybercriminels, le but est presque toujours le gain financier. En ciblant des particuliers, des entreprises, des hôpitaux ou même des gouvernements, les attaquants cherchent à extorquer de l'argent en exploitant le besoin de la victime d'accéder à ses propres données. Cependant, l'impact d'un rançongiciel va au-delà du simple coût financier immédiat. Il peut perturber des services essentiels, éroder la confiance, nuire aux réputations et, dans des secteurs critiques comme la santé, il peut même mettre des vies en danger.

Imaginez que vous possédez une petite galerie d'art remplie de peintures et de sculptures d'une valeur inestimable. Un matin, vous arrivez et découvrez que toutes vos œuvres d'art ont été enfermées pendant la nuit derrière des vitrines impénétrables. Une note laissée sur la porte exige une somme d'argent conséquente en échange des clés pour déverrouiller les vitrines. Tant que vous ne payez pas, vous ne pouvez ni accéder à votre art ni l'exposer, et votre activité est à l'arrêt. Ce scénario troublant reflète ce qui se passe lors d'une **attaque par rançongiciel** dans le monde numérique.

---

## Comment ça fonctionne

En mai 2017, une attaque massive par rançongiciel connue sous le nom de **WannaCry** s'est propagée rapidement à travers le monde, affectant plus de 200 000 ordinateurs dans plus de 150 pays. Les hôpitaux du National Health Service (NHS) du Royaume-Uni ont été particulièrement touchés. Le personnel n'avait plus accès aux dossiers des patients, ce qui a entraîné l'annulation d'opérations chirurgicales et le détournement d'ambulances. Les attaquants exigeaient des paiements de 300 à 600 dollars en Bitcoin pour restaurer l'accès.

Une attaque par rançongiciel est un acte de cybercriminalité sophistiqué qui se déroule généralement en plusieurs étapes. Initialement, l'attaquant obtient l'accès au système de la victime, souvent par le biais d'e-mails d'hameçonnage (phishing) trompeurs qui semblent provenir de sources fiables. Ces e-mails peuvent contenir des liens ou des pièces jointes malveillants qui, lorsqu'on clique dessus ou qu'on les ouvre, installent le rançongiciel sur l'ordinateur de la victime. Une fois infiltré, le rançongiciel commence à chiffrer des fichiers tels que des documents, des photos et des bases de données à l'aide d'algorithmes complexes, brouillant ainsi les données et les rendant illisibles sans une clé de déchiffrement.

Une fois le processus de chiffrement terminé, le rançongiciel affiche un message informant la victime de la situation et fournissant des instructions sur la manière de payer la rançon, généralement avec une date limite pour éviter la perte permanente des données. Si la victime décide de payer la rançon, il n'y a aucune garantie que les attaquants fourniront la clé de déchiffrement ou que celle-ci parviendra à restaurer l'accès aux fichiers. De plus, le paiement de la rançon peut faire de la victime une cible pour de futures attaques, perpétuant ainsi le cycle de la cybercriminalité.

WannaCry exploitait une vulnérabilité des systèmes d'exploitation Microsoft Windows, en particulier sur les ordinateurs qui n'avaient pas installé les récentes mises à jour de sécurité. L'attaque a causé des milliards de dollars de dommages dans le monde entier et a mis en évidence les vulnérabilités des infrastructures critiques.

---

## Impact

Les rançongiciels représentent une menace importante en raison de leur potentiel de perturbation à grande échelle dans divers secteurs. Les impacts d'une attaque par rançongiciel peuvent être graves et étendus. Les organisations peuvent faire face à des `arrêts opérationnels`, paralysant les entreprises et les services. Dans des secteurs critiques comme la santé, cela pourrait signifier l'incapacité d'accéder aux dossiers des patients ou de planifier des traitements, mettant potentiellement des vies en danger. Les `pertes financières` vont au-delà de la rançon elle-même, englobant les coûts associés à l'interruption d'activité, aux efforts de récupération et à la mise en œuvre de nouvelles mesures de sécurité.

La `perte de données` est une autre préoccupation majeure, surtout si les sauvegardes ne sont pas disponibles ou sont compromises, ce qui peut entraîner la perte permanente d'informations importantes. Les violations de données très médiatisées peuvent entraîner une `atteinte à la réputation` considérable, érodant la confiance des clients et provoquant potentiellement une baisse des revenus à long terme. Peut-être de manière plus insidieuse, le paiement des rançons peut perpétuer le cycle de la cybercriminalité, encourageant les attaquants à poursuivre leurs activités malveillantes et marquant potentiellement la victime comme une cible pour de futures attaques.

Prenons un autre exemple. Imaginez une bibliothèque publique qui constitue une ressource vitale pour la communauté. Un jour, tous les livres se retrouvent enfermés dans des boîtes spéciales avec des codes, et une note exige un paiement pour obtenir les codes permettant de les déverrouiller. Tant que la rançon n'est pas payée, personne ne peut emprunter de livres, étudier ou accéder à l'information. Cela n'affecte pas seulement la bibliothèque, mais aussi les étudiants, les chercheurs et toute personne qui dépend de ses ressources.

De même, un rançongiciel n'a pas d'impact que sur la victime immédiate. Il peut avoir des effets d'entraînement sur toutes les personnes qui dépendent des services fournis par l'organisation compromise. Le coût annuel de la cybercriminalité s'élèvera à des milliers de milliards de dollars par an d'ici 2025 selon [CybersecurityVentures](https://cybersecurityventures.com/hackerpocalypse-cybercrime-report-2016/).
---

← [[11 - Déni de service distribué]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[13 - Ingénierie sociale]] →
