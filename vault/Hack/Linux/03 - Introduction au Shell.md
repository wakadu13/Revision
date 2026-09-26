---
tags:
  - linux
ordre: 3
---

# Introduction au Shell

Il est crucial d'apprendre à utiliser le shell Linux, car de nombreux serveurs sont basés sur Linux. Ceux-ci sont souvent utilisés car Linux est moins sujet aux erreurs que les serveurs Windows. Par exemple, les serveurs web sont souvent basés sur Linux. Savoir utiliser le système d'exploitation pour le contrôler efficacement nécessite de comprendre et de maîtriser l'élément essentiel de Linux, le `Shell`. Lorsque nous sommes passés de Windows à Linux pour la première fois, cela ressemblait-il à quelque chose comme ça :

![Terminal Parrot affichant une invite de commande avec l'utilisateur 'user6@htb-wpjudq32ze' et la commande 'okay google' saisie.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/first_linux2.png)

Un terminal Linux, également appelé `shell` ou ligne de commande, fournit une interface d'entrée/sortie (E/S) textuelle entre les utilisateurs et le noyau (kernel) d'un système informatique. Le terme console est également courant, mais il ne fait pas référence à une fenêtre mais à un écran en mode texte. Dans la fenêtre du terminal, des commandes peuvent être exécutées pour contrôler le système.

Nous pouvons considérer un shell comme l'équivalent textuel d'une interface utilisateur graphique (`GUI` - Graphical User Interface) dans laquelle nous saisissons des commandes pour effectuer des actions comme naviguer vers d'autres répertoires, travailler avec des fichiers et obtenir des informations du système, mais avec des capacités bien plus étendues.

---

## Émulateurs de terminal

L'émulation de terminal est un logiciel qui émule la fonction d'un terminal. Il permet d'utiliser des programmes en mode texte au sein d'une interface utilisateur graphique (`GUI`). Il existe également ce que l'on appelle des interfaces en ligne de commande (`CLI` - Command-Line Interfaces) qui s'exécutent comme des terminaux supplémentaires au sein d'un même terminal. En bref, un terminal sert d'interface à l'interpréteur de commandes du shell.

Imaginez que vous êtes dans un grand immeuble de bureaux où le shell est la salle des serveurs principale qui traite toutes les données et commandes de l'entreprise. Le terminal est comme le bureau d'un réceptionniste qui sert de point de communication avec la salle des serveurs. Vous vous adressez au réceptionniste (terminal) pour transmettre des instructions ou des demandes à la salle des serveurs (shell).

Maintenant, supposons que vous travaillez à distance. Le logiciel d'émulation de terminal agit comme un bureau de réceptionniste virtuel sur l'écran de votre ordinateur (la `GUI`), vous permettant d'interagir avec la salle des serveurs sans être physiquement présent dans le bureau. Il émule la fonction du véritable bureau du réceptionniste, vous permettant d'utiliser des programmes et des commandes en mode texte dans un environnement graphique.

De plus, les interfaces en ligne de commande (`CLI`) qui s'exécutent comme des terminaux supplémentaires au sein d'un même terminal sont comme avoir plusieurs bureaux de réceptionnistes virtuels ouverts simultanément sur votre écran. Chacun vous permet d'envoyer des instructions différentes à la salle des serveurs de manière indépendante, mais via la même interface principale. En substance, le terminal sert de passerelle pour communiquer avec les opérations principales gérées par le shell et les contrôler.

Les émulateurs de terminal et les multiplexeurs sont des extensions utiles pour le terminal. Ils nous fournissent différentes méthodes et fonctions pour travailler avec le terminal, comme diviser le terminal en une seule fenêtre, travailler dans plusieurs répertoires, créer différents espaces de travail, et bien plus encore. Un exemple d'utilisation d'un tel multiplexeur, appelé Tmux, pourrait ressembler à ceci :

![Fenêtre de terminal avec trois volets affichant des listes de fichiers pour les répertoires : BloodHound, Impacket et SecLists. Chaque volet affiche divers fichiers et répertoires dans le répertoire personnel de l'utilisateur 'cry0l1t3' sur la branche 'master'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/tmux.png)

---

## Le Shell

Le shell le plus couramment utilisé sous Linux est le `Bourne-Again Shell` (`BASH`), et il fait partie du projet GNU. Tout ce que nous faisons via la `GUI` peut être fait avec le shell. Le shell nous offre beaucoup plus de possibilités pour interagir avec les programmes et les processus afin d'obtenir des informations plus rapidement. De plus, de nombreux processus peuvent être facilement automatisés avec des scripts plus ou moins grands qui facilitent grandement le travail manuel.

Outre Bash, il existe également d'autres shells comme [Tcsh/Csh](https://en.wikipedia.org/wiki/Tcsh), [Ksh](https://en.wikipedia.org/wiki/KornShell), [Zsh](https://en.wikipedia.org/wiki/Z_shell), le shell [Fish](https://en.wikipedia.org/wiki/Friendly_interactive_shell) et d'autres.

---

← [[02 - Distributions Linux]] | [[00 - Sommaire Linux|Sommaire]] | [[04 - Description de l'invite]] →
