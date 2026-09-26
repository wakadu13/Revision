---
tags:
  - brute-force
ordre: 8
---

# Formulaires de connexion

Au-delà du domaine de l'authentification HTTP de base (Basic HTTP Authentication), de nombreuses applications web utilisent des formulaires de connexion personnalisés comme principal mécanisme d'authentification. Ces formulaires, bien que visuellement variés, partagent souvent des mécanismes sous-jacents communs qui en font des cibles pour les attaques par force brute (brute forcing).

## Comprendre les formulaires de connexion

Bien que les formulaires de connexion puissent apparaître comme de simples boîtes de dialogue vous demandant votre nom d'utilisateur et votre mot de passe, ils représentent une interaction complexe de technologies côté client et côté serveur. À la base, les formulaires de connexion sont essentiellement des formulaires HTML intégrés dans une page web. Ces formulaires incluent généralement des champs de saisie (`<input>`) pour capturer le nom d'utilisateur et le mot de passe, ainsi qu'un bouton d'envoi (`<button>` ou `<input type="submit">`) pour lancer le processus d'authentification.

## Exemple de formulaire de connexion de base

La plupart des formulaires de connexion suivent une structure similaire. Voici un exemple :

```html
<form action="/login" method="post">   <label for="username">Username:</label>   <input type="text" id="username" name="username"><br><br>   <label for="password">Password:</label>   <input type="password" id="password" name="password"><br><br>   <input type="submit" value="Submit"> </form>
```

Ce formulaire, lorsqu'il est soumis, envoie une requête POST au point de terminaison (endpoint) `/login` sur le serveur, incluant le nom d'utilisateur et le mot de passe saisis en tant que données de formulaire.

```http
POST /login HTTP/1.1 Host: www.example.com Content-Type: application/x-www-form-urlencoded Content-Length: 29  username=john&password=secret123
```

- La méthode `POST` indique que des données sont envoyées au serveur pour créer ou mettre à jour une ressource.
- `/login` est le point de terminaison de l'URL qui traite la demande de connexion.
- L'en-tête `Content-Type` spécifie comment les données sont encodées dans le corps de la requête.
- L'en-tête `Content-Length` indique la taille des données envoyées.
- Le corps de la requête contient le nom d'utilisateur et le mot de passe, encodés sous forme de paires clé-valeur.

Lorsqu'un utilisateur interagit avec un formulaire de connexion, son navigateur gère le traitement initial. Le navigateur capture les identifiants saisis, utilisant souvent JavaScript pour la validation côté client ou l'assainissement des entrées (input sanitization). Lors de la soumission, le navigateur construit une requête HTTP POST. Cette requête encapsule les données du formulaire — y compris le nom d'utilisateur et le mot de passe — dans son corps, souvent encodées en `application/x-www-form-urlencoded` ou `multipart/form-data`.

## http-post-form

**Pour suivre les étapes, démarrez le système cible via la section des questions en bas de la page.**

Le service `http-post-form` de Hydra est spécifiquement conçu pour cibler les formulaires de connexion. Il permet d'automatiser les requêtes POST, en insérant dynamiquement des combinaisons de nom d'utilisateur et de mot de passe dans le corps de la requête. En exploitant les capacités de Hydra, les attaquants peuvent tester efficacement de nombreuses combinaisons d'identifiants contre un formulaire de connexion, découvrant potentiellement des connexions valides.

La structure générale d'une commande Hydra utilisant `http-post-form` est la suivante :

```bash
Hiterof13@htb[/htb]$ hydra [options] target http-post-form "path:params:condition_string"
```

### Comprendre la chaîne de condition

Dans le module `http-post-form` de Hydra, les conditions de réussite et d'échec sont cruciales pour identifier correctement les tentatives de connexion valides et invalides. Hydra se base principalement sur les conditions d'échec (`F=...`) pour déterminer quand une tentative de connexion a échoué, mais vous pouvez également spécifier une condition de réussite (`S=...`) pour indiquer quand une connexion est réussie.

