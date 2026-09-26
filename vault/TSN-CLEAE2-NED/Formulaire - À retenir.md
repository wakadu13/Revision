---
tags: [TSN, formulaire, révision]
---
# Formulaire — À retenir
Retour : [[00 - Sommaire TSN]]

## Fourier continu → [[04 - Transformée de Fourier à temps continu]]
| | |
|---|---|
| TF | $X(f) = \int x(t)e^{-2i\pi ft}dt$ ; $x(t) = \int X(f)e^{2i\pi ft}df$ |
| Plancherel | $\int\lvert x\rvert^2dt = \int\lvert X\rvert^2df$ |
| Retard | $x(t-t_0)\to e^{-2i\pi ft_0}X(f)$ |
| Modulation | $e^{2i\pi f_0t}x(t)\to X(f-f_0)$ |
| Convolution / produit | $h*x\to HX$ ; $hx\to H*X$ |
| Signal réel | $X(-f) = X^*(f)$ |
| $\delta_{t_0}$ | $e^{-2i\pi ft_0}$ |
| $e^{2i\pi f_0t}$ / $\cos(2\pi f_0t)$ | $\delta_{f_0}$ / $\frac12(\delta_{f_0}+\delta_{-f_0})$ |
| Porte $\Pi_{[-T/2;T/2]}$ | $T\operatorname{sinc}(\pi fT)$, nulle en $f = k/T$ |
| Peigne $\text{Ш}_{T_e}$ | $\frac1{T_e}\text{Ш}_{1/T_e}$ |

## Numérisation → [[06 - Étapes de la numérisation]]
$$P_\Gamma\big(s\cdot\Pi_{[-T/2;T/2]}\cdot\text{Ш}_{T_e}\big)$$
| Opération (temps) | Effet (fréquence) |
|---|---|
| Troncature (durée $T$) | convolution par sinc → **résolution $1/T$** |
| Échantillonnage ($T_e$) | **périodisation** de période $F_e = 1/T_e$ |
| Quantification ($n$ bits, pas $\Delta$) | bruit additif, $\sigma_q^2 = \Delta^2/12$, ≈ 6 dB/bit |

- **Shannon-Nyquist** : $F_e > 2f_{\max}$ ; sinon **repliement** (fréquence apparente $f - kF_e \in [-F_e/2;F_e/2]$).
- **Filtre anti-repliement** : passe-bas avant l'échantillonneur.
- $N = \lfloor T/T_e\rfloor + 1$.

## Fenêtres → [[08 - Résolution spectrale et fenêtrage]]
| Fenêtre | Lobe principal | 1er lobe sec. |
|---|---|---|
| Rectangulaire | $2/T$ | −13 dB |
| Hann | $4/T$ | −31 dB |
| Hamming | $4/T$ | −41 dB |
| Blackman | $6/T$ | −58 dB |
Compromis : **résolution ⟷ fuite spectrale**.

## DFT → [[09 - Transformée de Fourier discrète]]
$$X[k] = \sum_{n=0}^{N-1}x[n]e^{-2i\pi\frac{nk}{N}} \qquad x[n] = \frac1N\sum_{k=0}^{N-1}X[k]e^{2i\pi\frac{nk}{N}}$$
- $X[k] = \langle\mathbf{e}_k,\mathbf{x}\rangle$, $\langle\mathbf{e}_k,\mathbf{e}_l\rangle = N\delta_{kl}$, $\mathbf{F}_N^H\mathbf{F}_N = N\mathbf{I}_N$
- Indice $k$ ⟷ $f = kF_e/N$ ; pas $\Delta f = F_e/N$ ; `fftshift` pour centrer
- Plancherel : $\sum\lvert x[n]\rvert^2 = \frac1N\sum\lvert X[k]\rvert^2$
- Réel : $X[N-k] = X^*[k]$
- `abs(fft(x))/N` : un cosinus d'amplitude $A$ → deux pics de $A/2$
- **Zéro-padding** : interpole le spectre, **n'améliore pas la résolution**
- Produit de DFT = **convolution circulaire** ; compléter à $N_x + N_h - 1$ pour la convolution linéaire

