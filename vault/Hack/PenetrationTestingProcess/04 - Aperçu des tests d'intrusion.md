---
tags:
  - pentest-process
ordre: 4
---

# Aperçu des tests d'intrusion

---

L'informatique fait partie intégrante de presque toutes les entreprises. La quantité de données critiques et confidentielles stockées dans les systèmes informatiques ne cesse de croître, tout comme la dépendance au bon fonctionnement ininterrompu des systèmes informatiques utilisés. Par conséquent, les attaques contre les réseaux d'entreprise, la perturbation de la disponibilité des systèmes et d'autres moyens de causer des dommages importants à une entreprise (comme les attaques par rançongiciel ou ransomware) sont de plus en plus courants. Les informations importantes de l'entreprise obtenues par des brèches de sécurité et des cyberattaques peuvent être vendues à des concurrents, divulguées sur des forums publics ou utilisées à d'autres fins malveillantes. Les pannes de système sont délibérément provoquées car il est de plus en plus difficile de les contrer.

Un `test d'intrusion` (`Pentest` ou `Penetration Test`) est une tentative d'attaque organisée, ciblée et autorisée visant à tester une infrastructure informatique et ses défenseurs afin de déterminer leur vulnérabilité aux failles de sécurité informatique. Un pentest utilise les méthodes et techniques employées par de vrais attaquants. En tant que testeurs d'intrusion, nous appliquons diverses techniques et analyses pour évaluer l'impact qu'une vulnérabilité particulière ou une chaîne de vulnérabilités peut avoir sur la confidentialité, l'intégrité et la disponibilité des systèmes et des données informatiques d'une organisation.

- `Un pentest vise à découvrir et à identifier TOUTES les vulnérabilités des systèmes examinés et à améliorer la sécurité des systèmes testés.`

D'autres évaluations, comme une `évaluation Red Team`, peuvent être basées sur des scénarios et se concentrer uniquement sur les vulnérabilités exploitées pour atteindre un objectif final spécifique (par exemple, accéder à la boîte de réception du PDG ou obtenir un drapeau placé sur un serveur critique).

#### Gestion des risques

En général, cela fait également partie de la `gestion des risques` (`risk management`) d'une entreprise. L'objectif principal de la gestion des risques de sécurité informatique est d'identifier, d'évaluer et d'atténuer tous les risques potentiels qui pourraient nuire à la confidentialité, à l'intégrité et à la disponibilité des systèmes d'information et des données d'une organisation, et de réduire le risque global à un niveau acceptable. Cela inclut l'identification des menaces potentielles, l'évaluation de leurs risques et la prise des mesures nécessaires pour les réduire ou les éliminer. Ceci est réalisé en mettant en œuvre les contrôles et les politiques de sécurité appropriés, y compris le contrôle d'accès, le chiffrement et d'autres mesures de sécurité. En prenant le temps de gérer correctement les risques de sécurité des systèmes informatiques d'une organisation, il est possible de garantir que les données restent sûres et sécurisées.

Cependant, nous ne pouvons pas éliminer tous les risques. Il subsiste la nature du risque inhérent d'une brèche de sécurité, qui est présent même lorsque l'organisation a pris toutes les mesures raisonnables pour gérer le risque. Par conséquent, certains risques demeureront. Le risque inhérent est le niveau de risque présent même lorsque les contrôles de sécurité appropriés sont en place. Les entreprises peuvent accepter, transférer, éviter et atténuer les risques de diverses manières. Par exemple, elles peuvent souscrire une assurance pour couvrir certains risques, comme les catastrophes naturelles ou les accidents. En concluant un contrat, elles peuvent également transférer leurs risques à une autre partie, comme un fournisseur de services tiers. De plus, elles peuvent mettre en œuvre des mesures préventives pour réduire la probabilité que certains risques se produisent, et si certains risques se matérialisent, elles peuvent mettre en place des processus pour minimiser leur impact. Enfin, elles peuvent utiliser des instruments financiers, tels que les dérivés, pour réduire les conséquences économiques de risques spécifiques. Toutes ces stratégies peuvent aider les entreprises à gérer efficacement leurs risques.

