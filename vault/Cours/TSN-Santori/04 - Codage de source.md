---
tags: [telecom, NED, codage-source, entropie, huffman, shannon]
---
# Le codage de source
Retour : [[00 - Sommaire TSN-CLEAE2-NED]] · Précédent : [[03 - Modulations numériques]] · Suite : [[05 - Codage de canal]]

## Objectifs du cours

- Montrer l'intérêt du codage de source.
- Définir la notion d'entropie.
- Énoncer les théorèmes de Shannon.
- Donner les caractéristiques des codes en bloc et des codes de longueur variable.

## Plan et périmètre

1. Introduction sur la compression
2. Éléments de la théorie de l'information
3. Codage de source sans perte
   1. Codes à mots de longueur fixe
   2. Codes à mots de longueur variable

> [!tip] Position dans la chaîne
> - **Codage source** : élimination de la redondance inutile (compression).
> - **Codage canal** : augmenter la fiabilité par ajout de redondance utile (voir [[05 - Codage de canal]]).
> - **Codage en ligne** (mise en forme + modulation) : associe un support physique aux éléments binaires.

## Introduction sur la compression

Dans une image naturelle (par opposition à une mire artificielle), la corrélation entre pixels voisins est très élevée. Idée de base de la compression : **décorréler** l'information pour éviter de coder deux fois la même chose.

### Types de corrélation

| Type | Description |
|---|---|
| Spatiale | Entre échantillons voisins |
| Spectrale | Entre plans de couleur (ex : RGB → YUV/YIQ/YDbDr/YCbCr...), entre bandes spectrales (télédétection) |
| Temporelle | Entre images successives d'une séquence vidéo |

### Pourquoi la compression est-elle possible ?

- **Redondance** : liée à l'aspect statistique de la source, éliminée au codage et restituée au décodage ⇒ **codage exact** (sans perte).
- **Pertinence** : dépend de l'application, mesurée par un critère de fidélité/qualité ; les informations non pertinentes sont éliminées au codage ⇒ **codage approximatif** (avec pertes).

### Critères de choix d'un algorithme de compression

- Réversibilité
- Caractéristiques des données à compresser
- Taux de compression recherché (compromis quantité / qualité)
- Complexité (codeur/décodeur, temps réel/différé, parallélisation)
- Algorithme propriétaire / normalisé
- Autres : robustesse aux erreurs, délais de codage/décodage, débit constant / qualité constante...

### Principe du codage de source

1. Dans un premier temps, enlever la redondance contenue dans les données sources ⇒ **compression réversible**.
2. Si le taux de compression est insuffisant, enlever les informations non pertinentes (ou non perceptibles) pour l'utilisateur ⇒ **compression avec pertes**.

**Exemples** : compression d'image en JPEG / JPEG 2000, compression de son MP3.

## Éléments de la théorie de l'information

> [!info] Théorie de l'information
> Introduite par **Claude Elwood Shannon (1948)**, elle permet de définir :
> - la **capacité maximale** du canal de transmission (en bits utiles/seconde) pour un taux d'erreur binaire (TEB) donné ;
> - le **débit minimum** nécessaire pour coder une source (en bits/échantillon) pour une distorsion donnée.
>
> - Rôle du codeur de **source** : s'approcher au plus près du débit minimum.
> - Rôle du codeur de **canal** : s'approcher au plus près de la capacité maximale.

### Quantité d'information

Soit $\Omega = \{a_0, a_1, \dots, a_{M-1}\}$ l'alphabet des symboles délivrés par une source stationnaire et sans mémoire. On modélise la source par une variable aléatoire $X$ à valeurs dans $\Omega$, suivant une loi telle que $p(X=a_i) = p_i$.

La quantité d'information $h_i$ fournie par la réception d'un symbole $a_i$ est fonction décroissante de sa probabilité $p_i$ : $h_i = f(p_i)$.

- Un événement **probable** contient peu d'information (cas extrême : message certain = aucune information).
- Un événement **improbable** contient beaucoup d'information (cas extrême : message inconnu = information infinie).
- Pour 2 symboles indépendants $a_i, a_j$ : $h_{i+j} = h_i + h_j$, soit $f(p_i \times p_j) = f(p_i) + f(p_j)$.

