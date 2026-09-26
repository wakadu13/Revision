---
tags:
  - linux
ordre: 4
---

# Description de l'invite

L'invite de commande bash est simple à comprendre. Par défaut, elle affiche des informations telles que votre nom d'utilisateur (qui vous êtes), le nom de votre ordinateur (nom d'hôte), et le dossier/répertoire dans lequel vous travaillez actuellement. C'est une ligne de texte qui apparaît à l'écran pour vous informer que le système est prêt à recevoir vos instructions. L'invite apparaît sur une nouvelle ligne, et le curseur (la ligne ou le bloc clignotant) est placé juste après, attendant que vous saisissiez une commande.

Elle peut être personnalisée pour fournir des informations utiles à l'utilisateur. Le format peut ressembler à ceci :

```bash
<username>@<hostname><current working directory>$
```

Le répertoire personnel d'un utilisateur est marqué par un tilde <`~`> et constitue le dossier par défaut lorsque nous nous connectons.

```bash
<username>@<hostname>[~]$
```

Le symbole dollar, dans ce cas, représente un utilisateur. Dès que nous nous connectons en tant que `root`, le caractère se transforme en `dièse` <`#`> et ressemble à ceci :

```bash
root@htb[/htb]#
```

Par exemple, lorsque nous téléversons et exécutons un shell sur le système cible, il se peut que nous ne voyions pas le nom d'utilisateur, le nom d'hôte et le répertoire de travail actuel. Cela peut être dû au fait que la variable PS1 dans l'environnement n'est pas correctement définie. Dans ce cas, nous verrions les invites suivantes :

## Non privilégié - Invite de shell utilisateur

```bash
$
```

## Privilégié - Invite de shell root

```bash
#
```

La variable `PS1` dans les systèmes Linux contrôle l'apparence de votre invite de commande dans le terminal. C'est comme un modèle qui définit le texte que vous voyez chaque fois que le système est prêt à ce que vous saisissiez une commande. En personnalisant la variable PS1, vous pouvez modifier l'invite pour afficher des informations telles que votre nom d'utilisateur, le nom de votre ordinateur, le dossier actuel dans lequel vous vous trouvez, ou même ajouter des couleurs et des caractères spéciaux. Cela vous permet de personnaliser l'interface en ligne de commande (command-line interface) pour la rendre plus informative ou visuellement attrayante.

En plus d'afficher des informations de base comme votre nom d'utilisateur et votre dossier actuel, vous pouvez personnaliser l'invite de commande pour afficher d'autres détails utiles tels que l'adresse IP, la date, l'heure et la réussite ou l'échec de la dernière commande. Cette personnalisation est particulièrement utile lors des tests d'intrusion (penetration tests), car elle vous permet de suivre vos actions plus efficacement. Par exemple, vous pouvez configurer l'invite pour afficher le chemin complet du répertoire de travail actuel au lieu de son simple nom, et même inclure l'adresse IP de la cible si nécessaire. En utilisant des outils comme `script` ou en consultant le fichier `.bash_history` (situé dans le répertoire personnel de l'utilisateur), vous pouvez enregistrer toutes les commandes que vous avez utilisées et les organiser par date et heure, ce qui facilite la documentation et l'analyse.

L'invite peut être personnalisée à l'aide de caractères spéciaux et de variables dans le fichier de configuration du shell (`.bashrc` pour le shell Bash). Par exemple, nous pouvons utiliser : le caractère `\u` pour représenter le nom d'utilisateur actuel, `\h` pour le nom d'hôte, et `\w` pour le répertoire de travail actuel.

|**Caractère spécial**|**Description**|
|---|---|
|`\d`|Date (Lun 6 Fév)|
|`\D{%Y-%m-%d}`|Date (AAAA-MM-JJ)|
|`\H`|Nom d'hôte complet|
|`\j`|Nombre de tâches gérées par le shell|
|`\n`|Nouvelle ligne|
|`\r`|Retour chariot|
|`\s`|Nom du shell|
|`\t`|Heure actuelle format 24 heures (HH:MM:SS)|
|`\T`|Heure actuelle format 12 heures (HH:MM:SS)|
|`\@`|Heure actuelle|
|`\u`|Nom d'utilisateur actuel|
|`\w`|Chemin complet du répertoire de travail actuel|

La personnalisation de l'invite peut être un moyen utile de rendre votre expérience du terminal plus personnelle et efficace. Elle peut également être un outil précieux pour le dépannage et la résolution de problèmes, car elle peut fournir des informations importantes sur l'état du système à tout moment.

En plus de personnaliser l'invite, nous pouvons personnaliser notre environnement de terminal avec différents jeux de couleurs, polices et autres paramètres pour rendre notre environnement de travail plus agréable visuellement et plus facile à utiliser.

Cependant, nous constatons la même chose que lorsque nous travaillons sur l'interface graphique de Windows. Nous sommes connectés en tant qu'utilisateur sur un ordinateur portant un nom spécifique, et nous savons dans quel répertoire nous nous trouvons lorsque nous naviguons dans notre système. L'invite Bash peut également être personnalisée et modifiée selon nos propres besoins. Le réglage de l'invite bash dépasse le cadre de ce module. Cependant, nous pouvons consulter [bash-prompt-generator](https://bash-prompt-generator.org/) et [powerline](https://github.com/powerline/powerline), qui nous donnent la possibilité d'adapter notre invite à nos besoins.

---

← [[03 - Introduction au Shell]] | [[00 - Sommaire Linux|Sommaire]] | [[05 - Obtenir de l'aide]] →
