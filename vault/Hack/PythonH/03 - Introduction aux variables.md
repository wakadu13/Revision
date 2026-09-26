---
tags:
  - python
ordre: 3
---

# Introduction aux variables

---

Supposons un instant que nous soyons chargés d'effectuer un test d'intrusion pour un client disposant d'un environnement utilisateur verrouillé. En examinant nos options pour notre test de type `Assume Breach`, c'est-à-dire un test partant du principe que nous avons déjà réussi à compromettre un compte utilisateur et une machine standard par hameçonnage (phishing), nous découvrons que nous pouvons exécuter des scripts Python. Nous pouvons générer une liste de comptes utilisateurs potentiels, et nous aimerions également avoir une liste de mots de passe potentiels `target specific` (spécifique à la cible). Nous remarquons que le site web du client contient de nombreux `buzzwords` (mots à la mode), et nous nous demandons si certains utilisateurs n'ont pas utilisé des variantes de noms de produits comme mots de passe. Pour cela, nous devons écrire un script simple capable de produire une liste des mots les plus fréquents d'un site web. Comme le client souhaite en obtenir une copie, nous ferons de notre mieux pour que le script soit facile à lire et à maintenir.

Avant de nous emballer, nous devons définir les éléments de base essentiels. Pour cela, parlons des mathématiques. Les mathématiques et la programmation ont des points communs : toutes deux utilisent assez souvent des variables et des constantes, et toutes deux ont des fonctions. En Python, une variable est notre façon de stocker une valeur quelconque en mémoire. Par exemple, un nombre, du texte, ou les octets d'une image. Comme en mathématiques, les variables ont un nom que nous inventons, mais en Python, les noms doivent être descriptifs. Voici quelques exemples :

#### Quelques variables simples

        Python
`advice = "Don't panic" ultimate_answer = 42 potential_question = 6 * 7 confident = True something_false = False problems = None # Oh, and by the way, this is a comment. We can tell by the leading # sign. # (Oh, et au fait, ceci est un commentaire. On le reconnaît au signe # qui le précède.)`

#### Chaînes de caractères (Strings)

La première variable, `advice`, est une `string` (chaîne de caractères). En Python, les chaînes de caractères peuvent être spécifiées en utilisant à la fois des `"double quotes"` (guillemets doubles) et des `'single quotes'` (guillemets simples). Lorsque vous saisissez des chaînes qui contiennent l'un ou l'autre de ces symboles comme partie intégrante de la chaîne elle-même, par exemple `don't lie`, il est judicieux d'utiliser l'`other` (autre) type de guillemets. Écrire `"don't lie"` fonctionne parfaitement. Cependant, l'utilisation de guillemets simples lèverait une erreur.

#### Nombres entiers (Integers)

