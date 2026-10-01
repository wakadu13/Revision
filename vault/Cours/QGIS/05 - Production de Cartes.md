---
tags: [qgis, sig]
---
# Production de Cartes
Retour : [[00 - Sommaire QGIS]] · Précédent : [[04 - Représentation des Données]] · Suite : [[06 - Mise en Page]]

Ce chapitre présente les outils de représentation cartographique de QGIS permettant de faire parler les données attributaires : analyses thématiques (catégorisé, gradué, diagrammes), symboles proportionnels et gestion des étiquettes. L'objectif est de produire des cartes lisibles et pertinentes en fonction du message à transmettre.

## La représentation cartographique dans QGIS

Le style d'affichage d'une entité géographique (point, ligne ou polygone) peut dépendre soit d'une donnée attributaire (analyse thématique), soit d'un résultat calculé à partir d'une valeur numérique (variation de symbole).

Ces réglages sont accessibles :

- depuis l'onglet **Symbologie** des propriétés de la couche, pour les rendus **catégorisé**, **gradué** et **symboles proportionnels** ;
- depuis l'onglet **Diagrammes** des propriétés de la couche, pour les rendus **histogramme** et **diagramme en camembert**.

Le rendu **symbole unique** (vu dans un module précédent) affiche toutes les entités de la même façon. Les autres rendus disponibles sont :

| Rendu | Principe | Type de donnée |
|---|---|---|
| Catégorisé | Une couleur par valeur distincte d'un attribut | Alphanumérique (texte ou chiffre) |
| Gradué | Une couleur par plage (classe) de valeurs | Numérique |
| Histogramme | Barres juxtaposées, une par colonne numérique | Numérique |
| Diagramme en camembert | Secteurs proportionnels, un par colonne numérique | Numérique |

> [!note] Alphanumérique
> Un champ alphanumérique peut contenir des lettres et/ou des chiffres : en résumé, une colonne peut être une chaîne de caractères ou une valeur numérique, ce qui détermine si elle est utilisable en mode catégorisé (les deux) ou gradué (numérique uniquement).

Plusieurs analyses avancées existent dans QGIS (ensemble de règles, déplacement de point, groupe de points, carte de chaleur, point cluster, symboles intégrés, édition GRASS, diagramme texte) mais ne sont pas abordées dans cette formation d'initiation.

## Analyse thématique

### Les symboles catégorisés

Toutes les entités sont représentées par un symbole dont la couleur reflète la valeur d'un attribut donné (alphanumérique). Pour créer ce rendu :

1. Ouvrir les propriétés de la couche (ou le panneau de style ancré) ;
2. Dans l'onglet `Symbologie`, choisir le rendu **Catégorisé** ;
3. Sélectionner la colonne (`Valeur`) à utiliser, par exemple `NOM` ;
4. Cliquer sur **Classer** pour générer automatiquement une classe par valeur distincte, avec une palette de couleurs.

Chaque classe (symbole, valeur, légende) peut ensuite être modifiée manuellement, par exemple en double-cliquant sur son symbole.

### Les symboles gradués

Toutes les entités sont représentées par un symbole dont la couleur reflète la plage (tranche) à laquelle appartient la valeur d'un attribut numérique (par exemple la population `popul`).

La démarche est identique au mode catégorisé, mais :

- le **nombre de classes** est paramétrable (par exemple 5 classes) ;
- le **mode de calcul des tranches** est paramétrable (par exemple `Ruptures naturelles`, `Quantiles`...). Ces modes de calcul avancés sont détaillés dans la formation « perfectionnement ».

> [!tip] Modification directe d'une classe
> Il est possible de modifier directement la couleur d'une classe depuis le gestionnaire de couches, par clic droit sur la classe concernée, sans repasser par les propriétés de la couche.

### Les diagrammes

Les diagrammes se paramètrent depuis l'onglet **Diagrammes** des propriétés de la couche.

**Diagramme en camembert (ou graphique secteurs)**

Il représente plusieurs attributs numériques sous forme de secteurs d'un cercle. La taille du cercle de chaque entité est mise à l'échelle linéairement à partir d'un attribut auquel est affectée une taille maximum. Exemple : le champ `popul` définit le diamètre du cercle, et les champs population salariée / non salariée définissent les secteurs.

**Histogramme (ou graphique barres)**

