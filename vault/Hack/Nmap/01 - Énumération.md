---
tags:
  - nmap
ordre: 1
---

# Énumération

---

L'`Énumération (Enumeration)` est la partie la plus critique de toutes. L'art, la difficulté et l'objectif ne sont pas d'obtenir l'accès à notre ordinateur cible. Il s'agit plutôt d'identifier toutes les manières possibles d'attaquer une cible.

Cela ne repose pas uniquement sur les outils que nous utilisons. Ceux-ci ne seront vraiment utiles que si nous savons quoi faire des informations que nous en obtenons. Les outils ne sont que des outils, et les outils seuls ne devraient jamais remplacer nos connaissances et notre souci du détail. Ici, il s'agit bien plus d'interagir activement avec les services individuels pour voir quelles informations ils nous fournissent et quelles possibilités ils nous offrent.

Il est essentiel de comprendre comment ces services fonctionnent et quelle syntaxe ils utilisent pour une communication et une interaction efficaces avec les différents services.

Cette phase vise à améliorer notre connaissance et notre compréhension des technologies, des protocoles et de leur fonctionnement, ainsi qu'à apprendre à gérer les nouvelles informations et à les adapter à nos connaissances déjà acquises. L'énumération consiste à collecter autant d'informations que possible. Plus nous aurons d'informations, plus il nous sera facile de trouver des vecteurs d'attaque.

Imaginez la situation suivante :

Notre partenaire n'est pas à la maison et a égaré nos clés de voiture. Nous appelons notre partenaire pour lui demander où se trouvent les clés. Si nous obtenons une réponse du type « dans le salon », c'est totalement flou et cela peut prendre beaucoup de temps pour les y trouver. Cependant, que se passerait-il si notre partenaire nous disait quelque chose comme « dans le salon, sur l'étagère blanche, à côté de la télé, dans le troisième tiroir » ? Par conséquent, il sera beaucoup plus facile de les trouver.

Il n'est pas difficile d'obtenir l'accès au système cible une fois que nous savons comment le faire. La plupart des moyens d'accès peuvent être résumés aux deux points suivants :

- `Fonctions et/ou ressources qui nous permettent d'interagir avec la cible et/ou de fournir des informations supplémentaires.`
- `Informations qui nous fournissent des renseignements encore plus importants pour accéder à notre cible.`

Lors de l'analyse et de l'inspection, nous recherchons précisément ces deux possibilités. La plupart des informations que nous obtenons proviennent d'erreurs de configuration ou d'une négligence de la sécurité pour les services respectifs. Les erreurs de configuration sont soit le résultat de l'ignorance, soit d'une mauvaise mentalité en matière de sécurité. Par exemple, si l'administrateur ne se fie qu'au pare-feu (firewall), aux Objets de Stratégie de Groupe (GPO - Group Policy Objects) et aux mises à jour continues, cela n'est souvent pas suffisant pour sécuriser le réseau.

`L'énumération est la clé`.

C'est ce que la plupart des gens disent, et ils ont raison. Cependant, c'est trop souvent mal compris. La plupart des gens pensent qu'ils n'ont pas essayé tous les outils pour obtenir les informations dont ils ont besoin. La plupart du temps, cependant, ce ne sont pas les outils que nous n'avons pas essayés, mais plutôt le fait que nous ne savons pas comment interagir avec le service et ce qui est pertinent.

C'est précisément la raison pour laquelle tant de personnes restent bloquées et n'avancent pas. Si ces personnes avaient investi quelques heures pour en apprendre davantage sur le service, son fonctionnement et sa finalité, elles auraient économisé quelques heures, voire quelques jours, pour atteindre leur objectif et accéder au système.

L'`énumération manuelle` est un composant `critique`. De nombreux outils d'analyse simplifient et accélèrent le processus. Cependant, ceux-ci ne peuvent pas toujours contourner les mesures de sécurité des services. La manière la plus simple d'illustrer cela est d'utiliser l'exemple suivant :

La plupart des outils d'analyse utilisent un délai d'attente (timeout) en attendant de recevoir une réponse d'un service/port. Si ce service/port ne répond pas dans un certain laps de temps, l'outil le marquera comme fermé, filtré ou inconnu. Dans les deux derniers cas, nous pourrons toujours travailler avec. Cependant, si un port est marqué comme fermé et que Nmap ne nous le montre pas, nous serons dans une mauvaise situation. Ce service/port pourrait nous offrir une opportunité de trouver un moyen d'accéder au système. Par conséquent, cela peut nous faire perdre beaucoup de temps inutilement avant que nous ne le trouvions.
---

[[00 - Sommaire Nmap|Sommaire]] | [[02 - Introduction à Nmap]] →
