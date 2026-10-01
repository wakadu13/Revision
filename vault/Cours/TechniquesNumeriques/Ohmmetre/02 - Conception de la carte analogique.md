---
tags: [techniques-numeriques, mini-projet, ohmmetre]
---
# Phase 1 — Conception de la carte analogique

Retour : [[00 - Sommaire Mini-Projet Ohmmètre]] · Précédent : [[01 - Principe et cahier des charges]] · Suite : [[03 - Traitement numérique]]

La Phase 1 du mini-projet consiste à **concevoir et réaliser la carte
électronique** analogique de l'ohmmètre (celle qui porte le comparateur et
le circuit RC décrits dans [[01 - Principe et cahier des charges]]).

## Étapes de conception

1. **Schéma** : saisie du schéma électrique de la carte (condensateur,
   emplacement de la résistance à mesurer, potentiomètre de réglage de
   `Vref`, amplificateur opérationnel monté en comparateur).
2. **Circuit imprimé (PCB)** : conception du typon à partir du schéma.
3. **Placement et routage** des composants sur le circuit imprimé.
4. **Réalisation** physique du circuit imprimé et montage des composants
   (soudure).

## Outils de CAO électronique

- **KiCad** : logiciel de CAO électronique utilisé pour la saisie du
  schéma *et* la conception du circuit imprimé (PCB, *Printed Circuit
  Board*).
- **Labo CI – EAE** : réalisation physique du circuit imprimé.
- Tutoriels vidéo de référence (Eric Peronnin) :
  - saisie de schéma : vidéos n° 4, 5, 8, 10
  - conception et réalisation du PCB : vidéos n° 1-2, 3

> [!tip] À retenir
> Le connecteur entre la carte analogique et la carte FPGA transporte 4
> signaux essentiels : l'alimentation, la masse, le signal carré `v(t)`
> injecté dans le circuit RC, et la sortie logique du comparateur
> (`Vcomp`) qui indique si `uc(t)` a dépassé `Vref`. C'est cette sortie
> logique qui pilote la partie numérique du système (voir
> [[03 - Traitement numérique]]).

## Révision
- QCM du module : [/qcm/](/qcm/) (catégorie « TechniquesNumeriques »)
