---
tags:
  - pentest-process
ordre: 14
---

# Post-engagement

Tout comme il y a un travail préparatoire considérable avant qu'une mission ne commence officiellement (lorsque les tests débutent), nous devons effectuer de nombreuses activités (dont beaucoup sont contractuellement contraignantes) après que nos analyses, notre exploitation, notre mouvement latéral et nos activités de post-exploitation sont terminées. Il n'y a pas deux missions identiques, donc ces activités peuvent différer légèrement, mais elles doivent généralement être effectuées pour clôturer entièrement une mission.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process.png)

---

## Nettoyage

Une fois les tests terminés, nous devrions effectuer tout nettoyage nécessaire, comme la suppression des outils/scripts téléversés sur les systèmes cibles, l'annulation de toute modification de configuration (mineure) que nous aurions pu faire, etc. Nous devrions avoir des notes détaillées de toutes nos activités, rendant les activités de nettoyage faciles et efficaces. Si nous ne pouvons pas accéder à un système où un artefact doit être supprimé, ou si une autre modification doit être annulée, nous devons alerter le client et lister ces problèmes dans les annexes du rapport. Même si nous pouvons supprimer tous les fichiers téléversés et annuler les modifications (comme l'ajout d'un compte administrateur local), nous devons documenter ces changements dans les annexes de notre rapport au cas où le client recevrait des alertes sur lesquelles il doit enquêter et confirmer que l'activité en question faisait partie de nos tests autorisés.

---

## Documentation et rapports

Avant de terminer l'évaluation et de nous déconnecter du réseau interne du client ou d'envoyer des e-mails de notification d'arrêt pour signaler la fin des tests (ce qui signifie plus aucune interaction avec les hôtes du client), nous devons nous assurer d'avoir une documentation adéquate pour toutes les constatations que nous prévoyons d'inclure dans notre rapport. Cela inclut la sortie des commandes, les captures d'écran, une liste des hôtes affectés, et tout autre élément spécifique à l'environnement du client ou à la constatation. Nous devons également nous assurer que nous avons récupéré toutes les sorties d'analyse et de journaux si le client a hébergé une VM dans son infrastructure pour un test d'intrusion interne, ainsi que toute autre donnée qui pourrait être incluse dans le rapport ou comme documentation supplémentaire. Nous ne devons conserver aucune Information d'Identification Personnelle (PII), information potentiellement compromettante, ou autre donnée sensible que nous aurions pu rencontrer tout au long des tests.

Nous devrions déjà avoir une liste détaillée des constatations que nous inclurons dans le rapport et tous les détails nécessaires pour adapter les constatations à l'environnement du client. Le livrable de notre rapport (qui est traité en détail dans le module [Documentation & Reporting](https://academy.hackthebox.com/module/details/162)) devrait comprendre les éléments suivants :

- Une chaîne d'attaque (en cas de compromission interne complète ou d'accès de l'externe vers l'interne) détaillant les étapes suivies pour parvenir à la compromission
- Un résumé exécutif solide qu'un public non technique peut comprendre
- Des constatations détaillées spécifiques à l'environnement du client qui incluent une évaluation du risque, l'impact de la constatation, des recommandations de remédiation et des références externes de haute qualité liées au problème
- Des étapes adéquates pour reproduire chaque constatation afin que l'équipe responsable de la remédiation puisse comprendre et tester le problème tout en mettant en place les correctifs
- Des recommandations à court, moyen et long terme spécifiques à l'environnement
- Des annexes qui incluent des informations telles que le périmètre cible, les données OSINT (si pertinent pour la mission), l'analyse de cassage de mots de passe (si pertinent), les ports/services découverts, les hôtes compromis, les comptes compromis, les fichiers transférés vers les systèmes appartenant au client, toute création de compte/modification de système, une analyse de sécurité d'Active Directory (si pertinent), les données d'analyse/documentation supplémentaire pertinentes, et toute autre information nécessaire pour expliquer plus en détail une constatation ou une recommandation spécifique

