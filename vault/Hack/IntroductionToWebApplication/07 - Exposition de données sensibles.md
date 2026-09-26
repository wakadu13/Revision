---
tags:
  - web-applications
ordre: 7
---

# Exposition de données sensibles

---

Tous les composants `front-end` que nous avons abordés interagissent côté client. Par conséquent, s'ils sont attaqués, ils ne constituent pas une menace directe pour le cœur du `back-end` de l'application web et n'entraînent généralement pas de dommages permanents. Cependant, comme ces composants sont exécutés `côté client`, ils exposent l'utilisateur final au risque d'être attaqué et exploité s'ils présentent des vulnérabilités. Si une vulnérabilité front-end est exploitée pour attaquer des utilisateurs administrateurs, cela pourrait entraîner un accès non autorisé, un accès à des données sensibles, une interruption de service, et plus encore.

Bien que la majorité des tests d'intrusion d'applications web se concentrent sur les composants back-end et leurs fonctionnalités, il est également important de tester les composants front-end à la recherche de vulnérabilités potentielles. En effet, ce type de vulnérabilités peut parfois être utilisé pour obtenir un accès à des fonctionnalités sensibles (par exemple, un panneau d'administration), ce qui peut conduire à la compromission de l'ensemble du serveur.

[L'exposition de données sensibles (Sensitive Data Exposure)](https://owasp.org/www-project-top-ten/2017/A3_2017-Sensitive_Data_Exposure) désigne la disponibilité de données sensibles en clair pour l'utilisateur final. On la trouve généralement dans le `code source` de la page web ou le source de la page sur le front-end des applications web. Il s'agit du code source HTML de l'application, à ne pas confondre avec le code back-end qui n'est généralement accessible que sur le serveur lui-même. Nous pouvons afficher le code source de n'importe quelle page web dans notre navigateur en faisant un clic droit n'importe où sur la page et en sélectionnant `Afficher le code source de la page` dans le menu contextuel. Parfois, un développeur peut désactiver le clic droit sur une application web, mais cela ne nous empêche pas de visualiser le code source de la page, car nous pouvons simplement taper `ctrl + u` ou le visualiser via un proxy web tel que `Burp Suite`. Jetons un œil au code source de la page google.com. Faites un clic droit et choisissez `Afficher le code source de la page`, et un nouvel onglet s'ouvrira dans notre navigateur avec l'URL `view-source:https://www.google.com/`. Nous pouvons y voir le `HTML`, le `JavaScript` et les liens externes. Prenez un moment pour parcourir un peu le code source de la page.

view-source:https://www.google.com/

![Capture d'écran de code HTML et JavaScript dans un éditeur de texte.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/view_source1.png)

Parfois, nous pouvons trouver des `identifiants` de connexion, des `hachages` ou d'autres données sensibles cachés dans les commentaires du code source d'une page web ou dans du code `JavaScript` externe importé. D'autres informations sensibles peuvent inclure des liens ou des répertoires exposés, ou même des informations utilisateur exposées, qui peuvent toutes potentiellement être exploitées pour étendre notre accès au sein de l'application web ou même de son infrastructure de support (serveur web, serveur de base de données, etc.).

Pour cette raison, l'une des premières choses à faire lors de l'évaluation d'une application web est d'examiner son code source pour voir si nous pouvons identifier des « failles évidentes », telles que des identifiants exposés ou des liens cachés.

---

#### Exemple

À première vue, ce formulaire de connexion ne semble avoir rien d'extraordinaire :

![Formulaire de connexion avec des champs pour le nom d'utilisateur et le mot de passe, et un bouton de connexion.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/web_apps_login_form_.png)

Jetons un œil au code source de la page :

```html
<form action="action_page.php" method="post">      <div class="container">         <label for="uname"><b>Username</b></label>         <input type="text" required>          <label for="psw"><b>Password</b></label>         <input type="password" required>          <!-- TODO: remove test credentials test:test -->          <button type="submit">Login</button>     </div> </form>  </html>
```

Nous voyons que les développeurs ont ajouté des commentaires qu'ils ont oublié de supprimer, qui contiennent des identifiants de test :

```html
<!-- TODO: remove test credentials test:test -->
```

Le commentaire semble être un rappel pour que les développeurs suppriment les identifiants de test. Étant donné que le commentaire n'a pas encore été supprimé, ces identifiants pourraient toujours être valides.

Bien qu'il ne soit pas très courant de trouver des identifiants de connexion dans les commentaires des développeurs, nous pouvons tout de même trouver divers éléments d'information sensibles et précieux en examinant le code source, tels que des pages ou des répertoires de test, des paramètres de débogage ou des fonctionnalités cachées. Il existe divers outils automatisés que nous pouvons utiliser pour scanner et analyser le code source disponible afin d'identifier des chemins ou des répertoires potentiels et d'autres informations sensibles.

L'exploitation de ce type d'informations peut nous donner un accès plus large à l'application web, ce qui peut nous aider à attaquer les composants back-end pour prendre le contrôle du serveur.

---

## Prévention

Idéalement, le code source front-end ne devrait contenir que le code nécessaire à l'exécution de toutes les fonctions de l'application web, sans code ou commentaire supplémentaire non indispensable à son bon fonctionnement. Il est toujours important de relire le code qui sera visible par les utilisateurs finaux via le code source de la page ou de le passer dans des outils pour vérifier la présence d'informations exposées.

Il est également important de classifier les types de données dans le code source et d'appliquer des contrôles sur ce qui peut ou ne peut pas être exposé côté client. Les développeurs doivent également relire le code côté client pour s'assurer qu'aucun commentaire inutile ou lien caché n'a été laissé. De plus, les développeurs front-end peuvent vouloir utiliser l'empaquetage (`packing`) ou l'obfuscation de code `JavaScript` pour réduire les risques d'exposer des données sensibles via le `code JavaScript`. Ces techniques peuvent empêcher les outils automatisés de localiser ce type de données.
---

← [[06 - JavaScript]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[08 - Injection HTML]] →
