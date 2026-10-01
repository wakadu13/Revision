---
tags: [qgis, sig]
---
# Navigation et Sélections Graphiques
Retour : [[00 - Sommaire QGIS]] · Précédent : [[02 - Ouverture et Visualisation]] · Suite : [[04 - Représentation des Données]]

Ce chapitre présente les outils de base pour se déplacer dans une carte QGIS, consulter les données des couches, sélectionner des entités graphiquement et utiliser quelques outils généraux (mesures, infobulles, signets, annotations, décorations, barre de localisation).

## Naviguer dans la carte

La barre d'outils **Navigation Cartographique** (accessible aussi via le menu **Vue**) regroupe les commandes de déplacement et de zoom :

| Outil | Fonction |
|---|---|
| Se déplacer dans la carte | Panoramique (glisser la carte avec la souris, la « main ») |
| Se déplacer jusqu'à la sélection | Centre la vue sur les entités sélectionnées |
| Zoom + / Zoom - | Zoom avant / arrière |
| Zoom sur l'étendue de la carte (`Ctrl+Maj+F`) | Affiche l'ensemble des couches |
| Zoom sur la sélection | Zoome sur les entités sélectionnées |
| Zoom sur la couche | Zoome sur l'étendue d'une couche |
| Zoom à la résolution native (1:1) | Pour les rasters, affiche chaque pixel image à l'écran |
| Zoom précédent / suivant | Navigue dans l'historique des vues |
| Nouvelle vue cartographique / 3D | Ouvre une fenêtre supplémentaire liée au projet |
| Nouveau signet / Liste des signets | Gère les signets spatiaux |
| Panneau de contrôle temporel | Anime des données temporelles |
| Actualiser (`F5`) | Redessine la carte |

Le panneau **Vue d'ensemble** (activable par clic droit dans les barres d'outils) affiche une miniature de toute la zone couverte par le projet : un rectangle rouge y indique l'emprise actuellement affichée dans la fenêtre principale. Pour qu'une couche apparaisse dans ce panneau, il faut faire un clic droit sur elle puis choisir **Montrer dans l'aperçu**.

### Les vues cartographiques multiples

