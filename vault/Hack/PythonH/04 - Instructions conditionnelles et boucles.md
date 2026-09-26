---
tags:
  - python
ordre: 4
---

# Instructions conditionnelles et boucles

---

Maintenant, pimentons un peu les choses. Cette section traitera des instructions conditionnelles (if et else) et de divers types de boucles. Vous trouverez ci-dessous un exemple de ce à quoi ressemble un `bloc` de code if/else, c'est-à-dire la quantité de code qui constitue une technique particulière et qui est regroupée visuellement (généralement indentée au même niveau).

#### Un simple interrupteur de fonctionnalité

        Python
`happy = True  if happy:     print("Happy and we know it!") else:     print("Not happy...")`

Plusieurs choses se sont déjà produites ici. Portez une attention particulière à l'indentation du code. Python n'impose pas la largeur de chaque indentation, tant qu'il y a de la `cohérence`. Certaines personnes préfèrent deux espaces, d'autres 4. D'autres encore préfèrent un seul caractère de tabulation. Nous continuerons à utiliser quatre espaces par la suite.

Outre les indentations, deux nouveaux mots-clés sont utilisés ici : `if` et `else`. D'abord, nous définissons une variable qui, pour les besoins de la démonstration, est actuellement à TRUE. Ensuite, nous vérifions `if` la variable `happy` est `True` (`if some_var` est plus facile à lire mais aussi un raccourci pour `if some_var == True`), et si c'est `True`, alors nous affichons « Happy and we know it! » dans le terminal. Si `happy` n'est `pas` `True`, c'est-à-dire si elle est `False`, alors le bloc `else` est exécuté à la place, et « Not happy... » est affiché dans le terminal.

Néanmoins, nous devons également envisager la situation où nous voulons introduire plus que deux options différentes. L'expression `elif` (else-if) signifie que nous continuons avec celle-ci si la condition précédente n'est pas remplie. Fondamentalement, `elif` est la notation abrégée d'instructions `if` imbriquées.

#### Instruction If-Elif-Else

```python
happy = 2  if happy == 1:     print("Happy and we know it!") elif happy == 2:     print("Excited about it!") else:     print("Not happy...")
```

Cela nous amène au premier type de boucle : la `boucle while`. Considérez le code ci-dessous :

#### La boucle while

```python
counter = 0  while counter < 5:     print(f'Hello #{counter}')     counter = counter + 1
```

Avant de nous plonger dans le code, il est essentiel de savoir comment fonctionne une boucle while. Une boucle while est une boucle qui exécutera son contenu (le « bloc ») tant que la condition définie est `True`. Cela signifie que `while True` s'exécutera indéfiniment, et `while False` ne s'exécutera jamais. En faisant ce que nous faisons dans l'exemple, nous disons à Python d'exécuter le contenu de la boucle while tant que la variable `counter` est inférieure à 5. À l'intérieur de la boucle while, nous devons alors nous rappeler d'augmenter le `counter` d'au moins 1 à chaque itération, ou en tout cas à un moment donné. Si nous essayons d'exécuter l'exemple ci-dessus, `print` sera appelée cinq fois et affichera le contenu de la fonction.

Maintenant, quel est le contenu de `print` ? Parlons rapidement des chaînes de caractères formatées avant de continuer avec les boucles. Une chaîne de caractères formatée est une chaîne qui nous permet de `remplir la chaîne` avec des valeurs à l'exécution. Une nouvelle chaîne de caractères formatée a été introduite avec Python 3.6 : la [f-string](https://realpython.com/python-f-strings/) (exemple ci-dessus).

Alors qu'une chaîne de caractères normale pourrait ressembler à `'Hello world'`, une f-string ajoute un `f` au début : `f'Hello world'`. Ces deux chaînes particulières ont la même valeur. L'avantage de la f-string, cependant, est que nous pouvons remplacer des parties des chaînes par d'autres valeurs et variables en les encadrant d'une paire d'accolades, comme ceci :

#### Chaînes de caractères formatées

        Python
`equation = f'The meaning of life might be {6 * 7}.'  # -> Le sens de la vie pourrait être 42.  me = 'Birb' greeting = f'Hello {me}!'  # -> Bonjour Birb !`

