---
tags:
  - linux
ordre: 12
---

# Filtrer le contenu

Dans la section précédente, nous avons exploré comment utiliser la redirection pour envoyer la sortie d'un programme vers un autre pour un traitement ultérieur. Parlons maintenant de la lecture de fichiers directement depuis la ligne de commande, sans avoir besoin d'ouvrir un éditeur de texte.

Il existe deux outils puissants pour cela : `more` et `less`. Ils sont connus sous le nom de visualiseurs (pagers) et permettent de visualiser le contenu d'un fichier de manière interactive, un écran à la fois. Bien que ces deux outils aient un objectif similaire, ils présentent quelques différences de fonctionnalités, que nous aborderons plus tard.

En utilisant `more` et `less`, vous pouvez facilement faire défiler de gros fichiers, rechercher du texte et naviguer en avant ou en arrière sans modifier le fichier lui-même. C'est particulièrement utile lorsque vous travaillez avec des logs ou des fichiers texte volumineux qui ne tiennent pas sur un seul écran.

L'objectif de cette section est d'apprendre à filtrer le contenu et à gérer la sortie redirigée des commandes précédentes. Mais avant de nous plonger dans le filtrage, nous devons nous familiariser avec certains outils et commandes essentiels qui sont spécifiquement conçus pour rendre le filtrage plus efficace et plus puissant.

Avant de commencer à filtrer la sortie des commandes, explorons quelques outils fondamentaux qui vous aideront à trier et manipuler efficacement du texte. Ces outils sont cruciaux lorsque vous travaillez avec de grandes quantités de données ou lorsque vous devez automatiser des tâches impliquant la recherche, le tri ou le traitement d'informations.

Examinons quelques exemples pour comprendre comment ces outils fonctionnent en pratique.

---

## More

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | more
```

Le fichier `/etc/passwd` sous Linux est comme un annuaire téléphonique pour les utilisateurs du système. Il inclut des détails tels que le nom d'utilisateur, l'ID d'utilisateur, l'ID de groupe, le répertoire personnel et le shell par défaut qu'ils utilisent.

Après avoir lu le contenu avec `cat` et l'avoir redirigé vers `more`, le `visualiseur` déjà mentionné s'ouvre, et nous commencerons automatiquement au début du fichier.

```bash
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
<SNIP>
--More--
```

Avec la touche `[Q]`, nous pouvons quitter ce `visualiseur`. Nous remarquerons que la sortie reste dans le terminal.

---

## Less

Si nous examinons maintenant l'outil `less`, nous remarquerons sur la page de manuel qu'il contient beaucoup plus de fonctionnalités que `more`.

```bash
Hiterof13@htb[/htb]$ less /etc/passwd
```

La présentation est presque la même qu'avec `more`.

```bash
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
<SNIP>
:
```

En fermant `less` avec la touche `[Q]`, nous remarquerons que la sortie que nous avons vue, contrairement à `more`, ne reste pas dans le terminal.

---

## Head

Parfois, nous ne serons intéressés que par des éléments spécifiques, soit au début du fichier, soit à la fin. Si nous voulons seulement obtenir les `premières` lignes du fichier, nous pouvons utiliser l'outil `head`. Par défaut, `head` affiche les dix premières lignes du fichier ou de l'entrée donné, sauf indication contraire.

```bash
Hiterof13@htb[/htb]$ head /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
```

---

## Tail

Si nous voulons seulement voir les dernières parties d'un fichier ou de résultats, nous pouvons utiliser l'homologue de `head` appelé `tail`, qui renvoie les `dix dernières` lignes.

```bash
Hiterof13@htb[/htb]$ tail /etc/passwd
miredo:x:115:65534::/var/run/miredo:/usr/sbin/nologin
usbmux:x:116:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
rtkit:x:117:119:RealtimeKit,,,:/proc:/usr/sbin/nologin
nm-openvpn:x:118:120:NetworkManager OpenVPN,,,:/var/lib/openvpn/chroot:/usr/sbin/nologin
nm-openconnect:x:119:121:NetworkManager OpenConnect plugin,,,:/var/lib/NetworkManager:/usr/sbin/nologin
pulse:x:120:122:PulseAudio daemon,,,:/var/run/pulse:/usr/sbin/nologin
beef-xss:x:121:124::/var/lib/beef-xss:/usr/sbin/nologin
lightdm:x:122:125:Light Display Manager:/var/lib/lightdm:/bin/false
do-agent:x:998:998::/home/do-agent:/bin/false
user6:x:1000:1000:,,,:/home/user6:/bin/bash
```

Il serait très bénéfique d'explorer les options disponibles que ces outils offrent et d'expérimenter avec elles.

---

## Sort

Selon les résultats et les fichiers traités, ils sont rarement triés. Il est souvent nécessaire de trier les résultats souhaités par ordre alphabétique ou numérique pour obtenir une meilleure vue d'ensemble. Pour cela, nous pouvons utiliser un outil appelé `sort`.

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | sort
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
cry0l1t3:x:1001:1001::/home/cry0l1t3:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
dovecot:x:114:117:Dovecot mail server,,,:/usr/lib/dovecot:/usr/sbin/nologin
dovenull:x:115:118:Dovecot login user,,,:/nonexistent:/usr/sbin/nologin
ftp:x:113:65534::/srv/ftp:/usr/sbin/nologin
games:x:5:60:games:/usr/games:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
htb-student:x:1002:1002::/home/htb-student:/bin/bash <SNIP>
```

