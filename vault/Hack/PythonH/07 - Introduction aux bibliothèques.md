---
tags:
  - python
ordre: 7
---

# Introduction aux bibliothèques

---

Nous avons vu comment créer des classes et des fonctions, des fonctions au sein de classes et d'autres concepts simples. Tout cela se trouvait dans un seul fichier Python, également appelé `un module`, mais il serait formidable de pouvoir partager le code de ce module avec d'autres personnes ou de le réutiliser dans d'autres projets. Il serait également formidable de réutiliser du code que d'autres personnes ont créé pour nous, par exemple, du code qui nous permet de communiquer avec des serveurs web ou même quelque chose d'aussi simple que d'obtenir la date actuelle. C'est là qu'interviennent les bibliothèques.

Une `bibliothèque` (library) en programmation est à bien des égards similaire à une bibliothèque dans la vie réelle. C'est une collection de connaissances que nous pouvons emprunter dans nos projets sans avoir à réinventer la roue. Une fois que nous `importons` une bibliothèque, nous pouvons utiliser tout ce qu'elle contient, y compris des fonctions et des classes. Certaines bibliothèques sont fournies avec Python, par exemple, `datetime`, qui nous permet d'obtenir un objet représentant la date et l'heure locales actuelles.

Voyons quelles classes et fonctions la bibliothèque `datetime` contient. Pour cela, nous utiliserons la fonction intégrée appelée [dir()](https://docs.python.org/3/library/functions.html#dir).

#### Dir(datetime)

```python
>>> import datetime >>> dir(datetime) ['MAXYEAR', 'MINYEAR', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'date', 'datetime', 'datetime_CAPI', 'sys', 'time', 'timedelta', 'timezone', 'tzinfo']
```

#### La bibliothèque datetime

```python
import datetime  now = datetime.datetime.now() print(now)  # Prints: 2021-03-11 17:03:48.937590
```

Comme nous le voyons, nous devons appeler `datetime.datetime.now()` pour obtenir l'horodatage (timestamp) actuel. Nous importons la bibliothèque, ou `module`, `datetime`, qui devient alors disponible pour être référencée par son nom. Ce module s'appelle également `datetime` et contient une fonction `now()`. Donc, pour atteindre la fonction `now()`, nous devons d'abord référencer le module, puis la classe, et enfin la fonction, tous « enchaînés » les uns aux autres avec des points.

Cela peut devenir fastidieux et alourdir le code, alors examinons d'autres manières d'importer :

#### Importer une classe depuis une bibliothèque

```python
from datetime import datetime  print(datetime.now())
```

#### Lui donner un nouveau nom

```python
from datetime import datetime as dt  print(dt.now())
```

L'exemple ci-dessus contient deux sauts de ligne entre l'instruction d'importation et le code. C'est parce que le guide de style (style guide) PEP-8, les directives de Python pour un code Python « correct », incite les développeurs à ajouter deux sauts de ligne entre les instructions d'importation et le code lui-même. Il suggère également d'utiliser la convention CapWords pour les noms de classes, mais note un guide de style distinct pour les noms intégrés. Consultez [https://www.python.org/dev/peps/pep-0008/#class-names](https://www.python.org/dev/peps/pep-0008/#class-names) pour plus d'informations. C'est pourquoi les classes telles que `datetime` sont en minuscules.

Prochaine étape, nous allons voir plus en détail comment installer et gérer les bibliothèques externes en Python.
---

← [[06 - Donner de la classe au code]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[08 - Gérer les bibliothèques en Python]] →
