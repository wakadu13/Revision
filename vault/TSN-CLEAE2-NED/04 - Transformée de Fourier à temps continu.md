---
tags: [TSN, rappels, fourier]
---
# Transformée de Fourier d'un signal à temps continu (rappel)
Retour : [[00 - Sommaire TSN]] · Précédent : [[03 - Classes de signaux]] · Suite : [[05 - Densité spectrale de puissance]]

## Définition
> [!note] TF pour les signaux d'énergie finie
> Avec $L^2_{\mathbb{C}} = \{x : t\mapsto x(t) \mid \int_{\mathbb{R}}|x(t)|^2dt < +\infty\}$ (« en faisant une petite entorse aux mathématiques ») :
> $$\mathcal{F} : L^2_{\mathbb{C}} \to L^2_{\mathbb{C}},\qquad X(f) = \mathcal{F}(x)(f) = \int_{\mathbb{R}} x(t)\,e^{-2i\pi f t}\,dt$$
> **TF inverse** :
> $$x(t) = \mathcal{F}^{-1}(X)(t) = \int_{\mathbb{R}} X(f)\,e^{2i\pi f t}\,df$$

## Parseval et Plancherel
> [!note] Égalité de Parseval (conservation du produit scalaire)
> $$\underbrace{\int_{\mathbb{R}} x(t)\,y^*(t)\,dt}_{\langle x, y\rangle} = \underbrace{\int_{\mathbb{R}} X(f)\,Y^*(f)\,df}_{\langle X, Y\rangle}$$