Il représente plusieurs attributs numériques sous forme de barres accolées. Chaque barre est mise à l'échelle linéairement à partir d'un attribut auquel est affectée une taille maximum. Exemple : le champ `popul` définit la longueur de la barre de référence, les champs hommes/femmes salariés/non-salariés définissent les différentes barres.

**Diagrammes empilés (nouveauté QGIS 3.40)**

Ils permettent de visualiser sur une même entité plusieurs diagrammes accolés, horizontalement ou verticalement (par exemple des pyramides des âges), en combinant des sous-diagrammes de types différents (un camembert à côté d'un histogramme par exemple), chacun avec ses propres réglages de taille, de rendu et de légende. Cela offre une visualisation simultanée de plusieurs indicateurs par entité.

> [!tip] Légendes de diagrammes
> L'onglet `légende` des diagrammes permet de générer une légende complémentaire lorsque la taille du diagramme dépend d'une variable.

> [!question]- Exercice : analyse thématique avec symboles catégorisés ou gradués
> **Objectif** : représenter des objets par classe à l'aide de la symbologie.
>
> Ouvrir les couches vectorielles `IRIS_extrait72.shp`, `COMMUNE.shp` et `ROUTE.shp`, puis :
> - représenter les zones IRIS classées par nom (catégorisé) ;
> - représenter les communes par classe de valeur de population (5 classes, mode quantiles) ;
> - représenter les routes classées par nombre de voies (catégorisé).
>
> > [!example]- Corrigé
> > Pour la couche COMMUNE, choisir le rendu **Catégorisé** avec la colonne `Cl_admin`, classer, puis modifier manuellement les symboles (par exemple ligne jaune largeur 0,5 pour les départementales, ligne violette largeur 0,2 pour les autres). Activer les **Niveaux de symbole** (bouton `Avancé`) pour éviter les effets de segmentation des liaisons routières entre tronçons voisins.

## Symboles proportionnels

Cette technique fait varier la **taille** (et éventuellement d'autres caractéristiques) d'un symbole en fonction de la valeur d'un attribut, qui doit obligatoirement être numérique. Elle est **indépendante** du style de représentation utilisé (symbole unique, gradué, catégorisé) : elle vient s'ajouter au style choisi.

> [!warning] Attention à la lisibilité
> - Faire varier les symboles en fonction des attributs ajoute une dimension supplémentaire à la carte, qui doit rester compréhensible pour le lecteur et cohérente avec l'objectif de la carte.
> - La proportionnalité des symboles de lignes n'est **pas affichée dans la légende**, contrairement aux rendus catégorisés et gradués.

### Faire varier les caractéristiques des symboles

Pour faire varier un symbole en fonction des données attributaires, on utilise le bouton **« valeur définie par les données »** (icône en forme de petit signe égal/flèche) situé à côté du réglage à rendre variable (couleur, largeur de trait, taille...).

Exemple : affecter à une ligne représentant une route une largeur de trait proportionnelle à un attribut `LARGEUR`, `NB_VOIES` ou `trafic`. La source de données peut être affectée à la largeur globale du symbole composé ou à l'une de ses composantes (par exemple une ligne jaune et une ligne noire superposées).

**Ligne interpolée** (complément) : il est possible d'utiliser des lignes interpolées (sur la largeur ou la couleur) en remplacement de lignes simples, à condition de disposer d'une valeur de début et d'une valeur de fin dans la même table attributaire (exemple : couleur variant entre `Z_INI` et `Z_FIN` pour représenter une pente).

### Lignes avec épaisseur proportionnelle : Mise en pratique

Procédure type pour créer un symbole composé de deux lignes dont l'épaisseur varie :

1. Dupliquer la couche (clic droit → **Dupliquer la couche**), désactiver l'originale.
2. Repasser la couche dupliquée en **symbole unique** avec un symbole composé (par exemple `Topo main road`, formé d'une ligne claire et d'une ligne foncée superposées).
3. Cliquer sur la ligne claire → bouton **source de données** → **Éditer** → dans le constructeur d'expressions, saisir `"LARGEUR" / 2`.
4. Faire de même pour la ligne foncée avec `"LARGEUR" / 2 + 1`.
5. Conserver une largeur de trait exprimée en **millimètres**.

**Assistant de largeur (complément)** : le bouton de source de données propose un item **Assistant** qui permet de choisir un champ ou une expression, une méthode de calcul (**linéaire** ou **exponentielle décroissante**, facteur par défaut 0,57), ainsi que la taille de rendu en unité de carte et l'échelle des valeurs correspondantes.

### Cercles proportionnels sur une couche de polygones

Objectif type : représenter la population des communes sous forme d'un cercle proportionnel superposé au territoire de la commune. Cette technique combine deux fonctionnalités a priori indépendantes :

1. la possibilité de symboliser un polygone par son **centroïde** ;
2. la possibilité de paramétrer la **taille des points** en fonction d'un attribut.

**Procédure** :

1. Dans l'onglet `Symbologie`, ajouter une couche de symbole (bouton `+`).
2. Choisir **Remplissage de centroïde** pour la nouvelle couche de symbole (un point sera placé au centroïde du polygone), en conservant le remplissage simple de la surface d'origine.
3. Paramétrer la couleur du remplissage et de la bordure du point.
4. Cliquer sur le bouton **Source de définition des propriétés** pour la taille, puis choisir **Assistant de taille**.
5. Dans l'assistant, choisir le champ source (par exemple `POPULATION`), cliquer sur « charger la plage de valeurs depuis la couche », puis définir la taille de sortie (par exemple entre 1 et 40 mm).
6. Choisir la **méthode de calcul** de taille : `Flannery` est recommandée pour rendre les tailles mieux perceptibles visuellement (un certain M. Flannery a établi qu'un exposant de 0,57 rend mieux compte de notre perception des surfaces qu'une simple racine carrée).

> [!warning] Piège du calcul de taille « brut »
> Un calcul de taille proportionnel directement à la valeur (diamètre = n pixels/valeur) surreprésente fortement les grandes valeurs à l'écran, car le cerveau interprète une quantité en fonction de la surface d'un dessin, pas de sa longueur. Il faut préférer une méthode de calcul de type racine carrée (surface) ou la compensation Flannery, sauf pour des variables déjà normalisées (rarement des écarts type).

**Gérer les superpositions** : quand les cercles se chevauchent (grandes valeurs), il faut régler les **niveaux de symboles** :

1. Dans la fenêtre de style de la couche, cliquer sur **Avancé** (en bas à droite de la liste des styles), en s'assurant que la ligne `Fill` (remplissage) est sélectionnée dans la liste des symboles.
2. Choisir **Niveaux de symbole**, cocher **Activer les niveaux de symbole**.
3. Par défaut, l'ordre est correct : couche 0 = surfaces, couche 1 = cercles.

On peut aussi améliorer la lisibilité de l'ensemble en réglant le **mode de fusion** entre entités sur `Multiplier` (onglet Rendu de la couche).

### Exemple : carte de flux

QGIS permet de représenter des symboles de lignes sous forme de **flèches**, utile pour des cartes de flux ou de mouvements de population.

Procédure : ouvrir la couche de lignes (par exemple `mouv_popul.shp`), double-cliquer sur la couche → onglet `Symbologie`, choisir un symbole composé **Ligne** + **Flèche** (type de symbole `Flèche`), puis rendre variables :

- la **largeur de la flèche** : expression `"Mouvement" / 10` ;
- la **longueur de pointe** et l'**épaisseur de pointe** avec la même valeur ;
- ajouter éventuellement un effet d'ombre portée et choisir une couleur de remplissage/contour.

## Étiquettes

### Les étiquettes

Le paramétrage de l'étiquetage d'une couche vectorielle sélectionnée se fait :

- via le bouton `Étiquettes` (icône `abc`) de la barre d'outils Étiquettes ;
- via l'onglet `Étiquettes` des propriétés de la couche ;
- via le **panneau ancrable de style de couche** (fortement conseillé : il regroupe tous les paramètres de la couche et permet de gagner en productivité).

Dans le menu déroulant, choisir **Étiquette simple** puis sélectionner le champ à afficher (ou une expression, via le bouton `ε`).

Les autres modes disponibles :

| Mode | Effet |
|---|---|
| Pas d'étiquette | Désactive l'étiquetage de la couche |
| Étiquette simple | Un seul champ ou une expression pour toutes les entités |
| Étiquettes basées sur des règles | Filtre l'étiquetage selon des expressions, avec plusieurs configurations possibles |
| Bloquant | Définit la couche comme un obstacle aux étiquettes des autres couches |

**Le moteur d'étiquettes** propose plusieurs sous-menus de paramétrage, communs (avec quelques variantes selon points/lignes/polygones, notamment le menu `Position`) :

| Sous-menu | Rôle |
|---|---|
| Texte | Style du texte, casse des lettres, texte de substitution |
| Formatage | Retour à la ligne (`\n` par défaut), formatage des nombres |
| Tampon | Halo autour du texte, couleur, mode de fusion |
| Masque (fond) | Fond de forme, taille, rotation, décalage, couleur |
| Arrière-plan | Fond carré, rectangle, ellipse, cercle, symbole SVG ou marqueur |
| Ombre | Ombre portée personnalisable (décalage, rayon, couleur, fusion) |
| Connecteurs | Traits de rappel entre l'étiquette et son point d'ancrage |
| Position | Position de l'étiquette et priorités d'étiquetage, coordonnées/rotation par champ ou expression |
| Rendu | Visibilité selon l'échelle, nombre maximum d'étiquettes, gestion des conflits de superposition |

> [!important] Icône de valeur définie par les données
> L'icône `≡` présente dans tous ces menus permet d'utiliser des valeurs définies par les champs de la couche ou par des expressions.

**Étiquetage basé sur des règles** : pour filtrer l'affichage des étiquettes, choisir **Étiquettes basées sur des règles** puis ajouter une règle (bouton `+`) avec un titre descriptif et une expression filtre (exemple : `"POPULATION" > 1000`). Le bouton `test` vérifie le nombre d'entités filtrées. Une règle sans filtre (case `Else` ou expression `ELSE`) permet de traiter les entités n'ayant satisfait aucune règle précédente, avec un rendu différent (par exemple une taille de police plus petite).

**Formatage HTML des étiquettes** : l'option `Permettre le formatage HTML` (onglet Texte) autorise l'usage de balises HTML dans l'expression, par exemple pour afficher des couleurs variables selon le texte :
```
'<span style="color:red">' || "NOM_COMM" || '</span>' || '<span style="color:blue">' || ' : ' || "POPULATION" || ' habitants' || '</span>'
```

Il est possible d'**afficher ou masquer** les étiquettes d'une couche via un clic droit sur la couche dans le gestionnaire → **Afficher les étiquettes**.

> [!question]- Exercice : barre d'outils Étiquettes
> **Objectif** : étiqueter les objets d'une couche et définir les paramètres de position dans les données auxiliaires.
>
> Ouvrir `ROUTE.SHP`, représenter les routes départementales avec l'étiquetage du numéro de route, puis affiner l'affichage en masquant les étiquettes superflues. Sauvegarder le style sous le nom `ROUTE_EXO14.qml`.
>
> > [!example]- Corrigé
> > - Définir un rendu **catégorisé** sur `CL_ADMIN` (ligne jaune 0,5 et orange 1,2 pour les départementales, violette 0,2 pour les autres), activer les niveaux de symbole.
> > - Ajouter une règle d'étiquetage filtrée sur `"CL_ADMIN" = 'Départementale' AND $length > 130` (`$length` calcule la longueur de la ligne), étiqueter avec le champ `NUMERO`.
> > - Paramétrer le texte : police Arial, taille 9, couleur noire ; arrière-plan rectangle avec remplissage jaune et bordure orange (largeur 0,3 mm) ; position **parallèle**, distance 1,6 mm.
> > - Utiliser l'outil **Afficher/masquer les étiquettes** pour masquer certaines étiquettes à la souris (clic+shift), et l'option **Fusionner les lignes connectées** (menu Rendu) pour éviter les doublons.
> > - Sauvegarder le style via `Symbologie` → **Enregistrer le style sous** `ROUTE_EXO14.qml`.

> [!tip] À retenir
> QGIS propose trois familles de représentation cartographique : les analyses thématiques (catégorisé, gradué, diagrammes) pour visualiser des valeurs attributaires, les symboles proportionnels (taille ou épaisseur variable) pour visualiser des quantités numériques, et l'étiquetage pour afficher du texte contextuel. Ces techniques se combinent (par exemple symbologie catégorisée + largeur de trait proportionnelle) mais doivent toujours rester au service de la lisibilité de la carte.
