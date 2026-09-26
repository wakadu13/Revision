---
tags:
  - python
ordre: 6
---

# Donner de la classe au code

---

Dans cette section, nous allons parler des classes. Et de gâteau. Commençons par le gâteau. Lorsque nous avons un morceau de brownie devant nous, supposons, pour les besoins de la démonstration, que ce morceau de brownie est un `objet` du type alimentaire `Cake`. Notre morceau de gâteau a des propriétés que d'autres morceaux de gâteau pourraient ne pas avoir. L'une de ces propriétés pourrait être le glaçage qui, dans notre cas, pourrait être un glaçage au chocolat et une cerise. Nous devons nous demander comment ce morceau de gâteau a été produit et de quoi il est composé.

Les recettes de cuisine et les classes se ressemblent beaucoup car elles définissent la manière dont un plat - ou un objet - est produit. Un gâteau peut avoir une quantité fixe de farine et d'eau, mais laisser au chef le soin d'ajouter un glaçage au chocolat ou à la fraise. Une `classe` est une spécification de la manière dont un objet d'un certain type est produit. Le résultat de l'`instanciation` d'une telle `classe` est un objet de cette classe. Regardons un exemple :

#### La classe DreamCake

```python
class DreamCake:     # Measurements are defined in grams or units     eggs = 4     sugar = 300      milk = 200     butter = 50     flour = 250     baking_soda = 20     vanilla = 10      topping = None     garnish = None      is_baked = False      def __init__(self, topping='No topping', garnish='No garnish'):         self.topping = topping         self.garnish = garnish          def bake(self):         self.is_baked = True      def is_cake_ready(self):         return self.is_baked
```

De la même manière que les fonctions étaient définies à l'aide du mot-clé `def`, les classes sont définies à l'aide du mot-clé `class`, suivi du nom de la classe, en respectant la convention de nommage CapWords. CapWords signifie que tous les mots utilisés dans le nom commencent par une majuscule et sont collés ensemble, comme `CapWordsArePrettyCool`.

Viennent ensuite les ingrédients qui produisent un gâteau de base (et délicieux, soit dit en passant), qui ne changeront jamais dans cet exemple. Les variables `topping` et `garnish` sont définies sur `None` juste après. Cela suggère que des valeurs concrètes seront attribuées à ces variables plus tard, dans ce cas, à l'intérieur de la fonction `__init__` de la classe. Cette fonction est automatiquement appelée par Python dès qu'une nouvelle instance d'une classe est demandée. La fonction `__init__` est ce que l'on appelle une « méthode magique » (Magic Method). Nous ne couvrirons pas les méthodes magiques en détail, mais une note à leur sujet a été incluse dans la partie avancée facultative à la fin.

Pour en revenir à la classe, veuillez noter le paramètre `self` de la fonction `__init__`. Ce paramètre est le `premier paramètre obligatoire` de `toutes` les fonctions de classe. Pour faire court, les classes ont besoin d'un moyen de faire référence à leurs propres variables et fonctions. Python est conçu pour exiger un paramètre « `self` » en première position de la signature de la fonction. Nous pouvons ensuite faire référence à d'autres fonctions au sein des fonctions de la classe en appelant `self.other_func()` ou `self.topping`. Notez que nous n'avons pas besoin de lui fournir une valeur lors de l'appel de fonctions sur des objets de classe, malgré ce premier paramètre « self ». Nous verrons cela plus tard.

Une autre petite astuce à remarquer concerne les valeurs par défaut des paramètres de fonction. Celles-ci nous permettent d'omettre complètement la spécification d'une valeur pour un ou plusieurs des paramètres. Dans ce cas, les paramètres prendront alors leurs valeurs par défaut telles que spécifiées, et `topping` sera défini sur `'No topping'`, à moins d'être remplacé lorsque nous créons un objet.

