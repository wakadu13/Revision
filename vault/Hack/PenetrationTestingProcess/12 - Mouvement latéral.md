---
tags:
  - pentest-process
ordre: 12
---

# Mouvement latéral

---

Si tout s'est bien passé et que nous avons réussi à pénétrer le réseau d'entreprise (`Exploitation`), à collecter les informations stockées localement et à élever nos privilèges (`Post-Exploitation`), nous entrons ensuite dans la phase de `Mouvement latéral` (Lateral Movement). L'objectif ici est de tester ce qu'un attaquant pourrait faire au sein de l'ensemble du réseau. Après tout, le but principal n'est pas seulement d'exploiter avec succès un système accessible au public, mais aussi d'obtenir des données sensibles ou de trouver tous les moyens par lesquels un attaquant pourrait rendre le réseau inutilisable. L'un des exemples les plus courants est le [rançongiciel (ransomware)](https://www.csoonline.com/article/3236183/what-is-ransomware-how-it-works-and-how-to-remove-it.html). Si un système du réseau d'entreprise est infecté par un rançongiciel, celui-ci peut se propager sur l'ensemble du réseau. Il verrouille tous les systèmes à l'aide de diverses méthodes de chiffrement, les rendant inutilisables pour toute l'entreprise jusqu'à ce qu'une clé de déchiffrement soit saisie.

Dans les cas les plus courants, l'entreprise est financièrement extorquée dans un but lucratif. Souvent, ce n'est qu'à ce moment-là que les entreprises réalisent l'importance de la sécurité informatique. Si elles avaient eu un bon testeur d'intrusion (penetration tester) qui avait testé les choses (et mis en place des processus appropriés et des défenses en couches), elles auraient probablement pu éviter une telle situation et les dommages financiers (voire juridiques). On oublie souvent que dans de nombreux pays, `les PDG sont tenus pour responsables` de ne pas avoir sécurisé de manière appropriée les données de leurs clients.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-LA.png)

À ce stade, nous voulons tester jusqu'où nous pouvons nous déplacer manuellement dans l'ensemble du réseau et quelles vulnérabilités nous pouvons trouver d'un point de vue interne qui pourraient être exploitées. Pour ce faire, nous passerons à nouveau par plusieurs phases :

1. Pivoting
2. Tests évasifs
3. Collecte d'informations
4. Évaluation des vulnérabilités
5. Exploitation (de privilèges)
6. Post-Exploitation

Comme le montre le graphique ci-dessus, nous pouvons passer à cette étape depuis la phase d'`Exploitation` et de `Post-Exploitation`. Parfois, nous ne trouvons pas de moyen direct d'élever nos privilèges sur le système cible lui-même, mais nous avons des moyens de nous déplacer sur le réseau. C'est là que le `Mouvement latéral` entre en jeu.

---

## Pivoting

Dans la plupart des cas, le système que nous utilisons ne disposera pas des outils nécessaires pour énumérer efficacement le réseau interne. Certaines techniques nous permettent d'utiliser l'hôte exploité comme un proxy et d'effectuer tous les scans depuis notre machine d'attaque ou notre VM. Ce faisant, le système exploité représente et achemine toutes nos requêtes réseau envoyées depuis notre machine d'attaque vers le réseau interne et ses composants réseau.

De cette manière, nous nous assurons que les réseaux non routables (et donc inaccessibles publiquement) peuvent tout de même être atteints. Cela nous permet de les scanner à la recherche de vulnérabilités et de pénétrer plus profondément dans le réseau. Ce processus est également connu sous le nom de `Pivoting` ou `Tunneling`.

Un exemple très simple pourrait être que nous ayons une imprimante à la maison qui n'est pas accessible depuis Internet, mais nous pouvons envoyer des tâches d'impression depuis notre réseau domestique. Si l'un des hôtes de notre réseau domestique a été compromis, il pourrait être exploité pour envoyer ces tâches à l'imprimante. Bien qu'il s'agisse d'un exemple simple (et peu probable), il illustre l'objectif du `pivoting`, qui est d'accéder à des systèmes inaccessibles via un système intermédiaire.

---

## Tests évasifs

