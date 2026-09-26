---
tags:
  - python
ordre: 5
---

# Définir des Fonctions

---

Jusqu'à présent, nous avons examiné des techniques courantes pour contrôler le flux d'exécution du code, ce qui nous a permis de créer des outils simples, par exemple, des compteurs ou même un simple enrichisseur de listes de mots. Par exemple : pour chaque mot de la liste de mots, initialiser le compteur à 0, tant que le compteur est inférieur à 100, afficher le mot et le compteur, et incrémenter le compteur de 1. À titre de référence, cela pourrait ressembler à ceci :

#### Exemple de Générateur de Mots de Passe

```python
wordlist = ['password', 'john', 'qwerty', 'admin']  for word in wordlist:     counter = 0     while counter < 100:         print(f'{word}{counter}')         counter = counter + 1
```

Dans ce cas, la boucle for se répète jusqu'à ce qu'elle ait traité toutes les entrées de la liste. Comme nous l'avons vu, même avec des briques de base simples, nous pouvons accomplir beaucoup de choses. Parlons de la brique de base importante suivante en développement logiciel : les `Fonctions`

---

## Fonctions

Les fonctions nous permettent de définir des blocs de code qui effectuent une série d'actions, produisent une série de valeurs, et retournent optionnellement une ou plusieurs de ces valeurs. Comme en mathématiques, où `f(x)` est une `fonction f de x` et produit le même résultat lorsqu'on lui donne la même entrée. Par exemple `f(x) = x + 1` est une fonction `f` de `x` qui retourne `x + 1`. Ainsi `f(2)` serait `3`, car `f(2) = 2 + 1` ce qui est `3`.

De même, en Python, nous pouvons définir et appeler des fonctions pour réutiliser du code et travailler avec nos données plus efficacement - car nous n'avons pas besoin de réinventer la roue en permanence. Nous pouvons définir des fonctions en Python dans leur forme la plus simple très facilement.

Voici un exemple de définition de `f(x) = 2 * x + 5` en tant que fonction en Python :

#### Première Fonction

```python
def f(x):     return 2 * x + 5
```

Outre la syntaxe (essentielle) avec l'indentation au niveau de la `portée interne` de la fonction - le code à l'intérieur de la fonction - ce qu'il est important de noter ici sont les mots-clés `def` et `return`. Le mot-clé `def` est la manière dont nous définissons les fonctions en Python. Après `def` vient le nom de la fonction (écrit en snake_case), les paramètres d'entrée entre parenthèses, et un deux-points. Cette première ligne d'une fonction est appelée la `signature` de la fonction. Après avoir écrit quelques fonctions différentes, nous pouvons les distinguer simplement en regardant leurs noms et les arguments qu'elles acceptent. Nous pouvons les différencier en comparant leurs signatures de fonction.

Créons une fonction pour calculer et retourner la valeur d'un nombre élevé à la puissance d'un autre :

#### Fonction Power_Of

```python
def power_of(x, exponent):     return x ** exponent
```

En Python, les symboles `**` signifient « puissance de ». Si nous appelons `power_of(4, 2)`, nous obtiendrons quatre à la puissance deux ou simplement quatre au carré. Maintenant, où ce résultat finit-il ? Il finira dans l'un des deux endroits, selon ce que nous faisons : 1) le vide absolu du néant, 2) une variable. Considérez cet exemple :

#### Appel de Fonction

        Python
`def power_of(x, exponent):     return x ** exponent  power_of(4, 2)          # La fonction a été exécutée, mais rien n'a récupéré la valeur de retour. eight = power_of(2, 3)  # La variable "eight" est maintenant égale à deux à la puissance trois.`

Alors, la première forme est-elle inutile ? Non. Comme pour l'entrée/sortie d'un terminal, nous pouvons « rediriger » la sortie de la fonction vers l'« entrée » d'une autre. Nous pouvons utiliser le résultat de l'appel d'une fonction comme entrée pour une autre. Par exemple :

```python
print('My favourite number is:') print(power_of(4, 2))
```