Enfin, dans cet exemple, nous avons défini une fonction `à l'intérieur de la portée de la classe`, comme l'indique le niveau d'indentation. Cela signifie que la fonction `bake` est `uniquement` accessible au code depuis l'intérieur de la classe elle-même (par exemple, le code d'une fonction appelant une autre fonction) et aux objets instanciés à partir de la classe. Créons quelques objets d'exemple pour mieux illustrer ce comportement.

#### Un gâteau nature

Pour un gâteau nature, le glaçage et la garniture prennent par défaut les valeurs « No topping » et « No garnish », respectivement.

```python
plain_cake = DreamCake()
```

#### Un gâteau au chocolat

Pour un gâteau au chocolat, nous devons ajouter un glaçage au chocolat sur le dessus, mais pas de garniture (la valeur par défaut est `"No garnish"`).

```python
chocolate_cake = DreamCake(topping='Chocolate frosting')
```

#### Un gâteau de luxe

Nos gâteaux de luxe ont le glaçage et la garniture définis explicitement.

```python
luxury_strawberry_cake = DreamCake(topping='Strawberry frosting', garnish='Chocolate bits')
```

Cela peut, bien sûr, être également spécifié `sans` utiliser de paramètres nommés par souci de concision :

```python
luxury_strawberry_cake = DreamCake('Strawberry frosting', 'Chocolate bits')
```

Comme montré ci-dessus, les classes sont instanciées en objets de la même manière que nous appelons des fonctions : tapez le nom suivi de parenthèses avec d'éventuels paramètres spécifiés. Maintenant que nous avons des objets de la classe `DreamCake` stockés dans des variables, nous pouvons appeler les fonctions de la classe `sur` les variables d'objet en ajoutant un `.` et la fonction.

#### La cuisson du gâteau

```python
chocolate_cake = DreamCake(topping='Chocolate frosting')  chocolate_cake.bake()  # Call the function "bake" on the object. is_cake_done = chocolate_cake.is_cake_ready()  print(is_cake_done)  # Prints "True" because we called "bake" earlier
```

Voyez-vous l'appel de la fonction `bake()` sur `chocolate_cake` ? Même si la fonction `bake` au sein de la classe a un paramètre `self`, nous n'avons pas besoin de spécifier sa valeur. Nous n'entrerons pas dans les détails des décisions qui ont mené à cela, c'est simplement une chose à retenir. Pour conclure, il convient de mentionner que ce style de code est une petite partie de la [Programmation Orientée Objet (POO)](https://fr.wikipedia.org/wiki/Programmation_orient%C3%A9e_objet). La POO est bien plus que la simple utilisation de classes - assez pour un module entièrement distinct - mais dans ses formes les plus simples, nous définissons des classes, créons des objets (ou « instances ») de ces classes et les utilisons pour contenir des données ou appeler des fonctions.

---

## Notes avancées sur les classes

Si vous débutez en programmation, ne vous découragez pas si cela vous semble un peu trop compliqué. Ça l'est. Ce qui suit sont de très brèves notes sur des utilisations plus avancées des classes, dont nous n'avons généralement pas à nous soucier dans notre programmation quotidienne, mais qui sont plutôt intéressantes à connaître malgré tout.

Une chose que j'ai promis d'expliquer brièvement, ce sont les méthodes magiques (Magic Methods). Les méthodes magiques sont des fonctions - ou méthodes comme on les appelle aussi dans de nombreux langages de programmation - qui existent par défaut et ont une implémentation par défaut dans toutes les classes. Cela est dû à la `hiérarchie des classes` en Python, où toutes les classes héritent d'une classe de base `object` (« object » est le nom de la classe de base - ce qui est peut-être un peu déroutant).

Cette affirmation ouvre une grande boîte de la POO que nous n'explorerons pas, mais n'hésitez pas à faire vos propres recherches sur l'« héritage de classe en Python » et d'autres expressions similaires. En bref, l'« héritage de classe » signifie qu'une classe peut hériter du type, des fonctions et des variables internes d'une autre. Cette classe de base donne aux objets des fonctionnalités de base, par exemple, la capacité de se comparer les uns aux autres (un gâteau est-il identique à un autre ?) ou d'obtenir une `représentation sous forme de chaîne de caractères` de l'objet.

Disons que nous avons une classe `Circle`. L'objet lui-même est une donnée brute stockée en mémoire que seul Python sait lire, mais la `représentation sous forme de chaîne de caractères` d'un objet `Circle` pourrait être `"Circle(r=5)"`, décrivant par exemple un cercle avec un rayon de 5. La méthode magique responsable du renvoi d'une représentation de l'objet sous forme de chaîne de caractères est `__str__`. Appeler cette fonction sur un objet est similaire à appeler `str(...)` avec l'objet en paramètre. Par exemple, considérez l'extrait suivant de mon IDLE Python :

#### Redéfinir les méthodes magiques (IDLE)

```python
>>> class Circle: ...     def __init__(self, radius): ...         self.radius = radius ... ...     def __str__(self): ...         return f'Circle(r={self.radius})' ... >>> my_circle = Circle(5) >>> str(my_circle) 'Circle(r=5)'
```

Si nous n'avions pas redéfini la fonction `__str__`, le code fonctionnerait toujours, mais la sortie serait moins parlante :

```python
'<__main__.Circle object at 0x022FFB98>'
```

Cette chaîne représente un objet `Circle` à l'intérieur de `__main__` (ici, l'IDLE), situé à l'adresse mémoire `0x022FFB98`.