À ce stade, nous créerons une version préliminaire du rapport qui sera le premier livrable que notre client recevra. À partir de là, il pourra commenter le rapport et demander toute clarification/modification nécessaire.

---

## Réunion de revue du rapport

Une fois que la version préliminaire du rapport est livrée et que le client a eu l'occasion de le distribuer en interne et de l'examiner en profondeur, il est d'usage d'organiser une réunion de revue du rapport pour parcourir les résultats de l'évaluation. La réunion de revue du rapport inclut généralement les mêmes personnes du côté du client et de l'entreprise qui réalise l'évaluation. Selon les types de constatations, le client peut faire appel à des experts techniques supplémentaires si la constatation est liée à un système ou une application dont ils sont responsables. Typiquement, nous ne lirons pas l'intégralité du rapport mot pour mot, mais nous parcourrons brièvement chaque constatation et donnerons une explication de notre propre perspective/expérience. Le client aura l'occasion de poser des questions sur tout ce qui se trouve dans le rapport, de demander des clarifications, ou de signaler des problèmes qui doivent être corrigés. Souvent, le client viendra avec une liste de questions sur des constatations spécifiques et ne voudra pas couvrir chaque constatation en détail (comme celles à faible risque).

---

## Acceptation du livrable

Le Périmètre des travaux (Scope of Work) doit clairement définir l'acceptation de tout livrable du projet. Dans les évaluations de tests d'intrusion, nous livrons généralement un rapport portant la mention `DRAFT` et donnons au client une chance de l'examiner et de le commenter. Une fois que le client a soumis ses commentaires (c.-à-d., les réponses de la direction, les demandes de clarification/modification, des preuves supplémentaires, etc.) soit par e-mail, soit (idéalement) lors d'une réunion de revue du rapport, nous pouvons leur fournir une nouvelle version du rapport portant la mention `FINAL`. Certains cabinets d'audit auxquels les clients peuvent être soumis n'accepteront pas un rapport de test d'intrusion avec la désignation `DRAFT`. D'autres entreprises ne s'en soucieront pas, mais il est préférable de maintenir une approche uniforme pour tous les clients.

---

## Tests post-remédiation

La plupart des missions incluent des tests post-remédiation dans le coût total du projet. Dans cette phase, nous examinerons toute documentation fournie par le client montrant des preuves de remédiation ou simplement une liste des constatations corrigées. Nous devrons accéder de nouveau à l'environnement cible et tester chaque problème pour nous assurer qu'il a été correctement corrigé. Nous émettrons un rapport post-remédiation qui montre clairement l'état de l'environnement avant et après les tests post-remédiation. Par exemple, nous pouvons inclure un tableau tel que :

|#|Gravité de la constatation|Titre de la constatation|Statut|
|---|---|---|---|
|1|Élevée|Injection SQL|Corrigé|
|2|Élevée|Authentification défaillante|Corrigé|
|3|Élevée|Téléversement de fichiers non restreint|Corrigé|
|4|Élevée|Filtrage web et de sortie inadéquat|Non corrigé|
|5|Moyenne|Signature SMB non activée|Non corrigé|
|6|Faible|Listage de répertoires activé|Non corrigé|

Pour chaque constatation (si possible), nous voudrons montrer la preuve que le problème n'est plus présent dans l'environnement par le biais de sorties d'analyse ou la preuve que les techniques d'exploitation originales échouent.

---

## Rôle du pentester dans la remédiation

Puisqu'un test d'intrusion est essentiellement un audit, nous devons rester des tiers impartiaux et ne pas effectuer de remédiation sur nos constatations (comme corriger du code, appliquer des correctifs aux systèmes, ou faire des changements de configuration dans Active Directory). Nous devons maintenir un certain degré d'indépendance et pouvons servir de conseillers de confiance en donnant des conseils généraux de remédiation sur la manière dont un problème spécifique pourrait être résolu ou être disponibles pour expliquer davantage/démontrer une constatation afin que l'équipe chargée de la corriger ait une meilleure compréhension. Nous ne devrions pas mettre en œuvre les changements nous-mêmes ni même donner des conseils de remédiation précis (par exemple, pour une injection SQL, nous pouvons dire « assainir les entrées utilisateur » mais pas donner au client un morceau de code réécrit). Cela aidera à maintenir l'intégrité de l'évaluation et à n'introduire aucun conflit d'intérêts potentiel dans le processus.

