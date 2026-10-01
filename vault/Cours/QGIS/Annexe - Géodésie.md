---
tags: [qgis, sig, geodesie]
---
# Géodésie
Retour : [[00 - Sommaire QGIS]]

La géodésie est la science qui définit la forme réelle de la Terre et sert de fondation à tout système de coordonnées. Comprendre ses notions de base (ellipsoïde, géoïde, datum) permet de savoir pourquoi un SIG comme QGIS demande toujours de choisir un système de coordonnées de référence (SCR) avant de travailler, et d'éviter les décalages de plusieurs mètres entre des données mal référencées.

## Qu'est-ce que la géodésie ?

La géodésie est une science ayant pour but de déterminer et représenter :

- la forme de la Terre ;
- les champs de gravitation et de pesanteur de la Terre.

Chaque nation a longtemps développé son propre système géodésique, et il a fallu attendre **1886** et la création de l'Association Internationale de Géodésie (`IAG`, *International Association of Geodesy*) pour voir jetées les bases d'une collaboration géodésique internationale. La géodésie apporte les bases géométriques indispensables à la représentation de la Terre, et donc à toute donnée manipulée dans un SIG.

## Les surfaces de référence qui décrivent la Terre

La forme de la Terre est vue comme une sphère aplatie aux pôles, avec un axe de rotation et un plan de référence, l'équateur. Pour les travaux de géodésie et de topographie, on considère en réalité trois surfaces distinctes, emboîtées les unes dans les autres.

### La surface topographique

C'est la partie supérieure de la croûte terrestre, c'est-à-dire le relief réel tel qu'on le mesure sur le terrain (montagnes, vallées, bâtiments). Sa description fait l'objet de la topographie : la représentation sur un plan des formes du terrain, naturelles ou artificielles. Sur les cartes, elle est symbolisée par les **courbes de niveau**, des lignes reliant les points de même altitude, espacées d'une équidistance constante (par exemple 50 m).

### Le géoïde

La Terre n'est pas une sphère parfaite ni un solide géométrique régulier, mais un **géoïde** : une surface équipotentielle de pesanteur, qui correspond au niveau moyen des mers (en l'absence de marées, courants et vents). La surface moyenne des océans est en effet une surface équipotentielle, c'est-à-dire une surface où le potentiel de gravité est constant en tout point. Le géoïde est donc une surface irrégulière, « bosselée », qui reflète les variations réelles de la gravité terrestre (densité du sous-sol, relief, océans).

Pour pouvoir calculer et modéliser cette surface complexe, on utilise une figure géométrique plus régulière : l'**ellipsoïde**.

### L'ellipsoïde

Les ellipsoïdes permettent de positionner un point et d'en donner les coordonnées à partir de calculs d'angles et de distances. Ils sont destinés à modéliser au mieux une partie ou la totalité du géoïde.

Contrairement à la surface topographique et au géoïde, il n'existe pas un seul ellipsoïde de référence mais plusieurs : chaque ellipsoïde « de référence » est choisi parce qu'il se rapproche au mieux du géoïde à un endroit donné de la Terre (ellipsoïde **local**), ou en moyenne sur l'ensemble du globe (ellipsoïde **global**). Les centres de ces différents ellipsoïdes peuvent être légèrement décalés les uns par rapport aux autres.

Ces trois surfaces (topographique, géoïde, ellipsoïde) ne coïncident jamais parfaitement : elles s'écartent les unes des autres de façon variable selon le lieu. Ce sont les éléments essentiels pour poser les bases du positionnement.

> [!note] Ordres de grandeur
> Les écarts possibles entre la surface topographique et l'ellipsoïde n'excèdent pas 9000 mètres en positif (mont Everest, 8848 m) et 12000 mètres en négatif (fosse Challenger, 11034 m), alors que les écarts entre l'ellipsoïde et le géoïde restent inférieurs à 200 mètres.

## Le système géodésique (datum)