## Aléatoire → [[05 - Densité spectrale de puissance]]
- Stationnarité ordre 2 : $\mathbb{E}[x(t)] = m_x$, $R_x(t_1,t_2) = R_x(t_1-t_2)$
- Wiener–Khinchin : $S_x = \mathcal{F}(R_x)$ ; $P_x = \int S_x = R_x(0)$
- Filtrage : $S_y = \lvert H\rvert^2S_x$
- Bruit blanc : $R_b = \sigma^2\delta$, $S_b = \sigma^2$
- $A\cos(2\pi f_0t+\phi)$ : $R = \frac{A^2}{2}\cos(2\pi f_0\tau)$
- Indépendants : $S_{x+\lambda y} = S_x + \lvert\lambda\rvert^2S_y$

## Estimation → [[11 - Estimation de l'autocorrélation]] · [[12 - Estimation de la densité spectrale de puissance]]
| Estimateur | Formule | Propriétés |
|---|---|---|
| $\hat R$ biaisé | $\frac1N\sum_{k=n}^{N-1}x[k]x^*[k-n]$ | $\mathbb{E} = \frac{N-\lvert n\rvert}{N}R$, faible variance, **EQM plus faible** |
| $\hat R$ non biaisé | $\frac1{N-n}\sum_{k=n}^{N-1}x[k]x^*[k-n]$ | sans biais, variance forte aux grands retards |
| Corrélogramme | $\text{DFT}(\hat R)$ | = périodogramme si $\hat R$ biaisé |
| Périodogramme | $\frac1N\lvert\text{DFT}(x)\rvert^2$ | biaisé ($S*W$), **non consistant** |
| Pondéré | $\frac1N\lvert\text{DFT}(x\odot w)\rvert^2$ | moins de fuite, toujours non consistant |
| Bartlett | moyenne de $J$ périodogrammes disjoints | variance $\div J$, résolution $\sim F_e/M$ |
| Welch | segments **chevauchants** fenêtrés | variance $\div J'$ ($J'>J$), le standard |

$$\text{EQM}(\hat\theta) = \text{Var}(\hat\theta) + \text{biais}^2(\hat\theta)$$

## MATLAB
| Besoin | Commande |
|---|---|
| Axe temps | `t = 0:1/Fe:T-1/Fe;` |
| Bruit blanc $\mathcal N(0,\sigma^2)$ | `sigma*randn(1,N)` |
| Spectre centré | `fftshift(fft(x))/N` |
| Axe fréquence | `f = ((0:N-1)-floor(N/2))*Fe/N;` |
| Zéro-padding | `fft(x, Np)` |
| Autocorrélation | `[R,lags] = xcorr(x,'biased'/'unbiased'); tau = lags/Fe;` |
| Welch | `pwelch(x, hann(M), M/2, nfft, Fe, 'centered')` |
| Fenêtres | `rectwin`, `hann`, `hamming`, `blackman` |
| dB | `10*log10(P)` (puissance), `20*log10(abs(X))` (amplitude) |
| Filtrage | `filter(b,a,x)`, `conv(x,h)` |

## Les 5 idées à ne jamais oublier
1. **Produit en temps ⟺ convolution en fréquence** (et réciproquement).
2. **Échantillonner ⟹ périodiser le spectre** ; $F_e > 2f_{\max}$.
3. **Résolution = $1/T$** : seule la durée d'observation l'améliore.
4. **Fenêtrer = compromis résolution / fuite** ; **moyenner (Welch) = compromis résolution / variance**.
5. **Le bruit blanc** = pic en 0 dans l'autocorrélation, plancher plat $\sigma^2$ dans la DSP.
