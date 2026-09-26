---
tags: [TSN, fenêtrage, résolution, apodisation]
---
# Résolution spectrale et fenêtrage
Retour : [[00 - Sommaire TSN]] · Précédent : [[07 - Échantillonnage et théorème de Shannon-Nyquist]] · Suite : [[09 - Transformée de Fourier discrète]]

## Effet de la durée finie : fenêtre carrée
- Signal original : $e^{2i\pi f_0 t} \xrightarrow{\mathcal{F}} \delta_{f_0}(f)$ → une raie infiniment fine.
- Signal fenêtré (observé pendant $T$) :
$$
e^{2i\pi f_0 t}\,\Pi_{[-\frac T2;\frac T2]}(t) \xrightarrow{\ \mathcal{F}\ } \big(\delta_{f_0} * T\operatorname{sinc}(\pi f T)\big)(f) = T\operatorname{sinc}\big(\pi(f-f_0)T\big)
$$
- La raie devient un **sinc** centré en $f_0$ ; il s'annule pour $f - f_0 = k/T$, $k\in\mathbb{Z}^*$.

> [!important] Résolution spectrale
> $$\delta f \approx \frac{1}{T}$$
> Deux raies plus proches que $\sim 1/T$ ne peuvent **pas être séparées**. **Seule la durée d'observation $T$ améliore la résolution** (ni $F_e$, ni le zéro-padding).

## Fenêtres d'apodisation
Au lieu de couper brutalement (porte), on multiplie par une fenêtre $w$ qui descend doucement vers 0 aux bords :
$$
e^{2i\pi f_0 t}\,\Pi^{\text{Hann}}_{[-\frac T2;\frac T2]}(t) \xrightarrow{\ \mathcal{F}\ } \mathcal{F}\big(\Pi^{\text{Hann}}_{[-\frac T2;\frac T2]}\big)(f-f_0)
$$
- **Hann** : résolution $\approx 2/T$ (lobe plus large), mais lobes secondaires beaucoup plus bas.
- **Blackman** : résolution $> 2/T$, lobes secondaires encore plus bas.

## Comparaison des fenêtres usuelles

| Fenêtre | Largeur lobe principal | Bande passante à −3 dB | 1er lobe secondaire | Pente de décroissance |
|---|---|---|---|---|
| Rectangulaire | $2/T$ | $0{,}89/T$ | −13 dB | −6 dB/octave |
| Hann | $4/T$ | $1{,}44/T$ | −31 dB | −18 dB/octave |
| Hamming | $4/T$ | $1{,}30/T$ | −41 dB | −6 dB/octave |
| Blackman | $6/T$ | $1{,}64/T$ | −58 dB | −18 dB/octave |

> [!important] Le compromis fondamental
> **Largeur du lobe principal ⟷ niveau des lobes secondaires**
> = **résolution fréquentielle ⟷ fuite spectrale** (*spectral leakage*).
> - Rectangulaire : meilleure résolution, mais une raie forte « fuit » et peut masquer une raie faible voisine.
> - Blackman : raies faibles visibles (grande dynamique), mais raies proches confondues.
>
> Synonymes : **fenêtrage, apodisation, *tapering***.

> [!info] Complément : expressions discrètes ($n = 0,\dots,N-1$)
> - Rectangulaire : $w[n] = 1$
> - Hann : $w[n] = 0{,}5\left(1-\cos\frac{2\pi n}{N-1}\right)$
> - Hamming : $w[n] = 0{,}54 - 0{,}46\cos\frac{2\pi n}{N-1}$
> - Blackman : $w[n] = 0{,}42 - 0{,}5\cos\frac{2\pi n}{N-1} + 0{,}08\cos\frac{4\pi n}{N-1}$
>
> MATLAB : `rectwin(N)`, `hann(N)`, `hamming(N)`, `blackman(N)` (vecteurs colonnes → utiliser `.'` pour un signal ligne).

> [!tip] Lire les spectres en dB
> Les lobes secondaires (−13 dB, −31 dB…) ne sont visibles qu'en échelle logarithmique : `10*log10(abs(X).^2)` ou `20*log10(abs(X))`.

Voir aussi : [[12 - Estimation de la densité spectrale de puissance#Estimateurs pondérés (périodogramme fenêtré)]], [[09 - Transformée de Fourier discrète#Remplissage par zéros (zero-padding)]].
