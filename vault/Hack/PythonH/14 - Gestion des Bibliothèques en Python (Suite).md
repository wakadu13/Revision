---
tags:
  - python
ordre: 14
---

# Gestion des Bibliothèques en Python (Suite)

---

À ce stade, nous avons utilisé plusieurs paquets dans nos projets et même installé des paquets tiers. Ces paquets existent physiquement à un emplacement prédéterminé afin que l'interpréteur Python puisse les localiser lorsque nous essayons de les importer ou d'importer des éléments qu'ils contiennent. L'emplacement par défaut est le répertoire `site-packages`. C'est le cas pour les systèmes Windows, cependant sur les systèmes Debian et dérivés de Debian tels que Kali, Parrot et Ubuntu, les bibliothèques externes se trouvent dans un emplacement `dist-packages`. Cependant, le principe est le même.

Les emplacements par défaut `site-packages`/`dist-packages` sont les suivants :

- Windows 10 : `PYTHON_INSTALL_DIR\Lib\site-packages` :

```cmd
C:\Program Files\Python38\Lib\site-packages
```

- Linux : `/usr/lib/PYTHON_VERSION/dist-packages/` :

```bash
/usr/lib/python3/dist-packages
```

La raison pour laquelle les paquets se trouvent dans un répertoire `dist-packages` plutôt que `site-packages` sur les systèmes basés sur Debian provient de la manière dont ces systèmes gèrent les paquets installés avec le gestionnaire de paquets (`apt`). Cependant, par souci de simplicité, nous utiliserons désormais le nom commun de `site-packages`. Si nous jetons un œil à l'intérieur de ce répertoire, nous verrons de nombreux paquets disponibles pour Python. Un paquet, dans toute sa simplicité, n'est qu'un dossier contenant au moins un fichier `__init__.py` et éventuellement (bien que presque toujours) d'autres fichiers python et des structures de dossiers imbriquées.

---

## Répertoires et Chemins de Recherche

Au lieu de produire un script entièrement fonctionnel pour le scraping de mots sur un site web, nous avons décidé d'écrire le script sous forme d'API. Nous pourrions empaqueter le script avec un fichier `__init__.py` (même vide, cela convient) et placer le paquet dans le répertoire `site-packages`. Python sait déjà qu'il doit vérifier cet emplacement lors de la recherche de paquets. Ce n'est pas toujours pratique. Cependant, nous pouvons indiquer à Python de chercher dans un répertoire différent avant de parcourir le répertoire `site-packages` en spécifiant la variable d'environnement `PYTHONPATH`. Comme nous pouvons le voir ci-dessous, sans avoir défini de variable d'environnement `PYTHONPATH`, le chemin de recherche n'inclut que les répertoires standards :

#### Inspection du Chemin de Recherche par Défaut

```bash
Hiterof13@htb[/htb]$ python3  Python 3.9.2 (default, Feb 28 2021, 17:03:44)  [GCC 10.2.1 20210110] on linux Type "help", "copyright", "credits" or "license" for more information. >>> import sys >>> sys.path ['', '/usr/lib/python39.zip', '/usr/lib/python3.9', '/usr/lib/python3.9/lib-dynload', '/usr/local/lib/python3.9/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.9/dist-packages']  >>>
```

Maintenant, spécifions une variable d'environnement `PYTHONPATH` et voyons comment elle affecte le chemin de recherche :

#### Inspection du chemin de recherche par défaut

```bash
Hiterof13@htb[/htb]$ PYTHONPATH=/tmp/ python3  Python 3.9.2 (default, Feb 28 2021, 17:03:44)  [GCC 10.2.1 20210110] on linux Type "help", "copyright", "credits" or "license" for more information. >>> import sys >>> sys.path ['', '/tmp/', '/usr/lib/python39.zip', '/usr/lib/python3.9', '/usr/lib/python3.9/lib-dynload', '/usr/local/lib/python3.9/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.9/dist-packages']  >>>
```

Comme nous avons défini `PYTHONPATH` sur le répertoire racine, celui-ci a été ajouté au début du chemin de recherche. Cela signifie deux choses : premièrement, les paquets qui existent à l'emplacement `/tmp/` peuvent maintenant être importés et utilisés dans le projet ou IDLE, et deuxièmement, cela signifie que nous pouvons détourner d'autres paquets, en modifiant leur comportement. Ce dernier point est un avantage si nous pouvons contrôler le `PYTHONPATH` d'un système pour y inclure notre paquet malveillant. Nous utiliserons principalement le chemin de recherche pour spécifier où trouver nos API dans les scénarios de développement quotidiens.