Un système géodésique, ou **datum**, est une modélisation de la Terre afin d'exprimer des coordonnées géographiques. Il est matérialisé par un système de référence et est défini au strict minimum par :

- un repère géodésique (l'ensemble de points connus avec précision qui servent d'ancrage) ;
- un ellipsoïde de référence ;
- un méridien origine (par convention, celui de **Greenwich**).

Quand on choisit un ellipsoïde particulier pour approximer le géoïde, on dit que l'on choisit un ellipsoïde « de référence ». Il existe un grand nombre d'ellipsoïdes potentiellement utilisables, car certains se rapprochent davantage du géoïde à certains endroits de la Terre qu'à d'autres : un même point du globe peut donc avoir des coordonnées légèrement différentes selon le datum utilisé pour le calculer, ce qui explique les décalages observés entre systèmes de coordonnées différents.

> [!warning] Piège fréquent
> Deux jeux de données parfaitement justes mais référencés dans deux datums différents (ex. un ancien système local et le `WGS84`) peuvent apparaître décalés de plusieurs dizaines à plusieurs centaines de mètres une fois superposés dans QGIS, sans qu'il y ait d'erreur de saisie : c'est le système géodésique lui-même qui diffère.

## Les différents systèmes de coordonnées

Un système géodésique permet de positionner des points dans l'espace, à savoir de leur attribuer des coordonnées. On distingue trois façons d'exprimer ces coordonnées, qui s'enchaînent logiquement.

### Les coordonnées cartésiennes

Dans un système géodésique, les coordonnées sont d'abord présentées sous format cartésien, en $X, Y, Z$ :

- l'origine est le centre de la Terre ;
- le plan $XY$ est dans le plan de l'équateur ;
- l'axe $X$ recoupe le méridien d'origine (Greenwich) ;
- l'axe $Z$ est l'axe qui va du centre de la Terre aux pôles.

### Les coordonnées géographiques

En ajoutant un ellipsoïde de référence aux coordonnées cartésiennes, on obtient les **coordonnées géographiques**, exprimées en fonction de la latitude ($\varphi$), de la longitude ($\lambda$) et de l'altitude ($h$). En France, le système géodésique de référence utilisé est le `WGS84` (associé au `RGF93` pour le référentiel national).

Ces unités angulaires (latitude et longitude) peuvent être notées de trois façons :

| Notation | Exemple |
|---|---|
| Degrés, minutes, secondes | $48°36'36''$ |
| Degrés, minutes décimales | $48°36.6'$ |
| Degrés décimaux | $48.61°$ |

### Les coordonnées planes

La conversion de positions géographiques d'une surface courbe vers une surface plane nécessite l'utilisation d'une **projection cartographique** (voir [[Annexe - Les Projections]]). Une fois cette projection définie, la localisation d'un élément peut s'exprimer sous forme de coordonnées planes, à l'aide de deux valeurs linéaires **E (Est)** et **N (Nord)**, exprimées dans différentes unités (mètres, kilomètres, miles nautiques, etc.).

On peut résumer l'enchaînement complet ainsi :

$$\text{Coordonnées cartésiennes } (X, Y, Z) \xrightarrow{+\ \text{ellipsoïde}} \text{Coordonnées géographiques } (\varphi, \lambda, h) \xrightarrow{+\ \text{projection}} \text{Coordonnées planes } (E, N)$$

Dans QGIS, choisir un SCR (système de coordonnées de référence) revient donc toujours à choisir simultanément un datum géodésique (ellipsoïde + repère) et, si l'on travaille en coordonnées planes, une projection cartographique associée.

> [!tip] À retenir
> La Terre se modélise par trois surfaces emboîtées — topographique, géoïde, ellipsoïde — et un système géodésique (datum) associe un ellipsoïde de référence à un repère et un méridien origine pour permettre de calculer des coordonnées. On passe des coordonnées cartésiennes (X, Y, Z) aux coordonnées géographiques (latitude, longitude, hauteur) grâce à l'ellipsoïde, puis aux coordonnées planes (E, N) grâce à une projection.
