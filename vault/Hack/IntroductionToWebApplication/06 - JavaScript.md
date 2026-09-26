---
tags:
  - web-applications
ordre: 6
---

# JavaScript

---

[JavaScript](https://en.wikipedia.org/wiki/JavaScript) est l'un des langages les plus utilisés au monde. Il est principalement utilisé pour le développement web et le développement mobile. `JavaScript` est généralement utilisé sur le front-end d'une application pour être exécuté dans un navigateur. Cependant, il existe des implémentations de JavaScript back-end utilisées pour développer des applications web entières, comme [NodeJS](https://nodejs.org/en/about/).

Alors que `HTML` et `CSS` sont principalement responsables de l'apparence d'une page web, `JavaScript` est généralement utilisé pour contrôler toute fonctionnalité requise par la page web front-end. Sans `JavaScript`, une page web serait principalement statique et n'aurait pas beaucoup de fonctionnalités ou d'éléments interactifs.

---

#### Exemple

Dans le code source de la page, le code `JavaScript` est chargé avec la balise `<script>`, comme suit :

```html
<script type="text/javascript"> ..JavaScript code.. </script>
```

Une page web peut également charger du code `JavaScript` distant avec `src` et le lien du script, comme suit :

```html
<script src="./script.js"></script>
```

Voici un exemple d'utilisation basique de `JavaScript` dans une page web :

```javascript
document.getElementById("button1").innerHTML = "Changed Text!";
```

L'exemple ci-dessus modifie le contenu de l'élément HTML `button1`. À partir de là, il existe de nombreuses autres utilisations plus avancées de `JavaScript` sur une page web. Ce qui suit montre un exemple de ce que ferait le code `JavaScript` ci-dessus lorsqu'il est lié au clic d'un bouton :

Texte original

Comme avec HTML, il existe de nombreux sites disponibles en ligne pour expérimenter avec `JavaScript`. Un exemple est [JSFiddle](https://jsfiddle.net/) qui peut être utilisé pour tester `JavaScript`, `CSS` et `HTML` et pour sauvegarder des extraits de code. `JavaScript` est un langage avancé, et sa syntaxe n'est pas aussi simple que celle de `HTML` ou de `CSS`.

---

## Utilisation

La plupart des applications web courantes reposent fortement sur `JavaScript` pour gérer toutes les fonctionnalités nécessaires sur la page web, comme la mise à jour de la vue de la page web en temps réel, la mise à jour dynamique du contenu en temps réel, l'acceptation et le traitement des entrées utilisateur, et de nombreuses autres fonctionnalités potentielles.

`JavaScript` est également utilisé pour automatiser des processus complexes et effectuer des requêtes HTTP pour interagir avec les composants back-end et pour envoyer et récupérer des données, via des technologies comme [Ajax](https://en.wikipedia.org/wiki/Ajax_\(programming\)).

En plus de l'automatisation, `JavaScript` est aussi souvent utilisé avec `CSS`, comme mentionné précédemment, pour piloter des animations avancées qui ne seraient pas possibles avec `CSS` seul. Chaque fois que nous visitons une page web interactive et dynamique qui utilise de nombreuses animations avancées et visuellement attrayantes, nous voyons le résultat d'un code `JavaScript` actif s'exécutant sur notre navigateur.

Tous les navigateurs web modernes sont équipés de moteurs `JavaScript` qui peuvent exécuter du code `JavaScript` côté client (client-side) sans dépendre du serveur web back-end pour mettre à jour la page. Cela fait de l'utilisation de `JavaScript` un moyen très rapide de réaliser rapidement un grand nombre de processus.

---

## Frameworks

À mesure que les applications web deviennent plus avancées, il peut être inefficace d'utiliser du `JavaScript` pur pour développer une application web entière à partir de zéro. C'est pourquoi une multitude de frameworks (cadres d'application) `JavaScript` ont été introduits pour améliorer l'expérience du développement d'applications web.

Ces plateformes introduisent des bibliothèques qui rendent très simple la recréation de fonctionnalités avancées, comme la connexion et l'inscription des utilisateurs, et elles introduisent de nouvelles technologies basées sur celles qui existent déjà, comme l'utilisation de code `HTML` qui change dynamiquement, au lieu d'utiliser du code `HTML` statique.

Ces plateformes utilisent soit `JavaScript` comme langage de programmation, soit une implémentation de `JavaScript` qui compile son code en code `JavaScript`.

Voici quelques-uns des frameworks `JavaScript` front-end les plus courants :

- [Angular](https://www.w3schools.com/angular/angular_intro.asp)
- [React](https://www.w3schools.com/react/react_intro.asp)
- [Vue](https://www.w3schools.com/whatis/whatis_vue.asp)
- [jQuery](https://www.w3schools.com/jquery/)

Une liste et une comparaison des frameworks JavaScript courants peuvent être trouvées [ici](https://en.wikipedia.org/wiki/Comparison_of_JavaScript_frameworks).
---

← [[05 - Feuilles de style en cascade (CSS)]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[07 - Exposition de données sensibles]] →
