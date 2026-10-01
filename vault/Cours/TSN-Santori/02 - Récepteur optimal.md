---
tags: [telecom, NED, recepteur-optimal, filtrage-adapte, nyquist]
---
# Le récepteur optimal
Retour : [[00 - Sommaire TSN-CLEAE2-NED]] · Précédent : [[01 - Numérisation et codage en ligne]] · Suite : [[03 - Modulations numériques]]

## Objectifs du cours

- Détailler la structure du récepteur optimal.
- Expliquer l'origine des interférences entre symboles (IES).
- Présenter les moyens permettant d'optimiser la réception d'un signal.

## Plan

1. Structure du récepteur
2. Filtrage adapté
3. Interférences entre symboles
4. Filtre de Nyquist

## Structure du récepteur optimal

On admet la structure optimale du récepteur suivante :

```
u(t) → [Filtre gr(t)] → z(t) → [Échantillonnage à 1/Ts] → z̃(n) → [Détecteur à seuils] → symboles estimés
```

avec $z(t) = u(t) \ast g_r(t) = s'(t) \ast g_r(t) + b_e(t) \ast g_r(t)$ (terme signal + terme bruit), où $s'(t)$ est le signal déformé par son passage dans le canal.

> [!tip] À retenir
> Cette structure est valable pour toute transmission, qu'elle soit en bande de base ou sur porteuse HF.

Le récepteur numérique doit **prendre une décision** quant à la valeur d'origine du symbole reçu : il ne s'agit pas de restituer le signal le plus fidèlement possible (comme en analogique) mais d'identifier le symbole de l'alphabet le plus probablement envoyé.

Deux phénomènes compliquent la prise de décision :
1. Addition de **bruit** lors du passage dans le canal.
2. Comportement du canal de propagation en **filtre passe-bas** : diminution du support fréquentiel du signal et augmentation de son support temporel.

## 1. Minimisation du bruit : filtrage adapté

On modélise la chaîne à l'aide de filtres :

```
Émetteur [filtre ge(t)] → s(t) → Canal [addition de bruit, filtre passe-bas (IES)] → u(t) → Récepteur [filtre gr(t)]
                                        (filtre global g(t))
```

Afin d'optimiser les performances du détecteur, on cherche à **maximiser le rapport signal à bruit (RSB) en réception**, en utilisant un **filtre adapté** (*matched filter*) $g_r$ tel que :

$$g_r(t) = g^*(-t)$$

## 2. Effet du filtrage du canal

