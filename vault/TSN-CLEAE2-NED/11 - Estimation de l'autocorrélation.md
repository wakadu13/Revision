---
tags: [TSN, autocorrélation, estimation]
---
# Estimation de la fonction d'autocorrélation
Retour : [[00 - Sommaire TSN]] · Précédent : [[10 - Bruit de numérisation]] · Suite : [[12 - Estimation de la densité spectrale de puissance]]

## Rappel
- Autocorrélation : $R_X(t_1,t_2) = \mathbb{E}[X(t_1)X^*(t_2)]$
- Stationnarité d'ordre 2 : moyenne constante, $R_x(t_1,t_2) = R_x(t_1-t_2)$
- Wiener–Khinchin : $S_x(f) = \mathcal{F}(R_x)(f)$ → [[05 - Densité spectrale de puissance]]

**Problème** : on ne dispose que d'**une réalisation** de **$N$ échantillons** → on ne peut pas calculer l'espérance ; on la remplace par une **moyenne temporelle** (hypothèse d'ergodicité).

## Estimateur biaisé
> [!note] Estimateur biaisé
> $$\hat{R}_{\mathbf{x}}^{(\text{biaisé})}[n] = \frac{1}{N}\sum_{k=n}^{N-1} x[k]\,x^*[k-n], \qquad n = 0,\dots,N-1$$
> **Biais multiplicatif** :
> $$\mathbb{E}\big[\hat{R}_{\mathbf{x}}[n]\big] = \frac{N-|n|}{N}\,R_{\mathbf{x}}[n]$$

Il n'y a que $N - n$ produits dans la somme mais on divise par $N$ → l'estimation est **atténuée par une fenêtre triangulaire** (Bartlett) : elle tend vers 0 aux grands retards.

## Estimateur non biaisé
> [!note] Estimateur non biaisé
> $$\hat{R}_{\mathbf{x}}^{(\text{non-biaisé})}[n] = \frac{1}{N-n}\sum_{k=n}^{N-1} x[k]\,x^*[k-n], \qquad n = 0,\dots,N-1$$
> **Sans biais** : $\mathbb{E}\big[\hat R_{\mathbf{x}}[n]\big] = R_{\mathbf{x}}[n]$

Mais pour $n$ proche de $N$, la moyenne ne porte que sur **très peu de termes** → **variance très grande** aux bords (l'estimation « explose »).

> [!tip] Coût de calcul
> Dans les deux cas, **la DFT peut être utilisée pour réduire le coût de calcul** (corrélation = convolution de $x[n]$ avec $x^*[-n]$ → produit $|X[k]|^2$ en fréquence, avec zéro-padding à $2N-1$ points pour éviter l'effet circulaire).

## Compromis biais-variance
| | Estimateur biaisé | | Estimateur non biaisé |
|---|---|---|---|
| **Biais** | $\text{biais}(\hat R^{(b)}[n])$ | $\ge$ | $\text{biais}(\hat R^{(nb)}[n]) = 0$ |
| **Variance** | $\text{Var}(\hat R^{(b)}[n])$ | $\le$ | $\text{Var}(\hat R^{(nb)}[n])$ |
| **EQM** | $\text{EQM}(\hat R^{(b)}[n])$ | $\le$ | $\text{EQM}(\hat R^{(nb)}[n])$ |

> [!note] Erreur quadratique moyenne
> $$\text{EQM}(\hat\theta) = \mathbb{E}\big[(\hat\theta - \theta)^2\big] = \text{Var}(\hat\theta) + \text{biais}^2(\hat\theta)$$
> → L'estimateur **biaisé** est globalement **meilleur** (EQM plus faible). Il a en plus l'avantage de donner une DSP toujours positive (voir [[12 - Estimation de la densité spectrale de puissance]]).

## Exemples du cours
- $s[n] = A\cos(2\pi f_0 n + \phi)$ : l'autocorrélation est un **cosinus de même fréquence** (la phase disparaît).
  - biaisé → cosinus modulé par un triangle ;
  - non biaisé → cosinus d'amplitude constante, bruité aux bords.
- $s[n] = A\cos(2\pi f_0 n + \phi[n])$, $\phi[n]\sim\mathcal{N}(0,1)$ : la phase aléatoire décorrèle le signal → pic en 0 et structure oscillante atténuée ; les réalisations successives diffèrent, surtout aux grands retards.

> [!info] Autocorrélations théoriques utiles
> - $x(t) = A_1\cos(2\pi f_1 t) + A_2\cos(2\pi f_2 t)$ : $R_x(\tau) = \frac{A_1^2}{2}\cos(2\pi f_1\tau) + \frac{A_2^2}{2}\cos(2\pi f_2\tau)$, avec $R_x(0) = \frac{A_1^2+A_2^2}{2}$ = puissance.
> - Bruit blanc : $R_b[n] = \sigma^2\delta[n]$ (un pic en 0, rien ailleurs).
> - $y = x + b$ indépendants : $R_y = R_x + R_b$ → **le bruit n'affecte que le retard 0**. C'est ce qui permet de détecter une périodicité noyée dans le bruit.

## MATLAB
```matlab
[R, lags] = xcorr(x, 'biased');     % ou 'unbiased'
tau = lags/Fe;                       % retards en secondes
plot(tau, R); xlabel('\tau (s)');
```
`xcorr` renvoie les retards de $-(N-1)$ à $N-1$ ($2N-1$ points), la fonction étant à symétrie hermitienne : $R[-n] = R^*[n]$.
