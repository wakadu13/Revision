---
tags:
  - brute-force
ordre: 11
---

# Listes de mots personnalisées

---

Bien que les listes de mots prédéfinies comme `rockyou` ou `SecLists` fournissent un vaste répertoire de mots de passe et de noms d'utilisateur potentiels, elles opèrent sur un large spectre, ratissant large dans l'espoir de trouver la bonne combinaison. Bien qu'efficace dans certains scénarios, cette approche peut être inefficiente et chronophage, surtout lorsqu'on cible des individus ou des organisations spécifiques ayant des schémas de mots de passe ou de noms d'utilisateur uniques.

Considérez le scénario où un pentester tente de compromettre le compte de « Thomas Edison » sur son lieu de travail. Une liste de noms d'utilisateur générique comme `xato-net-10-million-usernames-dup.txt` a peu de chances de donner des résultats significatifs. Étant donné les conventions de nom d'utilisateur potentielles appliquées par son entreprise, la probabilité que son nom d'utilisateur spécifique soit inclus dans un ensemble de données aussi massif est minimale. Celles-ci pourraient aller d'un format simple prénom/nom de famille à des combinaisons plus complexes comme nom de famille/trois premières lettres du prénom.

Dans de tels cas, la puissance des listes de mots personnalisées entre en jeu. Ces listes, méticuleusement élaborées et adaptées à la cible spécifique et à son environnement, augmentent considérablement l'efficacité et le taux de réussite des attaques par force brute (brute-force attacks). Elles exploitent les informations recueillies auprès de diverses sources, telles que les profils de réseaux sociaux, les annuaires d'entreprise, ou même les données divulguées, pour créer un ensemble ciblé et très pertinent de mots de passe et de noms d'utilisateur potentiels. Cette approche chirurgicale minimise les efforts inutiles et maximise les chances de pirater le compte cible.

## Username Anarchy

Même face à un nom aussi simple que « Jane Smith », la génération manuelle de noms d'utilisateur peut rapidement devenir une entreprise complexe. Bien que les combinaisons évidentes comme `jane`, `smith`, `janesmith`, `j.smith` ou `jane.s` puissent sembler adéquates, elles ne font qu'effleurer la surface du paysage potentiel des noms d'utilisateur.

La créativité humaine ne connaît pas de limites, et les noms d'utilisateur deviennent souvent une toile d'expression personnelle. Jane pourrait facilement y intégrer son deuxième prénom, son année de naissance ou un passe-temps favori, menant à des variations comme `janemarie`, `smithj87`, ou `jane_the_gardener`. L'attrait du `leetspeak`, où les lettres sont remplacées par des chiffres ou des symboles, pourrait se manifester dans des noms d'utilisateur comme `j4n3`, `5m1th`, ou `j@n3_5m1th`. Sa passion pour un livre, un film ou un groupe particulier pourrait inspirer des noms d'utilisateur comme `winteriscoming`, `potterheadjane`, ou `smith_beatles_fan`.

C'est là que `Username Anarchy` brille. Il prend en compte les initiales, les substitutions courantes, et plus encore, ratissant plus large dans votre quête pour découvrir le nom d'utilisateur de la cible :

```bash
Hiterof13@htb[/htb]$ ./username-anarchy -l  Plugin name             Example -------------------------------------------------------------------------------- first                   anna firstlast               annakey first.last              anna.key firstlast[8]            annakey first[4]last[4]         annakey firstl                  annak f.last                  a.key flast                   akey lfirst                  kanna l.first                 k.anna lastf                   keya last                    key last.f                  key.a last.first              key.anna FLast                   AKey first1                  anna0,anna1,anna2 fl                      ak fmlast                  abkey firstmiddlelast         annaboomkey fml                     abk FL                      AK FirstLast               AnnaKey First.Last              Anna.Key Last                    Key
```

D'abord, installez ruby, puis clonez le dépôt git de `Username Anarchy` pour obtenir le script :

```bash
Hiterof13@htb[/htb]$ sudo apt install ruby -y

Hiterof13@htb[/htb]$ git clone https://github.com/urbanadventurer/username-anarchy.git

Hiterof13@htb[/htb]$ cd username-anarchy
```

Ensuite, exécutez-le avec les prénom et nom de famille de la cible. Cela générera des combinaisons de noms d'utilisateur possibles.

