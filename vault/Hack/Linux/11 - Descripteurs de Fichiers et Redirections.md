---
tags:
  - linux
ordre: 11
---

# Descripteurs de Fichiers et Redirections

Un descripteur de fichier (`FD`, pour File Descriptor) dans les systèmes d'exploitation Unix/Linux est une référence, maintenue par le noyau, qui permet au système de gérer les opérations d'Entrée/Sortie (`I/O`, pour Input/Output). Il agit comme un identifiant unique pour un fichier ouvert, un socket ou toute autre ressource d'I/O. Dans les systèmes d'exploitation basés sur Windows, cela est connu sous le nom de handle de fichier. Essentiellement, le descripteur de fichier est le moyen pour le système de suivre les connexions `d'I/O` actives, comme la lecture ou l'écriture dans un fichier.

Imaginez-le comme le numéro de ticket que vous recevez en déposant votre manteau au vestiaire. Le ticket (descripteur de fichier) représente votre connexion à votre manteau (fichier ou ressource), et chaque fois que vous avez besoin de récupérer votre manteau (effectuer une I/O), vous présentez le ticket au préposé (système d'exploitation) qui sait exactement où votre manteau est rangé (à quelle ressource le descripteur de fichier se réfère). Sans le ticket, vous n'auriez aucun moyen d'accéder efficacement à votre manteau parmi les nombreux autres, tout comme sans descripteur de fichier, le système d'exploitation ne saurait pas avec quelle ressource interagir. Vous verrez bientôt pourquoi les descripteurs de fichiers sont si importants et pourquoi leur compréhension est cruciale à mesure que nous aborderons les exemples à venir.

Par défaut, les trois premiers descripteurs de fichiers sous Linux sont :

1. Flux de données pour l'Entrée
    - `STDIN – 0`
2. Flux de données pour la Sortie
    - `STDOUT – 1`
3. Flux de données pour la Sortie relative à une erreur survenue.
    - `STDERR – 2`

---

## STDIN et STDOUT

Voyons un exemple avec `cat`. En exécutant `cat`, nous fournissons au programme en cours notre entrée standard (`STDIN - FD 0`), marquée en `vert`, qui dans ce cas est "SOME INPUT". Dès que nous avons confirmé notre entrée avec `[ENTER]`, elle est renvoyée au terminal en tant que sortie standard (`STDOUT - FD 1`), marquée en **rouge**.

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' affichant la commande 'cat' et la sortie 'Think Outside The Box' surlignée deux fois, une fois en vert et une fois en rouge.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find0.png)

---

## STDOUT et STDERR

Dans l'exemple suivant, en utilisant la commande `find`, nous verrons la sortie standard (`STDOUT - FD 1`) marquée en `vert` et la sortie d'erreur standard (`STDERR - FD 2`) marquée en rouge.

```bash
Hiterof13@htb[/htb]$ find /etc/ -name shadow
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' exécutant 'find /etc/ -name shadow'. La sortie affiche '/etc/shadow' et 'Permission denied' pour d'autres répertoires](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find1.png)

Dans ce cas, l'erreur est marquée et affichée avec "`Permission denied`". Nous pouvons le vérifier en redirigeant le descripteur de fichier pour les erreurs (`FD 2 - STDERR`) vers "`/dev/null`". De cette manière, nous redirigeons les erreurs résultantes vers le "périphérique nul", qui supprime toutes les données.

```bash
Hiterof13@htb[/htb]$ find /etc/ -name shadow 2>/dev/null
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' exécutant 'find /etc/ -name shadow 2>/dev/null'. La sortie affiche '/etc/shadow'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find2.png)

---

## Rediriger STDOUT vers un Fichier

Nous pouvons maintenant voir que toutes les erreurs (`STDERR`) précédemment présentées avec "`Permission denied`" ne sont plus affichées. Le seul résultat que nous voyons maintenant est la sortie standard (`STDOUT`), que nous pouvons également rediriger vers un fichier nommé `results.txt` qui ne contiendra que la sortie standard sans les erreurs standard.

```bash
Hiterof13@htb[/htb]$ find /etc/ -name shadow 2>/dev/null > results.txt
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' exécutant 'find /etc/ -name shadow 2>/dev/null > results.txt' et 'cat results.txt'. La sortie affiche '/etc/shadow'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find3.png)

---

## Rediriger STDOUT et STDERR vers des Fichiers Séparés

Nous aurions dû remarquer que nous n'avons pas utilisé de numéro avant le signe supérieur à (`>`) dans le dernier exemple. C'est parce que nous avons redirigé toutes les erreurs standard vers le "`périphérique nul`" auparavant, et la seule sortie que nous obtenons est la sortie standard (`FD 1 - STDOUT`). Pour être plus précis, nous allons rediriger la sortie d'erreur standard (`FD 2 - STDERR`) et la sortie standard (`FD 1 - STDOUT`) vers des fichiers différents.

```bash
Hiterof13@htb[/htb]$ find /etc/ -name shadow 2> stderr.txt 1> stdout.txt
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' exécutant 'find /etc/ -name shadow 2> stderr.txt 1> stdout.txt'. La sortie affiche '/etc/shadow' dans stdout.txt et des messages 'Permission denied' dans stderr.txt.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find4.png)

---

## Rediriger STDIN

Comme nous l'avons déjà vu, en combinaison avec les descripteurs de fichiers, nous pouvons rediriger les erreurs et la sortie avec le caractère supérieur à (`>`). Cela fonctionne également avec le signe inférieur à (`<`). Cependant, le signe inférieur à sert d'entrée standard (`FD 0 - STDIN`). Ces caractères peuvent être vus comme une "`direction`" sous la forme d'une flèche qui nous indique "`d'où`" et "`vers où`" les données doivent être redirigées. Nous utilisons la commande `cat` pour utiliser le contenu du fichier "`stdout.txt`" comme `STDIN`.

```bash
Hiterof13@htb[/htb]$ cat < stdout.txt
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' exécutant 'cat < stdout.txt'. La sortie affiche '/etc/shadow'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find5.png)

---

## Rediriger STDOUT et Ajouter à un Fichier

Lorsque nous utilisons le signe supérieur à (`>`) pour rediriger notre `STDOUT`, un nouveau fichier est automatiquement créé s'il n'existe pas déjà. Si ce fichier existe, il sera écrasé sans demander de confirmation. Si nous voulons ajouter `STDOUT` à notre fichier existant, nous pouvons utiliser le double signe supérieur à (`>>`).

```bash
Hiterof13@htb[/htb]$ find /etc/ -name passwd >> stdout.txt 2>/dev/null
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' exécutant 'find /etc/ -name passwd >> stdout.txt 2>/dev/null' et 'cat stdout.txt'. La sortie affiche '/etc/pam.d/passwd', '/etc/cron.daily/passwd', et '/etc/passwd'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find9.png)

---

## Rediriger un Flux STDIN vers un Fichier

Nous pouvons également utiliser les doubles caractères inférieur à (`<<`) pour ajouter notre entrée standard via un flux. Nous pouvons utiliser la fonction dite de `Fin de Fichier` (`End-Of-File` ou `EOF`) d'un fichier système Linux, qui définit la fin de l'entrée. Dans l'exemple suivant, nous utiliserons la commande `cat` pour lire notre entrée en flux et la diriger vers un fichier appelé "`stream.txt`".

```bash
Hiterof13@htb[/htb]$ cat << EOF > stream.txt
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' exécutant 'cat << EOF > stream.txt' avec l'entrée 'Hack The Box' et 'EOF'. Ensuite, 'cat stream.txt' affiche 'Hack The Box'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find6.png)

