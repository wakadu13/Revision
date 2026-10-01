---
tags: [qgis, sig]
---
# Représentation des Données
Retour : [[00 - Sommaire QGIS]] · Précédent : [[03 - Navigation et Sélections Graphiques]] · Suite : [[05 - Production de Cartes]]

La manière dont les données d'une carte sont représentées est essentielle à la compréhension du message que l'on veut faire passer. Ce chapitre rappelle les grandes règles de la sémiologie graphique, puis détaille la symbologie de QGIS pour les couches vecteur et raster, et présente les modes de fusion qui permettent d'améliorer le rendu visuel des cartes.

## Rappel sur la sémiologie graphique

Selon Jacques Bertin, la **sémiologie graphique** est « l'ensemble des règles d'un système graphique de signes pour la transmission d'une information ». C'est un système de signes rigoureux et simple qui utilise les propriétés du plan pour faire apparaître les relations de ressemblance, d'ordre ou de proportionnalité entre des ensembles de données.

Réussir une carte, c'est réaliser l'adéquation entre un message à transmettre et sa représentation graphique. Trois **règles d'or** doivent être respectées :

- **simplifier** : en regroupant les données, en épurant les symboles, en supprimant les signes brouilleurs, en séparant les données, en jouant sur les similitudes ;
- **hiérarchiser** : en dégageant l'information principale, en fournissant des points de repère ;
- **normaliser** : en utilisant une seule police de caractères, en plaçant titres et légendes aux mêmes endroits, en utilisant des formes et des échelles identiques.

## Présentation de la symbologie de QGIS

La symbologie de QGIS repose sur **3 types de symboles de base**, selon la géométrie des entités :

1. des **P**oints (ou marqueurs) ;
2. des **L**ignes ;
3. des **S**urfaces (ou remplissages, pour les polygones).

Un symbole complexe peut être composé de **plusieurs couches de symboles de base** superposées : par exemple, un marqueur de point peut être la superposition de deux symboles de police décalés, une ligne « autoroute » peut être composée de deux lignes simples superposées, et un polygone peut combiner un remplissage simple et une trame de motifs.

### Types de symboles disponibles

