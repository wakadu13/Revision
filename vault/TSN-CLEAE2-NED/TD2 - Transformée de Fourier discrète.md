---
tags: [TSN, TD, DFT, algèbre-linéaire, matlab]
---
# TD2 — Transformée de Fourier discrète (énoncé + correction)
Retour : [[00 - Sommaire TSN]] · Cours : [[09 - Transformée de Fourier discrète]]

## 1 Rappels

### 1.1 Vecteurs et matrices
- Une **matrice** est un tableau de nombres, ex. $\mathbf{A} = \begin{bmatrix}1&4&8\\7&2&1\end{bmatrix}$ ; $\mathbf{A}[1,2] = 4$ (ligne 1, colonne 2).
- $\mathbb{R}^{N\times M}$ / $\mathbb{C}^{N\times M}$ : matrices $N$ lignes × $M$ colonnes à coefficients réels / complexes.
- Un **vecteur** = « matrice à une dimension », ex. $\mathbf{v} = [2,3,5]^T$ ($^T$ = transposée).
- Pour un vecteur complexe $\mathbf{x} = [5+3i,\ 2-i]^T$ : conjugué $\mathbf{x}^*$ et **transposé conjugué** $\mathbf{x}^H = (\mathbf{x}^*)^T = [5-3i,\ 2+i]$.

### 1.2 Décomposition sur une base
> [!note] Base
> Une base de $\mathbb{C}^N$ est un ensemble ordonné $(\mathbf{u}_1,\dots,\mathbf{u}_N)$ qui permet d'écrire **de manière unique** tout vecteur $\mathbf{x} = \sum_{k=1}^N\alpha_k\mathbf{u}_k$ ; $[\alpha_1,\dots,\alpha_N]^T$ est la **décomposition** de $\mathbf{x}$ sur cette base.

- **Base canonique** de $\mathbb{C}^3$ : $\mathbf{u}_1 = [1,0,0]^T$, $\mathbf{u}_2 = [0,1,0]^T$, $\mathbf{u}_3=[0,0,1]^T$ → $\mathbf{v} = v_1\mathbf{u}_1+v_2\mathbf{u}_2+v_3\mathbf{u}_3$.
- **Autre base** : $\mathbf{h}_1 = [1,0,1]^T$, $\mathbf{h}_2 = [0,1,0]^T$, $\mathbf{h}_3 = [1,0,-1]^T$ → $\mathbf{v} = \lambda_1\mathbf{h}_1+\lambda_2\mathbf{h}_2+\lambda_3\mathbf{h}_3$.
- Exemple : $[1,2,3]$ sur $(\mathbf{u})$ ⟷ $[2,2,-1]$ sur $(\mathbf{h})$, car $2\mathbf{h}_1+2\mathbf{h}_2-\mathbf{h}_3 = [1,2,3]^T$.

**Même vecteur, plusieurs représentations** selon la base : c'est exactement ce que fait la DFT.

> [!question] 1.1 $\mathbf{v}_1$ se décompose en $[4,6,-4]$ sur $(\mathbf{u})$. Décomposition sur $(\mathbf{h})$ ?

> [!success]- Correction
> On cherche $\lambda$ tel que $\lambda_1\mathbf{h}_1+\lambda_2\mathbf{h}_2+\lambda_3\mathbf{h}_3 = [\lambda_1+\lambda_3,\ \lambda_2,\ \lambda_1-\lambda_3]^T = [4,6,-4]^T$
> ⟹ $\lambda_2 = 6$, $\lambda_1+\lambda_3 = 4$, $\lambda_1-\lambda_3 = -4$ ⟹ $\lambda_1 = 0$, $\lambda_3 = 4$.
> $$\boxed{[0,\ 6,\ 4]}$$
> Vérification : $0\cdot\mathbf{h}_1 + 6\mathbf{h}_2 + 4\mathbf{h}_3 = [4,6,-4]^T$ ✓

> [!warning] Coquille dans la correction distribuée
> La correction indique $[0,6,8]$, ce qui donnerait $[8,6,-8]^T$. La bonne réponse est $[0,6,4]$ (cohérente avec la formule générale de la question 1.3).

> [!question] 1.2 $\mathbf{v}_2$ se décompose en $[2,-1,8]$ sur $(\mathbf{h})$. Décomposition sur $(\mathbf{u})$ ?

> [!success]- Correction
> $2\mathbf{h}_1 - \mathbf{h}_2 + 8\mathbf{h}_3 = [2+8,\ -1,\ 2-8]^T$
> $$\boxed{[10,\ -1,\ -6]}$$

> [!question] 1.3 Cas général : si $\mathbf{v}$ se décompose en $[v_1,v_2,v_3]$ sur $(\mathbf{u})$, quelle est sa décomposition sur $(\mathbf{h})$ ?

> [!success]- Correction
> En résolvant $\lambda_1+\lambda_3 = v_1$, $\lambda_2 = v_2$, $\lambda_1-\lambda_3 = v_3$ :
> $$\mathbf{v} = \frac{v_1+v_3}{2}\mathbf{h}_1 + v_2\mathbf{h}_2 + \frac{v_1-v_3}{2}\mathbf{h}_3$$

