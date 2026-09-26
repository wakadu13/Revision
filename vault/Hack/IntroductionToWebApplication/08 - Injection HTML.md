---
tags:
  - web-applications
ordre: 8
---

# Injection HTML

---

Un autre aspect majeur de la sécurité front-end est la validation et l'assainissement des entrées utilisateur acceptées. Dans de nombreux cas, la validation et l'assainissement des entrées utilisateur sont effectués sur le back-end. Cependant, certaines entrées utilisateur n'atteignent jamais le back-end dans certains cas et sont entièrement traitées et rendues sur le front-end. Il est donc essentiel de valider et d'assainir les entrées utilisateur à la fois sur le front-end et sur le back-end.

L'[injection HTML (HTML injection)](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/03-Testing_for_HTML_Injection) se produit lorsque des entrées utilisateur non filtrées sont affichées sur la page. Cela peut se faire soit en récupérant du code précédemment soumis, comme la récupération d'un commentaire d'utilisateur depuis la base de données back-end, soit en affichant directement des entrées utilisateur non filtrées via `JavaScript` sur le front-end.

Lorsqu'un utilisateur a un contrôle total sur la manière dont son entrée sera affichée, il peut soumettre du code `HTML`, et le navigateur peut l'afficher comme faisant partie de la page. Cela peut inclure un code `HTML` malveillant, comme un formulaire de connexion externe, qui peut être utilisé pour inciter les utilisateurs à se connecter tout en envoyant en réalité leurs identifiants de connexion à un serveur malveillant pour être collectés en vue d'autres attaques.

Un autre exemple d'`Injection HTML` est le défaçage de page web (web page defacing). Cela consiste à injecter du nouveau code `HTML` pour modifier l'apparence de la page web, insérer des publicités malveillantes, ou même changer complètement la page. Ce type d'attaque peut entraîner une grave atteinte à la réputation de l'entreprise qui héberge l'application web.

---

#### Exemple

L'exemple suivant est une page web très basique avec un seul bouton « `Click to enter your name` ». Lorsque nous cliquons sur le bouton, il nous invite à saisir notre nom, puis affiche notre nom sous la forme « `Your name is ...` » :

![Bouton intitulé 'Click to enter your name' et texte 'Your name is user'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/web_apps_html_injection_5.jpg)

Si aucun assainissement des entrées n'est en place, il s'agit potentiellement d'une cible facile pour les attaques d'`Injection HTML` et de `Cross-Site Scripting (XSS)`. Nous examinons le code source de la page et ne voyons aucun assainissement des entrées en place, car la page prend l'entrée de l'utilisateur et l'affiche directement :

```html
<!DOCTYPE html> <html>  <body>     <button onclick="inputFunction()">Click to enter your name</button>     <p id="output"></p>      <script>         function inputFunction() {             var input = prompt("Please enter your name", "");              if (input != null) {                 document.getElementById("output").innerHTML = "Your name is " + input;             }         }     </script> </body>  </html>
```

Pour tester une `Injection HTML`, nous pouvons simplement saisir un petit extrait de code `HTML` comme nom, et voir s'il est affiché comme faisant partie de la page. Nous allons tester le code suivant, qui modifie l'image de fond de la page web :

```html
<style> body { background-image: url('https://academy.hackthebox.com/images/logo.svg'); } </style>
```

Une fois que nous l'avons saisi, nous voyons que l'image de fond de la page web change instantanément :

![Bouton intitulé 'Click to enter your name' et texte 'Your name is' à côté du logo 'ACADEMY'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/web_apps_html_injection_6.jpg)

Dans cet exemple, comme tout est exécuté sur le front-end, rafraîchir la page web réinitialiserait tout à la normale.
---

← [[07 - Exposition de données sensibles]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[09 - Script inter-sites (Cross-Site Scripting - XSS)]] →
