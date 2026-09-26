---
tags:
  - pentest-process
ordre: 7
---

# Pré-engagement

---

Le pré-engagement est la phase de préparation au test d'intrusion proprement dit. Au cours de cette étape, de nombreuses questions sont posées et certains accords contractuels sont conclus. Le client nous informe de ce qu'il souhaite faire tester, et nous lui expliquons en détail comment rendre le test aussi efficace que possible.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-PRE.png)

L'ensemble du processus de pré-engagement se compose de trois éléments essentiels :

1. Questionnaire de cadrage
2. Réunion de pré-engagement
3. Réunion de lancement

Avant de pouvoir discuter de l'un de ces points en détail, un `Accord de non-divulgation` (`NDA`, pour Non-Disclosure Agreement) doit être signé par toutes les parties. Il existe plusieurs types de NDA :

|**Type**|**Description**|
|---|---|
|`NDA unilatéral`|Ce type de NDA n'oblige qu'une seule partie à maintenir la confidentialité et autorise l'autre partie à partager les informations reçues avec des tiers.|
|`NDA bilatéral`|Dans ce cas, les deux parties sont tenues de garder confidentielles les informations résultantes et acquises. C'est le type de NDA le plus courant qui protège le travail des testeurs d'intrusion.|
|`NDA multilatéral`|Un NDA multilatéral est un engagement de confidentialité pris par plus de deux parties. Si nous effectuons un test d'intrusion pour un réseau coopératif, toutes les parties responsables et impliquées doivent signer ce document.|

Des exceptions peuvent également être faites dans les cas urgents, où nous passons directement à la réunion de lancement, qui peut également se dérouler par le biais d'une conférence en ligne. Il est essentiel de savoir `qui, au sein de l'entreprise, est autorisé` à nous mandater pour un test d'intrusion. En effet, nous ne pouvons pas accepter une telle commande de n'importe qui. Imaginez, par exemple, qu'un employé d'une entreprise nous engage sous prétexte de vérifier la sécurité du réseau de l'entreprise. Cependant, une fois l'évaluation terminée, il s'avère que cet employé voulait nuire à sa propre entreprise et n'avait aucune autorisation pour la faire tester. Cela nous mettrait dans une situation critique d'un point de vue juridique.

Vous trouverez ci-dessous une liste d'exemples (non exhaustive) de membres de l'entreprise qui peuvent être autorisés à nous engager pour des tests d'intrusion. Cela peut varier d'une entreprise à l'autre, les grandes organisations n'impliquant pas directement le personnel de direction (C-level) et la responsabilité incombant à la direction des services informatiques, de l'audit ou de la sécurité informatique, ou à des postes similaires.

||||
|---|---|---|
|Président-Directeur Général (PDG)|Directeur Technique (CTO)|Responsable de la Sécurité des Systèmes d'Information (RSSI)|
|Directeur de la Sécurité (CSO)|Directeur des Risques (CRO)|Directeur des Systèmes d'Information (DSI)|
|VP de l'audit interne|Responsable de l'audit|VP ou Directeur de l'informatique/de la sécurité de l'information|

Il est essentiel de déterminer au début du processus qui a le pouvoir de signer le contrat, les documents des règles d'engagement, et qui seront les points de contact principaux et secondaires, le support technique et le contact pour remonter tout problème.

Cette étape nécessite également la préparation de plusieurs documents avant qu'un test d'intrusion puisse être mené. Ces documents doivent être signés par notre client et par nous-mêmes afin que la déclaration de consentement puisse également être présentée sous forme écrite si nécessaire. Autrement, le test d'intrusion pourrait enfreindre le [Computer Misuse Act](https://www.legislation.gov.uk/ukpga/1990/18/contents). Ces documents comprennent, sans s'y limiter :

|**Document**|**Moment de la création**|
|---|---|
|`1. Accord de non-divulgation` (`NDA`)|`Après` le contact initial|
|`2. Questionnaire de cadrage`|`Avant` la réunion de pré-engagement|
|`3. Document de cadrage`|`Pendant` la réunion de pré-engagement|
|`4. Proposition de test d'intrusion` (`Contrat/Cahier des charges` (`SoW`))|`Pendant` la réunion de pré-engagement|
|`5. Règles d'engagement` (`RoE`)|`Avant` la réunion de lancement|
|`6. Contrat de prestation` (Évaluations physiques)|`Avant` la réunion de lancement|
|`7. Rapports`|`Pendant` et `après` le test d'intrusion|

