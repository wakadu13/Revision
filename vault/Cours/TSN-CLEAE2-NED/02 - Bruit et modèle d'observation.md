---
tags: [TSN, bruit, probabilités]
---
# Bruit et modèle d'observation
Retour : [[00 - Sommaire TSN]] · Précédent : [[01 - Introduction au traitement du signal numérique]] · Suite : [[03 - Classes de signaux]]

## Qu'est-ce qu'un bruit ?
> [!note] Définition (bruit)
> - Ce qui **n'est pas le signal** → ce qui ne porte pas l'information utile.
> - **Parasite** le signal.
> - Par nature **inconnu** et, dans une certaine mesure, **imprévisible**.

## Bruit additif blanc gaussien (BABG / AWGN)

### Modèle scalaire
$$
\underbrace{y[n]}_{\text{observation}} = \underbrace{s[n]}_{\text{signal utile}} + \underbrace{b[n]}_{\text{bruit}}, \qquad b[n] \sim \mathcal{N}(\mu, \sigma^2)
$$
$\mu$ et $\sigma^2$ peuvent être connus ou non.

### Modèle vectoriel
$$
\mathbf{y} = \mathbf{s} + \mathbf{b}, \qquad \mathbf{b} \sim \mathcal{N}(\mu \mathbf{1}_N,\ \sigma^2 \mathbf{I}_N)
$$
La covariance $\sigma^2 \mathbf{I}_N$ (diagonale) traduit que les échantillons de bruit sont **décorrélés** (bruit **blanc**) et de même variance.

> [!warning] On ne peut pas « soustraire le bruit »
> $b[n]$ étant inconnu, il est impossible de calculer $y[n] - b[n]$.

> [!tip] Idée : approche statistique
> On connaît le **comportement moyen** :
> $$\mathbb{E}[y[n]] = s[n] + \mu \qquad\text{(vectoriel : } \mathbb{E}[\mathbf{y}] = \mathbf{s} + \mu\mathbf{1}_N)$$
> → moyenner, estimer, filtrer plutôt que « retirer » le bruit.

## Origine de l'aléatoire dans les modèles
L'aléatoire peut se trouver dans **le bruit, le signal ET le modèle de mesure**.

| Incertitude **épistémique** (manque de connaissance) | Incertitude **aléatoire** (intrinsèque) |
|---|---|
| Erreurs de mesure : $\mathbf{y}\approx\mathbf{s} \to \mathbf{y} = \mathbf{s} + \mathbf{b}$ | Variabilité propre du système (non reproductible) |
| Méconnaissance du système / approximation : $\mathbf{y} = f(\mathbf{s}) + \mathbf{b}$, $f$ en partie inconnue | Physique quantique ; signal lui-même aléatoire : $\mathbf{s} \sim \mathcal{N}(\mathbf{m}_s, \mathbf{C}_s)$ |

## Pourquoi la loi normale est-elle omniprésente ?
> [!note] Théorème central limite (TCL)
> Soit $(X_i)_{i\in\mathbb{N}}$ des variables aléatoires réelles **i.i.d.**, de moyenne $\mu$ et de variance $\sigma^2 > 0$. Alors
> $$\sqrt{n}\,\frac{\overline{X}_n - \mu}{\sigma} \xrightarrow[n\to\infty]{\mathcal{L}} \mathcal{N}(0,1), \qquad \overline{X}_n = \frac{1}{n}\sum_{i=1}^n X_i.$$
> **La somme d'un grand nombre de variables indépendantes tend vers une loi normale.**

Le bruit physique (thermique, électronique…) résulte de la superposition de très nombreuses petites contributions indépendantes → gaussien.

Voir aussi : [[05 - Densité spectrale de puissance]] (bruit blanc = DSP constante), [[10 - Bruit de numérisation]].
