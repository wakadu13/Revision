---
tags: [qgis, sig]
---
# Extensions et Plugins
Retour : [[00 - Sommaire QGIS]] · Précédent : [[09 - Création de Couches]] · Suite : [[11 - Après la Formation]]

QGIS peut être enrichi par des extensions (*plug-ins*) qui ajoutent des fonctionnalités au logiciel. Ce chapitre explique la différence entre extensions principales et complémentaires, la manière de les installer et de les activer via le gestionnaire d'extensions, puis présente les extensions et plugins les plus utiles au quotidien.

## Extensions principales et complémentaires

Les extensions QGIS appartiennent à **deux catégories** : les extensions **principales** (*core plugins*) et les extensions **complémentaires**.

Les **extensions principales** sont maintenues par l'équipe de développement de QGIS et sont intégrées automatiquement à chaque nouvelle distribution du logiciel. Elles se trouvent par défaut dans le répertoire d'installation de QGIS :

- `<Répertoire installation QGIS>\apps\qgis\plugins\` (Windows) pour les plugins écrits en C++ (`.dll`) ;
- `<Répertoire installation QGIS>\apps\qgis\python\plugins` (Windows) pour les plugins écrits en Python ;
- `./share/qgis/python/plugins` (Linux et UNIX) ;
- `./Contents/MacOS/share/qgis/python/plugin` (Mac OS X).

Les **extensions complémentaires** sont actuellement toutes écrites en Python. Elles sont stockées dans des dépôts externes, maintenues par leurs propres auteurs, et peuvent être ajoutées à QGIS via le **Gestionnaire d'extensions**. Elles s'installent dans un sous-dossier du profil QGIS en cours, par défaut :

`C:\Users\<utilisateur>\AppData\Roaming\QGIS\QGIS3\profiles\<profil>\python\plugins`

Astuce : taper `%appdata%/QGIS/QGIS3` dans la barre de recherche de l'explorateur Windows permet de s'y rendre rapidement, ou passer par le menu `Préférences → Profils Utilisateurs → Ouvrir le dossier du profil actif`.

### Quelques extensions principales

| Extension | Description |
|---|---|
| Gestionnaire BD | Gestion de bases de données depuis QGIS |
| Vérificateur de géométrie | Vérification et réparation d'erreurs de géométrie dans les couches vecteur |
| GRASS 7 / GRASS GIS provider | Intégration des fonctionnalités et de l'outil de traitement GRASS |
| MetaSearch | Interaction avec les services de catalogue de métadonnées (CSW) |
| Édition hors-ligne | Édition hors-ligne et synchronisation de la base de données |
| OrfeoToolbox provider | Fournisseur d'algorithmes OrfeoToolbox (OTB) |
| Traitement | Outils de traitement de données spatiales |
| SAGA GIS provider | Intégration des outils de traitement SAGA |
| Vérificateur de topologie | Recherche des erreurs de topologie dans les couches vecteur |

## Installer et activer les extensions

Pour **activer les extensions présentes**, on ouvre le **gestionnaire d'extensions** depuis le menu `Extension`, puis on coche les extensions à activer. Chaque extension y est décrite sommairement ; certaines disposent d'un lien vers une page d'accueil, un gestionnaire de bugs et un dépôt de sources permettant d'y contribuer.

> [!warning] Attention
> Les plugins écrits en Python sont susceptibles de comporter du code malveillant. Il faut donc éviter d'utiliser des dépôts de plugins très exotiques. Les plugins du répertoire officiel de QGIS sont vérifiés avant d'être publiés.

### L'extension Processing

Activer l'extension **Processing** ajoute un menu `Traitement` à QGIS et enrichit les menus `Vecteur` et `Raster` de nombreux algorithmes de géotraitement (outils de recherche, outils de géométrie, analyse, projections, extraction, conversion…). Cette extension donne accès à la **Boîte à outils** du menu Traitement, qui rassemble un très grand nombre d'algorithmes classés par thématique (analyse vectorielle, analyse raster, GPS, interpolation, GDAL, GRASS, SAGA…).

Elle permet aussi d'accéder au **Modeleur graphique**, un outil très puissant permettant d'automatiser des chaînes de traitements (*workflow*). Les outils de Processing sont approfondis dans la formation « Perfectionnement ».

### Vérificateur de géométrie et vérificateur de topologie

Ces deux vérificateurs permettent d'analyser, et pour le vérificateur de géométrie de corriger, des défauts de qualité de couches. Le **vérificateur de géométrie** est un outil puissant pour la recherche des anomalies de géométrie (géométries invalides, auto-intersections…) dans une couche. Le **vérificateur de topologie** apporte des contrôles supplémentaires sur les relations entre entités (superposition, adjacence, etc.).

## Quelques extensions complémentaires (plugins) utiles

| Nom | Description | Exemple / commentaire |
|---|---|---|
| AutoSaver | Sauvegarde automatique à intervalle régulier | |
| Qconsolidate3 | Consolide toutes les couches du projet dans un dossier défini par l'utilisateur ; utile pour partager un projet avec toutes ses couches à une autre personne | Convertit les vecteurs en SHP ou GeoPackage |
| Group Stats | Statistiques et analyse pour les couches de vecteurs | Plugin un peu difficile d'abord mais puissant |
| Cadastre | Facilite l'utilisation des données cadastrales françaises dans QGIS ; plusieurs modules aident à importer les données, les afficher, faire des recherches et imprimer les relevés | Import des données MAJIC, … |
| Value tools | Affiche la valeur d'un pixel à la position du curseur pour les couches raster | |
| QuickMapServices | Ajoute des couches avec des serveurs externes (Bing, Google, OSM…) | Alternative au plugin OpenLayers |
| Localiser Parcelle Adresse | Géocodage à l'adresse et/ou à la parcelle ; la version BAN utilise la Base Adresse Nationale | Plugin interne au Ministère |
| Créer ses propres menus | Ajoute des menus avec des raccourcis vers des couches ou des fichiers | Plugin interne au Ministère, utile pour simplifier l'accès aux données aux utilisateurs |
| Layers Menu from project | Crée des menus à partir de projets QGIS | Complémentaire du précédent |
| Menu GeoIDE | Création automatique de menu pour accéder aux géobases | Plugin interne au Ministère |
| Spreadsheet Layer | Aide au chargement des fichiers de feuilles de calcul (`.ods`, `.xls`, `.xlst`) | Génère un fichier VRT |
| QGIS Resource Sharing | Permet de télécharger des ressources (symboles, styles, scripts…) créées par d'autres | Donne accès par exemple aux symboles SVG d'OSM |
| ImportPhotos | Création de points pour des photos « géo-taguées » | |
| Plugin Load Times | Donne les temps de chargement des plugins | Utile pour optimiser les temps d'ouverture de QGIS |
| Profile Tools | Dessin de profils à partir de couches raster ou vectorielles ponctuelles avec un champ d'élévation | |
| Changedatasource | Permet de changer la source d'une couche chargée | Ex. : une couche shapefile passée en base de données, en conservant les fichiers projet utilisant cette couche |
| Auto Filtre 3 | Permet de transformer une sélection en filtre de couche | Réduit le temps de chargement |
| Édition Multi-Utilisateurs | Permet de gérer les conflits d'accès sur des ressources partagées sur un réseau | Typiquement plusieurs personnes travaillant sur le même fichier SHP déposé sur une ressource réseau |
| Le Nettoyeur (de polygones) | Correction des géométries invalides | Complément aux outils natifs de QGIS |
| Search And Replace In Projects | Recherche une chaîne de caractères dans tous les projets d'une arborescence et la remplace par une autre | Ajoute un algorithme dans les traitements |
| Memory Layer Saver | Sauvegarde des couches mémoire | |
| QdrawDNUM | Dessins de formes simples et d'étiquettes à l'endroit cliqué | Dérivé de QDraw, avec ajout de la saisie de textes et d'étiquettes |

> [!info] Remarque
> Certains plugins sont progressivement transformés en algorithmes du module de traitement, ce qui permet de les utiliser dans des flux avec le Modeleur graphique. C'est par exemple le cas de `Dissolve with stat` (remplacé par l'algorithme `Agrégation`), de l'analyse raster de terrain, de la statistique de zone, de `MergeLines`/`join lines` (remplacés par `Fusionner les lignes`), de `create indexed vector grid` (remplacé par `Créer une grille`) ou de l'extension graphe routier (remplacée par les algorithmes d'analyse de réseau). Le plugin `autofields` est quant à lui remplacé par les valeurs par défaut (pouvant être des expressions) dans la conception des formulaires personnalisés.

> [!info] Complément
> On peut obtenir une liste des plugins QGIS marqués « vedette » par la communauté sur le dépôt officiel des plugins, trié par nombre de téléchargements.

## Mettre en pratique

> [!question]- Exercice 20 : gestion et usage des extensions
> **Objectif** : gérer le gestionnaire d'extensions et mettre en œuvre des extensions.
>
> **Énoncé** : ouvrir les couches vectorielles `BD_TOPO\H_ADMINISTRATIF\COMMUNE.SHP` et `BD_TOPO\I_ZONE_ACTIVITE\SURFACE_ACTIVITE.SHP`. Mettre des étiquettes sur la couche `SURFACE_ACTIVITE` en utilisant le champ `CATEGORIE`. Dans le gestionnaire de plugin, installer et/ou activer le plugin `Mask`, sélectionner la commune de **La Flèche** et l'utiliser pour créer un masque avec cette commune. Installer et/ou activer le plugin `QuickMapServices` : dans le nouveau menu `Internet`, aller dans `QuickMapServices → Settings → onglet More services`, cliquer sur `Get contributed pack` puis `Enregistrer`. Charger ensuite la couche OSM / WikimediaMap. Enfin, installer et/ou activer le plugin `Qconsolidate3` et l'utiliser pour sauver le projet et ses données dans un répertoire de son choix, au format **Geopackage** ; rouvrir le projet et vérifier que tout est correct.
>
> **Corrigé (résumé)** : dans `Propriétés de la couche → Étiquettes`, choisir `Étiquettes simples` avec la valeur `CATEGORIE`. Charger le plugin `Mask`, sélectionner la commune de La Flèche dans la couche `COMMUNE`, puis utiliser l'outil `Créer un masque` en limitant l'étiquetage au polygone de la couche `SURFACE_ACTIVITE`. Charger et paramétrer `QuickMapServices` comme demandé, puis ajouter la couche `OSM / WikimediaMap` (menu `Internet → QuickMapServices → OSM → Wikimedia Map`). Charger `Qconsolidate3`, indiquer un nom de projet et un dossier de sortie au format `GeoPackage`, valider ; vérifier ensuite dans le dossier choisi la présence du sous-dossier `layers` et du fichier `.qgs`, puis recharger ce fichier projet pour contrôler le résultat.

> [!question]- Exercice 20 bis (optionnel) : utilisation du plugin Group Stats
> **Objectif** : mettre en œuvre l'extension Group Stats.
>
> **Énoncé** : obtenir des statistiques de population par cantons à partir de la couche des communes de la BD Carto (`BD_CARTO\ADMINISTRATIF\COMMUNE.SHP`). Indice : installer et activer le plugin `Group Stats`, qui permet de réaliser des opérations de regroupement sur les champs selon des critères définis ; une fois installée, l'extension est disponible depuis le menu `Vecteur` ou par une icône de lancement.
>
> **Corrigé** : ouvrir Group Stats, choisir la couche `COMMUNE` dans `Layers`. Glisser le champ `INSEE_CANT` dans la zone `Rows` (lignes de regroupement) et le champ `POPULATION` dans la zone `Values`, puis sélectionner les opérateurs `maximum`, `minimum` et `somme` dans `Columns`. Cliquer sur `Calculate` : le tableau de résultat donne, pour chaque canton, la population maximale et minimale des communes qui le composent ainsi que la population totale du canton.

> [!tip] À retenir
> Les extensions principales sont livrées avec QGIS et maintenues par son équipe de développement ; les extensions complémentaires, écrites en Python, s'installent et s'activent via le gestionnaire d'extensions (`Extension → Gestionnaire d'extensions`) mais doivent venir de dépôts de confiance. Processing, le vérificateur de géométrie et les nombreux plugins communautaires (Mask, QuickMapServices, Qconsolidate3, Group Stats…) permettent d'étendre considérablement les capacités de QGIS sans écrire une ligne de code.