Ici, nous appelons la fonction `print` et lui donnons d'abord une chaîne de caractères en entrée, puis nous lui donnons `le résultat` d'un autre appel de fonction. Au moment de l'exécution (`runtime`), pendant l'exécution réelle du script, Python exécutera d'abord la première ligne, puis passera à la 2ème ligne et exécutera les commandes de l'intérieur vers l'extérieur. En d'autres termes, il commencera par calculer `power_of(4, 2)` puis utilisera ce résultat comme entrée pour la fonction `print`.

Imaginez que nous devions appeler une fonction avec dix paramètres. Devoir se souvenir de chaque paramètre est difficile une fois que le nombre de paramètres dépasse deux. C'est pourquoi, en plus de ces paramètres `positionnels`, Python prend en charge ce que l'on appelle les `paramètres nommés`. Alors que les paramètres positionnels nous obligent à toujours insérer les paramètres dans le bon ordre, les paramètres nommés nous permettent d'utiliser l'ordre que nous préférons. Cependant, ils nous obligent à spécifier explicitement quelle valeur va à quel paramètre. L'utilisation de paramètres nommés peut sembler ridicule, mais après une semaine ou un mois à regarder autre chose, cela peut être une bénédiction d'avoir spécifié expressément, par les noms des paramètres, qui est qui. Regardons un exemple. Considérez la fonction ci-dessous, qui est un modèle d'invitation à un événement scolaire.

#### Invitation.py

```python
def print_sample_invitation(mother, father, child, teacher, event):      # Remarquez ici l'utilisation d'une chaîne de formatage multiligne : f''' texte ici '''     sample_text = f''' Dear {mother} and {father}. {teacher} and I would love to see you both as well as {child} at our {event} tomorrow evening.   Best regards, Principal G. Sturgis. '''     print(sample_text)  print_sample_invitation()
```

Si nous nous contentions de remplir les blancs, il y a de fortes chances que nous oubliions qui est qui en quelques minutes, plutôt qu'en quelques semaines. Note : le code ci-dessus produira une erreur car nous ne fournissons aucun argument pour la fonction `print_sample_invitation`.

Ce que nous pouvons faire à la place, c'est de spécifier exactement qui est qui, comme ceci :

```python
print_sample_invitation(mother='Karen', father='John', child='Noah', teacher='Tina', event='Pizza Party')
```

Spécifier les noms dans la fonction modifiera notre script comme suit :

#### Invitation.py - Modifié

```python
# Définition de la fonction def print_sample_invitation(mother, father, child, teacher, event):      # Remarquez ici l'utilisation d'une chaîne de formatage multiligne : f''' texte ici '''     sample_text = f''' Dear {mother} and {father}. {teacher} and I would love to see you both as well as {child} at our {event} tomorrow evening.   Best regards, Principal G. Sturgis. '''     # Afficher la sortie     print(sample_text)  # Appeler la fonction print_sample_invitation(mother='Karen', father='John', child='Noah', teacher='Tina', event='Pizza Party')
```

Cela produira la sortie suivante :

#### Invitation.py - Exécution

```bash
Hiterof13@htb[/htb]$ python3 invitation.py  Dear Karen and John. Tina and I would love to see you both as well as Noah at our Pizza Party tomorrow evening.  Best regards, Principal G. Sturgis.
```

Encore une fois, les scripts Python sont exécutés de haut en bas, donc gardez toujours à l'esprit que Python doit connaître les fonctions et les variables avant qu'elles ne soient référencées. Gardez également à l'esprit les portées du code. Les portées nous permettent de référencer des variables et des fonctions `à l'extérieur` de notre portée actuelle (par exemple, le code dans les fonctions peut utiliser des variables et la portée globale), mais pas `à l'intérieur` de celle-ci. En d'autres termes, nous ne pouvons pas réutiliser une variable que nous avons définie à l'intérieur d'une fonction, à l'extérieur de celle-ci. En dehors de cela, Python est livré avec de nombreuses [Fonctions Intégrées](https://docs.python.org/3/library/functions.html).

Maintenant que nous connaissons les bases de la définition et de l'utilisation des fonctions, ajoutons d'autres briques de base à notre arsenal d'outils de codage : les `Classes`
---

← [[04 - Instructions conditionnelles et boucles]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[06 - Donner de la classe au code]] →
