---
tags: [TSN, bruit, quantification, gigue]
---
# Le bruit de numérisation
Retour : [[00 - Sommaire TSN]] · Précédent : [[09 - Transformée de Fourier discrète]] · Suite : [[11 - Estimation de l'autocorrélation]]

Toutes les imperfections de la chaîne de numérisation se traduisent par une **dégradation du rapport signal sur bruit (SNR)**.

## 1. Bruit d'échantillonnage : la gigue (*jitter*)
- **Cas idéal** : $x(t_n) = x(nT_e)$
- **Réalité** (instabilité de l'horloge) : $x(t_n) = x(nT_e + \varepsilon[n])$, avec $\varepsilon[n]\sim\mathcal{N}(0,\sigma_g^2)$
- Dégradation du SNR, **surtout aux fréquences élevées** (un signal qui varie vite est plus sensible à une erreur sur l'instant d'échantillonnage).

> [!info] Complément : pourquoi les hautes fréquences ?
> Au premier ordre, $x(nT_e+\varepsilon) \approx x(nT_e) + \varepsilon\,x'(nT_e)$. Pour $x = A\sin(2\pi f t)$, l'erreur a une amplitude $\propto 2\pi f A\,\sigma_g$, d'où
> $$\text{SNR}_{\text{gigue}} \approx -20\log_{10}(2\pi f\sigma_g) \ \text{dB}$$

## 2. Bruit de mesure
$$
\tilde x[n] = x[n] + b_{\text{mesure}}[n], \qquad b_{\text{mesure}}\sim\mathcal{N}(0,\sigma_m^2)
$$
(bruit thermique de l'électronique, etc.) → remonte le « plancher » du spectre, dégradation du SNR.

## 3. Bruit de quantification
$$
x_{\text{quant}}[n] = x[n] + b_{\text{quant}}[n], \qquad \mathbb{E}\big[b_{\text{quant}}[n]\big] = 0
$$
→ dégradation du SNR (cf. [[06 - Étapes de la numérisation#2. Quantification]]).

> [!info] Complément classique (quantification uniforme de pas $\Delta$)
> Si le signal « traverse » beaucoup de niveaux, l'erreur est à peu près uniforme sur $[-\frac\Delta2;\frac\Delta2]$ :
> $$\mathbb{E}[b_q] = 0, \qquad \sigma_q^2 = \frac{\Delta^2}{12}$$
> Pour une sinusoïde pleine échelle sur $n$ bits : $\text{SNR} \approx 6{,}02\,n + 1{,}76$ dB → **chaque bit supplémentaire gagne ≈ 6 dB**.

## 4. Modèle global
$$
x[n] = x(nT_e + \varepsilon[n]) + b[n], \qquad \mathbb{E}[b[n]] = 0
$$
où $b$ regroupe bruit de mesure et bruit de quantification.

> [!tip] Lien avec les TD
> C'est exactement le modèle $y = x + b$ du [[TD3 - Corrélation et DSP]] et de la question 4.1 du [[TD1 - Numérisation]] : un bruit blanc additif ajoute une constante $\sigma^2$ à la DSP.
