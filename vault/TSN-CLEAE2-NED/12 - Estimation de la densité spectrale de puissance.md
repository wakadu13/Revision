---
tags: [TSN, DSP, périodogramme, welch, bartlett]
---
# Estimation de la densité spectrale de puissance
Retour : [[00 - Sommaire TSN]] · Précédent : [[11 - Estimation de l'autocorrélation]] · TD associé : [[TD3 - Corrélation et DSP]] · Suite : [[13 - Filtrage linéaire]]

## Estimateurs basiques
> [!note] Corrélogramme (via Wiener–Khinchin)
> $$\hat S_{\mathbf{x}}[k] = \text{DFT}(\hat R_{\mathbf{x}})[k]$$

> [!note] Périodogramme
> $$\hat S_{\mathbf{x}}[k] = \frac{1}{N}\big|\text{DFT}(\mathbf{x})[k]\big|^2$$

> [!tip] Remarque : les deux coïncident
> $$\underbrace{\text{DFT}\big(\hat R^{(\text{biaisé})}_{\mathbf{x}}\big)[k]}_{\text{Wiener–Khinchin}} = \underbrace{\frac1N\big|\text{DFT}(\mathbf{x})[k]\big|^2}_{\text{Périodogramme}}$$
> (avec l'autocorrélation **biaisée** calculée sur tous les retards $-(N-1)\dots N-1$ et les deux spectres évalués aux mêmes fréquences.)
> Avec l'autocorrélation **non biaisée**, le corrélogramme peut devenir **négatif** (impossible pour une DSP) et il est plus bruité.

> [!warning] Défauts des estimateurs basiques
> - **Biaisés** : $\mathbb{E}\big[\hat S_{\mathbf{x}}[k]\big] = (S_{\mathbf{x}} * W)[k]$ — la vraie DSP est convoluée par le spectre $W$ de la fenêtre (ici un sinc², cf. [[08 - Résolution spectrale et fenêtrage]]).
> - **Non consistants** : $\text{Var}\big(\hat S_{\mathbf{x}}[k]\big) \not\to 0$ quand $N\to\infty$. Augmenter $N$ affine la grille mais **n'élimine pas les fluctuations** : le périodogramme d'un bruit blanc reste très « chevelu ».

## Estimateurs pondérés (périodogramme fenêtré)
> [!note] Périodogramme pondéré
> $$\hat S_{\mathbf{x}}[k] = \frac{1}{N}\big|\text{DFT}(\mathbf{x}\odot\mathbf{w})[k]\big|^2$$
> ($\odot$ : produit terme à terme, $\mathbf{w}$ : fenêtre de Hann, Blackman…)

- Même **compromis** que pour le fenêtrage : largeur du lobe principal vs niveau des lobes secondaires = résolution vs fuite spectrale.
- Toujours **biaisés** et **non consistants** : le fenêtrage réduit la fuite, pas la variance.

> [!info] Normalisation
> Avec une fenêtre non rectangulaire, on normalise souvent par $\sum_n w[n]^2$ au lieu de $N$ pour conserver la puissance (c'est ce que fait `pwelch`).

## Périodogrammes moyennés : méthode de Bartlett
> [!note] Méthode de Bartlett (écrit « Barlett » dans les slides)
> Pour un signal **stationnaire** :
> 1. Découper le signal en $J$ segments **disjoints** de $M$ points : $\{x_j[k]\}_{k=0,\dots,M-1}$ (donc $N = JM$)
> 2. Calculer $J$ périodogrammes pondérés : $\hat S_j[k] = \frac{1}{M}\big|\text{DFT}(\mathbf{x}_j\odot\mathbf{w})[k]\big|^2$
> 3. Moyenner : $$\hat S_{\mathbf{x}}[k] = \frac1J\sum_{j=0}^{J-1}\hat S_j[k]$$

**Compromis biais / variance** :
- la **variance décroît d'un facteur $J$** (moyenne de $J$ estimations ≈ indépendantes) ;
- la **résolution se dégrade** : chaque segment ne dure que $MT_e = T/J$ → résolution $\approx \frac{F_e}{M} = \frac{J}{T}$.

## Méthode de Welch
> [!note] Méthode de Welch (écrit « Welsh » dans les slides)
> Comme Bartlett, mais avec $J'$ segments **qui se chevauchent** (typiquement 50 % avec une fenêtre de Hann) :
> $$\hat S_{\mathbf{x}}[k] = \frac{1}{J'}\sum_{j=0}^{J'-1}\hat S_j[k], \qquad \hat S_j[k] = \frac{1}{M}\big|\text{DFT}(\mathbf{x}_j\odot\mathbf{w})[k]\big|^2$$

**Compromis** :
- variance réduite d'un facteur ≈ $J'$ avec **$J' > J$** → mieux que Bartlett à taille de segment égale ;
- résolution qui décroît (segments courts) ;
- la moyenne porte sur des segments **non indépendants** (chevauchement) → le gain en variance est un peu inférieur à $J'$.
- le chevauchement « récupère » les échantillons atténués par la fenêtre aux bords des segments.

## Synthèse

| Méthode | Biais | Variance | Résolution | Remarque |
|---|---|---|---|---|
| Corrélogramme (non biaisé) | faible | très forte | $\sim 1/T$ | peut être négatif |
| Périodogramme | sinc² (fuite) | forte, non consistant | $\sim 1/T$ | = corrélogramme biaisé |
| Périodogramme fenêtré | fuite réduite | forte | $\sim 2/T$ (Hann) | meilleure dynamique |
| Bartlett | fenêtre de $M$ pts | $\div J$ | $\sim F_e/M$ | segments disjoints |
| **Welch** | fenêtre de $M$ pts | $\div J'$ ($J'>J$) | $\sim F_e/M$ | le plus utilisé en pratique |

> [!important] Idée clé de la section
> On **échange de la résolution contre de la variance** : segments longs → spectre fin mais bruité ; segments courts → spectre lisse mais flou.

## MATLAB
```matlab
% Périodogramme (formule du cours), en dB
N  = length(x);
S  = abs(fftshift(fft(x))).^2/N;
f  = ((0:N-1) - floor(N/2))*Fe/N;
plot(f, 10*log10(S));

% Welch
M = 64; w = hann(M); noverlap = M/2; nfft = 512;
[Pw, fw] = pwelch(x, w, noverlap, nfft, Fe, 'centered');
plot(fw, 10*log10(Pw));   % pwelch renvoie une DSP en unités²/Hz
```
> [!warning] Unités pour comparer
> `pwelch` renvoie une DSP **par Hz** ; le périodogramme $|X|^2/N$ est une puissance **par case fréquentielle**. Pour comparer : diviser le périodogramme par $F_e$ (ou multiplier `Pw` par $F_e$).
