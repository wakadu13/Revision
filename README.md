# ProjetPluri

Wiki Django alimenté par des fichiers Markdown écrits avec la syntaxe
[Obsidian](https://obsidian.md), géré avec [uv](https://docs.astral.sh/uv/).

## Lancer le serveur

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Puis ouvrir http://127.0.0.1:8000/.

## Écrire des pages

Chaque fichier `.md` du dossier [`vault/`](vault/) devient une page du wiki,
sous-dossiers compris : `vault/Projets/Projet Pluri.md` est servi sur
`/wiki/Projets/Projet Pluri`. Le dossier est un coffre Obsidian, qu'on peut
ouvrir tel quel dans Obsidian. Les modifications apparaissent au rechargement
de la page, sans redémarrer le serveur.

La note `Accueil.md` sert de page d'accueil. Le dossier et la page d'accueil se
règlent avec `WIKI_DIR` et `WIKI_HOME` dans [`config/settings.py`](config/settings.py).

Syntaxe prise en charge (voir la page d'exemple `vault/Guide/Syntaxe Obsidian.md`) :

- liens `[[Page]]`, `[[Page|texte]]`, `[[Page#Titre]]`, `[[Page#^bloc]]`, alias
  définis dans les propriétés, liens Markdown `[texte](Page.md)` ;
- intégrations `![[image.png|300]]`, `![[Note]]`, `![[Note#Titre]]`, audio,
  vidéo et PDF ;
- callouts `> [!note]`, repliables avec `+` ou `-`, imbriquables ;
- propriétés YAML (`title`, `tags`, `aliases`...), tags `#tag` et `#tag/sous-tag` ;
- `==surlignage==`, `~~barré~~`, `%%commentaires%%`, listes de tâches,
  tableaux, notes de bas de page, formules `$...$` / `$$...$$`, diagrammes
  ` ```mermaid `.

Un lien vers une page inexistante s'affiche en pointillés ; il suffit de créer
le fichier `.md` correspondant pour qu'il devienne actif.

## QCM de révision

Le wiki intègre un module de QCM (repris de
[revision_qcm](https://github.com/wakadu13/revision_qcm)), accessible via **QCM**
dans la barre latérale ou sur `/qcm/`.

- Un set de questions est un fichier `.json` déposé **dans le coffre** (même
  format que l'application d'origine) ; le nom du dossier qui le contient devient
  sa catégorie. Voir la page d'aide `vault/Guide/QCM.md`.
- 4 types de questions : **QCM**, **QCR** (plusieurs réponses), **TROU** (texte à
  trous) et **FLASHCARD** (recto/verso). Markdown et formules LaTeX `$...$` gérés.
- Feedback immédiat, navigation clavier, et **révision espacée** (système de
  Leitner) avec statistiques de maîtrise par set.
- La progression est enregistrée en base de données (par utilisateur connecté,
  ou partagée si les modifications sont ouvertes). Après un `git pull` qui ajoute
  le module, lancer `uv run python manage.py migrate`.

## Routes

- `/` : page d'accueil du wiki
- `/wiki/<chemin>` : une note
- `/sommaire/` : sommaire de toutes les notes
- `/tags/` et `/tags/<tag>` : les tags
- `/recherche/?q=...` : recherche plein texte (insensible aux accents)
- `/qcm/` : QCM de révision (`/qcm/stats/` pour les statistiques)
- `/fichiers/<chemin>` : pièces jointes du coffre
- `/api/status/` : statut du serveur en JSON
- `/admin/` : administration Django (créer un compte avec `uv run python manage.py createsuperuser`)

## Tests

```bash
uv run python manage.py test
```