Sur $\mathbb{C}^N$ on utilise généralement la base canonique ; une autre représentation très utile est la **base de Fourier**.

## 2 La transformée de Fourier discrète

### 2.1 Définitions et propriétés
Vecteurs de la base de Fourier ($k = 0,\dots,N-1$) :
$$
\mathbf{e}_k = \begin{bmatrix}1\\ e^{2i\pi\frac{k}{N}}\\ \vdots\\ e^{2i\pi\frac{kn}{N}}\\ \vdots\\ e^{2i\pi\frac{k(N-1)}{N}}\end{bmatrix}, \qquad \mathbf{F}_N = \begin{bmatrix}\mathbf{e}_0^H\\ \mathbf{e}_1^H\\ \vdots\\ \mathbf{e}_{N-1}^H\end{bmatrix}
$$
$$
\text{DFT}(\mathbf{x}) = \mathbf{F}_N\mathbf{x} = \begin{bmatrix}\langle\mathbf{e}_0,\mathbf{x}\rangle\\ \vdots\\ \langle\mathbf{e}_{N-1},\mathbf{x}\rangle\end{bmatrix}, \quad \langle\mathbf{e}_k,\mathbf{x}\rangle = \mathbf{e}_k^H\mathbf{x} \quad\Longrightarrow\quad \text{DFT}(\mathbf{x})[k] = \sum_{n=0}^{N-1}x[n]\,e^{-2i\pi\frac{kn}{N}}
$$
- $\hat{\mathbf{x}} = \text{DFT}(\mathbf{x})$ est la **décomposition de $\mathbf{x}$ sur la base de Fourier**.
- Inverse : $\text{IDFT}(\mathbf{y}) = \frac1N\mathbf{F}_N^H\mathbf{y}$, et $\text{IDFT}(\text{DFT}(\mathbf{x})) = \mathbf{x}$.
- **Aucune information perdue** : on a seulement changé de représentation.

### 2.2 Démonstrations
Pour montrer que les $\mathbf{e}_k$ forment une base de $\mathbb{C}^N$, il suffit de montrer que ce sont $N$ vecteurs **orthogonaux deux à deux**.

> [!question] 2.1 Vérifier l'orthogonalité : $\langle\mathbf{e}_k,\mathbf{e}_l\rangle = 0$ pour $k\neq l$.

> [!success]- Correction
> Pour $k\neq k'$ (avec $0<|k'-k|<N$, donc $e^{2i\pi\frac{k'-k}{N}}\neq1$), somme géométrique de raison $q = e^{2i\pi\frac{k'-k}{N}}$ :
> $$\langle\mathbf{e}_k,\mathbf{e}_{k'}\rangle = \sum_{n=0}^{N-1}e^{-2i\pi\frac{kn}{N}}e^{2i\pi\frac{k'n}{N}} = \sum_{n=0}^{N-1}q^n = \frac{1-q^N}{1-q} = \frac{1-e^{2i\pi(k'-k)}}{1-e^{2i\pi\frac{k'-k}{N}}} = \frac{1-1}{1-q} = 0$$

> [!question] 2.2 Calculer la norme $\|\mathbf{e}_k\| = \sqrt{\langle\mathbf{e}_k,\mathbf{e}_k\rangle}$.

> [!success]- Correction
> $$\|\mathbf{e}_k\| = \sqrt{\sum_{n=0}^{N-1}e^{-2i\pi\frac{kn}{N}}e^{2i\pi\frac{kn}{N}}} = \sqrt{\sum_{n=0}^{N-1}1} = \sqrt N$$
> La base est **orthogonale** mais pas orthonormée (d'où le $\frac1N$ dans l'IDFT).

