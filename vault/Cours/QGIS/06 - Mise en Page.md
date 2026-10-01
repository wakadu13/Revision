---
tags: [qgis, sig]
---
# Mise en Page
Retour : [[00 - Sommaire QGIS]] · Précédent : [[05 - Production de Cartes]] · Suite : [[07 - Sélections et Requêtes]]

Ce chapitre décrit le **composeur d'impression** de QGIS, l'atelier de mise en page qui permet de produire des cartes prêtes à imprimer ou à exporter (carte, légende, échelle, étiquette, image, atlas...). Il couvre la création d'une mise en page, l'insertion et le paramétrage des différents objets, ainsi que la génération automatique d'atlas.

## Mise en page

### Créer une mise en page

QGIS propose plusieurs façons d'ouvrir une mise en page :

- Commande **Projet → Nouvelle mise en page** (`Ctrl+P`) : demande un titre pour la nouvelle mise en page ;
- Commande **Projet → Gestionnaire de mise en page** : permet de gérer et d'afficher les mises en page existantes, de dupliquer, renommer, ou créer depuis un modèle ;
- Commande **Projet → Mises en pages** : liste les mises en page déjà créées pour les rouvrir.

La fenêtre du composeur (ou « mise en page ») comporte 5 zones :

1. les menus ;
2. la barre d'outils ;
3. les options générales organisées en onglets (**Mise en page**, **Propriétés de l'objet**, **Éléments**, **Atlas**, **Historique**) ;
4. l'espace de composition de la carte (insertion des éléments) ;
5. une barre d'état indiquant la position du curseur, le numéro de page et le zoom en %.

### Présentation

La **barre d'outils** du composeur regroupe les fonctions suivantes :

| Groupe | Fonctions |
|---|---|
| Gestion | Sauvegarder le projet, gestionnaire de composition, charger/sauvegarder un modèle, ajouter des pages |
| Export | Imprimer, exporter comme image / SVG / PDF, annuler/rétablir |
| Atlas | Naviguer dans l'atlas, aperçu, imprimer l'atlas, paramètres |
| Zoom / rafraîchissement | Outils de zoom, rafraîchir après zoom ou modification de la gestion des couches |
| Manipulation d'objets | Déplacer la mise en page, sélectionner/déplacer un objet, zoom, déplacer le contenu de l'objet, outil édition de nœuds |
| Ajout d'objets | Ajouter une nouvelle carte, une échelle, une légende, une étiquette, une image, une forme, une table d'attributs, du HTML, outil création de nœuds |
| Organisation | Verrouillage/déverrouillage, ordre d'affichage, groupement/dégroupement, outils d'alignement |

**Options générales** : dans la partie droite se trouvent les onglets **Mise en page** (options générales) et **Propriétés de l'objet** (différentes selon l'objet sélectionné : carte, légende, étiquette...), ainsi qu'un onglet **Historique des commandes** (à activer par clic droit dans les barres d'outils) permettant de revenir en arrière sur plusieurs modifications.

L'activation de la grille et de l'alignement se fait dans le menu **Vue**, qui propose également : rafraîchir, zoom (avant/arrière/100%/emprise totale/largeur), afficher la grille, accrochage à la grille, afficher/accrochage aux guides, guides intelligents, gérer/effacer les guides, afficher les règles, les zones d'emprise, les pages, barres d'outils et panneaux.

Pour définir la **taille**, l'**orientation** et les **dimensions** de la page, effectuer un clic-droit sur la page → **Propriétés de la page**.

> [!tip] Manipulations utiles
> - On peut sélectionner et redimensionner plusieurs objets en même temps (Menu `Éditer` : tout sélectionner, inverser la sélection, tout désélectionner).
> - `SHIFT` en redimensionnant depuis un coin conserve le ratio de l'objet.
> - `CTRL` pendant un déplacement permet un déplacement libre même avec l'accrochage à la grille activé.
> - `CTRL` + clic sélectionne un objet situé en dessous d'un autre.
> - `SHIFT` + flèche permet un déplacement rapide au clavier.
> - Les lignes directrices (guides) peuvent être déplacées ou ajoutées en cliquant dans les règles.
> - `ALT` + sélection ne sélectionne que les objets entièrement contenus dans le rectangle de sélection.
> - Tous les objets peuvent subir une **rotation** (champ dédié dans leurs propriétés).
> - `Suppr` ou menu `Éditer → Effacer` supprime les objets sélectionnés.
> - Maintenir `SHIFT` en dessinant une polyligne/un polygone contraint les angles de ligne.
> - `CTRL + Tab` bascule la visibilité des panneaux du composeur.

