---
tags:
  - web-applications
ordre: 15
---

# Vulnérabilités Web Courantes

---

Si nous effectuions un test d'intrusion (penetration test) sur une application web développée en interne ou si nous ne trouvions aucun exploit public pour une application web publique, nous pourrions identifier manuellement plusieurs vulnérabilités. Nous pouvons également découvrir des vulnérabilités causées par de mauvaises configurations (misconfigurations), même dans des applications web accessibles au public, car ces types de vulnérabilités ne sont pas causés par la version publique de l'application web mais par une mauvaise configuration de la part des développeurs. Les exemples ci-dessous sont quelques-uns des types de vulnérabilités les plus courants pour les applications web, faisant partie des vulnérabilités du [Top 10 de l'OWASP](https://owasp.org/www-project-top-ten/) pour les applications web.

---

## Authentification/Contrôle d'Accès Défaillant

`L'authentification défaillante` (Broken authentication) et `le contrôle d'accès défaillant` (Broken Access Control) sont parmi les vulnérabilités les plus courantes et les plus dangereuses pour les applications web.

`L'authentification défaillante` fait référence aux vulnérabilités qui permettent aux attaquants de contourner les fonctions d'authentification. Par exemple, cela peut permettre à un attaquant de se connecter sans avoir un jeu d'identifiants valide ou permettre à un utilisateur normal de devenir administrateur sans en avoir les privilèges.

`Le contrôle d'accès défaillant` fait référence aux vulnérabilités qui permettent aux attaquants d'accéder à des pages et des fonctionnalités auxquelles ils ne devraient pas avoir accès. Par exemple, un utilisateur normal qui obtient l'accès au panneau d'administration.

Par exemple, `College Management System 1.2` a une simple vulnérabilité de [contournement d'authentification (Auth Bypass)](https://www.exploit-db.com/exploits/47388) qui nous permet de nous connecter sans avoir de compte, en saisissant ce qui suit dans le champ de l'e-mail : `' or 0=0 #`, et en utilisant n'importe quel mot de passe.

---

## Téléversement de Fichiers Malveillants

Un autre moyen courant de prendre le contrôle d'applications web est le téléversement de scripts malveillants. Si l'application web dispose d'une fonctionnalité de téléversement de fichiers et ne valide pas correctement les fichiers téléversés, nous pouvons téléverser un script malveillant (par exemple, un script `PHP`), ce qui nous permettra d'exécuter des commandes sur le serveur distant.

Bien qu'il s'agisse d'une vulnérabilité de base, de nombreux développeurs ne sont pas conscients de ces menaces, ils ne vérifient et ne valident donc pas correctement les fichiers téléversés. De plus, certains développeurs effectuent des vérifications et tentent de valider les fichiers téléversés, mais ces vérifications peuvent souvent être contournées, ce qui nous permettrait tout de même de téléverser des scripts malveillants.

Par exemple, le plugin WordPress `Responsive Thumbnail Slider 1.0` peut être exploité pour téléverser n'importe quel fichier arbitraire, y compris des scripts malveillants, en téléversant un fichier avec une double extension (par exemple, `shell.php.jpg`). Il existe même un [module Metasploit](https://www.rapid7.com/db/modules/exploit/multi/http/wp_responsive_thumbnail_slider_upload/) qui nous permet d'exploiter facilement cette vulnérabilité.

---

## Injection de Commande

De nombreuses applications web exécutent des commandes locales du système d'exploitation pour effectuer certains processus. Par exemple, une application web peut installer un plugin de notre choix en exécutant une commande du système d'exploitation qui télécharge ce plugin, en utilisant le nom de plugin fourni. S'il n'est pas correctement filtré et assaini, les attaquants peuvent être en mesure d'injecter une autre commande à exécuter en même temps que la commande initialement prévue (par exemple, en tant que nom de plugin), ce qui leur permet d'exécuter directement des commandes sur le serveur back-end et d'en prendre le contrôle. Ce type de vulnérabilité est appelé [injection de commande (command injection)](https://owasp.org/www-community/attacks/Command_Injection).

Cette vulnérabilité est répandue, car les développeurs peuvent ne pas assainir correctement les entrées utilisateur ou utiliser des tests faibles pour le faire, permettant aux attaquants de contourner les vérifications ou le filtrage mis en place et d'exécuter leurs commandes.

Par exemple, le plugin WordPress `Plainview Activity Monitor 20161228` présente une [vulnérabilité](https://www.exploit-db.com/exploits/45274) qui permet aux attaquants d'injecter leur commande dans la valeur `ip`, en ajoutant simplement `| COMMAND...` après la valeur `ip`.

---

## Injection SQL (SQLi)

Une autre vulnérabilité très courante dans les applications web est une vulnérabilité d'`injection SQL` (SQL Injection). Similaire à une vulnérabilité d'injection de commande, cette vulnérabilité peut se produire lorsque l'application web exécute une requête SQL, incluant une valeur provenant d'une entrée fournie par l'utilisateur.

Par exemple, dans la section `database`, nous avons vu un exemple de la manière dont une application web utiliserait une entrée utilisateur pour rechercher dans une certaine table, avec la ligne de code suivante :

```php
$query = "select * from users where name like '%$searchInput%'";
```

Si l'entrée utilisateur n'est pas correctement filtrée et validée (comme c'est le cas avec les `injections de commande`), nous pouvons exécuter une autre requête SQL en même temps que cette requête, ce qui peut éventuellement nous permettre de prendre le contrôle de la base de données et de son serveur d'hébergement.

Par exemple, le même `College Management System 1.2` précédent souffre d'une [vulnérabilité](https://www.exploit-db.com/exploits/47388) d'injection SQL, dans laquelle nous pouvons exécuter une autre requête `SQL` qui renvoie toujours `true`, ce qui signifie que nous nous sommes authentifiés avec succès, nous permettant de nous connecter à l'application. Nous pouvons utiliser la même vulnérabilité pour récupérer des données de la base de données ou même prendre le contrôle du serveur d'hébergement.

Nous rencontrerons ces vulnérabilités à maintes reprises au cours de notre parcours d'apprentissage et lors d'évaluations en situation réelle. Il est important de se familiariser avec chacune d'entre elles, car même une compréhension de base de chacune nous donnera une longueur d'avance dans n'importe quel domaine de la sécurité de l'information. Les modules ultérieurs couvriront chacune de ces vulnérabilités en profondeur.
---

← [[14 - Frameworks de Développement & APIs]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[16 - Vulnérabilités publiques]] →
