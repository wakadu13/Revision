# ProjetPluri

Wiki Django alimenté par des fichiers Markdown écrits avec la syntaxe
[Obsidian](https://obsidian.md), géré avec [uv](https://docs.astral.sh/uv/).

## Lancer le serveur

Le site est **privé** : il faut un compte pour voir quoi que ce soit.

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser   # premier compte admin
```

En développement (sur sa machine), activer le mode debug :

```bash
DJANGO_DEBUG=1 uv run python manage.py runserver          # bash
$env:DJANGO_DEBUG=1; uv run python manage.py runserver    # PowerShell
```

Puis ouvrir http://127.0.0.1:8000/. Sans `DJANGO_DEBUG=1`, le serveur démarre en
mode production (pas de traces d'erreur) ; en local il reste en HTTP. HTTPS est
forcé dès que `DJANGO_ALLOWED_HOSTS` contient un vrai nom de domaine (voir « Sécurité »).

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
  sa catégorie. Voir la page d'aide `vault/Guide/QCM.md`. Les admins peuvent
  aussi **glisser-déposer** des fichiers `.json` sur la page `/qcm/` : chaque set
  est validé puis enregistré dans `vault/QCM/<catégorie>/`.
- 5 types de questions : **QCM**, **QCR** (plusieurs réponses), **TROU** (texte à
  trous), **QRC** (réponse courte tapée : traduction, synonyme…, avec sens inverse
  optionnel) et **FLASHCARD** (recto/verso). Markdown et formules LaTeX `$...$` gérés.
- Feedback immédiat, navigation clavier, et **révision espacée** (système de
  Leitner) avec statistiques de maîtrise par set.
- **Révision intensive** (par set ou par catégorie) : les questions ratées
  reviennent dans la session jusqu'à être réussies 2 fois de suite.
- **Module Langues** (comme dans revision_qcm) : un fichier `.json` avec une clé
  `"langue"` décrit du vocabulaire, des tableaux de conjugaison et de la
  grammaire. Répétition espacée **FSRS**, mot découvert en reconnaissance puis
  revu en production (on le tape) et en contexte, conjugaison personne par
  personne, remise en ordre de mots, correction d'erreurs, exercices entrelacés,
  réessai des erreurs dans la session, quota de 20 nouveautés par jour,
  tolérance aux accents/fautes de frappe en vocabulaire. Pages `/qcm/langues/<langue>/`.
- **Prompts IA** : `prompts_ia/` contient un prompt prêt à copier-coller par
  type de carte (QCM, QCR, TROU, FLASHCARD, set mixte, vocabulaire, conjugaison,
  grammaire). Vérifier ensuite le fichier produit :
  `uv run python manage.py verifier_qcm vault/QCM/<catégorie>/<fichier>.json`
  (sans argument : tout `vault/QCM`).
- La progression est enregistrée en base de données, par utilisateur (il faut
  être connecté pour faire les QCM). Après un `git pull` qui ajoute
  le module, lancer `uv run python manage.py migrate`.

## Comptes et rôles

| Rôle | Peut… |
|---|---|
| visiteur (non connecté) | rien : seulement la page de connexion |
| **utilisateur** | lire le wiki, faire les QCM avec sa propre progression |
| **admin** | tout ce qui précède + créer/modifier des pages, gérer les comptes, `/admin/` |

- Créer le premier admin : `uv run python manage.py createsuperuser`.
- Pas d'inscription libre : un admin crée les comptes sur `/utilisateurs/`, où il
  peut aussi promouvoir, rétrograder ou désactiver un compte (un compte
  désactivé est déconnecté immédiatement). Le rôle admin correspond au champ
  « statut équipe » (`is_staff`) de Django. Pour rouvrir l'inscription sur
  `/inscription/` : `ACCOUNTS_REGISTRATION_OPEN = True` dans `config/settings.py`.
- Mots de passe : 12 caractères minimum, ni trop courants, ni uniquement des
  chiffres, ni proches du nom d'utilisateur. Stockés hachés (PBKDF2).
- Sessions : 2 semaines avec « Rester connecté », sinon jusqu'à la fermeture du
  navigateur.

## Sécurité

Mesures en place :

- **Site privé** : toutes les pages demandent d'être connecté
  (`LoginRequiredMiddleware`) ; la page de connexion n'affiche rien du wiki.
- **Anti-force brute** (django-axes) : 5 mots de passe faux pour un compte depuis
  une même IP → blocage 30 min. Débloquer : `uv run python manage.py axes_reset`.
- **Anti-XSS** : le HTML des notes et des QCM est nettoyé (nh3) ; Content Security
  Policy stricte (aucun script en ligne) ; bibliothèques du CDN à version figée
  avec contrôle d'intégrité (SRI) ; les fichiers HTML/SVG du coffre sont
  téléchargés, jamais exécutés.
- **Fichiers** : impossible de lire ou d'écrire hors du coffre (`..`, liens
  symboliques, chemins absolus).
- **CSRF, clickjacking, HTTPS** : jetons CSRF, `X-Frame-Options: DENY`, HTTPS
  forcé + HSTS 1 an, cookies `Secure`/`HttpOnly`/`SameSite` en production.
- **Secrets hors de Git** : la clé secrète vient de `DJANGO_SECRET_KEY`, sinon
  d'un fichier `.secret_key` généré au premier lancement (ignoré par Git).

Variables d'environnement :

| Variable | Rôle | Défaut |
|---|---|---|
| `DJANGO_DEBUG` | mode développement | `0` |
| `DJANGO_SECRET_KEY` | clé secrète | fichier `.secret_key` |
| `DJANGO_ALLOWED_HOSTS` | noms de domaine du site, séparés par des virgules | `localhost,127.0.0.1,[::1]` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | ex. `https://wiki.exemple.fr` | vide |
| `DJANGO_HTTPS` | HTTPS forcé, cookies sécurisés, HSTS | `1` si un vrai domaine est dans `DJANGO_ALLOWED_HOSTS` (hors debug), sinon `0` |
| `DJANGO_BEHIND_PROXY` | derrière nginx/Caddy (IP et HTTPS transmis par le proxy) | `0` |

### HTTPS sur le réseau local

Pour ouvrir le wiki depuis un autre appareil du même Wi‑Fi, en HTTPS :

1. Installer [Caddy](https://caddyserver.com) une fois : `winget install CaddyServer.Caddy`.
2. Lancer `.\scripts\serve-lan.ps1` : Caddy (HTTPS, port 443) relaie vers Django,
   qui n'écoute que sur `127.0.0.1`. Adresse affichée : `https://<IP du PC>/`.
3. Au premier lancement, accepter l'autorité de certification de Caddy. Sur les
   autres appareils, installer le fichier `%APPDATA%\Caddy\pki\authorities\local\root.crt`
   comme autorité de confiance. Ne jamais partager `root.key` (même dossier).
4. Le réseau Wi‑Fi doit être en profil « Privé » dans Windows, et un VPN doit
   autoriser l'accès au réseau local.

Mise en production : définir `DJANGO_ALLOWED_HOSTS` et `DJANGO_CSRF_TRUSTED_ORIGINS`,
servir le site en HTTPS derrière un proxy (`DJANGO_BEHIND_PROXY=1`) avec un
serveur WSGI (gunicorn, waitress…) plutôt que `runserver`, puis vérifier avec
`uv run python manage.py check --deploy`.

Les tests d'attaque (accès sans compte, élévation de privilèges, XSS, traversée
de chemins, CSRF, force brute, redirections ouvertes, fixation de session,
en-têtes) sont dans [`core/tests.py`](core/tests.py) :
`uv run python manage.py test core`.

## Routes

- `/` : page d'accueil du wiki
- `/wiki/<chemin>` : une note
- `/sommaire/` : sommaire de toutes les notes
- `/tags/` et `/tags/<tag>` : les tags
- `/recherche/?q=...` : recherche plein texte (insensible aux accents)
- `/qcm/` : QCM de révision (`/qcm/stats/` pour les statistiques, `/qcm/importer/`
  pour l'import de sets JSON par glisser-déposer, admins)
- `/qcm/langues/<langue>/` : module Langues (session du jour, modes, statistiques)
- `/documentation/` et `/documentation/ia/` : ce README et `README-IA.md`, lisibles dans le wiki
- `/fichiers/<chemin>` : pièces jointes du coffre
- `/connexion/`, `/deconnexion/`, `/inscription/` : session
- `/compte/` : mon compte (`/compte/mot-de-passe/` pour changer de mot de passe)
- `/utilisateurs/` : gestion des comptes (admins)
- `/api/status/` : statut du serveur en JSON
- `/admin/` : administration Django (créer un compte avec `uv run python manage.py createsuperuser`)

## Tests

```bash
uv run python manage.py test
```
