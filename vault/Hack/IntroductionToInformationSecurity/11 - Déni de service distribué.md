---
tags:
  - infosec
ordre: 11
---

# Déni de service distribué

---

Chaque domaine de la `sécurité de l'information (Information Security)` se caractérise par des risques et des `menaces` uniques, spécifiques à son périmètre, ses fonctions et ses objectifs. Ces risques peuvent varier considérablement en fonction de plusieurs facteurs, notamment la nature et la finalité du domaine, les technologies et les systèmes sur lesquels il repose, le type et la sensibilité des données qu'il traite, ainsi que les vulnérabilités inhérentes à son architecture et à ses opérations.

Une attaque par `déni de service distribué (Distributed Denial of Service)` (`DDoS`) est une tentative malveillante d'interrompre le fonctionnement normal d'un site web, d'un serveur ou d'un service en ligne en le submergeant d'un déluge de trafic Internet. Contrairement à une attaque par `déni de service (Denial of Service)` (`DoS`) traditionnelle, qui provient d'une source unique, une attaque DDoS émane de plusieurs sources simultanément. Ces sources sont souvent des ordinateurs ou des appareils compromis et infectés par des logiciels malveillants, collectivement appelés « botnet ».

Imaginez que vous organisez l'inauguration de votre nouvelle boulangerie en ville. Vous avez invité vos amis, votre famille et les habitants du quartier à venir déguster vos délicieuses pâtisseries. Soudain, une foule immense se présente, non seulement plus nombreuse que prévu, mais si dense qu'elle remplit la boulangerie, bloque les entrées et empêche les vrais clients d'entrer. Ces gens n'ont aucune intention d'acheter quoi que ce soit. Ils sont simplement là pour semer le chaos. Cette foule perturbatrice empêche vos véritables clients d'accéder à votre commerce, mettant ainsi fin à votre activité pour la journée. Dans le monde numérique, ce scénario est similaire à ce qui se produit lors d'une `attaque DDoS`.

Considérez les attaquants comme les organisateurs qui ont recruté un grand groupe de personnes (le botnet) pour envahir votre boulangerie. Chaque individu dans la foule représente un appareil compromis qui envoie des requêtes à votre site web. Le volume considérable de ce trafic submerge vos ressources, rendant impossible l'accès à vos services pour les clients légitimes.

---

## Comment ça marche

Une attaque DDoS se compose de trois éléments principaux :

1. `L'attaquant` : La personne ou le groupe qui coordonne l'attaque dans le but de perturber une cible spécifique.
2. `Le botnet (réseau d'amplification)` : Un réseau d'appareils compromis répartis sur différents sites. Il peut s'agir d'ordinateurs personnels, de serveurs et même d'appareils de l'`Internet des objets (Internet of Things)` (`IoT`) comme des thermostats intelligents ou des caméras de sécurité qui ont été piratés à l'insu de leurs propriétaires.
3. `La victime` : Le serveur, le service ou le réseau ciblé que l'attaquant veut neutraliser.

L'attaquant envoie des commandes au botnet, ordonnant à tous les appareils compromis d'envoyer simultanément des requêtes à la victime. Cet afflux de trafic consomme la bande passante et la capacité de traitement de la cible, provoquant un ralentissement important ou une panne complète. Les utilisateurs légitimes ne peuvent plus accéder au service et subissent des retards ou des interruptions totales.

Imaginez un scénario où une `foule immense` (`botnet`) est dirigée pour déferler d'un seul coup dans un `petit magasin` (`victime`). Le nombre impressionnant de personnes submerge la capacité du magasin, empêchant les employés de se déplacer librement dans leur espace de travail. Ce chaos les empêche d'effectuer des tâches de base ou de traiter efficacement toute opération. La surpopulation perturbe entièrement le flux de travail, laissant les employés paralysés par cet afflux inattendu de personnes.

---

## Impact

En 2016, une importante attaque DDoS a visé Dyn, une entreprise qui fournit des services Internet critiques. L'attaque a touché de grands sites web comme Twitter, Netflix et Reddit, ainsi que plus de 50 autres services, les rendant inaccessibles pendant des heures dans certaines régions des États-Unis et d'Europe. Les attaquants ont utilisé un botnet nommé Mirai, qui a compromis des milliers d'appareils IoT tels que des caméras et des routeurs domestiques. Cet incident a mis en évidence la manière dont des appareils du quotidien pouvaient être exploités pour lancer des attaques à grande échelle, affectant des millions d'utilisateurs et d'entreprises dans le monde entier.

Les attaques DDoS peuvent avoir de graves conséquences pour les organisations comme pour les particuliers. L'`impact financier` pour les entreprises dépendant de leur présence en ligne peut être considérable, les temps d'arrêt entraînant des pertes de ventes et de revenus, en particulier pour les sites de commerce électronique, les services bancaires en ligne et les plateformes de streaming. L'`atteinte à la réputation` est une autre préoccupation majeure, car des pannes de service fréquentes ou prolongées peuvent éroder la confiance des clients et potentiellement les pousser vers la concurrence.

De plus, ces attaques peuvent provoquer des `perturbations opérationnelles`, interrompant des services essentiels et affectant non seulement la cible, mais aussi les utilisateurs qui dépendent de ces services pour des fonctions critiques. Peut-être plus insidieusement encore, les attaques DDoS peuvent parfois servir d'écran de fumée pour des activités plus malveillantes. Pendant que les équipes de sécurité s'affairent à restaurer les services, les attaquants peuvent en profiter pour exfiltrer des données ou installer des logiciels malveillants sans être détectés, ce qui peut conduire à des failles de sécurité encore plus graves.
---

← [[10 - Sécurité de l'Internet des objets]] | [[00 - Sommaire Introduction to Information Security|Sommaire]] | [[12 - Rançongiciel]] →
