---
tags:
  - infosec
ordre: 6
---

# Reprise après sinistre et continuité d'activité

---

La reprise après sinistre (Disaster Recovery, `DR`) et la continuité d'activité (Business Continuity, `BC`) sont des composantes essentielles de la stratégie de résilience d'une organisation, conçues pour garantir qu'une entreprise puisse continuer à fonctionner face à des perturbations importantes. Bien que souvent mentionnés ensemble, ces deux concepts ont des objectifs et des méthodologies distincts. La reprise après sinistre traite principalement de la restauration des systèmes et des données critiques à la suite d'un événement catastrophique. Cela peut inclure des catastrophes naturelles comme des tremblements de terre ou des inondations, des catastrophes d'origine humaine comme des incendies ou des attaques terroristes, ou des défaillances technologiques comme des pannes majeures de système ou des cyberattaques. L'objectif de la DR est de minimiser le temps d'arrêt et la perte de données, en s'assurant qu'une organisation puisse reprendre rapidement ses fonctions essentielles. Un plan de DR typique comprend des procédures détaillées pour la sauvegarde des données, la réplication des systèmes et le basculement (failover) vers des sites de secours ou des environnements cloud.

![Schéma réseau montrant les applications, les serveurs, le cloud, Internet et les connexions des clients. Inclut les employés, les appareils mobiles, l'entreprise et les équipes : Bleue, Rouge et Violette.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

Imaginez que vous organisez un grand concert dans un parc. Vous avez tout planifié : la scène, le système de sonorisation, les artistes et les places pour le public. Mais que se passerait-il s'il se mettait soudainement à pleuvoir à verse ou s'il y avait une panne de courant ? La reprise après sinistre et la continuité d'activité sont comme vos plans de secours pour que le spectacle continue malgré les problèmes inattendus.

#### Reprise après sinistre

Pensez à la `Reprise après sinistre` (`DR`) comme le fait d'apporter un parapluie et un générateur au concert. S'il commence à pleuvoir, vous installez rapidement le parapluie au-dessus de la scène pour protéger l'équipement. Si le courant est coupé, vous allumez le générateur pour que les lumières et le son continuent de fonctionner. La DR se concentre sur la restauration des parties critiques qui ont échoué afin que l'événement puisse se poursuivre avec une interruption minimale. Dans une entreprise, la DR implique des mesures pour récupérer les systèmes et les données importants après un incident grave, comme une cyberattaque ou une catastrophe naturelle. Il s'agit de remettre en service les éléments essentiels le plus rapidement possible.

#### Continuité d'activité

La `Continuité d'activité` (`BC`) est un plan plus large. C'est comme avoir un plan d'urgence pour déplacer le concert à l'intérieur si les prévisions météorologiques sont mauvaises ou organiser une performance acoustique si tout le reste échoue. La BC garantit que, quoi qu'il arrive, le concert (l'entreprise) puisse continuer, même si des ajustements sont nécessaires. Pour les entreprises, la BC signifie trouver comment maintenir les opérations pendant et après une perturbation. Cela peut impliquer que les employés travaillent à domicile, utilisent des fournisseurs alternatifs ou déménagent dans un bureau temporaire.

Une stratégie DR/BC bien développée peut faire la différence entre une organisation qui surmonte une crise et une qui y succombe. Ces plans protègent non seulement contre les pertes financières, mais aident également à maintenir la confiance des clients, à respecter les exigences réglementaires et à préserver la réputation d'une organisation.

---

## Responsabilité

La responsabilité de la `DR` et de la `BC` incombe généralement à une équipe dédiée au sein d'une organisation, souvent dirigée par un Responsable de la continuité d'activité ou un rôle similaire. Cette équipe travaille en étroite collaboration avec les services informatiques, les opérations et la direction pour développer, mettre en œuvre et maintenir les plans de DR/BC. Elle effectue des évaluations des risques, identifie les fonctions commerciales critiques, fixe les `Objectifs de temps de reprise` (Recovery Time Objectives, `RTOs`) et les `Objectifs de point de reprise` (Recovery Point Objectives, `RPOs`), et conçoit des stratégies pour atteindre ces objectifs.

Les testeurs d'intrusion (penetration testers) peuvent jouer un rôle précieux dans ce processus, en aidant à identifier les vulnérabilités qui pourraient compromettre les efforts de DR et de BC et en testant l'efficacité des procédures de reprise. Le test des plans de DR et de BC est un processus crucial et continu. Des tests et des exercices réguliers garantissent que les plans sont efficaces et que le personnel connaît son rôle en cas de crise. Ces tests peuvent aller d'exercices sur table (tabletop exercises), où les membres de l'équipe passent en revue leurs réponses à un scénario simulé, à des simulations à grande échelle qui impliquent un basculement effectif vers des systèmes de sauvegarde ou des sites de secours. La fréquence et la portée des tests dépendent de la taille, de la complexité et des exigences réglementaires de l'organisation, mais des tests annuels sont courants pour de nombreuses entreprises.
---

← [[05 - Sécurité Opérationnelle]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[07 - Sécurité du cloud]] →
