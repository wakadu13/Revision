---
tags: [qgis, sig]
---
# Introduction à QGIS
Retour : [[00 - Sommaire QGIS]] · Suite : [[02 - Ouverture et Visualisation]]

Ce premier chapitre pose les bases indispensables avant de manipuler QGIS : quelques rappels sur les systèmes d'information géographique (SIG), une présentation du logiciel lui-même, puis une visite guidée de son interface et de ses paramètres de base.

## Rappels sur les SIG

### Qu'est-ce qu'un SIG ?

Un système d'information géographique (SIG) est un système d'information capable d'organiser et de présenter des données alphanumériques spatialement référencées, ainsi que de produire des plans et des cartes. Le terme désigne à la fois les outils logiciels, les données, le matériel et le savoir-faire liés à leur utilisation.

Les principales fonctionnalités d'un SIG sont :

- l'affichage ou la production de cartes ;
- l'analyse des données pour créer une nouvelle information ;
- l'acquisition des données ;
- l'abstraction ou la représentation des éléments choisis ;
- l'archivage.

### Les quatre composantes des données géographiques

| Composante | Description |
|---|---|
| Données géométriques | Forme et localisation des objets ou phénomènes |
| Données descriptives (attributaires) | Ensemble des attributs descriptifs des objets |
| Données de style | Paramètres d'affichage des objets (type de trait, couleur…) |
| Métadonnées | Données qui décrivent les données (date d'acquisition, propriétaire, méthode…) |

### Vecteur et raster

Il existe deux grandes familles de données géographiques.

Les données **vectorielles** représentent l'information sous forme de points, de lignes, de polygones (surfaces) ou de multi-polygones. Chaque objet géométrique porte des attributs qui le décrivent (un point pour une école, une ligne pour une route, un polygone pour une commune, par exemple).

Les données **raster** (ou matricielles) sont constituées d'une matrice de points colorés appelés pixels : une image aérienne, un modèle numérique de terrain (MNT), une orthophoto ou un fond scanné (type Scan25) sont des exemples de rasters.

### Superposition des couches et système de coordonnées

Les données d'un SIG sont organisées en **couches**, chacune correspondant à un thème (chef-lieu, route principale, communes, fond de plan…). L'intérêt du SIG est de pouvoir superposer ces couches pour composer une carte.

Pour que la superposition soit cohérente, toutes les couches doivent partager le même **système de coordonnées de référence** (SCR), c'est-à-dire le système géodésique et la projection utilisés pour positionner les objets les uns par rapport aux autres. En France métropolitaine, la projection officielle est le **Lambert 93** (code `EPSG:2154`), rattachée au système géodésique **RGF93**. QGIS utilise le sigle **SCR** pour désigner ce système de coordonnées de référence.

> [!tip] À retenir
> Un SIG combine des données géométriques, attributaires, de style et des métadonnées, organisées en couches vecteur ou raster, qui doivent toutes partager le même système de coordonnées de référence (en France, le Lambert 93 / EPSG:2154) pour se superposer correctement.

## Présentation de QGIS

### Un logiciel libre et complet

QGIS est un logiciel « open source » (code source libre), élaboré par une communauté internationale de développeurs et destiné au traitement des données géographiques. Il fonctionne sous Windows, Mac, Linux, BSD et Android, et permet de créer, éditer, visualiser, analyser et publier des informations géographiques.

### QGIS dans les ministères

La présente formation fait partie du plan d'accompagnement mis en place par les ministères. Elle a été élaborée en partenariat avec l'ENSG (École nationale des sciences géographiques de l'IGN) et est diffusable sous les termes de la licence ouverte ETALAB.

> [!warning] Avant de commencer
> Il est important de vérifier que le poste de travail dispose bien de la version de QGIS sur laquelle est basée la formation. La formation peut être suivie avec des versions ultérieures, mais certaines commandes peuvent avoir changé et certaines copies d'écran peuvent ne plus correspondre exactement aux nouvelles versions du logiciel.

## Interface de QGIS

L'interface de QGIS affiche de manière standard :

- la **barre des menus**, en haut de l'écran ;
- les **barres d'outils**, contenant des outils regroupés par famille de fonctionnalités (chaque barre d'outils peut être déplacée selon les besoins) ;
- différentes **fenêtres** : carte, aperçu, explorateur et gestionnaire de couches ;
- une **barre d'état**, en bas de l'écran, donnant un certain nombre d'informations relatives à l'affichage de la carte et au projet en cours : coordonnées du curseur, système de coordonnées, échelle, etc. ;
- la **barre de localisation**, en bas à gauche, qui permet d'effectuer des recherches rapides d'algorithmes, d'actions, de couches, et de localiser une entité dans la couche active.

Un clic droit avec la souris sur une barre d'outils fait apparaître la liste des fenêtres et des barres d'outils disponibles, ce qui permet de personnaliser l'interface selon ses besoins.

### La fenêtre « couches » (gestionnaire de couches)

La fenêtre « couches » liste les couches présentes dans la carte. Elle permet de :

- définir la **visibilité** ou non de chaque couche (case à cocher devant le nom) ;
- modifier l'**ordre d'empilement** des couches (cliquer-déplacer le nom de la couche) ;
- accéder aux **propriétés** de la couche (double-clic sur le nom de la couche, ou clic droit -> Propriétés) ;
- **décharger** une couche.

Par défaut, un double-clic sur le nom de la couche permet d'accéder à ses propriétés.

### La fenêtre « carte »

Cette fenêtre (aussi appelée canevas) sert à :

- afficher les couches listées dans la fenêtre « couches », de type raster ou vecteur ;
- effectuer des zooms avant/arrière pour modifier l'emprise de la carte ;
- déplacer la carte pour porter le focus sur une zone ;
- effectuer des opérations sur les objets comme les sélections, les mesures, l'affichage d'information, etc.

En plaçant le curseur sur la carte :

- on peut zoomer avec la molette de la souris ;
- on peut se déplacer avec les flèches du clavier, ou en maintenant la touche **espace** appuyée tout en bougeant la souris.

À l'aide de `CTRL+TAB`, on peut basculer la visibilité des panneaux ouverts dans la fenêtre principale, de sorte que seule la fenêtre carte reste visible.

> [!note] Remarque
> La fenêtre carte et le gestionnaire de couches sont étroitement liés : toute modification apportée au style d'une couche est immédiatement visible sur la carte.

### La fenêtre « données attributaires »

La table d'attributs affiche les données alphanumériques des entités de la couche vectorielle sélectionnée dans la fenêtre « couches ». Chaque ligne correspond à une entité, ses attributs étant distribués en colonnes.

Cette fenêtre, ouverte par la commande « Ouvrir la table d'attributs », permet de :

- visualiser sous forme de tableau les données attributaires de la couche vectorielle ;
- sélectionner des enregistrements dans la table ;
- effectuer des opérations sur la sélection (afficher, zoomer, supprimer…) ;
- effectuer des opérations sur la table (gestion des colonnes…) ;
- modifier les valeurs des données attributaires.

On peut modifier l'ordre d'affichage des enregistrements en cliquant sur l'en-tête d'une colonne : une petite flèche indique le sens du tri (vers le bas = tri décroissant, vers le haut = tri croissant).

## Paramétrages de base

### Accéder aux options

Les options de base du logiciel sont accessibles via le menu `Préférences > Options`.

> [!warning] Attention
> Les différents menus de configuration font appel à des connaissances spécifiques (réseau, géomatique, informatique…). Il est vivement conseillé de se rapprocher du responsable informatique et du responsable ADL (Administrateur de Domaine Local) avant de modifier les différentes options.

### Principaux onglets du menu Options

Le menu Options comporte de nombreux onglets, parmi lesquels :

| Onglet | Rôle |
|---|---|
| Général | Configuration de la fenêtre applicative et options par défaut des fichiers projet |
| Système | Chemins vers des ressources complémentaires (SVG, extensions C++) et variables d'environnement |
| User Profiles | Définit les profils utilisateurs |
| SCR et Transformations | Système de coordonnées de référence par défaut pour les nouveaux projets et couches, gestion des transformations entre systèmes géodésiques |
| Source de données | Comportement des tables attributaires, gestion des chemins masqués dans l'explorateur |
| Rendu | Comportement et qualité du rendu des couches vectorielles, coloration des rasters, couleur des objets sélectionnés |
| Couleurs | Gestionnaire des couleurs standard |
| Canevas et légende | Apparence par défaut de la carte et style des objets de la légende |
| Outils cartographiques | Mode d'identification des couches, outils de mesure, fonction zoom, échelles prédéfinies, paramètres de numérisation |
| GDAL | Options des pilotes GDAL (formats raster), options des pyramides |
| Réseau | Paramètres généraux du réseau, du cache réseau et du proxy pour l'accès Internet |
| GPS | Connexions et propriétés des appareils GPS |
| Localisateur | Configuration de la barre de localisation et des filtres de recherche |
| Traitement | Paramètres généraux des outils de l'extension Processing |

### Bien paramétrer le SCR pour la France métropolitaine

Deux réglages de l'onglet **SCR et Transformations** sont particulièrement importants pour bien débuter :

- **SCR pour les projets** : la projection par défaut des nouveaux projets doit être fixée avec le SCR courant de la zone d'activité. En France métropolitaine, le code SCR légal est le **RGF93 / Lambert-93 (EPSG:2154)**.
- **SCR pour les nouvelles couches** : on peut demander à QGIS de proposer systématiquement le choix du SCR à l'utilisateur (option « Demander le SCR »), ou de laisser QGIS utiliser celui du projet ou celui affiché dans la source de la donnée.

Concernant les **transformations de coordonnées**, QGIS utilise une table système de transformation pour améliorer la précision lors des reprojections de couches. En France, une grille de transformation est utile pour convertir entre le Lambert II (ancienne projection, aujourd'hui obsolète) et le Lambert 93 : dans ce cas, il est conseillé d'utiliser les codes **IGNF** pour la couche avec l'ancienne projection, car l'utilisation de la grille de conversion sera alors implicite.

Il est également possible de définir un **SCR personnalisé** (défini par l'utilisateur), à condition de fournir une définition conforme au format de chaîne WKT ou Proj.

### Le paramétrage réseau (proxy)

Les paramètres réseau (onglet **Réseau**) ne doivent être modifiés qu'en coordination avec le correspondant informatique. On y trouve notamment :

- les **paramètres du cache** (taille, avec un bouton « Effacer le cache » utile pour régénérer l'affichage de pages issues du web) ;
- l'utilisation d'un **serveur proxy**, qui joue le rôle d'intermédiaire entre les ordinateurs d'un réseau, notamment pour la sécurité, le filtrage et l'optimisation de la navigation (cache mémoire).

Le paramétrage d'un proxy nécessite de renseigner l'adresse du serveur (hôte, port) et éventuellement une authentification (utilisateur/mot de passe, qui peuvent être cryptés dans la base de données d'authentification de QGIS), ainsi que le type de proxy accepté sur le poste client (par exemple `defaultproxy` pour utiliser le proxy défini au niveau du système). Il est également possible d'exclure certaines adresses (par exemple les serveurs intranet) du relais par le proxy.

> [!note] Serveurs proxy du ministère en charge de l'écologie
> Pour l'adresse du serveur proxy, il convient de se rapprocher de la cellule informatique du service pour utiliser le serveur proxy du service (vivement conseillé). Par défaut, le type de proxy `defaultproxy` est recommandé.

> [!tip] À retenir
> Les paramètres de base à vérifier en priorité au démarrage d'une installation QGIS sont le proxy réseau (menu `Préférences > Options > Réseau`) et le système de coordonnées de référence par défaut (menu `Préférences > Options > SCR et Transformations`), en retenant RGF93 / Lambert-93 (EPSG:2154) pour la France métropolitaine.

> [!question]- Exercice : interface QGIS
> **Objectif** : vérifier les principaux paramètres du logiciel QGIS (réseau et système de coordonnées de référence).
>
> Ouvrir QGIS et définir le paramétrage du proxy et du système de coordonnées de référence :
> 1. Définir les paramètres du proxy local (voir le responsable informatique si besoin) ;
> 2. Sélectionner la projection pour les nouveaux projets : **RGF93 / Lambert-93 EPSG:2154** ;
> 3. Sélectionner la projection pour les nouvelles couches : « Demander le SCR ».
>
> Indice : ces réglages sont accessibles via `Préférences > Options`.
>
> **Corrigé**
> Définir le paramétrage du proxy avec la commande `Préférences > Options > Réseau` :
> - renseigner l'hôte et le port du proxy (voir la remarque sur les serveurs proxy du ministère) ;
> - spécifier le type de proxy : `defaultproxy`.
>
> Définir le système de coordonnées de référence avec la commande `Préférences > Options > SCR et Transformations` :
> - sélectionner **RGF93/Lambert93 – EPSG:2154** pour les nouveaux projets ;
> - activer « Demander le SCR » pour les nouvelles couches.
