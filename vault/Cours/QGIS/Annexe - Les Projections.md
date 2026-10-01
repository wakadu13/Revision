---
tags: [qgis, sig, geodesie]
---
# Les Projections
Retour : [[00 - Sommaire QGIS]]

Pour afficher la Terre — qui est une surface courbe — sur un écran ou une carte papier plane, il faut passer par une opération mathématique appelée projection cartographique. Ce choix conditionne directement la précision des mesures (distances, surfaces, angles) que l'on peut faire dans QGIS, d'où l'importance de bien comprendre ce que chaque projection déforme et ce qu'elle préserve.

## Définition

La projection cartographique est un ensemble de techniques géodésiques permettant de représenter une surface non plane, comme la surface de la Terre, dans son ensemble ou en partie, sur la surface plane d'une carte.

Concrètement, on part d'un modèle mathématique de la Terre (l'ellipsoïde, voir [[Annexe - Géodésie]]) et on « déplie » ce volume sur un plan à l'aide d'une formule mathématique. Toute projection déforme obligatoirement la réalité sur au moins un aspect : les angles, les surfaces, les distances ou les directions.

## Classification suivant les déformations locales

On distingue les projections selon ce qu'elles conservent :

- Les projections qui conservent les angles localement sont dites **conformes** (*conformal*). Elles préservent la forme des petits objets et sont indispensables pour la navigation ou les usages militaires — seules les projections conformes sont utilisées par les armées.
- Les projections qui conservent les surfaces sont dites **équivalentes** (*equal-area*). Elles sont utiles pour comparer des superficies (ex. statistiques, occupation du sol) mais déforment les formes.
- Il existe aussi des projections **équidistantes**, qui conservent les distances le long de certaines lignes particulières (souvent un méridien ou un parallèle de référence), sans être ni conformes ni équivalentes.

Le type de projection adopté dépend donc toujours du but recherché : navigation, cadastre, statistiques, cartographie topographique, etc. Dans tous les cas, les déformations deviennent plus importantes à mesure que l'on s'éloigne du point ou de la ligne de tangence entre l'ellipsoïde et la surface de projection.

Pour visualiser ces déformations, on utilise une méthode graphique appelée **indicatrice de Tissot** (inventée par le cartographe Nicolas Auguste Tissot) : on projette une série de petits cercles identiques répartis sur le globe, et on observe comment ils se déforment une fois projetés.

- Sur une projection Mercator (conforme), les cercles restent des cercles mais leur taille grandit fortement en s'éloignant de l'équateur (étirement Nord-Sud).
- Sur une projection de Peters (équivalente), les cercles deviennent des ellipses très allongées mais conservent tous la même surface.

> [!example] Indicatrice de Tissot
> Plus les ellipses de déformation sont grandes ou allongées à un endroit du globe, plus la projection y déforme fortement la réalité. Un point où l'ellipse reste un cercle parfait est un point où la projection est localement exacte (point ou ligne de tangence).

## Les principaux types de projection

Les projections se classent aussi selon la surface géométrique développable utilisée pour « recevoir » la projection de l'ellipsoïde. Il en existe trois grandes familles.

### La projection cylindrique

Les projections cylindriques consistent à projeter l'ellipsoïde sur une surface développable de forme cylindrique. On distingue plusieurs orientations (*aspects*) du cylindre par rapport à l'axe de la Terre :

- **directe** : l'axe du cylindre est confondu avec l'axe des pôles ;
- **transverse** : l'axe du cylindre est perpendiculaire à l'axe des pôles, dans le plan de l'équateur ;
- **oblique** : orientation intermédiaire quelconque.

**La projection de Mercator** est une projection cylindrique tangente d'aspect direct et conforme. Elle conserve les longueurs autour de l'équateur (ligne de tangence), mais occasionne des altérations de plus en plus importantes des longueurs lorsqu'on s'en éloigne vers les pôles. Parallèles et méridiens s'y coupent toujours à angle droit, ce qui en fait une projection historiquement précieuse pour la navigation maritime (un cap constant y est une ligne droite).

