---
tags:
  - pentest-process
ordre: 1
---

# Introduction au parcours de Testeur d'Intrusion

---

Ce module est une introduction au [parcours de carrière](https://academy.hackthebox.com/paths/jobrole) de Testeur d'Intrusion (Penetration Tester) et une introduction générale aux tests d'intrusion (Penetration Tests) ainsi qu'à chacune des phases que nous couvrons en profondeur tout au long des modules. Nous vous recommandons de commencer le parcours par ce module et de vous y référer périodiquement à mesure que vous terminez d'autres modules pour voir comment chaque sujet s'intègre dans la vue d'ensemble du processus de test d'intrusion. Ce module est également un excellent point de départ pour toute personne nouvelle sur HTB Academy ou dans le secteur.

Ce parcours est destiné aux aspirants testeurs d'intrusion de tous horizons et aux pentesters expérimentés cherchant à améliorer leurs compétences dans un domaine particulier, à devenir plus polyvalents ou à apprendre les choses sous un angle différent. Ce parcours couvre les concepts fondamentaux nécessaires pour réussir les tests d'intrusion externes, les tests d'intrusion internes (à la fois réseau et Active Directory) et les évaluations de la sécurité des applications web (Web Application Security Assessments). À travers chaque module, nous plongeons en profondeur dans les techniques spécialisées, les méthodologies et les outils nécessaires pour réussir dans un rôle de testeur d'intrusion. Le parcours emmène les étudiants dans un voyage très pratique à travers toutes les étapes d'un test d'intrusion, de la reconnaissance et de l'énumération à la documentation et à la rédaction de rapports, pour aboutir à un module de synthèse simulant un test d'intrusion complet. Les étudiants qui terminent ce parcours dans son intégralité seront armés des compétences pratiques et de l'état d'esprit nécessaires pour effectuer des évaluations de sécurité professionnelles sur des réseaux réels à un niveau de base à intermédiaire. Chacun de nos modules explore en profondeur le "pourquoi" derrière les problèmes et les tactiques que nous présentons et n'est pas seulement un tutoriel sur l'utilisation d'outils "point-and-click". Nous intégrons des récits et des scénarios issus de notre expérience réelle dans la réalisation d'évaluations de sécurité pour des clients de tous les secteurs, ainsi que pour des gouvernements locaux et fédéraux.

---

## Philosophie d'apprentissage de HTB Academy

Notre objectif est d'apprendre aux étudiants à voir les deux facettes d'un problème et à être capables de trouver des failles que d'autres pourraient manquer. Nous encourageons chaque étudiant à formuler sa propre méthodologie reproductible et approfondie qui peut être appliquée à tout type d'évaluation, peu importe la taille de l'environnement ou le secteur d'activité du client. Apprendre de cette manière et travailler sur des centaines d'exemples pratiques, chaque module se terminant par une ou plusieurs évaluations de compétences, renforce ces concepts et développe une "mémoire musculaire" autour des actions que nous effectuons lors de chaque évaluation. Si nous maîtrisons bien les bases, nous avons plus de temps pour approfondir et apporter une valeur ajoutée à nos clients. Pour chaque vulnérabilité et mauvaise configuration que nous démontrons, nous discutons de la faille sous-jacente, ce qui nous aide à mieux comprendre comment les choses fonctionnent, pourquoi un outil particulier peut échouer, et à fournir des conseils de remédiation plus précis à nos clients, qui peuvent être adaptés de manière unique à leur environnement et à leur appétit pour le risque.

Notre philosophie d'apprentissage peut se résumer comme suit :

Notre philosophie est "d'apprendre par la pratique", en suivant une approche basée sur les risques avec un fort accent sur l'apprentissage pratique et l'utilisation légale et éthique de nos compétences. Nous nous efforçons d'enseigner à nos étudiants le "pourquoi" derrière une vulnérabilité et comment découvrir, exploiter, corriger, détecter et prévenir la faille afin de former des professionnels polyvalents capables de transmettre ces connaissances et cet état d'esprit complets à leurs clients ou employeurs actuels/futurs pour les aider à sécuriser leurs personnes, leurs technologies et leurs missions contre les menaces cybernétiques modernes.

---

## Considérations éthiques et légales

Une partie essentielle de la philosophie ci-dessus réside dans les termes `légal` et `éthique`. Le test d'intrusion est l'une des rares professions où vous êtes, pour un temps (pendant la période de test autorisée), autorisé à effectuer des actions contre une entreprise qui seraient illégales dans d'autres circonstances. Tout au long des modules, dans ce parcours et d'autres, nous fournissons des cibles individuelles et des mini-réseaux (laboratoires) pour pratiquer en toute sécurité et légalité les techniques que nous démontrons. La plateforme principale de HTB contient des centaines de machines et plusieurs grands réseaux de laboratoire réalistes pour pratiquer ces compétences. Avec la montée de la gamification dans notre secteur et l'accès à du matériel de formation plus pratique et réaliste, nous devons nous rappeler qu'il existe une ligne entre les actions légales et illégales qui peut être facilement franchie si nous essayons de pratiquer nos compétences en dehors de ces environnements contrôlés. Mettre en œuvre des compétences de collecte d'informations et d'OSINT passif sur une cible pour travailler ces compétences est acceptable, à condition que nous n'utilisions que des bases de données publiques et des moteurs de recherche, mais sans sonder l'infrastructure externe d'une entreprise. Cependant, effectuer `TOUT` scan ou activité qui interagit avec `N'IMPORTE LEQUEL` des systèmes d'une organisation sans consentement écrit explicite sous la forme d'un périmètre des travaux (Scope of Work) (incluant un périmètre de test détaillé, un contrat et des règles d'engagement) signé par les deux parties est illégal et pourrait entraîner des poursuites judiciaires et même pénales à notre encontre.

Si vous êtes prêt à vous exercer sur des cibles réelles, vous pouvez obtenir une pratique supplémentaire en participant à des programmes de bug bounty hébergés par des organisations telles que [HackerOne](https://hackerone.com/directory/programs) et [Bugcrowd](https://bugcrowd.com/programs). Grâce à ces organisations de bug bounty, vous pouvez participer à des activités de test d'applications web sur de nombreuses entreprises différentes qui proposent un programme de bug bounty. Gardez à l'esprit que chacun de ces programmes a son propre périmètre et ses propres règles d'engagement, alors familiarisez-vous avec eux avant de commencer toute activité de test. La plupart de ces programmes n'autorisent pas les scans automatisés, ce qui en fait un excellent moyen de pratiquer vos compétences en collecte d'informations et en test manuel d'applications web.

Une fois que vous décrochez votre premier emploi de testeur d'intrusion, faites preuve de diligence raisonnable (due diligence) pour vous assurer que l'entreprise est une organisation légitime qui n'effectue des évaluations qu'après une coordination explicite (et la signature de documents contractuels) entre l'entreprise cible et le client. Bien que rares, certaines organisations criminelles peuvent se faire passer pour des entreprises légitimes afin de recruter des talents pour les aider dans des actions illégales. Si vous participez, même si vos intentions sont bonnes, vous pouvez toujours être tenu responsable et avoir des ennuis judiciaires, voire pénaux. Lorsque vous travaillez pour une entreprise, assurez-vous d'avoir une copie du périmètre des travaux/contrat signé et un document formel listant le périmètre des tests (URL, adresses IP individuelles, plages de réseau CIDR, SSID sans fil, installations pour une évaluation physique, ou listes d'e-mails ou de numéros de téléphone pour des missions d'ingénierie sociale), également signé par le client. En cas de doute, demandez des approbations et une documentation supplémentaires avant de commencer tout test. Pendant les tests, `restez dans le périmètre des tests`. Ne vous écartez pas du périmètre si vous remarquez d'autres adresses IP ou sous-domaines qui semblent plus intéressants. Encore une fois, `en cas de doute, demandez`. Peut-être que le client a oublié d'ajouter certains hôtes à la feuille de périmètre. Il n'y a pas de mal à demander si d'autres hôtes que vous remarquez devraient être inclus, mais, encore une fois, assurez-vous que cela soit `par écrit` et pas seulement donné lors d'un appel téléphonique.

Nos clients nous accordent une grande confiance en nous laissant entrer dans leur réseau et exécuter des outils qui pourraient potentiellement causer des ravages sur leur réseau et provoquer des perturbations pouvant entraîner des temps d'arrêt et une perte de revenus. Nous devons travailler avec le principe directeur de `ne pas nuire` et nous efforcer de mener toutes les activités de test de manière prudente et mesurée. Ce n'est pas parce que nous pouvons exécuter un certain outil que nous devrions le faire. Un PoC d'exploit particulier pourrait-il potentiellement faire planter un ou plusieurs serveurs ? En cas de doute sur quoi que ce soit pendant une évaluation, parlez-en à votre responsable et au client et obtenez un consentement explicite `par écrit` avant de continuer.

Pour résumer, nous sommes hautement qualifiés et une grande confiance nous est accordée. N'abusez pas de cette confiance, `travaillez toujours de manière éthique et dans les limites de la loi`, et vous aurez une carrière longue et fructueuse et nouerez d'excellentes relations professionnelles et personnelles en cours de route. Efforcez-vous toujours de choisir la voie de l'honnêteté et de faire ce qui est juste. `Documentez, documentez, documentez`. En cas de doute, documentez et communiquez excessivement. Assurez-vous que tous les aspects "ennuyeux" de la conformité sont réglés en premier afin que vous puissiez avoir l'esprit tranquille et profiter de la réalisation d'excellentes évaluations complètes pour vos clients en tant que leur conseiller de confiance.

---

## Programme du parcours de Testeur d'Intrusion

Le parcours simule un test d'intrusion contre l'entreprise Inlanefreight, décomposé en différentes étapes, couvrant les concepts et outils fondamentaux qui nous permettront de nous démarquer en tant que testeurs d'intrusion. Le parcours se termine par un module approfondi sur les compétences non techniques ("soft skills") essentielles telles que la prise de notes, l'organisation, la documentation, la rédaction de rapports et la communication avec le client, suivi d'un test d'intrusion simulé complet pour mettre en pratique toutes nos compétences dans un grand réseau d'entreprise simulé. Les modules qui composent le parcours sont présentés comme suit :

|**`Introduction`**|
|---|
|1. [Processus de test d'intrusion](https://academy.hackthebox.com/module/details/90)|
|2. [Pour commencer](https://academy.hackthebox.com/module/details/77)|

|**`Reconnaissance, Énumération & Planification d'attaque`**|
|---|
|3. [Énumération réseau avec Nmap](https://academy.hackthebox.com/module/details/19)|
|4. [Prise d'empreinte (Footprinting)](https://academy.hackthebox.com/module/details/112)|
|5. [Collecte d'informations - Édition Web](https://academy.hackthebox.com/module/details/144)|
|6. [Évaluation des vulnérabilités](https://academy.hackthebox.com/module/details/108)|
|7. [Transferts de fichiers](https://academy.hackthebox.com/module/details/24)|
|8. [Shells & Payloads](https://academy.hackthebox.com/module/details/115)|
|9. [Utilisation du Metasploit Framework](https://academy.hackthebox.com/module/details/39)|

|**`Exploitation & Mouvement latéral`**|
|---|
|10. [Attaques par mot de passe](https://academy.hackthebox.com/module/details/147)|
|11. [Attaquer les services courants](https://academy.hackthebox.com/module/details/116)|
|12. [Pivoting, Tunneling et Redirection de port](https://academy.hackthebox.com/module/details/158)|
|13. [Énumération & Attaques Active Directory](https://academy.hackthebox.com/module/details/143)|

|**`Exploitation Web`**|
|---|
|14. [Utilisation des Proxies Web](https://academy.hackthebox.com/module/details/110)|
|15. [Attaquer les applications Web avec Ffuf](https://academy.hackthebox.com/module/details/54)|
|16. [Brute Forcing de connexion](https://academy.hackthebox.com/module/details/57)|
|17. [Fondamentaux de l'injection SQL](https://academy.hackthebox.com/module/details/33)|
|18. [Essentiels de SQLMap](https://academy.hackthebox.com/module/details/58)|
|19. [Cross-Site Scripting (XSS)](https://academy.hackthebox.com/module/details/103)|
|20. [Inclusion de fichiers](https://academy.hackthebox.com/module/details/23)|
|21. [Attaques par téléversement de fichiers](https://academy.hackthebox.com/module/details/136)|
|22. [Injections de commandes](https://academy.hackthebox.com/module/details/109)|
|23. [Attaques Web](https://academy.hackthebox.com/module/details/134)|
|24. [Attaquer les applications courantes](https://academy.hackthebox.com/module/details/113)|

|**`Post-Exploitation`**|
|---|
|25. [Élévation de privilèges Linux](https://academy.hackthebox.com/module/details/51)|
|26. [Élévation de privilèges Windows](https://academy.hackthebox.com/module/details/67)|

|**`Rédaction de rapports & Synthèse`**|
|---|
|27. [Documentation & Rédaction de rapports](https://academy.hackthebox.com/module/details/162)|
|28. [Attaquer les réseaux d'entreprise](https://academy.hackthebox.com/module/details/163)|

Après avoir terminé ce parcours, nous recommandons aux étudiants de viser une spécialisation, que ce soit Active Directory, le Web ou le Reverse Engineering. Nous devrions continuer à développer lentement nos compétences dans tous les domaines pour devenir aussi polyvalents que possible, tout en visant un niveau de connaissance expert dans au moins une discipline. Pour ceux qui ne se sentiraient pas encore assez confiants pour entreprendre ce parcours de carrière, nous recommandons de suivre tous les modules du [parcours de compétences](https://academy.hackthebox.com/paths) `Information Security Foundations`, qui aidera à construire les connaissances prérequises nécessaires pour réussir dans le parcours de Testeur d'Intrusion. Il est préférable de suivre les modules du parcours de Testeur d'Intrusion dans l'ordre, car les concepts s'appuient les uns sur les autres. Tout au long du parcours, nous réitérons continuellement les concepts et présentons les choses de différentes manières pour donner aux étudiants plus de pratique et de scénarios afin d'approfondir leurs connaissances dans un domaine particulier. Par exemple, le mouvement latéral et le pillage (pillaging) sont des compétences vitales pour réussir en tant que testeur d'intrusion. Nous n'avons pas de modules séparés pour chacune de ces phases car le pillage et le mouvement latéral peuvent être considérés comme des processus itératifs que nous revisiterons de nombreuses fois au cours d'une évaluation. Au lieu de cela, nous introduisons des tactiques, des techniques et des procédures pour se déplacer latéralement et montrons une grande variété de scénarios où nous pouvons bénéficier de solides compétences en pillage/post-exploitation.

La section suivante détaille 36 modules différents de HTB Academy et comment ils s'intègrent dans chaque phase du processus de test d'intrusion.
---

[[00 - Sommaire Penetration Testing Process|Sommaire]] | [[02 - Disposition des modules de l'Academy]] →