Maintenant que nous savons qu'une boucle while est une boucle qui continue de s'exécuter `while` une certaine condition est vraie, et que nous savons que `f'Hello #{counter}'` sera égal à `Hello #` suivi du numéro de l'itération - en commençant à 0 - nous sommes prêts à essayer d'exécuter le code !

#### Boucle while

```bash
Hiterof13@htb[/htb]$ vim loop1.py

Hiterof13@htb[/htb]$ python3 loop1.py  Hello #0 Hello #1 Hello #2 Hello #3 Hello #4
```

Encore une fois : la boucle vérifie si le compteur, qui est initialement mis à 0, est inférieur à 5 - c'est le cas - puis affiche « Hello #0 » et définit la variable `counter` à la valeur d'elle-même (0) + 1. À l'itération suivante, elle vérifie si `counter`, qui est maintenant 1, est inférieur à 5 - c'est le cas - puis affiche « Hello #1 » et définit `counter` à la valeur d'elle-même (1) + 1. À la 3ème itération, `counter` est 2 (parce que nous avons commencé à 0), et ainsi de suite.

Dans la section suivante, nous continuerons à examiner les boucles, mais cette fois un type de boucle plus simple que nous privilégierons autant que possible.

---

## Boucles et listes

Rappelez-vous de la section précédente qu'une boucle est un bloc de code qui continue d'itérer sur son contenu jusqu'à ce qu'une certaine condition soit remplie. Cette section examinera un type de boucle souvent appelé « boucle for-each ». Il s'agit d'une boucle qui itère sur `chaque élément` d'une collection d'éléments et fait quelque chose `pour chaque` élément individuel. Considérez la ligne de code ci-dessous :

#### Une liste de chaînes de caractères

```python
groceries = ['Walnuts', 'Grapes', 'Bird seeds']
```

Ceci est une liste de chaînes de caractères. Les crochets indiquent une liste, et les valeurs séparées par des virgules à l'intérieur sont des chaînes de caractères. De même, `[]` est une liste vide, et `[42]` est une liste avec un seul élément, la valeur `int` `42`. Lorsqu'on désigne des valeurs à l'intérieur des listes, Python numérote les éléments d'une liste à partir de 0. Cela signifie que la liste ci-dessus a `trois éléments` et que `le premier` élément se trouve à l'`indice 0`. Le deuxième élément est à l'indice 1, et le troisième élément est à l'indice 2. Comme ceci :

#### Indices des valeurs

```python
groceries = ['Walnuts', 'Grapes', 'Bird seeds'] # indice :       0          1          2
```

Nous pouvons également écrire les listes de la manière suivante pour une meilleure lisibilité (surtout avec des listes beaucoup plus grandes) :

#### Syntaxe alternative

```python
groceries = [     'Walnuts',    # indice 0     'Grapes',     # indice 1     'Bird seeds'  # indice 2 ]
```

La dernière chose à mentionner sur les listes avant de continuer est la manière de retrouver un élément de la liste. Disons que nous voulons afficher le premier élément dans la console. Cela se fait en référençant le nom de la variable de la liste, par ex., `groceries` et l'indice désiré comme ceci : `groceries[0]` pour obtenir le premier élément, `'Walnuts'`. Le dernier élément, `'Bird seeds'`, serait dans cet exemple `groceries[2]` car la valeur `'Bird seeds'` se trouve à l'indice 2 dans la liste. Python peut même compter à rebours, donc nous aurions aussi pu obtenir le dernier élément de la liste - quel que soit le nombre d'éléments qu'elle contient - en demandant l'indice -1 : `groceries[-1]`. Cela fonctionne de la même manière que nous l'avons fait avec les chaînes de caractères.

#### Indexation des chaînes de caractères

Les chaînes de caractères peuvent également être indexées. C'est particulièrement utile lorsque nous voulons filtrer certaines parties d'une sortie. Nous pouvons considérer chaque mot comme une liste de lettres avec des indices. Cependant, il y a aussi l'indice négatif, qui nous permet de commencer à compter les lettres de la chaîne à partir de la fin. Prenons la chaîne suivante comme exemple : `ABCDEF`