> [!question] 2.3 Exprimer $\mathbf{F}_N^H\mathbf{F}_N$ en fonction de $\mathbf{e}_k$ et $\mathbf{e}_{k'}$.

> [!success]- Correction
> $$(\mathbf{F}_N^H\mathbf{F}_N)_{k,k'} = \langle\mathbf{e}_k,\mathbf{e}_{k'}\rangle$$
> (les colonnes de $\mathbf{F}_N^H$ sont les $\mathbf{e}_k$.)

> [!question] 2.4 Montrer que $\text{IDFT}(\text{DFT}(\mathbf{x})) = \mathbf{x}$.

> [!success]- Correction
> $$\text{IDFT}(\text{DFT}(\mathbf{x})) = \frac1N\mathbf{F}_N^H\mathbf{F}_N\mathbf{x}$$
> avec $(\mathbf{F}_N^H\mathbf{F}_N)_{k,k'} = 0$ si $k\neq k'$ (Q2.1) et $= N$ si $k=k'$ (Q2.2). Donc $\mathbf{F}_N^H\mathbf{F}_N = N\mathbf{I}_N$ et
> $$\text{IDFT}(\text{DFT}(\mathbf{x})) = \mathbf{I}_N\mathbf{x} = \mathbf{x}$$

## 3 Illustrations (MATLAB)

> [!question] 3.1 Sur une même figure, afficher les 4 premiers vecteurs de la base de Fourier (partie réelle seulement, car $|\mathbf{e}_k[n]| = 1$).

> [!success]- Correction
> ```matlab
> N = 2^10;
> n = 0:N-1;
> figure(); hold on;
> for k = 0:3
>     plot(cos(2*pi*k*n/N));   % Re(e_k[n]) ; la correction écrit cos(-2*pi*k*n/N), identique (cos pair)
> end
> hold off; legend(string(0:3));
> ```
> Vérification (doit donner la même figure) :
> ```matlab
> figure();
> v = zeros(1,N); v(1) = 1;
> plot(real(ifft(v))*N); hold on;       % k = 0
> for i = 2:4
>     v = zeros(1,N); v(i) = 1;
>     plot(real(ifft(v))*N);            % k = 1,2,3
> end
> hold off; legend(string(0:3));
> ```
> **Pourquoi ?** L'IDFT d'un vecteur canonique (un seul 1 en position $k$) vaut $\frac1N\mathbf{e}_k$ : `ifft(v)*N` redonne donc exactement le $k$-ième vecteur de Fourier. $\mathbf{e}_0$ est constant, $\mathbf{e}_1$ fait 1 oscillation sur $N$ points, $\mathbf{e}_2$ en fait 2, etc.

**La DFT décompose un vecteur sur une base de signaux oscillants à fréquence constante.**

```matlab
N = 100; n = 1:N;
x = cos(2*pi*(5/N)*n);
figure();
subplot(1,2,1); plot(x); title('x');
subplot(1,2,2); plot(abs(fft(x)/N));   % /N : correspondance avec la TF continue
title('DFT(x)');
```
Seuls **deux coefficients sont non nuls** car, par Euler (pour $N=100$) :
$$x = \cos(2\pi 5n/N) = \frac{e^{i\frac{2\pi}{N}5n}+e^{-i\frac{2\pi}{N}5n}}{2} = \frac12\mathbf{e}_5[n] + \frac12\mathbf{e}_{95}[n]$$
($e^{-i\frac{2\pi}{N}5n} = e^{i\frac{2\pi}{N}95n}$ : l'indice 95 représente la fréquence $-5$.)

- $|\text{DFT}(\mathbf{x})|$ : **spectre d'amplitude** ; $|\text{DFT}(\mathbf{x})|^2$ : **spectre de puissance**.
- `fft()` calcule la DFT efficacement (un des algorithmes les plus utilisés au monde) ; son inverse est `ifft()`.

> [!warning] Normalisation
> L'énoncé indique que `fft()` calcule $\sqrt N\mathbf{F}_N\mathbf{x}$ : en réalité `fft(x)` $= \mathbf{F}_N\mathbf{x}$ exactement (voir [[09 - Transformée de Fourier discrète#MATLAB : l'essentiel]]).

> [!note] Numérotation
> L'énoncé passe directement de la question 3.1 à la 3.5 (pas de questions 3.2–3.4).

> [!question] 3.5 Définir et afficher un vecteur (par exemple somme de deux sinusoïdes).

> [!success]- Correction
> ```matlab
> Fe = 500; Te = 1/Fe; T = 1;
> t  = 0:Te:T-Te;
> f1 = 10; f2 = 25; A1 = 1; A2 = 0.7;
> x  = A1*cos(2*pi*f1*t) + A2*cos(2*pi*f2*t);
> figure(); plot(t, x); xlabel('Temps (s)');
> ```

> [!question] 3.6 Calculer la DFT avec `fft()` et afficher $|\text{DFT}(\mathbf{x})|/N$.

> [!success]- Correction
> ```matlab
> figure(); plot(abs(fft(x)/length(x)));
> ```
> 4 pics : indices 11 et 26 (fréquences 10 et 25 Hz, hauteurs 0,5 et 0,35 = $A/2$) et leurs symétriques aux indices $N-9$ et $N-24$ (fréquences négatives). Ici $N = 500$, $\Delta f = F_e/N = 1$ Hz, donc l'indice MATLAB $k+1$ ⟷ $k$ Hz.

> [!question] 3.7 Afficher la version centrée (`fftshift`).

> [!success]- Correction
> ```matlab
> N = length(x);
> f = ((0:N-1) - floor(N/2))*Fe/N;          % axe en Hz (bonus)
> figure(); plot(f, abs(fftshift(fft(x)/N))); xlabel('Fréquence (Hz)');
> ```
> On affiche **toujours** la version centrée : plus directement interprétable, et les signaux naturels contiennent surtout des basses fréquences (au centre).

> [!question] 3.8 Inverser la DFT et vérifier qu'on retrouve $\mathbf{x}$ via l'erreur quadratique $\sum_n|\text{IDFT}(\text{DFT}(\mathbf{x}))[n]-x[n]|^2$.

> [!success]- Correction
> ```matlab
> sum(abs(ifft(fft(x)) - x).^2)
> ```
> Résultat de l'ordre de $10^{-28}$–$10^{-30}$ : zéro à la **précision machine** près (erreurs d'arrondi en double précision).
