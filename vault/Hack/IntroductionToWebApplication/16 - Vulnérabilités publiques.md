---
tags:
  - web-applications
ordre: 16
---

# Vulnérabilités publiques

---

Les vulnérabilités les plus critiques des composants back-end sont celles qui peuvent être attaquées de l'extérieur et exploitées pour prendre le contrôle du serveur back-end sans nécessiter un accès local à ce serveur (c'est-à-dire, via des tests d'intrusion externes (external penetration testing)). Ces vulnérabilités sont généralement causées par des erreurs de codage commises lors du développement des composants back-end d'une application web. Il existe donc une grande variété de types de vulnérabilités dans ce domaine, allant de vulnérabilités de base qui peuvent être exploitées avec une facilité relative à des vulnérabilités sophistiquées nécessitant une connaissance approfondie de l'ensemble de l'application web.

---

## CVE publiques

Étant donné que de nombreuses organisations déploient des applications web qui sont utilisées publiquement, comme les applications web open-source et propriétaires, ces applications web ont tendance à être testées par de nombreuses organisations et experts du monde entier. Cela conduit à la découverte fréquente d'un grand nombre de vulnérabilités, dont la plupart sont corrigées puis partagées publiquement et se voient attribuer un enregistrement et un score CVE ([Common Vulnerabilities and Exposures](https://en.wikipedia.org/wiki/Common_Vulnerabilities_and_Exposures)).

De nombreux testeurs d'intrusion créent également des exploits de type preuve de concept (proof of concept) pour tester si une certaine vulnérabilité publique peut être exploitée et rendent généralement ces exploits disponibles pour un usage public, à des fins de test et d'éducation. Cela fait de la recherche d'exploits publics la toute première étape que nous devons suivre pour les applications web.

Astuce : La première étape consiste à identifier la version de l'application web. Celle-ci peut être trouvée à de nombreux endroits, comme dans le code source de l'application web. Pour les applications web open-source, nous pouvons vérifier le dépôt de l'application web et identifier où le numéro de version est affiché (par exemple, dans la page (version.php)), puis vérifier la même page sur notre application web cible pour confirmer.

Une fois que nous avons identifié la version de l'application web, nous pouvons rechercher sur Google des exploits publics pour cette version de l'application. Nous pouvons également utiliser des bases de données d'exploits en ligne, comme [Exploit DB](https://www.exploit-db.com/), [Rapid7 DB](https://www.rapid7.com/db/) ou [Vulnerability Lab](https://www.vulnerability-lab.com/). L'exemple suivant montre une recherche d'exploits publics pour WordPress dans [Rapid7 DB](https://www.rapid7.com/db/) :

https://www.rapid7.com/db/?q=wordpress&type=nexpose