---

## Pipes

Une autre façon de rediriger `STDOUT` est d'utiliser des pipes (`|`). Ils sont utiles lorsque nous voulons que le `STDOUT` d'un programme soit traité par un autre. L'un des outils les plus couramment utilisés est `grep`, que nous utiliserons dans l'exemple suivant. Grep est utilisé pour filtrer `STDOUT` selon le motif que nous définissons. Dans l'exemple suivant, nous utilisons la commande `find` pour rechercher tous les fichiers dans le répertoire "`/etc/`" avec une extension "`.conf`". Toutes les erreurs sont redirigées vers le "`périphérique nul`" (`/dev/null`). En utilisant `grep`, nous filtrons les résultats et spécifions que seules les lignes contenant le motif "`systemd`" doivent être affichées.

```bash
Hiterof13@htb[/htb]$ find /etc/ -name *.conf 2>/dev/null | grep systemd
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' exécutant 'find /etc/ -name *.conf 2>/dev/null | grep systemd'. La sortie liste les fichiers de configuration systemd : system.conf, timesyncd.conf, journald.conf, user.conf, logind.conf, resolved.conf.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find7.png)

Les redirections ne fonctionnent pas qu'une seule fois. Nous pouvons utiliser les résultats obtenus pour les rediriger vers un autre programme. Pour l'exemple suivant, nous utiliserons l'outil appelé `wc`, qui devrait compter le nombre total de résultats obtenus.

```bash
Hiterof13@htb[/htb]$ find /etc/ -name *.conf 2>/dev/null | grep systemd | wc -l
```

![Fenêtre de terminal avec l'utilisateur 'htb-student@nixfund' exécutant 'find /etc/ -name *.conf 2>/dev/null | grep systemd | wc -l'. La sortie affiche '6'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/18/find8.png)

---

Maintenant que nous avons une compréhension fondamentale des descripteurs de fichiers, des redirections et des pipes, nous pouvons structurer nos commandes plus efficacement pour extraire exactement les informations dont nous avons besoin. Cette connaissance nous permet de manipuler la façon dont les entrées et les sorties circulent entre les fichiers, les processus et le système, nous permettant de gérer les données plus efficacement. En tirant parti de ces outils, nous pouvons rationaliser les tâches, éviter les étapes inutiles et travailler avec les fichiers et les ressources du système d'une manière beaucoup plus organisée et efficace, améliorant ainsi notre productivité et notre précision dans la gestion des opérations.

---

← [[10 - Rechercher des Fichiers et des Dossiers]] | [[00 - Sommaire Linux|Sommaire]] | [[12 - Filtrer le contenu]] →
