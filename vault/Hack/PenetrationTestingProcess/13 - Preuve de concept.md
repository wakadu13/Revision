---
tags:
  - pentest-process
ordre: 13
---

# Preuve de concept

---

La `Preuve de concept` (`PoC` ou `Proof of Concept`) ou `Preuve de principe` est un terme de gestion de projet. En gestion de projet, elle sert de preuve qu'un projet est réalisable en principe. Les critères peuvent être d'ordre technique ou commercial. Il s'agit donc de la base pour les travaux futurs, dans notre cas, les étapes nécessaires pour sécuriser le réseau de l'entreprise en confirmant les vulnérabilités découvertes. En d'autres termes, elle sert de base à la prise de décision pour la suite des opérations. En même temps, elle permet d'identifier et de minimiser les risques.

![Processus de test d'intrusion : Pré-engagement, Collecte d'informations, Évaluation des vulnérabilités, Exploitation, Post-exploitation, Mouvement latéral, Preuve de concept, Post-engagement.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/90/0-PT-Process-POC.png)

Cette étape du projet est souvent intégrée au processus de développement de nouveaux logiciels applicatifs (prototypage) ou de solutions de sécurité informatique. Pour nous, dans le domaine de la sécurité de l'information, c'est là que nous prouvons l'existence de vulnérabilités dans les systèmes d'exploitation ou les logiciels applicatifs. Nous utilisons ce PoC pour prouver qu'un problème de sécurité existe, afin que les développeurs ou les administrateurs puissent le valider, le reproduire, en constater l'impact et tester leurs efforts de remédiation. L'un des exemples les plus courants pour prouver les vulnérabilités d'un logiciel est l'exécution de la calculatrice (`calc.exe` sous Windows) sur le système cible. En principe, le PoC évalue également la probabilité de succès d'un accès au système à partir d'une exploitation réelle.

Un `PoC` peut avoir de nombreuses représentations différentes. Par exemple, la `documentation` des vulnérabilités trouvées peut également constituer un PoC. La version plus pratique d'un PoC est un `script` ou un `code` qui exploite automatiquement les vulnérabilités découvertes. Cela démontre l'exploitation sans faille des vulnérabilités. Cette variante est simple pour un administrateur ou un développeur, car il peut voir les étapes suivies par notre script pour exploiter la vulnérabilité.

Cependant, il existe un inconvénient majeur qui s'est produit de temps à autre. Une fois que les administrateurs et les développeurs ont reçu un tel script de notre part, il leur est facile de « combattre » notre script. Ils se concentrent sur la modification des systèmes pour que le script que nous avons créé ne fonctionne plus. L'important est que le script ne soit qu'`une seule façon` d'exploiter une vulnérabilité donnée. Par conséquent, travailler contre notre script au lieu de l'utiliser, et modifier et sécuriser les systèmes pour que notre script ne fonctionne plus, ne signifie pas que les informations obtenues par le script ne peuvent pas être obtenues d'une autre manière. C'est un aspect important qui doit être discuté avec les administrateurs et les développeurs, et qui doit être explicitement mentionné et souligné.

Le rapport qu'ils reçoivent de notre part doit les aider à avoir une vue d'ensemble, à se concentrer sur les problèmes plus larges et à fournir des conseils de remédiation clairs. Inclure une présentation de la chaîne d'attaque en cas de compromission de domaine lors d'une évaluation interne est un excellent moyen de montrer comment plusieurs failles peuvent être combinées et comment la correction d'une seule faille brisera la chaîne, mais que les autres failles existeront toujours. Si celles-ci ne sont pas également corrigées, il peut exister un autre chemin pour atteindre le point où la chaîne d'attaque a été corrigée et continuer au-delà. Nous devrions également insister sur ce point lors de notre réunion de revue du rapport.

Par exemple, si un utilisateur utilise le mot de passe `Password123`, la vulnérabilité sous-jacente n'est pas le mot de passe, mais la `politique de mots de passe`. Si l'on découvre qu'un administrateur de domaine utilise ce mot de passe et qu'il est changé, ce compte aura désormais un mot de passe plus fort, mais le problème des mots de passe faibles restera probablement endémique au sein de l'organisation.

Si la politique de mots de passe suivait des normes élevées, l'utilisateur ne serait pas en mesure d'utiliser un mot de passe aussi faible. Les administrateurs et les développeurs sont responsables de la fonctionnalité et de la qualité de leurs systèmes et applications. De plus, une qualité élevée est synonyme de normes élevées, ce que nous devrions souligner dans nos recommandations de remédiation.
---

← [[12 - Mouvement latéral]] | [[00 - Sommaire Penetration Testing Process|Sommaire]] | [[14 - Post-engagement]] →
