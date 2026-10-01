---
tags: [qgis, sig]
---
# Import et Export de Données
Retour : [[00 - Sommaire QGIS]] · Précédent : [[07 - Sélections et Requêtes]] · Suite : [[09 - Création de Couches]]

Ce chapitre traite de l'import de données géolocalisables (fichiers texte, GPS), de l'import de données attributaires pures avec jointure à une couche géographique, puis de l'export de données attributaires et géographiques vers différents formats.

Les données **géolocalisables** sont des données attributaires, en format feuille de calcul (`.ods`, `.xls`, `.xlsx`) ou texte délimité (`.txt`, `.csv` + `.csvt`), comportant soit des colonnes de coordonnées géographiques (géocodage direct), soit des colonnes d'identifiants permettant de les rattacher par une jointure à des objets géographiques déjà existants (géocodage indirect), tel qu'un code INSEE de commune.

## Import de données géolocalisables (texte délimité)

Pour créer une couche vectorielle de points à partir d'un fichier texte délimité contenant des coordonnées X/Y, cliquer sur l'icône **Ajouter une couche de texte délimité** dans la barre d'outils Gestion des couches (raccourci `Ctrl+Maj+T`), ou passer par `Couche > Ajouter une couche > Ajouter une couche de texte délimité`.

Un fichier texte délimité peut être un `.txt` ou un `.csv`, avec une ligne d'en-tête contenant les noms des champs. Il faut définir, pour chaque fichier, le **délimiteur de champ** (virgule, point-virgule, tabulation, ou un caractère personnalisé) et les **champs contenant l'information géographique**.

> [!warning] Attention
> L'utilisation de l'espace ou de la tabulation comme séparateur de champ peut générer des erreurs si une chaîne de caractères comporte un espace (ex. « La Flèche »). De même, utiliser la virgule comme séparateur de champ peut poser problème si la virgule sert aussi de séparateur décimal.

> [!tip] Conseil
> Les champs géométriques contiennent soit les coordonnées X et Y de chaque point, soit des coordonnées regroupées dans un seul champ au format **WKT** (Well-Known Text), qui décrit la géométrie des sommets d'un objet (et son altitude le cas échéant) sous forme textuelle standardisée par l'OGC. Dans ce format, la virgule sépare les couples de coordonnées des sommets. Il existe un équivalent binaire moins lisible mais destiné aux échanges entre bases de données, le WKB (Well-Known Binary).

### Exemple : import d'un fichier de chefs-lieux

Structure du fichier `chef-lieu.txt` :

```
ID,ID_COM,ORIGIN_NOM,NATURE,NOM,IMPORTANCE,X,Y
PAIHABIT0000000112004877,SURFCOMM0000000112528218,BDNyme,Sous-préfecture,la flèche,3,469437,6737324
```

On observe que les noms de champs, en majuscules, occupent la première ligne, séparés par une virgule ; à partir de la deuxième ligne figurent les valeurs, séparées de la même manière ; il n'y a pas de séparateur décimal, les coordonnées étant arrondies au mètre. Les deux derniers champs X et Y contiennent les coordonnées des points, en **RGF93 / Lambert-93** (reconnaissable au décalage de 6 600 000 m appliqué à l'ordonnée Y) : c'est une information importante pour choisir le bon système de coordonnées de référence (SCR) lors de l'import.

Dans la boîte de dialogue **Créer une couche depuis un fichier à texte délimité (CSV)** :

1. Sélectionner le fichier avec le bouton `...`.
2. Choisir le format (`CSV (virgule)`, délimiteur personnalisé, etc.).
3. Cocher `En-têtes en 1ère ligne` pour distinguer les noms de champs des attributs, et `Détecter les types de champs`.
4. Dans **Définition de la géométrie**, choisir `Point` puis faire correspondre `Champ X` et `Champ Y` aux colonnes du fichier (ou choisir `Well known text (WKT)` si les coordonnées sont dans un seul champ).
5. Choisir le **SCR de la géométrie**, ici `RGF93 v1 / Lambert-93`.
6. Valider par `Ajouter`.

Un clic sur `OK` crée la couche de points avec le système de coordonnées choisi ; la table attributaire comprend tous les champs et valeurs du fichier texte initial.

### Import de coordonnées GPS en degrés, minutes, secondes (DMS)

