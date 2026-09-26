---
tags:
  - brute-force
ordre: 5
---

# Attaques Hybrides

---

De nombreuses organisations mettent en place des politiques exigeant que les utilisateurs changent périodiquement leurs mots de passe pour renforcer la sécurité. Cependant, ces politiques peuvent involontairement engendrer des schémas de mots de passe prévisibles si les utilisateurs ne sont pas correctement formés à une bonne hygiène des mots de passe.

![Diagramme montrant le mot de passe original « Summer2023 » modifié en « Summer2023! » et « Summer2024 ».](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/57/2n.png)

Malheureusement, une pratique répandue et non sécurisée parmi les utilisateurs consiste à apporter des modifications mineures à leurs mots de passe lorsqu'ils sont contraints de les changer. Cela se manifeste souvent par l'ajout d'un chiffre ou d'un caractère spécial à la fin du mot de passe actuel. Par exemple, un utilisateur pourrait avoir un mot de passe initial comme « Summer2023 » puis, lorsqu'on lui demande de le mettre à jour, le changer en « Summer2023! » ou « Summer2024 ».

Ce comportement prévisible crée une faille que les attaques hybrides peuvent exploiter sans pitié. Les attaquants tirent parti de cette tendance humaine en employant des techniques sophistiquées qui combinent les forces des attaques par dictionnaire et des attaques par force brute, augmentant ainsi considérablement la probabilité de réussite des compromissions de mots de passe.

### Les Attaques Hybrides en Action

Illustrons cela avec un exemple pratique. Imaginons un attaquant ciblant une organisation connue pour imposer des changements de mot de passe réguliers.

