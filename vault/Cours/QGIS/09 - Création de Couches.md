---
tags: [qgis, sig]
---
# Création de Couches
Retour : [[00 - Sommaire QGIS]] · Précédent : [[08 - Import et Export de Données]] · Suite : [[10 - Extensions et Plugins]]

Ce chapitre présente la création d'une nouvelle couche vectorielle dans QGIS, la numérisation des objets (points, lignes, polygones) et la modification des géométries et des données attributaires. Il aborde aussi les couches d'annotation, utiles pour habiller une carte sans créer de véritable couche métier.

## Créer une nouvelle couche

Pour créer une nouvelle couche, il faut suivre le chemin `Menu Couche → Créer une couche → [choisir le type]`, ou cliquer sur l'une des icônes de la barre d'outils « gestion des sources de données », ou encore sur l'icône dédiée de la barre d'outils « Gestion des couches ». Plusieurs types de couches sont proposés : `GeoPackage`, `Shapefile`, `Spatialite`, `couche temporaire en mémoire`, `couche de maillage`, `GPX` ou `couche virtuelle`.

### Couche shapefile

Dans la fenêtre de création, il faut :

- définir le type d'objets de la couche (**point**, **ligne**, **polygone**). Il est aussi possible de créer une simple table attributaire en choisissant `Pas de géométrie` ;
- définir le système de coordonnées de référence (`SCR`), par exemple `RGF93 / Lambert 93` ;
- définir la structure de la nouvelle table en créant des **champs**, dont le type peut être :
  - `Nombre entier` (entier),
  - `Nombre décimal` (réel),
  - `Texte` (chaîne de caractères).

Une fois la couche créée, les objets géométriques peuvent être saisis, ainsi que les données attributaires de chaque objet créé.

### Couche GeoPackage

La création d'une couche GeoPackage suit une logique proche, avec quelques différences :

- on peut sélectionner une base de données Geopackage existante ou en créer une nouvelle ;
- le choix des types de géométrie est **plus varié** que pour une shapefile, notamment les géométries **multi-parties** ou de **courbes** ;
- on définit également le SCR et la structure de la table ;
- des **options avancées** permettent par exemple de créer un index spatial.

### Couche temporaire en mémoire

Une couche temporaire en mémoire est une couche de travail rapide qui n'est **pas sauvegardée automatiquement** : elle doit être enregistrée dans un autre format (shapefile, GeoPackage…) si l'on souhaite conserver son contenu, sinon elle est supprimée à la fermeture de QGIS. Sa création demande également de choisir le type de géométrie, le SCR et la structure des champs ; la saisie des objets se fait ensuite exactement comme pour une shapefile.

> [!tip] Rappel
> Il est conseillé d'activer la validation des géométries par défaut selon la méthode `GEOS`, dans `Préférences → Options → onglet Numérisation`.

## Les outils de numérisation

Pour créer des objets dans une nouvelle couche, il faut **basculer en mode édition** (icône crayon) puis utiliser les outils de numérisation. La barre d'outils de numérisation change selon le type géométrique de la couche active : elle propose la numérisation par **point**, par **ligne** ou par **polygone/surface**. Une barre d'outils complémentaire, « Numérisation avancée », offre des fonctions supplémentaires.

> [!warning] Attention
> La numérisation nécessite obligatoirement le passage en mode ÉDITION.

### Numériser un point

Après avoir créé une couche de type point et l'avoir sélectionnée dans le panneau des couches, il faut aller dans `Barre d'outils numérisation → Basculer en mode édition`, puis choisir l'`Outil point`. Il suffit alors de positionner le curseur à l'endroit souhaité sur la carte et de cliquer. Une fenêtre s'ouvre ensuite pour compléter les attributs de l'entité, en respectant le type de donnée (texte, entier, décimal) défini lors de la création de la couche.

Il est possible de paramétrer QGIS pour que la fenêtre de saisie des attributs n'apparaisse pas systématiquement à chaque nouvelle entité : dans `Préférences → Options → onglet Numérisation`, section `Création d'entité`, cocher `Supprimer la fenêtre de saisie des attributs lors de la création de chaque nouvelle entité`. Les attributs prennent alors la valeur `NULL` et peuvent être renseignés a posteriori dans la table d'attributs.

### Numériser une ligne

Le principe est identique : créer une couche de type ligne, la sélectionner, basculer en mode édition puis choisir l'`Outil ligne`. On dessine la nouvelle ligne en cliquant successivement les sommets, puis on termine avec un **clic droit**, ce qui ouvre la saisie des attributs.

QGIS permet aussi de numériser des **polylignes courbes** : pour les stocker réellement en tant que courbes, il faut utiliser un fournisseur de données qui les supporte (`PostGIS`, `GML`, `WFS`, `GeoPackage`) — pour une shapefile, les courbes sont approximées par une succession de segments droits. Pour activer le mode courbe, on utilise le bouton dédié de la barre d'outils de numérisation avancée. Il existe également un mode de saisie « à main levée » appelé **numérisation de flux** (raccourci `R`), dont la tolérance de « streaming » est réglable. Une barre d'outils « Numérisation de formes » permet de son côté de créer directement des formes courbes prédéfinies.

### Numériser un polygone

De la même façon, on crée une couche de type polygone, on la sélectionne, on bascule en mode édition puis on choisit l'`Outil polygone`. On dessine le contour du polygone en cliquant ses sommets et on **termine par un clic droit**, ce qui ouvre la saisie des attributs. Comme pour les lignes, un polygone peut comprendre des segments courbes si le mode courbe est activé.

