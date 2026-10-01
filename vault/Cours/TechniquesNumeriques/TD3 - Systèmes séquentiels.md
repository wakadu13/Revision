---
tags: [techniques-numeriques, td, sequentiel]
---
# TD : Systèmes séquentiels

Retour : [[00 - Sommaire Techniques Numériques]] · Cours : [[03 - Logique séquentielle]]

> [!question]- Exercice 1 — Combinatoire ou séquentiel ?
> On donne les chronogrammes de deux systèmes (entrées `A,B` ou `A,B,C` et
> sortie `S`). *Méthode* : un système est **séquentiel** si, pour une même
> combinaison des entrées, la sortie peut prendre des valeurs différentes
> selon l'historique — sinon il est **combinatoire**.

> [!question]- Exercice 2 — Bascule D et bascule JK
> Deux montages : une bascule D dont la sortie `Q1` rebouclée est reliée à
> une seconde bascule D (`Q2`), et une bascule JK avec `J` relié à `H`.
> Tracer le chronogramme de `Q` en fonction de `H` (signal carré régulier).
> *Pour la bascule D en boucle sur elle-même (D=Q̄) : elle **divise la
> fréquence d'horloge par 2*** (comportement de bascule T).

> [!question]- Exercice 3 — Compléter les chronogrammes
> 3.1. Montage à 2 bascules D en cascade (`Q0`, `Q1`) : en déduire la
> fonction réalisée (diviseur de fréquence par 4).
> 3.2. Montage à 2 bascules JK avec `J=K=1` en cascade : même conclusion,
> chaque étage divise la fréquence par 2 (**compteur asynchrone modulo 4**).

> [!question]- Exercice 4 — Synthèse d'un compteur synchrone (bascules D)
> Séquence à réaliser : `0, 8, 12, 14, 7, 11, 13, 6, 3, 9, 4, 10, 5, 2, 1, 0...`
>
> 1) Pour chaque bascule, exprimer l'état final en fonction de l'état
>    initial (table état présent / état futur), puis en déduire l'entrée
>    `D` de chaque bascule. On obtient (résultat classique pour cette
>    séquence, vérifié en TP) :
>    `D3 = Q̄1·Q̄0 + Q1·Q0`, `D2 = Q3`, `D1 = Q2`, `D0 = Q1`.
>
> 2) Cette séquence peut aussi se réaliser avec un **registre à décalage**
>    correctement rebouclé (registre à décalage à rétroaction, proche
>    d'un compteur de Johnson/Gray).
>
> 3) **Problème à la mise sous tension** : l'état initial du compteur est
>    imprévisible (les bascules peuvent démarrer dans un état hors
>    séquence). *Solution* : ajouter un circuit de détection des états
>    hors séquence qui force une réinitialisation (RAZ) vers un état de la
>    séquence normale.

> [!question]- Exercice 5 — Synthèse d'un compteur à bascules JK
> Séquence : `0, 2, 4, 5, 1, 0, 2, 4, 5, 1, 0...` (5 états, à réaliser sur 3
> bascules JK). *Méthode de Marcus* : tableau état présent → état futur →
> conditionnement des entrées `J,K` de chaque bascule, puis simplification
> par Karnaugh de chaque entrée (en exploitant les états `x` hors
> séquence).

## T.P. : circuits séquentiels (Quartus)

**I) Analyse d'un compteur à bascules JK.** Compteur synchrone à 3
bascules JK (`jkff` sous Quartus), avec :

$$K_2 = \bar Q_0 \bar Q_1 \qquad J_2 = Q_1 Q_0 \qquad K_1 = Q_0 \qquad J_1 = Q_0 Q_2 \qquad K_0 = J_0 = 1$$

Saisir le schéma avec une horloge de 1 Hz et un décodeur 7 segments,
ajouter des entrées de forçage pour choisir différentes valeurs initiales,
et relever les séquences obtenues pour `N = (Q2Q1Q0)₂` selon l'état
initial.

**II) Compteur/décompteur décimal à 2 chiffres.** Deux compteurs BCD en
cascade (unités + dizaines), reliés par la sortie *Carry Out* du compteur
des unités vers l'entrée *Carry In* du compteur des dizaines. Prévoir :
- un switch pour le sens de comptage,
- un bouton-poussoir de RAZ,
- 2 afficheurs 7 segments.

**III) Synthèse d'un compteur synchrone à bascules D.** Vérifier
expérimentalement la séquence de l'exercice 4 avec les équations
`D3 = Q̄1Q̄0 + Q1Q0`, `D2 = Q3`, `D1 = Q2`, `D0 = Q1` (composant `dff` sous
Quartus), et tester le comportement à la mise sous tension avec les
entrées de forçage `PRN` / `CLRN`.

## Révision
- QCM du module : [/qcm/](/qcm/) (catégorie « TechniquesNumeriques »)
