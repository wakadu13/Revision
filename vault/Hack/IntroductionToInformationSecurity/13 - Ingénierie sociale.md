---
tags:
  - infosec
ordre: 13
---

# Ingénierie sociale

---

L'ingénierie sociale (social engineering) est similaire aux tactiques d'un escroc, s'appuyant sur la `manipulation psychologique` pour tromper des individus afin qu'ils révèlent des informations confidentielles ou prennent des mesures qui compromettent la sécurité. Au lieu d'utiliser des méthodes techniques pour violer des systèmes, les ingénieurs sociaux exploitent la nature humaine — nos tendances à faire confiance et à aider les autres.

Dans le domaine de la cybersécurité, l'ingénierie sociale est une menace importante car elle cible l'élément humain, souvent considéré comme le maillon le plus faible des défenses de sécurité. Peu importe le degré de sophistication des protections techniques, si un attaquant peut tromper une personne pour qu'elle révèle des mots de passe ou accorde un accès, il peut contourner même les systèmes les plus robustes.

![Schéma de réseau montrant les applications, les serveurs, le cloud, Internet et les connexions client. Inclut les employés, les appareils mobiles, l'entreprise et les équipes : Bleue, Rouge et Mauve.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/293/InfoSec.png)

Imaginez que vous êtes dans une gare très fréquentée et qu'un étranger sympathique vous aborde. Il semble serviable et digne de confiance, portant peut-être un uniforme ou des documents d'apparence officielle. Il engage la conversation, vous demande peut-être de l'aide ou vous propose quelque chose d'alléchant. Avant même de vous en rendre compte, vous lui avez remis vos bagages ou partagé des informations personnelles, pour réaliser plus tard que vous avez été piégé. Ce scénario illustre l'essence de l'`ingénierie sociale` dans le monde numérique, une manipulation habile de la confiance humaine pour obtenir un accès non autorisé à des informations ou des ressources.

---

## Comment ça marche

Les techniques d'ingénierie sociale sont des méthodes sophistiquées qui exploitent la tendance humaine fondamentale à faire confiance aux autres. Ces tactiques tirent parti des vulnérabilités psychologiques pour manipuler les individus afin qu'ils divulguent des informations confidentielles ou effectuent des actions qui compromettent la sécurité. Les cybercriminels ont développé et affiné un large éventail de techniques d'ingénierie sociale, chacune conçue pour exploiter différents aspects du comportement humain et des interactions sociales. Ces méthodes sont en constante évolution, s'adaptant aux nouvelles technologies et aux normes sociales, ce qui les rend particulièrement difficiles à contrer. Il existe cinq techniques fondamentales utilisées, mais la liste n'est pas exhaustive :

1. Hameçonnage (Phishing)
2. Prétexte (Pretexting)
3. Appâtage (Baiting)
4. Filature (Tailgating)
5. Quid Pro Quo

#### Hameçonnage (Phishing)

Imaginez recevoir un e-mail qui semble provenir de votre banque, vous pressant de mettre à jour immédiatement les informations de votre compte pour éviter sa suspension. L'e-mail fournit un lien vers un site web qui ressemble trait pour trait à celui de votre banque. Faisant confiance à l'e-mail, vous saisissez vos identifiants de connexion, qui sont alors capturés par l'attaquant.

L'hameçonnage est l'une des techniques d'ingénierie sociale les plus courantes. Les attaquants envoient des e-mails ou des messages trompeurs qui semblent provenir de sources légitimes pour inciter les individus à révéler des informations sensibles comme des noms d'utilisateur, des mots de passe ou des numéros de carte de crédit.

#### Prétexte (Pretexting)

Pensez à un scénario où quelqu'un vous appelle en prétendant appartenir au service informatique. Il dit qu'il y a un problème avec votre ordinateur et a besoin de vos identifiants de connexion pour le résoudre. Croyant qu'il est bien qui il prétend être, vous fournissez les informations. Le prétexte consiste à créer un scénario fabriqué (un prétexte) pour solliciter la cible et en extraire des informations ou la persuader d'effectuer une action.

#### Appâtage (Baiting)

Imaginez trouver une clé USB intitulée « Salaires des employés 2023 » sur le parking du bureau. Votre curiosité piquée, vous la branchez sur votre ordinateur pour voir ce qu'elle contient. À votre insu, la clé installe un logiciel malveillant (malware) sur votre système. L'appâtage utilise la promesse de quelque chose d'alléchant pour attirer les victimes dans un piège.

#### Filature (Tailgating)

Supposons que vous entriez dans un bâtiment sécurisé qui nécessite un badge d'accès. Un individu portant une grosse boîte s'approche et vous demande de tenir la porte car il ne peut pas atteindre son badge. Par politesse, vous le laissez entrer, autorisant sans le savoir un accès non autorisé. La filature implique qu'un attaquant suive une personne autorisée dans une zone à accès restreint sans les autorisations appropriées.

#### Quid Pro Quo

Imaginez recevoir un appel de quelqu'un offrant une mise à jour logicielle gratuite en échange de vos identifiants de connexion. Il promet que la mise à jour améliorera les performances de votre ordinateur. Les attaques de type quid pro quo offrent un avantage en échange d'informations ou d'un accès.

---

## Impact

L'impact des attaques d'ingénierie sociale peut être dévastateur et de grande portée. Ces attaques peuvent conduire à :

- `Violations de données (Data Breaches)` : Accès non autorisé à des informations sensibles, affectant potentiellement des millions d'utilisateurs.
- `Pertes financières` : Les entreprises peuvent subir des dommages monétaires importants par le biais de la fraude ou du vol.
- `Atteinte à la réputation` : Les organisations peuvent perdre la confiance des clients et subir des dommages à long terme pour leur image de marque.
- `Perturbation des opérations` : Les systèmes critiques peuvent être compromis, entraînant des temps d'arrêt et une perte de productivité.

Ce qui rend l'ingénierie sociale particulièrement dangereuse, c'est sa capacité à contourner des défenses technologiques sophistiquées en exploitant les vulnérabilités humaines. Même les organisations dotées de mesures de sécurité robustes peuvent être victimes de ces attaques, car elles ciblent l'élément humain imprévisible. En effet, les employés sont habilités à effectuer certaines actions au sein de leur organisation qu'un individu externe ne pourrait pas faire. Cela rend la création de défenses totalement efficaces exceptionnellement difficile, car même des individus bien formés peuvent être manipulés par un attaquant compétent.
---

← [[12 - Rançongiciel]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[14 - Menace interne]] →
