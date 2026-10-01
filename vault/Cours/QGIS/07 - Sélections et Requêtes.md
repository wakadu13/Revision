---
tags: [qgis, sig]
---
# Sélections et Requêtes
Retour : [[00 - Sommaire QGIS]] · Précédent : [[06 - Mise en Page]] · Suite : [[08 - Import et Export de Données]]

Ce chapitre présente les différentes manières d'extraire un sous-ensemble d'entités dans QGIS : le filtrage attributaire, la sélection par expression et la sélection spatiale (relation entre les objets géographiques de plusieurs couches). Il se termine par les méthodes d'export du résultat d'un filtre ou d'une sélection.

## Filtrage d'entités et sélection attributaire : deux notions à ne pas confondre

QGIS propose deux modes de « sélection attributaire » qui ne conduisent pas aux mêmes résultats, même si leurs boîtes de dialogue se ressemblent.

Le **filtrage**, qui s'appuie sur le **constructeur de requête**, agit comme un filtre SQL de la forme `SELECT * FROM Couche WHERE condition`. Il définit un sous-ensemble d'entités qui seront seules chargées en mémoire dans QGIS : après filtrage, seules les entités correspondant à la requête apparaissent dans la fenêtre carte et dans la table attributaire. Ce filtre reste actif tant que l'expression n'a pas été effacée dans le constructeur de requête ; il est sauvegardé en enregistrant le projet, et la couche filtrée peut être exportée comme nouvelle couche (clic droit sur la couche puis « Exporter/Sauvegarder les entités sous... »).

La **sélection par expression** consiste, elle, à « marquer » des entités dans la fenêtre carte au moyen d'une couleur particulière (le jaune par défaut, couleur paramétrable). Dans la table attributaire, les lignes des entités sélectionnées apparaissent en surbrillance, mais **toutes les entités de la couche restent chargées et visibles**, contrairement au filtrage.

> [!warning] Attention
> Une sélection n'est **pas** sauvegardée dans le projet : elle est perdue à la réouverture du fichier projet enregistré. Le filtrage, lui, est bien conservé.

## Filtrage avec le constructeur de requête

Trois méthodes permettent d'accéder au **Constructeur de requête** :

| Méthode | Accès |
|---|---|
| 1 | Clic droit sur la couche active dans le panneau Couches → **Filtrer...** |
| 2 | Propriétés de la couche → onglet **Source** → bouton **Constructeur de requête** |
| 3 | Menu **Couche → Filtrer** |

La boîte de dialogue Constructeur de requête comporte plusieurs zones :

- **Champs** : liste tous les attributs de la couche. Un double-clic sur un champ l'ajoute à la clause `WHERE` (cadre Expression).
- **Valeurs** : affiche tout ou partie des valeurs du champ sélectionné. Le bouton `[Tout]` liste toutes les valeurs, `[Échantillon]` seulement les 25 premières. Un double-clic ajoute la valeur à l'expression. Si la couche a déjà été filtrée, seules les valeurs du sous-ensemble déjà sélectionné sont proposées ; pour voir toutes les valeurs, cocher `Utiliser la couche non filtrée`.
- **Opérateurs** : boutons pour les opérateurs les plus courants (`=`, `<`, `>`, `LIKE`, `IN`, `AND`, `OR`, `NOT`...).
- **Expression de filtrage** : contient la clause `WHERE` littérale de la requête.

