---
tags: [TSN, rappels, DSP, aléatoire]
---
# Densité spectrale de puissance (rappel)
Retour : [[00 - Sommaire TSN]] · Précédent : [[04 - Transformée de Fourier à temps continu]] · Suite : [[06 - Étapes de la numérisation]]

## Pourquoi la DSP ?
- La **TF d'un signal aléatoire n'existe pas** (ni énergie finie, ni forme déterministe).
- On passe par un outil statistique : la **fonction d'autocorrélation**
$$
R_X(t_1, t_2) = \mathbb{E}\big[X(t_1)\,X^*(t_2)\big]
$$

## Stationnarité
> [!note] Stationnarité en moyenne d'ordre 2 (= au sens large, *WSS*)
> - $\mathbb{E}[x(t)] = m_x$ → **ne dépend pas de $t$**
> - $R_x(t_1, t_2) = R_x(t_1 - t_2)$ → ne dépend **que de l'écart** $\tau = t_1 - t_2$

## Définition (théorème de Wiener–Khinchin)
> [!note] Densité spectrale de puissance
> Pour $x(t)$ processus stochastique stationnaire en moyenne d'ordre 2 :
> $$S_x(f) = \mathcal{F}(R_x)(f) = \int_{\mathbb{R}} R_x(\tau)\,e^{-2i\pi f\tau}\,d\tau$$

## Propriétés
- $S_x(f)$ = **puissance par unité de fréquence** (W/Hz)
- Puissance totale : $P_x = \displaystyle\int_{\mathbb{R}} S_x(f)\,df$ $\ \ (= R_x(0))$
- $S_x(f) \ge 0$
- $x$ déterministe → $S_x(f) = |X(f)|^2$
- **Filtrage linéaire invariant** : $y = h * x \ \Rightarrow\ S_y(f) = |H(f)|^2\,S_x(f)$
- $\mathcal{F}^{-1}(S_x)(\tau) = R_x(\tau)$
- $x$ et $y$ **indépendants** (et centrés) : $S_{x+\lambda y}(f) = S_x(f) + |\lambda|^2 S_y(f)$

> [!info] Exemples classiques (utiles pour le [[TD3 - Corrélation et DSP|TD3]])
> - **Bruit blanc** $b \sim \mathcal{N}(0,\sigma^2)$ : $R_b(\tau) = \sigma^2\delta(\tau)$ ⟹ $S_b(f) = \sigma^2$ (**DSP plate**, d'où le nom « blanc » par analogie avec la lumière).
> - **Sinusoïde à phase aléatoire** $x(t) = A\cos(2\pi f_0 t + \phi)$, $\phi\sim\mathcal{U}[0,2\pi]$ : $R_x(\tau) = \frac{A^2}{2}\cos(2\pi f_0\tau)$ ⟹ $S_x(f) = \frac{A^2}{4}\big(\delta_{f_0}(f)+\delta_{-f_0}(f)\big)$.
> - **Signal + bruit indépendant** $y = x + b$ : $R_y = R_x + R_b$ et $S_y = S_x + \sigma^2$.

Voir : [[11 - Estimation de l'autocorrélation]], [[12 - Estimation de la densité spectrale de puissance]].