Deux autres méthodes magiques dignes d'être mentionnées sont les fonctions `__enter__` et `__exit__`, qui nous permettent de créer des classes compatibles avec le mot-clé `with`. Le mot-clé `with` nous permet de spécifier la fonctionnalité par défaut d'une classe pour les procédures d'initialisation et de nettoyage. Par exemple, la classe `C2TcpConnection` qui représente une connexion TCP à un serveur C2. L'étape d'initialisation pourrait inclure le démarrage d'un socket et la tentative d'authentification à partir d'entrées externes. L'étape de nettoyage pourrait inclure une gestion appropriée des erreurs et la garantie que le socket est correctement fermé après utilisation. C'est du code avancé mais amusant et « Pythonique » que je vous recommande d'explorer.

Considérons brièvement un exemple avant de passer à la section suivante du module.

#### Classe prenant en charge le gestionnaire de contexte `with`

```python
class Foo():      def __enter__(self):         print("Enter...")      def __exit__(self, type, value, traceback):         print("...and exit.")
```

Ici, une classe `Foo` est définie avec une simple fonction `__enter__` et `__exit__`, qui ne font rien d'autre qu'afficher un message. Cela nous permet d'utiliser la clause `with` pour « envelopper » ce supposé code répétitif réutilisé autour d'un code concret, par exemple :

        Python
`with Foo():     print("Hello world!")`

Ceci affiche le résultat suivant dans la console :

```bash
Enter... Hello world! ...and exit.
```

De plus, nous pouvons changer la clause `with` en quelque chose comme `with Foo() as foo`, ce qui nous permet de faire référence à l'objet instancié de `Foo` utilisé pour envelopper notre code. C'est utile si, par exemple, la classe `Foo` a des fonctions que nous voulons appeler depuis l'intérieur de la clause `with`, comme `get_connection_status` dans l'exemple de la création d'une classe `C2TcpConnection`. Une utilisation plus fréquente de la clause `with` est `with open('/path/to/file.txt', 'w') as wr`, qui ouvre un fichier en écriture. Nous pouvons alors utiliser `wr.write('something')` pour écrire « something » dans le fichier. À la fin de la clause `with`, nous n'avons pas besoin de fermer les flux de sortie vers le fichier - la fonctionnalité de nettoyage de la classe `open` s'en charge.
---

← [[05 - Définir des Fonctions]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[07 - Introduction aux bibliothèques]] →