**La projection Mercator transverse** est une projection cylindrique transverse, également conforme. Le méridien de tangence et l'équateur s'y présentent sous forme de droites perpendiculaires, alors que les autres méridiens se présentent sous forme d'arcs de cercle concourant aux pôles. Les distances sont conservées le long du méridien de tangence. C'est le principe utilisé par le système `UTM` (*Universal Transverse Mercator*), qui découpe le globe en 60 fuseaux de 6° de longitude, chacun avec son propre méridien central de tangence, afin de limiter les déformations.

### La projection conique

Il existe plusieurs types de projections coniques, les plus couramment utilisées étant la projection conique tangente et la projection conique sécante.

**La projection conique tangente conforme** : le cône développé se présente sous une forme circulaire, de manière à être tangent au parallèle central de la zone à cartographier (le **parallèle de tangence**). Les méridiens y sont des droites concourantes au sommet du cône, et les parallèles des arcs de cercle concentriques. Les distances sont conservées le long du parallèle de tangence.

**La projection conique sécante conforme** procède de la même manière, à la différence qu'il n'y a plus un seul parallèle tangent mais deux parallèles sécants : le cône est légèrement sécant à l'ellipsoïde entre ces deux parallèles. Les distances sont conservées le long des deux parallèles sécants, ce qui répartit mieux les déformations sur toute la zone cartographiée. C'est le principe utilisé par les projections **Lambert** en France (voir plus bas).

### La projection azimutale

Ce sont des projections particulières, dans lesquelles on projette l'ellipsoïde directement sur un plan tangent en un point (souvent un pôle) ou sécant selon un cercle. C'est dans cette classe que l'on rencontre les projections dites vraies (centrales ou orthogonales), bien adaptées à la cartographie des zones polaires ou circulaires autour d'un point central.

> [!info] Retenir la logique
> Cylindrique → zones étirées en longitude (planisphères, fuseaux UTM) · Conique → zones aux latitudes moyennes, étendues en longitude (France, Europe) · Azimutale → zones circulaires autour d'un point (pôles).

## Les systèmes usuels en France

En pratique, dans QGIS, l'utilisateur manipule surtout quelques systèmes de référence normalisés :

| Système | Type | Usage |
|---|---|---|
| `WGS84` (EPSG:4326) | Coordonnées géographiques (lat/lon) | Référence mondiale, GPS |
| `RGF93` | Système géodésique national | Référence officielle en France métropolitaine |
| `Lambert 93` (EPSG:2154) | Projection conique conforme sécante | Projection officielle française (cartographie, cadastre, IGN) |
| `UTM` | Projection cylindrique transverse conforme, par fuseaux | Cartographie internationale, imagerie satellite |

Le **Lambert 93** s'appuie sur le système géodésique **RGF93** et utilise une projection conique conforme sécante centrée sur la France métropolitaine : c'est la projection réglementaire pour les données géographiques officielles françaises, et le système par défaut recommandé dans QGIS pour tout travail cartographique national.

> [!warning] Piège fréquent
> Ne pas confondre un **système géodésique** (ex. RGF93, WGS84 — qui définit l'ellipsoïde et le datum, en coordonnées géographiques) et une **projection** (ex. Lambert 93, UTM — qui convertit ces coordonnées géographiques en coordonnées planes X,Y en mètres). Dans QGIS, le SCR (Système de Coordonnées de Référence) choisi combine toujours les deux.

> [!tip] À retenir
> Toute projection déforme la Terre : on choisit une projection **conforme** (angles), **équivalente** (surfaces) ou **équidistante** (distances) selon l'usage, et une famille géométrique — cylindrique, conique ou azimutale — selon la zone à représenter. En France, le couple RGF93 / Lambert 93 est la référence officielle à privilégier dans QGIS.
