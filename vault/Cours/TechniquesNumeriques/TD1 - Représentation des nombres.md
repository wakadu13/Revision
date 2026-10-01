---
tags: [techniques-numeriques, td, binaire]
---
# TD : Représentation des nombres

Retour : [[00 - Sommaire Techniques Numériques]] · Cours : [[01 - Représentation des nombres]]

## 1ère partie : conversion de bases

> [!question]- Exercice 1.1 — Convertir 192 (base 10) en base 2, puis en base 16.
> `192 = (11000000)₂ = (C0)₁₆`

> [!question]- Exercice 1.1 — Convertir 17,150 (base 10) en base 2, puis en base 16.
> Partie entière : `17 = (10001)₂`. Partie fractionnaire (multiplications
> successives par 2) : `0,150×2=0,3 → 0 ; 0,3×2=0,6 → 0 ; 0,6×2=1,2 → 1 ;
> 0,2×2=0,4 → 0 ; ...` soit `≈ (10001,0010…)₂ ≈ (11,26)₁₆`

> [!question]- Exercice 1.2 — Convertir FFFF (hexa) en base 2 puis en base 10.
> `(FFFF)₁₆ = (1111111111111111)₂ = (65535)₁₀`

> [!question]- Exercice 1.2 — Convertir 0,13 (hexa) en base 2 puis en base 10.
> `1 = 0001₂`, `3 = 0011₂` → `(0,00010011)₂`.
> `(0,13)₁₆ = 1×16⁻¹ + 3×16⁻² = 0,0625 + 0,01171875 ≈ (0,0742)₁₀`

> [!question]- Exercice 2 — Un nombre s'écrit en base 10 avec D chiffres. Combien de chiffres faut-il pour l'écrire en base 2, 3, 4, 8, 16 ?
> Le nombre de chiffres nécessaires en base `b` est
> `⌈D·log₁₀(10)/log₁₀(b)⌉ = ⌈D/log₁₀(b)⌉` (arrondi supérieur). Plus la base
> est grande, moins il faut de chiffres : base 2 (le plus de chiffres),
> puis 3, 4, 8, 16 (le moins de chiffres).

### Exemples travaillés (méthode des divisions successives)

> [!example] Convertir 42 (base 10) en base 3
> ```text
> 42 / 3 = 14  reste 0
> 14 / 3 = 4   reste 2
> 4  / 3 = 1   reste 1
> 1  / 3 = 0   reste 1
> ```
> `42₁₀ = 1120₃`

> [!example] Convertir 1739 (base 10) en base 7
> `1739₁₀ = 5033₇` (divisions successives par 7 : restes 3,3,0,5,5)

> [!example] Convertir 423₅ en base 10
> `423₅ = 4×5² + 2×5¹ + 3×5⁰ = 100+10+3 = 113₁₀`

> [!example] Convertir 357₉ en base 10
> `357₉ = 3×9² + 5×9¹ + 7×9⁰ = 243+45+7 = 295₁₀`

> [!example]- Convertir 1230230120₄ en base 16 (deux méthodes)
> **Méthode 1** (passage par la base 10) :
> `1230230120₄ = 445208₁₀ = 6CB18₁₆`
>
> **Méthode 2** (passage par la base 2, regroupement par 4 bits) :
> `445208₁₀ = 1101100101100011000₂`
> regroupé par 4 : `0110 1100 1011 0001 1000` → `6 C B 1 8` → `6CB18₁₆`

> [!example]- Convertir 15,4921875 (base 10) en base 16
> Partie entière `15 = F₁₆`. Partie fractionnaire par multiplications
> successives par 2 (0,4921875→0,984375→1,96875→1,9375→1,875→1,75→1,5→1),
> on obtient `0111 1110₂` groupé par 4 bits → `7E`.
> **`15,4921875₁₀ = F,7E₁₆`**

> [!example]- Convertir 10,6640625 (base 10) en base 16
> Même méthode : partie entière `10 = A₁₆`, partie fractionnaire
> `0,6640625 → ... → 10101010₂` groupé par 4 → `AA`.
> **`10,6640625₁₀ = A,AA₁₆`**

## 2ème partie : représentation dans les calculateurs

> [!question]- Exercice 3 — Convertir en complément à 2 sur 8 bits : a) 19  b) -52  c) 127  d) -127  e) -128
> a) `19 = 00010011`
> b) `-52 = 11001100` (complément de `00110100` + 1)
> c) `127 = 01111111`
> d) `-127 = 10000001`
> e) `-128 = 10000000`
>
> **Généralisation** : sur `n` bits, le plus grand nombre représentable est
> `2ⁿ⁻¹ - 1`, le plus petit est `-2ⁿ⁻¹`.

> [!question]- Exercice 4 — Additions en complément à 2 sur 8 bits (préciser s'il y a dépassement)
> a) `10110110 + 01001010` : résultat correct si pas de dépassement de
>    capacité (à vérifier en comparant le signe des opérandes et du
>    résultat : deux opérandes de même signe donnant un résultat de signe
>    opposé = dépassement).
> b) `10000010 + 11111111` = addition d'un nombre négatif et de -1 → décrémente.
> c) `00110110 + 01001010` : deux positifs, vérifier que le résultat reste
>    positif sur 8 bits, sinon dépassement.
> e) `A + A` avec `A = 11111111` (= -1) → `-1 + -1 = -2` = `11111110`, correct.
> f) `A + A` avec `A = 01000000` (= 64) → `64+64=128`, **dépassement** (128
>    n'est pas représentable sur 8 bits signés, max = 127).
>
> *Méthode générale : effectuer l'addition binaire normalement (retenues
> propagées), puis détecter un dépassement si la retenue entrant dans le
> bit de signe diffère de la retenue sortante.*

> [!question]- Exercice 5 — Norme IEEE 754 simple précision
> a) Le plus grand nombre positif : `e=254` (max hors code réservé 255),
> `f` tout à 1 → `s=0, e=11111110, f=111...1` soit en hexa `7F7FFFFF`,
> valeur ≈ `3,4×10³⁸`.
> b) Le plus petit négatif normalisé et le plus petit positif normalisé
> (en valeur absolue) correspondent à `e=1` (le plus petit exposant non
> nul) et `f=0` : `±1,0 × 2⁻¹²⁶ ≈ ±1,18×10⁻³⁸`.
> c-1) `86 20 00 00` : `s=1`, `e=00001100`, `f=0100000...` →
>   nombre négatif.
> c-2) `3F C0 00 00` : `s=0`, `e=01111111`, `f=1000...` → `N = 1,5`.
> c-3) `7F 80 00 00` : `e=255`, `f=0` → représente **l'infini positif**.

> [!question]- Exercice 6 — Pour des entiers signés codés sur n bits en complément à 2, montrer que l'équation x = -x a deux solutions.
> On cherche `x` tel que `x = -x`, c'est-à-dire `2x = 0` modulo `2ⁿ`.
> Les deux solutions sont **`x = 0`** (trivialement) et **`x = -2ⁿ⁻¹`**
> (le nombre le plus négatif représentable, dont l'opposé « déborde » et
> revient sur lui-même : `-(-2ⁿ⁻¹)` ne peut pas être représenté positivement
> sur n bits, le résultat calculé reboucle sur `-2ⁿ⁻¹` lui-même).

## Révision
- QCM du module : [/qcm/](/qcm/) (catégorie « TechniquesNumeriques »)
