---
tags:
  - python
ordre: 10
---

# Les premières itérations

---

Nous allons commencer à implémenter le programme petit à petit, en veillant toujours à atteindre une étape importante où le code fonctionne, même s'il n'est pas encore tout à fait complet. Même si nous avons une idée précise de la manière dont le code sera implémenté et de ce à quoi il ressemblera au final, il est toujours bon d'y aller doucement et de construire les choses couche par couche.

Puisque nous voulons aboutir à un programme qui peut récupérer tous les mots d'une page web et peut-être aussi avoir quelques autres fonctionnalités, écrivons d'abord le code nécessaire pour effectuer la tâche la plus basique : afficher le HTML d'une page web. En bref, voici ce que nous devrions viser :

- Le code téléchargera et affichera l'intégralité du HTML d'une page web.
- L'URL de la page web est fixée dans le code.
- Nous écrirons le code dans sa forme la plus simple et réécrirons des morceaux si nécessaire.
- Nous utiliserons la bibliothèque `requests`.

Alors, commençons par le commencement, importons la bibliothèque `requests` et stockons l'URL cible dans une variable. Ensuite, nous utilisons la bibliothèque `requests` pour obtenir l'URL que nous avons fournie et afficher le HTML.

#### Affichage du code source de la page web

```python
import requests  PAGE_URL = 'http://target:port'  resp = requests.get(PAGE_URL) html_str = resp.content.decode() print(html_str)
```

Maintenant, que se passe-t-il si nous nous trompons dans l'orthographe de l'URL ? Essayons dans notre terminal interactif Python et voyons :

#### Expérimentation dans IDLE

```python
>>> r = requests.get('http://target:port/missing.html') >>> r.status_code  404 >>> print(r.content.decode())  <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"         "http://www.w3.org/TR/html4/strict.dtd"> <html>     <head>         <meta http-equiv="Content-Type" content="text/html;charset=utf-8">         <title>Error response</title>     </head>     <body>         <h1>Error response</h1>         <p>Error code: 404</p>         <p>Message: File not found.</p>         <p>Error code explanation: HTTPStatus.NOT_FOUND - Nothing matches the given URI.</p>     </body> </html>
```

Sur une note positive, nous obtenons un `status_code` correct du serveur web, qui dans cet exemple est le module de serveur web fourni avec Python (`http.server`). Cependant, si nous nous attendions à ce que la sortie HTML contienne des éléments spécifiques auxquels nous aurions ensuite essayé d'accéder et d'utiliser, par exemple, un `<div id="products">`, notre programme Python planterait en essayant d'utiliser des choses qui n'existent pas. Il n'y a pas de produits sur cette page d'erreur ! Oups. Mettons en place une simple vérification d'échec qui garantit que nous n'essayons pas de travailler avec des liens brisés.

#### Gestion « naïve » des erreurs

```python
import requests  PAGE_URL = 'http://target:port'  resp = requests.get(PAGE_URL)  if resp.status_code != 200:     print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')     exit(1)  html_str = resp.content.decode() print(html_str)
```

Maintenant, nous avons un code qui fait quelque chose, mais il n'est pas dans une fonction. Pour éviter d'encombrer le code, il est conseillé de garder les choses `simples` et `séparées`, alors allons-y et `refactorisons` le code, c'est-à-dire, changeons et donc améliorons le code.

---

## La fonction get_html_of

Jetons un coup d'œil au code suivant :

```python
import requests  PAGE_URL = 'http://target:port'  def get_html_of(url):     resp = requests.get(url)      if resp.status_code != 200:         print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')         exit(1)      return resp.content.decode()  print(get_html_of(PAGE_URL))
```

Nous avons déplacé la partie du code qui récupère le HTML dans une fonction, puis nous avons changé la dernière ligne du code pour afficher le résultat de cet appel de fonction au lieu d'une variable (qui n'existe plus). Notez également l'indentation à l'intérieur de la fonction.

Maintenant que la fonctionnalité la plus basique est en place, nous pouvons commencer à travailler avec la page HTML. Alors, réfléchissons un instant à ce que nous devons faire. Pour ce genre d'exercice, il peut être judicieux de lister les actions sur un bout de papier, puis pour chaque action, de se demander : « Comment faire cela ? » et d'écrire les étapes à côté. Dans notre cas, nous devons :

- Trouver tous les mots sur la page, en ignorant les balises HTML et autres métadonnées.
- Compter l'occurrence de chaque mot et la noter.
- Trier par occurrence.
- Faire quelque chose avec les mots les plus fréquents, par exemple, les afficher.