### Insertion d'éléments (objets) dans l'espace de mise en page

Pour insérer un nouvel objet, après activation du bouton correspondant (« Ajouter une nouvelle carte », « Ajouter une légende », etc.) dans la barre d'outils, il faut pointer avec un clic gauche dans l'espace de composition (zone blanche) et maintenir le clic en traçant une fenêtre aux dimensions souhaitées (tirer - lâcher).

Le cadre créé peut ensuite être redimensionné et/ou déplacé après activation du bouton **Sélectionner/Déplacer un objet**.

**Figer un objet** : la position et la dimension d'un objet (carte, légende, étiquette...) peuvent être « figées » en utilisant l'outil de verrouillage (icône cadenas), ou dans l'onglet `Éléments` via la case à cocher cadenas — pratique pour éviter les mauvaises manipulations. Le cadre de l'objet disparaît alors visuellement.

### Paramétrages d'un objet « Carte »

Depuis la barre d'outils, cliquer sur l'icône **Ajouter une carte**, tracer le cadre, puis ouvrir l'onglet **Propriétés de l'objet**. Les principales sections sont :

| Section | Contenu |
|---|---|
| Propriétés principales | Échelle, rotation de la carte, SCR, dessiner les objets du canevas de carte |
| Couches | Suivre le thème de la carte, verrouiller les couches / le style des couches |
| Emprise | Coordonnées min X / min Y / max X / max Y |
| Plage temporelle | Filtrage temporel des données affichées |
| Contrôlé par Atlas | Lien de l'objet carte à un atlas (voir plus bas) |
| Grilles | Ajout d'un ou plusieurs graticules (grilles de coordonnées) |
| Aperçus | Utiliser un autre objet carte comme carte d'aperçu |
| Position et taille / Rotation / Cadre / Arrière-plan | Mise en forme du cadre |

Le bouton **Déplacer le contenu de l'objet** permet de déplacer l'emprise de la carte à l'intérieur du cadre carte ; dans ce mode, la molette de la souris agit comme un zoom sur le contenu.

**Ajouter un graticule (grille de coordonnées)** : dans la section `Grilles` des propriétés de l'objet carte, on peut ajouter une ou plusieurs grilles, avec de nombreux réglages (type de grille, unité, intervalle, style de ligne, cadre, annotations des coordonnées).

