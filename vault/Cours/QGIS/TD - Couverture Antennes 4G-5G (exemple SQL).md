---
tags: [qgis, sig, postgis, sql]
---
# TD — Couverture des antennes 2G à 5G en France (exemple QGIS + SQL)
Retour : [[00 - Sommaire QGIS]]

> [!abstract] Présentation
> Étude de cas complète, à titre d'exemple, montrant comment combiner **QGIS** et une base spatiale pilotable en **SQL** (type PostGIS ou SpatiaLite) pour explorer, filtrer et cartographier un jeu de données Open Data volumineux : les antennes mobiles 2G à 5G en France, publiées par l'ANFR.

## Le jeu de données

Les données sont publiées par l'ANFR (Agence Nationale des Fréquences), au format GeoJSON, dans le référentiel géographique **EPSG:4326 (WGS 84)**.

> [!warning] Harmoniser le système de coordonnées
> Si le reste du projet travaille dans un autre référentiel (par exemple **EPSG:3857 - WGS 84 / Pseudo-Mercator**), il faut reprojeter la couche avant de l'exploiter : clic droit sur la couche → **Exporter** → **Enregistrer les entités sous...**, puis choisir le SCR cible dans la liste déroulante (« SCR du projet » convient dans la majorité des cas) et cocher **Ajouter les fichiers sauvegardés à la carte**.

## Nettoyage et allègement de la base

Un jeu de données Open Data brut contient souvent des champs inutiles et peut être très volumineux (plusieurs centaines de Mo). Avant toute analyse :

