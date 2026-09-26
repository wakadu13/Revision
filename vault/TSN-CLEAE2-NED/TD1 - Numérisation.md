---
tags: [TSN, TD, numérisation]
---
# TD1 — Numérisation (énoncé + correction)
Retour : [[00 - Sommaire TSN]] · Cours : [[06 - Étapes de la numérisation]], [[07 - Échantillonnage et théorème de Shannon-Nyquist]], [[08 - Résolution spectrale et fenêtrage]]

> [!abstract] Objectif
> Voir l'effet de chaque étape de la numérisation d'un signal analogique sur son **spectre** :
> 1. **troncature** à une durée $T$ : $s(t)\,\Pi_{[-\frac T2;\frac T2]}(t)$
> 2. **échantillonnage** à pas $T_e$ : $s(t)\,\Pi_{[-\frac T2;\frac T2]}(t)\,\text{Ш}_{T_e}(t)$
> 3. **quantification** : $P_\Gamma\big(s\,\Pi_{[-\frac T2;\frac T2]}\,\text{Ш}_{T_e}\big)(t)$, modélisée par l'ajout d'un signal aléatoire.
>
> On admet que les intégrales existent (au sens des distributions) et qu'on peut intervertir somme et intégrale.

**Rappels** : $\int_{\mathbb{R}} x(t)\,\delta_{t_0}(t)\,dt = x(t_0)$ et $\int_{\mathbb{R}}x(t)\,\text{Ш}_{T_e}(t)\,dt = \sum_{n\in\mathbb{Z}}x(nT_e)$.

## 1 Questions préliminaires

> [!question] 1.1 Calculer les TF de $\delta(t)$ et $\delta_{t_0}(t)$ et les tracer.

> [!success]- Correction
> $$\mathcal{F}(\delta)(f) = \int_{\mathbb{R}}\delta(t)\,e^{-2i\pi ft}\,dt = e^{-2i\pi f\cdot 0} = 1$$
> $$\mathcal{F}(\delta_{t_0})(f) = \int_{\mathbb{R}}\delta(t-t_0)\,e^{-2i\pi ft}\,dt = \int_{\mathbb{R}}\delta(t)\,e^{-2i\pi f(t+t_0)}\,dt = e^{-2i\pi f t_0}$$
> **Tracés** : $|\mathcal{F}(\delta)| = |\mathcal{F}(\delta_{t_0})| = 1$ pour tout $f$ (spectre plat) ; la phase de $\mathcal{F}(\delta_{t_0})$ est linéaire, $-2\pi f t_0$. Un Dirac contient **toutes les fréquences**.

> [!question] 1.2 Calculer la TF de $\text{Ш}_{T_e}(t)$ et la tracer. On remarquera d'abord que $\text{Ш}_{T_e}$ est périodique et on calculera ses coefficients de Fourier.

> [!success]- Correction
> $\text{Ш}_{T_e}$ est $T_e$-périodique → série de Fourier $\text{Ш}_{T_e}(t) = \sum_{n}c_n e^{2i\pi\frac{n}{T_e}t}$ avec
> $$c_n = \frac{1}{T_e}\int_{-T_e/2}^{T_e/2}\text{Ш}_{T_e}(t)\,e^{-2i\pi\frac{n}{T_e}t}dt = \frac{1}{T_e}\int_{-T_e/2}^{T_e/2}\delta(t)\,e^{-2i\pi\frac{n}{T_e}t}dt = \frac{1}{T_e}$$
> (sur une période, seul le Dirac en 0 compte). Donc
> $$\mathcal{F}(\text{Ш}_{T_e})(f) = \sum_{n\in\mathbb{Z}}c_n\,\mathcal{F}\big(e^{2i\pi\frac{n}{T_e}t}\big)(f) = \frac{1}{T_e}\sum_{n\in\mathbb{Z}}\delta_{n/T_e}(f) = \frac{1}{T_e}\text{Ш}_{1/T_e}(f)$$
> **Un peigne de pas $T_e$ a pour TF un peigne de pas $1/T_e = F_e$ et de hauteur $1/T_e$.**
>
> *Remarque* (formule sommatoire de Poisson) : en calculant directement, $\mathcal{F}(\text{Ш}_{T_e})(f) = \sum_k e^{-2i\pi fkT_e}$, d'où $\sum_{k\in\mathbb{Z}}e^{-2i\pi fkT_e} = \frac{1}{T_e}\text{Ш}_{1/T_e}(f)$ (le signe de l'exponentielle est indifférent car on somme sur $k\in\mathbb{Z}$ ; la correction écrit $e^{+2i\pi\dots}$).

> [!question] 1.3 À quelles classes appartiennent : $s(t) = \cos(2\pi f_0 t)$, $e_{f_0}(t) = e^{2i\pi f_0 t}$, $\frac1T\Pi_{[-\frac T2;\frac T2]}(t)$ ($f_0\in\mathbb{R}$) ?

