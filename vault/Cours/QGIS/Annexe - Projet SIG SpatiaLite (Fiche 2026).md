---
tags: [qgis, sig, projet]
---
# Projet SIG, SpatiaLite & Open Data — Fiche 2026
Retour : [[00 - Sommaire QGIS]]

> [!abstract] Cadre
> Module : Systèmes d'Information Géographique (SIG) · Parcours : Licence NED 2e année.
> Logiciel principal : **QGIS**. Gestionnaire de données : **SpatiaLite**.
> Formats de rendu : le projet QGIS (`.qgz`), la base SpatiaLite (`.sqlite`) et une note de synthèse (`.pdf`).

Cette fiche décrit un Apprentissage Par Projet (APP) consistant à répondre, avec un SIG vectoriel, à une problématique d'analyse spatiale sur un sujet libre (civil ou militaire).

## Objectifs de l'apprentissage

À l'issue du projet, l'apprenant doit savoir :

- **Sourcing & Open Data** : identifier, évaluer et extraire des jeux de données géographiques ouverts (France, OACI, Eurocontrol, international).
- **Gestion de données en base** : structurer, nettoyer et stocker les couches vectorielles dans une base **SpatiaLite** (interopérable, légère, exploitable hors réseau).
- **Analyse spatiale vectorielle** : requêtes spatiales et attributaires, analyses de gabarits/servitudes, de proximité (tampons, intersections, zones d'exclusion) ou d'accessibilité.
- **Sémiologie graphique & cartographie décisionnelle** : concevoir des cartes lisibles et normées d'aide à la décision.

## Le cadre du projet

### Choix du sujet (libre ou militaire)

Le sujet est libre, choisi selon les intérêts ou enjeux métier de l'apprenant.

**Exemples — orientation Armée de l'Air & de l'Espace :**

- *Protections & emprises* : périmètres de sécurité, servitudes de dégagement ou exposition au bruit autour d'une base aérienne.
- *Sécurité aérienne* : cartographie du risque aviaire (proximité zones humides/décharges avec les axes d'approche).
- *Déploiement d'Éléments Air Projetés (EAP)* : analyse de sites pour l'implantation d'une piste sommaire ou d'un campement (accès routiers, contraintes du sol).
- *Logistique air* : accessibilité routière pour l'approvisionnement (kérosène, munitions) vers les bases.

**Exemples — thématique civile / libre :**

- *Aménagement & environnement* : implantation de bornes de recharge, accès aux services publics ou aux espaces verts.
- *Risques naturels & sécurité civile* : vulnérabilité aux inondations, couverture d'un territoire par les centres de secours.

### Contraintes techniques

- Logiciel : **QGIS** exclusivement.
- Base de données : toutes les données vectorielles nettoyées doivent résider dans une **unique base SpatiaLite** (`.sqlite`) — aucun fichier Shapefile éparpillé.
- Périmètre :
  - Exclusion des traitements raster et de l'orthoréférencement d'images.
  - Exploitation obligatoire de données vectorielles Open Data (`.geojson`, `.gpkg`, `.shp`, OpenStreetMap, etc.).

## Sources de données Open Data préconisées

| Domaine | Sources |
|---|---|
| Aéronautique & Air | SIA / AIP France (espaces aériens, obstacles, infrastructures) ; OpenSky Network / Eurocontrol (flux d'aéronefs) |
| Territoire & Infrastructures | Géoservices IGN (BD TOPO®, ADMIN EXPRESS) ; Data.gouv.fr ; OpenStreetMap via l'extension **QuickOSM** sous QGIS |
| International & théâtres | HDX (Humanitarian Data Exchange), USGS Open Data (pistes d'atterrissage, limites administratives, réseaux mondiaux) |

## Étapes clés de la démarche

1. **Cadrage** : question décisionnelle, territoire, liste des données requises.
2. **Collecte & intégration** : récupération des couches Open Data, import dans la base SpatiaLite.
3. **Préparation** : harmonisation du système de coordonnées de référence (SCR), nettoyage des tables attributaires.
4. **Analyses spatiales vectorielles** : requêtes attributaires/spatiales, zones d'influence (*buffers*), intersections, jointures.
5. **Restitution cartographique** : sémiologie graphique adaptée, mise en page professionnelle exportée sous QGIS.

## Livrables attendus

1. La base de données SpatiaLite (`.sqlite`), dédiée au projet, structurée et nettoyée.
2. Le projet QGIS (`.qgz`), pointant directement vers la base SpatiaLite.
3. La note de synthèse (3 à 5 pages) :
   - présentation de la problématique retenue (libre ou militaire) ;
   - tableau de traçabilité des données Open Data (source, date, précision) ;
   - description de la chaîne de traitements vectoriels réalisés sous QGIS ;
   - carte(s) finale(s) accompagnée(s) d'un commentaire d'analyse.

## Grille d'évaluation

| Critère | Poids | Description |
|---|---|---|
| Pertinence du sujet & Open Data | 10 % | Clarté de la problématique choisie et adéquation des données Open Data mobilisées |
| Rigueur dans SpatiaLite | 20 % | Structuration de la BDD, propreté des couches, absence de doublons, typage des champs |
| Exploitation & analyses SIG | 30 % | Pertinence et technicité des requêtes et traitements vectoriels réalisés sous QGIS |
| Qualité cartographique | 20 % | Respect des règles de sémiologie graphique, lisibilité, présence des éléments obligatoires (Nord, échelle, légende, titre, sources) |
| Note de synthèse | 20 % | Esprit de synthèse, justification des choix techniques, traçabilité de la démarche |

> [!tip] À retenir
> Une seule base SpatiaLite propre, un projet QGIS qui pointe dessus, et une note de synthèse courte mais complète (traçabilité des sources, chaîne de traitement, carte commentée) : c'est ce triptyque qui est noté, avec le plus gros poids (30 %) sur la pertinence des analyses spatiales elles-mêmes.

> [!question]- Par où commencer ?
> 1. Choisir une problématique précise (une question à laquelle la carte doit répondre), pas un thème vague.
> 2. Lister à l'avance les couches Open Data nécessaires et vérifier leur disponibilité avant de s'engager sur le sujet.
> 3. Créer la base SpatiaLite dès le départ et y importer systématiquement chaque couche nettoyée, plutôt que de travailler sur des fichiers épars.