1. Repérer les champs réellement utiles (ex. identifiant de l'antenne, opérateur, technologie 2G/3G/4G/5G, code postal, coordonnées).
2. Supprimer les champs redondants ou inutiles (doublons d'identifiant, adresses détaillées non nécessaires...).
3. Filtrer par type de donnée (génération, opérateur, région) pour ne travailler que sur le sous-ensemble pertinent à l'étude.

## Filtrage par expression

Le filtre attributaire (clic droit sur la couche → **Filtrer...**) ouvre le **constructeur de requête** : on y compose une expression logique avec les opérateurs `=`, `<`, `>`, `LIKE`, `IN`, `AND`, `OR`, `NOT`, en s'aidant des boutons **Échantillon** et **Toutes** pour lister les valeurs possibles d'un champ.

```sql
"generation" = '5G' AND "sta_nm_dpt" = '059'
```

Les conditions se combinent pour des besoins plus complexes :

```sql
("generation" = '3G' AND "sta_nm_dpt" = '067')
OR
(("generation" = '4G' OR "generation" = '5G') AND "sta_nm_dpt" = '059')
OR
("generation" = '2G' AND "sta_nm_dpt" = '013')
```

> [!tip] Lire le résultat
> Après validation, une boîte de dialogue **« La clause WHERE a retourné N ligne(s) »** confirme le nombre d'entités correspondant au filtre — un bon moyen de vérifier rapidement la cohérence du résultat avec l'ordre de grandeur attendu.

## Séparer les données en tables par requête SQL

Plutôt que de dupliquer des filtres à répétition, une base pilotable en SQL permet d'automatiser la séparation des données (par exemple par opérateur) de façon reproductible :

```sql
-- Supprimer les tables si elles existent
DROP TABLE IF EXISTS "public"."antennes_4g_bouygues";
DROP TABLE IF EXISTS "public"."antennes_5g_bouygues";

-- Recréer les tables avec la structure de la table source
CREATE TABLE "public"."antennes_4g_bouygues" AS
  SELECT * FROM "public"."antennes_4g" WHERE 1=0;
CREATE TABLE "public"."antennes_5g_bouygues" AS
  SELECT * FROM "public"."antennes_5g" WHERE 1=0;

-- Insérer les données correspondantes
INSERT INTO "public"."antennes_4g_bouygues"
  SELECT * FROM "public"."antennes_4g" WHERE "adm_lb_nom" = 'BOUYGUES TELECOM';
INSERT INTO "public"."antennes_5g_bouygues"
  SELECT * FROM "public"."antennes_5g" WHERE "adm_lb_nom" = 'BOUYGUES TELECOM';
```

Un comptage rapide par type de table permet de vérifier la répartition :

```sql
SELECT 'antennes_5g' AS type, COUNT(*) AS count FROM antennes_5g
UNION ALL
SELECT 'antennes_4g' AS type, COUNT(*) AS count FROM antennes_4g;
```

> [!question]- Pourquoi créer des tables plutôt que de filtrer à chaque fois ?
> Une requête SQL enregistrée est **reproductible** : si les données source sont mises à jour, il suffit de rejouer le script pour reconstruire les tables filtrées, alors qu'un filtre attributaire est à refaire manuellement à chaque nouvelle donnée. En contrepartie, pour une opération ponctuelle et unique, l'interface graphique de filtrage reste plus rapide à utiliser.

## Représentation : du nuage de points à la carte de chaleur

Avec un jeu de données de plusieurs dizaines de milliers de points, l'affichage en symboles ponctuels classiques devient vite illisible (points superposés). Deux leviers permettent d'améliorer la lisibilité :

- **Réduire la taille des points** dans les propriétés de symbologie de la couche, pour distinguer les zones de forte et de faible densité en zoomant.
- **Utiliser le rendu « Carte de chaleur »** (Propriétés de la couche → Symbologie → Carte de chaleur) : on règle le **rayon** (en pixels) et la **palette de couleurs**. Ce rendu fait ressortir les zones de concentration, mais reste purement visuel — il ne prend pas en compte la puissance réelle des antennes ni le relief.

> [!warning] Piège de l'empilement de couches
> Lorsque plusieurs cartes de chaleur (une par opérateur, par exemple) sont superposées, seule la couche du dessus reste visible aux endroits où elles se recouvrent : la règle d'affichage suit l'ordre des couches dans le panneau, **pas** l'intensité ou la dominance réelle d'un opérateur. Pour comparer plusieurs opérateurs sur une même carte, il faut donc soit appliquer une transparence identique à toutes les couches, soit changer l'ordre d'empilement selon ce que l'on veut mettre en évidence — dans tous les cas le résultat reste une approximation, pas une mesure de dominance.

## Analyse de proximité : zones de couverture et distance à un point

Pour simuler une zone de couverture réseau, on peut générer un **tampon (buffer)** autour de chaque antenne avec une fonction spatiale de type `ST_Buffer` :

```sql
-- Remplir une table de polygones avec un cercle de 5 km autour de chaque antenne
INSERT INTO couverture_4g_free ("id", "geom", "id_ant")
  SELECT nextval('suite_ids'),
         ST_Buffer(row_antenne.geom, 5000),
         row_antenne.id
  FROM antennes_4g_free AS row_antenne;
```

En appliquant un dégradé de transparence, les zones où plusieurs cercles se chevauchent apparaissent plus foncées — une première approximation visuelle de la densité de couverture.

Pour répondre à une question du type *« de quelles antennes un usager situé à tel endroit bénéficie-t-il ? »*, on combine une jointure spatiale avec un calcul de distance :

```sql
SELECT a.id, a.adm_lb_nom, a.generation,
       FLOOR(ST_Distance(a.geom, ST_Transform(u.geom, 3857))) AS distance_en_metres
FROM antennes_5g AS a,
     (SELECT id, ST_Transform(geom, 3857) AS geom
      FROM utilisateurs_test WHERE id = 1) AS u
WHERE ST_Distance(a.geom, ST_Transform(u.geom, 3857)) <= 5000
ORDER BY distance_en_metres;
```

Cette requête liste les antennes situées à moins de 5 km d'un point donné, avec leur distance exacte — et peut être enrichie de calculs additionnels (pourcentage de réception théorique, débit indicatif...) selon les besoins de l'étude.

> [!tip] À retenir
> - Toujours vérifier et harmoniser le système de coordonnées avant de croiser des couches (`ST_Transform` / réexport avec un SCR cible).
> - Sur un jeu de données volumineux, filtrer et alléger la base avant de styliser ou d'analyser, sinon les traitements deviennent très lents.
> - L'interface graphique de QGIS (filtrage, symbologie, carte de chaleur) convient bien aux opérations ponctuelles ; des requêtes SQL enregistrées sont préférables dès qu'un traitement doit être répété ou réappliqué à de nouvelles données.
> - Une couverture réseau simulée par un simple tampon circulaire reste une approximation : elle ignore la puissance d'émission, l'altitude de l'antenne et le relief.