> [!success]- Correction
> - $s$ et $e_{f_0}$ : 1D, continus, déterministes, d'**énergie infinie** et de **puissance finie**, **périodiques** de période $1/f_0$ (puissance $\frac12$ et $1$).
> - $\frac1T\Pi_{[-\frac T2;\frac T2]}$ : 1D, continu, déterministe, d'**énergie finie** ($E = 1/T$).
>
> Voir [[03 - Classes de signaux]].

> [!question] 1.4 Tracer l'allure de ces signaux.

> [!success]- Correction
> - $\cos(2\pi f_0t)$ : sinusoïde réelle d'amplitude 1, période $1/f_0$.
> - $e_{f_0}(t)$ : complexe → tracer $\text{Re} = \cos(2\pi f_0t)$ et $\text{Im} = \sin(2\pi f_0t)$ (hélice dans l'espace $(t,\text{Re},\text{Im})$), module constant égal à 1.
> - $\frac1T\Pi$ : rectangle de hauteur $1/T$ sur $[-\frac T2;\frac T2]$, **d'aire 1**.
> ```matlab
> t = -1:1e-3:1; f0 = 3; T = 0.5;
> subplot(3,1,1); plot(t, cos(2*pi*f0*t));
> subplot(3,1,2); plot(t, real(exp(2i*pi*f0*t)), t, imag(exp(2i*pi*f0*t)));
> subplot(3,1,3); plot(t, (abs(t)<=T/2)/T);
> ```

> [!question] 1.5 Calculer et tracer leurs transformées de Fourier.

> [!success]- Correction
> $$\mathcal{F}(s)(f) = \mathcal{F}\!\left(\frac{e^{2i\pi f_0t}+e^{-2i\pi f_0t}}{2}\right)(f) = \frac{\delta_{f_0}(f) + \delta_{-f_0}(f)}{2}$$
> $$\mathcal{F}(e_{f_0})(f) = \delta_{f_0}(f)$$
> $$\mathcal{F}\!\left(\tfrac1T\Pi_{[-\frac T2;\frac T2]}\right)(f) = \frac1T\int_{-T/2}^{T/2}e^{-2i\pi ft}dt = \frac1T\,\frac{e^{i\pi fT}-e^{-i\pi fT}}{2i\pi f} = \frac{\sin(\pi fT)}{\pi fT} = \operatorname{sinc}(\pi fT)$$
> **Tracés** : deux raies de poids ½ en $\pm f_0$ ; une raie en $f_0$ ; un sinc de hauteur 1 en 0, lobe principal de largeur $2/T$.

## 2 Effet de la réduction du support temporel

> [!question] 2.1 Pour quelles fréquences $\mathcal{F}\big(\frac1T\Pi_{[-\frac T2;\frac T2]}\big)(f)$ est-elle nulle ?

> [!success]- Correction
> $\operatorname{sinc}(\pi fT) = 0 \iff \sin(\pi fT)=0$ et $f\neq0$ $\iff f = \dfrac{k}{T},\ k\in\mathbb{Z}^*$.

> [!question] 2.2 Calculer et tracer la TF de $s(t) = A_0\cos(2\pi f_0t)\,\frac1T\Pi_{[-\frac T2;\frac T2]}(t)$.

> [!success]- Correction
> Produit en temps → convolution en fréquence :
> $$\mathcal{F}(s)(f) = A_0\Big(\tfrac{\delta_{f_0}+\delta_{-f_0}}{2} * \operatorname{sinc}(\pi\,\cdot\,T)\Big)(f) = \frac{A_0}{2}\Big(\operatorname{sinc}\big(\pi(f+f_0)T\big) + \operatorname{sinc}\big(\pi(f-f_0)T\big)\Big)$$
> **Tracé** : deux sinc de hauteur $A_0/2$ centrés en $\pm f_0$.

> [!question] 2.3 Effet sur le spectre de la sélection de $[-\frac T2;\frac T2]$ ? En déduire la résolution spectrale.

> [!success]- Correction
> Le spectre est **convolué par $\operatorname{sinc}(\pi fT)$** : chaque raie est élargie en un sinc. Deux raies ne sont séparables que si elles sont distantes d'au moins ~ la demi-largeur du lobe principal :
> $$\text{résolution spectrale} = \frac1T$$
> → [[08 - Résolution spectrale et fenêtrage]]

## 3 Effet de l'échantillonnage

> [!question] 3.1 Calculer et tracer la TF de $s(t) = A_0\cos(2\pi f_0t)\,\Pi_{[-\frac T2;\frac T2]}(t)\,\text{Ш}_{T_e}(t)$.

> [!success]- Correction
> $$\mathcal{F}(s)(f) = \frac{A_0}{2}\Big(\operatorname{sinc}\big(\pi(f+f_0)T\big)+\operatorname{sinc}\big(\pi(f-f_0)T\big)\Big) * \frac{1}{T_e}\text{Ш}_{1/T_e}(f)$$
> $$= \frac{A_0}{2T_e}\sum_{k\in\mathbb{Z}}\Big[\operatorname{sinc}\big(\pi(f+f_0+kF_e)T\big)+\operatorname{sinc}\big(\pi(f-f_0+kF_e)T\big)\Big], \qquad F_e = \frac1{T_e}$$
> (la correction utilise la porte normalisée $\frac1T\Pi$ ; avec $\Pi$ seule il y aurait un facteur $T$ en plus.)
> **Tracé** : les deux sinc en $\pm f_0$ **recopiés tous les $F_e$**.

> [!question] 3.2 Effet sur le spectre de la sélection des échantillons à pas constant par $\text{Ш}_{T_e}$ ?

> [!success]- Correction
> Convolution du spectre par $\frac{1}{T_e}\text{Ш}_{1/T_e}(f)$, c'est-à-dire une **périodisation du spectre de période $F_e = 1/T_e$**.

> [!question] 3.3 Tracer le spectre dans le cas $2f_0 < \frac{1}{T_e}$ et dans le cas $2f_0 > \frac1{T_e}$. Comment appelle-t-on ce phénomène ?

> [!success]- Correction
> - **$2f_0 < F_e$** : sur $[-\frac{F_e}2;\frac{F_e}2]$ on ne voit que les deux lobes en $\pm f_0$ ; les répliques (en $\pm f_0 + kF_e$) restent en dehors → spectre fidèle.
> - **$2f_0 > F_e$** : $f_0 > F_e/2$, la réplique $-f_0 + F_e$ (et $f_0 - F_e$) **retombe dans $[-\frac{F_e}{2};\frac{F_e}{2}]$** ; on y observe des raies en $\pm(F_e - f_0)$ qui n'appartiennent pas au spectre initial.
>
> C'est le **repliement de spectre** (*aliasing*).

> [!question] 3.4 Quel peut être le problème ? Tracer un schéma pour expliquer la situation.

> [!success]- Correction
> Le spectre du signal est **corrompu** par la réplique : on mesure une sinusoïde à $F_e - f_0$ au lieu de $f_0$, et on ne peut plus distinguer les deux (ni reconstruire le signal).
> Schéma : axe des fréquences avec $-F_e/2$, $0$, $F_e/2$, $F_e$ ; placer $f_0 > F_e/2$ ; sa réplique $f_0 - F_e$ tombe dans $[-F_e/2;0]$ et celle de $-f_0$ dans $[0;F_e/2]$.
> Exemple numérique : $f_0 = 25$ Hz, $F_e = 30$ Hz → raie apparente à 5 Hz.

> [!question] 3.5 Pour un signal de support fréquentiel $[f_{\min};f_{\max}]$, comment choisir $T_e$ ou $F_e$ pour l'éviter ?

> [!success]- Correction
> Il faut
> $$F_e > 2f_{\max}$$
> où $f_{\max}$ est la fréquence maximale présente dans le signal : **théorème d'échantillonnage de Shannon-Nyquist**. En pratique on place un **filtre anti-repliement** avant l'échantillonneur.

## 4 Effet de la quantification

> [!question] 4.1 On considère un bruit blanc additif $b(t)\sim\mathcal{N}(0,\sigma^2)$, $y(t) = s(t)+b(t)$. Calculer la DSP de $y$ et la tracer.

> [!success]- Correction
> $s$ et $b$ indépendants, $b$ centré ⟹ $S_y = S_s + S_b$ avec $S_b(f)=\sigma^2$ (bruit blanc) et $S_s = |\mathcal{F}(s)|^2$ ($s$ déterministe) :
> $$S_y(f) = \frac{A_0^2}{4T_e^2}\left|\sum_{k\in\mathbb{Z}}\operatorname{sinc}\big(\pi(f+f_0+kF_e)T\big)+\operatorname{sinc}\big(\pi(f-f_0+kF_e)T\big)\right|^2 + \sigma^2$$
> **Tracé** (en dB de préférence) : les lobes en $\pm f_0$ (périodisés) posés sur un **plancher constant** à $\sigma^2$. Plus $\sigma^2$ est grand, plus les lobes secondaires puis les raies elles-mêmes sont noyés dans le bruit.
> → [[10 - Bruit de numérisation]]

> [!example]- Illustration MATLAB (bonus)
> ```matlab
> f0 = 25; T = 1;
> for Fe = [100 50 30]
>     t = 0:1/Fe:T-1/Fe; N = length(t);
>     x = cos(2*pi*10*t) + 0.7*cos(2*pi*f0*t);
>     X = fftshift(fft(x, 8*N))/N;              % zéro-padding pour lisser
>     f = ((0:8*N-1) - floor(8*N/2))*Fe/(8*N);
>     figure; plot(f, abs(X)); title(sprintf('Fe = %d Hz', Fe)); xlabel('f (Hz)');
> end
> ```
> À $F_e = 30$ Hz, le pic à 25 Hz apparaît à 5 Hz.