Note : Notre client peut fournir un document de cadrage distinct répertoriant les adresses/plages IP/URL concernées et les informations d'identification nécessaires, mais ces informations doivent également être documentées en annexe du document des RoE.

**Note importante :**

Ces documents doivent être examinés et adaptés par un avocat après leur préparation.

---

## Questionnaire de cadrage

Après un premier contact avec le client, nous lui envoyons généralement un `Questionnaire de cadrage` afin de mieux comprendre les services qu'il recherche. Ce questionnaire de cadrage doit expliquer clairement nos services et peut généralement lui demander de choisir un ou plusieurs éléments de la liste suivante :

|||
|---|---|
|☐ Évaluation interne des vulnérabilités|☐ Évaluation externe des vulnérabilités|
|☐ Test d'intrusion interne|☐ Test d'intrusion externe|
|☐ Évaluation de la sécurité sans fil|☐ Évaluation de la sécurité des applications|
|☐ Évaluation de la sécurité physique|☐ Évaluation d'ingénierie sociale|
|☐ Évaluation Red Team|☐ Évaluation de la sécurité des applications web|

Sous chacun de ces points, le questionnaire doit permettre au client d'être plus précis sur l'évaluation requise. A-t-il besoin d'une évaluation d'application web ou mobile ? D'une revue de code sécurisé ? Le test d'intrusion interne doit-il être en boîte noire et semi-évasif ? Souhaite-t-il simplement une évaluation de phishing dans le cadre de l'évaluation d'ingénierie sociale ou également des appels de vishing ? C'est l'occasion pour nous d'expliquer l'étendue et la portée de nos services, de nous assurer que nous comprenons les besoins et les attentes de notre client, et de garantir que nous pouvons réaliser de manière adéquate l'évaluation qu'il demande.

Outre le type d'évaluation, le nom du client, son adresse et les coordonnées du personnel clé, d'autres informations essentielles sont à recueillir :

|||
|---|---|
|Combien d'hôtes actifs sont attendus ?||
|Combien d'adresses IP/plages CIDR sont dans le périmètre ?||
|Combien de domaines/sous-domaines sont dans le périmètre ?||
|Combien de SSID sans fil sont dans le périmètre ?||
|Combien d'applications web/mobiles ? Si le test est authentifié, combien de rôles (utilisateur standard, admin, etc.) ?||
|Pour une évaluation de phishing, combien d'utilisateurs seront ciblés ? Le client fournira-t-il une liste, ou devrons-nous la collecter via OSINT ?||
|Si le client demande une évaluation physique, combien de sites ? Si plusieurs sites sont dans le périmètre, sont-ils géographiquement dispersés ?||
|Quel est l'objectif de l'évaluation Red Team ? Certaines activités (comme le phishing ou les attaques de sécurité physique) sont-elles hors périmètre ?||
|Une évaluation de la sécurité d'Active Directory distincte est-elle souhaitée ?||
|Les tests réseau seront-ils effectués à partir d'un utilisateur anonyme sur le réseau ou d'un utilisateur de domaine standard ?||
|Devons-nous contourner le contrôle d'accès réseau (NAC) ?||

