---
tags:
  - infosec
ordre: 4
---

# Sécurité des applications

---

La sécurité des applications (Application Security) est une composante essentielle de la sécurité de l'information et constitue souvent un facteur important dans les brèches si elle n'est pas correctement mise en œuvre. Elle se concentre sur la protection des applications logicielles contre les menaces externes tout au long de leur cycle de vie. Cela englobe un large éventail de pratiques, d'outils et de méthodologies conçus pour identifier, prévenir et atténuer les vulnérabilités de sécurité dans le code des applications et leur infrastructure associée.

![Schéma de réseau montrant des applications, des serveurs, le cloud, Internet et des connexions client. Inclut des employés, des appareils mobiles, une entreprise et des équipes : Bleue, Rouge et Violette.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

L'objectif principal est de s'assurer que les applications sont développées, déployées et maintenues d'une manière qui préserve la confidentialité, l'intégrité et la disponibilité ([triade CIA](https://www.fortinet.com/resources/cyberglossary/cia-triad)) des données qu'elles traitent et des systèmes avec lesquels elles interagissent. Ceci est particulièrement crucial dans le paysage numérique interconnecté d'aujourd'hui, où les applications gèrent souvent des informations sensibles et sont exposées à une myriade de menaces potentielles provenant d'acteurs malveillants.

La sécurité des applications commence dès les premières étapes du cycle de vie du développement logiciel et se poursuit jusqu'au déploiement et à la maintenance continue. Elle implique une combinaison de pratiques de codage sécurisé, de procédures de test rigoureuses et de la mise en œuvre de divers contrôles de sécurité. Les développeurs jouent un rôle crucial dans ce processus en écrivant du code qui respecte les meilleures pratiques de sécurité et qui est résistant aux vulnérabilités courantes telles que l'injection SQL (SQL injection), le cross-site scripting (XSS) et les dépassements de tampon (buffer overflows).

Imaginez que vous concevez une maison et que l'objectif est de s'assurer qu'elle est à l'abri des cambrioleurs (pirates informatiques) et des catastrophes naturelles (menaces). Vous trouverez ci-dessous un pseudo-code simple illustrant le fonctionnement de la sécurité des applications, décomposé étape par étape :

#### Pseudo-application logicielle

Maintenant, imaginons que nous travaillons avec un logiciel qui pourrait être vulnérable. Pour faciliter la compréhension de ce concept, nous utiliserons un pseudo-code en guise d'exemple. Cet exemple illustrera comment un `programme` (ou le `processus` de construction et de sécurisation d'une maison) pourrait fonctionner.

Le pseudo-code est une manière simplifiée et informelle de décrire la logique et la structure d'un programme. Il utilise un langage clair mélangé à des concepts de programmation de base, ce qui le rend facile à comprendre pour les publics techniques et non techniques. Contrairement au code réel, le pseudo-code n'est pas destiné à être exécuté par un ordinateur, mais sert de guide pour visualiser le fonctionnement d'un processus ou d'un programme.

```python
# 1. Commencer à construire la maison (Développer l'application) def build_house():     # Mettre des serrures sur les portes et les fenêtres (Authentification sécurisée)     install_locks_on_doors_and_windows()      # Utiliser des murs et des matériaux solides (Écrire du code sécurisé)     use_strong_materials_for_walls()      # S'assurer que le toit ne fuit pas (Chiffrer les données)     install_waterproof_roof()   # 2. Inspecter la maison à la recherche de points faibles (Tester les vulnérabilités) def inspect_house():     # Vérifier si les portes sont bien verrouillées (Tests d'intrusion)     test_if_locks_are_working()      # S'assurer qu'il n'y a pas de fissures dans les murs (Rechercher des bogues)     look_for_cracks_in_walls()      # Tester si le toit résiste à la pluie (Tester la sécurité des données)     test_roof_with_water()   # 3. Maintenir la sécurité de la maison dans le temps (Surveillance continue de la sécurité) def maintain_house_security():     # Surveiller toute activité inhabituelle (Surveiller les menaces)     install_security_cameras()      # Réparer les nouvelles fissures et remplacer les serrures cassées (Corriger les vulnérabilités)     repair_cracks_and_replace_broken_locks()   # Le processus global de la sécurité des applications def protect_application():     build_house()              # Développer l'application de manière sécurisée     inspect_house()            # Tester les vulnérabilités     maintain_house_security()  # Surveiller et maintenir la sécurité dans le temps   # Appeler la fonction pour sécuriser l'application (la maison) protect_application()
```

Décortiquons cela :

#### 1. Commencer à construire la maison (Développer l'application)

- `Serrures sur les portes et les fenêtres` : Lorsque vous créez une application, vous devez vous assurer que seules les bonnes personnes peuvent y accéder (authentification), tout comme une maison a besoin de bonnes serrures pour tenir les étrangers à l'écart.
- `Murs et matériaux solides` : Le code de l'application doit être solide et exempt de faiblesses que les pirates pourraient exploiter, tout comme vous construiriez une maison avec des matériaux solides pour l'empêcher de s'effondrer.
- `Toit étanche` : Chiffrer les données signifie protéger les informations sensibles, comme s'assurer que le toit de votre maison ne fuit pas pendant la pluie. Cela garantit que personne ne peut lire ou voler vos données pendant leur transfert.

---

#### 2. Inspecter la maison à la recherche de points faibles (Tester les vulnérabilités)

- `Vérifier si les serrures fonctionnent` : C'est comme tester une application pour voir si des pirates peuvent s'y introduire en essayant différentes méthodes (tests d'intrusion - penetration testing).
- `Rechercher des fissures dans les murs` : Tout comme vous inspecteriez une maison à la recherche de fissures, les développeurs doivent vérifier le code de leur application pour y déceler des bogues ou des points faibles qui pourraient être utilisés par des attaquants.
- `Tester le toit avec de l'eau` : Après avoir construit l'application, vous devez vous assurer que les données sensibles restent protégées, tout comme vous testeriez un toit pour vous assurer qu'il ne fuit pas pendant une tempête.

#### 3. Maintenir la sécurité de la maison dans le temps (Surveillance continue de la sécurité)

- `Installer des caméras de sécurité` : Même après avoir construit et testé votre application, vous devez la surveiller régulièrement pour détecter toute nouvelle menace ou tout nouveau problème, tout comme vous utiliseriez des caméras de sécurité pour surveiller les intrus.
- `Réparer les fissures et remplacer les serrures cassées` : Les applications nécessitent des mises à jour régulières pour corriger les vulnérabilités ou les bogues, tout comme vous répareriez des fissures ou remplaceriez des serrures cassées pour maintenir la sécurité d'une maison.

Or, lorsque le processus `test_if_locks_are_working()` se passe mal, par exemple lorsque le vérificateur omet de tester une porte en raison d'une erreur ou d'un manque de temps pour remplacer la serrure, cela laisse un point d'entrée vulnérable. Si un intrus (pirate) remarque que cette serrure spécifique ne fonctionne pas, il peut exploiter cette faiblesse pour s'introduire dans la maison (l'application).

Une approche clé est appelée `Security by Design` (sécurité dès la conception), ce qui signifie que la sécurité n'est pas une préoccupation tardive, mais qu'elle est intégrée à l'application dès le départ. Pour poursuivre notre analogie, imaginez que vous construisez une maison. Si vous la concevez en tenant compte de la sécurité dès le début, vous choisirez des matériaux solides, des serrures sécurisées, et peut-être même mettrez en place un système de surveillance alors que la maison est encore en construction. De cette façon, la maison est sécurisée de A à Z, et non pas après coup, une fois qu'elle est déjà construite. Cependant, la sécurité ne s'arrête pas au code de l'application. Tout comme une maison a besoin d'un quartier sûr, de services publics fiables et d'un bon éclairage, les applications ont également besoin d'un environnement sûr.

Dans le développement logiciel, la sécurité dès la conception fonctionne de la même manière. Lors de la création d'une application, les développeurs pensent à la sécurité dès la phase de planification. Cela peut inclure :

- `Modélisation des menaces` (threat modeling) : Tout comme on imagine toutes les manières dont quelqu'un pourrait s'introduire dans votre maison, la modélisation des menaces aide les développeurs à identifier très tôt les risques potentiels pour l'application.
- `Revues de code sécurisé` : Après avoir écrit le code, les développeurs le vérifient soigneusement pour s'assurer qu'il n'y a pas de points faibles, de la même manière que l'on inspecte les fondations de la maison à la recherche de fissures avant de terminer la construction.
- `Serveurs et bases de données` : Ils sont comme le terrain sur lequel votre maison est construite et l'approvisionnement en eau qu'elle utilise. S'ils ne sont pas sécurisés, l'ensemble du système est en danger.
- `Authentification et autorisation` : Considérez-les comme des serrures de haute qualité sur vos portes. L'authentification garantit que seules les bonnes personnes peuvent entrer, tandis que l'autorisation s'assure qu'elles ne peuvent accéder qu'aux pièces (données) qui leur sont autorisées.

---

## Responsabilité de la sécurité des applications

La responsabilité de la sécurité des applications incombe généralement à plusieurs rôles différents au sein d'une organisation. Les `développeurs d'applications` sont en première ligne, responsables de l'écriture de code sécurisé et de la mise en œuvre des fonctionnalités de sécurité. Les `architectes de sécurité` conçoivent la structure de sécurité globale des applications et de leur infrastructure de soutien. Les équipes des `opérations informatiques` sont responsables du maintien de la sécurité de l'environnement de production où les applications s'exécutent. La gestion globale de la sécurité des applications incombe souvent à un `responsable de la sécurité des applications` dédié ou, dans les grandes organisations, au directeur de la sécurité des systèmes d'information (`CISO` - Chief Information Security Officer). Ces personnes sont chargées de définir les politiques de sécurité des applications, de garantir la conformité avec les normes et réglementations de sécurité pertinentes, et de superviser la mise en œuvre des mesures de sécurité sur l'ensemble des applications d'une organisation.

Tester la sécurité d'une application est une partie cruciale du processus et est généralement effectué par des `testeurs de sécurité` spécialisés ou des `testeurs d'intrusion` (penetration testers). Ces professionnels utilisent une variété d'outils et de techniques pour identifier les vulnérabilités dans les applications, y compris des outils d'analyse statique et dynamique, des techniques de fuzzing et des revues de code manuelles. Ils peuvent également effectuer des attaques simulées sur les applications pour tester leur résilience face aux menaces du monde réel. Cependant, l'évaluation globale de la sécurité des applications n'est pas un effort ponctuel, mais un processus continu. De nouvelles vulnérabilités et techniques d'attaque apparaissent constamment, ce qui nécessite une surveillance, des tests et une mise à jour continus des mesures de sécurité. Cela implique souvent l'utilisation d'outils de sécurité automatisés qui peuvent analyser les applications à la recherche de vulnérabilités de manière continue, ainsi que des évaluations de sécurité et des tests d'intrusion réguliers.

De nos jours, où les violations de données (data breaches) et les cyberattaques peuvent entraîner des pertes financières importantes, une atteinte à la réputation et des conséquences juridiques, une sécurité des applications robuste est essentielle pour toute organisation qui développe ou utilise des applications logicielles.

De nombreuses entreprises sont confrontées au défi d'équilibrer la sécurité avec la pression du temps pour lancer rapidement des applications. C'est une difficulté courante, car les entreprises sont souvent pressées de publier de nouvelles applications ou mises à jour pour rester compétitives sur le marché. Cependant, précipiter le processus peut conduire à prendre des raccourcis en matière de sécurité, ce qui peut laisser l'application vulnérable aux attaques. Imaginez que vous construisez une maison, mais que vous avez un délai serré pour emménager. Vous pourriez être tenté de sauter quelques étapes pour finir plus vite, peut-être ne pas vérifier chaque fenêtre installée ou précipiter l'installation des serrures sur les portes du jardin. Bien que la maison puisse paraître prête, le manque de contrôles de sécurité appropriés pourrait la laisser exposée aux cambrioleurs.

En mettant en œuvre des mesures complètes de sécurité des applications, les organisations peuvent protéger leurs données et systèmes critiques, maintenir la confiance de leurs utilisateurs et assurer la continuité de leurs opérations face à l'évolution des cybermenaces.
---

← [[03 - Sécurité des réseaux]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[05 - Sécurité Opérationnelle]] →
