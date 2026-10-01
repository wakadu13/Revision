---
tags: [techniques-numeriques, mini-projet, ohmmetre]
---
# Principe et cahier des charges

Retour : [[00 - Sommaire Mini-Projet Ohmmètre]] · Suite : [[02 - Conception de la carte analogique]]

## Introduction

Le but du mini-projet est de concevoir et réaliser la **mesure et
l'affichage numérique** de la valeur d'une résistance, grâce à une carte à
FPGA (Altera DE0, ou DE10-Lite selon les promotions).

Le travail se fait en **binômes**, sur trois séances de 2 heures :

1. Conception, saisie de schéma et simulation d'une **partie seulement**
   du système par chaque élève.
2. Réunion des différentes parties et mise au point du fonctionnement
   d'ensemble.
3. Démonstration du fonctionnement complet par chaque groupe.

> [!warning] À prévoir
> En dehors de ces créneaux, un volume supplémentaire de **4 à 6 heures**
> de travail est vraisemblablement nécessaire. Un compte-rendu par groupe
> est à fournir dans un délai d'une semaine après la dernière séance (voir
> [[04 - Attendus du rapport]]).

## Principe de fonctionnement

Un circuit analogique complémentaire comporte les composants nécessaires à
la mesure :

- un condensateur fixe de **100 nF**,
- un emplacement pour la résistance à mesurer,
- un potentiomètre pour créer et ajuster une tension de seuil,
- un amplificateur opérationnel utilisé comme **comparateur**.

Le condensateur `C` (100 nF) est chargé à travers la résistance `R` à
mesurer. On applique un signal carré `v(t)` (valeur max ≈ 3,4 V) : la
tension `uc(t)` aux bornes de `C` présente des montées et descentes
exponentielles. Le comparateur indique si `uc(t)` est inférieure ou
supérieure à une tension de référence `Vref` (réglée à **1,87 V**).

> [!tip] Idée clé
> Le temps que met `uc(t)` pour atteindre `Vref` est **proportionnel à la
> constante de temps `RC`** du circuit, donc à la résistance `R` à
> mesurer. En **chronométrant** cette durée avec un compteur numérique
> cadencé par une horloge connue, on en déduit la valeur de `R`, que l'on
> affiche en kΩ.

Schéma de principe : signal carré `v(t)` → charge du condensateur `C` à
travers `R` → tension `uc(t)` → comparateur (référence `Vref`) → sortie
logique exploitée par la partie numérique (voir [[03 - Traitement numérique]]).

## Cahier des charges

### 1) Travail initial

- Construire un **schéma fonctionnel** de l'ensemble faisant apparaître les
  principales fonctions du système (à présenter en première séance).
- Concevoir et réaliser le **compteur** qui chronomètre le temps de charge
  du condensateur.
- Afficher la résistance mesurée en kΩ sur **3 digits** dont 1 pour les
  décimales (mesures jusqu'à 99,9 kΩ).
- Le condensateur et le comparateur sont déjà câblés sur le circuit
  complémentaire fourni.

> [!important] Contraintes de fonctionnement
> - Fonctionnement **permanent**, sans intervention manuelle.
> - Affichage **rafraîchi entre 2 et 5 fois par seconde** (lecture
>   confortable).
> - **Précision de l'ordre de 1 à 2 %** souhaitable.

### 2) Améliorations

- **2.1** Si `R < 10 kΩ` : afficher avec 1 chiffre avant la virgule et 2
  chiffres après (3 chiffres significatifs), changement de calibre
  **automatique et réversible**.
  Exemples d'affichage : `27.5`, `10.1`, `9.25`, `1.23`, `0.47`, `0.09` (en kΩ).
- **2.2** Si `R` est trop grande (ou infinie) : faire **clignoter**
  l'affichage pour signaler un dépassement de capacité.
- **2.3** Prendre en compte les résistances `> 100 kΩ`, avec changement de
  calibre manuel ou automatique.
- **2.4** La résistance interne de la source qui fournit `v(t)` (≈30 à
  40 Ω) introduit une erreur systématique : chercher à la **corriger**.

## Ressources disponibles

### Les compteurs

Le logiciel Quartus permet de créer des compteurs sur mesure via le
composant `lpm_counter` (largeur configurable, Clear et entrées de
préchargement synchrones ou asynchrones). La mise en cascade de plusieurs
compteurs se fait en reliant la sortie de retenue (*Carry Out*) d'un
digit à l'entrée de retenue (*Carry In*) du digit de poids supérieur ;
l'horloge est commune à tous les étages.

### Les horloges

Le composant `Clock_Div` fournit plusieurs fréquences dérivées d'une
horloge de 50 MHz (50 MHz, 1 MHz, 100 kHz, 10 kHz, 1 kHz, 100 Hz, 10 Hz,
5 Hz, 1 Hz). Les autres fréquences nécessaires sont à réaliser à partir de
ces fréquences disponibles.

## Méthode de travail

Une attention particulière doit être portée à la **hiérarchisation** du
travail : chaque bloc, chaque fonction ou schéma intermédiaire fait
l'objet d'une **création de symbole** (`File → Create/Update → Create
Symbol Files for Current File`).

À l'issue du mini-projet, chaque binôme rédige un compte-rendu comportant :
- le découpage du projet et le rôle de chacun,
- la conception de chacune des parties (schémas),
- la simulation et la validation de ces mêmes parties (chronogrammes).

Le fonctionnement d'ensemble est démontré pendant la dernière séance.

## Évaluation

- Répartition du travail
- Simplicité et concision du schéma d'ensemble
- Structure et hiérarchisation du système
- Pertinence du choix des noms des boîtiers et des signaux
- Pertinence des simulations des sous-parties
- Qualité des explications
- Bon fonctionnement par rapport au cahier des charges
- Réalisation des améliorations

## Révision
- QCM du module : [/qcm/](/qcm/) (catégorie « TechniquesNumeriques »)
