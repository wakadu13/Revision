---
tags:
  - web-applications
ordre: 4
---

# HTML

---

Le premier et principal composant du front-end des applications web est le [HTML (HyperText Markup Language)](https://en.wikipedia.org/wiki/HTML). Le HTML est au cœur même de toute page web que nous voyons sur internet. Il contient les éléments de base de chaque page, y compris les titres, les formulaires, les images et de nombreux autres éléments. Le navigateur web, à son tour, interprète ces éléments et les affiche à l'utilisateur final.

Voici un exemple très simple de page HTML :

#### Exemple

```html
<!DOCTYPE html> <html>     <head>         <title>Page Title</title>     </head>     <body>         <h1>A Heading</h1>         <p>A Paragraph</p>     </body> </html>
```

Cela afficherait ce qui suit :![Fenêtre de navigateur avec le titre de page 'Page Title', l'URL 'www.example.coml', l'en-tête 'A Heading', et le paragraphe 'A Paragraph'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/75/web_apps_html_2.jpg)

Comme nous pouvons le voir, les éléments HTML sont affichés sous forme d'arborescence, similaire au `XML` et à d'autres langages :

#### Structure HTML

```bash
document  - html    -- head       --- title    -- body       --- h1       --- p
```

Chaque élément peut contenir d'autres éléments HTML, tandis que la balise `HTML` principale doit contenir tous les autres éléments de la page, qui relèvent de `document`, ce qui permet de distinguer le `HTML` des documents écrits pour d'autres langages, tels que les documents `XML`.

Les éléments HTML du code ci-dessus peuvent être visualisés comme suit :

<html>

    <head>

<title>Page Title</title>

    </head>

    <body>

<h1>A Heading</h1>

<p>A Paragraph</p>

    </body>

</html>

  

Chaque élément HTML est ouvert et fermé par une balise qui spécifie le type de l'élément (par ex. `<p>` pour les paragraphes), où le contenu est placé entre ces balises. Les balises peuvent également contenir l'ID ou la classe de l'élément (par ex. `<p id='para1'>` ou `<p id='red-paragraphs'>`), ce qui est nécessaire pour que le CSS formate correctement l'élément. Les balises et le contenu constituent l'élément entier.

---

## Encodage d'URL

Un concept important à apprendre en HTML est l'[encodage d'URL (URL Encoding)](https://en.wikipedia.org/wiki/Percent-encoding), ou encodage en pourcentage (percent-encoding). Pour qu'un navigateur affiche correctement le contenu d'une page, il doit connaître le jeu de caractères (charset) utilisé. Dans les URL, par exemple, les navigateurs ne peuvent utiliser que l'encodage [ASCII](https://en.wikipedia.org/wiki/ASCII), qui n'autorise que les caractères alphanumériques et certains caractères spéciaux. Par conséquent, tous les autres caractères en dehors du jeu de caractères ASCII doivent être encodés dans une URL. L'encodage d'URL remplace les caractères ASCII non sûrs par un symbole `%` suivi de deux chiffres hexadécimaux.

Par exemple, le caractère apostrophe '`'`' est encodé en '`%27`', ce que les navigateurs peuvent interpréter comme une apostrophe. Les URL ne peuvent pas contenir d'espaces et remplaceront un espace par un signe `+` (plus) ou par `%20`. Voici quelques encodages de caractères courants :

|Caractère|Encodage|
|---|---|
|space|%20|
|!|%21|
|"|%22|
|#|%23|
|$|%24|
|%|%25|
|&|%26|
|'|%27|
|(|%28|
|)|%29|

Une table d'encodage de caractères complète est disponible [ici](https://www.w3schools.com/tags/ref_urlencode.ASP).

De nombreux outils en ligne peuvent être utilisés pour effectuer l'encodage/décodage d'URL. De plus, le populaire proxy web [Burp Suite](https://portswigger.net/burp) dispose d'un décodeur/encodeur qui peut être utilisé pour convertir entre différents types d'encodages. Essayez d'encoder/décoder certains caractères et chaînes de caractères à l'aide de cet [outil en ligne](https://www.url-encode-decode.com/).

#### Utilisation

L'élément `<head>` contient généralement des éléments qui ne sont pas directement affichés sur la page, comme le titre de la page, tandis que tous les éléments principaux de la page se trouvent dans `<body>`. D'autres éléments importants incluent `<style>`, qui contient le code CSS de la page, et `<script>`, qui contient le code JS de la page, comme nous le verrons dans la section suivante.

Chacun de ces éléments est appelé un [DOM (Document Object Model)](https://en.wikipedia.org/wiki/Document_Object_Model). Le [World Wide Web Consortium (W3C)](https://www.w3.org/) définit le `DOM` comme suit :

`« Le Document Object Model (DOM) du W3C est une interface indépendante de la plateforme et du langage qui permet aux programmes et aux scripts d'accéder et de mettre à jour dynamiquement le contenu, la structure et le style d'un document. »`

La norme DOM est divisée en 3 parties :

- `Core DOM` - le modèle standard pour tous les types de documents
- `XML DOM` - le modèle standard pour les documents XML
- `HTML DOM` - le modèle standard pour les documents HTML

Par exemple, à partir de l'arborescence ci-dessus, nous pouvons nous référer aux DOM en tant que `document.head` ou `document.h1`, et ainsi de suite.

Comprendre la structure du DOM HTML peut nous aider à savoir où se trouve chaque élément que nous voyons sur la page, ce qui nous permet de visualiser le code source d'un élément spécifique de la page et de rechercher d'éventuels problèmes. Nous pouvons localiser les éléments HTML par leur ID, leur nom de balise ou leur nom de classe.

Ceci est également utile lorsque nous voulons exploiter des vulnérabilités front-end (comme le `XSS`) pour manipuler des éléments existants ou en créer de nouveaux pour nos besoins.
---

← [[03 - Front-end vs. Back-end]] | [[00 - Sommaire Introduction to Web Applications|Sommaire]] | [[05 - Feuilles de style en cascade (CSS)]] →