Lors d'un pentest, nous préparons une documentation détaillée sur les étapes suivies et les résultats obtenus. Cependant, il incombe au client ou à l'opérateur de ses systèmes examinés de corriger les vulnérabilités trouvées. Notre rôle est celui de conseillers de confiance : nous signalons les vulnérabilités, fournissons des étapes de reproduction détaillées et des recommandations de remédiation appropriées, mais nous n'intervenons pas pour appliquer des correctifs ou modifier le code, etc. Il est important de noter qu'un pentest n'est pas une surveillance de l'infrastructure ou des systèmes informatiques, mais un instantané de l'état de la sécurité à un moment donné. Une déclaration à cet effet doit figurer dans notre livrable, le rapport de test d'intrusion.

#### Évaluations de vulnérabilités

L'`analyse de vulnérabilités` (`Vulnerability analysis`) est un terme générique qui peut inclure des évaluations de vulnérabilités ou de sécurité et des tests d'intrusion. Contrairement à un test d'intrusion, les évaluations de vulnérabilités ou de sécurité sont effectuées à l'aide d'outils purement automatisés. Les systèmes sont vérifiés par rapport à des problèmes connus et des vulnérabilités de sécurité en exécutant des outils d'analyse comme [Nessus](https://www.tenable.com/products/nessus), [Qualys](https://www.qualys.com/apps/vulnerability-management/), [OpenVAS](https://www.openvas.org/) et autres. Dans la plupart des cas, ces vérifications automatisées ne peuvent pas adapter les attaques aux configurations du système cible. C'est pourquoi les tests manuels effectués par un testeur humain expérimenté sont essentiels.

D'un autre côté, un pentest est un mélange de tests/validation automatisés et manuels, réalisé après une collecte d'informations approfondie et, dans la plupart des cas, manuelle. Il est adapté et ajusté individuellement au système testé. La planification, l'exécution et la sélection des outils utilisés sont beaucoup plus complexes dans un pentest. Les tests d'intrusion comme les autres évaluations de sécurité ne peuvent être effectués qu'après un accord mutuel entre l'entreprise contractante et l'organisation qui emploie le testeur d'intrusion. En effet, les tests et activités individuels réalisés pendant le pentest pourraient être considérés comme des infractions pénales si le testeur ne dispose pas d'une autorisation écrite explicite pour attaquer les systèmes du client. L'organisation qui commande le test d'intrusion ne peut demander des tests que sur ses propres actifs. Si elle utilise des tiers pour héberger des sites web ou d'autres infrastructures, elle doit dans la plupart des cas obtenir une approbation écrite explicite de ces entités. Des entreprises comme Amazon n'exigent plus d'autorisation préalable pour tester certains services, conformément à cette [politique](https://aws.amazon.com/security/penetration-testing/), si une entreprise utilise AWS pour héberger tout ou partie de son infrastructure. Cela varie d'un fournisseur à l'autre, il est donc toujours préférable de confirmer la propriété des actifs avec le client pendant la phase de cadrage et de vérifier si les tiers qu'ils utilisent exigent un processus de demande écrite avant tout test.

Un pentest réussi nécessite une organisation et une préparation considérables. Il doit y avoir un modèle de processus simple que nous pouvons suivre tout en l'adaptant aux besoins de nos clients, car chaque environnement que nous rencontrons sera différent et aura ses propres nuances. Dans certains cas, nous pouvons travailler avec des clients qui n'ont jamais fait l'expérience d'un pentest auparavant, et nous devons être capables d'expliquer ce processus en détail pour nous assurer qu'ils comprennent clairement nos activités prévues et les aider à cadrer l'évaluation avec précision.

En principe, les employés ne sont pas informés des tests d'intrusion à venir. Cependant, les responsables peuvent décider d'informer leurs employés des tests. En effet, les employés ont le droit de savoir quand ils n'ont aucune attente en matière de vie privée.

En tant que testeurs d'intrusion, nous pouvons trouver des données personnelles, telles que des noms, des adresses, des salaires et bien plus encore. La meilleure chose que nous puissions faire pour respecter la [Loi sur la protection des données](https://www.gov.uk/data-protection) est de garder ces informations privées. Un autre exemple serait que nous obtenions l'accès à une base de données contenant des numéros de carte de crédit, des noms et des codes CVV. En conséquence, nous recommandons à nos clients d'améliorer et de changer les mots de passe dès que possible et de chiffrer les données de la base de données.

---

## Méthodes de test

Une partie essentielle du processus est le point de départ à partir duquel nous devons effectuer notre pentest. Chaque pentest peut être réalisé selon deux perspectives différentes :

- `Externe` ou `Interne`

#### Test d'intrusion externe

De nombreux pentests sont effectués d'une perspective externe ou en tant qu'utilisateur anonyme sur Internet. La plupart des clients veulent s'assurer qu'ils sont aussi protégés que possible contre les attaques sur leur périmètre réseau externe. Nous pouvons effectuer les tests depuis notre propre machine (en utilisant de préférence une connexion VPN pour éviter que notre FAI ne nous bloque) ou depuis un VPS. Certains clients ne se soucient pas de la furtivité, tandis que d'autres nous demandent de procéder aussi discrètement que possible, en approchant les systèmes cibles de manière à éviter les blocages de pare-feu, la détection IDS/IPS et le déclenchement d'alarmes. Ils peuvent demander une approche furtive ou "hybride" où nous devenons progressivement plus "bruyants" pour tester leurs capacités de détection. En fin de compte, notre objectif ici est d'accéder aux machines exposées sur l'extérieur, d'obtenir des données sensibles ou d'accéder au réseau interne.

#### Test d'intrusion interne

Contrairement à un pentest externe, un pentest interne est réalisé depuis l'intérieur du réseau d'entreprise. Cette étape peut être exécutée après avoir réussi à pénétrer le réseau de l'entreprise via le pentest externe ou en partant d'un scénario de compromission supposée. Les pentests internes peuvent également accéder à des systèmes isolés sans aucun accès à Internet, ce qui nécessite généralement notre présence physique dans les locaux du client.

---

## Types de tests d'intrusion

Peu importe comment nous commençons le pentest, le type de pentest joue un rôle important. Ce type détermine la quantité d'informations qui nous est fournie. Nous pouvons regrouper ces types comme suit :

|**Type**|**Informations fournies**|
|---|---|
|`Blackbox`|`Minimales`. Seules les informations essentielles, telles que les adresses IP et les domaines, sont fournies.|
|`Greybox`|`Étendues`. Dans ce cas, des informations supplémentaires nous sont fournies, telles que des URL spécifiques, des noms d'hôte, des sous-réseaux, etc.|
|`Whitebox`|`Maximales`. Ici, tout nous est divulgué. Cela nous donne une vue interne de toute la structure, ce qui nous permet de préparer une attaque en utilisant des informations internes. On peut nous fournir des configurations détaillées, des identifiants d'administrateur, le code source d'applications web, etc.|
|`Red-Teaming`|Peut inclure des tests physiques et de l'ingénierie sociale, entre autres. Peut être combiné avec n'importe lequel des types ci-dessus.|
|`Purple-Teaming`|Peut être combiné avec n'importe lequel des types ci-dessus. Cependant, il se concentre sur une collaboration étroite avec les défenseurs.|

Moins nous recevons d'informations, plus l'approche sera longue et complexe. Par exemple, pour un test d'intrusion de type blackbox, nous devons d'abord obtenir un aperçu des serveurs, des hôtes et des services présents dans l'infrastructure, surtout si des réseaux entiers sont testés. Ce type de reconnaissance peut prendre un temps considérable, en particulier si le client a demandé une approche de test plus furtive.

---

## Types d'environnements de test

Outre la méthode et le type de test, une autre considération est ce qui doit être testé, ce qui peut être résumé dans les catégories suivantes :

||||||
|---|---|---|---|---|
|Réseau|App Web|Mobile|API|Clients lourds|
|IoT|Cloud|Code source|Sécurité physique|Employés|
|Hôtes|Serveur|Politiques de sécurité|Pare-feux|IDS/IPS|

Il est important de noter que ces catégories peuvent souvent être mélangées. Tous les composants de test listés peuvent être inclus en fonction du type de test à effectuer. Nous allons maintenant changer de sujet et aborder en profondeur le processus d'intrusion pour voir comment chaque phase est décomposée et dépend de la précédente.
---

← [[03 - Exercices et questions de l'Academy]] | [[00 - Sommaire Penetration Testing Process|Sommaire]] | [[05 - Lois et réglementations]] →