Comment trouver tous les mots sur la page, en ignorant les balises HTML et autres métadonnées ? C'est là que BeautifulSoup entre en jeu. Un rapide coup d'œil à la documentation ([https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)) montre que nous pouvons appeler l'objet `get_text()` de BeautifulSoup pour obtenir tout le texte de la page web sous forme de chaîne de caractères.

Ensuite, nous devons compter les occurrences de chaque mot. Il y a de nombreuses façons de le faire. Nous pourrions prendre le premier mot, compter toutes ses occurrences, le noter, et noter quel mot nous avons déjà compté. Ensuite, nous pourrions passer au mot suivant et - s'il n'a pas déjà été compté - compter son occurrence et le noter, tout en cochant le mot comme « compté ». Ce processus est relativement simple mais aussi assez lent. Imaginez faire cet exercice pour un livre entier rempli de mots. C'est relativement inefficace.

Soyons plus innovants et réfléchissons un instant si une application ou une machine dans la vie réelle compte déjà plusieurs articles d'une taille, d'une forme ou d'une valeur spécifiques. Le compteur de pièces des anciens distributeurs automatiques vient à l'esprit.

#### Les distributeurs automatiques à l'ancienne

Avant les smartphones et la numérisation de nombreuses machines, les distributeurs automatiques devaient compter le nombre de pièces que quelqu'un insérait et combien de chaque. Certaines machines pouvaient le faire en faisant glisser la pièce sur une rampe et en la faisant tomber dans le plus petit trou possible, en commençant du plus petit au plus grand. Ainsi, une grosse pièce glisserait sur un trou pour petite pièce, tandis qu'une petite pièce tomberait à travers le trou. Une pièce serait alors comptabilisée une fois (par exemple, en activant un petit bras/interrupteur métallique lors de sa chute).

Si nous comptons les mots de la même manière que certains distributeurs automatiques comptent les pièces, nous pouvons compter toutes les occurrences de tous les mots et n'avons besoin de parcourir le texte qu'une seule fois. Nous aurons un `dictionnaire` d'occurrences de mots, puis, pour chaque mot, nous vérifierons s'il a déjà été vu. Si c'est le cas, nous incrémenterons le compteur de un. S'il n'a pas été ajouté auparavant, nous ajouterons un enregistrement du mot et une occurrence de un pour ce mot.

Après cela, nous devons trier par occurrence pour voir quels mots sont apparus le plus souvent, et enfin, nous pouvons décider d'afficher les dix mots les plus utilisés. Alternativement, nous pourrions filtrer les mots et ne regarder que ceux de plus de quatre caractères, ou ajouter des variations de chiffres et de symboles et générer un dictionnaire pour les attaques par mot de passe. Nous y reviendrons plus tard.

---

## Regex

La première étape consistait à trouver tous les mots dans le HTML en ignorant les balises HTML. Si nous utilisons la fonction `get_text()` dont nous avons parlé plus tôt, nous pouvons utiliser le module d'expressions régulières `re` pour nous aider. Ce module dispose d'une fonction `findall` qui prend une chaîne de `regex` (abréviation de « `reg`ular `ex`pression », expression régulière) et du texte en paramètres, puis renvoie toutes les occurrences dans une liste. Nous utiliserons la chaîne de regex `\w+`, qui correspond à tous les caractères de mot, c'est-à-dire `a-z`, `A-Z`, `0-9` et `_`. Voici le code mis à jour :

#### Trouver tous les mots dans le HTML

```python
import requests import re from bs4 import BeautifulSoup  PAGE_URL = 'http://target:port'  def get_html_of(url):     resp = requests.get(url)      if resp.status_code != 200:         print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')         exit(1)      return resp.content.decode()  html = get_html_of(PAGE_URL) soup = BeautifulSoup(html, 'html.parser') raw_text = soup.get_text() all_words = re.findall(r'\w+', raw_text)
```

