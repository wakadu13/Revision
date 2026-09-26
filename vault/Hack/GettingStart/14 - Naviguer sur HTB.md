---
tags:
  - getting-started
ordre: 14
---

# Naviguer sur HTB

---

`Hack The Box` fournit une mine d'informations pour quiconque débute dans les tests d'intrusion (penetration testing) ou cherche à améliorer ses compétences. Le site web offre de nombreuses opportunités d'apprentissage, il est donc impératif de comprendre sa structure et sa disposition pour tirer le meilleur parti de l'expérience d'apprentissage.

---

## Profil

Vous pouvez accéder à la page de votre profil HTB soit depuis le volet de gauche, soit en cliquant sur votre nom d'utilisateur dans le volet supérieur.

https://app.hackthebox.eu/profile/overview

![Aperçu du profil montrant le rang, la progression et les statistiques de possession.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_profile.jpg)

La page de votre profil affiche vos statistiques HTB, y compris votre rang, votre progression vers le rang suivant, le pourcentage de possession des différents challenges et laboratoires HTB, ainsi que d'autres statistiques similaires.

https://app.hackthebox.eu/profile/overview

![Graphique montrant les possessions utilisateur, système, challenge, les first bloods et les respect sur un an ; progression des machines et des challenges en dessous.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_profile_2.jpg)

Vous pouvez également trouver des statistiques détaillées sur votre progression dans les machines et les challenges, ainsi que l'historique de votre progression pour chacun d'eux. Vous y trouverez aussi les différents badges et certificats que vous avez obtenus. Vous pouvez partager la page de votre profil en cliquant sur le bouton `Share Profile`.

---

## Classements

La page des classements HTB (HTB Rankings) affiche les classements actuels des utilisateurs, des équipes, des universités, des pays et des membres VIP.

https://app.hackthebox.eu/rankings/teams

![Classement des équipes montrant les points, les utilisateurs, les systèmes, les challenges, les forteresses et les endgames.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_rankings.jpg)

Vous pouvez également consulter votre classement parmi les autres utilisateurs, votre meilleur rang et votre progression générale. De plus, votre classement et vos points s'ajoutent au classement de votre pays, que vous pouvez également consulter sur la page de classement par pays. Si vous faites partie d'une équipe ou d'une université, vos points s'ajouteront également aux leurs. Si vous êtes un utilisateur avec un abonnement VIP, vous pouvez voir votre rang VIP, qui comptabilise les points gagnés sur toutes les machines. Lorsque nous commençons sur la page principale de `HackTheBox`, nous voyons l'onglet `Labs` dans le panneau latéral, qui comprend les sections principales suivantes :

https://app.hackthebox.eu/home

