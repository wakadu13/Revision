---
tags:
  - brute-force
ordre: 4
---

# Attaques par dictionnaire

Bien que complète, l'approche par force brute (brute-force) peut être longue et gourmande en ressources, surtout face à des mots de passe complexes. C'est là que les attaques par dictionnaire (dictionary attacks) entrent en jeu.

## Le pouvoir des mots

L'efficacité d'une attaque par dictionnaire réside dans sa capacité à exploiter la tendance humaine à privilégier les mots de passe mémorisables plutôt que sécurisés. Malgré les avertissements répétés, de nombreuses personnes continuent d'opter pour des mots de passe basés sur des informations facilement accessibles telles que des mots du dictionnaire, des phrases courantes, des noms ou des motifs faciles à deviner. Cette prévisibilité les rend vulnérables aux attaques par dictionnaire, où les attaquants testent systématiquement une liste prédéfinie de mots de passe potentiels sur le système cible.

Le succès d'une attaque par dictionnaire dépend de la qualité et de la spécificité de la liste de mots (wordlist) utilisée. Une liste de mots bien conçue et adaptée au public ou au système cible peut augmenter de manière significative la probabilité d'une brèche réussie. Par exemple, si la cible est un système fréquenté par des joueurs, une liste de mots enrichie de terminologie et de jargon liés aux jeux vidéo se révélera plus efficace qu'un dictionnaire générique. Plus la liste de mots reflète fidèlement les choix de mots de passe probables de la cible, plus les chances de succès de l'attaque sont élevées.

À la base, le concept d'une attaque par dictionnaire est ancré dans la compréhension de la psychologie humaine et des pratiques courantes en matière de mots de passe. En tirant parti de cette connaissance, les attaquants peuvent casser efficacement des mots de passe qui nécessiteraient autrement une attaque par force brute d'une longueur prohibitive. Dans ce contexte, le pouvoir des mots réside dans leur capacité à exploiter la prévisibilité humaine et à compromettre des mesures de sécurité autrement robustes.

## Attaque par force brute vs. Attaque par dictionnaire

La distinction fondamentale entre une attaque par force brute et une attaque par dictionnaire réside dans leur méthodologie de génération de mots de passe potentiels :

- `Brute Force` : Une attaque par force brute pure teste systématiquement _toutes les combinaisons possibles_ de caractères dans un jeu et une longueur prédéterminés. Bien que cette approche garantisse un succès éventuel avec suffisamment de temps, elle peut être extrêmement longue, en particulier contre des mots de passe longs ou complexes.
- `Attaque par dictionnaire` : À l'inverse, une attaque par dictionnaire emploie une liste précompilée de mots et de phrases, réduisant considérablement l'espace de recherche. Cette méthodologie ciblée se traduit par une attaque beaucoup plus efficace et rapide, surtout lorsque le mot de passe cible est suspecté d'être un mot ou une phrase courante.