La condition d'échec (`F=...`) est utilisée pour rechercher une chaîne de caractères spécifique dans la réponse du serveur qui signale une tentative de connexion échouée. C'est l'approche la plus courante, car de nombreux sites web renvoient un message d'erreur (comme « Nom d'utilisateur ou mot de passe invalide ») lorsque la connexion échoue. Par exemple, si un formulaire de connexion renvoie le message « Invalid credentials » lors d'une tentative échouée, vous pouvez configurer Hydra comme suit :

```bash
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:F=Invalid credentials"
```

Dans ce cas, Hydra vérifiera chaque réponse pour y trouver la chaîne « Invalid credentials ». S'il trouve cette phrase, il marquera la tentative de connexion comme un échec et passera à la paire nom d'utilisateur/mot de passe suivante. Cette approche est couramment utilisée car les messages d'échec sont généralement faciles à identifier.

Cependant, il arrive que vous n'ayez pas de message d'échec clair, mais plutôt une condition de réussite distincte. Par exemple, si l'application redirige l'utilisateur après une connexion réussie (en utilisant le code de statut HTTP `302`), ou affiche un contenu spécifique (comme « Dashboard » ou « Welcome »), vous pouvez configurer Hydra pour rechercher cette condition de réussite en utilisant `S=`. Voici un exemple où une connexion réussie entraîne une redirection 302 :

```bash
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
```

Dans ce cas, Hydra considérera toute réponse renvoyant un code de statut HTTP 302 comme une connexion réussie. De même, si une connexion réussie entraîne l'apparition d'un contenu comme « Dashboard » sur la page, vous pouvez configurer Hydra pour rechercher ce mot-clé comme condition de réussite :

```bash
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:S=Dashboard"
```

Hydra enregistrera désormais la connexion comme réussie s'il trouve le mot « Dashboard » dans la réponse du serveur.

Avant de lancer Hydra sur un formulaire de connexion, il est essentiel de recueillir des informations sur son fonctionnement interne. Cela implique de déterminer les paramètres exacts que le formulaire utilise pour transmettre le nom d'utilisateur et le mot de passe au serveur.

### Inspection manuelle

En accédant à l'adresse `IP:PORT` dans votre navigateur, un formulaire de connexion de base est présenté. En utilisant les outils de développement de votre navigateur (généralement en faisant un clic droit et en sélectionnant « Inspecter » ou une option similaire), vous pouvez afficher le code HTML sous-jacent de ce formulaire. Analysons ses composants clés :

```html
<form method="POST">     <h2>Login</h2>     <label for="username">Username:</label>     <input type="text" id="username" name="username">     <label for="password">Password:</label>     <input type="password" id="password" name="password">     <input type="submit" value="Login"> </form>
```

Le HTML révèle un formulaire de connexion simple. Points clés pour Hydra :

- `Method` : `POST` - Hydra devra envoyer des requêtes POST au serveur.
- Champs :
    - `Username` : Le champ de saisie nommé `username` sera ciblé.
    - `Password` : Le champ de saisie nommé `password` sera ciblé.

Avec ces détails, vous pouvez construire la commande Hydra pour automatiser l'attaque par force brute contre ce formulaire de connexion.

### Outils de développement du navigateur

Après avoir inspecté le formulaire, ouvrez les outils de développement de votre navigateur (F12) et accédez à l'onglet « Réseau ». Soumettez une tentative de connexion avec des identifiants quelconques. Cela vous permettra de voir la requête POST envoyée au serveur. Dans l'onglet « Réseau », trouvez la requête correspondant à la soumission du formulaire et vérifiez les données du formulaire, les en-têtes et la réponse du serveur.

![Formulaire de connexion avec erreur d'identifiants invalides et panneau réseau montrant les détails de la requête HTTP POST.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/57/devtools.png)

Cette information consolide davantage les renseignements dont nous aurons besoin pour Hydra. Nous avons maintenant la confirmation définitive à la fois du chemin cible (`/`) et des noms des paramètres (`username` et `password`).

### Interception par proxy

Pour des scénarios plus complexes, l'interception du trafic réseau avec un outil de proxy comme Burp Suite ou OWASP ZAP peut être d'une valeur inestimable. Configurez votre navigateur pour acheminer son trafic via le proxy, puis interagissez avec le formulaire de connexion. Le proxy capturera la requête POST, vous permettant de disséquer chacun de ses composants, y compris les paramètres de connexion précis et leurs valeurs.

## Construire la chaîne params pour Hydra

Après avoir analysé la structure et le comportement du formulaire de connexion, il est temps de construire la chaîne `params`, un composant essentiel du module d'attaque `http-post-form` de Hydra. Cette chaîne encapsule les données qui seront envoyées au serveur à chaque tentative de connexion, imitant une soumission de formulaire légitime.

La chaîne `params` se compose de paires clé-valeur, de la même manière que les données sont encodées dans une requête POST. Chaque paire représente un champ du formulaire de connexion, avec sa valeur correspondante.

- `Paramètres du formulaire` : Ce sont les champs essentiels qui contiennent le nom d'utilisateur et le mot de passe. Hydra remplacera dynamiquement les espaces réservés (`^USER^` et `^PASS^`) dans ces paramètres par des valeurs de vos listes de mots (wordlists).
- `Champs supplémentaires` : Si le formulaire inclut d'autres champs cachés ou des jetons (par exemple, des jetons CSRF), ils doivent également être inclus dans la chaîne `params`. Ceux-ci peuvent avoir des valeurs statiques ou des espaces réservés dynamiques si leurs valeurs changent à chaque requête.
- `Condition de réussite` : Ceci définit les critères que Hydra utilisera pour identifier une connexion réussie. Il peut s'agir d'un code de statut HTTP (comme `S=302` pour une redirection) ou de la présence ou de l'absence d'un texte spécifique dans la réponse du serveur (par ex., `F=Invalid credentials` ou `S=Welcome`).

Appliquons cela à notre scénario. Nous avons découvert :

- Le formulaire soumet les données au chemin racine (`/`).
- Le champ du nom d'utilisateur est nommé `username`.
- Le champ du mot de passe est nommé `password`.
- Un message d'erreur « Invalid credentials » est affiché lors d'une connexion échouée.

Par conséquent, notre chaîne `params` serait :

```bash
/:username=^USER^&password=^PASS^:F=Invalid credentials
```

- `"/"` : Le chemin où le formulaire est soumis.
- `username=^USER^&password=^PASS^` : Les paramètres du formulaire avec des espaces réservés pour Hydra.
- `F=Invalid credentials` : La condition d'échec – Hydra considérera une tentative de connexion comme infructueuse s'il voit cette chaîne dans la réponse.

Nous utiliserons [top-usernames-shortlist.txt](https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Usernames/top-usernames-shortlist.txt) pour la liste des noms d'utilisateur, et [2023-200_most_used_passwords.txt](https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt) pour la liste des mots de passe.

Cette chaîne `params` est intégrée dans la commande Hydra comme suit. Hydra substituera systématiquement `^USER^` et `^PASS^` par des valeurs de vos listes de mots, en envoyant des requêtes POST à la cible et en analysant les réponses pour la condition d'échec spécifiée. Si une tentative de connexion ne déclenche pas le message « Invalid credentials », Hydra la marquera comme un succès potentiel, révélant les identifiants valides.

```bash
# Télécharger les listes de mots si nécessaire

Hiterof13@htb[/htb]$ curl -s -O https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt

Hiterof13@htb[/htb]$ curl -s -O https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt # Commande Hydra

Hiterof13@htb[/htb]$ hydra -L top-usernames-shortlist.txt -P 2023-200_most_used_passwords.txt -f IP -s 5000 http-post-form "/:username=^USER^&password=^PASS^:F=Invalid credentials"  Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).  Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-09-05 12:51:14 [DATA] max 16 tasks per 1 server, overall 16 tasks, 3400 login tries (l:17/p:200), ~213 tries per task [DATA] attacking http-post-form://IP:PORT/:username=^USER^&password=^PASS^:F=Invalid credentials [5000][http-post-form] host: IP   login: ...   password: ... [STATUS] attack finished for IP (valid pair found) 1 of 1 target successfully completed, 1 valid password found Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-09-05 12:51:28
```

N'oubliez pas que la création de la bonne chaîne `params` est cruciale pour une attaque Hydra réussie. Des informations précises sur la structure et le comportement du formulaire sont essentielles pour construire cette chaîne efficacement. Une fois que Hydra a terminé l'attaque, connectez-vous au site web en utilisant les identifiants trouvés, et récupérez le flag.
---

← [[07 - Authentification HTTP de base]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[09 - Medusa]] →
