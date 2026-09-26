---
tags:
  - bash-scripting
ordre: 8
---

# Contrôle de flux - Branchements

---

Comme nous l'avons déjà vu, les branchements dans le contrôle de flux (flow control) incluent les instructions `if-else` et `case`. Nous avons déjà abordé en détail les instructions `if-else` et savons comment elles fonctionnent. Nous allons maintenant examiner de plus près les instructions `case`.

---

## Instructions Case

Les instructions `Case` sont également connues sous le nom d'instructions `switch-case` dans d'autres langages, tels que C/C++ et C#. La principale différence entre `if-else` et `switch-case` est que les constructions `if-else` nous permettent de vérifier n'importe quelle expression booléenne, tandis que `switch-case` compare toujours uniquement la variable avec la valeur exacte. Par conséquent, les mêmes conditions que pour `if-else`, telles que « supérieur à », ne sont pas autorisées pour `switch-case`. La syntaxe des instructions switch-case se présente comme suit :

#### Syntaxe - Switch-Case

```bash
case <expression> in
    pattern_1 ) statements ;;
    pattern_2 ) statements ;;
    pattern_3 ) statements ;;
esac
```

La définition de switch-case commence par `case`, suivi de la variable ou de la valeur en tant qu'expression, qui est ensuite comparée dans le motif (pattern). Si la variable ou la valeur correspond à l'expression, les instructions sont exécutées après la parenthèse et se terminent par un double point-virgule (`;;`).

Dans notre script `CIDR.sh`, nous avons utilisé une telle instruction `case`. Ici, nous avons défini quatre options différentes que nous avons attribuées à notre script, indiquant comment il doit procéder après notre décision.

#### CIDR.sh

```bash
<SNIP>
# Available options
echo -e "Additional options available:"
echo -e "\t1) Identify the corresponding network range of target domain."
echo -e "\t2) Ping discovered hosts."
echo -e "\t3) All checks."
echo -e "\t*) Exit.\n"

read -p "Select your option: " opt

case $opt in
    "1") network_range ;;
    "2") ping_host ;;
    "3") network_range && ping_host ;;
    "*") exit 0 ;;
esac
<SNIP>
```

Avec les deux premières options, ce script exécute différentes fonctions que nous avions définies auparavant. Avec la troisième option, les deux fonctions sont exécutées, et avec n'importe quelle autre option, le script sera terminé.
---

← [[07 - Contrôle de flux - Boucles]] | [[00 - Sommaire Bash Scripting|Sommaire]] | [[09 - Fonctions]] →