> [!info] Suivi de tracés (accrochage)
> Pour faciliter la numérisation, on peut activer la barre d'outils `Accrochage` (clic droit dans une barre d'outils pour l'afficher), puis activer l'accrochage (icône en forme d'aimant en fer à cheval) et régler ses options : couches concernées (toutes les couches, couche active, ou configuration avancée), type d'accrochage (sommet, segment) et tolérance en pixels.
>
> Les options d'accrochage sont également accessibles depuis `Projet → Options d'accrochage…`. Le mode **Avancé** permet de définir un réglage détaillé par couche, par exemple pour numériser de nouveaux polygones en suivant exactement le contour d'une couche `COMMUNE` (autotrace) : il suffit de cliquer sur le premier sommet, puis de positionner le pointeur sur un autre point du contour à suivre — le suivi devient alors automatique, y compris en modification d'entités existantes.
>
> Il est aussi possible de rendre l'accrochage **dépendant d'une plage d'échelle**, et de changer le style de numérisation (par exemple l'opacité de la couleur de remplissage, réglée par défaut à 9 %) dans `Préférences → Options → onglet Numérisation`.

## Modifier les objets géométriques

Toute modification nécessite de passer en mode **édition**. Pour modifier un objet géométrique (point, ligne ou surface), il faut basculer la couche en mode édition puis cliquer sur l'outil de **gestion des sommets**.

Il est utile de faire apparaître l'ensemble des sommets des entités de la couche dès le passage en mode édition ; il faut vérifier, dans `Préférences → Options → onglet Numérisation`, que la case `Montrer les symboles uniquement pour les entités sélectionnées` n'est **pas** cochée.

En cliquant sur un sommet, on peut le **déplacer** (cliqué-relâché : un clic pour attraper le sommet, un second clic pour le déposer) ou le **supprimer** (sélectionner l'outil nœud, cliquer sur le point puis appuyer sur `Suppr`).

Les **coordonnées précises** d'un ou plusieurs sommets peuvent être consultées et modifiées via l'`Éditeur de sommet` : sélectionner le ou les sommets (`Maj + clic`), puis clic droit sur la sélection → `Éditeur de sommet`. Les coordonnées des points sélectionnés apparaissent alors en gras dans un tableau, particulièrement utile lorsqu'un objet possède beaucoup de sommets.

L'outil d'édition de nœud permet également d'**ajouter un nouveau sommet** : un marqueur apparaît au milieu de chaque segment, qu'il suffit de faire glisser pour créer un nouveau point sur le contour.

Pour **supprimer un objet** entier, on le sélectionne à l'aide de l'outil de sélection de la barre d'outils Attribut, puis on utilise l'outil « Supprimer les entités sélectionnées » (icône poubelle) de la barre d'outils numérisation.

> [!info] Complément
> Une vidéo de démonstration (`video_numerisation.mp4`) présente ces outils de numérisation. Elle rappelle que l'option « Éviter les intersections » a été renommée « Éviter le chevauchement », et que le bouton poubelle supprime une entité complètement. Des compléments sont proposés dans la formation « Perfectionnement ».

## Modifier les données attributaires

Pour toute modification, il convient de passer en mode édition. Pour faire apparaître la table d'attributs d'une couche : clic droit sur la couche → `Ouvrir la table d'attributs`, ou `Barre d'outils attributs → Ouvrir la table d'attributs`, ou via l'icône dédiée.

Pour **modifier** une valeur attributaire, il suffit d'ouvrir la table d'attributs puis de double-cliquer sur la donnée à modifier et de changer le contenu du champ.

Pour **supprimer** une donnée attributaire (une entité), on ouvre la table d'attributs en mode édition, on sélectionne l'entité concernée, puis on clique sur l'icône « Supprimer les entités sélectionnées ».

## La couche d'annotation

Une couche d'annotation permet d'ajouter des éléments graphiques directement sur la carte, indépendamment des couches métier : marqueurs (points), lignes, polygones et **textes**, avec une barre d'outils dédiée. Pour créer une annotation, il suffit de sélectionner le type d'élément souhaité dans la barre d'outils puis de dessiner directement sur la carte ; les mêmes raccourcis que pour la numérisation classique s'appliquent, y compris les outils de numérisation avancée (courbes, flux/main libre).

Contrairement aux entités d'une couche vectorielle classique, il est facile de **styler chaque élément d'annotation individuellement** ; toutes les propriétés d'apparence peuvent être définies de manière interactive via le dock « stylage de couche ».

Par défaut, tout élément d'annotation nouvellement créé est placé au-dessus de tous les autres contenus de la carte : il est ajouté dans une **couche d'annotation principale**, toujours dessinée tout en haut de la carte et qui n'est pas répertoriée dans le gestionnaire de couches du projet. Pour interagir avec elle (par exemple modifier l'opacité ou le mode de fusion), on utilise l'option `Propriétés du calque d'annotation principal` dans la barre d'outils des annotations.

Il est également possible de créer des **couches d'annotation secondaires** via l'option `Nouveau calque d'annotation` ; celles-ci apparaissent, elles, dans la liste des couches du projet.

> [!warning] Attention
> Les couches d'annotation sont sauvegardées **dans le projet**, et non dans un fichier de données séparé.

> [!info] Complément
> Le plugin `QDraw` (ou sa variante `QDrawDNUM`) propose des fonctionnalités approchantes, par exemple la création de formes circulaires en donnant un rayon (voir le chapitre sur les extensions et plugins).

> [!tip] À retenir
> Créer une couche (shapefile, GeoPackage, temporaire) impose de définir son type de géométrie, son SCR et ses champs ; la numérisation d'un objet nécessite toujours le mode édition, et les outils d'accrochage/suivi de tracés facilitent grandement la saisie précise. Les couches d'annotation permettent d'habiller une carte sans créer de véritable couche métier.