QGIS permet d'ajouter une ou plusieurs **vues cartographiques** supplémentaires au projet (menu **Vue -> Nouvelle vue cartographique**). Chaque vue dispose de sa propre barre d'outils (zoom sur l'emprise, zoom sur la sélection, zoom sur la couche, thème de visibilité, paramètres de la vue).

Dans les **paramètres de la vue**, on peut notamment :

- **Synchroniser le centre de la vue avec la carte principale** ;
- **Synchroniser la vue avec la sélection** : la vue se recentre automatiquement sur les entités sélectionnées dans une couche donnée ;
- régler l'**échelle**, la **rotation**, l'**agrandissement** ;
- appliquer un **thème de visibilité** (`Configurer le thème de la vue`) indépendant de la carte principale, pour par exemple afficher un fond de plan différent dans chaque vue.

Ce mécanisme est très utile en configuration double écran : on peut garder une vue d'ensemble sur un écran et zoomer en détail sur l'autre, ou afficher des couches différentes (par exemple un fond SCAN 100 sur une vue pendant que la vue principale montre les limites communales).

## La barre d'outils Attributs

La barre d'outils **Attributs** (également accessible en partie depuis le menu **Vue**) regroupe les commandes qui portent sur les données des couches :

- Identifier les entités ;
- Ouvrir la calculatrice de champs ;
- Boîtes à outils (de traitement) ;
- Montrer le résumé statistique ;
- Ouvrir la table des attributs ;
- Mesurer une longueur, une aire, le relèvement, un angle ;
- Afficher les infobulles ;
- Actions.

Le menu **Vue -> Décorations** propose en complément d'ajouter une grille, une barre d'échelle, une image, une flèche du Nord et une étiquette de copyright sur la carte.

## Sélection graphique des entités

**Sélectionner des entités** consiste à les « marquer » pour réaliser ensuite des opérations sur cette sélection (affichage attributaire, zoom, export, modification, etc.). Les entités sélectionnées apparaissent en jaune sur la carte (couleur modifiable dans les préférences).

Le sous-menu de l'outil de sélection propose quatre modes :

| Mode | Principe |
|---|---|
| Sélectionner des entités (clic simple ou rectangle) | Clic sur un objet, ou glisser-lâcher pour un rectangle |
| Sélectionner des entités avec un polygone | Clic à chaque sommet, clic droit pour terminer |
| Sélectionner des entités à main levée | Glisser-lâcher en dessinant une forme libre |
| Sélectionner des entités selon un rayon | Glisser-lâcher pour définir un cercle |

> [!warning] Attention
> Tous les objets intersectés par la zone de sélection sont sélectionnés, même partiellement.

L'utilisation combinée avec les touches du clavier permet d'affiner le mode de sélection :

- **Maintien de `Shift`** = ajouter à la sélection ;
- **Maintien de `Ctrl`** = soustraire de la sélection ;
- **Maintien de `Ctrl + Shift`** = sélectionne l'intersection entre la sélection précédente et la sélection courante ;
- **Maintien de `Alt`** (combinable avec `Shift`/`Ctrl`) = sélectionne uniquement les éléments entièrement contenus dans la surface dessinée ;
- Pour les sélections en un seul clic, maintenir `Shift` ou `Ctrl` bascule la sélection de l'entité cliquée (ajout ou retrait).

Pour désélectionner, le bouton **Désélectionner toutes les entités** (`Ctrl+Alt+A`) efface la sélection courante ; sa flèche déroulante propose aussi de ne désélectionner que la couche courante (`Ctrl+Maj+A`). Le bouton voisin permet de **sélectionner toutes les entités** ou d'**inverser la sélection des entités**.

## Voir les données des couches

### Identifier les entités

La commande **Identifier les entités** (bouton dédié ou `Ctrl+Maj+I`) permet d'obtenir, en cliquant sur un objet de la carte, les informations contenues dans ses données attributaires. Le panneau **Résultats de l'identification** liste alors, pour l'entité concernée, chaque champ et sa valeur, ainsi qu'une section **(Dérivé)** donnant des informations géométriques calculées (coordonnées du point cliqué, longueur, périmètre ou surface selon la nature de l'objet).

Le mode d'identification (bouton en bas du panneau) peut être réglé sur :

1. **Couche courante** (celle sélectionnée dans le gestionnaire de couches) ;
2. **De haut en bas, s'arrêter à la première** entité trouvée sur la première couche activée (même non sélectionnée) ;
3. **De haut en bas** sur toutes les couches actives ;
4. **Choix de la couche** : un choix est proposé à chaque clic.

Pour les **couches raster** (qui n'ont pas de données attributaires), la commande donne la valeur du pixel cliqué pour chacune des bandes de l'image.

> [!info] Informations dérivées
> Les mesures dérivées peuvent être calculées selon un système cartésien ou ellipsoïdal (WGS 84, RGF 93…). Les mesures ellipsoïdales sont plus susceptibles de refléter la réalité du terrain. Il est possible de masquer ces données dérivées via l'outil de paramétrage (icône clé).

### Afficher la table d'attributs

La table d'attributs est accessible par le menu **Couche -> Ouvrir la table d'attributs**, le bouton correspondant dans la barre d'outils Attributs, ou un clic droit sur la couche. Elle affiche un tableau où chaque **ligne = une entité** et chaque **colonne = un attribut (champ)**. Elle peut aussi s'afficher en mode **formulaire**, où les entités sont listées à gauche (avec le champ de tri au choix) et le détail d'une entité affiché à droite.

Le bouton de filtre en bas à gauche de la table propose plusieurs modes d'affichage des entités :

- **Montrer toutes les entités** (comportement par défaut) ;
- **Ne montrer que les entités sélectionnées** (nécessite une sélection préalable) ;
- **Ne montrer que les entités visibles sur la carte** : très pratique pour limiter l'affichage à la zone affichée à l'écran ;
- **Montrer les entités nouvelles ou éditées** ;
- **Filtre de champ** : on choisit une colonne (l'attribut), puis on saisit la chaîne de caractères à rechercher pour cet attribut ;
- **Filtre avancé (expression)** : version plus complète utilisant la calculatrice d'expression (voir le module 7 « Requêtes et sélections ») ;
- **Expressions de filtre stockées**.

Le **filtre de champ** recherche la chaîne saisie dans l'ensemble des valeurs de la colonne choisie. Une recherche sur `Revêtu` renverra par exemple aussi `Non revêtu` si la case **sensible à la casse** n'est pas cochée. Deux caractères joker sont disponibles :

- `%` remplace un nombre quelconque de caractères (`D%2` renvoie `D323`, `D12`, `D102`, `D102bis`…) ;
- `_` remplace un seul caractère (`D_2` renvoie `D323` ou `D12`).

Plusieurs raccourcis d'ouverture existent également : **Ouvrir la table d'attributs** (`F6`), **entités sélectionnées** (`Maj+F6`), **entités visibles** (`Ctrl+F6`), **entités éditées et nouvelles**.

> [!warning] Ne pas confondre filtre et sélection
> Le filtre de la table d'attributs n'agit que sur l'affichage de la table et ne modifie pas le nombre d'entités affichées sur la carte. Les entités filtrées ne sont pas sélectionnées automatiquement : il faut cliquer dessus dans la table (ou `Ctrl+A` / le bouton « sélectionner tout ») pour les sélectionner. Le nombre d'entités totales, filtrées et sélectionnées apparaît dans le titre de la fenêtre de la table.

Un clic droit sur l'entête d'une colonne permet de masquer une colonne, de définir sa largeur, de la redimensionner automatiquement (**taille automatique**), de trier selon une expression (**Tri…**) ou de réorganiser l'ordre et la visibilité des colonnes (**Organiser les colonnes…**). Il est aussi possible de définir des règles de **mise en forme conditionnelle** (par exemple colorer en vert les communes de plus de 1000 habitants).

### Modification des attributs d'une couche

Le bouton **Basculer le mode d'édition** (icône crayon) permet de passer une couche en mode édition, ce qui active les outils suivants dans la table d'attributs : sauvegarder les modifications, ajouter une entité, couper/coller les entités sélectionnées, supprimer les entités sélectionnées, **supprimer un champ**, **ajouter un champ** et **ouvrir la calculatrice de champ**.

**Ajouter un champ** : dans la boîte de dialogue « Ajouter une colonne », on saisit le nom du champ, un commentaire éventuel, son type (nombre entier, nombre décimal, texte…), sa longueur et sa précision, puis on valide. Le nouveau champ est initialisé à `NULL` pour toutes les entités.

**Supprimer un champ** : on sélectionne le ou les champs à supprimer dans la boîte de dialogue **Supprimer les champs**, puis on valide.

**Calculatrice de champ** : elle permet de créer un nouveau champ calculé ou de mettre à jour un champ existant, en s'appuyant sur les valeurs d'autres attributs ou sur des fonctions prédéfinies (opérateurs mathématiques et logiques, expressions conditionnelles, fonctions de date, de chaîne de caractères, de géométrie…). La boîte de dialogue comprend une zone de choix (nouveau champ / champ existant), la liste des fonctions disponibles, une aide contextuelle, une barre d'outils d'opérateurs et la zone de saisie de l'expression.

Exemple concret : pour calculer la densité de population d'une commune (habitants au km²) à partir des champs `POPUL` (population) et `SUPERFICIE` (exprimée en hectares), on crée un champ `DENSITE` (réel, longueur 10, précision 2) avec l'expression :

```
"POPUL" / "SUPERFICIE" * 100
```

(le facteur 100 convertit le rapport population/hectares en habitants par km², puisqu'il y a 100 hectares dans un km²).

> [!warning] Sauvegarder les modifications
> Après un ajout ou un calcul de champ, il faut quitter le mode d'édition (et sauvegarder) pour que l'affichage se mette réellement à jour ; fermer puis rouvrir la table d'attributs peut être nécessaire. Il est conseillé de sauvegarder les modifications à chaque étape (ajout de colonne, calcul, suppression).

## Outils généraux

### Outils de mesures

La barre d'outils Mesure (menu **Vue -> Mesure**, ou bouton dédié dans la barre Attributs) propose :

- **Mesurer une longueur** (`Ctrl+Maj+M`) : on peut enchaîner plusieurs segments et terminer par un clic droit ;
- **Mesurer une aire** (`Ctrl+Maj+J`) : clic droit pour terminer le polygone ;
- **Mesure de relèvement** : mesure un angle par rapport au Nord géographique ;
- **Mesurer un angle** : le sommet de l'angle doit être cliqué en deuxième position ; le résultat est signé (positif dans le sens des aiguilles d'une montre).

Les unités préférées (longueur, angle) et la précision se règlent dans **Préférences / Options / Outils cartographiques**.

Pour une plus grande précision, il est recommandé d'activer le mode **accrochage d'objets** (menu Projet/options d'accrochage, ou barre d'outils Accrochage), qui positionne le clic de la souris exactement sur le sommet ou le segment le plus proche, avec une tolérance réglable (en pixels ou en unités de carte). Il est également utile de représenter les sommets des lignes/polygones par un marqueur (style « ligne de symboles », marqueur sur chaque sommet) pour mieux viser les points à accrocher.

> [!warning] Mesure suivant un ellipsoïde
> Aucune projection plane ne conserve exactement les distances terrain. QGIS peut calculer les mesures selon un ellipsoïde (GRS 1980 ou WGS 84 par exemple) plutôt qu'en distance cartésienne projetée : ce réglage se fait dans **Projet -> Propriétés du projet -> onglet Général**, et l'état du calcul (ellipsoïdal ou non) est rappelé dans la boîte de dialogue de mesure.

### Infobulles, signets, annotations

**Infobulles** : le bouton **Infobulles** de la barre d'outils Attributs active ou désactive l'affichage d'une bulle d'information lorsque le curseur survole un objet de la couche active, dans le champ d'affichage défini dans l'onglet **Infobulles** des propriétés de la couche.

**Signets spatiaux** : un signet enregistre la position géographique et le niveau de zoom de la carte à un instant donné, pour pouvoir y retourner facilement. On les gère via le menu **Vue** (`Nouveau signet spatial` = `Ctrl+B`, `Afficher les signets spatiaux` = `Ctrl+Maj+B`, `Gestionnaire de Signets Spatiaux`) ou depuis l'explorateur (dossiers `Signets du projet` et `Signets utilisateurs`). Un signet peut être enregistré dans le projet ou au niveau utilisateur (disponible dans toutes les sessions). L'éditeur de signet permet de nommer le signet, de lui affecter un groupe, et de définir son emprise (calculée depuis la couche, l'étendue actuelle du canevas, ou dessinée à la main).

**Annotations** : la barre d'outils dédiée permet de saisir :

- du **texte simple** (annotation de texte, éditable en double-cliquant dans la bulle) ;
- un **formulaire d'annotation** ;
- du **HTML** (fichier au format HTML) ;
- une **image SVG**.

Chaque annotation est composée d'un **marqueur** (le point ancré sur la carte) et d'une **bulle d'information** (le texte, déplaçable indépendamment). Pour déplacer ou supprimer une annotation, il faut la sélectionner avec l'outil annotation puis cliquer-glisser le marqueur ou la bulle, ou appuyer sur `Suppr` pour l'effacer.

Les **couches d'annotations** permettent, plus globalement, d'ajouter des éléments libres (marqueur, ligne, polygone, texte) sur une couche dédiée ; cette fonctionnalité est approfondie dans le chapitre sur la numérisation des données.

### Décorations de la carte

Le menu **Vue -> Décorations** permet d'ajouter à la carte :

- une **grille** (lignes ou marqueurs, avec ou sans affichage des valeurs de coordonnées) ;
- une **échelle graphique** (barre d'échelle) ;
- une **image** ;
- une **flèche du Nord** (orientation manuelle ou alignement automatique) ;
- une **étiquette de titre** ;
- une **étiquette de copyright** ;
- les **emprises des mises en page** (pour visualiser où se situeront les mises en page réalisées avec le composeur).

> [!warning] Décorations et mises en page
> Ces décorations n'appartiennent pas réellement au canevas de carte : elles n'apparaîtront pas dans une mise en page réalisée avec le composeur (module 6), mais subsistent si l'on exporte la carte en image ou en PDF depuis le menu **Projet -> Importer/exporter**. Pour une mise en page définitive (légende, échelle, flèche du Nord…), ces éléments devront être intégrés directement dans le composeur.

### Barre de localisation

La **barre de localisation** (widget de recherche rapide, accessible en bas à gauche de la barre d'état ou via `Ctrl+K`) permet d'effectuer des recherches rapides dans QGIS sans passer par les menus. Par défaut, elle recherche parmi :

- les **couches du projet** ;
- les **mises en page du projet** ;
- les **actions** ;
- les **entités par attributs** (recherche les attributs de la couche active et zoome sur l'entité correspondante) ;
- les **calculs** (évalue une expression) ;
- les **signets spatiaux** ;
- les **paramètres de QGIS** ;
- les **algorithmes de traitements** ;
- le **géocodeur Nominatim** (recherche par adresse).

On peut restreindre la recherche à l'une de ces catégories en tapant un **préfixe** (ex. `f ` pour rechercher dans les entités par attributs). Des extensions (plugins) permettent d'étendre la liste des filtres disponibles, par exemple pour rechercher des adresses ou des parcelles françaises (extension « Localiser parcelle adresse (BAN) »). La configuration des préfixes se fait dans **Préférences -> Options -> Localisateur**.

## Paramétrage de QGIS pour la navigation et les outils de base

Dans **Préférences / Options / Outils cartographiques**, il est possible de régler :

- l'**outil de mesure** : unités utilisées et précision (nombre de décimales) ;
- le **panoramique et zoom** (navigateur de carte) : action de la molette de la souris et facteur de zoom pour les outils zoom + / zoom - ;
- les **échelles prédéfinies** : gère la liste des échelles proposées dans la liste déroulante de la barre d'état.

> [!tip] À retenir
> La navigation dans QGIS repose sur la barre d'outils Navigation Cartographique (déplacement, zoom, vues multiples) et la barre Attributs (identification, table d'attributs, mesures). La sélection graphique offre quatre modes combinables avec `Shift`/`Ctrl`/`Alt`, et la table d'attributs permet de consulter, filtrer et modifier les données ; toute modification de structure ou de valeur nécessite d'activer le mode édition et de sauvegarder.

> [!question]- Exercice : le navigateur de cartes
> Ouvrir les couches `COMMUNE.SHP` et un SCAN 100. Créer une nouvelle vue cartographique renommée « Sélection SCAN », synchronisée avec la sélection sur la couche COMMUNE, et configurer un réglage de visibilité affichant le SCAN 100 au-dessus de COMMUNE dans cette vue.
>
> **Corrigé** : ajouter les deux couches (`Ajouter une couche vecteur` / `Ajouter une couche raster`), déplacer le SCAN 100 au-dessus de COMMUNE dans le gestionnaire de couches et créer un thème « SCAN 100 » (bouton œil). Ouvrir une nouvelle vue cartographique (`Ctrl+M`), la renommer et cocher « Synchroniser la vue sur la sélection », puis activer le thème « SCAN 100 » dans cette vue. En sélectionnant des communes dans la vue principale, la nouvelle vue zoome automatiquement sur la sélection en affichant le SCAN par-dessus.

> [!question]- Exercice : sélections graphiques
> Sur la couche `COMMUNE.SHP`, tester successivement : sélectionner une commune avec l'outil « une seule entité », sélectionner toutes les communes avec l'outil rectangle, sélectionner quelques communes avec l'outil polygone, à main levée, et selon un rayon.
>
> **Corrigé** : utiliser la flèche du sous-menu de l'outil de sélection pour changer de mode entre chaque manipulation ; pour le rectangle et le polygone, encadrer les entités avec un cliquer-glisser (rectangle/main levée/rayon) ou une succession de clics terminée par un clic droit (polygone).

> [!question]- Exercice : table d'attributs
> Ouvrir `COMMUNE.SHP` et `TRONCON_ROUTE.SHP`. À l'aide du filtre sur la table attributaire, rechercher : la sous-préfecture, les communes du canton de « LA FLECHE », les routes à 3 voies, et les routes départementales D102 et D102bis.
>
> **Corrigé** : ouvrir la table d'attributs de la couche concernée, choisir « Filtre de champs », sélectionner l'attribut (`STATUT`, `CANTON`, `NB_VOIES`, `NUM_ROUTE`), saisir la chaîne recherchée (attention à la casse), cliquer sur Appliquer, puis sélectionner les lignes trouvées (clic ou « sélectionner tout ») et zoomer sur la sélection.

> [!question]- Exercice : infobulle, signet, annotation
> Ouvrir `COMMUNE.SHP` et `CHEF_LIEU.SHP`. Activer les infobulles sur ces deux couches, créer des signets sur chaque chef-lieu avec zoom, puis annoter les villes de la couche CHEF_LIEU.
>
> **Corrigé** : vérifier le champ d'affichage (onglet Affichage des propriétés de couche, choisir NOM), activer l'infobulle (bouton dédié) et survoler les objets ; créer un nouveau signet spatial pour chaque commune via l'explorateur ou le gestionnaire de signets ; utiliser l'outil « Annotation de texte », cliquer sur la ville puis double-cliquer dans la bulle pour saisir le nom.