![Organigramme montrant le processus d'attaque de mot de passe : l'organisation cible utilise des mots de passe courants et des termes du secteur ; l'attaquant effectue une reconnaissance, une attaque par dictionnaire et une attaque par force brute ciblant les comptes utilisateurs.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/57/3n.png)

L'attaquant commence par lancer une attaque par dictionnaire (dictionary attack), en utilisant une liste de mots (wordlist) composée de mots de passe courants, de termes spécifiques au secteur d'activité et potentiellement d'informations personnelles liées à l'organisation ou à ses employés. Cette phase tente d'identifier rapidement les cibles faciles - les comptes protégés par des mots de passe faibles ou faciles à deviner.

Cependant, si l'attaque par dictionnaire s'avère infructueuse, l'attaque hybride passe de manière transparente en mode de force brute (brute-force). Au lieu de générer aléatoirement des combinaisons de mots de passe, elle modifie stratégiquement les mots de la liste de mots originale, en ajoutant des chiffres, des caractères spéciaux, ou même en incrémentant des années, comme dans notre exemple « Summer2023 ».

Cette approche ciblée par force brute réduit considérablement l'espace de recherche par rapport à une attaque par force brute traditionnelle, tout en couvrant de nombreuses variations de mots de passe potentielles que les utilisateurs pourraient employer pour se conformer à la politique de changement de mot de passe.

### La Puissance des Attaques Hybrides

L'efficacité des attaques hybrides réside dans leur adaptabilité et leur efficience. Elles tirent parti des forces des techniques par dictionnaire et par force brute, maximisant les chances de casser les mots de passe, en particulier dans les scénarios où les utilisateurs tombent dans des schémas prévisibles.

Il est important de noter que les attaques hybrides ne se limitent pas au scénario de changement de mot de passe décrit ci-dessus. Elles peuvent être adaptées pour exploiter tout schéma de mot de passe observé ou suspecté au sein d'une organisation cible. Considérons un scénario où vous avez accès à une liste de mots de passe courants et que vous ciblez une organisation avec la politique de mot de passe suivante :

- Longueur minimale : 8 caractères
- Doit inclure :
    - Au moins une lettre majuscule
    - Au moins une lettre minuscule
    - Au moins un chiffre

Pour extraire uniquement les mots de passe qui respectent cette politique, nous pouvons tirer parti des puissants outils en ligne de commande disponibles par défaut sur la plupart des systèmes basés sur Linux/Unix, en particulier `grep` associé à des expressions régulières (regex). Nous allons utiliser pour cela la liste de mots de passe [darkweb2017-top10000.txt](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/darkweb2017_top-10000.txt). Tout d'abord, téléchargez la liste de mots.

```bash
Hiterof13@htb[/htb]$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/darkweb2017_top-10000.txt
```

Ensuite, nous devons commencer à faire correspondre cette liste de mots à la politique de mot de passe.

```bash
Hiterof13@htb[/htb]$ grep -E '^.{8,}$' darkweb2017_top-10000.txt > darkweb2017-minlength.txt
```

Cette première commande `grep` cible l'exigence principale de la politique, à savoir une longueur de mot de passe minimale de 8 caractères. L'expression régulière `^.{8,}$` agit comme un filtre, garantissant que seuls les mots de passe contenant au moins 8 caractères sont conservés et enregistrés dans un fichier temporaire nommé `darkweb2017-minlength.txt`.

```bash
Hiterof13@htb[/htb]$ grep -E '[A-Z]' darkweb2017-minlength.txt > darkweb2017-uppercase.txt
```

En s'appuyant sur le filtre précédent, cette commande `grep` applique l'exigence de la politique d'au moins une lettre majuscule. L'expression régulière `[A-Z]` garantit que tout mot de passe ne contenant pas de lettre majuscule est écarté, affinant davantage la liste enregistrée dans `darkweb2017-uppercase.txt`.

```bash
Hiterof13@htb[/htb]$ grep -E '[a-z]' darkweb2017-uppercase.txt > darkweb2017-lowercase.txt
```

En poursuivant la chaîne de filtrage, cette commande `grep` assure la conformité avec l'exigence de la politique d'au moins une lettre minuscule. L'expression régulière `[a-z]` sert de filtre, ne conservant que les mots de passe qui incluent au moins une lettre minuscule et les stockant dans `darkweb2017-lowercase.txt`.

```bash
Hiterof13@htb[/htb]$ grep -E '[0-9]' darkweb2017-lowercase.txt > darkweb2017-number.txt
```

Cette dernière commande `grep` s'attaque à l'exigence numérique de la politique. L'expression régulière `[0-9]` agit comme un filtre, garantissant que les mots de passe contenant au moins un chiffre sont conservés dans `darkweb2017-number.txt`.

```bash
Hiterof13@htb[/htb]$ wc -l darkweb2017-number.txt  89 darkweb2017-number.txt
```

Comme le montre la sortie ci-dessus, le filtrage méticuleux de la liste exhaustive de 10 000 mots de passe par rapport à la politique de mot de passe a considérablement réduit nos mots de passe potentiels à 89. Cette réduction drastique de l'espace de recherche représente un gain d'efficacité significatif pour toute tentative ultérieure de cassage de mot de passe. Une liste plus petite et ciblée se traduit par une attaque plus rapide et plus ciblée, optimisant l'utilisation des ressources de calcul et augmentant la probabilité d'une compromission réussie.

## Bourrage d'Identifiants : Tirer Parti des Données Volées pour un Accès Non Autorisé

![Organigramme montrant les sources d'identifiants comme les fuites de données et le phishing, menant à des actions de l'attaquant telles que l'acquisition d'identifiants et l'accès non autorisé, entraînant le vol de données et l'usurpation d'identité.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/57/5n.png)

Les attaques par bourrage d'identifiants (credential stuffing) exploitent la malheureuse réalité que de nombreux utilisateurs réutilisent leurs mots de passe sur plusieurs comptes en ligne. Cette pratique omniprésente, souvent motivée par le désir de commodité et la difficulté de gérer de nombreux identifiants uniques, crée un terrain fertile que les attaquants peuvent exploiter.

C'est un processus en plusieurs étapes qui commence par l'acquisition par les attaquants de listes de noms d'utilisateur et de mots de passe compromis. Ces listes peuvent provenir de fuites de données (data breaches) à grande échelle ou être compilées par le biais d'escroqueries par hameçonnage (phishing) et de logiciels malveillants. Notamment, des listes de mots publiquement disponibles comme `rockyou` ou celles trouvées dans `seclists` peuvent également servir de point de départ, offrant aux attaquants une mine de mots de passe couramment utilisés.

Une fois armés de ces identifiants, les attaquants identifient des cibles potentielles - des services en ligne susceptibles d'être utilisés par les individus dont ils possèdent les informations. Les réseaux sociaux, les fournisseurs de messagerie, les services bancaires en ligne et les sites de commerce électronique sont des cibles de choix en raison des données sensibles qu'ils détiennent souvent.

L'attaque passe alors à une phase automatisée. Les attaquants utilisent des outils ou des scripts pour tester systématiquement les identifiants volés contre les cibles choisies, imitant souvent le comportement normal des utilisateurs pour éviter la détection. Cela leur permet de tester rapidement un grand nombre d'identifiants, augmentant leurs chances de trouver une correspondance.

Une correspondance réussie accorde un accès non autorisé, ouvrant la porte à diverses activités malveillantes, du vol de données et de l'usurpation d'identité aux crimes financiers. Le compte compromis peut servir de rampe de lancement pour d'autres attaques, propageant des logiciels malveillants ou infiltrant des systèmes connectés.

### Le Problème de la Réutilisation des Mots de Passe

Le problème fondamental qui alimente le succès du bourrage d'identifiants est la pratique omniprésente de la réutilisation des mots de passe. Lorsque les utilisateurs se fient aux mêmes mots de passe, ou à des mots de passe similaires, pour plusieurs comptes, une compromission sur une plateforme peut avoir un effet domino, compromettant de nombreux autres comptes. Cela souligne le besoin urgent d'avoir des mots de passe forts et uniques pour chaque service en ligne, associé à des mesures de sécurité proactives comme l'authentification multifacteur.
---

← [[04 - Attaques par dictionnaire]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[06 - Hydra]] →
