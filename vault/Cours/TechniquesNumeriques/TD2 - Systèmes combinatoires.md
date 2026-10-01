---
tags: [techniques-numeriques, td, combinatoire]
---
# TD : Systèmes combinatoires

Retour : [[00 - Sommaire Techniques Numériques]] · Cours : [[02 - Logique combinatoire]]

> [!question]- Exercice 1 — Simplifier les fonctions suivantes
> a) `F1 = A·B̄·C̄ + A·C·(B̄+C̄)`
> b) `F2 = AB̄C + ĀBC + AB̄C̄ + ĀB̄C + ABC`
> c) `F3 = A·(B+C)̄·B` puis donner son complément
> d) `F4 = (A+B̄)·(C̄D) + AB·(C̄+D)`
>
> *Méthode : construire la table de vérité ou le tableau de Karnaugh de
> chaque fonction, puis regrouper les « 1 » adjacents en blocs de 1, 2, 4
> ou 8 pour obtenir l'expression minimale. Le complément s'obtient soit en
> développant par les « 0 », soit par les lois de De Morgan.*

> [!question]- Exercice 2 — Détecteur N > 5
> Soit `N = (ABCD)₂` un nombre binaire non signé. On veut `S=1` si `N>5`.
>
> a) Table de vérité : `S=1` pour `N=6,7,...,15` soit les lignes où
> `A=1` (sauf `N=6,7` à examiner en détail avec B,C,D) — après
> simplification par Karnaugh, on obtient une expression minimale du type
> `S = A + BC + BD` *(à vérifier ligne à ligne selon la table exacte)*.
>
> b) Schéma avec opérateurs de base (portes ET, OU).
>
> c) Schéma en n'utilisant que des **portes NAND à 2 entrées** : on
> complémente deux fois l'expression puis on applique De Morgan pour
> remplacer chaque ET/OU par des NAND (structure « universelle »).

> [!question]- Exercice 3 — Circuit à 4 portes NAND
> Un montage à 4 portes NAND2 (référence type `SN74LS00`) relie deux
> entrées `E1, E2`. En analysant le schéma (portes 1, 2, 3 et une porte de
> sortie 4), on retrouve que le montage réalise la fonction
> **OU EXCLUSIF** : `S = E1 ⊕ E2` (structure classique de réalisation du
> XOR à 4 NAND).

> [!question]- Exercice 4 — Opérateur logique programmable
> `S = f(E1, E2, P1, P2)` défini par un tableau de Karnaugh à 4 variables.
>
> 1) Après simplification par Karnaugh (en tenant compte de la valeur
>    indifférente `X`), on obtient l'expression minimale de `S`.
>
> 2) En figeant `P1, P2` à chacune des 4 combinaisons possibles, on
>    retrouve que le circuit réalise successivement les 4 fonctions
>    logiques de base à 2 entrées (par exemple ET, OU, NON-ET, NON-OU selon
>    le tableau) :
>
> | P1 | P2 | Expression de S | Fonction |
> |---|---|---|---|
> | 0 | 0 | ... | ... |
> | 0 | 1 | ... | ... |
> | 1 | 0 | ... | ... |
> | 1 | 1 | ... | ... |

> [!question]- Exercice 5 — Circuit à multiplexeur
> `S = f(E0,E1,E2,E3,X,Y)`. Le circuit est un **multiplexeur à 4 entrées** :
> `X` et `Y` sont les entrées de **sélection** (adressage) qui choisissent
> laquelle des 4 entrées `E0` à `E3` est recopiée sur la sortie `S`.

> [!question]- Exercice 6 — Circuit à comparateurs
> `Y = f(S1, S2, E1, E2)`. Ce montage réalise la fonction **comparateur** :
> `Y` indique si les mots d'entrée sont égaux (ou une relation d'ordre
> selon le câblage exact de `S1, S2`).

> [!question]- Exercice 7 — Décodeur 7 segments
> Réaliser un décodeur qui affiche, sur un afficheur 7 segments, le chiffre
> codé sur 4 bits `b3 b2 b1 b0`. Pour chaque segment (a à g), établir la
> table de vérité à partir du dessin des chiffres 0 à 9, puis simplifier
> par Karnaugh (les combinaisons 10 à 15 sont des états indifférents `X`).
> *Application pratique* : voir aussi le TP Quartus dans le [[00 - Sommaire Techniques Numériques|sommaire du module]].

## Application : circuits industriels réels

> [!example] Afficheur piloté par un clavier
> Réaliser un système combinatoire affichant le numéro de la touche
> appuyée sur un afficheur 7 segments :
> - **1ère solution** : trouver directement l'équation de chaque segment à
>   partir de la table de vérité complète (7 fonctions de plusieurs
>   variables).
> - **2nde solution**, plus réaliste : utiliser des circuits industriels
>   existants avec un codage intermédiaire **BCD** — un encodeur de
>   priorité (`74LS148`) puis un décodeur BCD → 7 segments (`74LS47`).

## T.P. Quartus : circuits combinatoires

Objectif : prendre en main **Quartus II** (Altera) à travers l'étude de
circuits combinatoires simples.

1. Suivre le tutoriel Quartus (saisie de schéma, création de projet).
2. Mettre en œuvre un **décodeur 7 segments** de la bibliothèque, piloté
   par 4 interrupteurs (utilisation d'un **bus** `E[3..0]`).
3. Étudier une **transmission numérique codée** (4 bits de donnée + 3 bits
   de contrôle) capable de détecter et corriger automatiquement une erreur
   sur un bit (codeur `codeur47` / décodeur `décodeur74`), avec injection
   d'erreurs simulée par des portes OU EXCLUSIF.
4. *(optionnel)* Réaliser un décodeur **code de Gray → binaire pur**, testé
   avec un décodeur 7 segments et 4 interrupteurs.

## Révision
- QCM du module : [/qcm/](/qcm/) (catégorie « TechniquesNumeriques »)