À ce stade également, nous devrions nous demander si les tests évasifs font partie du périmètre de l'évaluation. Il existe différentes procédures pour chaque tactique, qui nous aident à dissimuler ces requêtes pour ne pas déclencher une alarme interne chez les administrateurs et l'équipe bleue (blue team).

Il existe de nombreuses façons de se protéger contre le mouvement latéral, notamment la (micro)segmentation du réseau, la surveillance des menaces (threat monitoring), les `IPS`/`IDS`, les `EDR`, etc. Pour les contourner efficacement, nous devons comprendre comment ils fonctionnent et à quoi ils réagissent. Nous pouvons alors adapter et appliquer des méthodes et des stratégies qui aident à éviter la détection.

---

## Collecte d'informations

Avant de cibler le réseau interne, nous devons d'abord obtenir une `vue d'ensemble` des systèmes et du nombre de systèmes qui peuvent être atteints depuis notre système. Ces informations peuvent déjà être à notre disposition depuis la dernière étape de post-exploitation, où nous avons examiné de plus près les paramètres et les configurations du système.

Nous revenons à l'étape de collecte d'informations, mais cette fois, nous le faisons depuis l'intérieur du réseau avec une vision différente de celui-ci. Une fois que nous avons découvert tous les hôtes et serveurs, nous pouvons les énumérer individuellement.

---

## Évaluation des vulnérabilités

L'évaluation des vulnérabilités depuis l'intérieur du réseau diffère des procédures précédentes. En effet, beaucoup plus d'erreurs se produisent à l'intérieur d'un réseau que sur les hôtes et les serveurs exposés à Internet. Ici, les `groupes` auxquels on a été assigné et les `droits` sur différents composants du système jouent un rôle essentiel. De plus, il est courant que les utilisateurs partagent des informations et des documents et travaillent dessus ensemble.

Ce type d'information nous intéresse particulièrement lors de la planification de nos attaques. Par exemple, si nous compromettons un compte utilisateur assigné à un groupe de développeurs, nous pouvons obtenir l'accès à la plupart des ressources utilisées par les développeurs de l'entreprise. Cela nous fournira probablement des informations internes cruciales sur les systèmes et pourrait nous aider à identifier des failles ou à étendre notre accès.

---

## Exploitation (de privilèges)

Une fois que nous avons trouvé et hiérarchisé ces chemins, nous pouvons passer à l'étape où nous les utilisons pour accéder aux autres systèmes. Nous trouvons souvent des moyens de casser des mots de passe et des hachages (hashes) et d'obtenir des privilèges plus élevés. Une autre méthode courante consiste à utiliser nos identifiants existants sur d'autres systèmes. Il y aura aussi des situations où nous n'aurons même pas à casser les hachages mais pourrons les utiliser directement. Par exemple, nous pouvons utiliser l'outil [Responder](https://github.com/lgandx/Responder) pour intercepter des hachages NTLMv2. Si nous parvenons à intercepter un hachage d'un administrateur, nous pouvons alors utiliser la technique `pass-the-hash` pour nous connecter en tant que cet administrateur (dans la plupart des cas) sur plusieurs hôtes et serveurs.

Après tout, l'objectif de la phase de `Mouvement latéral` est de se déplacer à travers le réseau interne. Les données et informations existantes peuvent être polyvalentes et souvent utilisées de nombreuses manières.

---

## Post-Exploitation

Une fois que nous avons atteint un ou plusieurs hôtes ou serveurs, nous repassons par les étapes de la phase de post-exploitation pour chaque système. Ici, nous collectons à nouveau des informations système, des données provenant des utilisateurs créés et des informations commerciales qui peuvent être présentées comme preuves. Cependant, nous devons à nouveau considérer comment ces différentes informations doivent être traitées et les règles définies dans le contrat concernant les données sensibles.

Enfin, nous sommes prêts à passer à la phase de `Preuve de concept` (Proof-of-Concept) pour présenter notre travail acharné et aider notre client, ainsi que les responsables de la remédiation, à reproduire efficacement nos résultats.
---

← [[11 - Post-exploitation]] | [[00 - Sommaire Penetration Testing Process|Sommaire]] | [[13 - Preuve de concept]] →
