---
tags: [techniques-numeriques, mini-projet, ohmmetre, quartus]
---
# Phase 2 — Traitement numérique (Quartus)

Retour : [[00 - Sommaire Mini-Projet Ohmmètre]] · Précédent : [[02 - Conception de la carte analogique]] · Suite : [[04 - Attendus du rapport]]

La Phase 2 porte sur la conception, sous **Quartus**, du système logique
programmé dans le FPGA qui exploite la sortie du comparateur de la carte
analogique (Phase 1) pour **chronométrer** la charge du condensateur et
**afficher** la résistance mesurée.

## Architecture générale

Le dispositif numérique complet s'organise en **sous-systèmes**, chacun
désigné par la fonction qu'il réalise (c'est d'ailleurs ce découpage par
fonction qui est attendu dans le rapport, voir
[[04 - Attendus du rapport]]) :

- une **horloge de référence** (50 MHz sur la carte DE0) associée à un
  **diviseur de fréquence** pour générer l'horloge de mesure ;
- un ou plusieurs **compteurs** qui chronomètrent le temps de charge du
  condensateur, cadencés par l'horloge de mesure, et remis à zéro à chaque
  période du signal `v(t)` ;
- un circuit de **détection du dépassement de capacité** (résistance trop
  grande, ou infinie) qui déclenche le clignotement de l'affichage ;
- un circuit de **sélection de calibre** (automatique ou manuel selon les
  améliorations demandées), qui choisit le quartet bas / milieu / haut du
  compteur à afficher selon la plage de résistance mesurée ;
- une **conversion binaire → BCD → 7 segments** pour chacun des 3 digits
  affichés ;
- une gestion du **point décimal** (position variable selon le calibre
  sélectionné, cf. cahier des charges 2.1).

> [!important] Point clé du cahier des charges
> La durée mesurée par le compteur (en microsecondes) doit être convertie,
> par un choix judicieux de la **fréquence d'horloge**, en une valeur
> directement exploitable pour l'affichage de `R` en kΩ. Ce calcul
> (fréquence d'horloge ↔ résolution de mesure ↔ plage de résistances) est
> un attendu explicite du rapport — voir [[04 - Attendus du rapport]].

## Exemple de schéma (correction / exemple type)

Le schéma ci-dessous illustre une réalisation possible du sous-système de
traitement numérique complet sous Quartus, avec sa hiérarchie de
sous-blocs (horloge/diviseur, compteurs de mesure, détection de
dépassement, sélection de quartet, conversion BCD → 7 segments,
gestion du changement de calibre automatique) :

![[ohmmetre-traitement-numerique.png]]

> [!tip] Méthode
> Comme pour le mini-projet dans son ensemble (voir
> [[01 - Principe et cahier des charges]]), chaque bloc intermédiaire doit
> faire l'objet d'une **création de symbole** Quartus
> (`File → Create/Update → Create Symbol Files for Current File`) afin de
> garder un schéma de haut niveau **simple et lisible**, qui ne fait
> apparaître que les fonctions principales du système.

## Ressources Quartus utiles

- `lpm_counter` : compteur paramétrable (largeur, Clear synchrone ou
  asynchrone, entrées de préchargement) — voir
  [[01 - Principe et cahier des charges]].
- `Clock_Div` : diviseur de fréquence fournissant plusieurs horloges
  dérivées de l'horloge 50 MHz de la carte.
- Décodeurs 7 segments et bus (`[N..0]`) : voir [[02 - Logique combinatoire]]
  et [[TD2 - Systèmes combinatoires]] pour la méthode de conception d'un
  décodeur 7 segments.
- Compteurs et bascules synchrones : voir [[03 - Logique séquentielle]].

## Révision
- QCM du module : [/qcm/](/qcm/) (catégorie « TechniquesNumeriques »)
