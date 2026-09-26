---
tags: [TSN, DFT, FFT, fourier]
---
# Transformée de Fourier discrète (DFT)
Retour : [[00 - Sommaire TSN]] · Précédent : [[08 - Résolution spectrale et fenêtrage]] · TD associé : [[TD2 - Transformée de Fourier discrète]] · Suite : [[10 - Bruit de numérisation]]

## Définitions
**Signal discret** : $\mathbf{x}\in\mathbb{C}^N$, $x[n] = x(t_0 + nT_e)$, avec $N = \left\lfloor \frac{T}{T_e}\right\rfloor + 1$.

> [!note] DFT (à court terme)
> $$\text{DFT}(\mathbf{x})[k] = X[k] = \sum_{n=0}^{N-1} x[n]\,e^{-2i\pi\frac{nk}{N}}, \qquad k = 0,\dots,N-1$$

> [!note] DFT inverse
> Pour $\mathbf{X}\in\mathbb{C}^N$, $X[k] = X\!\left(\frac{kF_e}{N}\right)$ :
> $$\text{IDFT}(\mathbf{X})[n] = \frac{1}{N}\sum_{k=0}^{N-1} X[k]\,e^{2i\pi\frac{kn}{N}}$$

**Effets sur le spectre** : le spectre n'est calculé qu'en $N$ points $X[0],\dots,X[N-1]$ → mauvaise interprétation / visualisation si $N$ est petit.

## Interprétation : changement de base
- Vecteurs de la **base de Fourier** : $\mathbf{e}_k = \big[1, e^{2i\pi\frac{k}{N}}, \dots, e^{2i\pi\frac{k(N-1)}{N}}\big]^T$
- $X[k] = \langle \mathbf{e}_k, \mathbf{x}\rangle = \mathbf{e}_k^H\mathbf{x}$ : la DFT est la **décomposition de $\mathbf{x}$ sur la base de Fourier**.
- Matriciellement : $\text{DFT}(\mathbf{x}) = \mathbf{F}_N\mathbf{x}$ et $\text{IDFT}(\mathbf{y}) = \frac{1}{N}\mathbf{F}_N^H\mathbf{y}$, avec $\mathbf{F}_N^H\mathbf{F}_N = N\,\mathbf{I}_N$.
- **Aucune information perdue** : on a seulement changé de représentation. Démonstrations dans [[TD2 - Transformée de Fourier discrète]].

## Correspondance de l'axe fréquentiel
L'indice $k$ correspond à la **fréquence normalisée** $\tilde f = k/N$ (sans unité), et à la **fréquence physique** $f = F_e\tilde f$ (Hz) :

| $k$ | $0$ | $1$ | $2$ | … | $N-1$ |
|---|---|---|---|---|---|
| $\tilde f$ | $0$ | $\frac1N$ | $\frac2N$ | … | $1-\frac1N$ |
| $f$ (Hz) | $0$ | $\frac{F_e}{N}$ | $\frac{2F_e}{N}$ | … | $F_e - \frac{F_e}{N}$ |

- **Fréquences positives** : indices $0,\dots,\left\lfloor\frac N2\right\rfloor$ → $0$ à $\frac{\lfloor N/2\rfloor F_e}{N}$
- **Fréquences négatives** : indices $\left\lfloor\frac N2\right\rfloor+1,\dots,N-1$ → $\frac{(\lfloor N/2\rfloor+1)F_e}{N},\dots,F_e-\frac{F_e}{N}$, qui représentent en réalité $-\frac{F_e}{2},\dots,-\frac{F_e}{N}$ (le spectre est $F_e$-périodique).
- ⟶ **`fftshift()`** pour réordonner : fréquences négatives à gauche, 0 au centre.

> [!tip] Pas de la grille fréquentielle
> $$\Delta f = \frac{F_e}{N} = \frac{1}{N T_e} \approx \frac{1}{T}$$

```matlab
% Axe fréquentiel physique, centré (valable pour N pair ou impair)
N  = length(x);
X  = fftshift(fft(x))/N;              % /N : correspondance avec la TF continue
f  = ((0:N-1) - floor(N/2))*Fe/N;     % Hz
plot(f, abs(X)); xlabel('Fréquence (Hz)');
```

Étapes de visualisation vues en cours : indices → fréquences normalisées → fréquences normalisées centrées → **fréquences physiques centrées** (la bonne représentation).