> [!note] Théorème de Plancherel (conservation de l'énergie)
> $$\underbrace{\int_{\mathbb{R}} |x(t)|^2\,dt}_{E_x} = \underbrace{\int_{\mathbb{R}} |X(f)|^2\,df}_{E_X}$$

## Spectres
- $|x(t)|^2$ → **puissance instantanée**
- $|X(f)|$ → **spectre d'amplitude**
- $|X(f)|^2$ → **densité spectrale d'énergie** (spectre de puissance)

## Propriétés démontrées en cours

### Modulation
Avec $e_{f_0}(t) = e^{2i\pi f_0 t}$ :
$$
\mathcal{F}(x\,e_{f_0})(f) = \int_{\mathbb{R}} x(t)\,e^{2i\pi f_0 t}e^{-2i\pi f t}dt = \int_{\mathbb{R}} x(t)\,e^{-2i\pi (f-f_0) t}dt = X(f - f_0)
$$
→ **décalage du spectre** de $f_0$ (exemple du cours : modulation à 15 Hz).

> [!warning] Modulation par un cosinus réel
> Les slides montrent aussi $x(t)\cos(2\pi f_0 t)$. Par Euler, $\cos(2\pi f_0 t) = \frac{e_{f_0}+e_{-f_0}}{2}$, donc
> $$\mathcal{F}\big(x(t)\cos(2\pi f_0 t)\big)(f) = \frac{X(f-f_0) + X(f+f_0)}{2}$$
> Le spectre est **dupliqué** en $\pm f_0$ avec amplitude divisée par 2 (et non simplement décalé).

### Retard
Avec $x_{t_0}(t) = x(t - t_0)$ :
$$
\mathcal{F}(x_{t_0})(f) = \int_{\mathbb{R}} x(t-t_0)e^{-2i\pi f t}dt = \int_{\mathbb{R}} x(t)e^{-2i\pi f (t+t_0)}dt = X(f)\,e^{-2i\pi f t_0}
$$
→ le module $|X(f)|$ est **inchangé**, seule la phase tourne. (On peut aussi écrire $x_{t_0} = x * \delta_{t_0}$ et utiliser la propriété de convolution.)

### Linéarité
$$
\mathcal{F}(x_1 + \lambda x_2)(f) = X_1(f) + \lambda X_2(f)
$$

### Produit de convolution
$$
(h * x)(t) = \int_{\mathbb{R}} h(\tau)\,x(t-\tau)\,d\tau \qquad\xrightarrow{\ \mathcal{F}\ }\qquad \mathcal{F}(h*x)(f) = H(f)\,X(f)
$$
(la slide écrit $dt$ : c'est bien $d\tau$.)

## Tableau des propriétés
| Propriété | Temps | Fréquence |
|---|---|---|
| Linéarité | $x_1 + \lambda x_2$ | $X_1 + \lambda X_2$ |
| Retard | $x(t-t_0)$ | $e^{-2i\pi f t_0}X(f)$ |
| Modulation | $e^{2i\pi f_0 t}x(t)$ | $X(f-f_0)$ |
| Contraction | $x(\alpha t)$ | $\frac{1}{\lvert\alpha\rvert}X\!\left(\frac{f}{\alpha}\right)$ |
| Convolution | $(h*x)(t)$ | $H(f)X(f)$ |
| Produit | $h(t)x(t)$ | $(H*X)(f)$ |
| Conjugaison | $x^*(t)$ | $X^*(-f)$ |
| Dérivation | $\frac{\partial x}{\partial t}(t)$ | $2i\pi f\,X(f)$ |
| Parseval | $\int x y^*$ | $\int X Y^*$ |
| Plancherel | $\int \lvert x\rvert^2$ | $\int \lvert X\rvert^2$ |
| **Signal réel** (symétrie hermitienne) | $x\in\mathbb{R}$ | $X(-f) = X^*(f)$ |

> [!tip] Dualité à retenir
> **Produit dans un domaine ⟺ convolution dans l'autre.** C'est LA propriété qui explique tous les effets de la numérisation : fenêtrage (produit par une porte → convolution par un sinc) et échantillonnage (produit par un peigne → convolution par un peigne = périodisation).

## TF à connaître (au sens des distributions)
> [!note] Distribution de Dirac
> $\delta$ est définie par $\int_{\mathbb{R}} x(t)\delta(t)\,dt = x(0)$ pour toute fonction $x$. On note $\delta_{t_0}(t) = \delta(t-t_0)$.

| Signal | $x(t)$ | $X(f)$ |
|---|---|---|
| Dirac | $\delta_{t_0}(t)$ | $e^{-2i\pi f t_0}$ (et $\mathcal{F}(\delta)=1$) |
| Sinusoïde complexe | $e^{2i\pi f_0 t}$ | $\delta_{f_0}(f)$ |
| Sinusoïde réelle | $\cos(2\pi f_0 t)$ | $\frac{\delta_{f_0}(f) + \delta_{-f_0}(f)}{2}$ |
| Porte | $\Pi_{[-\frac T2;\frac T2]}(t)$ | $T\,\operatorname{sinc}(\pi f T)$ |
| Peigne de Dirac | $\text{Ш}_{T_e}(t) = \sum_{n\in\mathbb{Z}}\delta_{nT_e}(t)$ | $\frac{1}{T_e}\text{Ш}_{1/T_e}(f)$ |

> [!info] Conventions
> - $\operatorname{sinc}(x) = \dfrac{\sin x}{x}$ (convention du cours : le $\pi$ est écrit explicitement).
> - La fonction porte est notée $\pi_{[-T/2;T/2]}$ dans les supports ; ici $\Pi$ pour ne pas la confondre avec la constante $\pi$.
> - Le peigne de Dirac est noté « $X_{T_e}$ » dans les PDF : c'est la lettre cyrillique **Ш** (« cha »).

## Cas des signaux périodiques
> [!note] Série de Fourier
> Pour $x$ périodique de période $T$ (de carré intégrable sur une période) :
> $$x(t) = \sum_{n\in\mathbb{Z}} c_n\,e^{2i\pi \frac{n}{T} t}, \qquad c_n = \frac{1}{T}\int_{-T/2}^{T/2} x(t)\,e^{-2i\pi\frac{n}{T}t}\,dt$$

> [!note] TF d'un signal périodique → **spectre de raies**
> $$X(f) = \mathcal{F}\Big(\sum_n c_n e_{n/T}\Big)(f) = \sum_n c_n\,\mathcal{F}(e_{n/T})(f) = \sum_{n\in\mathbb{Z}} c_n\,\delta_{n/T}(f)$$

Voir aussi : [[TD1 - Numérisation]] (calculs de TF du Dirac, du peigne, de la porte), [[09 - Transformée de Fourier discrète]].