**Aperçus (carte d'aperçu / carton de localisation)** : un objet carte peut servir de carte d'aperçu pour un autre objet carte. Il faut :

1. Dans les propriétés de l'objet « grande carte », section `Aperçus`, ajouter un aperçu et indiquer `Cadre d'aperçu → Carte 0` (la petite carte de localisation).
2. Choisir le style d'affichage de l'emprise (couleur, mode de fusion).
3. Le style de l'aperçu affiche dans le cadre en cours l'emprise de la carte désignée avec le style choisi ; chaque zoom dans l'objet carte 0 modifie la représentation de l'emprise dans l'objet carte 1.

> [!tip] Suivre le thème de la carte
> Il est conseillé, pour la carte d'aperçu, de **suivre un thème** (voir ci-dessous) avec un affichage simplifié, sauvegardé au préalable dans le gestionnaire de couches, de façon à obtenir une vue simplifiée et lisible.

**Les thèmes (ou réglages de visibilité)** : dans le panneau des couches, le menu du bouton « œil » permet d'**ajouter un thème** qui mémorise l'état de visibilité (et le style) des couches. Ce thème est ensuite sélectionnable dans l'objet carte du composeur via l'option **Suivre le thème de la carte**, ce qui permet par exemple d'afficher une version simplifiée des données pour une petite carte de localisation sans dupliquer les couches.

### Paramétrages d'un objet « Barre d'échelle »

Menu : **Ajouter un objet → Ajouter barre d'échelle**. La barre d'échelle informe de la notion de distance, même après une déformation du format de sortie (export en image ou PDF).

Réglages principaux :

| Section | Paramètres |
|---|---|
| Propriétés principales | Carte associée, style (8 styles disponibles, dont « Boîte unique ») |
| Unités | Unité de la barre (ex. Kilomètres), multiplicateur, étiquette d'unité (ex. « km »), format de nombre |
| Segments | Nombre de segments à gauche/droite, largeur fixe ou ajustée au segment, hauteur, subdivisions |
| Affichage | Marge de la boîte, marge de l'étiquette |

### Paramétrages d'un objet « Légende »

Menu : **Ajouter un objet → Ajouter légende**.

Lors de la création d'une légende, les couches déclarées comme « visibles » dans le gestionnaire de couches apparaissent automatiquement, avec le nom défini dans la fenêtre des couches. Dans le composeur, il est cependant possible de changer le nom des couches et des sous-thèmes (notamment lors d'une analyse thématique).

> [!note] Bonnes pratiques
> - Pour gagner du temps (cas de plusieurs mises en page dans un même projet), il est préférable de renommer la couche directement dans le panneau des couches (clic droit `Renommer`) plutôt que dans chaque légende.
> - Lors d'une analyse thématique, les « étiquettes » des classes ne peuvent être changées que dans la légende du composeur.
> - Modifier le nom, l'ordre ou supprimer une couche dans la légende **n'entraîne aucune modification** dans le panneau des couches : ces changements ne concernent que la légende.
> - Si une seconde légende est créée, elle reprend automatiquement l'ensemble des couches visibles : il faut refaire le travail de modification de nom/ordre.
> - Il est souhaitable de **décocher « Mise à jour auto »** afin d'apporter des modifications manuelles à la légende sans qu'elles soient écrasées.

**Propriétés principales** : Titre, Carte associée, retour à la ligne, disposition (par exemple « Symboles à gauche »), ajuster au contenu.

**Éléments de la légende** : liste des couches/classes, avec boutons pour :

- monter/descendre un élément de la légende ;
- ajouter un nouveau groupe ;
- ajouter/supprimer une couche ou une classe ;
- éditer le nom de la couche ou de la classe ;
- compter les entités.

Le bouton `ε` permet le filtrage des classes selon une expression (exemple : `"Nom_Iris" LIKE 'C%'` pour n'afficher que les classes commençant par C). Les options **« ne montrer que les entités à l'intérieur de la carte liée »** et **« ne montrer que les entités à l'intérieur de l'entité atlas courante »** permettent d'adapter dynamiquement le contenu de la légende.

**Légende WMS** : certains serveurs WMS sont capables de délivrer une légende (`GetLegendGraphic`) ; QGIS permet de régler la largeur et la hauteur de la légende réclamée.

> [!tip] Étiquettes de légende définies par des valeurs
> Le bouton `ε` permet de définir des étiquettes de légende sophistiquées à l'aide d'une expression (voir la documentation QGIS).

### Paramétrages d'un objet « Étiquette »

Menu : **Ajouter un objet → Ajouter Étiquette**. Utilisé pour ajouter du texte dans la composition, par exemple un titre.

Options principales :

- **Rendu en HTML** : à activer pour que du code HTML saisi dans le contenu soit correctement interprété ;
- **Insérer/Éditer l'expression** : permet d'utiliser une expression dynamique ;
- **Texte dynamique** : menu pré-rempli proposant date actuelle, propriétés de la carte, nom de la mise en page, numéro de page, nombre de pages, crédits de la couche, auteur/titre/chemin du projet, nom de l'utilisateur actuel, compte de l'utilisateur actuel ;
- **Apparence** : police, marges horizontale/verticale, alignement horizontal (gauche/centré/droite/justifié) et vertical (au-dessus/centré/en dessous).

**Étiquettes HTML (complément)** : l'option `Permettre le formatage HTML` (dans les paramètres de police de l'étiquette) autorise l'insertion de code HTML, avec par exemple des balises `<style>` et `<img>` pour intégrer une image locale ou distante, ou des tableaux `<TABLE>` avec `<TR>`/`<TH>`/`<TD>` pour composer un tableau mis en forme.

Exemple d'image redimensionnée en HTML :
```html
<style>
* {margin: 0px; padding: 0px}
</style>
<img src="file:///I:/qgis.gif" style="width: auto; height: 100%; display: block; margin: 0px 0px 0px auto;"/>
```

Ceci est particulièrement utile lorsque la source de l'image est une URL distante.

**Ajout de variables (complément)** : QGIS permet d'ajouter des variables personnalisées dans un projet (**Projet → Propriétés → Variables**), dans une mise en page (onglet `Mise en page` du composeur, sous-menu `Variables`, bouton `+`), ou pour un élément de mise en page précis (onglet propriétés de l'objet). Les variables sont appelables partout en les préfixant par `@` (les noms de variables sont sensibles à la casse). Exemple dans une étiquette :

```
Créé par [%@auteur%]
Version [%@Version_projet%]
Chemin du projet [%@project_folder%]
```

Les variables de mise en page `layout_name`, `layout_page` (numéro de page) et `date` se mettent à jour automatiquement en fonction de la page où se trouve l'étiquette, ce qui permet de créer un pied de page copié-collé sur toutes les pages, par exemple :
```
[%@layout_name%] ([%@date%]) : page [%@layout_page%]
```

> [!info] Simulation des déficiences de perception des couleurs
> Le menu **Vue → Mode d'affichage** permet de simuler différentes formes de déficience de perception des couleurs, pour vérifier la lisibilité de la carte par tous.

> [!question]- Exercice : Mise en page
> **Objectif** : réaliser une mise en page simple d'une carte.
>
> Ouvrir les couches `COMMUNE.SHP`, `CHEF_LIEU.SHP` et la couche raster `SC100_0440_6750_L93.tif`. Réaliser une composition avec titre, légende, barre d'échelle et carte, puis sauvegarder le projet.
>
> > [!example]- Corrigé
> > - Ordonner les couches (du haut vers le bas) : CHEF_LIEU, COMMUNE, scan raster.
> > - Modifier le remplissage des communes en rendu **Catégorisé** sur `NOM`, opacité 70 %.
> > - Modifier le symbole des chefs-lieux avec un symbole SVG de la bibliothèque (par exemple taille 10 mm).
> > - Créer une nouvelle mise en page, format A4 paysage.
> > - Ajouter une carte (largeur 230, hauteur 160, échelle 1:130 000, case « dessiner les objets du canevas de carte » cochée), recentrer avec « déplacer le contenu ».
> > - Ajouter une étiquette de titre, une légende (désactiver la mise à jour auto et retirer l'entrée du scan raster), une barre d'échelle graphique (unité mètre, taille de segment 1000, 5 segments).
> > - Composer la mise en page en déplaçant les objets, et définir pour chacun l'affichage ou non du cadre, la couleur du cadre et du fond.

## Mise en page, compléments pour fonctionnalités avancées

### Paramétrages d'un objet « Image »

Menu : **Ajouter un objet → Ajouter image**, puis onglet `Propriétés de l'objet`. Fonction utile pour insérer une photographie, un logo, une flèche nord, etc.

Deux modes : **Image raster** (chargée depuis un fichier — attention à la perte du lien si l'image est déplacée) ou **Image SVG** (choisie dans la bibliothèque QGIS par défaut, personnalisable, ou une bibliothèque personnelle).

Pour certains symboles SVG, il est possible de modifier des paramètres (couleur de remplissage, couleur de bordure, largeur de bordure). Il est également possible de synchroniser la **rotation de l'image** avec la rotation de la carte désignée — utile typiquement pour une flèche nord alignée avec le Nord de la grille ou le vrai Nord géographique.

### Paramétrages d'un objet « Table d'attributs »

Menu : **Ajouter un objet → Ajouter Table attributaire**, puis onglet `Propriétés de l'objet`. Cet objet insère un extrait ou la totalité de la table attributaire d'une couche.

| Section | Paramètres |
|---|---|
| Propriétés principales | Source (entités de la couche), couche, actualiser la table de données, choix des attributs |
| Filtrage des entités | Lignes maximales, suppression des doublons, n'afficher que les entités visibles sur la carte (avec choix de la carte liée si plusieurs cartes), n'afficher que les entités intersectant l'atlas, filtrer avec une expression |
| Apparence | Afficher des lignes vides, marges de cellule, affichage de l'en-tête, tables vides, couleur de fond, personnalisation avancée |

Il est possible d'ajouter de nouvelles colonnes calculées (bouton `+`) avec le calculateur de champs, de modifier le nom affiché des colonnes et de définir un ordre de tri (plusieurs critères possibles, avec priorité).

### Paramétrages d'un objet « Cadre HTML »

Menu : **Ajouter un objet → Ajouter HTML**, puis onglet `Propriétés de l'objet`. Permet d'insérer un cadre HTML dans une composition, dont la source peut être une URL, un fichier local (extension `.htm`/`.html`) ou du code HTML directement saisi. Le bouton d'insertion d'expression peut être utilisé pour insérer une expression dynamique, par exemple `[%Year($now)%]` pour afficher l'année courante.

> [!question]- Exercice : Mise en page avancée
> **Objectif** : réaliser une mise en page avancée avec différents éléments (objets).
>
> Ouvrir `IRIS_extrait72.shp`. Réaliser une composition avec légende (contenu et police du titre, de la couche et de l'objet personnalisés), une flèche nord, des photos (`PHOTOS\*.jpg`), un logo, des mentions de copyright/réalisation, et une rotation de la carte à 30° avec une échelle 1:70 000. Sauvegarder le projet.
>
> > [!example]- Corrigé
> > Utiliser un objet **Image** pour la flèche nord (SVG, coloré) et pour chaque photo (image raster). Insérer le logo via un objet Image. Ajouter les mentions de copyright dans un objet Étiquette. Régler la rotation de la carte à 30° et l'échelle à 70 000 dans les propriétés principales de l'objet carte.

### Impression et export

Une fois l'impression configurée (position et échelle de la carte, légende, etc.), il est possible de **sauvegarder le modèle de mise en page** (boutons ouvrir/enregistrer un modèle) pour des impressions ultérieures du même type (par exemple pour réutiliser une charte graphique).

Il est possible d'imprimer directement le document, ou de l'exporter en fichier image (`.jpg`, `.png`, `.tif`...), `.pdf` ou `.svg`.

> [!warning] Enregistrement obligatoire
> L'enregistrement dans un fichier projet est indispensable pour sauvegarder la carte composée : une mise en page n'existe qu'attachée à son projet `.qgs`/`.qgz`.

> [!tip] Chemin additionnel de recherche pour les modèles
> Il est possible d'ajouter des chemins de recherche pour les modèles dans **Préférences → Options → Mise en page**, ce qui permet de partager des modèles communs au sein d'un service.

### Génération d'atlas de cartes

Il est possible de générer automatiquement un **atlas de cartes** (par exemple un atlas de cartes communales). Le principe : utiliser la géométrie et les attributs d'une couche vectorielle (par exemple une couche de COMMUNES) comme **couche de couverture**. Pour chaque entité de cette couche, une nouvelle carte est générée dont l'emprise correspond à la géométrie de l'entité ; les attributs de la couche peuvent être utilisés dans des zones de texte (par exemple pour adapter le titre de la carte).

Pour activer l'atlas : onglet `Atlas` du composeur (menu `Atlas → Paramètres de l'atlas` si l'onglet n'apparaît pas), puis cocher **Générer un atlas**.

**Configuration de l'atlas** :

| Paramètre | Rôle |
|---|---|
| Couche de couverture | Couche vectorielle définissant les pages (une entité = une page), avec option de masquer cette couche dans les sorties |
| Nom de la page | Champ ou expression déterminant le nom donné à chaque page |
| Filtrer avec | Filtre les entités de la couverture |
| Ordonner par | Champ de tri des pages (ordre croissant/décroissant) |

**Sortie** : export dans un seul fichier ou dans des fichiers distincts (le numéro de l'entité `@atlas_featurenumber` remplace alors un motif dans le nom de fichier, ex. `commune_1.pdf` pour la première commune). Formats d'export possibles : image (bmp, png, jpg, jpeg...), PDF ou SVG.

Pour lier une carte à l'atlas : dans les propriétés de l'objet **Carte**, cocher **Contrôlé par Atlas** (une marge autour de l'entité — « rayon » — peut être définie en %, par exemple 10 %). Une étiquette peut alors utiliser le champ de la couche de couverture comme variable pour afficher un titre dynamique.

La **barre de l'atlas** (aperçu, entité précédente/suivante/première/dernière, impression, paramètres) permet de générer un aperçu et de naviguer de page en page. Le menu Atlas permet d'imprimer en PDF ou d'exporter en tant qu'images ou SVG.

**Mise en surbrillance de l'entité traitée dans chaque page (complément)** : quand l'atlas est activé, QGIS crée deux variables `@atlas_featureid` et `@atlas_geometry`, qui représentent respectivement l'identifiant et la géométrie de l'objet traité dans chaque page. On peut s'en servir pour affecter un style spécifique à l'entité en cours, par exemple :

- style **Ensemble de règles** sur la couche de couverture avec une règle `@atlas_featureid = $id` (affichée par exemple en jaune) et une règle `ELSE` (affichée en gris) pour les autres entités ;
- étiquetage conditionnel avec l'expression `CASE WHEN $id = @atlas_featureid THEN "Nom_iris" END` pour n'afficher le nom que de l'entité en cours (ou l'inverse avec `IS NOT` pour n'étiqueter que les entités *inactives*) ;
- pour une couche liée (par exemple les bâtiments contenus dans l'IRIS traité), un style basé sur `within($geometry, @atlas_geometry)` avec règle `ELSE` permet de distinguer visuellement les objets à l'intérieur de l'entité en cours.

Il existe également une variable `@map_id`, indépendante de l'atlas, qui permet de personnaliser le style d'une couche en fonction de l'identifiant d'un objet carte précis (renseigné dans `Identifiant de l'objet` des propriétés de la carte), par exemple pour ne restreindre un effet de surbrillance qu'à la carte principale et non aux cartons de localisation.

> [!question]- Exercice : Atlas
> **Objectif** : réaliser un atlas avec différents paramètres de visualisation.
>
> Ouvrir `IRIS_extrait72.shp` et `BATIMENT.shp` (afficher BATIMENT au-dessus des IRIS). Réaliser un atlas des IRIS en insérant une carte unique visualisant les deux couches, un titre avec la variable du nom de l'IRIS en cours, et une flèche nord. Afficher les étiquettes des noms des IRIS *inactifs*, une surbrillance pour la couche BATIMENT, une ombre pour mettre en surbrillance l'entité en cours, avec une marge de 20 % autour de l'entité en cours. Exporter l'atlas au format PDF.
>
> > [!example]- Corrigé
> > - Couche de couverture : `IRIS_extrait72`, nom de page = `Nom_Iris`, ordonner par `Nom_Iris`.
> > - Objet carte « Contrôlé par un atlas », marge 20 %.
> > - Étiquette de titre avec la variable `[%@atlas_pagename%]`.
> > - Sur la couche IRIS : style **Ensemble de règles** avec la règle `within($geometry, @atlas_geometry)` (remplissage + effet d'ombre portée) et une règle `ELSE` de même couleur de remplissage ; activer les **Niveaux de symbole** pour que l'ombre s'affiche correctement.
> > - Étiquetage simple avec l'expression `CASE WHEN $id IS NOT @atlas_featureid THEN "Nom_iris" END`, taille 15, couleur noire, tampon blanc de 1 mm, position au centroïde.
> > - Sur la couche BATIMENT : style Ensemble de règles avec `within($geometry, @atlas_geometry)` (couleur de surbrillance) et `ELSE` (couleur plus terne).
> > - Rafraîchir l'aperçu de la carte, puis exporter l'atlas en PDF (éventuellement au format **PDF Géospatial / GeoPDF** pour un PDF interactif).

> [!tip] À retenir
> Le composeur d'impression assemble des objets indépendants (carte, légende, échelle, étiquette, image, table, HTML) sur une page dont il faut sauvegarder le projet pour conserver la mise en page. Les variables (`@nom_variable`, `@atlas_featureid`, `@atlas_geometry`, `@map_id`) et l'étiquetage conditionnel (`CASE WHEN`) permettent de rendre les objets dynamiques, ce qui devient particulièrement puissant avec la génération automatique d'**atlas** pour produire en une seule fois une série de cartes (une par entité d'une couche de couverture).
