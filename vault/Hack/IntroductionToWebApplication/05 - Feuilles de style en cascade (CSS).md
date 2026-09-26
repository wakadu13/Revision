---
tags:
  - web-applications
ordre: 5
---

# Feuilles de style en cascade (CSS)

---

[CSS (Cascading Style Sheets ou feuilles de style en cascade)](https://www.w3.org/Style/CSS/Overview.en.html) est le langage de feuilles de style utilisé avec HTML pour formater et définir le style des éléments HTML. Comme pour HTML, il existe plusieurs versions de CSS, et chaque version ultérieure introduit un nouvel ensemble de fonctionnalités qui peuvent être utilisées pour formater les éléments HTML. Les navigateurs sont mis à jour en parallèle pour prendre en charge ces nouvelles fonctionnalités.

---

#### Exemple

À un niveau fondamental, CSS est utilisé pour définir le style de chaque classe ou type d'éléments HTML (c'est-à-dire, `body` ou `h1`), de sorte que tout élément de cette page soit représenté tel que défini dans le fichier CSS. Cela peut inclure la famille de polices, la taille de la police, la couleur de l'arrière-plan, la couleur et l'alignement du texte, et plus encore.

        CSS
`body {   background-color: black; }  h1 {   color: white;   text-align: center; }  p {   font-family: helvetica;   font-size: 10px; }`

Comme mentionné précédemment, c'est pourquoi nous pouvons définir des ID ou des noms de classe uniques pour certains éléments HTML afin de pouvoir nous y référer plus tard dans CSS ou JavaScript si nécessaire.

---

## Syntaxe

CSS définit le style de chaque élément ou classe HTML entre des accolades `{}`, à l'intérieur desquelles les propriétés sont définies avec leurs valeurs (c'est-à-dire `element { property : value; }`).

Chaque élément HTML possède de nombreuses propriétés qui peuvent être définies via CSS, telles que `height`, `position`, `border`, `margin`, `padding`, `color`, `text-align`, `font-size`, et des centaines d'autres propriétés. Toutes ces propriétés peuvent être combinées et utilisées pour concevoir des pages web visuellement attrayantes.

CSS peut être utilisé pour des animations avancées pour une grande variété d'usages, du déplacement d'éléments jusqu'à des animations 3D complexes. De nombreuses propriétés CSS sont disponibles pour les animations, comme `@keyframes`, `animation`, `animation-duration`, `animation-direction`, et bien d'autres. Vous pouvez vous informer et essayer plusieurs de ces propriétés d'animation [ici](https://www.w3schools.com/css/css3_animations.asp).

---

#### Utilisation

CSS est souvent utilisé avec JavaScript pour effectuer des calculs rapides, ajuster dynamiquement les propriétés de style de certains éléments HTML, ou réaliser des animations avancées basées sur les frappes au clavier ou la position du curseur de la souris.

L'exemple suivant illustre magnifiquement de telles capacités de CSS lorsqu'il est utilisé avec HTML et JavaScript « Parallax Depth Cards - par Andy Merskin sur [CodePen](https://codepen.io/andymerskin/pen/XNMWvQ) » :

Vous pouvez cliquer sur les onglets en haut à gauche pour voir le code source.

Cela montre que même si HTML et CSS comptent parmi les pierres angulaires les plus fondamentales du développement web, lorsqu'ils sont utilisés correctement, ils peuvent servir à créer des pages web visuellement époustouflantes, ce qui peut rendre l'interaction avec les applications web beaucoup plus facile et conviviale.

De plus, CSS peut être utilisé avec d'autres langages pour implémenter leurs styles, comme `XML` ou au sein d'éléments `SVG`, et peut également être utilisé dans les plateformes de développement mobile modernes pour concevoir des interfaces utilisateur (UI) d'applications mobiles entières.

---

## Frameworks

Beaucoup peuvent considérer que le développement en CSS est difficile. D'autres, au contraire, peuvent affirmer qu'il est inefficace de définir manuellement le style et la conception de tous les éléments HTML de chaque page web. C'est pourquoi de nombreux frameworks CSS ont été introduits. Ils contiennent une collection de feuilles de style et de designs CSS, pour rendre la création de beaux éléments HTML beaucoup plus rapide et facile.

De plus, ces frameworks sont optimisés pour l'utilisation dans les applications web. Ils sont conçus pour être utilisés avec JavaScript et pour un usage étendu au sein d'une application web, et contiennent des éléments habituellement requis dans les applications web modernes. Voici quelques-uns des frameworks CSS les plus courants :

- [Bootstrap](https://www.w3schools.com/bootstrap4/)
- [SASS](https://sass-lang.com/)
- [Foundation](https://en.wikipedia.org/wiki/Foundation_\(framework\))
- [Bulma](https://bulma.io/)
- [Pure](https://purecss.io/)
---

← [[04 - HTML]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[06 - JavaScript]] →
