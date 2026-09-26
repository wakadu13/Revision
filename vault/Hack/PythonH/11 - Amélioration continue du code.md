---
tags:
  - python
ordre: 11
---

# Amélioration continue du code

---

À ce stade, nous disposons d'un script Python fonctionnel qui extrait les mots d'une page web et affiche dans la console les 10 qui apparaissent le plus souvent.

Supposons maintenant que notre mission nous demande de compter les mots sur deux pages web. Nous devrions alors répéter une grande partie du code ci-dessus pour la nouvelle page web. Une autre solution serait de _refactoriser_ le code actuel et de déplacer la partie qui s'occupe du comptage des mots dans sa propre fonction.

#### Extraction du code de comptage dans sa propre fonction

```python
def count_occurrences_in(word_list):     word_count = {}     for word in word_list:         if word not in word_count:             word_count[word] = 1         else:             current_count = word_count.get(word)             word_count[word] = current_count + 1     return word_count
```

Remarquez comment nous avons ajouté un paramètre d'entrée et remplacé la liste de mots à parcourir par ce nouveau paramètre `word_list`. Nous avons aussi ajouté une instruction `return` à la fin pour que notre fonction puisse renvoyer le résultat. Nous pouvons faire de même pour le code qui sert actuellement de liaison dans notre script :

#### Code de liaison actuel

```python
html = get_html_of(PAGE_URL) soup = BeautifulSoup(html, 'html.parser') raw_text = soup.get_text() all_words = re.findall(r'\w+', raw_text)
```

En remplaçant simplement la constante `PAGE_URL` (qui, par convention de nommage, n'est pas une constante) par la variable `url` et en renvoyant le résultat de l'appel à la fonction d'expression régulière `findall`, nous avons transformé le code de liaison statique en code réutilisable :

#### Refactorisé dans sa propre fonction

```python
def get_all_words_from(url):     html = get_html_of(url)     soup = BeautifulSoup(html, 'html.parser')     raw_text = soup.get_text()     return re.findall(r'\w+', raw_text)  all_words = get_all_words_from(PAGE_URL)
```

Si nous effectuons le même exercice pour le reste du code, nous obtenons ceci :

#### Refactorisation du code restant

```python
import requests import re from bs4 import BeautifulSoup  PAGE_URL = 'http://target:port'  def get_html_of(url):     resp = requests.get(url)      if resp.status_code != 200:         print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')         exit(1)      return resp.content.decode()  def count_occurrences_in(word_list):     word_count = {}      for word in word_list:         if word not in word_count:             word_count[word] = 1         else:             current_count = word_count.get(word)             word_count[word] = current_count + 1     return word_count  def get_all_words_from(url):     html = get_html_of(url)     soup = BeautifulSoup(html, 'html.parser')     raw_text = soup.get_text()     return re.findall(r'\w+', raw_text)  def get_top_words_from(all_words):     occurrences = count_occurrences_in(all_words)     return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)  all_words = get_all_words_from(PAGE_URL) top_words = get_top_words_from(all_words)  for i in range(10):     print(top_words[i][0])
```

Notez, en plus de ce qui précède, le morceau de code refactorisé suivant.

#### Code de liaison, mais plus propre

```python
def get_top_words_from(url):     all_words = get_all_words_from(url)     occurrences = count_occurrences_in(all_words)     return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)
```

Cette fonction prend une URL comme paramètre et l'utilise ensuite immédiatement pour appeler une autre fonction qui récupère la liste de mots nécessaire. Cette refactorisation supplémentaire a rendu le code nettement plus propre et plus facile à lire `dans cette situation`. Si nous devions parcourir dix pages, nous devrions à nouveau refactoriser pour ne pas nous répéter sans cesse. Une autre possibilité serait de charger une liste d'URL à partir d'un fichier texte, de collecter les mots pour chaque URL et d'agréger les données à la fin. Cependant, au lieu d'essayer de résoudre un problème qui n'existe pas, passons à autre chose.
---

← [[10 - Les premières itérations]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[12 - Améliorations supplémentaires]] →