Supposons que nous voulions que les paquets soient installés dans un dossier spécifique. Par exemple, nous voulions conserver tous les paquets qui nous sont liés dans un répertoire `/var/www/packages/`. Dans ce cas, nous pouvons demander à pip d'installer le paquet et de stocker le contenu dans ce dossier avec l'option `--target`, comme ceci :

#### Installation de Modules Python à un Emplacement Cible

```bash
Hiterof13@htb[/htb]$ python3 -m pip install --target /var/www/packages/ requests  Collecting requests   Using cached requests-2.25.1-py2.py3-none-any.whl (61 kB) Collecting urllib3<1.27,>=1.21.1   Downloading urllib3-1.26.4-py2.py3-none-any.whl (153 kB)      |████████████████████████████████| 153 kB 8.1 MB/s ...SNIP...
```

---

## Environnements Virtuels

Jusqu'à présent, nous avons vu comment installer des paquets sur la machine locale, rendant les paquets disponibles pour tous les scripts de notre système. Si, pour une raison ou une autre, nous avons besoin d'utiliser une version spécifique d'un paquet pour un projet et une autre version du même paquet pour un autre projet, nous rencontrerons des problèmes. Une solution pour ce type d'isolation de projets est l'utilisation d'environnements virtuels (`virtual environments`), ou `venv` en abrégé. Le module `venv` nous permet de créer des environnements virtuels pour nos projets, composés d'une structure de dossiers pour l'environnement du projet lui-même, d'une copie du binaire Python et de fichiers pour configurer notre shell afin qu'il fonctionne avec cet environnement spécifique. Jetons un œil à quelques exemples.

Tout d'abord, nous allons créer un environnement virtuel appelé `academy`.

#### Préparation de l'Environnement Virtuel

```bash
Hiterof13@htb[/htb]$ python3 -m venv academy
```

Ensuite, nous pouvons sourcer le script `activate` situé dans `academy/bin/`. Cela configure notre shell en définissant les variables d'environnement nécessaires afin que lorsque nous exécutons, par exemple, `pip install requests`, nous utilisions le binaire Python qui a été copié lors de la création de l'environnement virtuel, comme ceci :

#### Sourcer le venv et installer un paquet

```bash
Fugl@htb[/htb]$ source academy/bin/activate (academy) Fugl@htb[/htb]$ pip install requests  Collecting requests   Using cached requests-2.25.1-py2.py3-none-any.whl (61 kB) Collecting idna<3,>=2.5 ...SNIP... Successfully installed certifi-2020.12.5 chardet-4.0.0 idna-2.10 requests-2.25.1 urllib3-1.26.4
```

Remarquez le préfixe `(academy)` après avoir sourcé le script `activate`. Cela indique que notre terminal est configuré pour exécuter des commandes pour cet environnement virtuel particulier.

Pour les tests d'intrusion (`penetration testing`), il peut être conseillé d'utiliser des environnements virtuels afin que les projets et les paquets qui leur sont associés soient maintenus séparés. Cela garantira qu'un projet dont nous savons qu'il fonctionne en l'état ne se cassera pas à l'avenir parce que, par exemple, un paquet externe a été mis à jour en travaillant sur un autre projet.

---

## En Conclusion

Il existe de nombreuses façons d'atteindre le même objectif. Nous en avons examiné quelques-unes, et elles nous mèneront très loin ; cependant, il existe de meilleurs outils et solutions pour des projets plus importants ou plus permanents. Imaginons que nous ayons développé un `C2` (`Command & Control` ou Commande et Contrôle) personnalisé en Python et que nous ayons besoin d'un environnement fiable et séparé pour héberger le serveur. Les environnements virtuels fonctionneront probablement bien, mais une alternative est d'utiliser un logiciel de conteneurisation tel que `Docker` ou même une Machine Virtuelle entièrement isolée. Pour les projets logiciels plus importants en Python, les environnements virtuels peuvent être satisfaisants pour une partie du chemin. De plus, les logiciels de gestion de paquets et d'environnements tels que [Conda](https://docs.conda.io/en/latest/) permettront un meilleur contrôle du projet, surtout en cas de collaboration avec d'autres. Ces technologies et méthodologies méritent leurs propres modules.

---

## Exercices

Pour les exercices de cette section, veuillez trouver ci-dessous les blocs de code pertinents.

#### Question 1

```python
foo = set()  for i in range(42):     foo.add('Cake')  foo.add('Hello') foo.add('World')
```

#### Question 2

```python
x_coordinate = (42,)
```

---

← [[13 - Un simple shell de liaison]] | [[00 - Sommaire Introduction to Python 3|Sommaire]]
