---
tags:
  - brute-force
ordre: 1
---

# Introduction

Les clés et les mots de passe, équivalents modernes des serrures et des combinaisons, sécurisent le monde numérique. Mais que se passerait-il si quelqu'un essayait toutes les combinaisons possibles jusqu'à trouver celle qui ouvre la porte ? C'est, en substance, ce qu'on appelle une `attaque par force brute`.

## Qu'est-ce qu'une attaque par force brute ?

En cybersécurité, une attaque par force brute (brute forcing) est une méthode par essais et erreurs utilisée pour casser des mots de passe, des identifiants de connexion ou des clés de chiffrement. Elle consiste à essayer systématiquement toutes les combinaisons de caractères possibles jusqu'à trouver la bonne. Le processus peut être comparé à un voleur qui essaierait chaque clé d'un trousseau géant jusqu'à trouver celle qui ouvre le coffre au trésor.

Le succès d'une attaque par force brute dépend de plusieurs facteurs, notamment :

- La `complexité` du mot de passe ou de la clé. Les mots de passe plus longs avec un mélange de lettres majuscules et minuscules, de chiffres et de symboles sont exponentiellement plus complexes à casser.
- La `puissance de calcul` (computational power) dont dispose l'attaquant. Les ordinateurs modernes et le matériel spécialisé peuvent essayer des milliards de combinaisons par seconde, réduisant considérablement le temps nécessaire à une attaque réussie.
- Les `mesures de sécurité` en place. Les verrouillages de compte, les CAPTCHA et autres défenses peuvent ralentir, voire contrecarrer, les tentatives d'attaques par force brute.

## Comment fonctionne une attaque par force brute

Le processus d'une attaque par force brute peut être visualisé comme suit :

![Organigramme montrant le processus : Démarrer, générer une combinaison, appliquer la combinaison, vérifier le succès, accès accordé en cas de succès.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/57/1n.png)

1. `Start` : L'attaquant lance le processus d'attaque par force brute, souvent à l'aide d'un logiciel spécialisé.
2. `Generate Possible Combination` : Le logiciel génère une combinaison potentielle de mot de passe ou de clé en fonction de paramètres prédéfinis, tels que les jeux de caractères et la longueur.
3. `Apply Combination` : La combinaison générée est testée sur le système cible, tel qu'un formulaire de connexion ou un fichier chiffré.
4. `Check if Successful` : Le système évalue la combinaison testée. Si elle correspond au mot de passe ou à la clé stocké(e), l'accès est accordé. Sinon, le processus continue.
5. `Access Granted` : L'attaquant obtient un accès non autorisé au système ou aux données.
6. `End` : Le processus se répète, générant et testant de nouvelles combinaisons jusqu'à ce que la bonne soit trouvée ou que l'attaquant abandonne.

## Types d'attaques par force brute

L'attaque par force brute n'est pas une entité monolithique mais un ensemble de techniques diverses, chacune ayant ses forces, ses faiblesses et ses cas d'utilisation idéaux. Comprendre ces variations est crucial tant pour les attaquants que pour les défenseurs, car cela permet aux premiers de choisir l'approche la plus efficace et aux seconds de mettre en œuvre des contre-mesures ciblées. Le tableau suivant offre un aperçu comparatif des différentes méthodes d'attaque par force brute :