$f$ doit donc vérifier $f(1)=0$, $f(0)=+\infty$, et $f(p_i \times p_j) = f(p_i)+f(p_j)$ : $f$ est une fonction **logarithmique décroissante** sur $[0,1]$.

> [!tip] Quantité d'information d'un événement
> $$h(A) = -\log_2\big(p(A)\big) \quad \text{(en bits d'information)}$$

### Entropie d'une source

L'**entropie** est la quantité moyenne d'information contenue par symbole :

$$H = E[h(x)] = -\sum_{i=1}^{M} p_i \log_2(p_i) \quad \text{(bits d'information par symbole)}$$

Pour une source binaire : $H = -p('0')\log_2 p('0') - p('1')\log_2 p('1')$.

> [!tip] Entropie maximale
> L'entropie d'une source est **maximale** lorsque tous les symboles sont équiprobables. Pour un alphabet de taille $M$ :
> $$H_{max} = -\sum_{i=1}^{M} \frac{1}{M}\log_2\left(\frac{1}{M}\right) = \log_2(M)$$

## Codage de source sans pertes

```
Source (Rm, H) → Codeur → sortie
```

**Principe** : traduire en trains binaires (mots de code) les symboles émis par la source, en minimisant le nombre de bits utilisés (augmentation de l'efficacité, suppression de la redondance).

Deux types de codage de source :
- **Sans pertes (réversible)** : codage de Huffman, .zip, etc.
- **Avec pertes (irréversible)** : JPEG, MP3, etc. (méthodes psycho-acoustiques, psycho-visuelles).

### Mots de code de longueur fixe (sans extension)

```
Source (Rm, H) → Codeur (D, H') avec D = n × Rm, H' = H/n
```

On code chaque symbole de l'alphabet par un mot de $n$ bits, tel que $2^{n-1} < M \leq 2^n$ :
- $n \geq \log_2 M$ et $H \leq \log_2 M$, c'est-à-dire $n \geq H$ (égalité lorsque les symboles sont équiprobables et $M$ est une puissance de 2).
- La longueur du code (mots de longueur fixe) a donc une **borne inférieure égale à l'entropie** de la source.

> [!tip] Grandeurs caractéristiques
> - **Débit d'information** (≠ débit binaire) : $H(X) \times R_m = H(X)/T_s$, en bits d'information/s (ou shannon/s).
> - **Débit binaire** : $D = n \times R_m = n/T_s$, en bits/s.
> - **Efficacité du codage** : $\eta = H' = H/n$ (entropie par bit transmis), en % ou en bit d'info/bit transmis. Si les symboles sont équiprobables et $M$ est une puissance de 2, $\eta = 1$ (100%).

> [!example]- Exemple A : $M=16$ (puissance de 2), symboles équiprobables
> - Entropie : $H(X) = \log_2(16) = 4$ bits d'information.
> - $R = 4$ bits (car $2^3 < 16 \leq 2^4$).
> - Efficacité : $\eta = H/R = 1$, soit 100 %.
> - Débit binaire = débit d'information.

> [!example]- Exemple B : $M=24$ (pas une puissance de 2), symboles équiprobables
> - Entropie : $H(X) = \log_2(24) = 4{,}584$ bits d'information.
> - $n=5$ bits (car $2^4 < 24 \leq 2^5 = 32$ symboles possibles, dont 8 non utilisés).
> - Efficacité : $\eta = H/n = 4{,}584/5 = 91{,}68\%$.
> - Débit binaire > débit d'information.
>
> **Question :** Comment améliorer l'efficacité quand les symboles sont équiprobables mais que la taille de l'alphabet n'est pas une puissance de 2 ? → *Utiliser le codage en bloc (extension).*

### Codage en bloc (extension d'ordre J)

Soit $X$ une source à valeurs dans $\Omega = \{a_0, \dots, a_{M-1}\}$ de cardinal $M$. La **jème extension** de $X$, notée $X^j$, est la source composée des $M^j$ combinaisons possibles (mots) de $j$ lettres de $\Omega$.

> [!example] Exemple : $\Omega=\{0,1\}$
> - Extension d'ordre 2 : $X^2 = \{00, 01, 10, 11\}$
> - Extension d'ordre 3 : $X^3 = \{000, 001, \dots, 111\}$

**Propriété** : pour une source sans mémoire, l'entropie de la jème extension vaut $j$ fois son entropie : $H(X^j) = j \cdot H(X)$.

**Codage en bloc** : on regroupe $J$ symboles pour former un symbole secondaire (bloc), parmi $M^J$ blocs possibles, chacun codé par un mot de $N$ bits tel que $2^{N-1} < M^J \leq 2^N$.

```
Source (Rm, H) → Codeur en bloc (D, H') avec D = n × Rm, H' = H×J/n
```

- On en déduit que le nombre de bits nécessaires pour coder un symbole primaire est $n' = N/J$.

> [!example]- Exemple Bbis : extension d'ordre 3 de l'exemple B ($M=24$)
> $J=3$, $M^J = 13\,824$ symboles secondaires possibles.
> $N=14$ bits (car $2^{13} < 13\,824 \leq 2^{14} = 16\,384$, soit 2560 symboles inutilisés).
> Astuce pratique : $N = E(H \times J) + 1$.
>
> $H(X^3) = 3\log_2(24) = 13{,}752$ bits d'information.
> $n' = N/J = 14/3 = 4{,}67$
> $\eta = H(X^3)/N = 13{,}752/14 = 98{,}25\%$
>
> En utilisant un codage en bloc d'extension d'ordre 3, on envoie **0,9825 bit d'information par bit transmis** contre 0,9168 sans extension : on a bien augmenté l'efficacité et diminué le débit binaire.

> [!question]- Exercice : codage en bloc, $M=24$, $J=3$
> 1. Nombre de symboles secondaires : $M^J = 24^3 = 13\,824$
> 2. Nombre de bits $N$ pour les coder : $N=14$
> 3. Nombre $n'$ de bits par symbole primaire : $n' = 14/3 \approx 4{,}67$ (à comparer aux 5 bits du code fixe sans extension : gain d'efficacité)
> 4. Efficacité $\eta = 13{,}752/14 = 98{,}25\%$
> 5. Débit binaire : $D = n'/T_s \approx 4{,}67/T_s$

### Premier théorème de Shannon (codes de longueur fixe)

> [!tip] Théorème
> Pour avoir un codage sans erreur avec un code à mots de longueur fixe, une source $X$ doit être codée avec au minimum $H(X)$ bits par symbole : $n' \geq H(X)$.
>
> Si les symboles sont équiprobables, on peut toujours trouver un code permettant d'avoir $n'$ aussi proche de $H$ qu'on le souhaite.

### Mots de code de longueur variable

**Conséquence** : si les symboles ne sont **pas équiprobables**, il n'est pas possible d'avoir $n'$ aussi proche de $H$ qu'on le souhaite avec un codage en bloc à mots de longueur fixe. On utilise alors des **mots de code de longueur variable** : mots courts pour les symboles fréquents, mots longs pour les symboles rares.

**Définitions** :
- **Code non singulier** : deux mots de code différents correspondent à deux symboles différents.
- **Code instantané (code préfixe)** : satisfait la condition du préfixe — aucun mot de code n'est le début d'un autre mot de code.

> [!example]- Illustration : codage de « BOF »
> - Code I : `001001` — non décodable de manière unique.
> - Code III : `01111011` — non décodable instantanément.
> - Code II : `10111110` — code préfixe, décodable de manière unique et instantanément.

**Longueur moyenne d'un code** :
$$L = \sum_{i=1}^{M} p_i\, l_i = p_1 l_1 + p_2 l_2 + \dots + p_M l_M$$
où $l_i$ est la longueur du mot de code $i$.

**Efficacité du codage** : $\eta = H' = H/L$

> [!example] Exemple
> | Symbole | Probabilité | Codage |
> |---|---|---|
> | A | 0,81 | 0 |
> | B | 0,09 | 10 |
> | C | 0,01 | 110 |
> | D | 0,09 | 111 |
>
> $H(X) = 0{,}94$ bits d'information, $L = 1{,}29$, $\eta = 0{,}73$ (73 %).
>
> Comparaison avec un codage à longueur fixe ($M=4 \Rightarrow n'=2$) : $\eta = H/n' = 0{,}47$ (47 %). Le codage à longueur variable est ici bien plus performant.

### Premier théorème de Shannon (codes de longueur variable)

> [!tip] Théorème
> Pour un codage sans erreur avec un code de longueur variable, la longueur moyenne $L$ doit vérifier :
> $$H(X) \leq L \leq H(X) + 1$$
> L'égalité est atteinte lorsque $l_i = -\log_2(p_i)$ pour tout $i$, avec $l_i$ entier.

> [!warning] Limite pratique
> La limite théorique ($L=H$) ne peut être atteinte que si les $-\log_2(p_i)$ sont tous entiers — condition rarement respectée en pratique.

## Codage de Huffman

Codage de longueur variable **sans pertes**, dit **code entropique** : les symboles fréquents sont codés avec des mots courts, les symboles rares avec des mots longs. C'est un code déchiffrable et instantané. Dans ce cours, on se limite au cas binaire ($M=2$).

### Processus itératif

1. Lister les symboles par probabilité d'occurrence décroissante.
2. Regrouper les 2 symboles les moins fréquents pour créer un nouveau symbole, dont la probabilité est la somme des deux probabilités regroupées.
3. Itérer les deux étapes précédentes jusqu'à l'obtention d'un symbole unique (la **racine**).
4. Nommer les branches de l'arbre (0/1) avec une logique constante (ex : « 0 » pour la branche la plus probable, « 1 » pour la moins probable).

> [!question]- Exercice résolu : codage de Huffman
> Alphabet : A(0,36), B(0,15), C(0,13), D(0,11), E(0,09), F(0,07), G(0,05), H(0,03), I(0,01)
>
> Règles : « 0 » pour la branche la plus probable, « 1 » pour la moins probable ; à probabilité équivalente, le nouveau symbole est placé en dessous.
>
> **Regroupements successifs :**
> - H(0,03) + I(0,01) → 0,04
> - G(0,05) + [H,I](0,04) → 0,09
> - E(0,09) + F(0,07) → 0,16
> - D(0,11) + [G,H,I](0,09) → 0,20
> - B(0,15) + C(0,13) → 0,28
> - [E,F](0,16) + [D,G,H,I](0,20) → 0,36
> - [B,C](0,28) + [E,F,D,G,H,I](0,36) → 0,64
> - A(0,36) + [tout le reste](0,64) → 1
>
> **Codes obtenus :**
>
> | Symbole | Probabilité | Code | Longueur |
> |---|---|---|---|
> | A | 0,36 | 1 | 1 |
> | B | 0,15 | 010 | 3 |
> | C | 0,13 | 011 | 3 |
> | D | 0,11 | 0000 | 4 |
> | E | 0,09 | 0001 | 4 |
> | F | 0,07 | 0011 | 4 |
> | G | 0,05 | 00100 | 5 |
> | H | 0,03 | 001010 | 6 |
> | I | 0,01 | 001011 | 6 |
>
> Longueur moyenne du code : $L = \sum p_i l_i$ (à calculer avec le tableau ci-dessus).

## Codage de source : conclusion

> [!warning] Compromis fondamental
> Plus le codage de source est optimal (proche de l'entropie), plus le message transmis est **sensible au bruit** : perdre un bit fait perdre proportionnellement plus d'information.
>
> Dans l'exemple précédent (source A,B,C,D) :
> - Code de longueur fixe : perdre 1 bit équivaut à perdre 0,47 bit d'information.
> - Code de longueur variable : perdre 1 bit équivaut à perdre 0,73 bit d'information.
>
> Il faut donc **durcir** le message transmis pour lutter contre les perturbations du canal : c'est l'objet du [[05 - Codage de canal|codage de canal]].

## Entraînement

> [!question]- Questions de cours
> - Pourquoi la compression d'une source est-elle possible ?
> - Par quelle grandeur caractérise-t-on la quantité moyenne d'information délivrée par une source ?

> [!question]- Exercice 1 : code de longueur fixe, symboles non équiprobables
> Source $S$ à 4 symboles : $P(S_1)=0{,}81$, $P(S_2)=0{,}09$, $P(S_3)=0{,}09$, $P(S_4)=0{,}01$.
>
> **Q1 : Entropie ?**
> $H = -0{,}81\log_2(0{,}81) - 2\times0{,}09\log_2(0{,}09) - 0{,}01\log_2(0{,}01) \approx 0{,}93$ bit/symbole.
>
> **Q2 : Bits nécessaires (codage individuel) ?**
> $M=4 \Rightarrow n=2$ bits.
>
> **Q3 : Efficacité de ce codage ?**
> $\eta = H/n \approx 0{,}93/2 \approx 46{,}5\%$.
>
> **Extension d'ordre 4 :**
>
> **Q4 : Bits nécessaires par symbole (secondaire) ?**
> $H(X^4) = 4H \approx 3{,}72$ bits ⇒ $N$ tel que $2^{N-1} < 4^4=256 \leq 2^N$ ⇒ $N=8$ bits pour 256 symboles secondaires (ici $M^J$ est une puissance de 2 exacte, donc $N=8$ exactement).
>
> **Q5 : Efficacité de ce nouveau codage ?**
> $\eta = H(X^4)/N = 3{,}72/8 \approx 46{,}5\%$ — inchangée ici car $M^J=256=2^8$ est déjà une puissance de 2 exacte (pas de gaspillage de combinaisons), l'extension n'apporte donc pas de gain avec un codage en bloc à longueur fixe pour ce cas particulier.
>
> **Q6 : Qu'en déduisez-vous ?**
> Pour des symboles non équiprobables, le codage en bloc à longueur fixe n'apporte un gain que s'il permet de réduire l'écart entre $N$ et $H(X^J)$ ; le vrai gain vient du passage à un **codage de longueur variable** (Huffman), qui exploite directement l'inégalité des probabilités.

> [!question]- Exercice 2 : source à 6 symboles, 5000 symboles/s
> **Cas équiprobable :**
>
> 1. $H = \log_2(6) \approx 2{,}585$ bits/symbole.
> 2. $D_i = H \times R_m = 2{,}585 \times 5000 \approx 12\,925$ shannon/s.
> 3. $n=3$ bits (car $2^2 < 6 \leq 2^3$).
> 4. $\eta = H/n = 2{,}585/3 \approx 86{,}2\%$.
> 5. Pour augmenter l'efficacité : utiliser un **codage en bloc** (extension).
> 6. Extension d'ordre 5 : $6^5 = 7776$ symboles secondaires, $N=13$ bits (car $2^{12}=4096 < 7776 \leq 2^{13}=8192$).
> 7. $\eta = H(X^5)/N = 5\times2{,}585/13 = 12{,}925/13 \approx 99{,}4\%$.
> 8. On constate un gain net d'efficacité grâce à l'extension.
>
> **Cas non équiprobable :** $P(S)=\{0{,}3; 0{,}25; 0{,}15; 0{,}15; 0{,}1; 0{,}05\}$
>
> 9. $h(S_1) = -\log_2(0{,}3) \approx 1{,}74$ bit. $H(S) \approx 2{,}42$ bits/symbole — inférieure au cas équiprobable (l'entropie est maximale pour des symboles équiprobables).
> 10. Codage de Huffman à construire par regroupements successifs des deux symboles les moins probables (méthode identique à l'exercice résolu ci-dessus).
> 11-13. Une fois l'arbre construit : calculer $L=\sum p_i l_i$, puis $\eta = H/L$, à comparer à l'efficacité d'un code de longueur fixe ($n=3$ bits, $\eta=H/n$).
> 14. Conclusion attendue : le codage de Huffman (longueur variable) est plus efficace que le codage à longueur fixe dès que les symboles ne sont pas équiprobables, car il exploite l'inégale répartition des probabilités.
