---
tags:
  - linux
ordre: 13
---

# Expressions régulières

Les expressions régulières (`RegEx`), ou expressions rationnelles, sont comme l'art de créer des plans précis pour rechercher des motifs dans du texte ou des fichiers. Elles vous permettent de trouver, remplacer et manipuler des données avec une précision incroyable. Considérez les RegEx comme un filtre hautement personnalisable qui vous permet de passer au crible des chaînes de texte, à la recherche de ce dont vous avez besoin, que ce soit pour analyser des données, valider des entrées ou effectuer des opérations de recherche avancées.

À la base, une expression régulière est une séquence de caractères et de symboles qui forment ensemble un motif de recherche. Ces motifs impliquent souvent des symboles spéciaux appelés métacaractères, qui définissent la structure de la recherche plutôt que de représenter du texte littéral. Par exemple, les métacaractères vous permettent de spécifier si vous recherchez des chiffres, des lettres ou tout caractère correspondant à un certain motif.

Les RegEx sont disponibles dans de nombreux langages de programmation et outils, tels que `grep` ou `sed`, ce qui en fait un outil polyvalent et puissant dans notre boîte à outils.

---

## Groupement

Entre autres choses, les regex nous offrent la possibilité de grouper les motifs de recherche souhaités. Fondamentalement, les regex suivent trois concepts différents, qui se distinguent par les trois types de crochets :

### Opérateurs de groupement

||**Opérateurs**|**Description**|
|---|---|---|
|1|`(a)`|Les parenthèses sont utilisées pour grouper des parties d'une regex. À l'intérieur des parenthèses, vous pouvez définir d'autres motifs qui doivent être traités ensemble.|
|2|`[a-z]`|Les crochets sont utilisés pour définir des classes de caractères. À l'intérieur des crochets, vous pouvez spécifier une liste de caractères à rechercher.|
|3|`{1,10}`|Les accolades sont utilisées pour définir des quantificateurs. À l'intérieur des accolades, vous pouvez spécifier un nombre ou une plage qui indique combien de fois un motif précédent doit être répété.|
|4|`\|`|Aussi appelé opérateur OU (OR) et affiche des résultats lorsque l'une des deux expressions correspond|
|5|`.*`|Fonctionne de manière similaire à un opérateur ET (AND) en affichant des résultats uniquement lorsque les deux expressions sont présentes et correspondent dans l'ordre spécifié|

Supposons que nous utilisions l'opérateur `OR`. La regex recherche l'un des paramètres de recherche donnés. Dans l'exemple suivant, nous recherchons les lignes contenant le mot `my` ou `false`. Pour utiliser ces opérateurs, vous devez appliquer les regex étendues en utilisant l'option `-E` dans `grep`.

### Opérateur OR

```bash
cry0l1t3@htb:~$ grep -E "(my|false)" /etc/passwd
lxd:x:105:65534::/var/lib/lxd/:/bin/false
pollinate:x:109:1::/var/cache/pollinate:/bin/false
mysql:x:116:120:MySQL Server,,:/nonexistent:/bin/false
```

Comme l'un des deux paramètres de recherche apparaît toujours dans les trois lignes, les trois lignes sont affichées en conséquence. Cependant, si nous utilisons l'opérateur `AND`, nous obtiendrons un résultat différent pour les mêmes paramètres de recherche.

### Opérateur AND

```bash
cry0l1t3@htb:~$ grep -E "(my.*false)" /etc/passwd
mysql:x:116:120:MySQL Server,,:/nonexistent:/bin/false
```

En gros, ce que nous disons avec cette commande, c'est que nous cherchons une ligne où nous voulons voir à la fois `my` et `false`. Un exemple simplifié serait également d'utiliser `grep` deux fois, ce qui ressemblerait à ceci :

```bash
cry0l1t3@htb:~$ grep -E "my" /etc/passwd | grep -E "false"
mysql:x:116:120:MySQL Server,,:/nonexistent:/bin/false
```

---

Voici quelques tâches facultatives pour vous aider à pratiquer les RegEx et à améliorer votre capacité à les gérer plus efficacement. Ces exercices utiliseront le fichier `/etc/ssh/sshd_config` sur votre instance `Pwnbox`, vous permettant d'explorer des applications concrètes des RegEx dans un fichier de configuration. En accomplissant ces tâches, vous acquerrez une expérience pratique du travail avec des motifs, de la recherche et de la manipulation de texte dans des scénarios pratiques.

|||
|---|---|
|1|Afficher toutes les lignes qui ne contiennent pas le caractère `#`.|
|2|Rechercher toutes les lignes qui contiennent un mot commençant par `Permit`.|
|3|Rechercher toutes les lignes qui contiennent un mot se terminant par `Authentication`.|
|4|Rechercher toutes les lignes contenant le mot `Key`.|
|5|Rechercher toutes les lignes commençant par `Password` et contenant `yes`.|
|6|Rechercher toutes les lignes qui se terminent par `yes`.|

---

← [[12 - Filtrer le contenu]] | [[00 - Sommaire Linux|Sommaire]] | [[14 - Gestion des permissions]] →