|Méthode|Description|Exemple|Idéalement utilisé lorsque...|
|---|---|---|---|
|`Simple Brute Force`|Tente systématiquement toutes les combinaisons de caractères possibles au sein d'un jeu de caractères et d'une plage de longueurs définis.|Essayer toutes les combinaisons de lettres minuscules de 'a' à 'z' pour des mots de passe de 4 à 6 caractères.|Aucune information préalable sur le mot de passe n'est disponible, et les ressources de calcul sont abondantes.|
|`Dictionary Attack`|Utilise une liste précompilée de mots, d'expressions et de mots de passe courants.|Essayer des mots de passe d'une liste comme 'rockyou.txt' contre un formulaire de connexion.|La cible est susceptible d'utiliser un mot de passe faible ou facile à deviner, basé sur des modèles courants.|
|`Hybrid Attack`|Combine des éléments d'attaques par force brute simple et d'attaques par dictionnaire, en ajoutant souvent des caractères avant ou après les mots du dictionnaire.|Ajouter des chiffres ou des caractères spéciaux à la fin des mots d'une liste de dictionnaire.|La cible pourrait utiliser une version légèrement modifiée d'un mot de passe courant.|
|`Credential Stuffing`|Exploite des identifiants divulgués d'un service pour tenter d'accéder à d'autres services, en supposant que les utilisateurs réutilisent leurs mots de passe.|Utiliser une liste de noms d'utilisateur et de mots de passe divulgués lors d'une fuite de données pour essayer de se connecter à divers comptes en ligne.|Un grand ensemble d'identifiants divulgués est disponible, et la cible est suspectée de réutiliser ses mots de passe sur plusieurs services.|
|`Password Spraying`|Tente un petit ensemble de mots de passe couramment utilisés contre un grand nombre de noms d'utilisateur.|Essayer des mots de passe comme 'password123' ou 'qwerty' contre tous les noms d'utilisateur d'une organisation.|Des politiques de verrouillage de compte sont en place, et l'attaquant cherche à éviter la détection en répartissant les tentatives sur plusieurs comptes.|
|`Rainbow Table Attack`|Utilise des tables précalculées de hachages de mots de passe pour inverser les hachages et retrouver rapidement les mots de passe en clair.|Précalculer les hachages pour tous les mots de passe possibles d'une certaine longueur et d'un certain jeu de caractères, puis comparer les hachages capturés avec la table pour trouver des correspondances.|Un grand nombre de hachages de mots de passe doivent être cassés, et l'espace de stockage pour les tables arc-en-ciel est disponible.|
|`Reverse Brute Force`|Cible un seul mot de passe contre plusieurs noms d'utilisateur, souvent utilisé en conjonction avec des attaques de type credential stuffing.|Utiliser un mot de passe divulgué d'un service pour essayer de se connecter à plusieurs comptes avec des noms d'utilisateur différents.|Il existe une forte suspicion qu'un mot de passe particulier est réutilisé sur plusieurs comptes.|
|`Distributed Brute Force`|Répartit la charge de travail de l'attaque par force brute sur plusieurs ordinateurs ou appareils pour accélérer le processus.|Utiliser un cluster d'ordinateurs pour effectuer une attaque par force brute augmente considérablement le nombre de combinaisons pouvant être testées par seconde.|Le mot de passe ou la clé cible est très complexe, et une seule machine n'a pas la puissance de calcul nécessaire pour le casser dans un délai raisonnable.|

## Le rôle de l'attaque par force brute dans les tests d'intrusion

Le test d'intrusion (penetration testing), ou piratage éthique (ethical hacking), est une mesure de cybersécurité proactive qui simule des attaques réelles pour identifier et corriger les vulnérabilités avant que des acteurs malveillants ne puissent les exploiter. L'attaque par force brute est un outil crucial dans ce processus, en particulier pour évaluer la résilience des mécanismes d'authentification basés sur les mots de passe.

Bien que les tests d'intrusion englobent un éventail de techniques, l'attaque par force brute est souvent employée de manière stratégique lorsque :

- `Les autres pistes sont épuisées` : Les tentatives initiales pour obtenir un accès, comme l'exploitation de vulnérabilités connues ou l'utilisation de tactiques d'ingénierie sociale (social engineering), peuvent s'avérer infructueuses. Dans de tels scénarios, l'attaque par force brute est une alternative viable pour surmonter les barrières de mots de passe.
- `Les politiques de mots de passe sont faibles` : Si le système cible applique des politiques de mots de passe laxistes, il est plus probable que les utilisateurs aient des mots de passe faibles ou faciles à deviner. L'attaque par force brute peut exposer efficacement ces vulnérabilités.
- `Des comptes spécifiques sont ciblés` : Dans certains cas, les testeurs d'intrusion peuvent se concentrer sur la compromission de comptes d'utilisateurs spécifiques, comme ceux disposant de privilèges élevés. L'attaque par force brute peut être adaptée pour cibler directement ces comptes.
---

[[00 - Sommaire Login Brute Forcing|Sommaire]] | [[02 - Les principes fondamentaux de la sécurité des mots de passe]] →