![Tableau de bord affichant 914 joueurs en ligne, 1020 possessions de machines et 618 possessions de challenges aujourd'hui.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_main_1.jpg)

|`Parcours`|`Machines`|`Challenges`|`Forteresse`|`Endgame`|`Pro Lab`|
|---|---|---|---|---|---|

---

## Parcours

https://app.hackthebox.eu/tracks

![Parcours : Débutant, Intro à Dante, Intro à Offshore, Active Directory 101.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_tracks.jpg)

`HTB Tracks` est une excellente fonctionnalité qui aide à planifier vos prochaines machines et challenges. Un Parcours (Track) est une sélection de machines et de challenges regroupés pour permettre aux utilisateurs de progresser dans la maîtrise d'un sujet particulier. Que vous débutiez, que vous souhaitiez tester vos compétences Active Directory, ou que vous soyez prêt pour un défi dans le parcours Expert, vous trouverez un parcours approprié qui comprend une excellente sélection de machines et de challenges qui vous aideront à améliorer vos compétences dans un domaine spécifique. Les parcours sont créés par l'équipe `HTB`, des entreprises, des universités et même des utilisateurs. Lorsque vous cliquez sur un parcours, vous verrez toutes les machines et tous les challenges qu'il contient, votre progression dans chacun d'eux, et votre progression générale dans le parcours.

https://app.hackthebox.eu/tracks/1

![Progression du Parcours Débutant : 82% terminé, inclut les challenges Lame, Find The Easy Pass, Templated, Weak RSA.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/beginner_track.jpg)

Vous pouvez facilement vous inscrire au parcours et commencer à y progresser.

---

## Machines

Ensuite, nous avons la page `Machines`, l'une des pages les plus populaires de `HackTheBox`.

https://app.hackthebox.eu/machines

![Laboratoire de machines : Tenet (Moyen, Linux) et Registry (Difficile, Linux).](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_machines_1.jpg)

La première chose que vous verrez, ce sont deux machines recommandées sur lesquelles vous pouvez jouer : l'une est la dernière machine hebdomadaire publiée, et l'autre est une machine `Staff Pick` (choix de l'équipe) recommandée par l'équipe `HTB`.

https://app.hackthebox.eu/machines

![Machines actives : Doctor, Academy, Laboratory ; toutes de difficulté facile.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_machines_2.jpg)

Si vous faites défiler vers le bas, vous trouverez une liste de toutes les machines `HTB` réparties en deux onglets : `Active` (Actives) et `Retired` (Retirées).

Les `Machines Actives` sont celles qui vous rapportent des points pour votre classement, mais vous devrez les résoudre par vous-même en utilisant vos connaissances en pentesting. Il y a toujours 20 machines actives réparties entre les différentes difficultés. Une nouvelle machine est ajoutée chaque semaine, et l'une des machines actives est retirée, et ses points sont réinitialisés pour tout le monde.

Les `Machines Retirées` sont toutes les machines qui ont été précédemment présentées comme machine active hebdomadaire. Vous pouvez trouver une solution (walkthrough) pour chacune d'elles, mais les machines retirées ne vous rapporteront aucun point pour votre classement, bien qu'elles vous donnent des points pour le classement VIP, comme nous l'avons vu précédemment.

Note : Les machines retirées ne sont accessibles qu'avec un abonnement VIP, car seules les deux machines les plus récemment retirées sont accessibles gratuitement.

Vous pouvez filtrer les machines selon que vous les ayez terminées ou non, et en fonction de leur difficulté ou du type de système d'exploitation. Vous pouvez également trier les machines par leur date de sortie, leur note ou la difficulté évaluée par les utilisateurs. Si nous cliquons sur une machine, nous sommes redirigés vers sa page spécifique.

https://app.hackthebox.eu/machines/297

![Machine Academy : Difficulté Facile, note de 4.6, 6623 possessions utilisateur, 5837 possessions système.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/machine_page.jpg)

Vous pourrez jouer sur la machine en cliquant sur `Join Machine`. Vous obtiendrez alors l'IP de la machine, à laquelle vous pourrez accéder une fois connecté via le VPN de `HTB`. Vous pouvez également soumettre les drapeaux (flags) utilisateur et root que vous trouverez sur cette page.

Si la machine est retirée, vous pouvez cliquer sur l'onglet `Walkthroughs` pour voir une liste des solutions fournies, à la fois écrites et en vidéo. Enfin, vous pouvez consulter les onglets des statistiques et de l'activité pour voir les statistiques et l'activité les plus récentes des utilisateurs.

---

## Challenges

https://app.hackthebox.eu/challenges

![Challenges actifs : 11 Rétro-ingénierie, 8 Stéganographie, 12 Divers, 12 Web.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_challenges.jpg)

La disposition de la page des challenges est similaire à celle de la page des machines. Vous y trouverez des challenges `Actifs` et `Retirés`, classés en dix catégories différentes, chacune contenant un maximum de 10 challenges. Vous pouvez cliquer sur n'importe quelle catégorie pour prévisualiser la liste des challenges qu'elle contient, puis cliquer sur un challenge pour afficher sa page et soumettre ses drapeaux.

---

## Forteresse

Les forteresses (Fortresses) sont des laboratoires vulnérables créés par des entreprises externes et hébergés sur `HackTheBox`.

https://www.hackthebox.eu/home/careers/company/9

![Page Contexte : Point d'entrée 10.13.37.12, suivi de progression à 0%, état de réinitialisation du laboratoire.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_fortress_1.jpg)

Chaque laboratoire comporte plusieurs drapeaux qui peuvent être trouvés et soumis sur la page de la forteresse. Une fois que vous avez terminé le laboratoire en trouvant tous les drapeaux, vous recevez un badge de l'entreprise qui a créé la forteresse. Certaines entreprises proposent également des offres d'emploi qui sont conditionnées à la réussite des laboratoires pour se qualifier. Vous devez avoir le rang `HTB` `Hacker` ou supérieur pour jouer aux forteresses. Essayez d'améliorer votre classement en jouant aux machines et challenges actifs pour vous qualifier.

---

## Endgame

Les Endgames sont des laboratoires virtuels qui contiennent plusieurs machines connectées à un seul réseau. Les scénarios s'efforcent de refléter une situation du monde réel que vous pourriez rencontrer lors d'un test d'intrusion pour une véritable entreprise.

https://www.hackthebox.eu/home/endgame/view/5

![Page Ascension : Point d'entrée 10.13.38.20, suivi de progression à 0%, état de réinitialisation du laboratoire.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_endgame_1.jpg)

Tout comme les machines, chaque laboratoire Endgame a un chemin d'attaque (attack path) spécifique que vous devez exploiter. Cependant, comme les Endgames comportent plusieurs machines, nous pouvons apprendre des chemins d'attaque spécifiques que nous ne pourrions pas apprendre en utilisant une seule machine. Vous devez avoir le rang `HTB` `Guru` ou supérieur pour jouer aux Endgames actifs. Les Endgames retirés ne sont disponibles que pour les utilisateurs avec un abonnement VIP, et ils peuvent être joués à n'importe quel rang.

---

## Pro Labs

Les Pro Labs sont l'expérience de laboratoire ultime, car ils sont conçus pour simuler une infrastructure d'entreprise du monde réel, ce qui constitue une excellente occasion de tester vos compétences en pentesting.

https://www.hackthebox.eu/home/labs/pro/view/4

![Aperçu du Pro Lab Dante avec une mascotte de cowboy, 14 machines, 27 drapeaux, difficulté débutant, testeur d'intrusion de niveau 1.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_prolab_dante.jpg)

Les Pro Labs sont vastes et peuvent prendre un certain temps à terminer et à apprendre tous leurs chemins d'attaque et défis de sécurité. Chaque Pro Lab a un scénario et un niveau de difficulté spécifiques :

|Labo|Scénario|
|---|---|
|`Dante`|Adapté aux débutants pour apprendre les techniques et méthodologies de pentesting courantes, les outils de pentesting courants et les vulnérabilités communes.|
|`Offshore`|Laboratoire Active Directory qui simule un réseau d'entreprise du monde réel.|
|`Cybernetics`|Simule un environnement réseau Active Directory entièrement mis à niveau et à jour, qui est renforcé contre les attaques. Il s'adresse aux testeurs d'intrusion expérimentés et aux Red Teamers.|
|`RastaLabs`|Environnement de simulation Red Team, combinant l'attaque de mauvaises configurations et des utilisateurs simulés.|
|`APTLabs`|Ce laboratoire simule une attaque ciblée par un agent de menace externe contre un MSP (fournisseur de services gérés) et constitue le Pro Lab le plus avancé proposé à ce jour.|

Les Pro Labs nécessitent un plan d'abonnement distinct. Une fois que vous avez terminé un Pro Lab, vous obtenez un certificat de réussite HTB (HTB Certificate of Completion).

---

## Battlegrounds

Le dernier ajout à `HackThebox` est `HTB Battlegrounds`.

https://app.hackthebox.eu/battlegrounds/lobby

![Modes de jeu Cyber Mayhem et Server Siege, avec des icônes d'un pirate et d'un serveur.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/77/htb_battlegrounds.jpg)

`HTB Battlegrounds` est un jeu de stratégie et de piratage en temps réel. Vous pouvez jouer en équipe de 4 ou en équipe de 2.

Les batailles `Cyber Mayhem` sont basées sur le style attaque/défense, dans lequel chaque équipe se voit attribuer plusieurs machines qu'elle doit défendre contre les attaques tout en attaquant les machines de l'équipe adverse. Chaque attaque/défense vous rapporte un certain nombre de points, et chaque drapeau collecté compte également. Vous jouez pendant un certain temps, et l'équipe qui a le plus de points à la fin gagne.

`HTB Battlegrounds` est accessible à tous, mais il y a une limite sur le nombre de matchs autorisés, comme suit :

|**Statut**|**Matchs**|
|---|---|
|`Utilisateurs Gratuits`|2 matchs par mois|
|`VIP`|5 matchs par mois|
|`VIP+`|10 matchs par mois|

Le mode `Server Siege` est un style d'attaque uniquement, dans lequel l'équipe qui pirate l'autre équipe le plus rapidement gagne. Vous pouvez trouver un article détaillé sur `HTB Battlegrounds` en suivant ce [lien](https://help.hackthebox.com/en/articles/5185620-gs-how-to-play-battlegrounds).
---

← [[13 - Pour commencer]] | [[00 - Sommaire Getting Started|Sommaire]] | [[15 - Nibbles - Énumération]] →
