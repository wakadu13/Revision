---
tags: [guide, wiki/documentation]
---
Le wiki intègre un module de **QCM de révision** (repris de l'application
[revision_qcm](https://github.com/wakadu13/revision_qcm)), accessible via **QCM**
dans la barre latérale, ou sur [/qcm/](/qcm/).

## Créer un set de questions

Un set est un fichier `.json` déposé dans le coffre (n'importe où). Le **nom du
dossier** qui le contient devient la **catégorie**. Par exemple
`QCM/reseaux/osi.json` → catégorie « reseaux ».

```json
{
  "titre": "Titre affiché du set",
  "description": "Courte description (optionnel)",
  "questions": [
    {"type": "QCM", "question": "Aire d'un cercle de rayon $r$ ?", "choix": ["$2\\pi r$", "$\\pi r^2$"], "reponses": [1], "explication": "Aire = $\\pi r^2$."},
    {"type": "QCR", "question": "Plusieurs bonnes réponses ?", "choix": ["A", "B", "C"], "reponses": [0, 2]},
    {"type": "TROU", "question": "She ___ (go) to school.", "reponses_texte": ["goes"]},
    {"type": "FLASHCARD", "question": "to achieve", "verso": "réussir"}
  ]
}
```

## Les 4 types

- **QCM** — une seule bonne réponse.
- **QCR** — plusieurs bonnes réponses.
- **TROU** — réponse libre (casse, accents et espaces ignorés).
- **FLASHCARD** — recto/verso auto-évalué.

Les `reponses` sont les **indices** des bons choix (à partir de 0). Le texte des
questions et des choix accepte le **Markdown** et les **formules LaTeX** `$...$`.
Dans le JSON, doublez les backslash LaTeX : `$\\pi$`, `$\\frac{a}{b}$`.

## Révision espacée (Leitner)

Chaque question monte d'une boîte (0→5) à une bonne réponse, redescend à une
mauvaise. Plus la boîte est haute, plus l'intervalle avant la prochaine révision
est long (1, 3, 7, 14, 30 jours). La **Révision intelligente** ne propose que les
questions dues, les moins maîtrisées d'abord. La progression est enregistrée
automatiquement ; les [statistiques](/qcm/stats/) montrent la maîtrise par set.
