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
    {"type": "QRC", "consigne": "Traduire en anglais", "question": "chien", "reponses_texte": ["dog"], "inverse": true, "consigne_inverse": "Traduire en français"},
    {"type": "FLASHCARD", "question": "to achieve", "verso": "réussir"}
  ]
}
```

### Importer par glisser-déposer

Les admins voient en haut de la page [/qcm/](/qcm/) une zone d'import : il suffit
d'y **glisser des fichiers `.json`** (ou de cliquer pour les choisir). Choisissez
d'abord la catégorie (dossier existant ou nouveau nom ; « Importés » par défaut).
Chaque set est vérifié avant d'être enregistré dans `vault/QCM/<catégorie>/` ;
les erreurs (JSON invalide, champ manquant…) s'affichent en haut de la page. Un
fichier du même nom n'est remplacé que si « Remplacer les sets existants » est
coché.

## Les 5 types

- **QCM** — une seule bonne réponse.
- **QCR** — plusieurs bonnes réponses.
- **TROU** — réponse libre (casse, accents et espaces ignorés).
- **QRC** — question à réponse courte : un mot ou une phrase à retrouver en le
  tapant (traduction, synonyme…). Voir ci-dessous.
- **FLASHCARD** — recto/verso auto-évalué.

### QRC : traduction, synonyme

- `consigne` (optionnel) s'affiche au-dessus du mot : « Traduire en anglais »,
  « Donner un synonyme »…
- `reponses_texte` liste **toutes** les réponses acceptées. Si on trouve la
  bonne, les autres sont affichées (pratique pour les synonymes).
- `"inverse": true` ajoute automatiquement la question dans l'autre sens
  (*chien → dog* puis *dog → chien*), avec sa propre consigne
  `consigne_inverse`. L'inverse demande la 1re réponse de `reponses_texte` et
  attend le texte de `question` : garde-les en texte simple, sans Markdown.
- Casse, accents, espaces, apostrophes ’ / ' et ponctuation finale (`. ! ?`)
  sont ignorés, pour les QRC comme pour les TROU.

> Attention à ne pas confondre **QRC** (réponse tapée) et **QCR** (cases à cocher).

Les `reponses` sont les **indices** des bons choix (à partir de 0). Le texte des
questions et des choix accepte le **Markdown** et les **formules LaTeX** `$...$`.
Dans le JSON, doublez les backslash LaTeX : `$\\pi$`, `$\\frac{a}{b}$`.

## Révision espacée (Leitner)

Chaque question monte d'une boîte (0→5) à une bonne réponse. Une mauvaise
réponse la renvoie en boîte 0 : elle est reproposée le jour même (hors quota)
puis repart du début. Plus la boîte est haute, plus l'intervalle avant la
prochaine révision est long (1, 3, 7, 14, 30 jours).

Les **flashcards** s'auto-évaluent avec 4 boutons (touches 1 à 4) :
**À revoir** (retour en boîte 0), **Difficile** (reste dans sa boîte, même
intervalle), **Bien** (boîte suivante) et **Facile** (saute une boîte).

Le panneau **Planning** de chaque set fixe deux quotas par jour : les
**nouvelles** questions et les **révisions** (questions déjà vues revenues à
échéance). Limitez surtout les nouvelles et laissez les révisions libres. Avec
une **date d'examen**, il estime la durée nécessaire et la date à laquelle
commencer. La **Révision intelligente** ne propose que les
questions dues, les moins maîtrisées d'abord. La progression est enregistrée
automatiquement ; les [statistiques](/qcm/stats/) montrent la maîtrise par set.

## Révision intensive

Pour tout savoir **dès le lendemain** (veille d'examen), le bouton **Intensif**
d'un set — ou **Révision intensive de la catégorie** — pose toutes les questions,
y compris celles déjà maîtrisées. Une question ratée revient quelques questions
plus loin, puis encore plus tard : elle n'est considérée comme sue qu'après
**2 bonnes réponses de suite**. Au passage suivant, l'ordre des choix est mélangé
pour qu'on retienne la réponse, pas sa position. La session se termine quand tout
est su, avec la liste des questions les plus difficiles.

Seule la **première réponse** à chaque question est enregistrée pour la révision
espacée : les répétitions ne gonflent pas les boîtes. Les questions ratées restent
donc « à réviser » et reviennent le lendemain dans la Révision intelligente.

## Langues

La section **Langues** en haut de la [page des QCM](/qcm/) regroupe les
fichiers de langue (vocabulaire, conjugaison, grammaire). Elle applique les
techniques les mieux établies pour apprendre une langue :

- **Répétition espacée FSRS** (l'algorithme d'Anki) : chaque élément revient
  quand la probabilité de s'en souvenir tombe à 90 %. Les cartes ont 4 boutons
  (touches 1 à 4) qui indiquent quand la carte reviendra.
- **Rappel actif** : un mot est d'abord découvert en **reconnaissance**
  (anglais → français), puis revient en **production** (on tape le mot) et
  **en contexte** (phrase à compléter) — jamais deux facettes d'un même mot
  dans la même session.
- **Conjugaison** personne par personne, avec le tableau complet à la
  correction ; **grammaire** par phrases à trous, **remise en ordre** de mots
  (clic ou numéro, ⌫ pour retirer) et **correction d'erreurs**.
- **Entrelacement** : la **Session du jour** mélange vocabulaire, conjugaison
  et grammaire. Un exercice raté revient quelques questions plus tard.
- **Tolérance** : en vocabulaire, un accent oublié ou une faute de frappe
  compte comme « presque » ; en conjugaison et en grammaire, la réponse doit
  être exacte. Les lettres fausses sont surlignées dans la réponse attendue.
- Après une bonne réponse, **F** signale qu'elle était trop facile : elle
  reviendra plus tard. Au plus 20 nouveautés par jour ; les révisions dues
  passent toujours en premier.

Autres modes : **Vocabulaire**, **Conjugaison**, **Grammaire** et **Points
faibles** (éléments souvent oubliés), avec des statistiques par langue.
Format d'un fichier de langue : voir `README-IA.md` (§ 5.1) et les prompts du
dossier `prompts_ia/`.