**Pour les points**, on trouve notamment : symbole animé (GIF, WebP, MNG…), symbole ellipse, symbole remplissage, symbole de police (caractère d'une police installée), générateur de géométries, masque, symbole d'image raster, symbole simple, symbole SVG, symbole de champ vectoriel.

**Pour les lignes** : flèches (cartes de flux), générateur de géométrie, ligne hachurée, ligne interpolée (couleur/largeur variant entre un attribut de début et de fin), dégradé de ligne, ligne de symboles (répétition d'un marqueur le long de la ligne), ligne raster, ligne simple.

**Pour les surfaces (polygones)** : remplissage de centroïdes, générateur de géométrie, remplissage en dégradé, motif de lignes, motif de points, remplissage de marqueurs aléatoires, remplissage image raster, remplissage SVG, remplissage en dégradé suivant la forme, remplissage simple, et les mêmes options déclinées pour la **bordure** (flèches, ligne hachurée, ligne interpolée, dégradé, ligne de symboles, ligne raster, ligne simple).

> [!info] Symboles variables selon les attributs
> Il est possible de faire varier le symbole en fonction des données attributaires (petit bouton en forme de flèche à côté de nombreux paramètres) : couleur, taille, rotation, etc. peuvent ainsi dépendre de la valeur prise par un champ. Ce point est approfondi au module suivant, « Production de cartes », au paragraphe « Symboles proportionnels ».

### Les palettes de couleurs

Pour les rendus **gradués** ou **catégorisés** (vus plus loin), on peut utiliser des palettes de couleurs. Plusieurs types de palettes sont disponibles :

1. **Dégradé** : un dégradé linéaire d'une couleur à l'autre ;
2. **Préréglage de couleurs** : une liste de couleurs choisies (depuis QGIS 3.0) ;
3. **Aléatoire** : couleurs générées à partir d'un espace de couleur (Teinte, Saturation, Luminosité — TSL) ;
4. **Catalogue cpt-city** : bibliothèque de plus de 1100 palettes classées par thèmes ;
5. **Catalogue Palette de couleur (ColorBrewer)** : création d'un espace de couleur depuis un schéma prédéfini (séquentiel, divergent…).

### Le choix des couleurs dans QGIS

Pour choisir une couleur (par exemple de remplissage), QGIS propose une **roue colorimétrique**, une **jauge de transparence**, un accès aux **couleurs récentes**, aux **couleurs standard** (définies dans Préférences -> Options -> Onglet couleurs, ou dans les propriétés du projet), et une **pipette** pour piocher une couleur affichée n'importe où sur l'écran. La boîte de dialogue « Choisir la couleur » permet également de saisir une notation HTML (`#RRGGBB`) ou de régler Teinte/Saturation/Valeur/RVB avec des curseurs (utilisables aussi à la molette de la souris). Les couleurs peuvent être importées/exportées sous forme de fichier `.gpl`.

### Gestion de la symbologie

Le **gestionnaire de style** (menu **Préférences -> Gestionnaire de style**, ou onglet **Style** des propriétés de couche) permet d'ajouter, supprimer, éditer, exporter (format XML) ou importer les marqueurs, lignes, remplissages et palettes de couleurs utilisés dans QGIS. Les symboles peuvent être organisés en groupes via des **mots-clés (tags)** ou des **groupes intelligents** (smart groups), qui rassemblent dynamiquement les symboles répondant à une ou plusieurs conditions sur leur nom ou leurs mots-clés.

Un symbole est décrit sous forme d'une **arborescence** de symboles de base, à partir d'une racine appelée `marker` (points), `line` (lignes) ou `fill` (remplissage). Des boutons permettent de rajouter, supprimer, monter/descendre, dupliquer ou verrouiller la couleur d'un niveau de l'arborescence. Le **cadenas** sert à figer la couleur d'un symbole de base pour qu'elle ne soit pas modifiée quand on change la couleur « globale » du symbole composé.

Il est également possible de définir plusieurs **styles nommés pour une même couche** (clic droit sur la couche -> Styles -> Ajouter…) et de basculer facilement de l'un à l'autre.

> [!info] Sauvegarde du style
> Le bouton **Style** (bas de la fenêtre des propriétés) permet de **charger** un style précédemment enregistré (fichier `.qml`), de l'**enregistrer** (formats QML ou SLD), de l'**enregistrer par défaut** (fichier `nom-de-la-couche.qml` au même endroit que la couche, chargé automatiquement à l'ouverture de la couche) ou de **restaurer le style par défaut**. Le projet `.qgs` enregistre également les styles des couches qu'il utilise.

Un **panneau ancrable « style de couche »** (activable depuis la bannière du gestionnaire de couches) permet de rester visible en permanence, y compris hors de la fenêtre QGIS (utile en double écran), avec mise à jour immédiate si la case **« Mise à jour en direct »** est cochée. Il reprend 6 onglets (symbologie, étiquettes, masques, vue 3D, shading renderer, gestionnaire de style et historique) et conserve un **historique complet** des modifications appliquées, avec boutons annuler/refaire.

## Représentation des couches vecteurs

### Style de représentation d'une couche vecteur

L'onglet **Symbologie** des propriétés de couche permet de visualiser et modifier le style utilisé pour représenter la donnée. La fenêtre se compose de 3 parties :

1. la partie supérieure, où l'on choisit le **type de rendu** (symbole unique, catégorisé, gradué…) et les caractéristiques du symbole ;
2. une partie inférieure permettant de régler la **transparence** de la couche, son **mode de fusion**, ses **effets**, le contrôle du rendu des entités ;
3. un bouton de gestion des **styles**.

#### Transparence et mode de fusion

L'**opacité** de la couche va de 0 % (couche totalement transparente) à 100 % (couche totalement opaque, cache ce qui se trouve en dessous). Le **mode de fusion** prend par défaut la valeur « Normal » : les couches sont simplement superposées comme des calques, seule leur transparence conditionne l'affichage. Les autres modes de fusion sont détaillés plus loin dans ce chapitre.

#### Type de rendu

Le bouton de choix du type de rendu propose :

| Type de rendu | Principe |
|---|---|
| Pas de symbole | Aucune représentation |
| Symbole Unique | Toutes les entités sont représentées de manière identique |
| Catégorisé | Un symbole défini par l'utilisateur reflète les valeurs discrètes d'un champ ou d'une expression |
| Gradué | La couleur ou la taille du symbole varie selon la classe de valeur d'un attribut |
| Ensemble de règles | Les entités sont discriminées selon leurs attributs/propriétés, avec des règles imbricables |
| Déplacement de point | Regroupe les entités ponctuelles proches en écartant leurs symboles autour d'un barycentre commun |
| Groupe de points | Fusionne les points proches en un seul symbole rendu |
| Carte de chaleur | Crée une carte de chaleur dynamique à partir d'une couche de points |
| Polygones inversés | Applique un symbole à l'extérieur des polygones de la couche |
| 2.5 D | Représentation avec effet de perspective |
| Symboles intégrés / Édition GRASS | Rendus spécifiques |

Par défaut, QGIS propose un **symbole unique**, dont l'aspect dépend du type de géométrie (marqueur pour les points, ligne pour les polylignes, remplissage pour les polygones).

#### Caractéristiques du style utilisé

Les commandes de cette partie permettent de choisir le **symbole**, sa **couleur**, sa **taille** et sa **transparence** (à ne pas confondre avec la transparence globale de la couche). Pour représenter un point, on peut choisir parmi une liste de symboles disponibles et/ou composer son propre symbole comme superposition de symboles simples : cliquer sur la ligne « symbole » revient à l'affichage des symboles disponibles ; cliquer sur « Symbole simple » permet de le modifier ; les boutons `+`, `-`, haut, bas permettent d'ajouter, supprimer ou réordonner les niveaux du symbole composé. Le même principe s'applique aux lignes (« Ligne ») et aux surfaces (« Fill »), chacune pouvant être la résultante de plusieurs sous-symboles superposés.

Le bouton **Enregistrer le symbole** permet de sauvegarder directement le symbole créé sous un nom, éventuellement classé par mots-clés dans le gestionnaire de style.

### Niveau de symboles

Lorsqu'un symbole est composé de plusieurs couches de symboles élémentaires, l'ordre d'affichage de ces couches peut créer des effets de bord indésirables (segmentation des lignes, superposition aléatoire aux intersections). Le bouton **Avancé -> Niveaux de symbole** (en bas à droite de la fenêtre de symbologie) permet d'activer et de contrôler cet ordre.

Dans la fenêtre « Niveaux de symbole », chaque ligne correspond à une catégorie de symbole composé, et chaque colonne (« Couche 0 », « Couche 1»…) représente le niveau de chacun de ses symboles élémentaires, tel qu'ils ont été définis dans le gestionnaire de symboles. Le numéro saisi dans chaque cellule définit l'ordre dans lequel les symboles élémentaires sont dessinés (du niveau le plus bas au plus haut, les niveaux supérieurs recouvrant les inférieurs). Pour un réseau routier par exemple, activer les niveaux de symboles permet de garantir qu'une route départementale (dessinée en dernier, donc au-dessus) reste visible et continue aux intersections, plutôt que d'afficher un désordre apparent dû à un ordre de tracé aléatoire des tronçons.

## Représentation d'une couche raster

### Les différents types de couches raster

Une couche raster correspond à une matrice de cellules (pixels) rectangulaires de même dimension représentant des objets. Les données raster typiques sont :

- les **cartes scannées** et les **orthophotos** aériennes ou satellitaires, pour lesquelles chaque pixel correspond à une cellule de base de la matrice ;
- les **modèles numériques de terrain** (format ASC), où la cellule de base correspond à la maille élémentaire portant l'altitude.

QGIS propose quatre types de rendu selon le type de données, en particulier selon qu'il s'agit d'images à bandes multiples ou à bande unique :

- **Couleur à bandes multiples** : les photographies aériennes et satellitaires sont codées pour chaque pixel par un triplet de valeurs (modèle RVB). On parle d'**images à 3 bandes** (par exemple la BD Ortho « couleur » : bande 1 = rouge, bande 2 = vert, bande 3 = bleu ; la BD Ortho IRC infrarouge couleur inverse l'ordre : bande 1 = infrarouge, bande 2 = rouge, bande 3 = vert). Certaines images satellitaires (RapidEye) comportent 5 bandes spectrales (bleu, vert, rouge, rededge, proche infrarouge). Un écran ne pouvant afficher que 3 couleurs primaires, il faut choisir quelles bandes seront affichées sur le rouge, le vert et le bleu.
- **Palette / valeurs uniques** : rendu standard pour les couches raster à **une seule bande** possédant déjà une palette de couleurs interne (une couleur précise assignée à chaque valeur de pixel), typiquement les cartes scannées.
- **Bande grise unique** : représente une couche raster à une seule bande avec un dégradé de gris (du blanc au noir, ou l'inverse). Rendu fréquemment utilisé pour les modèles numériques de terrain.
- **Pseudo-couleur à bande unique** : rendu utilisé pour les couches à une seule bande, en définissant une palette continue de « pseudo-couleurs » (qui ne sont pas les vraies couleurs des pixels), utile pour représenter un MNT de manière plus lisible.

> [!warning] Modification du rendu des couches raster
> Il n'est pas toujours possible ou pertinent de modifier la représentation d'une couche raster, certains types de rendu n'étant pas compatibles avec toutes les données même si la commande semble exécutable. Modifications utiles courantes : paramétrer les bandes affichées pour une couche multi-bandes, isoler une seule bande, modifier la gamme de couleur d'un rendu de type palette, ou appliquer une palette continue à un fichier représenté par défaut en bande grise unique (MNT).

### Propriétés des couches raster

Comme pour les couches vecteur, les propriétés d'une couche raster s'obtiennent par double-clic sur son nom (ou clic droit -> Propriétés). L'onglet **Symbologie** est divisé en 4 parties :

1. le **rendu des bandes raster**, spécifique au type de données, qui permet de régler la représentation de chaque bande ;
2. le **rendu de couche**, où l'on applique au rendu obtenu des réglages de luminosité, saturation, contraste, etc., et où l'on choisit un rendu « Normal » ou un **mode de fusion** ;
3. le **ré-échantillonnage**, qui améliore le rendu de l'image lors des zooms avant/arrière ;
4. le bouton **Style**, qui permet d'enregistrer, charger, renommer le style.

Pour une **couche à bandes multiples**, on peut choisir quelle bande sera affichée sur le canal rouge, vert et bleu de l'image finale. Pour une **carte scannée**, le rendu par bande « palette/valeurs uniques » permet de modifier chaque classe de couleur (couleur, transparence, étiquette), d'ajouter ou supprimer des classes individuelles. Pour un **modèle numérique de terrain**, le rendu « bande grise unique » propose de choisir le sens du dégradé (du blanc vers le noir ou l'inverse) ainsi que les valeurs min/max de référence (issues de l'emprise totale ou de l'emprise actuelle). Le rendu « pseudo-couleur à bande unique » permet en outre d'appliquer une palette continue à un MNT, en choisissant successivement le mode d'interpolation, le modèle de palette, le mode de classification et le nombre de classes. Les palettes créées peuvent être enregistrées dans la bibliothèque du gestionnaire de style pour être réutilisées.

Un MNT peut également être représenté avec les rendus **contours** (courbes de niveau) ou **ombrage**, pour améliorer sa lisibilité.

Le **ré-échantillonnage** fait effet à chaque zoom avant/arrière, lorsque l'image est recalculée par le moteur graphique. Par défaut, le mode « Plus proche voisin » est utilisé, ce qui peut conduire à une pixellisation de l'image lors d'un fort zoom ; les modes « Bilinéaire » ou « Cubique » (zoom avant) et « Moyenne » (zoom arrière) peuvent améliorer le rendu, en particulier pour les cartes scannées et les fichiers au format ECW.

**Onglet Transparence** : on peut définir un niveau d'**opacité globale** pour la couche (de 0 % à 100 %) et, avec les **options de transparence personnalisée**, fixer le niveau de transparence en fonction des valeurs de pixels. Le bouton **Ajouter les valeurs depuis l'affichage** permet de sélectionner, en cliquant directement sur la carte, la valeur des pixels à rendre transparents (par exemple le fond blanc d'un scan, sans affecter les dégradés de gris du relief).

> [!info] Déterminer la valeur des pixels d'un raster
> Le bouton **Identifier les entités** de la barre d'outils Attributs permet d'obtenir la valeur de chaque pixel en cliquant sur la carte : sur un modèle numérique de terrain, on obtient l'altitude du point cliqué ; pour une photographie aérienne, la valeur du pixel est affichée pour chaque bande de l'image.

## Mode de fusion

### Présentation du mode de fusion

Les **modes de fusion** (ou de mélange) permettent de définir la manière dont une couche va s'intégrer avec celle(s) située(s) en dessous (fusion entre couches) ou dont les objets d'une même couche vont s'intégrer entre eux (fusion entre objets). Ces effets, initialement conçus pour la photographie et le graphisme (Photoshop, GIMP), peuvent surprendre en cartographie s'ils sont utilisés sans discernement, mais peuvent aussi indéniablement améliorer l'affichage des cartes en mettant en valeur certaines données indépendamment de leur position dans l'empilement des couches, et en gommant les effets « délavés » de la transparence.

Dans QGIS, les modes de fusion sont utilisables **entre les couches**, **entre les objets** d'une même couche (à manier avec discernement car cela peut remettre en cause la sémiologie de la couche), et (pour l'impression) **dans le composeur**.

### Fonctionnement des modes de fusion

La fusion entre deux couches se fait par l'application de **formules mathématiques** entre les valeurs des pixels appartenant aux différentes couches, ce qui explique que certains modes portent des noms d'opérations : Multiplier, Addition, Soustraire, Différencier…

Par exemple, pour le mode **« Multiplier »**, les valeurs des pixels (comprises entre 0 et 255) sont multipliées entre elles puis le produit est divisé par 255 pour revenir dans l'intervalle des valeurs possibles. Le résultat est généralement une image plus sombre : deux pixels de valeur 100 donneront un pixel de valeur égale à 39 (100 × 100 / 255) ; si l'un des calques est blanc (255), l'image résultante est semblable à l'autre calque ; si l'un des calques est noir (0), l'image résultante est complètement noire.

Certaines opérations sont commutatives (le résultat est le même quel que soit l'ordre de superposition des couches, par exemple Multiplier, Addition), tandis que d'autres (Soustraire, Diviser) donnent des résultats différents selon l'ordre des couches.

Principaux modes de fusion disponibles dans QGIS et leur pertinence en cartographie :

| Mode | Effet | Pertinence en cartographie |
|---|---|---|
| Normal | Utilise la transparence (canal alpha) du pixel de la couche supérieure ; pas de mélange de couleurs | Mode par défaut, pertinent dans la grande majorité des cas, mais aspect « délavé » avec la transparence |
| Éclaircir (lighten) | Retient la plus grande composante RVB de chaque pixel entre les deux couches | Peu pertinent, les couleurs résultantes ne respectent pas les couleurs originales |
| Filtrer (screen) | Inverse, multiplie, puis inverse à nouveau les valeurs de pixels (inverse de Multiplier) ; image plus lumineuse | Peu pertinent |
| Éviter (dodge) | Éclaire et sature les pixels sous-jacents selon la luminosité de la couche du dessus | Résultat souvent trop saturé |
| Addition | Ajoute les valeurs de pixels (saturation au blanc au-delà de 1) | Pas convaincant |
| Assombrir (darken) | Retient la plus petite composante RVB de chaque pixel (inverse d'Éclaircir) | Intéressant pour combattre l'aspect délavé de la transparence alpha |
| **Multiplier** | Multiplie chaque composante des deux couches ; image plus foncée | **Le mode de fusion qui semble le plus pertinent et le plus intéressant pour la cartographie** |
| Découper (burn) | Divise la couche sous-jacente inversée par la couche supérieure ; assombrit et augmente le contraste | Peu pertinent |
| Revêtement (overlay) | Combine Multiplier et Filtrer : parties claires plus claires, parties sombres plus sombres | Peu pertinent |
| Lumière douce | Semblable au revêtement mais utilise Éviter ; imite un éclairage diffus | Peu pertinent |
| Lumière dure | Semblable au revêtement mais utilise Découper et Éviter ; effet d'ombre | Peu pertinent |
| Différencier | Soustrait le pixel du haut à celui du bas (ou inverse) pour obtenir une valeur toujours positive ; le noir ne change rien, le blanc inverse l'image | Éventuellement utilisable en fusion entre objets |
| Soustraire | Soustrait les valeurs de pixels d'une couche à l'autre ; affichage du noir si valeur négative | Peu pertinent |

### Principes de fonctionnement et mise en œuvre

Les modes de fusion entre couches s'appliquent aussi bien sur les couches raster que sur les couches vecteur. Ils sont particulièrement intéressants pour fusionner des couches raster entre elles, fusionner des couches vecteur de type polygones (ou surfaces) avec une trame unie, ou fusionner ces deux types de couches entre elles ; ils sont en revanche moins utiles pour des couches de lignes ou de points (sauf symboles de grande taille).

Points d'attention avant d'appliquer un mode de fusion :

- la fusion se fait entre les pixels de la couche ainsi paramétrée et **tous** les pixels visibles en dessous, quelle que soit la couche à laquelle ils appartiennent (visibles par transparence, par un autre mode de fusion, etc.) ;
- on peut paramétrer plusieurs couches successives, ce qui peut produire des effets inattendus (fusion entre couches elles-mêmes fusionnées) ;
- si une couche intermédiaire est masquée, la fusion se fera directement avec les couches inférieures, ce qui peut conduire à des affichages non prévus ;
- les couleurs des objets pouvant être modifiées par la fusion (assombrissement, éclaircissement…), la sémiologie initialement prévue de la couche peut être altérée et le message de la carte compromis.

Le choix du mode de fusion entre couches se fait dans l'onglet **Symbologie** des propriétés de la couche (section « Rendu de couche »), ou dans l'onglet **Style** du panneau ancrable, via la liste déroulante **Mode de fusion**. Le mode de fusion peut être utilisé en parallèle de la transparence de la couche ; il fait partie du style de la couche et est donc enregistré dans les fichiers `.qml` et dans les projets `.qgs`.

> [!tip] À retenir
> La symbologie QGIS distingue trois familles de symboles (points, lignes, surfaces), combinables en symboles composés à plusieurs niveaux, et propose plusieurs types de rendu (unique, catégorisé, gradué, règles...) pour les couches vecteur, ainsi que des rendus spécifiques (bandes multiples, palette, bande grise, pseudo-couleurs) pour les couches raster. Le mode de fusion « Multiplier » est généralement le plus pertinent en cartographie pour combiner plusieurs couches sans obtenir un rendu délavé, mais tout mode de fusion doit être utilisé avec discernement pour ne pas altérer le message porté par la carte.

> [!question]- Exercice : style de représentation des couches vecteur
> Ouvrir les couches COMMUNE, CHEF_LIEU, ROUTE_PRIMAIRE et ROUTE_SECONDAIRE. Colorer les routes primaires en bleu avec une épaisseur de 0,5 mm et les routes secondaires en marron ; modifier le symbole des chefs-lieux (carré, bleu clair, transparence 50 %) ; appliquer aux communes un rendu catégorisé sur le champ nom, avec une transparence de 70 %. Ordonner les couches (CHEF_LIEU, COMMUNE au-dessus des ROUTE) pour vérifier la transparence.
>
> **Corrigé** : pour chaque couche, ouvrir les propriétés (onglet Style ou panneau ancrable), modifier la couleur et l'épaisseur du symbole simple pour les routes ; pour les chefs-lieux, choisir le style « carré », changer la couleur et régler le curseur de transparence à 50 % ; pour les communes, choisir le rendu « Catégorisé », la colonne « nom », une palette de couleurs aléatoire, cliquer sur « Classer », puis régler l'opacité globale à 70 %.

> [!question]- Exercice : style de représentation des couches raster
> Ouvrir les couches BD Ortho, MNT (`MNT_25M_asc`) et un SCAN 100. Observer les différents types de rendu proposés par défaut pour chacune. Pour le SCAN 100, visualiser la palette de couleurs utilisée par l'IGN. Pour le MNT, appliquer un rendu « pseudo-couleur à bande unique » avec 4 classes (interpolation linéaire, couleurs bleu = 105, vert = 90, jaune = 70, rouge = 25), enregistrer ce style sous forme de fichier `.qml`, puis fixer sa transparence à 70 % pour visualiser le SCAN 100 en fond.
>
> **Corrigé** : double-cliquer sur chaque couche pour ouvrir l'onglet Symbologie et constater le type de rendu par défaut (bandes multiples pour la BD Ortho, palette/valeurs uniques pour le SCAN, bande grise unique pour le MNT). Pour le MNT, choisir le rendu « pseudo-couleur à bande unique », définir 4 classes avec les couleurs indiquées, valider, puis enregistrer le style via le bouton Style -> Enregistrer sous. Régler ensuite la transparence dans l'onglet Transparence des propriétés du MNT.

> [!question]- Exercice : mise en œuvre du mode de fusion
> En reprenant le projet de l'exercice précédent, appliquer au MNT un mode de fusion « Multiplier », supprimer sa transparence (qui était à 70 %) pour vérifier que la couche sous-jacente reste tout de même visible, puis choisir une valeur de transparence qui donne un bon résultat final.
>
> **Corrigé** : dans l'onglet Symbologie du MNT, section « Rendu de couche », choisir le mode de fusion « Multiplier » et valider ; ouvrir l'onglet Transparence pour remettre l'opacité à 100 % et constater que le SCAN reste partiellement visible grâce au mode de fusion (et non plus grâce à la transparence) ; ajuster ensuite la transparence pour affiner le contraste final.