Comme nous pouvons le voir maintenant, la sortie ne commence plus par root mais est maintenant triée par ordre alphabétique.

---

## Grep

Dans de nombreux cas, nous devrons rechercher des résultats spécifiques qui correspondent aux motifs que nous définissons. L'un des outils les plus couramment utilisés à cette fin est grep, qui offre un large éventail de fonctionnalités puissantes pour la recherche de motifs. Par exemple, nous pouvons utiliser grep pour rechercher les utilisateurs dont le shell par défaut est `/bin/bash`.

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | grep "/bin/bash"
root:x:0:0:root:/root:/bin/bash
mrb3n:x:1000:1000:mrb3n:/home/mrb3n:/bin/bash
cry0l1t3:x:1001:1001::/home/cry0l1t3:/bin/bash
htb-student:x:1002:1002::/home/htb-student:/bin/bash
```

Ce n'est qu'un exemple de la manière dont grep peut être appliqué pour filtrer efficacement les données en fonction de motifs prédéfinis. Une autre possibilité est d'exclure des résultats spécifiques. Pour cela, l'option « `-v` » est utilisée avec `grep`. Dans l'exemple suivant, nous excluons tous les utilisateurs qui ont désactivé le shell standard avec le nom « `/bin/false` » ou « `/usr/bin/nologin` ».

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | grep -v "false\|nologin"
root:x:0:0:root:/root:/bin/bash
sync:x:4:65534:sync:/bin:/bin/sync
postgres:x:111:117:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
user6:x:1000:1000:,,,:/home/user6:/bin/bash
```

---

## Cut

Des résultats spécifiques avec différents caractères peuvent être séparés en tant que délimiteurs. Ici, il est pratique de savoir comment supprimer des délimiteurs spécifiques et afficher les mots sur une ligne à une position spécifiée. L'un des outils qui peuvent être utilisés pour cela est `cut`. Par conséquent, nous utilisons l'option « `-d` » et définissons le délimiteur sur le caractère deux-points (`:`) et nous définissons avec l'option « `-f` » la position dans la ligne que nous voulons afficher.

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | grep -v "false\|nologin" | cut -d":" -f1
root sync postgres mrb3n cry0l1t3 htb-student
```

---

## Tr

Une autre possibilité de remplacer certains caractères d'une ligne par des caractères que nous définissons est l'outil `tr`. En première option, nous définissons le caractère que nous voulons remplacer, et en deuxième option, nous définissons le caractère par lequel nous voulons le remplacer. Dans l'exemple suivant, nous remplaçons le caractère deux-points par un espace.

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | grep -v "false\|nologin" | tr ":" " "
root x 0 0 root /root /bin/bash
sync x 4 65534 sync /bin /bin/sync
postgres x 111 117 PostgreSQL administrator,,, /var/lib/postgresql /bin/bash
mrb3n x 1000 1000 mrb3n /home/mrb3n /bin/bash
cry0l1t3 x 1001 1001  /home/cry0l1t3 /bin/bash
htb-student x 1002 1002  /home/htb-student /bin/bash
```

---

## Column

Comme les résultats de recherche peuvent souvent avoir une représentation peu claire, l'outil `column` est bien adapté pour afficher de tels résultats sous forme de tableau en utilisant le « `-t` ».

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | grep -v "false\|nologin" | tr ":" " " | column -t
root         x  0     0      root               /root                /bin/bash
sync         x  4     65534  sync               /bin                 /bin/sync
postgres     x  111   117    PostgreSQL         administrator,,,    /var/lib/postgresql     /bin/bash
mrb3n        x  1000  1000   mrb3n              /home/mrb3n          /bin/bash
cry0l1t3     x  1001  1001   /home/cry0l1t3     /bin/bash
htb-student  x  1002  1002   /home/htb-student  /bin/bash
```

---

## Awk

Comme nous l'avons peut-être remarqué, la ligne de l'utilisateur « `postgres` » a une colonne de trop. Pour que le tri de tels résultats soit le plus simple possible, la programmation (`g`)`awk` est bénéfique, car elle nous permet d'afficher le premier (`$1`) et le dernier (`$NF`) résultat de la ligne.

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | grep -v "false\|nologin" | tr ":" " " | awk '{print $1, $NF}'
root /bin/bash
sync /bin/sync
postgres /bin/bash
mrb3n /bin/bash
cry0l1t3 /bin/bash
htb-student /bin/bash
```

