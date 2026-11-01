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

### Mettre le serveur à jour

Sur le PC qui sert le wiki (PowerShell, dans le dossier du projet) :

```powershell
.\scripts\mettre-a-jour.ps1
```

Le script récupère la dernière version de `main` sans toucher aux notes du
coffre. Si un fichier du programme a été modifié à la main sur ce PC (et que la
mise à jour le change aussi), il le signale et propose de remettre sa version
d'origine. Ensuite, **relancer le serveur** (<kbd>Ctrl</kbd>+<kbd>C</kbd> dans sa
fenêtre, puis relancer son script) : il ne relit pas le code tout seul. Les
fichiers CSS et JavaScript portent une empreinte (`wiki.css?v=…`) : navigateurs
et Cloudflare chargent la nouvelle version tout de suite, sans vider de cache.

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

### Éditeur dans le navigateur (admins)

Le bouton **Modifier** d'une page (ou <kbd>Ctrl</kbd>+<kbd>E</kbd>) ouvre un
éditeur façon Obsidian, construit sur [CodeMirror 6](https://codemirror.net) comme
Obsidian lui-même :

- **Édition** (aperçu en direct) : la mise en forme s'affiche pendant la saisie
  (titres, gras, liens, cases à cocher cliquables, images, encadrés colorés) et la
  syntaxe Markdown ne réapparaît que sur la ligne en cours ; **Source** : le
  Markdown brut ; **Lecture** : la page telle qu'elle sera publiée ;
- **formules LaTeX** rendues pendant la saisie (KaTeX, comme les pages) :
  `$…$` dans le texte, blocs `$$…$$` (même collés au texte qui précède) ;
  un clic sur une formule réaffiche son LaTeX. Bouton ∑ ou
  <kbd>Ctrl</kbd>+<kbd>Maj</kbd>+<kbd>M</kbd> : bloc `$$` sur une ligne vide,
  sinon `$…$` autour de la sélection ;
- `[[` propose les pages (alias compris), `![[` les images et fichiers du coffre ;
  <kbd>Ctrl</kbd>+clic ouvre un lien dans un nouvel onglet ;
- <kbd>Ctrl</kbd>+<kbd>S</kbd> enregistre sans quitter la page (enregistrement
  automatique en option), avec détection des modifications faites ailleurs ;
- une image **collée** ou **glissée** dans le texte est ajoutée au coffre et
  intégrée (`![[Pasted image ….png]]`), rangée comme dans Obsidian (réglage
  « Dossier des pièces jointes » de `.obsidian/app.json`, racine par défaut) ;
- menu **Fichier** : ouvrir un `.md` de son ordinateur (remplace le texte ou
  s'insère au curseur ; on peut aussi glisser le fichier dans le texte) et
  télécharger la page en `.md` ;
- plan de la page cliquable, compteur de mots, recherche et remplacement
  (<kbd>Ctrl</kbd>+<kbd>F</kbd>), plein écran (voir ci-dessous) : la barre
  d'outils rentre et revient quand la souris touche le haut de l'écran.

### Lecture : le menu se cache

Sur une page de note ou un PDF, le menu de gauche (Accueil, Sommaire, Tags, QCM,
arborescence) est caché pour laisser toute la largeur au texte. Il revient d'un
appui sur la languette › du bord gauche, d'un appui ou d'un glissement du doigt
depuis le bord, ou quand la souris touche le bord ; un appui sur le texte (ou
<kbd>Échap</kbd>) le referme. Le bouton ▯ en haut du menu le garde affiché
pendant la lecture (choix retenu sur l'appareil) ; un nouvel appui le cache de
nouveau. Sur téléphone, le menu reste derrière le bouton ☰.

### Plein écran

Bouton ⛶ en haut du menu (ou dans la barre de l'éditeur), ou
<kbd>Ctrl</kbd>+<kbd>Maj</kbd>+<kbd>F</kbd> : il ne reste que le texte. Le
menu revient quand la souris touche le **bord gauche** de l'écran, le panneau
de droite (sommaire de la page, rétroliens, plan de l'éditeur) le **bord
droit**, la barre d'outils de l'éditeur le **bord haut** ; ils se cachent quand
la souris s'en éloigne. Sur écran tactile, un appui sur le bord. <kbd>Échap</kbd>
pour quitter. On passe d'une note à l'autre (menu, liens, recherche, retour)
sans quitter le plein écran ; l'éditeur, les QCM et le lecteur PDF s'ouvrent en
rechargeant la page, ce qui fait quitter le plein écran au navigateur.

### Cours écrits en LaTeX

Un cours LaTeX (document `.tex` complet ou extrait) est **converti en page** du
wiki : chapitres et sections numérotés comme dans le PDF, formules (macros
`\newcommand` développées, équations numérotées), théorèmes, définitions,
remarques… (`\newtheorem`) et encadrés `tcolorbox` en callouts colorés,
démonstrations repliées, listes (étiquettes `(i)`, `(a)` comprises), tableaux,
renvois `\ref` et notes de bas de page. Trois façons :

- importer le fichier `.tex` sur `/importer/` (il devient `nom.md`) ;
- dans l'éditeur, coller le LaTeX (la conversion est proposée), ou menu
  **Fichier ▸ Ouvrir un fichier .md ou .tex** ;
- une page qui contient déjà du LaTeX brut affiche un bandeau « Le convertir en
  page » (aussi : **Fichier ▸ Convertir du LaTeX en Markdown**, sur la sélection
  ou toute la page).

Les figures dessinées en LaTeX (TikZ, circuitikz, chronogrammes, tableaux de
Karnaugh) ne peuvent pas être affichées sans LaTeX : leur légende est gardée et
leur code source rangé dans un encadré replié. Pour les voir, importer aussi le
PDF compilé et l'intégrer avec `![[cours.pdf]]`.

### Importer des fichiers .md et des PDF (admins)

**↥ Importer (.md, PDF)** dans la barre latérale (`/importer/`) : glisser-déposer
des notes `.md`, des PDF, ou un **dossier entier** (un coffre Obsidian par ex.)
dont les sous-dossiers, images, PDF, sons et vidéos sont importés avec. On
choisit le dossier de destination ; un fichier existant n'est remplacé que si
« Remplacer » est coché. Les dossiers cachés (`.obsidian`, `.trash`) et les
autres types de fichiers (HTML, scripts…) sont ignorés. Limites : 5 Mo par note,
100 Mo par pièce jointe (derrière nginx, augmenter `client_max_body_size`).

### Lire les PDF dans le wiki

Les PDF du coffre s'ouvrent dans un lecteur intégré (`/pdf/<chemin>`, construit
sur [PDF.js](https://mozilla.github.io/pdf.js/) de Mozilla) qui marche aussi sur
téléphone : défilement continu, zoom (aussi <kbd>Ctrl</kbd>+molette), recherche
dans le texte sans tenir compte des accents, sommaire du document, plein écran,
reprise à la dernière page lue, téléchargement.

- Les PDF apparaissent dans l'arborescence de la barre latérale et dans le sommaire.
- Dans une note : `[[cours.pdf]]` est un lien vers le lecteur, `![[cours.pdf]]`
  affiche le lecteur dans la page et `![[cours.pdf#page=3]]` l'ouvre à la page 3.
- La page d'un PDF liste les notes qui le citent (rétroliens).

Les bibliothèques de l'éditeur et du lecteur sont regroupées dans
`wiki/static/wiki/vendor/` (servies par le site, sans CDN). Pour les mettre à
jour : voir [`bibliotheques/README.md`](bibliotheques/README.md).

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
- **Hors ligne** : `/qcm/hors-ligne/` (installable depuis Chrome, HTTPS requis), ou
  l'**application Android** : sets téléchargés sur le téléphone, révision sans
  réseau, réponses synchronisées au retour de la connexion.
- La progression est enregistrée en base de données, par utilisateur (il faut
  être connecté pour faire les QCM). Après un `git pull` qui ajoute
  le module, lancer `uv run python manage.py migrate`.

## Application Android (téléphone, tablette)

L'APK **ProjetPluri** ([releases](https://github.com/wakadu13/Revision/releases),
tags `apk-v2.…`) affiche le wiki complet avec une navigation tactile : barre en
bas de l'écran (Accueil, Parcourir, Rechercher, QCM, Hors ligne), menu latéral
en tiroir, import et téléchargement de fichiers, PDF en plein écran, zoom au
pincement. On se connecte une fois (identifiant, mot de passe ; l'adresse
publique `https://wiki.airhiterofprovence.fr` est proposée) ; le wiki s'ouvre
ensuite directement, partout. Les QCM restent disponibles sans réseau. Marche
aussi avec l'adresse du réseau local (HTTP, ou HTTPS avec Caddy). Détails :
[`android/README.md`](android/README.md).

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
  Derrière Caddy ou Cloudflare, c'est l'IP réelle du visiteur qui compte, lue
  seulement dans ce que le proxy écrit lui-même (impossible à falsifier,
  [`accounts/ip.py`](accounts/ip.py)).
- **Cache** : pages et fichiers du wiki en `Cache-Control: private` ; Cloudflare
  ou un proxy ne les gardent jamais pour les resservir à quelqu'un sans compte.
- **Anti-XSS** : le HTML des notes et des QCM est nettoyé (nh3) ; Content Security
  Policy stricte (aucun script en ligne) ; bibliothèques du CDN à version figée
  avec contrôle d'intégrité (SRI) ; les fichiers HTML/SVG du coffre sont
  téléchargés, jamais exécutés.
- **Fichiers** : impossible de lire ou d'écrire hors du coffre (`..`, liens
  symboliques, chemins absolus). L'import n'accepte que des notes `.md` (texte
  UTF-8) et des médias (images, PDF, audio, vidéo), jamais dans `.obsidian`.
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
| `DJANGO_CLOUDFLARE` | derrière Cloudflare : IP du visiteur lue dans `CF-Connecting-IP` (inclut `DJANGO_BEHIND_PROXY`) | `0` |

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
5. Après une mise à jour du code (`git pull`, changement de branche), arrêter le
   script (<kbd>Ctrl</kbd>+<kbd>C</kbd>) et le relancer : le serveur ne relit pas
   le code à chaud, et les pages modifiées renverraient « Server Error (500) ».
   Le détail d'une erreur 500 s'affiche dans la fenêtre du script.

### Accès depuis Internet (Cloudflare)

Le wiki est en ligne sur <https://wiki.airhiterofprovence.fr> : Cloudflare →
Caddy → Django. Dans le script de lancement, en plus des réglages de
`serve-lan.ps1` :

```powershell
$env:DJANGO_ALLOWED_HOSTS = "wiki.airhiterofprovence.fr,$Ip"   # domaine + IP pour le Wi-Fi
$env:DJANGO_CLOUDFLARE = "1"
```

- `DJANGO_CLOUDFLARE=1` : l'anti-force brute compte les essais par visiteur
  (IP donnée par Cloudflare). Sans ce réglage, tout le monde arrive par les
  mêmes adresses de Cloudflare : un inconnu qui tape 5 mots de passe faux
  bloque le compte 30 minutes, y compris pour son propriétaire.
- Le PC ne doit être joignable que par Cloudflare : Cloudflare Tunnel
  (`cloudflared`, aucun port ouvert sur la box), ou ports de la box limités aux
  [adresses de Cloudflare](https://www.cloudflare.com/ips/). Sinon, quelqu'un qui
  connaît l'IP de la box contourne Cloudflare et choisit l'IP qu'il annonce.
- Pas de règle de cache « Cache Everything » dans Cloudflare : les pages et
  fichiers du wiki sont marqués privés, les fichiers statiques (`/static/`)
  restent en cache.
- Cloudflare refuse les envois de plus de 100 Mo (offre gratuite) : un très gros
  PDF s'importe depuis l'adresse locale.

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
- `/modifier/<chemin>` : éditeur d'une note (admins) ; `/nouvelle/` : nouvelle page
- `/importer/` : import de fichiers `.md`, de PDF et de pièces jointes (admins)
- `/pdf/<chemin>` : lecteur de PDF (`?integre=1` : version intégrée dans les notes)
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
- `/api/appareil/connexion/`, `/api/appareil/deconnexion/` et `/api/appareil/session/` : jeton de l'application Android
- `/qcm/hors-ligne/` : QCM hors ligne (PWA)
- `/admin/` : administration Django (créer un compte avec `uv run python manage.py createsuperuser`)

## Tests

```bash
uv run python manage.py test
```