Un nouvel ajout est la chaîne de caractères `r'...'`. Il s'agit d'une chaîne de caractères brute (`r`aw string), ce qui signifie que Python doit supposer que les caractères à l'intérieur de la chaîne sont les caractères réels à utiliser. Normalement, un `\` est utilisé comme `caractère d'échappement`, ce qui nous aide à définir des caractères spéciaux - ou plutôt des octets - par exemple, `\n` ou `\t`, les caractères de nouvelle ligne et de tabulation, respectivement. Ici `r'\w+'` dit à Python d'interpréter la partie `\w` de la chaîne comme deux caractères individuels et non comme un `w` échappé.

Lorsque nous exécutons ce code, rien ne se passe, sauf en mémoire. La variable `all_words` est, en supposant que tout se passe bien, une liste de tous les mots de la page web par ordre d'occurrence et incluant les doublons. Nous allons ensuite parcourir cette liste et compter chaque mot. Une façon d'y parvenir est le morceau de code ci-dessous :

#### Comptage des occurrences de mots

```python
# Code précédent omis all_words = re.findall(r'\w+', raw_text)  word_count = {}  for word in all_words:     if word not in word_count:         word_count[word] = 1     else:         current_count = word_count.get(word)         word_count[word] = current_count + 1
```

Cet extrait de code devrait vous sembler familier. Pour résumer rapidement, nous déclarons une nouvelle variable `word_count` comme un dictionnaire vide - une structure de données de paires clé/valeur permettant de rechercher une valeur donnée à partir d'une clé. Ensuite, nous parcourons chaque mot dans `all_words` et vérifions s'il existe déjà. Nous définissons la clé (le mot) avec une valeur de `1` si ce n'est pas le cas. Sinon (else), nous obtenons la valeur actuelle définie pour `word` et définissons la nouvelle valeur de `word` à la valeur précédente plus un.

Nous avons maintenant un dictionnaire de tous les mots trouvés sur le site web et de leur occurrence respective.

|**Astuces avancées : « Python, c'est facile »**|
|---|
|On dit souvent que Python est facile, ce à quoi je réponds toujours « le Python simple est facile, le Python complexe ne l'est pas ». L'exemple précédent de comptage de mots peut en fait être réduit à ces deux lignes :  <br>  <br>for word in all_words:  <br>    word_countword = word_count.setdefault(word, 0) + 1  <br>  <br>Cependant, le nombre de choses qui se passent ici est assez surprenant. En bref, « setdefault » va SOIT définir la valeur de la clé (« word ») à la valeur spécifiée (0), si le dictionnaire ne contient pas déjà une clé « word », SOIT il retournera la valeur actuelle de la clé « word ». La 2ème ligne définit donc SOIT une valeur de 1 pour la clé « word », SOIT elle récupère la valeur actuelle et l'incrémente de un. Déroutant ? Oui. Notre propos ? Un code sophistiqué n'est pas toujours le meilleur choix, alors restez simple et intelligent. Nous ne sommes pas là pour nous vanter, nous sommes là pour résoudre des problèmes.|

Pour obtenir une liste triée des mots afin de nous concentrer sur ceux qui apparaissent le plus souvent, soit nous trouvons comme par magie le morceau de code ci-dessous, soit - de manière plus réaliste - nous cherchons de l'aide sur Google (« python sort dictionary by values » et des termes de recherche similaires) et trouvons la réponse ci-dessous.

#### Trier les mots dans une liste

```python
top_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
```

Comme pour tout ce qui se trouve en ligne, ne vous contentez pas de croire aveuglément qu'il n'y a rien de malveillant. En ce qui concerne le contenu très bien noté et les réponses avec beaucoup de retours positifs, un petit conseil est le vieil adage : faites confiance, mais vérifiez. Une fois que nous sommes sûrs que le morceau de code que nous avons trouvé est ce dont nous avons besoin. Nous pouvons enfin afficher les 10 mots les plus fréquents comme ceci :

#### Afficher 10 éléments

```python
>>> top_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True) >>> for i in range(10): ...    print(top_words[i])
```

Cela affichera une sortie similaire à :

```python
>>> top_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True) >>> for i in range(10): ...    print(top_words[i])  ('foo', 6) ('bar', 5) ('bas', 5) ('hello', 4) ('academy', 4) ('birb', 1)
```

Cela peut paraître un peu étrange ou du moins pas très utile pour la suite de notre parcours. Ce que nous pouvons faire, c'est afficher le mot réel au lieu d'afficher chaque tuple de (mot, occurrence) en sélectionnant le premier élément du tuple pour chaque tuple (`top_words[i][0]`). L'itération actuelle de l'ensemble du code ressemble à ceci :

#### La première itération

```python
import requests import re from bs4 import BeautifulSoup  PAGE_URL = 'http://target:port'  def get_html_of(url):     resp = requests.get(url)      if resp.status_code != 200:         print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')         exit(1)      return resp.content.decode()  html = get_html_of(PAGE_URL) soup = BeautifulSoup(html, 'html.parser') raw_text = soup.get_text() all_words = re.findall(r'\w+', raw_text)  word_count = {}  for word in all_words:     if word not in word_count:         word_count[word] = 1     else:         current_count = word_count.get(word)         word_count[word] = current_count + 1  top_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True)  for i in range(10):     print(top_words[i][0])
```

---

← [[09 - L'importance des bibliothèques]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[11 - Amélioration continue du code]] →
