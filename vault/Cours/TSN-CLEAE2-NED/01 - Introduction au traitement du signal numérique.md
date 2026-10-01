---
tags: [TSN, introduction]
---
# Introduction au traitement du signal numérique
Retour : [[00 - Sommaire TSN]] · Suite : [[02 - Bruit et modèle d'observation]]

## Qu'est-ce qu'un signal ?
> [!note] Définition (signal) — d'après le cours de P. Flandrin (ENS Lyon)
> - **Support physique d'une information**.
> - On parle de signal pour toute mesure et/ou transmission d'information d'une **source** vers un **destinataire**.

**Domaines d'application** : électricité, électronique, acoustique, optique, mécanique, astronomie, biologie, économie…

## Qu'est-ce qu'un signal numérique ?
> [!note] Définition (signal numérique / *digital signal*)
> - Suite de **nombres ou symboles** associés à une grandeur physique.
> - **Numérique** (temps discret, valeurs quantifiées) ≠ **analogique** (temps continu, valeurs continues).
> - Un signal peut exister **uniquement** sous forme numérique, ou être la **version numérisée** d'un signal analogique.

**Représentations** :
- $s[n] \in \mathbb{R}$ (1D, ex. audio)
- $s[m,n] \in \mathcal{M}_{M,N}(\mathbb{R})$ (2D, ex. image)
- $s[m,n,l] \in \mathcal{M}_{M,N,L}(\mathbb{R})$ (3D, ex. vidéo)…

Les indices $n, m, l$ peuvent représenter le temps, l'espace, etc. Le support est **généralement fini** : $n \in \{1, 2, \dots, N\}$.

**Exemples** : enregistrements audio, images, vidéos ; télécommunications numériques entre deux machines.

## Qu'est-ce que le traitement du signal numérique ?
> [!note] Définition (traitement du signal numérique)
> Discipline qui développe et étudie les techniques de **traitement** (filtrage…), d'**analyse** et d'**interprétation** des signaux numériques. Elle s'appuie sur la théorie de l'information, les statistiques, les mathématiques appliquées, l'informatique et la physique.
>
> **Traiter un signal** = extraire l'information jugée utile, la mettre en forme pour mieux l'analyser, la transmettre ou la stocker, la nettoyer de parasites éventuels.

**Applications** : compression audio/image/vidéo (MP3, JPEG, MP4), traitement du son et de l'image, télécommunications numériques, IoT, robotique, navigation. Exemples du cours : images radio, images SAR, courbes de performances.

## Avantages et inconvénients du numérique

| Avantages | Inconvénients |
|---|---|
| Immunité aux interférences | Bruit de quantification |
| Maintenance (pas de dérive des composants) | Erreurs d'arrondi |
| Adaptabilité | Plage dynamique limitée |
| Reproductibilité | Repliement de spectre (Nyquist–Shannon) |
| Stockage | Latence / temps de calcul |
| Transmission sans perte | Consommation énergétique |
| Compression | Sensibilité aux pannes logicielles |
| Matériel standardisé / coûts moindres | |
| Interopérabilité | |

> [!tip] Tendance actuelle
> **Numériser le plus tôt possible** dans la chaîne de traitement.

Voir aussi : [[06 - Étapes de la numérisation]], [[10 - Bruit de numérisation]].
