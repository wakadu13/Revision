---
tags: [qgis, sig]
---
# Ouverture et Visualisation
Retour : [[00 - Sommaire QGIS]] · Précédent : [[01 - Introduction à QGIS]] · Suite : [[03 - Navigation et Sélections Graphiques]]

Ce chapitre examine les différentes ressources (fichiers et services web) que l'on peut ouvrir avec QGIS, aborde la notion de projet, puis détaille le fonctionnement du gestionnaire de couches et des propriétés de couche. Il s'agit du cœur du travail quotidien avec QGIS : charger des données, les organiser et les visualiser correctement.

## Les ressources ouvrables

### Formats supportés

QGIS utilise la bibliothèque **OGR** pour lire et écrire des données vectorielles, et la bibliothèque **GDAL** pour lire et écrire des rasters, dans de multiples formats :

- la plupart des formats vecteurs, dont les shapefiles d'ESRI (`.shp`), les tables MapInfo (`.tab`) et les fichiers KML ;
- les tables de bases de données à cartouche spatiale telles que PostgreSQL/PostGIS ou SQLite/SpatiaLite, ou le GeoPackage (`.gpkg`), qui permet de stocker aussi bien du vecteur que du raster ;
- les formats raster tels que les modèles numériques de terrain, les photographies aériennes ou les images satellitaires, les fonds cartographiques scannés de l'IGN ;
- les données en ligne (intranet, Internet) accessibles sur des serveurs géographiques via les protocoles **WMS** (*Web Map Service*, le serveur renvoyant une image des données) ou **WFS** (*Web Feature Service*, le serveur renvoyant les données elles-mêmes).

Au cours de la formation, on utilise principalement les commandes « ajouter une couche vecteur », « ajouter une couche raster » et « ajouter une couche WMS ou WFS », accessibles depuis le **gestionnaire des sources de données**.

### Ajouter une couche vecteur

Pour ajouter une couche vecteur :

1. ouvrir le **gestionnaire de ressources** (icône représentant des couches avec un `+`) ;
2. cliquer sur le bouton « Vecteur ».

On peut aussi passer par le menu `Couche > Ajouter une couche > Ajouter une couche vecteur`, ou afficher la barre d'outils « Gestion des couches ».

Dans la boîte de dialogue, il est possible de sélectionner un format précis en cliquant sur le bouton « Tous les fichiers (*.*) », ou de désigner directement un fichier (QGIS reconnaît alors automatiquement le format). Les principaux formats vecteurs utilisés sont :

- ESRI Shapefile `.shp` ;
- MapInfo `.tab` ;
- GML (*Geography Markup Language*) ;
- KML (*Keyhole Markup Language*) ;
- AutoCAD DXF ;
- Excel `.xls` / MS Office `.xlsx` / Open Document `.ods`.

> [!info] Choix du codage (encodage)
> Le codage généralement utilisé est l'**UTF-8**. Il convient toutefois de modifier ce codage si les caractères accentués ne s'affichent pas correctement. Certaines anciennes versions des référentiels de l'IGN ont par exemple été diffusées au format SHP avec un encodage `ISO-8859-1`. Il est possible de modifier le codage d'une couche déjà chargée depuis l'onglet Source de ses propriétés.

### Ajouter une couche raster

La procédure est similaire à celle des couches vecteur :

1. ouvrir le gestionnaire de ressources ;
2. cliquer sur le bouton « Raster ».

On peut aussi passer par le menu `Couche > Ajouter une couche > Ajouter une couche raster`. On peut présélectionner un type de fichier (TIFF, Virtual raster, ASCII Grid, ECW, JPEG2000…).

### L'explorateur de ressources

L'explorateur de ressources (panneau « Explorateur ») est accessible depuis le gestionnaire des sources de données, ou en permanence via `Vue > Panneaux > Explorateur` (ou clic droit dans une barre d'outils). Il est conseillé de le laisser affiché en continu.

L'explorateur permet de :

- charger directement des ressources par **double-clic** ou par **glisser-déposer** dans le canevas ;
- **masquer** certaines ressources par un clic droit « Masquer dans le navigateur » (les chemins masqués se retrouvent dans `Préférences > Options > onglet Sources de données > Chemins masqués`) ;
- ajouter une couche par clic droit puis « Ajouter la couche » ou « Ajouter les couches sélectionnées » (plusieurs couches en une seule fois) ;
- afficher un **détail sur les propriétés** de la couche sélectionnée (bouton *i*, ou clic droit « Propriétés de la couche ») : nombre d'entités, encodage, SCR, descriptif des champs, etc. ;
- depuis QGIS 3.22, **définir une couleur** par clic droit sur un répertoire, pour une classification visuelle.

