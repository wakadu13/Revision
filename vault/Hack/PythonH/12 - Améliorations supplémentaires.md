---
tags:
  - python
ordre: 12
---

# Améliorations supplémentaires

---

Rappelez-vous ce dont nous avons discuté au début à propos de l'importation de modules et du fait que les scripts Python sont exécutés de haut en bas, même lorsqu'ils sont importés. Cela signifie que si quelqu'un importait notre script, par exemple, pour réutiliser certaines de nos fonctions (cela pourrait être nous-mêmes), le code s'exécuterait dès son importation. La manière habituelle d'éviter cela est de placer tout le code qui `fait quelque chose` dans le bloc "main". Faisons-le :

#### Le bloc "main"

```python
if __name__ == '__main__':     page_url = 'http://target:port'     the_words = get_all_words_from(page_url)     top_words = get_top_words_from(the_words)      for i in range(10):         print(top_words[i][0])
```

La chose la plus importante à savoir sur l'instruction conditionnelle est ce que nous devons taper pour que le code à l'intérieur s'exécute chaque fois que nous l'exécutons avec le binaire Python. Veuillez vous référer à la brillante réponse sur [StackOverflow](https://stackoverflow.com/a/419185) pour une explication approfondie de ce qui se passe ici. Le point essentiel à retenir est que le code à l'intérieur de cette instruction conditionnelle ne s'exécute que lorsque le script est `exécuté` (`run`), et non `importé` (`imported`).

Cependant, nous pouvons supprimer la constante `PAGE_URL`, sur laquelle nous nous appuyions auparavant, et tout placer à l'intérieur du bloc main du code.

Une autre amélioration que nous pouvons apporter est de nous débarrasser complètement de la variable URL en rendant le script flexible et en acceptant un argument d'entrée lors de l'exécution de Python et du script. Par exemple, nous pourrions améliorer le programme pour accepter des arguments d'entrée du type `python3 wordextractor.py http://foo.bar/baz` ou, mieux encore, préparer le script à accepter des paramètres nommés dans un ordre arbitraire, par exemple :

#### Accepter des arguments

```bash
Hiterof13@htb[/htb]$ python3 wordextractor.py --url http://foo.bar/baz
```

Cela nous permettrait d'étendre facilement le programme avec, par exemple, une limite de longueur de mot, afin d'éviter les mots inintéressants comme `and`, `is` et `that`.

Examinons un module pour nous aider à réaliser cela : [click](https://click.palletsprojects.com/).

Pour comprendre ce que fait `click`, nous devons parler de `décorateurs` (`decorators`). Cependant, comme c'est un peu complexe à aborder directement, laissons cela en lecture optionnelle à la fin de cette section. Tout ce que nous devons savoir sur `click` à ce stade, ce sont quelques concepts simples spécifiques à click qui sont faciles à mémoriser. Commençons par l'installer comme toujours en utilisant pip : `pip3 install click`. Ce qui suit est un exemple de script de la documentation officielle, mais légèrement modifié pour plus de simplicité :

#### Un script Click simple

```python
import click  @click.command() @click.option('--count', default=1, help='Number of greetings.') @click.option('--name', prompt='Your name', help='The person to greet.') def hello(count, name):     for i in range(count):         click.echo('Hello %s!' % name)  if __name__ == '__main__':     hello()
```

Beaucoup de nouvelles choses se sont produites ici en relativement peu de lignes de code. Tout d'abord, il y a les `décorateurs` qui, en un sens, « décorent les fonctions ». Ce sont les éléments de la définition de la fonction qui commencent par un `@`. Nous devons nous concentrer sur le fait de ne pas devenir trop technique trop rapidement, car ces décorateurs dans `click` nous permettent de configurer des arguments de ligne de commande pour le script. D'abord, nous spécifions le décorateur `@click.command()`, indiquant que nous aurons une entrée en ligne de commande pour cette fonction `hello`. Ensuite, deux options `@click.option` sont spécifiées. Dans cet exemple, les paramètres sont assez simples : nous avons une valeur `default` pour le compteur, au cas où cela ne serait pas spécifié comme argument de ligne de commande, nous avons un texte d'aide (`help`) pour la sortie `--help`, et nous avons un paramètre `prompt`. Cela indique à Python de demander (`prompt`) une entrée à l'utilisateur si aucun argument de ligne de commande n'est fourni.

Enfin, et c'est probablement le plus important, remarquez que tout ce que fait la « partie principale » du code est d'appeler la fonction `hello()`. Click exige que nous appelions une fonction avec ces décorateurs spécifiés pour fonctionner. Notez également que les noms des paramètres de la fonction `hello` et les noms des arguments d'entrée `--count` et `--name` correspondent si nous ignorons les `--`.

Examinons quelques exemples pour mieux illustrer les choses. D'abord, une exécution simple sans aucun argument. Ici, on nous demande une entrée pour le paramètre `--name` :

#### Jouer avec Click

```cmd
C:\Users\Birb> python click_test.py  Your name: Birb Hello Birb!
```

Nous pouvons également le spécifier explicitement :

```cmd
C:\Users\Birb> python click_test.py --name Birb  Hello Birb!
```

De plus, le paramètre `--count` peut être défini explicitement au lieu de sa valeur par défaut de 1 :

```cmd
C:\Users\Birb> python click_test.py --name Birb --count 3  Hello Birb! Hello Birb! Hello Birb!
```

Enfin, voici la sortie de `--help` :

```cmd
C:\Users\Birb> python click_test.py --help  Usage: click_test.py [OPTIONS]  Options:   --count INTEGER  Number of greetings.   --name TEXT      The person to greet.   --help           Show this message and exit.
```

Comme nous pouvons le voir dans le message d'aide, `INTEGER` et `TEXT` sont affichés. Cependant, nous n'avons jamais spécifié cela dans le code. La raison est que `click` tentera de `deviner le type correct` en se basant sur des éléments comme le paramètre `default`. Pour plus d'informations, veuillez vous référer à la documentation (relativement bien écrite).

En préparation de l'utilisation de `click`, nous allons déplacer tout le code qui se trouvait auparavant dans la « partie principale » du script dans sa propre nouvelle fonction `main()`. Le nom de cette nouvelle fonction n'est pas essentiel tant que la fonction est appelée.

#### Refactorisation en une fonction distincte

```python
def main():     page_url = 'http://target:port'     the_words = get_all_words_from(page_url)     top_words = get_top_words_from(the_words)      for i in range(10):         print(top_words[i][0])  if __name__ == '__main__':     main()
```

Nous devons ensuite ajouter la fonctionnalité click à la fonction, ainsi que remplacer les variables si nécessaire :

#### Ajout d'options Click

```python
@click.command() @click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.') @click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).') def main(url, length):     the_words = get_all_words_from(url)     top_words = get_top_words_from(the_words, length)     # Remaining code omitted
```

Comme on peut le voir, nous avons ajouté deux paramètres à la fonction, `url` et `length`, et les avons utilisés à la place de l'URL codée en dur que nous utilisions auparavant. Les noms des paramètres doivent être les mêmes que le `--name` dans la spécification de l'option pour que click mappe automatiquement l'entrée à ces variables. Si nous devions utiliser un argument d'entrée (c'est-à-dire un `click.option`) qui devait être différent du nom du paramètre en Python - par exemple, pour des raisons esthétiques - nous pourrions dire à `click` de mapper les variables en ajoutant le nom du paramètre Python après les noms d'option de l'argument, par exemple, `@click.option('--url', '-u', 'target_uri', ...)`.

Dans ce cas, nous pouvons laisser la fonction `count_occurrences_in` s'occuper du filtrage. Pour ce faire, nous devons d'abord passer la variable de longueur à la fonction `get_top_words_from`, et à l'intérieur de celle-ci, la transmettre à la fonction `count_occurrences_in`. Il y a plusieurs façons de faire cela. Si nous devions ajouter une autre option de filtrage, par exemple, ne trouver que les mots qui correspondent à une expression régulière, il pourrait être judicieux de garder le filtrage comme un processus distinct qui peut appliquer un filtre sur une liste de mots et retourner ceux qui correspondent. Les deux fonctions suivantes ont été mises à jour :

```python
def count_occurrences_in(word_list, min_length):     word_count = {}      for word in word_list:         if len(word) < min_length:             continue         if word not in word_count:             word_count[word] = 1         else:             current_count = word_count.get(word)             word_count[word] = current_count + 1     return word_count  def get_top_words_from(all_words, min_length):     occurrences = count_occurrences_in(all_words, min_length)     return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)
```

En partant du bas, nous passons le paramètre `min_length` à la première fonction. Ici, nous ajoutons une vérification supplémentaire : `if len(word) < min_length`. Si c'est le cas, nous utilisons `continue`, ce qui, dans le contexte d'une boucle, signifie « ne vous souciez pas du reste de ce bloc, passez simplement à l'élément suivant et oubliez celui-ci ». Ainsi, si le mot est plus court que notre longueur minimale, nous passerons (`continue`) au mot suivant et ne l'ajouterons donc _pas_ au dictionnaire `word_count`.

Le script final ressemble à ceci :

#### Le script final

```python
import click import requests import re from bs4 import BeautifulSoup  def get_html_of(url):     resp = requests.get(url)      if resp.status_code != 200:         print(f'HTTP status code of {resp.status_code} returned, but 200 was expected. Exiting...')         exit(1)      return resp.content.decode()  def count_occurrences_in(word_list, min_length):     word_count = {}      for word in word_list:         if len(word) < min_length:             continue         if word not in word_count:             word_count[word] = 1         else:             current_count = word_count.get(word)             word_count[word] = current_count + 1     return word_count  def get_all_words_from(url):     html = get_html_of(url)     soup = BeautifulSoup(html, 'html.parser')     raw_text = soup.get_text()     return re.findall(r'\w+', raw_text)  def get_top_words_from(all_words, min_length):     occurrences = count_occurrences_in(all_words, min_length)     return sorted(occurrences.items(), key=lambda item: item[1], reverse=True)  @click.command() @click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.') @click.option('--length', '-l', default=0, help='Minimum word length (default: 0, no limit).') def main(url, length):     the_words = get_all_words_from(url)     top_words = get_top_words_from(the_words, length)      for i in range(10):         print(top_words[i][0])  if __name__ == '__main__':     main()
```

Pour l'étudiant plus audacieux, voici une liste d'idées pour étendre davantage l'outil :

- Ajouter un argument `--output` / `-o` qui nous permet de définir un fichier de sortie pour l'affichage au lieu de la console (quelque chose comme `with open('path.txt', 'w') as wr:` et `wr.write(word)`).
- Ajouter des mutations de mot de passe courantes à la sortie, par exemple, avec une majuscule, en minuscules, en MAJUSCULES, et avec divers éléments ajoutés comme l'année en cours et les années récentes, des nombres ou des symboles aléatoires, par exemple, 2019, 1!, 2!, 3!, 01, 123. `Summer2021!` et des variations similaires sont des mots de passe d'une fréquence déprimante.
- Ajouter un argument `--depth` / `-d` spécifiant la _profondeur d'exploration_ (`crawl depth`) du script. Cela implique la capacité de récupérer non seulement des mots mais aussi des URL sur la ou les pages web, de vérifier s'ils sont dans le périmètre défini (par exemple, le domaine), et de les ajouter à une liste de pages à explorer ensuite.
- Le programme plante actuellement si une longueur minimale de 10 ou plus est spécifiée. Essayez de comprendre pourquoi et de le corriger (indice : jetez un œil à cette dernière boucle for).
---

← [[11 - Amélioration continue du code]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[13 - Un simple shell de liaison]] →
