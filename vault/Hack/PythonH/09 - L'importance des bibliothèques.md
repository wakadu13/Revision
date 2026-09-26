---
tags:
  - python
ordre: 9
---

# L'importance des bibliothèques

---

Maintenant que nous savons à quel point les bibliothèques (libraries) peuvent être importantes pour notre développement et comment les gérer, nous allons aborder deux des plus populaires que nous utiliserons dans notre projet, en commençant par la bibliothèque `requests`.

---

## Le package Requests

La bibliothèque [requests](https://requests.readthedocs.io/en/master/) est une bibliothèque HTTP élégante et simple pour Python. D'après la documentation :

Requests vous permet d'envoyer des requêtes HTTP/1.1 très facilement. Il n'est pas nécessaire d'ajouter manuellement des chaînes de requête (query strings) à vos URL, ni d'encoder le formulaire de vos données POST. Le maintien de la connexion (keep-alive) et le regroupement des connexions HTTP (HTTP connection pooling) sont 100 % automatiques, grâce à urllib3.

Installons `requests` de la même manière que nous l'avons appris.

#### Installation de requests

```bash
Hiterof13@htb[/htb]$ python3 -m pip install requests  Collecting requests   Downloading requests-2.25.1-py2.py3-none-any.whl (61 kB)      |████████████████████████████████| 61 kB 3.8 MB/s Collecting chardet<5,>=3.0.2   Downloading chardet-4.0.0-py2.py3-none-any.whl (178 kB)      |████████████████████████████████| 178 kB 6.8 MB/s Collecting certifi>=2017.4.17 ...SNIP... Successfully installed certifi-2020.12.5 chardet-4.0.0 idna-2.10 requests-2.25.1 urllib3-1.26.3
```

Une fois installée, nous pouvons importer la bibliothèque dans notre code en tapant `import requests`, puis l'utiliser immédiatement.

Les deux choses les plus utiles à savoir sur la bibliothèque `requests` sont, premièrement, l'envoi de requêtes HTTP et, deuxièmement, qu'elle dispose d'une classe `Session`, qui est utile lorsque nous devons maintenir un certain contexte durant notre activité web. Par exemple, si nous devons conserver une série de cookies, nous pouvons utiliser un objet `Session`. Pour en obtenir un, nous importons `requests` et créons un objet de la classe `Session` comme ceci : `sess = requests.Session()`. Alternativement, nous pouvons utiliser le module `requests` (la bibliothèque elle-même) pour effectuer des requêtes HTTP. Cependant, l'état ne sera pas conservé automatiquement.

Considérez le code suivant :

#### Exemple avec `requests`

```python
import requests  resp = requests.get('http://httpbin.org/ip') print(resp.content.decode())  # Prints: # { #   "origin": "X.X.X.X" # }
```

Ceci est un exemple simple de la manière d'effectuer une requête GET pour obtenir notre adresse IP publique. Comme la variable `resp.content` est une chaîne d'octets (`byte-string`), c'est-à-dire une chaîne de bytes qui peut être imprimable ou non, nous devons appeler `decode()` sur l'objet. Décoder la chaîne d'octets avec la fonction `decode()` sans paramètres indique à Python d'interpréter les octets comme des caractères UTF-8. L'UTF-8 est l'encodage par défaut utilisé lorsqu'aucun autre encodage n'est spécifié. Cependant, d'autres encodages peuvent être utilisés et définis comme arguments de paramètre pour la fonction `decode()`, par exemple, `decode(encoding='UTF-16')`. Pour en revenir à l'objet `resp`, il contient des informations utiles telles que le `status_code`, le code de statut HTTP numérique de la requête que nous avons effectuée, et les cookies. Nous utiliserons cette bibliothèque plus tard, mais pour l'instant, continuons sur le thème de la nourriture.

---

## Le package BeautifulSoup

Un autre package pratique est la bibliothèque BeautifulSoup (ou plus précisément `beautifulsoup4`). Cette bibliothèque facilite grandement le travail avec le HTML en Python. Précédemment, nous avons appris à interroger un site web et à récupérer une sortie, qui pouvait être le HTML brut. Fouiller dans ce HTML peut être fastidieux si nous devons effectuer une recherche manuelle dans une sortie textuelle. BeautifulSoup transforme le HTML en objets Python beaucoup plus faciles à manipuler et nous permet de mieux analyser le contenu de manière programmatique. Installons BeautifulSoup.

#### Installation de BeautifulSoup

```bash
Hiterof13@htb[/htb]$ python3 -m pip install beautifulsoup4  Collecting beautifulsoup4   Downloading beautifulsoup4-4.9.3-py3-none-any.whl (115 kB)      |████████████████████████████████| 115 kB ... Collecting soupsieve>1.2   Downloading soupsieve-2.2-py3-none-any.whl (33 kB) Installing collected packages: soupsieve, beautifulsoup4 Successfully installed beautifulsoup4-4.9.3 soupsieve-2.2
```

Une fois installé, voyons quelques exemples rapides d'utilisation de `BeautifulSoup`. Pour une présentation plus détaillée, veuillez consulter la [documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). Pour l'instant, veuillez considérer le code ci-dessous :

#### HTML - Format brut

```html
<html> <head><title>Birbs are pretty</title></head> <body><p class="birb-food"><b>Birbs and their foods</b></p> <p class="food">Birbs love:<a class="seed" href="http://seeds" id="seed">seed</a>    and     <a class="fruit" href="http://fruit" id="fruit">fruit</a></p>  </body></html>
```

Ce code HTML semble un peu désordonné. Nous supposerons que ce HTML est stocké dans une variable `html_doc`. Nous le chargerons ensuite dans BeautifulSoup et l'afficherons de manière joliment formatée, comme suit :

#### Exemple avec BeautifulSoup

```python
from bs4 import BeautifulSoup  html_doc = """ html code goes here """ soup = BeautifulSoup(html_doc, 'html.parser') print(soup.prettify())
```

ce qui affiche alors :

#### HTML - Format indenté

```html
<html>  <head>   <title>    Birbs are pretty   </title>  </head>  <body>   <p class="birb-food">    <b>     Birbs and their foods    </b>   </p>   <p class="food">    Birbs love:    <a class="seed" href="http://seeds" id="seed">     seed    </a>    and    <a class="fruit" href="http://fruit" id="fruit">     fruit    </a>   </p>  </body> </html>
```

L'instruction d'importation de BeautifulSoup est intéressante. Comme la classe `BeautifulSoup` se trouve dans le module `bs4`, nous l'importerons généralement de cette manière. Dans le code, la classe est importée depuis le module, puis nous créons un nouvel objet BeautifulSoup et nous définissons l'analyseur (parser) de la classe sur l'analyseur HTML de BeautifulSoup. Nous devons définir cet analyseur lors du chargement du HTML.

Ne nous attardons pas trop sur des exemples inventés et passons directement à la mise en œuvre réelle de notre produit final : l'extracteur de mots.
---

← [[08 - Gérer les bibliothèques en Python]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[10 - Les premières itérations]] →