Les principaux boutons de l'explorateur sont :

| Bouton | Fonction |
|---|---|
| Ajouter les couches sélectionnées | Charge en une fois toutes les couches sélectionnées |
| Actualiser | Actualise l'affichage |
| Filtre de navigateur | N'affiche que les noms de ressources correspondant à un motif (avec gestion de la sensibilité à la casse) |
| Réduire tout | Replie l'arbre des couches |
| Activer/désactiver l'outil des propriétés | Affiche ou non les propriétés de la ressource sélectionnée |

> [!question]- Exercice : les différents formats des ressources ouvrables
> **Objectif** : paramétrer l'explorateur de ressources et ouvrir différentes couches vectorielles et rasters.
>
> Paramétrer l'explorateur de couches pour mettre en évidence le répertoire de la formation, puis ouvrir les couches vectorielles suivantes :
> - `BD_CARTO\ADMINISTRATIF\COMMUNE.SHP` ;
> - `BD_TOPO\A_RESEAU_ROUTIER\ROUTE.SHP`.
>
> Ouvrir ensuite les couches raster suivantes :
> - table raster TIFF `SCAN\SCAN_25\Extrait_72_Topo.tif` ;
> - table raster ECW (*ERDAS Compressed Wavelets*) `BD_ORTHO\0468_6740.ecw`.
>
> **Corrigé**
> Pour paramétrer l'explorateur, masquer par clic droit tous les répertoires inutiles, se positionner sur le répertoire souhaité et commencer à taper son nom dans le filtre.
>
> Sans passer par l'explorateur, on peut aussi utiliser la commande `Couche > Ajouter une couche vecteur` (ou `Ajouter une couche raster`) : laisser l'encodage à « Automatique », naviguer jusqu'au répertoire indiqué avec le bouton de navigation « … », sélectionner la table demandée, puis cliquer sur Ouvrir. Pour les rasters, penser à choisir le bon type de fichier (GeoTIFF, ECW…) et à définir au besoin le système de coordonnées de référence (RGF93/Lambert-93).

### Ajouter une couche WMS

Le protocole **WMS** (*Web Map Service*) consiste à interroger un serveur cartographique distant via son adresse (intranet ou Internet, URL). Le serveur renvoie une **image** (JPEG, PNG, GIF, TIF…) des couches géographiques demandées, correspondant à l'étendue de la fenêtre carte de QGIS et calée géographiquement, donc superposable aux données vecteur et raster.

Pour ajouter une couche WMS :