Après la variable `advice` viennent deux nombres, ou `integers` (nombres entiers), dont le premier est un nombre. La deuxième variable, `potential_question`, est également un nombre, mais seulement au `runtime` (à l'exécution). Pendant l'exécution, l'équation `6 * 7` est évaluée à `42`, qui est ensuite stockée en tant que variable.

#### Booléens (Booleans)

Après les variables numériques viennent deux variables `boolean` (booléennes), `confident` et `something_false`. Une valeur booléenne est une valeur de vérité et peut être soit `True` (vrai), soit `False` (faux). Celles-ci s'avéreront utiles plus tard. Juste après vient la variable `problems`, qui est définie à `None`. [None](https://realpython.com/null-in-python/#:~:text=Python%20uses%20the%20keyword%20None,and%20a%20first%2Dclass%20citizen!) est une valeur spéciale de « néant », similaire à `null` dans d'autres langages. L'utilité de cette valeur est, entre autres, qu'elle nous permet de `define variables` (définir des variables) dans le code sans leur donner encore de valeur concrète. Elle nous permet également de créer un flux de programme plus significatif et de décider de transmettre `either` (soit) des données, `or` (soit) `None`, par exemple, en cas d'erreurs. De plus, elle nous permet de la retourner comme valeur si « rien de quelque chose » n'a été trouvé. Cela améliore également le flux et la lisibilité du programme.

#### Commentaires

Enfin, nous voyons un commentaire. Les commentaires fonctionnent de la même manière en Python que dans tous les autres langages : ils sont ignorés lors de l'exécution du programme et ne sont destinés qu'aux yeux des développeurs. Il peut parfois être conseillé d'utiliser des commentaires pour se souvenir de ce que fait un morceau de code ou pour expliquer une bizarrerie. Cependant, il est fortement recommandé d'écrire un code propre et simple qui n'aura pas besoin d'autre explication que le code lui-même. Ce n'est pas toujours la façon la plus simple de commencer, mais nous essaierons de viser cet objectif plus tard.

---

## Combinaison de variables

Passons en revue quelques exemples pour voir comment toutes ces variables peuvent également être combinées. Plus tard, que ce soit pour nos projets ou pour des tâches spécifiques, nous voudrons afficher des variables (et donc aussi leur contenu) ensemble. Par conséquent, passons d'abord brièvement en revue quelques opérations mathématiques de base avec Python.

#### Opérations mathématiques de base

```python
>>> 10 + 10     # Addition 20 >>> 20 - 10     # Soustraction 10 >>> 5 * 5       # Multiplication 25 >>> 10 / 5      # Division 2
```

Pour toutes ces valeurs, nous pouvons définir des variables pour les stocker. Quant au nom lui-même, nous pouvons les nommer comme nous le souhaitons, à quelques exceptions près, par exemple, ils doivent commencer par une lettre ou un `_`.

#### Sauvegarder des valeurs dans des variables

```python
>>> add = 10 + 10 >>> sub = 20 - 10 >>> multi = 5 * 5 >>> div = 10 / 5 >>> >>> print(add, sub, multi, div) 20 10 25 2
```

Cela nous permet également de travailler avec les valeurs stockées dans les variables individuelles.

#### Travailler avec des variables

```python
...SNIP... >>> print(add, sub, multi, div) 20 10 25 2 >>> result = (add * sub) - (multi * div)        # (20 * 10) - (25 * 2) >>> print('Result: ', result) Result:  150
```

Une autre fonctionnalité pratique de l'interpréteur Python est que l'IDLE assigne la dernière expression à la variable `_`. Cela nous permet de continuer à travailler avec la dernière valeur.

```python
>>> 38 + 4 42 >>> 50 - _      # 50 - 42 8
```

Notez cependant que cela n'est vrai _que_ pour l'IDLE. Dans du code Python standard exécuté à partir de fichiers `.py`, par exemple depuis la ligne de commande ou dans un Environnement de Développement Intégré (IDE), `_` est simplement une variable. Il est souvent utilisé comme espace réservé (placeholder) pour les valeurs dont nous ne nous soucions pas. Par exemple, si une fonction retourne deux valeurs, mais qu'une seule d'entre elles est importante pour nous, comme dans `x_coord, _ = get_position_of_birb()`. Cela sert à montrer aux autres développeurs, et à nous-mêmes quelques mois plus tard, que la valeur retournée, par exemple la coordonnée y de l'exemple précédent, n'est pas nécessaire.

---

## Style de codage

En Python, les noms de variables suivent la convention de nommage [snake_case](https://en.wikipedia.org/wiki/Snake_case). Cela signifie que les noms de variables doivent être entièrement en minuscules au départ, et qu'un tiret bas doit séparer les mots si le nom en contient plusieurs. Bien que le non-respect de ces conventions de nommage ne pose aucun problème pour le script - Python se moque de la façon dont nous nommons nos éléments - d'autres développeurs Python pourraient être déconcertés s'ils s'attendent à un ensemble de règles mais en rencontrent d'autres.

L'essentiel ici est que notre code soit facile à suivre et à lire. Chaque programmeur a son propre style et ses propres préférences en matière d'écriture de code. Il existe même plusieurs guides de style pour Python, comme le [PEP8](https://www.python.org/dev/peps/pep-0008/#type-variable-names), qui décrit certains types de définitions de variables ou de fonctions. Avoir un guide de style est très important lorsque nous voulons que quelqu'un lise le code que nous écrivons. Nous écrivons généralement du code pour que quelqu'un puisse l'utiliser, en tirer profit et éventuellement y travailler ou en apprendre quelque chose de nouveau. Sans guide de style, le débogage, l'amélioration ou l'extension deviennent extrêmement difficiles. Bien sûr, il y a beaucoup d'autres choses en dehors du guide de style auxquelles nous, en tant que programmeurs professionnels, devons prêter attention, comme l'architecture du code, les principes généraux de qualité du code, etc.
---

← [[02 - Exécuter du code Python]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[04 - Instructions conditionnelles et boucles]] →