Vidéo : [IES et Nyquist](https://youtu.be/Z-CJVTfMjZ4)

Le canal (modélisé en filtre passe-bas) déforme une impulsion rectangulaire : plus la fréquence de coupure $f_c$ du canal est basse (par rapport à $1/T$), plus l'impulsion s'étale dans le temps, débordant sur les symboles voisins.

### Interférences entre symboles (IES)

Les formants utilisés sont des fonctions rectangles, qui contiennent de l'énergie à hautes fréquences. L'augmentation du support temporel due au filtrage passe-bas du canal est à l'origine des **interférences entre symboles (IES)**.

Forme du signal $u(t)$ en entrée du récepteur :

$$u(t) = \sum_k a_k\, g(t - kT_s) + b_e(t)$$

Forme du signal $z(t)$ après filtrage adapté ($\tilde g(t) = g^*(-t) \ast g(t)$, $\tilde b(t) = h^*(-t) \ast b_e(t)$) :

$$z(t) = \sum_k a_k\, \tilde g(t - kT_s) + \tilde b(t)$$

Forme du signal $\tilde z(n)$ après échantillonnage :

$$\tilde z(n) = \sum_k \tilde g(n-k)\, a_{n-k} + \tilde b_n$$

Le terme pour $k \neq 0$ est le **terme d'interférence entre symboles**.

## Appréciation de la qualité du signal reçu : diagramme de l'œil

On affiche $u(t)$ sur un oscilloscope avec une base de temps réglée sur $T_s$ (2 ou 3 $T_s$ en abscisse), pour visualiser la superposition des symboles sur plusieurs périodes.

- Plus l'**ouverture verticale** est grande, plus facile est la distinction entre symboles ('0' et '1') ⇒ meilleure résistance au bruit.
- Plus l'**ouverture horizontale** est large, plus simple est le système de récupération de rythme ⇒ relâchement de la contrainte sur l'instant d'échantillonnage.

Vidéo : [Diagramme de l'œil](https://youtu.be/3OezVhSq8mg) (signal optique, mais valable pour des signaux électriques).

## Élimination des IES

Les IES modifient la valeur des symboles envoyés, ce qui entraîne une mauvaise transmission du message et des erreurs de décision :

$$\tilde z(n) = \sum_k \tilde g(k)\, a_{n-k} + \tilde b_n = \tilde g(0)\, a_n + \tilde b_n \quad \text{(cas idéal sans IES)}$$

Pour minimiser les IES, il faut trouver un filtre tel que $\tilde g(k) = 0$ pour tout $k \neq 0$, c'est-à-dire que les effets des symboles précédemment transmis soient annulés à tous les instants d'échantillonnage. Un tel filtre est appelé **filtre de Nyquist**.

## Filtres de Nyquist

**Critère temporel** : $\tilde g(t)|_{t=kT_s} = 0$ pour $k \neq 0$

**Critère fréquentiel équivalent** :
$$\sum_k \tilde G\left(f - \frac{k}{T_s}\right) = \text{cste} = T_s\, \tilde g(0)$$

> [!tip] Critère fréquentiel de Nyquist
> L'IES est nulle si le point $\left(\dfrac{1}{2T_s}, \dfrac{\tilde G(0)}{2}\right)$ de la réponse en fréquence est un **centre de symétrie**.

### Le cosinus surélevé

Le critère de Nyquist élargi propose un compromis entre largeur de bande et limitation temporelle de la réponse impulsionnelle : le filtre en **cosinus surélevé**.

$$
G(f) =
\begin{cases}
T_s & \text{si } |f| \leq \dfrac{1-\alpha}{2T_s} \\[4pt]
\dfrac{T_s}{2}\left[1 + \cos\left(\pi T_s \left(|f| - \dfrac{1-\alpha}{2T_s}\right)\right)\right] & \text{si } \dfrac{1-\alpha}{2T_s} \leq |f| \leq \dfrac{1+\alpha}{2T_s} \\[4pt]
0 & \text{si } |f| > \dfrac{1+\alpha}{2T_s}
\end{cases}
$$

- $\alpha$ est appelé **facteur d'excès de bande**, *facteur d'arrondi*, ou encore *facteur de retombée* (**roll-off factor**).
- On prend en général un $\alpha$ faible pour minimiser la bande occupée.
- Le point $\left(\dfrac{1}{2T_s}, \dfrac{G(0)}{2}\right)$ est bien un centre de symétrie.

## Entraînement

> [!question]- Questions de cours
> **Q1 : Débit binaire et débit symbole, quelle relation ?**
> $D = R \times n$, avec $n = \log_2(M)$ le nombre de bits par symbole et $R$ la rapidité de modulation (symboles/s).
>
> **Q2 : Qu'appelle-t-on interférence entre symboles ? Comment s'en affranchir ?**
> Phénomène par lequel l'étalement temporel d'un symbole (dû au filtrage du canal) vient perturber les symboles voisins. On s'en affranchit en utilisant un filtre global (émission + canal + réception) vérifiant le **critère de Nyquist**.
>
> **Q3 : Pourquoi communiquer en numérique plutôt qu'en analogique ?**
> Voir [[01 - Numérisation et codage en ligne#Numérique vs analogique]] : meilleure résistance au bruit, compression, chiffrement et filtrage facilités, régénération parfaite du signal.
>
> **Q4 : En quoi consiste l'opération de codage ?**
> Convention d'association entre symboles et/ou groupes de symboles d'alphabets différents ou non (voir [[01 - Numérisation et codage en ligne#Définitions et principe]]).
>
> **Q5 : Comment comparer les différents codes vis-à-vis d'un canal de transmission ?**
> Par leurs propriétés spectrales (largeur de bande, présence de composante continue) et leurs propriétés statistiques (nombre de transitions, capacité de synchronisation).
>
> **Q6 : Citez 6 codes différents.**
> NRZ, NRZI, RZ, Manchester (biphase), Manchester différentiel (DME), codage de Miller, bipolaire (AMI), HDBn.

> [!question]- Vrai ou Faux
> **Q7 : Un filtre de Nyquist a une réponse impulsionnelle non nulle en un seul point. VRAI ou FAUX ?**
> FAUX — un filtre de Nyquist a une réponse impulsionnelle nulle à tous les instants d'échantillonnage $kT_s$ sauf en $k=0$ (elle peut être non nulle entre ces instants).
>
> **Q8 : L'objectif du filtre adapté est d'éliminer l'IES. VRAI ou FAUX ?**
> FAUX — le filtre adapté maximise le rapport signal à bruit ; c'est le filtre de Nyquist (filtre global) qui élimine l'IES.
>
> **Q9 : L'objectif du filtre global de Nyquist est d'éliminer l'IES. VRAI ou FAUX ?**
> VRAI.
>
> **Q10 : Un filtre adapté est mis en place à l'émission. VRAI ou FAUX ?**
> FAUX — le filtre adapté est mis en place à la **réception** ($g_r(t) = g^*(-t)$).

## Exercices

> [!question]- Exercice 3 : Téléphone numérique
> Comparer la largeur de bande d'un canal audio téléphonique analogique de 3 kHz et d'un canal numérique où la voix est échantillonnée et quantifiée sur 256 niveaux, avec un débit binaire de 64 000 bit/s (IES nulle demandée).
>
> 256 niveaux = 8 bits/échantillon. Avec un débit de 64 000 bit/s, la rapidité de modulation (en binaire, $n=1$) est $R = D = 64\,000$ Bd. Avec un filtre de Nyquist idéal (bande minimale = $R/2$), la largeur de bande nécessaire est $B \geq 32$ kHz — nettement supérieure aux 3 kHz du canal analogique.

> [!question]- Exercice 4 : Filtres de Nyquist
> Liaison numérique de rapidité de modulation $R = 1/T_s$ bauds. Pour une transmission sans IES, le filtre global doit satisfaire le critère de Nyquist.
>
> **Q1 : Rappelez les deux versions du critère.**
> - Temporel : $\tilde g(kT_s) = 0$ pour $k \neq 0$.
> - Fréquentiel : $\sum_k \tilde G(f - k/T_s) = \text{cste}$ (ou : le point $(1/2T_s, \tilde G(0)/2)$ est un centre de symétrie).
>
> **Q2-Q3 :** un filtre rectangulaire de largeur totale $B = 3/(2T_s)$ (occupant $[-3/4T_s, 3/4T_s]$) ne vérifie pas nécessairement le critère de symétrie autour de $1/2T_s$ selon sa forme exacte ; un filtre de largeur $B=1/T_s$ (occupant $[-1/2T_s, 1/2T_s]$), rectangulaire, vérifie le critère de Nyquist (c'est le filtre de Nyquist « idéal », bande minimale de Nyquist). La rapidité de modulation maximale sans IES pour un filtre de bande $B$ est $R = B$ (cas du filtre rectangulaire).

> [!question]- Exercice 5 : Filtre en cosinus surélevé
> Transmission binaire bipolaire, filtre de mise en forme en racine de cosinus surélevé, roll-off $\alpha = 22\%$, $T_s \approx 0{,}26042\ \mu s$, largeur de bande du canal $B = 5$ MHz.
>
> **Q1 : Débit binaire ?**
> Transmission binaire ⇒ $D = R = 1/T_s \approx 3{,}84$ Mbit/s.
>
> **Q2 : Transmission sans IES possible ?**
> Bande occupée par un cosinus surélevé de roll-off $\alpha$ : $B_{occ} = \dfrac{1+\alpha}{T_s} \approx \dfrac{1{,}22}{0{,}26042\ \mu s} \approx 4{,}69$ MHz $< 5$ MHz ⇒ oui, c'est possible.
>
> **Q3 : Efficacité spectrale ?**
> $\eta = D/B = 3{,}84/5 \approx 0{,}77$ bit/s/Hz.
