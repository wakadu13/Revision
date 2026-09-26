---
tags:
  - python
ordre: 8
---

# Gérer les bibliothèques en Python

---

La manière la plus populaire d'installer des paquets externes en Python est d'utiliser [pip](https://pip.pypa.io/en/stable/). Selon son auteur, `pip` est l'abréviation de ["pip installs packages"](https://ianbicking.org/blog/2008/10/pyinstall-is-dead-long-live-pip.html), une abréviation récursive (ce qui signifie que la définition fait référence à l'abréviation, et donc tourne en rond). Très drôle, en effet. Quoi qu'il en soit, `pip` est le nom du module Python qui gère les paquets Python externes. Avec `pip`, nous pouvons installer, désinstaller et mettre à jour les paquets Python. Contrairement au téléchargement et à l'installation de plugins pour un navigateur ou un éditeur de texte, il n'est pas courant de « faire son marché » (go shopping) de paquets Python.

La programmation consiste à utiliser le bon outil pour la bonne tâche, alors ne vous souciez pas de trouver des paquets à installer. La bonne approche, et probablement aussi la plus courante, est de chercher `comment faire quelque chose` et d'obtenir des recommandations de paquets en cours de route. La documentation de ces paquets - leurs sites web la plupart du temps - montrera généralement des exemples d'installation du paquet pour les nouveaux utilisateurs. Voyons également comment gérer les paquets.

Quelques arguments utiles pour `pip` que nous allons examiner sont `install` et le drapeau (flag) `--upgrade`, `uninstall` et `freeze`. L'argument `install` permet aux utilisateurs d'installer de nouveaux paquets ou de mettre à jour des paquets existants vers la dernière version (si le paramètre `--upgrade` est fourni). L'argument `uninstall`, comme son nom l'indique, supprimera le paquet du système. Étonnamment, la commande `freeze` n'a rien à voir avec le fait d'arrêter quoi que ce soit ou avec les films policiers ringards. Ceci affiche une liste de tous les paquets installés (via pip) et de leurs dépendances. Nous pouvons appeler les commandes soit en utilisant `pip` directement, soit en tant que module Python. Vous trouverez ci-dessous quelques exemples de ce à quoi cela pourrait ressembler.

#### Installer « flask » avec Pip

```bash
Hiterof13@htb[/htb]$ # Syntax: python3 -m pip install [package]

Hiterof13@htb[/htb]$ python3 -m pip install flask  Collecting flask   Using cached Flask-1.1.2-py2.py3-none-any.whl (94 kB) Collecting Werkzeug>=0.15   Using cached Werkzeug-1.0.1-py2.py3-none-any.whl (298 kB) Collecting itsdangerous>=0.24   Using cached itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB) Collecting click>=5.1   Using cached click-7.1.2-py2.py3-none-any.whl (82 kB) Collecting Jinja2>=2.10.1   Downloading Jinja2-2.11.3-py2.py3-none-any.whl (125 kB)      |████████████████████████████████| 125 kB 7.0 MB/s  Collecting MarkupSafe>=0.23   Downloading MarkupSafe-1.1.1-cp39-cp39-macosx_10_9_x86_64.whl (16 kB) Installing collected packages: Werkzeug, itsdangerous, click, MarkupSafe, Jinja2, flask Successfully installed Jinja2-2.11.3 MarkupSafe-1.1.1 Werkzeug-1.0.1 click-7.1.2 flask-1.1.2 itsdangerous-1.1.0
```

Comme on peut le voir, bien que nous n'ayons demandé que l'installation de `flask`, un excellent paquet pour exécuter des serveurs web basés sur Python (tout comme `bottle` - pareil, mais différent), nous obtenons également une multitude d'autres paquets, qui sont tous des prérequis de `flask`. Nous pourrions essayer de le mettre à jour, mais on nous dit déjà que nous exécutons la dernière version.

#### Mettre à jour les paquets

```bash
Hiterof13@htb[/htb]$ python3 -m pip install --upgrade flask  Requirement already up-to-date: flask in /usr/local/lib/python3.9/site-packages (1.1.2) Requirement already satisfied, skipping upgrade: itsdangerous>=0.24 in /usr/local/lib/python3.9/site-packages (from flask) (1.1.0) Requirement already satisfied, skipping upg... <SNIP>
```

Si nous voulions désinstaller un paquet particulier, nous pourrions le faire en appelant :

#### Désinstaller les paquets

```bash
Hiterof13@htb[/htb]$ pip uninstall [package]
```

Voyons ce qui est actuellement installé en exécutant `pip` avec l'argument `freeze`. Comme certains d'entre eux sont des dépendances de `flask`, nous laisserons la désinstallation elle-même en « bonus ». Veuillez noter que si nous choisissons de désinstaller un paquet de dépendance, le paquet principal ne fonctionnera probablement pas. Notez également que `freeze` peut produire des résultats différents d'une machine à l'autre et d'une version de Python à l'autre.

#### Lister les paquets installés

```bash
Hiterof13@htb[/htb]$ # Syntax: python3 -m pip freeze [package]

Hiterof13@htb[/htb]$ python3 -m pip freeze  click==7.1.2 Flask==1.1.2 itsdangerous==1.1.0 Jinja2==2.11.3 MarkupSafe==1.1.1 protobuf==3.13.0 pynput==1.7.3 pyobjc-core==7.1 pyobjc-framework-Cocoa==7.1 pyobjc-framework-Quartz==7.1 six==1.15.0 Werkzeug==1.0.1
```

Il serait pratique de donner cette liste de paquets installés à une autre personne pour qu'elle puisse utiliser nos scripts ou aider au développement. De cette façon, elle saura quels paquets doivent être installés (et même quelles versions).

Il se trouve que `pip` prend en charge la maintenance des paquets à partir d'un fichier de prérequis (requirements file). Ce fichier, souvent appelé littéralement `requirements.txt`, contient une liste de tous les paquets requis nécessaires pour exécuter le script avec succès. Le format est assez simple. Nous pourrions copier la sortie de `freeze` ci-dessus et l'enregistrer en tant que fichier de prérequis. Cependant, c'est un peu lourd, et nous n'avons pas besoin de connaître ou même de lister les dépendances des paquets dont nous avons besoin.

Pour l'exemple, supposons que nous souhaitions utiliser `flask` et `click` (nous reviendrons sur `click` plus tard). Si nous ne connaissons pas les versions requises ou si cela nous est égal, nous pourrions lister les paquets les uns après les autres et les enregistrer, comme ceci :

#### Exemple de requirements.txt

```bash
Hiterof13@htb[/htb]$ cat requirements.txt  flask click
```

Ensuite, pour installer tous les paquets du fichier de prérequis, nous taperions :

#### Installer depuis requirements.txt

```bash
Hiterof13@htb[/htb]$ python3 -m pip install -r requirements.txt
```

Ceci parcourra alors chacun des prérequis et les installera en sélectionnant la dernière version disponible et autorisée. Disons que nous voulions explicitement la version 1.1.2 de `flask`. Tout ce que nous aurions à faire serait de remplacer `flask` par `flask==1.1.2` dans le fichier de prérequis, tout comme dans la sortie de la commande `pip freeze`. Vous trouverez ci-dessous une liste d'opérateurs de comparaison de version courants que nous sommes très susceptibles de rencontrer dans des projets Python plus importants (pour en savoir plus, consultez la [PEP 440](https://www.python.org/dev/peps/pep-0440/#version-specifiers)).

|**Opérateur de comparaison**|**Description**|
|---|---|
|`==`|Clause de correspondance de version|
|`<=` / `>=`|Clause de comparaison ordonnée inclusive|
|`<` / `>`|Clause de comparaison ordonnée exclusive|

Ils nous permettent de spécifier, dans le fichier de prérequis, nos exigences exactes en matière de versions. Par exemple, si nous savons qu'un paquet `xyz` est vulnérable à une exploitation dans les versions 1.0.4 et inférieures, nous pouvons spécifier dans notre fichier de prérequis que nous avons besoin de `xyz>=1.0.5`. Il est également assez courant que de nouvelles mises à jour d'un paquet cassent le code existant (par exemple, les paquets qui dépendent d'autres systèmes tiers comme l'API de bot Discord pour Python). Dans ces cas, nous pouvons forcer une version plus ancienne d'un paquet avec l'opérateur `<` ou `<=`, pendant que les modifications nécessaires sont en cours.

Pour ne pas trop approfondir le sujet dès le début, nous reviendrons sur ce point plus tard dans le module. Pour l'instant, passons aux prérequis pour notre premier projet.
---

← [[07 - Introduction aux bibliothèques]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[09 - L'importance des bibliothèques]] →