```bash
Hiterof13@htb[/htb]$ ./username-anarchy Jane Smith > jane_smith_usernames.txt
```

En inspectant `jane_smith_usernames.txt`, vous rencontrerez un large éventail de noms d'utilisateur, comprenant :

- Combinaisons de base : `janesmith`, `smithjane`, `jane.smith`, `j.smith`, etc.
- Initiales : `js`, `j.s.`, `s.j.`, etc.
- etc.

Cette liste complète, adaptée au nom de la cible, est précieuse dans une attaque par force brute.

## CUPP

L'aspect du nom d'utilisateur étant traité, le prochain obstacle redoutable dans une attaque par force brute est le mot de passe. C'est là qu'intervient `CUPP` (Common User Passwords Profiler), un outil conçu pour créer des listes de mots de passe hautement personnalisées qui exploitent les renseignements collectés sur votre cible.

Poursuivons notre exploration avec Jane Smith. Nous avons déjà utilisé `Username Anarchy` pour générer une liste de noms d'utilisateur potentiels. Maintenant, utilisons CUPP pour compléter cela avec une liste de mots de passe ciblée.

L'efficacité de CUPP dépend de la qualité et de la profondeur des informations que vous lui fournissez. C'est un peu comme un détective qui reconstitue le profil d'un suspect - plus vous avez d'indices, plus l'image devient claire. Alors, où peut-on recueillir ces précieux renseignements pour une cible comme Jane Smith ?

- `Réseaux Sociaux` : Une mine d'or de détails personnels : anniversaires, noms d'animaux de compagnie, citations préférées, destinations de voyage, partenaires, et plus encore. Des plateformes comme Facebook, Twitter, Instagram et LinkedIn peuvent révéler une grande quantité d'informations.
- `Sites web d'entreprise` : Les sites web des employeurs actuels ou passés de Jane pourraient lister son nom, son poste, et même sa biographie professionnelle, offrant des aperçus sur sa vie professionnelle.
- `Registres publics` : Selon la juridiction et les lois sur la vie privée, les registres publics pourraient divulguer des détails sur l'adresse de Jane, les membres de sa famille, la propriété de biens, ou même d'anciens démêlés judiciaires.
- `Articles de presse et blogs` : Jane a-t-elle été mentionnée dans des articles de presse ou des billets de blog ? Ceux-ci pourraient éclairer ses intérêts, ses réalisations ou ses affiliations.

L'OSINT sera une mine d'or d'informations pour CUPP. Fournissez autant d'informations que possible ; l'efficacité de CUPP dépend de la profondeur de vos renseignements. Par exemple, disons que vous avez constitué ce profil à partir des publications Facebook de Jane Smith.

|Champ|Détails|
|---|---|
|Nom|Jane Smith|
|Surnom|Janey|
|Date de naissance|11 décembre 1990|
|Statut relationnel|En couple avec Jim|
|Nom du partenaire|Jim (Surnom : Jimbo)|
|Naissance du partenaire|12 décembre 1990|
|Animal de compagnie|Spot|
|Entreprise|AHI|
|Intérêts|Hackers, Pizza, Golf, Chevaux|
|Couleurs favorites|Bleu|

CUPP prendra alors vos entrées et créera une liste complète de mots de passe potentiels :

- Original et avec majuscule : `jane`, `Jane`
- Chaînes inversées : `enaj`, `enaJ`
- Variations de date de naissance : `jane1994`, `smith2708`
- Concaténations : `janesmith`, `smithjane`
- Ajout de caractères spéciaux : `jane!`, `smith@`
- Ajout de chiffres : `jane123`, `smith2024`
- Substitutions Leetspeak : `j4n3`, `5m1th`
- Mutations combinées : `Jane1994!`, `smith2708@`

Ce processus aboutit à une liste de mots hautement personnalisée, beaucoup plus susceptible de contenir le mot de passe réel de Jane que n'importe quel dictionnaire générique prêt à l'emploi ne pourrait jamais l'espérer. Cette approche ciblée augmente considérablement les chances de succès dans nos tentatives de craquage de mot de passe.

Si vous utilisez Pwnbox, CUPP est probablement pré-installé. Sinon, installez-le en utilisant :

