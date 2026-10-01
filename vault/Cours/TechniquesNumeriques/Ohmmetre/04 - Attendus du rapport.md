---
tags: [techniques-numeriques, mini-projet, ohmmetre]
---
# Attendus du rapport à déposer

Retour : [[00 - Sommaire Mini-Projet Ohmmètre]] · Précédent : [[03 - Traitement numérique]]

> [!warning] Dépôt
> Le document (format Word, **20 pages maximum**) doit être déposé avec
> **tous les fichiers annexes** (fichiers de simulation, projet KiCad...)
> sous Moodle, dans un dossier nommé `Nom1_Nom2_NED202526`.
> Consulter la date limite de dépôt indiquée sur Moodle : au-delà, le
> dépôt n'est plus possible.

## 1ère partie — Carte électronique (analogique)

- **Explication critique** du fonctionnement du schéma de la carte
  électronique ohmmètre, **courbes à l'appui** (voir
  [[01 - Principe et cahier des charges]] pour le principe de mesure par
  charge du condensateur).
- Explication de la **réalisation technique** de cette carte : PCB,
  circuit imprimé, montage des composants (voir
  [[02 - Conception de la carte analogique]]).
- Partie technique avec **schéma et typon**.

## 2ème partie — Traitement numérique (Quartus)

- **Explication complète de chaque sous-système** du dispositif numérique
  élaboré sous Quartus (voir le découpage en sous-blocs proposé dans
  [[03 - Traitement numérique]]). Chaque sous-partie doit être **désignée
  par la fonction qu'elle réalise**. Des **chronogrammes** doivent, si
  besoin, constituer la base des explications, en s'appuyant, lorsque
  c'est pertinent, sur les signaux allant ou venant de la carte analogique
  fabriquée (comparateur + circuit RC).

- **Justifier précisément, calculs à l'appui, le choix de la fréquence
  d'horloge.** Il faut en particulier préciser (par le calcul) comment une
  mesure en **microsecondes** par le compteur de chronométrage est
  équivalente, au niveau de l'affichage, à la valeur de la résistance `R`
  mesurée (en kΩ).

- **Fournir les chronogrammes** ou, à défaut (non exclusif), la **preuve
  expérimentale** du bon fonctionnement de la sous-partie tirée au sort.
  Tout calcul, lorsqu'il est pertinent, est le bienvenu pour appuyer
  l'explication la plus précise possible du fonctionnement de ce
  dispositif. L'obtention des chronogrammes par le **simulateur de
  Quartus** constitue un plus.

> [!tip] Conseil de rédaction
> Le fil conducteur attendu est le même que la méthode de travail du
> mini-projet (voir [[01 - Principe et cahier des charges]]) :
> découpage du projet → conception de chaque partie (schémas) → simulation
> et validation (chronogrammes) → calculs justificatifs → fonctionnement
> global démontré.

## Révision
- QCM du module : [/qcm/](/qcm/) (catégorie « TechniquesNumeriques »)