## Remplissage par zéros (zero-padding)
$$
\tilde{\mathbf{x}} = [\mathbf{x}, \mathbf{0}_N, \dots, \mathbf{0}_N] \quad(\text{longueur } N' = MN)
$$
- **Aucune information ajoutée** (puissance identique).
- DFT calculée sur $N' = MN$ points → **plus de fréquences échantillonnées** ; $M-1$ points ajoutés entre deux fréquences calculées précédemment (interpolation du spectre).

```matlab
M  = 3;
Np = length(x)*M;
X  = fftshift(fft(x,Np))/length(x);   % fft(x,Np) complète avec des zéros
df = Fe/Np;
f  = (-round(Np/2):round(Np/2)-1)*df; % code du cours (Np pair)
% version robuste : f = ((0:Np-1) - floor(Np/2))*df;
```

> [!important] Le remplissage par zéros ne modifie PAS la résolution du spectre
> Il rend la courbe plus lisse (on voit mieux la forme du sinc et la position des pics), mais deux raies distantes de moins de $\sim 1/T$ restent confondues. La résolution dépend uniquement de la **durée d'observation $T$** ([[08 - Résolution spectrale et fenêtrage]]).

## Propriétés de la DFT
Les indices sont pris **modulo $N$** (tout est circulaire, voir plus bas).

| Propriété | Temps | Fréquence |
|---|---|---|
| Linéarité | $x_1 + \lambda x_2$ | $X_1 + \lambda X_2$ |
| Retard (circulaire) | $x[n-n_0]$ | $e^{-2i\pi\frac{n_0 k}{N}}X[k]$ |
| Modulation | $e^{2i\pi\frac{k_0 n}{N}}x[n]$ | $X[k-k_0]$ |
| Convolution circulaire | $(h\circledast x)[n]$ | $H[k]X[k]$ |
| Produit | $h[n]x[n]$ | $\frac1N(\hat{h}\circledast\hat{x})[k]$ |
| Conjugaison | $x^*[n]$ | $X^*[N-k]$ |
| Parseval | $\mathbf{x}^H\mathbf{y}$ | $\frac1N\hat{\mathbf{x}}^H\hat{\mathbf{y}}$ |
| Plancherel | $\sum_{n=0}^{N-1}\lvert x[n]\rvert^2$ | $\frac1N\sum_{k=0}^{N-1}\lvert X[k]\rvert^2$ |
| Signal réel | $x\in\mathbb{R}^N$ | $X[N-k] = X^*[k]$ |

> [!warning] Différences avec la slide « Propriétés de la DFT »
> Avec la convention du cours (DFT sans normalisation, IDFT en $1/N$), les facteurs **$1/N$** apparaissent pour le produit, Parseval et Plancherel (la slide les omet ou les place mal, et fait aller les sommes jusqu'à $N$ au lieu de $N-1$). Vérification rapide sous MATLAB : `sum(abs(x).^2)` vs `sum(abs(fft(x)).^2)/length(x)`.
> La slide mentionne aussi une propriété de « contraction » $x[\alpha n] \to \frac{1}{|\alpha|}\hat x[k/\alpha]$ : elle n'a pas de sens général en discret (indices non entiers) ; ne pas l'utiliser telle quelle.

## Convolution circulaire
- **Échantillonner les fréquences** lors de la DFT ⟶ **périodisation de $\mathbf{x}$** (période $N$) : dualité avec [[07 - Échantillonnage et théorème de Shannon-Nyquist|l'échantillonnage temporel]].
- Avec $\odot$ le produit terme à terme :
$$
\text{IDFT}(\hat{\mathbf{h}}\odot\hat{\mathbf{x}})[n] = \sum_{m=0}^{N-1} h[m]\,x[(n-m) \bmod N] = (\mathbf{h}\circledast\mathbf{x})[n] \ \neq\ (\mathbf{h}*\mathbf{x})[n] \text{ en général}
$$
⟶ c'est une convolution avec une **version périodisée de $\mathbf{x}$**.
- **Complétion par zéros** pour retrouver la convolution linéaire : si $\mathbf{h}$ a $L$ points et $\mathbf{x}$ en a $N$, compléter les deux à $N' \ge N + L - 1$ :

```matlab
Np = length(x) + length(h) - 1;
y  = ifft(fft(x,Np).*fft(h,Np));   % == conv(x,h)
```

## MATLAB : l'essentiel
| Fonction | Rôle |
|---|---|
| `fft(x)` / `fft(x,Np)` | DFT (algorithme rapide FFT, $O(N\log N)$), avec zéro-padding éventuel |
| `ifft(X)` | DFT inverse (inclut le $1/N$) |
| `fftshift(X)` | centre le spectre (0 Hz au milieu) |
| `abs(X)`, `abs(X).^2` | spectre d'amplitude, de puissance |

> [!warning] Normalisation de `fft`
> MATLAB `fft` calcule exactement $\mathbf{F}_N\mathbf{x}$ (aucun facteur). L'énoncé du TD indique « $\sqrt{N}\mathbf{F}_N\mathbf{x}$ » : c'est inexact (la version unitaire serait $\mathbf{F}_N\mathbf{x}/\sqrt N$). C'est pour cela qu'on divise par $N$ pour retrouver les amplitudes : un cosinus d'amplitude $A$ donne deux pics de hauteur $A/2$ dans `abs(fft(x))/N`.