---

## Conservation des données

Après la conclusion d'un test d'intrusion, nous aurons une quantité considérable de données spécifiques au client, telles que les résultats d'analyse, les sorties de journaux, les identifiants, les captures d'écran, et plus encore. Les exigences de conservation et de destruction des données peuvent différer d'un pays à l'autre et d'une entreprise à l'autre, et les procédures relatives à chacune devraient être clairement décrites dans le langage contractuel du Périmètre des travaux et des Règles d'engagement (Rules of Engagement). Selon le [Guide des tests d'intrusion](https://www.pcisecuritystandards.org/documents/Penetration_Testing_Guidance_March_2015.pdf) de la norme de sécurité des données de l'industrie des cartes de paiement (PCI DSS) :

"Bien qu'il n'existe actuellement aucune exigence PCI DSS concernant la conservation des preuves collectées par le testeur d'intrusion, il est recommandé comme bonne pratique que le testeur conserve ces preuves (qu'il soit interne à l'organisation ou un fournisseur tiers) pendant une certaine période, tout en tenant compte des lois locales, régionales ou d'entreprise qui doivent être respectées pour la conservation des preuves. Ces preuves devraient être disponibles sur demande de l'entité cible ou d'autres entités autorisées, comme défini dans les règles d'engagement."

Nous devrions conserver les preuves pendant un certain temps après le test d'intrusion au cas où des questions surviendraient à propos de constatations spécifiques ou pour aider à retester les constatations « fermées » après que le client a effectué des activités de remédiation. Toutes les données conservées après l'évaluation doivent être stockées dans un endroit sécurisé appartenant à l'entreprise et contrôlé par elle, et chiffrées au repos. Toutes les données doivent être effacées des systèmes du testeur à la fin d'une évaluation. Une nouvelle machine virtuelle spécifique au client en question devrait être créée pour tout test post-remédiation ou investigation de constatations liées aux demandes du client.

---

## Clôture

Une fois que nous avons livré le rapport final, aidé le client avec des questions concernant la remédiation, et effectué les tests post-remédiation/émis un nouveau rapport, nous pouvons enfin clore le projet. À ce stade, nous devons nous assurer que tous les systèmes utilisés pour se connecter aux systèmes du client ou pour traiter des données ont été effacés ou détruits et que tous les artefacts restants de la mission sont stockés de manière sécurisée (chiffrés) conformément à la politique de notre entreprise et aux obligations contractuelles envers notre client. Les dernières étapes seraient de facturer le client et de percevoir le paiement pour les services rendus. Enfin, il est toujours bon de faire un suivi avec une enquête de satisfaction client post-évaluation afin que l'équipe et la direction, en particulier, puissent voir ce qui s'est bien passé pendant la mission et ce qui pourrait être amélioré du point de vue des processus de l'entreprise et du consultant individuel assigné au projet. Des discussions pour des travaux de suivi peuvent survenir dans les semaines ou les mois suivants si le client a été satisfait de notre travail et de nos interactions quotidiennes.

À mesure que nous développons continuellement nos compétences techniques, nous devrions toujours chercher des moyens d'améliorer nos compétences non techniques (soft skills) et de devenir des consultants professionnels plus complets. En fin de compte, le `client se souviendra généralement des interactions` pendant l'évaluation, de la communication et de la manière dont il a été traité/valorisé par l'entreprise qu'il a engagée, `et non de la chaîne d'exploit sophistiquée que le pentester a réussie pour pwn leurs systèmes`. Prenez ce temps pour faire une auto-réflexion et travailler sur l'amélioration continue dans tous les aspects de votre rôle en tant que testeur d'intrusion professionnel
---

← [[13 - Preuve de concept]] | [[00 - Sommaire Penetration Testing Process|Sommaire]] | [[15 - Pratique]] →