|**Indice négatif**|**Indice**|**Caractère**|
|---|---|---|
|`-6`|`0`|A|
|`-5`|`1`|B|
|`-4`|`2`|C|
|`-3`|`3`|D|
|`-2`|`4`|E|
|`-1`|`5`|F|

Nous utilisons l'indice pour dire à Python quelle lettre nous voulons en extraire. Dans cet exemple, nous voulons extraire la première et la dernière lettre.

```python
>>> var = "ABCDEF" >>> print(var[0], var[1], var[2], var[3], var[4], var[5]) A B C D E F >>> print(var[-1], var[-2], var[-3], var[-4], var[-5], var[-6]) F E D C B A
```

Nous pouvons également travailler avec ces indices pour nous donner des sous-chaînes particulières.

#### Sous-chaînes

```python
>>> var = "ABCDEF" >>> print(var[:2])  # Jusqu'à l'indice 2 AB >>> print(var[2:])  # Ignorer tout jusqu'à l'indice 2 CDEF >>> print(var[2:4]) # Tout entre les indices 2 et 4 (l'indice "2" est inclus) CD >>> print(var[-2:]) # Jusqu'à l'indice négatif -2 (les deux derniers caractères) EF
```

---

## Boucle For-Each

Comme déjà mentionné, Python nous permet de boucler sur chaque élément (ou valeur) d'une liste. Considérez le morceau de code ci-dessous où nous avons d'abord défini une liste, puis la boucle.

#### La boucle For-Each

```python
groceries = ['Walnuts', 'Grapes', 'Bird seeds']  for food in groceries:     print(f'I bought some {food} today.')
```

La boucle for-each est structurée de cette manière : d'abord le mot-clé `for`, puis le nom de variable que nous choisissons, suivi du mot-clé `in` et d'une collection à parcourir. Dans cet exemple, nous avons dit à Python d'exécuter le code à l'intérieur du bloc « pour chaque élément », où nous appelons alors l'élément courant `food`. Nous disons ensuite à Python où trouver ces éléments, ce qui dans ce cas est à l'intérieur de `groceries`. Décomposons l'ensemble du processus d'itération.

Au début de la première itération, une variable `food` est définie sur la première valeur de `groceries`, `'Walnuts'`. Ensuite, nous affichons `'I bought some Walnuts today.'` car la f-string insère la valeur actuelle de `food` dans la chaîne. Nous répétons ensuite le processus ; cependant, `food` est défini sur le `deuxième` élément de la liste, `'Grapes'`. La troisième fois, `food` est défini sur le dernier élément de la liste de trois éléments, `'Bird seeds'`, parce que nous avons demandé à Python d'exécuter le `print` `pour` chaque élément de la liste.

Essayez d'implémenter l'exemple dans un nouveau script Python et de l'exécuter. Il devrait ressembler à quelque chose comme ceci :

#### Boucle while

```bash
Hiterof13@htb[/htb]$ vim groceries.py

Hiterof13@htb[/htb]$ python3 groceries.py  I bought some Walnuts today. I bought some Grapes today. I bought some Bird seeds today.
```

Notez qu'en Python, nous pouvons itérer sur chaque élément produit par un « générateur » ainsi que sur une collection de données. Nous ne couvrirons pas les générateurs dans ce module, car nous n'avons généralement pas besoin de nous en préoccuper lors de l'écriture de programmes Python.

---

## Exercices

Vous trouverez ci-dessous les blocs de code pertinents pour les exercices de cette section.

#### Bloc de code 1

```python
list_1  = [5, 3, 'Cake', True, 4, 5]
```

#### Bloc de code 2

```python
list_2 = [4, 3, 2, 1]  for num in list_2:     __________
```

#### Bloc de code 3

```python
list_3 = ['Accidental', '4daa7fe9', 'eM131Me', 'Y!.90'] secret = []  for x in list_3:     secret.append(x[:2])  print(''.join(secret))
```

---

← [[03 - Introduction aux variables]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[05 - Définir des Fonctions]] →