```bash
Hiterof13@htb[/htb]$ sudo apt install cupp -y
```

Lancez CUPP en mode interactif. CUPP vous guidera à travers une série de questions sur votre cible, entrez les informations suivantes lorsqu'on vous le demande :

```bash
Hiterof13@htb[/htb]$ cupp -i  ___________    cupp.py!                 # Common       \                     # User        \   ,__,             # Passwords         \  (oo)____         # Profiler            (__)    )\               ||--|| *      [ Muris Kurgas
| j0rgan@remote-exploit.org ]                             [ Mebus
| https://github.com/Mebus/]
[+] Insert the information about the victim to make a dictionary
[+] If you don't know all the info, just hit enter when asked! ;)  > First Name: Jane > Surname: Smith > Nickname: Janey > Birthdate (DDMMYYYY): 11121990   > Partners) name: Jim > Partners) nickname: Jimbo > Partners) birthdate (DDMMYYYY): 12121990   > Child's name: > Child's nickname: > Child's birthdate (DDMMYYYY):   > Pet's name: Spot > Company name: AHI   > Do you want to add some key words about the victim? Y/[N]: y > Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed: hacker,blue > Do you want to add special chars at the end of words? Y/[N]: y > Do you want to add some random numbers at the end of words? Y/[N]:y > Leet mode? (i.e. leet = 1337) Y/[N]: y
[+] Now making a dictionary...
[+] Sorting list and removing duplicates...
[+] Saving dictionary to jane.txt, counting 46790 words.
[+] Now load your pistolero with jane.txt and shoot! Good luck!
```

Nous avons maintenant généré une liste de noms d'utilisateur (`jane_smith_usernames.txt`) et une liste de mots de passe (`jane.txt`), mais il y a encore une chose dont nous devons nous occuper. CUPP a généré de nombreux mots de passe possibles pour nous, mais l'entreprise de Jane, AHI, a une politique de mot de passe (password policy) assez étrange.

- Longueur minimale : 6 caractères
- Doit inclure :
    - Au moins une lettre majuscule
    - Au moins une lettre minuscule
    - Au moins un chiffre
    - Au moins deux caractères spéciaux (de l'ensemble `!@#$%^&*`)

Comme nous l'avons fait précédemment, nous pouvons utiliser grep pour filtrer cette liste de mots de passe afin qu'elle corresponde à cette politique :

```bash
Hiterof13@htb[/htb]$ grep -E '^.{6,}$' jane.txt
| grep -E '[A-Z]'
| grep -E '[a-z]'
| grep -E '[0-9]'
| grep -E '([!@#$%^&*].*){2,}' > jane-filtered.txt
```

Cette commande filtre efficacement `jane.txt` pour correspondre à la politique fournie, passant d'environ 46000 mots de passe à environ 7900. Elle assure d'abord une longueur minimale de 6 caractères, puis vérifie la présence d'au moins une lettre majuscule, une lettre minuscule, un chiffre, et enfin, au moins deux caractères spéciaux de l'ensemble spécifié. Les résultats filtrés sont stockés dans `jane-filtered.txt`.

Utilisez les deux listes générées dans Hydra contre la cible pour forcer par brute-force le formulaire de connexion. N'oubliez pas de changer les informations de la cible pour votre instance.

```bash
Hiterof13@htb[/htb]$ hydra -L jane_smith_usernames.txt -P jane-filtered.txt IP -s PORT -f http-post-form "/:username=^USER^&password=^PASS^:Invalid credentials"  Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these * ignore laws and ethics anyway).  Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-09-05 11:47:14 [DATA] max 16 tasks per 1 server, overall 16 tasks, 655060 login tries (l:14/p:46790), ~40942 tries per task [DATA] attacking http-post-form://IP:PORT/:username=^USER^&password=^PASS^:Invalid credentials [PORT][http-post-form] host: IP   login: ...   password: ... [STATUS] attack finished for IP (valid pair found) 1 of 1 target successfully completed, 1 valid password found Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-09-05 11:47:18
```

Une fois que Hydra a terminé l'attaque, connectez-vous au site web en utilisant les identifiants découverts et récupérez le flag.
---

← [[10 - Services Web]] | [[00 - Sommaire Login Brute Forcing|Sommaire]] | [[12 - Évaluation des compétences - Partie 2]] →