Les boutons `Tester` (compte le nombre d'entités correspondant à la requête), `Effacer`, `Enregistrer`, `Charger`, `OK` (exécute et ferme) et `Annuler` complètent la boîte de dialogue.

> [!example] Exemple
> Sélectionner les communes du canton de MALICORNE-SUR-SARTHE dans la couche COMMUNE (BD_TOPO/H_ADMINISTRATIF) :
> 1. Ouvrir le constructeur de requête sur la couche COMMUNE.
> 2. Double-cliquer sur le champ `CANTON` (il s'ajoute entre doubles guillemets, syntaxe SQL des noms de champs).
> 3. Cliquer sur l'opérateur `=`.
> 4. Cliquer sur `CANTON` dans le cadre Champs puis sur `Tout` dans le cadre Valeurs, puis double-cliquer sur `MALICORNE-SUR-SARTHE` (elle s'ajoute entre simples quotes, syntaxe SQL des valeurs).
>
> L'expression obtenue est : `"CANTON" = 'MALICORNE-SUR-SARTHE'`
>
> La requête SQL complète exécutée est :
> ```sql
> SELECT * FROM COMMUNE WHERE "CANTON" = 'MALICORNE-SUR-SARTHE'
> ```
> Le bouton `Tester` indique alors : « La clause WHERE a retourné 4 lignes ». Après validation par `OK`, seules ces 4 communes restent visibles dans la carte et dans la table attributaire.

L'expression de la clause `WHERE` reste visible dans l'onglet **Source** des Propriétés de la couche, dans le cadre « Filtre d'entité du fournisseur de données ». Tant que la requête n'est pas effacée, seul le sous-ensemble filtré est affiché ; un petit **symbole de filtrage** apparaît sur la couche dans le panneau Couches et une info-bulle (survol du nom) affiche l'expression active.

## Sélection par expression

Il existe deux façons d'accéder à la sélection par expression :

- Rendre la couche active, puis dans la barre d'outils **Attributs**, cliquer sur le bouton `ε` (epsilon) « Sélectionne les entités en utilisant une expression » (raccourci `Ctrl+F3`).
- Dans la table attributaire, cliquer sur le même bouton `ε`.

La boîte de dialogue **Sélection par expression** (très proche du calculateur de champs) propose :

- une **liste de fonctions** très large : opérateurs booléens et arithmétiques, branchements conditionnels, fonctions mathématiques, de conversion, de date, de traitement de chaînes de caractères, de géométrie (opérateurs spatiaux et géotraitement), et fonctions d'information sur les enregistrements ;
- un cadre **Opérateurs** avec les boutons les plus courants et les parenthèses ;
- un cadre **Expression** contenant l'expression littérale ;
- un menu déroulant **Sélection**, avec quatre actions : `Sélectionner des entités`, `Ajouter à la sélection courante`, `Supprimer de la sélection actuelle`, `Filtrer la sélection actuelle` ;
- une zone de **Prévisualisation**, qui fait défiler les entités une par une pour vérifier le résultat de l'expression ;
- lorsqu'on clique sur un champ, un cadre **Valeurs** apparaît, listant les valeurs uniques ou un échantillon de 10, exactement comme dans le constructeur de requête.

> [!example] Exemple
> Pour sélectionner les communes du canton de MALICORNE-SUR-SARTHE : dans la branche **Champs et Valeurs**, double-cliquer sur `CANTON`, cliquer sur l'opérateur `=`, cliquer sur `Tous uniques` dans le cadre Valeurs puis double-cliquer sur `MALICORNE-SUR-SARTHE`. L'expression obtenue est :
> ```sql
> "CANTON" = 'MALICORNE-SUR-SARTHE'
> ```
> Un clic sur **Sélection** fait apparaître les entités correspondantes en jaune dans la carte, alors que toutes les autres communes restent affichées normalement (contrairement au constructeur de requête).

Le menu déroulant Sélection permet aussi d'enchaîner des opérations : par exemple, sélectionner d'abord les communes du canton de Malicorne-sur-Sarthe, puis **Supprimer de la sélection actuelle** celles ayant moins de 500 habitants (`"POPUL" < 500`), ou à l'inverse partir d'une expression sur la population puis **Ajouter à la sélection courante** un filtre sur le canton. Il est possible de remplacer un tel enchaînement de deux sélections successives par une seule expression combinant les deux conditions avec `AND` ou `OR`.

Pour **désélectionner** toutes les entités, utiliser le bouton « Désélectionner toutes les entités » de la barre d'outils Attributs ou de la table attributaire.

> [!tip] Sauvegarde de la sélection
> La sélection par expression n'est **pas** sauvegardée en enregistrant le projet. Cependant, une fois exécutée, elle est mémorisée dans l'item « Récent (Sélection) » de la liste des fonctions de la boîte de dialogue Sélection par expression ; un double-clic la réaffiche, et il est possible de la transformer en expression stockée (bouton disquette) pour la retrouver dans les « expressions de l'utilisateur ».
>
> Pour sauvegarder le **résultat** d'une sélection comme une nouvelle couche : clic droit sur la couche → « Exporter/Sauvegarder les entités sélectionnées sous... ».

## Sélectionner ou filtrer depuis le formulaire de la table attributaire

Une autre méthode, plus simple pour un utilisateur occasionnel, consiste à utiliser le bouton **filtre** (entonnoir) de la barre d'outils de la table attributaire. Chaque champ dispose alors d'un menu déroulant d'opérateurs (`Égal à`, `Différent de`, `Contient`, `Ne contient pas`, `Commence par`, `Se termine par`...) où saisir directement un critère. On peut ensuite cliquer sur `Sélection des entités` pour sélectionner les entités correspondantes, ou sur `Filtrer les entités` pour ne montrer dans la table que les entités sélectionnées. Cette opération génère automatiquement, en coulisse, un filtre équivalent à une expression (filtre avancé).

## Tableau de synthèse

| Outil | Où | Résultat | Sauvegardé dans le projet |
|---|---|---|---|
| Filtre par la table attributaire (case, colonne) | Table attributaire | Limite l'affichage de la table uniquement | Non |
| Filtrer / Constructeur de requête | Clic droit couche → Filtrer, ou Propriétés → Source | Sous-ensemble d'entités chargées dans QGIS (carte + table) | Oui |
| Sélection graphique | Barre d'outils Attributs (rectangle, polygone, à main levée) | Entités « marquées » en couleur, toute la couche reste visible | Non |
| Sélection par expression | Barre d'outils Attributs ou table attributaire (bouton ε) | Entités « marquées » via une expression, toute la couche reste visible | Non |

## Requêtes spatiales

Une requête spatiale met en relation les objets géographiques de deux couches selon leur position relative. QGIS propose deux algorithmes principaux :

- **Sélection par localisation** crée une sélection sur une couche vectorielle : les critères sont basés sur la relation spatiale entre chaque entité de cette couche et les entités d'une autre couche. Accessible par le menu `Vecteur > Outils de recherche > Sélection par localisation`. Pour être sauvegardée, la sélection doit être enregistrée comme une nouvelle couche vectorielle.
- **Extraire par localisation** crée une **nouvelle couche vectorielle** à partir d'une couche d'entrée, ne contenant que les entités correspondant à la relation spatiale définie avec une autre couche. Disponible uniquement dans la boîte à outils de traitement (menu `Traitement > Boîte à outils`).

> [!info] Complément
> Pour un algorithme qui génère une couche en sortie (comme « Extraire par localisation »), le résultat peut être obtenu sous plusieurs formes : `Créer une couche temporaire` (en mémoire, valide seulement le temps de la session), `Enregistrer vers un fichier`, `Enregistrer dans un GeoPackage` ou `Enregistrer vers une table de base de données`.

> [!example] Exemple
> Pour sélectionner tous les objets de la couche ZONE_VEGETATION qui intersectent la commune de Clermont-Créans : `Vecteur > Outils de recherche > Sélection par localisation`, choisir la couche source ZONE_VEGETATION, le prédicat `intersecte`, et la couche de référence COMMUNE avec le ou les objets sélectionnés (ici la commune de Clermont-Créans). Le résultat apparaît en jaune : tous les polygones de végétation intersectant la commune, y compris ceux qui débordent de son emprise.

### Les prédicats géométriques

Les relations spatiales entre objets géométriques s'appuient sur les notions d'**intérieur**, de **limite** et d'**extérieur** des objets (schéma spatial OGC) :

| Type | Intérieur | Limite | Extérieur |
|---|---|---|---|
| Point (dim 0) | le point lui-même | n'existe pas | tout le reste |
| Polyligne (dim 1) | la ligne, hors extrémités | les 2 points d'extrémité | tout le reste |
| Polygone (dim 2) | la surface, hors périmètre | le périmètre (polyligne fermée) | tout le reste |

QGIS propose 8 prédicats spatiaux conformes aux normes OGC, applicables à tous les types d'objets (point, polyligne, polygone) sauf mention contraire :

- **Est égal** (`Equals`) : les géométries sont topologiquement identiques (peu importe le nombre de sommets).
- **Est disjoint** (`Disjoint`) : les géométries n'ont aucun point commun.
- **Intersecte** (`Intersects`) : les géométries ont au moins un point commun.
- **Est à l'intérieur de** (`Within`) : toute la géométrie de l'objet contenu est à l'intérieur de l'objet contenant.
- **Contient** (`Contains`) : l'objet contient toute la géométrie de l'objet contenu (relation inverse de « Est à l'intérieur de »).
- **Chevauche** (`Overlaps`) : une partie seulement des objets est contenue dans l'autre ; applicable entre objets de même type (polyligne/polyligne, polygone/polygone).
- **Croise** (`Crosses`) : les intérieurs des objets ont au moins un point commun mais pas tous ; le résultat du croisement doit être un objet de dimension inférieure à celle de l'objet de plus grande dimension (par exemple, une polyligne peut croiser un polygone si elle n'est pas entièrement contenue dedans ; deux polygones ne peuvent jamais se croiser, dans ce cas ils se chevauchent).
- **Touche** (`Touches`) : les limites des objets ont au moins un point commun et les intérieurs n'ont pas de point commun (non applicable aux relations point/point, un point n'ayant pas de limite).

## Tableau de synthèse des filtres et sélections

| Outil | Type | Sauvegarde |
|---|---|---|
| Filtre par la table attributaire | Attributaire | Non (perdu à la fermeture de la table) |
| Constructeur de requête (filtrage) | Attributaire | Oui, dans le projet |
| Sélection graphique | Graphique | Non |
| Sélection par expression | Attributaire | Non |
| Sélection ou requête spatiale | Spatiale | Non (le résultat doit être exporté comme nouvelle couche) |

## Sauvegarder le résultat d'un filtre ou d'une sélection

Pour enregistrer le résultat d'un **filtrage** (constructeur de requête, sous-ensemble d'une couche) comme une nouvelle couche : clic droit sur la couche → **Exporter → Sauvegarder les entités sous...**.

Pour une **sélection par expression ou une requête spatiale** : dans le menu Couche, `Sauvegarder sous...` ou `N'enregistrer que les entités sélectionnées sous...`.

Dans la boîte de dialogue « Enregistrer la couche vectorielle sous... », les principales options sont :

- **Format** : n'importe quel format vecteur auquel GDAL peut écrire (GeoPackage, GML, ESRI Shapefile, AutoCAD DXF, ESRI FileGDB, MapInfo TAB ou MIF, SpatiaLite, CSV, KML, ODS...).
- **Nom de la couche** : disponible pour un format de type conteneur (ex. GeoPackage).
- **Encodage des caractères**.
- **N'enregistrer que les entités sélectionnées** (case à cocher).
- **Sélectionner les champs à exporter et leurs options d'export** : choix des champs à conserver (boutons Sélectionner tout / Tout désélectionner), option pour utiliser les alias de champ comme nom exporté, et remplacement des valeurs brutes par les valeurs affichées lorsque des widgets de formulaire (value map) sont utilisés.

> [!tip] À retenir
> Le filtrage (constructeur de requête) réduit les entités **chargées en mémoire** et se sauvegarde avec le projet ; la sélection par expression « marque » des entités sans changer ce qui est chargé, et se perd à la fermeture du projet. Les requêtes spatiales comparent la position relative de deux couches à l'aide de prédicats géométriques normalisés OGC (intersecte, contient, touche, croise...) ; leur résultat doit être explicitement exporté pour être conservé.

> [!question]- Exercice 17 : sélection par expression et constructeur de requête
> **Objectif** : utiliser les deux modes de sélection et constater les résultats différents.
>
> Ouvrir la couche vectorielle `BD_TOPO/H_ADMINISTRATIF/COMMUNE.SHP`.
> 1. À l'aide de la sélection par expression, surligner les communes qui ont une population supérieure à 1000 habitants.
> 2. À l'aide du constructeur de requête, filtrer la table COMMUNE pour n'afficher que les communes qui ont une population supérieure à 1000 habitants.
> Comparer les résultats.
>
> > Corrigé : l'expression `"POPUL" > 1000` est identique dans les deux outils. Avec la sélection par expression, toutes les communes restent visibles dans la carte, seules celles correspondant au critère apparaissent en jaune. Avec le constructeur de requête, seules les communes de plus de 1000 habitants restent affichées dans la carte et dans la table attributaire, les autres disparaissent tant que le filtre n'est pas effacé.

> [!question]- Exercice 18 : requêtes spatiales
> **Objectif** : sélectionner des objets à l'aide des opérateurs spatiaux de la sélection ou de l'extraction par localisation.
>
> Ouvrir les couches `BD_TOPO/A_RESEAU_ROUTIER/ROUTE.SHP` et `BD_TOPO/D_HYDROGRAPHIE/SURFACE_EAU.SHP`. Créer une nouvelle couche de tous les tronçons de la couche ROUTE qui **intersectent** les objets de la couche SURFACE_EAU (indice : `Sélectionner à l'aide d'une expression` puis `Extraire par localisation`), à enregistrer dans un GeoPackage nommé `Intersect_route_surface.gpkg`.
>
> Ouvrir ensuite `BD_TOPO/F_VEGETATION/ZONE_VEGETATION.SHP` et `BD_TOPO/H_ADMINISTRATIF/COMMUNE.SHP`. Créer une nouvelle couche depuis la sélection des peupleraies de ZONE_VEGETATION qui sont **à l'intérieur** de la commune de La Flèche (indice : sélectionner la commune de la Flèche avec `Sélectionner à l'aide d'une expression`, puis utiliser `Extraire par localisation`), à enregistrer dans `Interieur_ZV_Lafleche.gpkg`.
