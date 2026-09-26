---
tags:
  - python
ordre: 2
---

# Exécuter du code Python

---

Il existe de nombreuses manières d'exécuter un morceau de code Python. Deux des méthodes les plus fréquemment utilisées sont l'exécution du code à partir d'un fichier `.py` et son exécution directe dans l'[IDLE](https://docs.python.org/3/library/idle.html) de Python, l'environnement de développement et d'apprentissage intégré (Integrated Development and Learning Environment). Dans cette section, nous verrons comment exécuter du code de ces deux manières. L'approche par fichier est pratique lors du développement d'un script réel, et l'approche avec IDLE est très utile pour tester rapidement quelque chose de petit. Nous commencerons par l'approche basée sur les fichiers.

---

## Python3

Commençons par un premier morceau de code très répandu qui affiche « Hello world » dans le terminal ou à l'écran. En Python, cela ressemble à ceci :

#### welcome.py

```python
print("Hello Academy!")
```

Si nous exécutons ce script, la chaîne de caractères `"Hello Academy!"` sera affichée dans le terminal. Pour l'essayer, nous ouvrons un éditeur de texte, nous tapons ce qui précède, et nous enregistrons le fichier sous le nom `welcome.py`. Ensuite, nous essayons de l'exécuter en tapant `python3 welcome.py`.

```bash
Hiterof13@htb[/htb]$ vim welcome.py

Hiterof13@htb[/htb]$ python3 welcome.py  Hello Academy!
```

---

## IDLE

Nous pouvons utiliser `IDLE`, l'environnement de développement intégré propre à Python, directement dans notre terminal pour un prototypage plus rapide. Nous le lançons en exécutant le binaire Python sans aucun argument. À l'intérieur, nous pouvons lui faire évaluer des équations mathématiques simples, par ex. `4 + 2`, ou stocker et utiliser des variables. Lors de l'évaluation d'une expression, le résultat sera affiché sur la ligne suivante si un résultat est retourné. Cependant, si l'expression est stockée dans une variable, rien ne sera affiché car rien n'est retourné (tout est contenu dans la variable). Nous pouvons également importer des bibliothèques et définir des fonctions et des classes directement dans l'IDLE pour les utiliser dans la même session. Nous approfondirons les bibliothèques, les fonctions et les classes plus tard. Pour quitter à nouveau l'IDLE, nous tapons `exit(0)`. Le nombre `0` est le [code de retour](https://en.wikipedia.org/wiki/Exit_status) (return code) du processus Python, où 0 signifie que tout va bien et un nombre différent de 0 indique une erreur. Considérez cet exemple d'utilisation de l'IDLE :

#### Python IDLE

```bash
Hiterof13@htb[/htb]$ python3  Python 3.9.0 (default, Oct 27 2020, 14:15:17)  [Clang 12.0.0 (clang-1200.0.32.21)] on darwin Type "help", "copyright", "credits" or "license" for more information. >>>
```

```python
>>> 4 + 3 7 >>> foo = 3 * 5 >>> foo 15 >>> foo + 4 19 >>> print('Hello Academy!') Hello Academy! >>> exit(0)
```

Python exécute le code de haut en bas. Il est important de garder cela à l'esprit lors de l'écriture de scripts Python, car Python n'a aucune idée de ce qui se trouve plus bas dans le script tant qu'il ne l'a pas atteint. Si nous voulions afficher une variable au lieu d'une valeur littérale, elle doit être définie avant d'y faire référence. Par exemple :

#### Hello Again, Academy

        Python
`>>> greeting = 'Hello again, Academy' >>> print(greeting) Hello again, Academy`

Cependant, nous pouvons afficher la sortie non seulement d'une variable, mais de plusieurs, dans différentes variations.

#### Printing Multiple Variables

```python
>>> a = 'HTB' >>> b = 'Academy' >>> print(a, b) HTB Academy
```

---

## Shebang

Une autre méthode consiste à ajouter le [shebang](https://en.wikipedia.org/wiki/Shebang_%28Unix%29#Portability) (`#!/usr/bin/env python3`) à la première ligne d'un script Python. Sur les systèmes d'exploitation basés sur Unix, le fait de marquer ceci avec un croisillon et un point d'exclamation provoque l'exécution de la commande suivante avec tous les arguments spécifiés lorsque le programme est appelé. Nous pouvons donner au script Python des droits d'exécution et l'exécuter directement sans taper `python` au début de la ligne de commande. Le nom du fichier est alors passé en tant qu'argument.

#### welcome.py

```python
#!/usr/bin/env python3  print("Hello Academy!")
```

#### Shebang Execution

```bash
Hiterof13@htb[/htb]$ chmod +x welcome.py

Hiterof13@htb[/htb]$ ./welcome.py  Hello Academy!
```

---

← [[01 - Introduction à Python 3]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[03 - Introduction aux variables]] →
