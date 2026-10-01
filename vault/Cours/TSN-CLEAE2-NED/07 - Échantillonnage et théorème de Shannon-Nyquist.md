---
tags: [TSN, échantillonnage, shannon, repliement]
---
# Effet de l'échantillonnage — Théorème de Shannon-Nyquist
Retour : [[00 - Sommaire TSN]] · Précédent : [[06 - Étapes de la numérisation]] · Suite : [[08 - Résolution spectrale et fenêtrage]]

## Analyse théorique
**Outils** :
- Peigne de Dirac : $\text{Ш}_{T_e}(t) \xrightarrow{\ \mathcal{F}\ } \dfrac{1}{T_e}\text{Ш}_{1/T_e}(f)$
- Porte : $\Pi_{[-\frac T2;\frac T2]}(t) \xrightarrow{\ \mathcal{F}\ } T\operatorname{sinc}(\pi f T)$

**Échantillonnage à pas $T_e$ sur une durée $T$** (produit en temps → convolutions en fréquence) :
$$
x(t)\,\text{Ш}_{T_e}(t)\,\Pi_{[-\frac T2;\frac T2]}(t) \quad\xrightarrow{\ \mathcal{F}\ }\quad \left(\Big(X * \tfrac{1}{T_e}\text{Ш}_{1/T_e}\Big) * T\operatorname{sinc}(\pi f T)\right)(f)
$$

## Effet de l'échantillonnage : périodisation du spectre
Pour $T \gg 1$ (on néglige l'effet de la porte) :
$$
\Big(X * \frac{1}{T_e}\text{Ш}_{1/T_e}\Big)(f) = \frac{1}{T_e}\sum_{k\in\mathbb{Z}}(X*\delta_{k/T_e})(f) = \frac{1}{T_e}\sum_{k\in\mathbb{Z}} X\Big(f - \frac{k}{T_e}\Big)
$$
$$
= \dots + \underbrace{X(f+\tfrac{2}{T_e})}_{\text{réplique}} + \underbrace{X(f+\tfrac{1}{T_e})}_{\text{réplique}} + \underbrace{X(f)}_{\text{original}} + \underbrace{X(f-\tfrac{1}{T_e})}_{\text{réplique}} + \underbrace{X(f-\tfrac{2}{T_e})}_{\text{réplique}} + \dots
$$

> [!tip] À retenir
> **Échantillonner en temps (période $T_e$) ⟺ périodiser en fréquence (période $F_e = 1/T_e$).**
> Le spectre d'un signal numérique est donc **périodique de période $F_e$** : on ne l'étudie que sur $[-F_e/2 ; F_e/2]$.

## Repliement de spectre (*aliasing*)
Si les répliques **se chevauchent**, des composantes qui n'appartiennent pas au spectre original apparaissent dans $[-\frac{F_e}{2};\frac{F_e}{2}]$ : c'est le **repliement spectral**. Le spectre est **corrompu** et le signal ne peut plus être reconstruit.

> [!example] Exemples du cours : $s(t) = \cos(2\pi\cdot 10\,t) + 0.7\cos(2\pi\cdot 25\,t)$
> | $F_e$ | $F_e/2$ | Résultat |
> |---|---|---|
> | 100 Hz | 50 Hz | Raies à ±10 et ±25 Hz, répliques à ±75, ±90 Hz… **pas de repliement** |
> | 50 Hz | 25 Hz | 25 Hz est **pile à la limite** : la raie en +25 et la réplique de −25 (en −25+50 = +25) se superposent → cas limite |
> | 30 Hz | 15 Hz | 10 Hz OK ; **25 Hz se replie en 25 − 30 = −5 Hz** (et −25 en +5 Hz) → **fausse raie à 5 Hz** |
>
> Pour une **gaussienne** (support fréquentiel infini), il y a toujours un peu de repliement ; il est négligeable à 200 Hz et visible à 100 Hz.

> [!info] Complément : calculer une fréquence repliée
> Une sinusoïde de fréquence $f$ échantillonnée à $F_e$ apparaît à
> $$f_{\text{app}} = f - k F_e \quad\text{avec } k \text{ tel que } f_{\text{app}}\in\left[-\tfrac{F_e}{2};\tfrac{F_e}{2}\right]$$
> (pour un signal réel on lit $|f_{\text{app}}|$). Ex. : 25 Hz à $F_e = 30$ Hz → 5 Hz ; 25 Hz à $F_e=40$ Hz → 15 Hz.

## Théorème de Shannon-Nyquist
> [!important] Théorème (Shannon-Nyquist)
> Soit $x$ un signal à bande limitée $[f_{\min}; f_{\max}]$ échantillonné à la fréquence $F_e = 1/T_e$. Pour permettre une **reconstruction idéale** de $x$ après échantillonnage, il faut
> $$F_e \ge 2 f_{\max}$$
> (en pratique strictement $F_e > 2f_{\max}$ : une sinusoïde à exactement $F_e/2$ est ambiguë, cf. cas 50 Hz ci-dessus).
>
> $F_e/2$ est appelée **fréquence de Nyquist**.

## Filtre anti-repliement
Dans le [[06 - Étapes de la numérisation#Modèle de récepteur (homodyne)|récepteur]], le **filtre passe-bas avant l'échantillonneur** coupe tout ce qui dépasse $F_e/2$ : c'est le **filtre anti-repliement** (*anti-aliasing filter*). Il garantit l'hypothèse « bande limitée » du théorème, y compris pour le bruit.

Voir le calcul complet dans [[TD1 - Numérisation#3 Effet de l'échantillonnage]].