---

## Sed

Il arrivera des moments où nous voudrons changer des noms spécifiques dans tout le fichier ou l'entrée standard. L'un des outils que nous pouvons utiliser pour cela est l'éditeur de flux (stream editor) appelé `sed`. L'une de ses utilisations les plus courantes est la substitution de texte. Ici, `sed` recherche des motifs que nous avons définis sous forme d'expressions régulières (regex) et les remplace par un autre motif que nous avons également défini. Restons sur les derniers résultats et disons que nous voulons remplacer le mot « `bin` » par « `HTB` ».

L'indicateur « `s` » au début signifie la commande de substitution. Ensuite, nous spécifions le motif que nous voulons remplacer. Après la barre oblique (`/`), nous entrons le motif que nous voulons utiliser comme remplacement en troisième position. Enfin, nous utilisons l'indicateur « `g` », qui signifie remplacer toutes les correspondances.

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | grep -v "false\|nologin" | tr ":" " " | awk '{print $1, $NF}' | sed 's/bin/HTB/g'
root /HTB/bash
sync /HTB/sync
postgres /HTB/bash
mrb3n /HTB/bash
cry0l1t3 /HTB/bash
htb-student /HTB/bash
```

---

## Wc

Enfin et surtout, il sera souvent utile de savoir combien de correspondances réussies nous avons. Pour éviter de compter les lignes ou les caractères manuellement, nous pouvons utiliser l'outil `wc`. Avec l'option « `-l` », nous spécifions que seules les lignes sont comptées.

```bash
Hiterof13@htb[/htb]$ cat /etc/passwd | grep -v "false\|nologin" | tr ":" " " | awk '{print $1, $NF}' | wc -l
6
```

---

## Pratique

Gardez à l'esprit qu'il existe de nombreux autres outils disponibles que vous pouvez utiliser et intégrer tout au long de votre parcours. Il est fortement recommandé d'explorer des outils alternatifs pour des tâches spécifiques afin d'élargir vos compétences, car vous pourriez découvrir des options qui correspondent mieux à vos préférences personnelles et à vos flux de travail. Il n'y a pas de limites rigides, alors n'hésitez pas à explorer différentes possibilités et à profiter de la richesse des ressources partagées au sein de la communauté.

Il peut être un peu écrasant au début de faire face à tant d'outils différents et à leurs fonctions si nous ne les connaissons pas. Prenez votre temps et expérimentez avec les outils. Jetez un œil aux pages de manuel (`man <tool>`) ou appelez l'aide correspondante (`<tool> -h` / `<tool> --help`). La meilleure façon de se familiariser avec tous les outils est de pratiquer. Essayez de les utiliser aussi souvent que possible, et nous serons capables de filtrer beaucoup de choses intuitivement après peu de temps.

Voici quelques exercices facultatifs que nous pouvons utiliser pour améliorer nos compétences en matière de filtrage et nous familiariser davantage avec le terminal et les commandes. Le fichier avec lequel nous devrons travailler est le fichier `/etc/passwd` sur notre `cible` et nous pouvons utiliser n'importe laquelle des commandes présentées ci-dessus. Notre objectif est de filtrer et d'afficher uniquement des contenus spécifiques. Lisez le fichier et filtrez son contenu de manière à ne voir que :

|||
|---|---|
|1.|Une ligne avec le nom d'utilisateur `cry0l1t3`.|
|2.|Les noms d'utilisateur.|
|3.|Le nom d'utilisateur `cry0l1t3` et son UID.|
|4.|Le nom d'utilisateur `cry0l1t3` et son UID séparés par une virgule (,).|
|5.|Le nom d'utilisateur `cry0l1t3`, son UID et le shell défini, séparés par une virgule (,).|
|6.|Tous les noms d'utilisateur avec leur UID et les shells définis, séparés par une virgule (,).|
|7.|Tous les noms d'utilisateur avec leur UID et les shells définis, séparés par une virgule (,), en excluant ceux qui contiennent `nologin` ou `false`.|
|8.|Tous les noms d'utilisateur avec leur UID et les shells définis, séparés par une virgule (,), en excluant ceux qui contiennent `nologin` et en comptant toutes les lignes de la sortie filtrée.|

---

← [[11 - Descripteurs de Fichiers et Redirections]] | [[00 - Sommaire Linux|Sommaire]] | [[13 - Expressions régulières]] →
