---
tags:
  - linux
ordre: 30
---

# Raccourcis

Il existe de nombreux raccourcis que nous pouvons utiliser pour travailler avec Linux plus facilement et plus rapidement. Une fois que nous nous serons familiarisés avec les plus importants d'entre eux et que nous en aurons fait une habitude, nous nous épargnerons beaucoup de saisie. Certains d'entre eux nous aideront même à éviter d'utiliser notre souris dans le terminal.

---

## Saisie semi-automatique

`[TAB]` - Lance la saisie semi-automatique. Cela nous proposera différentes options en fonction de l'entrée standard (`STDIN`) que nous fournissons. Il peut s'agir de suggestions spécifiques comme des répertoires dans notre environnement de travail actuel, des commandes commençant par le même nombre de caractères que nous avons déjà saisis, ou des options.

---

## Déplacement du curseur

`[CTRL] + A` - Déplace le curseur au `début` de la ligne actuelle.

`[CTRL] + E` - Déplace le curseur à la `fin` de la ligne actuelle.

`[CTRL] + [←]` / `[→]` - Saute au début du mot actuel/précédent.

`[ALT] + B` / `F` - Recule/Avance d'un mot.

---

## Effacer la ligne actuelle

`[CTRL] + U` - Efface tout depuis la position actuelle du curseur jusqu'au `début` de la ligne.

`[Ctrl] + K` - Efface tout depuis la position actuelle du curseur jusqu'à la `fin` de la ligne.

`[Ctrl] + W` - Efface le mot précédant la position du curseur.

---

## Coller le contenu effacé

`[Ctrl] + Y` - Colle le texte ou le mot effacé.

---

## Terminer une tâche

`[CTRL] + C` - Termine la tâche/le processus en cours en envoyant le signal `SIGINT`. Par exemple, il peut s'agir d'un scan en cours d'exécution par un outil. Si nous observons le scan, nous pouvons l'arrêter / tuer ce processus en utilisant ce raccourci. À moins que l'outil que nous utilisons soit configuré ou développé pour gérer ce cas, le processus sera tué sans nous demander de confirmation.

---

## Fin de fichier (EOF)

`[CTRL] + D` - Ferme le canal `STDIN`, également connu sous le nom de Fin de fichier (End-of-File ou EOF) ou Fin de transmission (End-of-Transmission).

---

## Effacer le terminal

`[CTRL] + L` - Efface le terminal. Une alternative à ce raccourci est la commande `clear` que vous pouvez taper pour effacer notre terminal.

---

## Mettre un processus en arrière-plan

`[CTRL] + Z` - Suspend le processus en cours en envoyant le signal `SIGTSTP`.

---

## Rechercher dans l'historique des commandes

`[CTRL] + R` - Recherche dans l'historique les commandes que nous avons saisies précédemment et qui correspondent à nos modèles de recherche.

`[↑]` / `[↓]` - Va à la commande précédente/suivante dans l'historique des commandes.

---

## Basculer entre les applications

`[ALT] + [TAB]` - Bascule entre les applications ouvertes.

---

## Zoom

`[CTRL] + [+]` - Zoom avant.

`[CTRL] + [-]` - Zoom arrière.

---

← [[29 - Solaris]] | [[00 - Sommaire Linux|Sommaire]]