Il arrive qu'un fichier texte comporte des champs de coordonnées (longitude, latitude) exprimés en degrés, minutes et secondes d'arc, notamment dans le système **WGS 84** — par exemple un fichier d'obstacles à la circulation aérienne publié par le service de l'information aéronautique. Dans un tel fichier, les degrés et minutes d'arc sont des nombres entiers, les secondes d'arc peuvent être décimales (le point est alors le séparateur décimal), et les longitudes à l'ouest du méridien de Greenwich ainsi que les latitudes méridionales sont **négatives**.

Pour importer ce type de fichier : ouvrir la boîte de dialogue d'ajout de couche de texte délimité, choisir le bon codage (`ISO-8859-1`), vérifier le séparateur (point-virgule), définir le SCR **WGS84 (EPSG:4326)**, et cocher la case **Coordonnées DMS (Degrés Minutes Secondes)** en face des champs `Champ X` (Longitude) et `Champ Y` (Latitude). Après avoir cliqué sur `Ajouter` puis `Fermer`, la couche de points est ouverte **en lecture seule** dans la fenêtre carte, avec en table attributaire l'ensemble des champs du fichier CSV d'origine.

## Ouvrir une table attributaire pure puis géocoder par un algorithme

Il est aussi possible d'ouvrir un fichier purement attributaire (`.csv`, mais aussi directement `.ods`, `.xls`, `.xlsx`) via **Ajouter une couche vecteur** ou l'explorateur de QGIS, sans passer par l'import de texte délimité (donc sans géocodage à l'import). Dans le gestionnaire de couches, l'icône devant le nom de la couche indique alors qu'il s'agit d'une table purement attributaire (pas de géométrie).

Pour vérifier ou corriger l'encodage de la table une fois ouverte : Propriétés de la couche → onglet **Source** → **Encodage des données sources** (par exemple `ISO-8859-1`).

Pour géocoder a posteriori une telle table (créer une couche géographique à partir de colonnes X/Y), on utilise l'algorithme de traitement **Créer une couche de points à partir d'une table** (`native:createpointslayerfromtable`) :

1. Activer les algorithmes via `Traitement > Boîte à outils`.
2. Rechercher « couche de points » dans la boîte de recherche, ou taper directement le nom de l'algorithme précédé d'un `a` dans la barre de localisation.
3. Double-cliquer sur l'algorithme pour l'ouvrir.
4. Renseigner la **Couche source**, le **Champ X**, le **Champ Y**, éventuellement les champs Z et M optionnels, le **SCR cible**, et le type de sortie (`Créer une couche temporaire` par défaut, ou `Enregistrer vers un fichier` / `Enregistrer dans un GeoPackage` / `Enregistrer vers une table de base de données`).
5. Cliquer sur **Exécuter**.

La couche mémoire créée (nommée « Points depuis une table ») est **temporaire** : si l'on souhaite la conserver, il faut l'enregistrer explicitement (`Enregistrer sous...`).

## Importer des données saisies par GPS au format GPX

Le **GPS** (Global Positioning System) permet d'obtenir sa position exacte grâce à des signaux satellites (latitude, longitude, élévation). Le système européen équivalent, sous contrôle civil, est **Galileo**.

La plupart des récepteurs stockent trois types d'objets basiques : les **points d'intérêt** (waypoints), les **itinéraires** (routes) et les **tracks** (journal de suivi des déplacements dans le temps). QGIS affiche les points d'intérêt dans des couches de points, tandis que les itinéraires et les tracks sont affichés dans des couches linéaires.

Le format **GPX** (GPS eXchange Format) est un format ouvert, standard de fait, permettant l'échange de coordonnées GPS et décrivant une collection de points de cheminement (waypoint), de trace (track) ou d'itinéraire (route).

Pour importer des données GPX :