1. ouvrir le gestionnaire de ressources et cliquer sur le bouton « WMS/WMTS » (ou passer par `Couche > Ajouter une couche > Ajouter une couche WMS`, ou par l'explorateur, section « WMS/WMTS ») ;
2. créer une nouvelle connexion en cliquant sur « Nouveau » (si elle n'existe pas déjà), en renseignant l'URL du serveur et un nom de connexion (exemple pour le serveur du BRGM sur les risques : `http://geoservices.brgm.fr/risques`) ;
3. cliquer sur **Connexion** ;
4. choisir la ou les couches à afficher (maintenir `CTRL` enfoncé pour en sélectionner plusieurs) ;
5. choisir l'encodage de l'image (PNG par défaut) ;
6. modifier au besoin le système de coordonnées (RGF93 / Lambert-93 EPSG:2154).

> [!info] JPEG ou PNG ?
> Le format **JPEG** est un format de compression avec perte : il convient bien si la donnée WMS est une orthophotographie et qu'une légère perte de qualité d'image n'est pas gênante (ce compromis permet de réduire par 5 le volume transféré comparé au PNG). Le format **PNG** reproduit pleinement les données raster brutes : à privilégier si l'on souhaite une représentation précise des données originales. Le PNG24 est une extension du PNG en 16 millions de couleurs et 24 bits, chaque composante RVB gérant un canal alpha pour la transparence.

> [!warning] Échelles de visibilité
> Les couches WMS sont parfois visibles uniquement entre deux échelles fixes. Tous les serveurs WMS n'indiquent pas ces échelles de visibilité dans leur résumé : si une couche n'apparaît pas, c'est peut-être que l'on se trouve hors des limites de visibilité définies par le serveur.

> [!info] Reprojection automatique
> Si un raster ou un WMS est fourni dans une projection autre que celle du projet en cours, QGIS reprojette automatiquement le raster dans la projection du projet. Ceci peut conduire à un effet « baveux » sur les détails, en particulier sur les étiquettes comme les noms de rues. Dans ce cas, il peut être opportun d'adopter, avant impression, la projection native du raster (menu `Projet > Propriétés > SCR`).

### Ajouter une couche WFS

Le protocole **WFS** (*Web Feature Service*) consiste également à interroger un serveur cartographique distant via son URL, mais le serveur renvoie cette fois les **couches géographiques elles-mêmes** (objets géométriques et attributs), et non une simple image.

Pour ajouter une couche WFS :

1. ouvrir le gestionnaire de ressources et cliquer sur le bouton « WFS/OGC API - Features » (ou passer par `Couche > Ajouter une couche > Ajouter une couche WFS`, ou par l'explorateur) ;
2. créer une nouvelle connexion en cliquant sur « Nouveau », en renseignant l'URL du serveur et le nom de la connexion (exemple pour le serveur BRGM Géologie : `http://geoservices.brgm.fr/geologie`) ;
3. choisir le serveur WFS et cliquer sur **Connexion** ;
4. choisir la ou les couches à afficher ;
5. modifier le système de coordonnées si le serveur le permet, sinon activer la reprojection à la volée (voir `Préférences > Options > SCR`, EPSG:2154 - RGF93/Lambert-93 par défaut).

> [!warning] Limiter le volume téléchargé
> Il faut activer la case à cocher **« Requêter uniquement les entités dans la vue courante »** pour limiter la zone de téléchargement à la fenêtre en cours : cela conditionne directement le volume de données téléchargées. Par défaut, les serveurs WFS limitent le nombre d'enregistrements renvoyés à 1000 ; si le nombre d'enregistrements ne correspond pas aux attentes, c'est probablement que cette limite du serveur a été atteinte.
>
> Il est conseillé de charger une couche au préalable pour zoomer au plus près de la zone cible, ce qui, combiné à l'activation de « requêter uniquement dans la vue courante », permet de limiter le téléchargement. Il est également possible de contourner la limite des 1000 entités en activant la **pagination** pour les serveurs WFS de version au moins égale à 2.0 (dans la boîte de dialogue des détails de connexion du serveur).

> [!question]- Exercice : les ressources web ouvrables (WMS et WFS)
> **Objectif** : ouvrir différentes couches à partir de serveurs cartographiques en service web.
>
> Préalable : ouvrir la couche vectorielle `BD_TOPO\H_ADMINISTRATIF\COMMUNE.SHP` pour fixer l'emprise de la fenêtre carte (important pour limiter les accès réseau).
>
> 1. Ouvrir le serveur **Géoplateforme - WMS Raster Libre**, et charger la couche « Ortho 20 cm » en EPSG:2154.
> 2. Ouvrir le serveur **Géoplateforme - Service Sélection WFS**, et charger la couche `BDTOPO_V3 : cours_d_eau` en limitant le volume de téléchargement (case « Requêter uniquement les entités dans la vue courante » cochée).
>
> **Corrigé**
> Ouvrir la couche `COMMUNE` (codage ISO8859-1 pour un bon affichage des accents) depuis `BD_TOPO\H_ADMINISTRATIF`. Cette ouverture fixe l'emprise de téléchargement des services web.
>
> Pour le WMS : créer un nouveau serveur avec l'URL `https://data.geopf.fr/wms/r?VERSION=1.3.0`, se connecter, sélectionner la couche « Ortho 20 cm » en EPSG:2154, puis Ajouter.
>
> Pour le WFS : créer un nouveau serveur avec l'URL `https://data.geopf.fr/wfs/ows?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities`, se connecter, sélectionner `BDTOPO_V3 : cours_d_eau`, cocher « Requêter uniquement les entités dans la vue courante », puis Ajouter.

## La notion de projet

### Qu'est-ce qu'un projet ?

QGIS sauvegarde l'état complet du travail en cours dans un **projet**. Les informations enregistrées dans un projet comprennent notamment :

- les couches ouvertes ;
- les propriétés des couches, notamment la sémiologie (style) ;
- la projection de la carte ;
- l'étendue de la dernière zone de visualisation ;
- les éléments des compositions d'impression ainsi que leurs paramètres (mise en page) ;
- les paramètres des atlas parmi les compositions d'impression ;
- le filtrage des couches via le constructeur de requête ;
- l'état des fenêtres attributaires.

Il existe deux formats de fichier projet :

- **`.qgs`** : stocke l'ensemble des informations listées ci-dessus, sous forme de fichier texte (XML) ;
- **`.qgz`** (format par défaut) : format de compression permettant de stocker, en plus du `.qgs`, des ressources associées (par exemple des tables de données auxiliaires servant à personnaliser des étiquettes). Le fichier `.qgs` intégré dans l'archive `.qgz` peut être extrait, par exemple avec 7-zip.

### Gérer un projet

| Action | Bouton / Menu |
|---|---|
| Nouveau projet | Bouton « Nouveau », ou `Projet > Nouveau` (réinitialise la fenêtre carte et la fenêtre couches, supprime toutes les couches chargées) |
| Ouvrir un projet | Bouton « Ouvrir », ou `Projet > Ouvrir`, ou `Projet > Ouvrir un projet récent`, ou par l'explorateur de ressources |
| Enregistrer un projet | Bouton « Enregistrer », ou `Projet > Enregistrer` |
| Enregistrer sous | `Projet > Enregistrer sous`, pour sauvegarder un projet existant sous une autre destination et/ou un autre nom (y compris dans une base GeoPackage, Oracle ou PostgreSQL) |

Pour ouvrir plusieurs projets en même temps, il faut ouvrir autant de fois le logiciel QGIS. Les projets stockés dans une base GeoPackage, PostgreSQL ou Oracle peuvent également être chargés depuis le panneau Explorateur, en double-cliquant ou en les faisant glisser sur le canevas.

Par défaut, la page d'accueil de QGIS au lancement affiche une prévisualisation des derniers projets ouverts. Ce comportement est personnalisable dans `Préférences > Options > onglet Général > Fichiers projet` (page d'accueil, dernier projet, un projet spécifique, ou nouveau projet vierge).

> [!tip] Conseil
> Dans l'onglet « Général » des propriétés du projet, il est conseillé de mettre l'enregistrement des chemins en mode **relatif**. Cela permet de conserver les liens vers les couches en cas de déplacement du fichier projet (`.qgs`) et du répertoire contenant les couches, à condition que l'arborescence entre le fichier projet et les couches soit respectée.

> [!info] Sauvegarde automatique
> Il est fortement conseillé de travailler sur des projets et de faire des sauvegardes régulières. Le plugin **autosaver** permet de faire des sauvegardes à intervalles réguliers : lors d'une nouvelle sauvegarde, la version n-1 est conservée sur le disque sous le nom `monprojet.qgs~`, ce qui permet de revenir manuellement à cette version antérieure en supprimant `monprojet.qgs` et en renommant `monprojet.qgs~`.

### Les propriétés du projet

Par défaut, QGIS s'ouvre sur un nouveau projet configuré selon les options définies dans les Préférences, mais certaines options peuvent être précisées pour chaque projet via le menu `Projet > Propriétés du projet`. Les principaux onglets sont :

| Onglet | Rôle |
|---|---|
| Général | Titre du projet, couleur de sélection et de fond, unités des couches et précision, sauvegarde des chemins en relatif, ellipsoïde de mesure des distances (IAG GRS 1980 pour le RGF93) |
| Métadonnées | Auteur, date de création, langue, résumé, catégories, mots-clés, coordonnées, liens, historique |
| Paramètres de la vue | Échelles prédéfinies du projet, étendue complète du projet |
| SCR | Système de coordonnées de référence du projet (ou « Aucune projection », utile pour des mesures en coordonnées cartésiennes) |
| Transformations | Paramètres de reprojection des couches (préférences de transformation de datum) |
| Styles | Style par défaut des nouvelles couches sans style prédéfini (fichier `.qml`), transparence par défaut, attribution aléatoire des couleurs |
| Sources de données | Paramétrage de l'édition, de l'affichage et du chargement des données issues de tables PostgreSQL, protection contre la suppression accidentelle de couches |
| Relations | Définition des relations entre couches (un à un, un à plusieurs, polymorphes), utiles par exemple pour l'historique des inspections d'un tronçon de route |
| Variables | Variables disponibles au niveau du projet (en plus des variables globales) |
| Macros | Module Python sauvegardé dans le fichier `.qgs`, avec des fonctions sur les événements `openProject()`, `saveProject()`, `closeProject()` |
| QGIS Server | Capacités WMS/WFS des couches pour la publication via QGIS Server |
| Temporel | Plage temporelle du projet (manuelle ou calculée depuis les couches temporelles), exploitable dans le contrôleur temporel du canevas |
| Terrain | Paramètres par défaut du terrain et de l'élévation pour les nouvelles vues 3D |
| Sensors (Capteurs) | Configuration et activation des capteurs, qui collectent passivement des données exploitables par les expressions et scripts Python |

Une barre de recherche, en haut de la fenêtre des propriétés, permet de retrouver rapidement un élément de configuration.

> [!tip] À retenir
> Un projet QGIS (`.qgs` ou `.qgz`) conserve l'ensemble de l'état de travail (couches, styles, projection, mises en page…) ; il doit être enregistré régulièrement, de préférence avec des chemins relatifs, pour rester portable avec ses couches.

## Le gestionnaire de couches

### Fonctionnement général

Le **gestionnaire de couches** (aussi appelé zone de légende cartographique), accessible via `Vue > Panneaux > Couches` ou par clic droit dans une barre d'outils, permet de :

- **sélectionner** une couche d'un clic ;
- **afficher les propriétés** de la couche d'un double-clic ;
- afficher les différents **menus contextuels** (vecteur ou raster) par clic droit ;
- **déplacer une couche** sélectionnée par glisser-déposer : il faut maintenir un clic gauche sur le nom de la couche et déplacer la souris vers le haut ou le bas (un trait bleu indique où se trouvera la couche si l'on relâche le clic).

Pour chaque couche, une icône permet de connaître le type de représentation des objets :

- pour une **couche vecteur**, l'icône devant le nom indique le type géométrique de la donnée (point, ligne, surface ou polygones) ; la couche soulignée est la couche active ;
- pour une **couche raster**, une miniature de l'image ou un symbole « raster » est affichée devant le nom de la couche. Pour les couches raster avec un rendu de type « palette », cette palette de couleurs est visualisable en cliquant sur le symbole de déploiement situé en tête de ligne.

### Gestion de l'affichage

La case à cocher présente à gauche du nom d'une couche permet de l'**afficher ou de la cacher**. Une couche peut être sélectionnée puis glissée vers le haut ou le bas de la légende pour modifier l'**ordre d'empilement** : une couche située au sommet de la liste s'affiche au-dessus de celles qui sont plus bas dans la liste (ce comportement peut être supplanté par le panneau « Ordre des couches »).

Dans la fenêtre de gestion de couches, l'utilisateur peut également **grouper les couches par thème**, modifier les propriétés de chaque couche (couleurs, épaisseur de trait, étiquettes…), les opérations s'effectuant sur la couche sélectionnée.

> [!note] Renommer la couche
> La fonction « Renommer la couche » ne modifie pas le nom du fichier : elle modifie uniquement l'affichage de la légende dans la zone de légende cartographique et lors de l'impression de la carte.

### Boutons du gestionnaire de couches

| Bouton | Fonction |
|---|---|
| Ouvrir le panneau de style de couche | Gère les styles d'une couche de manière interactive (accès aussi aux étiquettes et au rendu 3D) ; ce panneau peut être sorti de la fenêtre principale, par exemple sur un second écran |
| Ajouter groupe | Crée un nouveau groupe de couches ; les couches peuvent y être glissées-déposées et leur visibilité gérée collectivement |
| Gérer les thèmes de cartes | Contrôle la visibilité des couches (tout visible, tout caché, visibilité des couches sélectionnées…), permet de mémoriser un réglage et de le rappeler |
| Filtrer la légende | Deux fonctions : filtrer la légende par le contenu de la carte (n'affiche que les couches représentées à l'écran, selon le zoom), ou afficher les couches privées par une expression (ex. `NOM LIKE 'B%'` n'affiche que les communes dont le nom commence par B) |
| Étendre tout / Réduire tout | Développe ou replie l'arbre des couches |
| Supprimer la couche/groupe | Décharge une couche ou un groupe de couches de QGIS |

> [!info] Groupe mutuellement exclusif
> Il est possible de spécifier qu'un groupe contient des couches mutuellement exclusives, ce qui est utile par exemple pour un groupe de fonds de plan dont un seul doit être affiché à la fois. Ce réglage s'active par clic droit sur le groupe, puis « Groupe mutuellement exclusif ».

> [!info] Notes de couche
> Il est possible d'ajouter des « notes de couche », qui permettent de stocker des messages importants pour les utilisateurs (par exemple des consignes de diffusion). Elles se créent par clic droit sur une couche, puis « Ajouter des notes de couche » (ou « Modifier les notes de couche »), et peuvent être sauvegardées dans le fichier projet ou dans le style de la couche (fichier `.qml`).

### Propriétés des couches vecteur et raster

La fenêtre des propriétés d'une couche est accessible par double-clic sur son nom dans le gestionnaire de couches, par clic droit puis « Propriétés », ou par le menu `Couche > Propriétés`. Les onglets diffèrent selon qu'il s'agit d'une couche vecteur ou raster.

**Principaux onglets pour une couche vecteur :**

| Onglet | Rôle |
|---|---|
| Information | Métadonnées et résumé issus du fournisseur, de la géométrie et des attributs |
| Source | Nom et encodage de la couche, SCR, création d'un index spatial, filtrage des entités par requête |
| Symbologie | Rendu et sémiologie des couches vectorielles |
| Étiquettes | Système d'étiquetage paramétrable pour points, lignes et polygones |
| Masques | Superposition des symboles de la couche avec d'autres couches, pour améliorer la lisibilité en cas de chevauchement |
| Diagrammes | Ajout d'une couche de graphiques (camemberts, texte, histogrammes) |
| Champs | Informations sur les champs de la couche |
| Formulaire d'attribut | Configuration du formulaire de saisie/consultation des entités |
| Jointure | Association d'entités de la couche à une autre couche via un attribut partagé (relation un à un) |
| Stockage auxiliaire | Stockage de propriétés définies par les données (étiquettes, diagrammes, symbologie) dans une base SQLite, sans éditer la source d'origine |
| Actions | Configuration d'actions déclenchables sur les attributs d'une entité |
| Rendu | Échelles maximale et minimale de visibilité, couleur/symbole spécifique par défaut, fréquence d'actualisation |
| Métadonnées | Ajout/édition d'informations exploitées par QGIS Server en cas de publication |
| Légende | Paramètres avancés du panneau de gestion des couches et de la légende du composeur d'impression |

**Principaux onglets pour une couche raster :**

| Onglet | Rôle |
|---|---|
| Information / Source | Métadonnées du fournisseur ; encodage et SCR de la source |
| Symbologie | Type de rendu (dépend du type de données) |
| Transparence | Niveaux de transparence pour visualiser les couches sous-jacentes |
| Histogramme | Distribution des bandes ou des couleurs du raster |
| Rendu | Échelle maximale et minimale de visibilité |
| Pyramides | Construction de copies des données à plus basse résolution pour améliorer les performances d'affichage (attention : construire des pyramides peut altérer le fichier original) |
| Élévation | Propriétés d'élévation de la couche dans une vue 3D et dans les outils de profil |
| Légende | Widgets intégrables dans le panneau de gestion des couches (par exemple pour configurer rapidement la transparence) |
| QGIS Serveur | Paramètres des données lors de leur publication par QGIS Server |

> [!question]- Exercice : le gestionnaire de couches
> **Objectif** : ouvrir différentes couches et les ordonner correctement pour une bonne visualisation.
>
> Ouvrir les couches BDTOPO dans l'ordre suivant :
> - `BD_TOPO\A_RESEAU_ROUTIER\ROUTE_PRIMAIRE.SHP` ;
> - `BD_TOPO\H_ADMINISTRATIF\CHEF_LIEU.SHP` ;
> - `BD_TOPO\H_ADMINISTRATIF\COMMUNE.SHP`.
>
> Ordonner ensuite les couches dans le gestionnaire de couches pour toutes les visualiser simultanément (en général : points en tête, puis lignes, puis polygones en dessous, pour éviter qu'une couche de fond ne masque les autres).
>
> **Corrigé**
> Après ouverture des trois couches vectorielles, faire glisser dans le gestionnaire de couches la couche `CHEF_LIEU` (points) et `ROUTE_PRIMAIRE` (lignes) au-dessus de `COMMUNE` (polygones), afin que le polygone des communes ne recouvre pas les chefs-lieux et les routes. Une couche placée en haut de la légende s'affiche au-dessus des couches placées plus bas.

> [!tip] À retenir
> Le gestionnaire de couches organise la visibilité, l'ordre d'empilement et l'accès aux propriétés (style, étiquettes, source) de chaque couche vecteur ou raster ; l'ordre d'empilement doit toujours placer les couches ponctuelles et linéaires au-dessus des couches surfaciques pour une lecture correcte de la carte.