![Page de la base de données de vulnérabilités et d'exploits montrant les résultats de recherche pour les vulnérabilités 'WordPress', incluant les détails CVE et la sévérité.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/rapid7-db.jpg)

Nous serons généralement intéressés par les exploits ayant un score CVE de 8-10 ou les exploits qui mènent à une `exécution de code à distance (Remote Code Execution)`. D'autres types d'exploits publics devraient également être considérés si aucun des précédents n'est disponible.

De plus, ces vulnérabilités ne sont pas exclusives aux applications web et s'appliquent aux composants utilisés par l'application web. Si une application web utilise des composants externes (par exemple, un plugin), nous devrions également rechercher des vulnérabilités pour ces composants externes.

---

## Common Vulnerability Scoring System (CVSS)

Le [Common Vulnerability Scoring System (CVSS)](https://en.wikipedia.org/wiki/Common_Vulnerability_Scoring_System) est une norme industrielle open-source pour évaluer la sévérité des vulnérabilités de sécurité. Ce système de notation est souvent utilisé comme une mesure standard pour les organisations et les gouvernements qui ont besoin de produire des scores de sévérité précis et cohérents pour les vulnérabilités de leurs systèmes. Cela aide à la priorisation des ressources et à la réponse à une menace donnée.

Les scores CVSS sont basés sur une formule qui utilise plusieurs métriques : `de base` (`Base`), `temporelles` (`Temporal`), et `environnementales` (`Environmental`). Lors du calcul de la sévérité d'une vulnérabilité à l'aide du CVSS, les métriques `de base` produisent un score allant de 0 à 10, modifié en appliquant les métriques `temporelles` et `environnementales`. La [National Vulnerability Database (NVD)](https://nvd.nist.gov/) fournit des scores CVSS pour presque toutes les vulnérabilités connues et divulguées publiquement. À ce jour, la NVD ne fournit que des scores `de base` basés sur les caractéristiques intrinsèques d'une vulnérabilité donnée. Les systèmes de notation actuellement en place sont CVSS v2 et CVSS v3. Il existe plusieurs différences entre les systèmes v2 et v3, notamment des changements dans les groupes `de base` et `environnementaux` pour prendre en compte des métriques supplémentaires. Plus d'informations sur les différences entre les deux systèmes de notation peuvent être trouvées [ici](https://www.balbix.com/insights/cvss-v2-vs-cvss-v3).

Les échelles d'évaluation des scores CVSS diffèrent légèrement entre la V2 et la V3, comme on peut le voir dans les tableaux suivants :

|Évaluations CVSS V2.0||
|---|---|
|**Sévérité**|**Plage de score de base**|
|Faible|0.0-3.9|
|Moyenne|4.0-6.9|
|Élevée|7.0-10.0|

|**Évaluations CVSS V3.0**||
|---|---|
|**Sévérité**|**Plage de score de base**|
|Aucune|0.0|
|Faible|0.1-3.9|
|Moyenne|4.0-6.9|
|Élevée|7.0-8.9|
|Critique|9.0-10.0|

La NVD ne prend pas en compte les métriques `temporelles` et `environnementales` car les premières peuvent changer au fil du temps en raison d'événements externes. Les dernières constituent une métrique personnalisée basée sur l'impact potentiel de la vulnérabilité sur une organisation donnée. La NVD fournit un [calculateur CVSS v2](https://nvd.nist.gov/vuln-metrics/cvss/v2-calculator) et un [calculateur CVSS v3](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator) que les organisations peuvent utiliser pour prendre en compte le risque additionnel provenant des données `temporelles` et `environnementales` qui leur sont propres. Les calculateurs sont très interactifs et peuvent être utilisés pour affiner le score CVSS à notre environnement. Nous pouvons survoler chaque métrique pour en savoir plus à son sujet et déterminer exactement comment elle s'applique à notre organisation. Ci-dessous, un exemple de vue du calculateur CVSS v3 :

![Tableau des métriques de score CVSS montrant les métriques de score de base, temporelles et environnementales avec divers facteurs d'impact et d'exploitabilité.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/cvssv3_calc.png)

Expérimentez avec le calculateur CVSS et voyez comment les différentes métriques peuvent être ajustées pour arriver à un score donné. Examinez quelques CVE et essayez d'obtenir le même score CVSS. Comment le score CVSS change-t-il lorsque vous appliquez les métriques `temporelles` et `environnementales` ? Ce [guide](https://www.first.org/cvss/user-guide) pratique est extrêmement utile pour comprendre la V2 et la V3 et comment utiliser les calculateurs pour arriver à un score donné.

---

## Vulnérabilités du serveur back-end

Tout comme pour les vulnérabilités publiques des applications web, nous devrions également envisager de rechercher des vulnérabilités pour d'autres composants back-end, comme le serveur back-end ou le serveur web.

Les vulnérabilités les plus critiques pour les composants back-end se trouvent dans les serveurs web, car ils sont accessibles publiquement via le protocole `TCP`. Un exemple de vulnérabilité de serveur web bien connue est `Shell-Shock`, qui a affecté les serveurs web Apache publiés en 2014 et avant, et qui utilisait des requêtes `HTTP` pour obtenir le contrôle à distance du serveur back-end.

Quant aux vulnérabilités dans le serveur back-end ou la base de données, elles sont généralement utilisées après avoir obtenu un accès local au serveur back-end ou au réseau back-end, qui peut être obtenu par le biais de vulnérabilités `externes` ou lors de tests d'intrusion internes. Elles sont généralement utilisées pour obtenir un accès à privilèges élevés sur le serveur back-end ou le réseau back-end, ou pour prendre le contrôle d'autres serveurs au sein du même réseau.

Bien que non directement exploitables de l'extérieur, ces vulnérabilités restent critiques et doivent être corrigées pour protéger l'ensemble de l'application web contre toute compromission.
---

← [[15 - Vulnérabilités Web Courantes]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[17 - Prochaines Étapes]] →