|Caractéristique|Attaque par dictionnaire|Attaque par force brute|Explication|
|---|---|---|---|
|`Efficacité`|Considérablement plus rapide et plus économe en ressources.|Peut être extrêmement longue et gourmande en ressources.|Les attaques par dictionnaire s'appuient sur une liste prédéfinie, réduisant de manière significative l'espace de recherche par rapport à la force brute.|
|`Ciblage`|Très adaptable et peut être personnalisée pour des cibles ou des systèmes spécifiques.|Aucune capacité de ciblage inhérente.|Les listes de mots peuvent intégrer des informations pertinentes pour la cible (ex: nom de l'entreprise, noms des employés), augmentant ainsi le taux de réussite.|
|`Efficacité`|Exceptionnellement efficace contre les mots de passe faibles ou couramment utilisés.|Efficace contre tous les mots de passe avec suffisamment de temps et de ressources.|Si le mot de passe cible se trouve dans le dictionnaire, il sera rapidement découvert. La force brute, bien qu'universellement applicable, peut être irréalisable pour les mots de passe complexes en raison du volume considérable de combinaisons.|
|`Limites`|Inefficace contre les mots de passe complexes et générés de manière aléatoire.|Souvent irréalisable pour les mots de passe longs ou très complexes.|Un mot de passe vraiment aléatoire a peu de chances de figurer dans un dictionnaire, ce qui rend cette attaque vaine. Le nombre astronomique de combinaisons possibles pour les mots de passe longs peut rendre les attaques par force brute infaisables.|

Considérons un scénario hypothétique où un attaquant cible le portail de connexion des employés d'une entreprise. L'attaquant pourrait construire une liste de mots spécialisée qui intègre les éléments suivants :

- Mots de passe faibles et couramment utilisés (ex: "password123", "qwerty")
- Le nom de l'entreprise et ses variantes
- Les noms des employés ou des départements
- Le jargon spécifique au secteur d'activité

En déployant cette liste de mots ciblée dans une attaque par dictionnaire, l'attaquant augmente considérablement ses chances de réussir à casser les mots de passe des employés par rapport à une tentative de force brute purement aléatoire.

## Créer et utiliser des listes de mots

Les listes de mots peuvent être obtenues à partir de diverses sources, notamment :

- `Listes publiquement disponibles` : Internet héberge une pléthore de listes de mots librement accessibles, comprenant des collections de mots de passe couramment utilisés, des identifiants divulgués lors de fuites de données (data breaches), et d'autres données potentiellement précieuses. Des dépôts comme [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Passwords) offrent diverses listes de mots adaptées à différents scénarios d'attaque.
- `Listes personnalisées` : Les testeurs d'intrusion (penetration testers) peuvent créer leurs propres listes de mots en exploitant les informations glanées lors de la phase de reconnaissance. Celles-ci peuvent inclure des détails sur les intérêts de la cible, ses loisirs, ses informations personnelles, ou toute autre donnée pouvant être utilisée pour la création de mots de passe.
- `Listes spécialisées` : Les listes de mots peuvent être affinées pour cibler des industries, des applications ou même des entreprises spécifiques. Ces listes spécialisées augmentent la probabilité de succès en se concentrant sur les mots de passe qui sont plus susceptibles d'être utilisés dans un contexte particulier.
- `Listes préexistantes` : Certains outils et frameworks sont livrés avec des listes de mots couramment utilisées. Par exemple, les distributions de test d'intrusion comme ParrotSec incluent souvent des listes de mots comme `rockyou.txt`, une collection massive de mots de passe divulgués, prête à l'emploi.

Voici un tableau de quelques-unes des listes de mots les plus utiles pour la force brute sur les identifiants de connexion :

|Liste de mots|Description|Usage typique|Source|
|---|---|---|---|
|`rockyou.txt`|Une liste de mots de passe populaire contenant des millions de mots de passe divulgués lors de la fuite de RockYou.|Couramment utilisée pour les attaques par force brute de mots de passe.|[Jeu de données de la fuite RockYou](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)|
|`top-usernames-shortlist.txt`|Une liste concise des noms d'utilisateur les plus courants.|Adaptée pour des tentatives rapides de force brute sur les noms d'utilisateur.|[SecLists](https://github.com/danielmiessler/SecLists/blob/master/Usernames/top-usernames-shortlist.txt)|
|`xato-net-10-million-usernames.txt`|Une liste plus complète de 10 millions de noms d'utilisateur.|Utilisée pour une force brute approfondie sur les noms d'utilisateur.|[SecLists](https://github.com/danielmiessler/SecLists/blob/master/Usernames/xato-net-10-million-usernames.txt)|
|`2023-200_most_used_passwords.txt`|Une liste des 200 mots de passe les plus couramment utilisés en 2023.|Efficace pour cibler les mots de passe couramment réutilisés.|[SecLists](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt)|
|`Default-Credentials/default-passwords.txt`|Une liste de noms d'utilisateur et de mots de passe par défaut couramment utilisés dans les routeurs, logiciels et autres appareils.|Idéale pour essayer les identifiants par défaut.|[SecLists](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/default-passwords.txt)|

## Lancer un dictionnaire sur le problème

**Pour suivre, démarrez le système cible via la section des questions en bas de la page.**

Copiez et collez le script Python ci-dessous sous le nom `dictionary-solver.py` sur votre machine. Vous n'avez qu'à modifier les variables IP et port pour qu'elles correspondent aux informations de votre système cible.

```python
import requests  ip = "127.0.0.1"  # Change this to your instance IP address port = 1234       # Change this to your instance port number  # Download a list of common passwords from the web and split it into lines passwords = requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/500-worst-passwords.txt").text.splitlines()  # Try each password from the list for password in passwords:     print(f"Attempted password: {password}")      # Send a POST request to the server with the password     response = requests.post(f"http://{ip}:{port}/dictionary", data={'password': password})      # Check if the server responds with success and contains the 'flag'     if response.ok and 'flag' in response.json():         print(f"Correct password found: {password}")         print(f"Flag: {response.json()['flag']}")         break
```

Le script Python orchestre l'attaque par dictionnaire. Il exécute les étapes suivantes :

1. `Télécharge la liste de mots` : Premièrement, le script récupère une liste de mots de 500 mots de passe couramment utilisés (et donc faibles) depuis SecLists en utilisant la bibliothèque `requests`.
2. `Itère et soumet les mots de passe` : Il parcourt ensuite chaque mot de passe de la liste de mots téléchargée. Pour chaque mot de passe, il envoie une requête POST au point de terminaison `/dictionary` de l'application Flask, en incluant le mot de passe dans les données du formulaire de la requête.
3. `Analyse les réponses` : Le script vérifie le code de statut de la réponse après chaque requête. S'il est 200 (OK), il examine plus en détail le contenu de la réponse. Si la réponse contient la clé "flag", cela signifie une connexion réussie. Le script affiche alors le mot de passe découvert et le flag capturé.
4. `Continue ou termine` : Si la réponse n'indique pas de succès, le script passe au mot de passe suivant dans la liste de mots. Ce processus se poursuit jusqu'à ce que le bon mot de passe soit trouvé ou que toute la liste de mots soit épuisée.

```bash
Hiterof13@htb[/htb]$ python3 dictionary-solver.py  ... Tentative de mot de passe : turtle Tentative de mot de passe : tiffany Tentative de mot de passe : golf Tentative de mot de passe : bear Tentative de mot de passe : tiger Mot de passe correct trouvé : ... Flag : HTB{...}
```

---

← [[03 - Attaques par force brute]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[05 - Attaques Hybrides]] →