- Ouvrir une couche vectorielle avec `Couche > Ajouter une couche vecteur` (ou l'icône correspondante), et choisir le type de fichier « GPS eXchange format (\*.GPX) », **ou**
- dans l'explorateur, se positionner sur le fichier `.gpx`, sélectionner toutes les sous-couches proposées (`route_points`, `routes`, `track_points`, `tracks`, `waypoints`), puis faire un clic droit → **Ajouter les couches sélectionnées au projet**.

Toutes les couches sont alors importées et affichées.

> [!tip] Remarque
> Les couches issues d'un fichier GPX sont systématiquement importées avec le système géodésique de référence du GPS, le **WGS 84 (EPSG:4326)**. QGIS les reprojette « à la volée » pour qu'elles se superposent correctement aux couches dans un autre système de référence (par exemple RGF93 / Lambert-93).

> [!warning] Attention
> Les couches issues d'un fichier GPX importé sont en **lecture seule**, donc non modifiables.

## Import de données attributaires suivi d'une jointure

La **jointure attributaire** permet de joindre une table attributaire pure (fichier `.txt`, `.csv`, `.dbf`, `.xls`, `.xlsx`, `.ods`, ne comportant pas d'objets géométriques) avec une couche vectorielle géographique déjà chargée dans QGIS. Les formats autorisés pour la table à joindre sont les formats texte délimité, les formats de feuille de calcul, et les formats de bases de données gérés par QGIS (SQLite, PostgreSQL).

> [!warning] Attention
> Il faut veiller à ce qu'une ligne de la table attributaire de la couche vectorielle soit en correspondance avec au plus une (0 ou 1) ligne de la table attributaire à joindre, sinon QGIS prendra une ligne correspondante de façon imprévisible.

### Méthode

1. Ouvrir la couche géographique cible (ex. `COMMUNE.SHP`) avec `Couche > Ajouter une couche vecteur`.
2. Ouvrir la couche attributaire à joindre (ex. `ATTRIBUTS_COMMUNES.csv`) avec `Couche > Ajouter une couche de texte délimité`, en choisissant le type de fichier « Valeurs séparées par une virgule [OGR] (\*.csv) ».
3. Repérer, dans les deux tables, le champ commun qui servira de clé de jointure — par exemple le code INSEE, présent en tant que `CODE_INSEE` dans la couche COMMUNE et `INSEE_COMM` dans la table ATTRIBUTS_COMMUNES.

> [!tip] Conseil
> Même si QGIS peut joindre des champs de types différents (numérique et chaîne de caractères), il est conseillé d'utiliser des **champs de même type**.

4. Ouvrir les Propriétés de la couche géographique (double-clic sur son nom), onglet **Jointures**, cliquer sur le bouton `+` : **Ajouter une jointure vectorielle**.
5. Renseigner : la couche attributaire à joindre, le champ de jointure de cette couche (`INSEE_COMM`), le champ cible de la couche géographique (`CODE_INSEE`).
6. Choisir de **préfixer les champs de la table à joindre** avec un préfixe court (par défaut, c'est le nom de la table distante, ce qui peut conduire à des noms de champs très longs, posant problème avec le format Shapefile qui limite les noms de champs à 10 caractères).
7. Valider par `OK`.

Les attributs de la couche jointe sont alors ajoutés à chaque entité de la couche vectorielle géographique, avec le préfixe choisi (ex. `J_NOM_COMM`).

L'enregistrement du projet QGIS permet de **sauvegarder cette jointure** et de prendre en compte les mises à jour successives de la couche attributaire (le fichier `.csv`) effectuées hors QGIS. Le résultat de la jointure peut aussi être sauvegardé dans une nouvelle table vecteur (`Couche > Sauvegarder sous...` ou clic droit sur la couche → `Exporter/Sauvegarder les entités sous...`).

> [!tip] Remarque — édition des champs de jointure
> Si l'option « Jointure de table éditable » n'a pas été activée lors de la définition de la jointure, les champs joints ne sont pas directement éditables dans la couche résultante ; on ne peut alors les modifier qu'en passant par le fichier de la table d'origine, ou en sauvegardant la couche vecteur résultat de la jointure comme nouvelle table. Si cette option a été activée, les entités de la table jointe peuvent être modifiées, à condition d'activer également le mode édition pour la couche d'origine des entités jointes.

> [!tip] Remarque — types de champs et fichier CSVT
> Si on importe un fichier CSV en passant par l'explorateur de QGIS avec « Ajouter la couche au projet », toutes les colonnes du fichier sont interprétées comme des chaînes de caractères. Pour préciser à QGIS les types de champs (notamment les champs numériques), il est nécessaire d'associer au fichier CSV un fichier **CSVT** portant le même nom et enregistré dans le même répertoire : il contient la structure et le format des champs, et est automatiquement détecté lorsque le CSV est importé dans QGIS. Sinon, il faut activer l'option `Détecter les types de champs` dans l'interface d'ouverture.

> [!tip] Remarque — filtrage sur champs joints
> Pour filtrer une table possédant des champs joints, QGIS propose de transformer la couche en **couche virtuelle** (les champs joints ne peuvent être filtrés autrement). La notion de couche virtuelle, qui permet de réaliser des requêtes SQL sur une ou plusieurs tables ouvertes dans QGIS, est développée dans la formation Perfectionnement.

> [!question]- Exercice 19 : import de données attributaires et import de données géographiques
> **Objectif** : réaliser une analyse thématique à partir de données attributaires jointes et créer une couche géographique à partir d'un fichier texte.
>
> Ouvrir les couches vectorielles `BD_TOPO/H_ADMINISTRATIF/COMMUNE.SHP` et `Contours_Iris/carto/IRIS_extrait72.shp`, ainsi que les fichiers attributaires `Divers/base-cc-carac-emploi-09.csv` et `Divers/BTX_IC_ACT_2008_72.csv`.
>
> 1. Joindre les données `base-cc-carac-emploi-09` à la table COMMUNE, et représenter les actifs salariés 2009 (`P09_SAL15P`) et actifs non salariés 2009 (`P09_NSAL15P`) proportionnellement à la population (`POPUL`).
> 2. Joindre les données `BTX_IC_ACT_2008_72` à la table IRIS_extrait72, et représenter la population 2008 par tranche d'âge 15-24 ans, 25-54 ans, 55-64 ans proportionnellement à la population 15-64 ans.
>
> > Corrigé : après jointure sur le code INSEE (pour COMMUNE) et le code IRIS (pour IRIS_extrait72), une symbologie de type « diagramme camembert » (Propriétés de la couche → Diagrammes) appliquée aux champs joints permet d'obtenir une analyse thématique par secteurs, chaque commune ou IRIS affichant un diagramme dont la taille est proportionnelle à la population et les parts proportionnelles aux effectifs de chaque catégorie.

## Export de données attributaires

La commande `Menu Couche > Sauvegarder sous...`, au format « Valeurs séparées par une virgule », permet de sauvegarder les données attributaires d'une couche, avec ou sans sa géométrie. Le fichier généré est au format **CSV** (texte délimité).

Les principales **options OGR** de création pour la couche sont :

| Option | Valeurs | Effet |
|---|---|---|
| `CREATE_CSVT` | `YES` / `NO` | crée un fichier `.csvt` associé, décrivant le type de chaque colonne |
| `GEOMETRY` | `AS_WKT` / `AS_XY` / `AS_XYZ` | crée (ou non) un champ géométrique en première colonne du fichier texte |
| `LINEFORMAT` | `CRLF` / `LF` | format de fin de ligne Dos ou Unix |
| `SEPARATOR` | `COMMA` / `SEMICOLON` / `TAB` | virgule, point-virgule ou tabulation |
| `WRITE_BOM` | `YES` / `NO` | écrit un marqueur d'ordre des octets UTF-8 en tête du fichier, pour améliorer la compatibilité avec certains logiciels |

> [!tip] Remarque
> Le champ géométrique WKT est sans objet pour l'export de données purement attributaires (aucune géométrie).

### Exemple : export de la couche BATI_REMARQUABLE en CSV

1. Ouvrir la couche `BATI_REMARQUABLE.SHP` (répertoire `BD_TOPO/E_BATI`).
2. Clic droit sur la couche → **Exporter/Sauvegarder les entités sous...**.
3. Choisir le format `Valeurs séparées par une virgule (CSV)`, nommer le fichier (l'extension `.csv` est ajoutée automatiquement), localiser le répertoire de sauvegarde, choisir le codage `ISO-8859-1`.
4. Dans les **Options de la couche** : `CREATE_CSVT → YES`, `GEOMETRY → <Défaut>`, `LIGNEFORMAT → LF`, `SEPARATOR → SEMICOLON`, `STRING_QUOTING → IF_AMBIGUOUS`, `WRITE_BOM → NO`.
5. Valider par `OK`.

Deux fichiers texte sont créés : `Bati_Remarquable.csv`, contenant en première ligne les noms des champs séparés par un point-virgule puis les données, et `Bati_Remarquable.csvt`, contenant la structure et le format des champs (par exemple `String(24),Real(6.1),Real(7.1),String(8),String(25),Integer(4),Real(8.2),Real(8.2)`).

> [!tip] Remarque
> Sans ce fichier CSVT, lorsqu'on réimporte le fichier CSV dans QGIS sans activer l'option `Détecter les types de champs`, toutes les colonnes sont interprétées comme des chaînes de caractères. Un fichier CSVT portant le même nom que le fichier CSV et enregistré dans le même répertoire est automatiquement détecté à l'import : il permet de conserver tous les types de champs reconnus par QGIS, notamment les champs numériques.

### Export au format feuille de calcul (ODS, XLSX)

N'importe quelle couche peut être exportée dans un format « feuille de calcul » (ODS de LibreOffice, ou XLSX). Par clic droit sur la couche → `Exporter/Sauvegarder les entités sous...`, choisir le format `Tableur Open Document [ODS]`. Dans les options de la couche, la variable `OGR_ODS_FIELD_TYPE` peut être positionnée à `STRING` si l'on souhaite exporter tous les champs en chaîne de caractères ; par défaut, le mode `AUTO` est actif et conserve les types détectés.

## Export de données géographiques

### Export CSV avec géométrie (WKT)

On peut exporter une couche géographique de points, de polylignes ou de polygones en stockant la géométrie des objets dans un champ texte au format **WKT**. C'est le seul moyen d'exporter des couches de polylignes ou de polygones dans un format texte délimité, avec l'enregistrement des coordonnées de tous les sommets constituant les objets géographiques.

Exemple avec la couche `TERRAIN_SPORT.SHP` (polygones, répertoire `BD_TOPO/E_BATI`) :

1. Clic droit sur la couche → `Exporter/Sauvegarder les entités sous...`.
2. Choisir le format `Valeurs séparées par une virgule`, codage `ISO-8859-1`, nommer le fichier (`Terrain_Sport`).
3. Dans les Options de la couche : `CREATE_CSVT → YES`, `GEOMETRY → AS_WKT`, `LIGNEFORMAT → LF`, `SEPARATOR → SEMICOLON`, `WRITE_BOM → NO`.
4. Valider par `OK`.

Le premier champ nommé `WKT` du fichier texte délimité créé comprend la description de la géométrie de chaque objet dans le format Well-Known Text, par exemple :

```
WKT;ID;PREC_PLANI;PREC_ALTI;NATURE;Z_MOYEN
"POLYGON Z ((465174.6 6735209.4 62.6,465208.2 6735194.2 62.6,...))";TERRSPOR0000...;1.5;1.0;Terrain de tennis;62.60
```

QGIS sait ouvrir directement ce type de fichier texte comprenant un champ WKT : via **Ajouter une couche vecteur**, sélectionner le type `Valeurs séparées par une virgule [OGR] (.csv)`, le codage `ISO-8859-1`, le fichier, puis (après validation) le SCR (par exemple RGF93 / Lambert-93). Aucune autre information n'est demandée et la couche est créée, en **lecture seule**, et affichée dans la fenêtre carte, avec sa table attributaire comprenant le champ WKT décrivant la géométrie des polygones.

L'import d'un tel fichier peut aussi être réalisé avec la commande « Créer une couche depuis un fichier à texte délimité (CSV) » : dans la boîte de dialogue, choisir l'option `Well known text (WKT)` (plutôt que Point) pour la définition de la géométrie, et sélectionner le champ `WKT` correspondant. Dans ce cas, la table attributaire de la couche créée ne comprend pas le champ WKT (il est utilisé uniquement pour construire la géométrie).

### Export de données géographiques au format KML

Le format **KML** (Keyhole Markup Language) est un standard international de données géographiques ouvert, développé par la société Keyhole Inc., proposé par Google et adopté par l'OGC (Open Geospatial Consortium) en 2007. C'est un langage basé sur XML, adapté aux données géographiques, et utilisé notamment dans Google Earth et Google Maps.

Le système de coordonnées de référence associé (`LonLat84_5773`) est issu du WGS84 : les coordonnées sont exprimées en degrés décimaux (longitude, puis latitude, dans cet ordre) dans le système de référence **WGS84 (EPSG:4326)**.

Une couche KML est une couche géographique vectorielle de points, de polylignes ou de polygones ; son export se fait de la même manière que pour les autres formats, via `Exporter/Sauvegarder les entités sous...` en choisissant le format `Keyhole Markup Language [KML]`.

> [!tip] À retenir
> L'import de données attributaires géolocalisables se fait via « Ajouter une couche de texte délimité », en précisant le délimiteur, les champs de coordonnées (X/Y ou WKT, éventuellement en degrés-minutes-secondes) et le bon système de coordonnées de référence. La jointure attributaire permet d'enrichir une couche géographique avec une table externe (CSV, feuille de calcul) sur un champ commun, à condition de respecter la relation 0 ou 1 pour 1. L'export de données attributaires ou géographiques utilise « Exporter/Sauvegarder les entités sous... » vers de nombreux formats (CSV, ODS/XLSX, GeoPackage, KML...), avec des options spécifiques selon le format (CSVT, séparateur, encodage, géométrie en WKT).