Enfin, nous voudrons poser des questions sur la divulgation d'informations et l'évasivité (si applicable au type d'évaluation) :

- Le test d'intrusion est-il en boîte noire (aucune information fournie), en boîte grise (seules les adresses IP/plages CIDR/URL sont fournies), ou en boîte blanche (informations détaillées fournies)
- Souhaitent-ils que nous testions de manière non évasive, hybride-évasive (commencer discrètement et devenir progressivement plus « bruyant » pour évaluer à quel niveau le personnel de sécurité du client détecte nos activités), ou entièrement évasive.

Ces informations nous aideront à nous assurer que nous affectons les bonnes ressources et que nous réalisons la mission en fonction des attentes du client. Ces informations sont également nécessaires pour fournir une proposition précise avec un calendrier de projet (par exemple, une évaluation des vulnérabilités prendra beaucoup moins de temps qu'une évaluation Red Team) et un coût (un test d'intrusion externe sur 10 adresses IP coûtera beaucoup moins cher qu'un test d'intrusion interne avec 30 réseaux /24 dans le périmètre).

Sur la base des informations que nous avons reçues du questionnaire de cadrage, nous créons un aperçu et résumons toutes les informations dans le `Document de cadrage`.

---

## Réunion de pré-engagement

Une fois que nous avons une idée initiale des exigences du projet du client, nous pouvons passer à la `réunion de pré-engagement`. Cette réunion permet de discuter de tous les éléments pertinents et essentiels avec le client avant le test d'intrusion, en les lui expliquant. Les informations que nous recueillons durant cette phase, ainsi que les données collectées à partir du questionnaire de cadrage, serviront de base à la `Proposition de test d'intrusion`, également connue sous le nom de `Contrat` ou de `Cahier des charges` (`SoW`). On peut considérer l'ensemble du processus comme une visite chez le médecin pour s'informer des examens prévus. Cette phase se déroule généralement par e-mail et lors d'une conférence téléphonique en ligne ou d'une réunion en personne.

Note : Nous pourrons rencontrer au cours de notre carrière des clients qui subissent leur tout premier test d'intrusion, ou dont le point de contact direct n'est pas familier avec le processus. Il n'est pas rare d'utiliser une partie de la réunion de pré-engagement pour revoir le questionnaire de cadrage, en partie ou étape par étape.

#### Contrat - Liste de contrôle

|**Point de contrôle**|**Description**|
|---|---|
|`☐ NDA`|L'accord de non-divulgation (NDA) fait référence à un contrat de confidentialité entre le client et le prestataire concernant toutes les informations écrites ou verbales relatives à une commande/un projet. Le prestataire s'engage à traiter comme strictement confidentielles toutes les informations confidentielles portées à sa connaissance, même après l'achèvement de la commande/du projet. En outre, toutes les exceptions à la confidentialité, la transférabilité des droits et des obligations, ainsi que les pénalités contractuelles, doivent être stipulées dans l'accord. Le NDA doit être signé avant la réunion de lancement ou au plus tard pendant la réunion avant que toute information ne soit discutée en détail.|
|`☐ Objectifs`|Les objectifs sont des jalons qui doivent être atteints au cours de la commande/du projet. Dans ce processus, la définition des objectifs commence par les objectifs principaux et se poursuit avec des objectifs plus fins et plus petits.|
|`☐ Périmètre`|Les différents composants à tester sont discutés et définis. Il peut s'agir de domaines, de plages d'adresses IP, d'hôtes individuels, de comptes spécifiques, de systèmes de sécurité, etc. Nos clients peuvent s'attendre à ce que nous découvrions nous-mêmes l'un ou l'autre point. Cependant, la base juridique pour tester les différents composants a ici la plus haute priorité.|
|`☐ Type de test d'intrusion`|Lors du choix du type de test d'intrusion, nous présentons les différentes options et expliquons les avantages et les inconvénients. Comme nous connaissons déjà les objectifs et le périmètre de nos clients, nous pouvons et devons également faire une recommandation sur ce que nous conseillons et justifier notre recommandation en conséquence. Le type qui sera finalement utilisé est la décision du client.|
|`☐ Méthodologies`|Exemples : OSSTMM, OWASP, analyse non authentifiée automatisée et manuelle des composants du réseau interne et externe, évaluations de vulnérabilités des composants réseau et des applications web, vectorisation des menaces de vulnérabilité, vérification et exploitation, et développement d'exploits pour faciliter les techniques d'évasion.|
|`☐ Lieux des tests d'intrusion`|Externe : à distance (via VPN sécurisé) et/ou Interne : en interne ou à distance (via VPN sécurisé)|
|`☐ Estimation du temps`|Pour l'estimation du temps, nous avons besoin des dates de début et de fin du test d'intrusion. Cela fournit une fenêtre de temps précise pour effectuer le test et nous aide à planifier notre procédure. Il est également essentiel de déterminer explicitement la durée des fenêtres de temps pour chaque phase de l'attaque, telles que l'exploitation, la post-exploitation et le mouvement latéral. Celles-ci peuvent être effectuées pendant ou en dehors des heures de travail habituelles. Lors des tests en dehors des heures de travail habituelles, l'accent est davantage mis sur les solutions et systèmes de sécurité qui doivent résister à nos attaques.|
|`☐ Tiers`|Pour les tiers, il faut déterminer par quels fournisseurs tiers notre client obtient des services. Il peut s'agir de fournisseurs de cloud, de FAI et d'autres fournisseurs d'hébergement. Notre client doit obtenir le consentement écrit de ces fournisseurs, décrivant qu'ils acceptent et sont conscients que certaines parties de leur service seront soumises à une attaque de piratage simulée. Il est également fortement conseillé d'exiger du prestataire qu'il nous transmette l'autorisation du tiers afin que nous ayons une confirmation réelle que cette autorisation a bien été obtenue.|
|`☐ Tests évasifs`|Les tests évasifs consistent à tester l'évasion et le contournement du trafic de sécurité et des systèmes de sécurité dans l'infrastructure du client. Nous recherchons des techniques qui nous permettent de trouver des informations sur les composants internes et de les attaquer. Cela dépend si notre client souhaite que nous utilisions de telles techniques ou non.|
|`☐ Risques`|Nous devons également informer notre client des risques liés aux tests et des conséquences possibles. En fonction des risques et de leur gravité potentielle, nous pouvons alors fixer ensemble les limites et prendre certaines précautions.|
|`☐ Limitations et restrictions du périmètre`|Il est également essentiel de déterminer quels serveurs, postes de travail ou autres composants réseau sont essentiels au bon fonctionnement du client et de ses clients. Nous devrons les éviter et ne pas les influencer davantage, car cela pourrait entraîner des erreurs techniques critiques qui pourraient également affecter les clients de notre client en production.|
|`☐ Traitement des informations`|HIPAA, PCI, HITRUST, FISMA/NIST, etc.|
|`☐ Coordonnées`|Pour les coordonnées, nous devons créer une liste avec le nom, le titre, le poste, l'adresse e-mail, le numéro de téléphone, le numéro de téléphone professionnel et un ordre de priorité pour l'escalade de chaque personne.|
|`☐ Canaux de communication`|Il convient également de documenter les canaux de communication utilisés pour échanger des informations entre le client et nous. Il peut s'agir de correspondance par e-mail, d'appels téléphoniques ou de réunions en personne.|
|`☐ Rapports`|Outre la structure du rapport, toutes les exigences spécifiques du client que le rapport doit contenir sont également discutées. De plus, nous clarifions comment les rapports doivent être effectués et si une présentation des résultats est souhaitée.|
|`☐ Conditions de paiement`|Enfin, les prix et les conditions de paiement sont expliqués.|

L'élément le plus crucial de cette réunion est la présentation détaillée du test d'intrusion à notre client et de son orientation. Comme nous le savons déjà, chaque infrastructure est unique pour la plupart, et chaque client a des préférences particulières auxquelles il accorde le plus d'importance. Découvrir ces priorités est une partie essentielle de cette réunion.

On peut comparer cela à une commande au restaurant. Si nous voulons un steak saignant et que le chef nous donne un steak bien cuit parce qu'il pense que c'est meilleur, ce ne sera pas ce que nous espérions. Par conséquent, nous devons donner la priorité aux souhaits de notre client et servir le steak comme il l'a commandé.

Sur la base de la `Liste de contrôle du contrat` et des informations partagées lors du cadrage, la `Proposition de test d'intrusion` (`Contrat`) et les `Règles d'engagement` (`RoE`) associées sont créées.

#### Règles d'engagement - Liste de contrôle

|**Point de contrôle**|**Contenu**|
|---|---|
|`☐ Introduction`|Description de ce document.|
|`☐ Prestataire`|Nom de l'entreprise, nom complet du prestataire, poste.|
|`☐ Testeurs d'intrusion`|Nom de l'entreprise, nom complet des testeurs.|
|`☐ Coordonnées`|Adresses postales, adresses e-mail et numéros de téléphone de toutes les parties côté client et des testeurs d'intrusion.|
|`☐ Finalité`|Description de la finalité du test d'intrusion mené.|
|`☐ Objectifs`|Description des objectifs qui doivent être atteints avec le test d'intrusion.|
|`☐ Périmètre`|Toutes les adresses IP, noms de domaine, URL ou plages CIDR.|
|`☐ Canaux de communication`|Conférences en ligne, appels téléphoniques, réunions en personne ou par e-mail.|
|`☐ Estimation du temps`|Dates de début et de fin.|
|`☐ Heures de la journée pour les tests`|Heures de la journée pour les tests.|
|`☐ Type de test d'intrusion`|Test d'intrusion externe/interne/Évaluations de vulnérabilités/Ingénierie sociale.|
|`☐ Lieux des tests d'intrusion`|Description de la manière dont la connexion au réseau du client est établie.|
|`☐ Méthodologies`|OSSTMM, PTES, OWASP et autres.|
|`☐ Objectifs / Drapeaux`|Utilisateurs, fichiers spécifiques, informations spécifiques et autres.|
|`☐ Traitement des preuves`|Chiffrement, protocoles sécurisés|
|`☐ Sauvegardes système`|Fichiers de configuration, bases de données et autres.|
|`☐ Traitement des informations`|Chiffrement fort des données|
|`☐ Gestion et signalement des incidents`|Cas de contact, interruptions du pentest, type de rapports|
|`☐ Réunions de suivi`|Fréquence des réunions, dates, heures, parties incluses|
|`☐ Rapports`|Type, lecteurs cibles, orientation|
|`☐ Re-tests`|Dates de début et de fin|
|`☐ Avertissements et limitation de responsabilité`|Dommages au système, perte de données|
|`☐ Autorisation de test`|Contrat signé, contrat de prestation|

---

## Réunion de lancement

La `réunion de lancement` a généralement lieu à une heure programmée et en personne après la signature de tous les documents contractuels. Cette réunion inclut généralement les points de contact du client (de l'audit interne, de la sécurité de l'information, de l'informatique, de la gouvernance et des risques, etc., selon le client), le personnel de support technique du client (développeurs, administrateurs système, ingénieurs réseau, etc.), et l'équipe de test d'intrusion (une personne ayant un rôle de management (comme le responsable de la pratique), le ou les testeurs d'intrusion réels, et parfois un chef de projet ou même le responsable de compte commercial ou un poste similaire). Nous passerons en revue la nature du test d'intrusion et la manière dont il se déroulera. Habituellement, il n'y a pas de tests de déni de service (DoS). Nous expliquons également que si une vulnérabilité critique est identifiée, les activités de test d'intrusion seront suspendues, un rapport de notification de vulnérabilité sera généré et les contacts d'urgence seront contactés. En général, ces notifications ne sont générées que lors des tests d'intrusion externes pour des failles critiques telles qu'une exécution de code à distance (RCE) non authentifiée, une injection SQL, ou une autre faille menant à la divulgation de données sensibles. Le but de cette notification est de permettre au client d'évaluer le risque en interne et de déterminer si le problème justifie un correctif d'urgence. Nous n'arrêterions généralement un test d'intrusion interne et n'alerterions le client que si un système ne répond plus, si nous trouvons des preuves d'activité illégale (comme du contenu illégal sur un partage de fichiers) ou la présence d'un acteur de menace externe sur le réseau ou une violation antérieure.

Nous devons également informer nos clients des risques potentiels lors d'un test d'intrusion. Par exemple, nous devons mentionner qu'un test d'intrusion peut laisser de nombreuses `entrées de journal et alarmes` dans leurs applications de sécurité. De plus, si des attaques par force brute ou similaires sont utilisées, il convient de mentionner que nous pourrions accidentellement `verrouiller certains utilisateurs` trouvés lors du test d'intrusion. Nous devons également informer nos clients qu'ils doivent nous contacter immédiatement si le test d'intrusion effectué a un `impact négatif sur leur réseau`.

Expliquer le processus de test d'intrusion donne à toutes les personnes impliquées une idée claire de l'ensemble de notre processus. Cela démontre notre approche professionnelle et convainc nos interlocuteurs que nous savons ce que nous faisons. Car, à part le personnel technique, le CTO et le CISO, cela ressemblera à une sorte de magie très difficile à comprendre pour les professionnels non techniques. Nous devons donc être attentifs à notre public et cibler l'interlocuteur le moins expérimenté techniquement afin que notre approche puisse être suivie par tous ceux à qui nous parlons.

Tous les points liés aux tests doivent être discutés et clarifiés. Il est crucial de répondre précisément aux souhaits et aux attentes du client. La structure et le réseau de chaque entreprise sont différents et nécessitent une approche adaptée. Chaque client a des objectifs différents, et nous devons ajuster nos tests à leurs souhaits. Nous pouvons généralement voir dès le début de l'appel à quel point nos clients sont expérimentés en matière de tests d'intrusion, nous devrons donc peut-être nous concentrer sur une explication plus détaillée et être prêts à répondre à plus de questions, ou la réunion de lancement peut être très rapide et simple.

---

## Contrat de prestation

Si le test d'intrusion comprend également des tests physiques, un contrat de prestation supplémentaire est requis. Comme il ne s'agit pas seulement d'un environnement virtuel mais aussi d'une intrusion physique, des lois complètement différentes s'appliquent ici. Il est également possible que de nombreux employés n'aient pas été informés du test. Si nous rencontrons des employés ayant une très forte conscience de la sécurité lors de l'attaque physique et des tentatives d'ingénierie sociale, et que nous nous faisons prendre, les employés contacteront dans la plupart des cas la police. Ce `contrat de prestation` supplémentaire est notre « `carte de sortie de prison` » dans ce cas.

#### Contrat de prestation - Liste de contrôle pour les évaluations physiques

|**Point de contrôle**|
|---|
|`☐ Introduction`|
|`☐ Prestataire`|
|`☐ Finalité`|
|`☐ Objectif`|
|`☐ Testeurs d'intrusion`|
|`☐ Coordonnées`|
|`☐ Adresses physiques`|
|`☐ Nom du bâtiment`|
|`☐ Étages`|
|`☐ Identifiants des locaux physiques`|
|`☐ Composants physiques`|
|`☐ Calendrier`|
|`☐ Légalisation`|
|`☐ Autorisation de test`|

---

## Mise en place

Après que tous les points ci-dessus ont été traités et que nous disposons des informations nécessaires, nous planifions notre approche et préparons tout. Nous constaterons que les résultats du test d'intrusion sont encore inconnus, mais nous pouvons préparer nos VM, VPS et autres outils/systèmes pour tous les scénarios et toutes les situations. Plus d'informations et comment préparer ces systèmes peuvent être trouvées dans le module [Mise en place](https://academy.hackthebox.com/module/details/87).
---

← [[06 - Processus de test d'intrusion]] | [[00 - Sommaire Penetration Testing Process|Sommaire]] | [[08 - Collecte d'informations]] →
