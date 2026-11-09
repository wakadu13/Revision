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

Sur le serveur Linux (Raspberry Pi, Docker Compose, voir les chemins dans
[`README-IA.md`](README-IA.md)) :

```bash
cd /home/pi/ProjetPluri/ProjetPluri && git pull --ff-only
```

```bash
cd /home/pi/deploy && docker compose exec -T web python manage.py migrate
```

```bash
cd /home/pi/deploy && docker compose restart web
```

Quand `pyproject.toml` ou `uv.lock` ont changé (nouvelle dépendance, par
exemple Pillow pour les images allégées), reconstruire d'abord l'image si elle
installe les dépendances (`docker compose build`, puis `docker compose up -d`).
La configuration Docker est dans `/home/pi/deploy`, hors de ce dépôt.

**Serveur de production : gunicorn.** Dans le `compose.yaml` de `/home/pi/deploy`,
le service `web` doit lancer gunicorn avec la configuration du dépôt, plutôt que
`runserver` (serveur de développement de Django, pas fait pour Internet) :

```yaml
    command: gunicorn -c config/gunicorn.conf.py config.wsgi
    restart: unless-stopped
```

La configuration garde **un seul processus** avec plusieurs fils
(`GUNICORN_THREADS`, 4 par défaut ; `GUNICORN_BIND`, `0.0.0.0:8000` par défaut) :
la file des travaux de Claude vit dans le processus, et plusieurs processus
pourraient reprendre deux fois un même travail. gunicorn étant une dépendance du
projet, reconstruire l'image avant de changer la commande. Les journaux restent
lisibles avec `docker compose logs web`.

**Rappels par notification web** : la commande `envoyer_rappels` envoie les
rappels dus ; à lancer toutes les 15 minutes par cron sur le serveur
(`crontab -e`) :

```bash
*/15 * * * * cd /home/pi/deploy && docker compose exec -T web python manage.py envoyer_rappels
```

Les clés du serveur pour ces notifications sont créées au premier usage dans
`vapid_prive.pem` du dossier de données (le dossier du projet sans
`DJANGO_DATA_DIR`) : à sauvegarder, car les changer oblige chaque appareil à
réactiver le rappel. `WIKI_PUSH_CONTACT` (une adresse `mailto:` ou `https://`)
remplace au besoin le contact donné aux services de notifications, par défaut
l'adresse publique du wiki.

**Espaces personnels** : les sets et listes de mots que chaque compte importe
dans « Mon espace » sont rangés dans `perso/<compte>/` du même dossier de
données, hors du coffre : à sauvegarder aussi (comme `copies/`, les photos des
copies corrigées).

**Fichiers du coffre** : le wiki vérifie au plus toutes les 2 secondes si des
fichiers ont changé (`WIKI_VERIF_INTERVALLE`, en secondes) au lieu de parcourir
tout le coffre à chaque requête ; une page déposée à la main ou par Obsidian
apparaît donc au plus tard 2 secondes après. Ce que le wiki écrit lui-même
(éditeur, import, Claude) est visible tout de suite.

Sur un PC Windows (PowerShell, dans le dossier du projet) :

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
- **liens suggérés** : à l'enregistrement, les titres (ou alias) de pages
  existantes cités dans le texte sans lien sont proposés sous l'éditeur ; un
  clic change la première mention en `[[lien]]`. Le code, les formules, les
  liens et les titres de section sont ignorés. « Enregistrer et fermer » les
  montre une fois avant de fermer s'ils n'ont pas encore été proposés ;
- une image **collée** ou **glissée** dans le texte est ajoutée au coffre et
  intégrée (`![[Pasted image ….png]]`), rangée comme dans Obsidian (réglage
  « Dossier des pièces jointes » de `.obsidian/app.json`, racine par défaut) ;
- menu **Fichier** : ouvrir un `.md` de son ordinateur (remplace le texte ou
  s'insère au curseur ; on peut aussi glisser le fichier dans le texte) et
  télécharger la page en `.md` ;
- **Côte à côte** : le texte à gauche, la page rendue à droite, mise à jour
  pendant la saisie et qui défile avec le texte (quatrième mode, à côté
  d'Édition, Source et Lecture) ;
- **brouillon de secours** : le texte non enregistré est gardé sur l'appareil ;
  onglet fermé, batterie à plat ou session expirée, il est proposé à la
  prochaine ouverture de la page (« Reprendre le brouillon » ou « Ignorer ») ;
- menu **Encadré** (définition, théorème, propriété, méthode, exemple,
  démonstration repliée, attention, question, à retenir…) et complétion du type
  en tapant `[!` ; menu **Insérer** : symboles (→ ≤ ∞ α π…), formules types
  (fraction, somme, intégrale, matrice…), date du jour, séparateur, **aligner le
  tableau** où se trouve le curseur ; `#` propose les tags du wiki ;
- boutons **Annuler / Rétablir** (utiles sur tablette), bouton **?** : aide
  avec la syntaxe et les raccourcis, temps de lecture estimé ;
- plan de la page cliquable, compteur de mots, recherche et remplacement
  (<kbd>Ctrl</kbd>+<kbd>F</kbd>), plein écran (voir ci-dessous) : la barre
  d'outils rentre et revient quand la souris touche le haut de l'écran ;
- **historique des versions** (`/historique/<page>`, lien « Historique » au bas
  de chaque page et dans le menu Fichier de l'éditeur) : chaque enregistrement
  qui modifie une page (éditeur, import avec remplacement, page réécrite par
  Claude) garde le texte précédent, hors du coffre (`versions/` du dossier de
  données, 50 versions par page au plus) ; différences ligne à ligne avec la page
  actuelle, texte complet, **restauration** (la page actuelle est gardée avant).

### Lire hors ligne, installer le wiki sur un téléphone

Le wiki est une application installable (PWA, manifeste à la racine) : depuis
Chrome ou Safari, « Ajouter à l'écran d'accueil » l'installe sur Android comme
sur iPhone. Un service worker garde en cache les pages lues, les images et les
fichiers statiques : sans connexion, une page déjà ouverte s'affiche encore ;
sinon la page « hors connexion » liste ce qui est disponible. Sur le
**sommaire**, « ⤓ Hors ligne » sur un dossier met en cache d'un coup ses pages,
ses images et ses PDF (clic de nouveau pour les retirer). Les QCM hors ligne
gardent leur propre application (`/qcm/hors-ligne/`). L'application Android
n'utilise pas ce service worker : elle a sa propre gestion du hors ligne.

### Lecture : le menu se cache

Sur une page de note ou un PDF, le menu de gauche (Accueil, Sommaire, Tags, QCM,
arborescence) est caché pour laisser toute la largeur au texte. Il revient d'un
appui sur la languette › du bord gauche, d'un appui ou d'un glissement du doigt
depuis le bord, ou quand la souris touche le bord ; un appui sur le texte (ou
<kbd>Échap</kbd>) le referme. Le bouton ▯ en haut du menu le garde affiché
pendant la lecture (choix retenu sur l'appareil) ; un nouvel appui le cache de
nouveau. Sur téléphone, le menu reste derrière le bouton ☰.

**Imprimer** : le bouton « Imprimer » d'une page (ou <kbd>Ctrl</kbd>+<kbd>P</kbd>)
n'imprime que le contenu, en clair même en thème sombre, sans menus ni boutons,
encadrés repliés ouverts ; « Enregistrer au format PDF » du navigateur donne une
fiche à garder. Dans l'application Android, le bouton passe par l'impression
d'Android.

### Recherche, « Demander au wiki » et graphe

- **Recherche** (`/recherche/`, champ du menu) : dans les notes et dans le
  **texte des PDF**, page par page, avec un lien qui ouvre le lecteur à la bonne
  page. Le texte des PDF est lu une fois, en arrière-plan, à la première
  recherche (puis seulement pour les PDF nouveaux ou modifiés) ; la commande
  `python manage.py indexer_pdf` fait tout d'un coup. Un PDF scanné (images
  sans texte) n'est pas trouvable.
- **✦ Demander au wiki** (`/demander/`, menu et palette, avec une clé d'API) :
  le tuteur étendu à tout le wiki. Le serveur choisit les pages et les pages de
  PDF qui parlent le plus de la question, Claude (Haiku) répond d'après elles en
  citant ses sources [1], [2]… : chaque numéro mène à la page ou à la page du
  PDF. Il dit quand le wiki n'en parle pas. Les questions de suite tiennent
  compte des précédentes ; l'historique reste sur la page. Même plafond mensuel
  que le tuteur.
- **📷 Corriger ma copie** (`/copie/`, palette, lien sous le tuteur de chaque
  page) : les photos d'une copie manuscrite (1 à 4 pages), l'énoncé et la page
  du cours en option ; Claude (Sonnet, qui lit bien l'écriture manuscrite)
  transcrit la démarche, la corrige étape par étape (✅ juste, ⚠️ imprécis,
  ❌ faux, avec la correction) et fait un bilan avec une note indicative. Photos
  réduites dans le navigateur avant l'envoi, gardées avec la correction (30
  dernières par compte, dans `copies/` du dossier de données), visibles de leur
  seul auteur. Dans l'application Android, le choix des photos propose aussi
  l'appareil photo. Même plafond mensuel que le tuteur.
- **Graphe** (`/graphe/`, menu, et « Voir dans le graphe » sous les rétroliens
  d'une page) : les pages et leurs liens, colorés par dossier ; glisser pour se
  déplacer, molette ou deux doigts pour zoomer, survol pour voir les liens d'une
  page, clic pour l'ouvrir ; recherche d'une page, vue limitée aux voisines
  d'une page (1 ou 2 niveaux).

### Thème et palette de commandes

- **Thème** : bouton ☀/☾ en haut du menu (clair, sombre, ou automatique selon
  le réglage de l'appareil). Le choix est retenu sur l'appareil et appliqué
  avant le premier affichage, sans scintillement.
- **Palette de commandes** : <kbd>Ctrl</kbd>+<kbd>K</kbd> (ou le bouton ≡✓ du
  menu) ouvre une page, un PDF ou un QCM, lance une session de langue ou une
  commande (nouvelle page, importer, thème, plein écran…), au clavier, avec
  une recherche tolérante aux accents. Dans l'éditeur, <kbd>Ctrl</kbd>+<kbd>K</kbd>
  reste le lien vers une page : utiliser <kbd>Ctrl</kbd>+<kbd>P</kbd>.

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
Les images (PNG, JPEG, WebP) de plus de 2000 pixels de côté sont réduites et
recompressées à l'import, sous le même nom : une photo de téléphone de 4 Mo
tient en quelques centaines de Ko, sans toucher aux liens des notes.

### Transformer un cours en page avec Claude (admins)

Avec une clé d'API Claude sur le serveur, chaque cours importé (PDF ou `.tex`)
devient une page du wiki rédigée par Claude : plan du cours en sections,
formules en LaTeX, encadrés pour les définitions, théorèmes, démonstrations
(repliées), méthodes et pièges, tableaux. Le PDF d'origine reste en bas de la
page. Case **« Transformer les cours avec Claude »** sur la page d'import
(cochée par défaut, choix retenu sur l'appareil), ou bouton **« Créer une page
de cours avec Claude »** sur un PDF déjà dans le wiki.

- La transformation se fait en arrière-plan (de quelques dizaines de secondes à
  quelques minutes par cours) ; la page **Cours transformés par Claude**
  (`/transformations/`) suit l'avancement, se met à jour toute seule, affiche
  le coût de chaque cours et permet de relancer un échec.
- Une page modifiée à la main n'est jamais écrasée : la version de Claude est
  enregistrée à côté (« Cours (Claude) »). Pour un `.tex`, la conversion faite
  sur place à l'import est remplacée par celle de Claude.
- Mise en place : créer une clé d'API sur platform.claude.com, puis la coller
  dans la page **Réglages de Claude** (`/claude/reglages/`, menu des admins,
  « ✦ Claude (clé d'API) »), qui la vérifie auprès d'Anthropic avant de
  l'enregistrer et permet de choisir le modèle. La clé reste dans la base de
  données du site (jamais dans le dépôt) et n'est jamais réaffichée en entier.
  À défaut, le wiki lit les variables d'environnement `WIKI_CLAUDE_CLE` (sinon
  `ANTHROPIC_API_KEY`) : un nom à part, car Claude Code, sur le même PC,
  utiliserait une variable `ANTHROPIC_API_KEY` globale à la place de l'abonnement.
- **Gratuit avec un abonnement Claude Max** : 100 $ de crédits d'API par mois,
  sans moyen de paiement (claude.ai → Paramètres → Facturation → Crédits d'API :
  relier une organisation de la Console, puis y créer la clé). Crédits épuisés :
  les transformations s'arrêtent sans rien facturer jusqu'au mois suivant
  ([détails](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)).
- Modèle : Claude Opus 5.5 (`claude-opus-5-5`) par défaut, ou Claude Sonnet 5.5
  (deux fois moins cher), au choix dans les réglages ; coût de l'ordre de 0,50 à 1 $ pour un cours d'une
  trentaine de pages, facturé sur le compte de la clé. Le contenu des cours est
  envoyé à l'API d'Anthropic.
- PDF jusqu'à 600 pages ; au-delà de 20 Mo, il passe par l'API Files
  d'Anthropic (supprimé juste après). Les PDF scannés sont lus aussi.
- **Sans urgence : en lot, moitié prix.** Case « ⧗ Sans urgence » à l'import,
  sur un PDF du wiki et dans les formulaires de génération : la demande part
  dans un lot (Message Batches d'Anthropic), facturé 50 % du prix normal et
  traité sous 24 heures, souvent bien moins. La page Travaux de Claude montre
  « Dans un lot », vérifie toutes les 10 minutes et propose « Vérifier
  maintenant » ; le résultat arrive comme pour une transformation directe.

### Générer des QCM et du vocabulaire avec Claude (admins)

Sur la page des QCM, bloc **« ✦ Générer avec Claude »** (avec une clé d'API
dans les réglages de Claude) :

- **Vocabulaire** : coller des mots ou expressions, un par ligne (en français
  ou dans la langue apprise, avec ou sans traduction), cocher les **types de
  cartes**, choisir la langue (anglais par défaut). Claude ajoute la
  traduction, une phrase d'exemple et la prononciation de chaque mot. Chaque
  envoi crée un **paquet à part** (un fichier de langue), révisable seul
  (« Réviser ce paquet ») ou avec le reste de la langue, ou en **révision intensive** (« Intensif »). Types de cartes :
  carte FR → EN, traduction à taper FR → EN, QCM FR → EN (le bon mot parmi
  ceux du paquet), phrase à compléter, **dictée** (le mot est lu à voix haute,
  on l'écrit), carte EN → FR, traduction à taper EN → FR, **prononciation**
  (voir plus bas) ; cochés par défaut : les trois premiers du français vers l'anglais
  hors QCM (choix retenu sur l'appareil). La première carte cochée fait
  découvrir le mot, les autres viennent ensuite.
- **QCM** : choisir une page du wiki (ou coller un texte) et un nombre de
  questions ; Claude écrit un set (QCM, QCR, textes à trous, réponses courtes,
  cartes), rangé dans la catégorie de la page. Bouton **« Générer un QCM »**
  aussi dans la marge de chaque page de cours.
- **Relecture avant publication** : QCM et paquets arrivent en **brouillon**
  sur la page Travaux de Claude. « Relire et publier » montre chaque question
  (énoncé, choix, bonne réponse, explication) ou chaque mot (traductions,
  exemple, note) : on décoche ce qu'on ne garde pas, on corrige, on publie.
  « Publier tel quel » et « Supprimer » sont aussi là ; la case « Publier
  directement, sans relecture » des formulaires saute l'étape.
- **« Explique-moi »** : après une réponse à une question de QCM (hors examen
  blanc), un bouton demande à Claude (Haiku, quasi gratuit) d'expliquer la
  bonne réponse d'après la page du cours dont le set vient ; l'explication
  est gardée et resservie sans nouvel appel.
- **Fiche de révision** : dans la marge d'une page, « ✦ Fiche de révision »
  fait rédiger par Claude l'essentiel de la page (définitions, formules,
  méthodes, pièges, « à retenir ») dans « Page (Fiche).md », liée à la page.
- **Variantes des questions ratées** : sur la page des statistiques, colonne
  « Ratées » (ratée la dernière fois, ou réussie une fois sur deux au plus),
  bouton « ✦ Variantes » : Claude écrit une question nouvelle par question
  ratée (autre angle, autre type), d'après le cours quand le set en vient, en
  brouillon à relire ; pour retravailler la notion au lieu d'apprendre la
  réponse par cœur.
- **Réponses rédigées corrigées par Claude** : pour une question à réponse
  courte (QRC), une réponse qui n'est pas mot pour mot celle attendue est
  soumise à Claude (Haiku), qui juge le fond : juste, partiel ou faux, avec un
  retour d'une à trois phrases. Hors examen blanc ; correction stricte si
  Claude n'est pas disponible.
- **Tuteur de la page** : dans la marge de chaque page de cours, « ✦ Demander
  au tuteur » : une question, une réponse de Claude (Haiku) ancrée sur la page,
  qui dit quand la réponse n'y est pas ; les échanges restent dans le panneau
  et nourrissent les questions suivantes. Ouvert à tous les comptes.
- **Plafond mensuel** (réglages de Claude, 5 $ par défaut) : explications,
  corrections de réponses rédigées et tuteur s'arrêtent pour le mois une fois
  le plafond atteint (le coût du mois s'affiche dans les réglages) ; les
  transformations demandées par un admin ne sont pas plafonnées.
- **« ✦ Améliorer »** dans la barre de l'éditeur : Claude corrige
  l'orthographe et rend plus clair le passage sélectionné (ou toute la page,
  12 000 caractères au plus) sans toucher au sens ni au balisage ;
  <kbd>Ctrl</kbd>+<kbd>Z</kbd> annule.

Le suivi (et le coût) de chaque demande est sur la page **Travaux de Claude**.
Dans un fichier de langue écrit à la main, la clé `"exercices"` choisit de la
même façon les cartes de vocabulaire (`decouverte`, `production`, `choix`,
`contexte`, `dictee`, `reconnaissance`, `traduction`, `prononciation`) ; sans elle, rien ne change.

**Prononciation vérifiée** (carte `prononciation`) : le mot s'affiche, « 🎤
Prononcer » (ou Espace) écoute ; la reconnaissance vocale compare ce qu'elle
a entendu au mot (accents, ponctuation et petits mots comme « to » ignorés, une
lettre d'écart tolérée sur les mots longs). Bien prononcé : la carte se
retourne avec « Bien » proposé ; trois essais manqués : « À revoir » ; un
silence ne compte pas. La carte retournée lit le mot pour comparer. Marche dans
Chrome et Edge (ordinateur, Android) et dans l'application Android (écran
d'écoute du système) ; ailleurs (Firefox…), la carte devient une carte à dire
puis retourner. La reconnaissance du navigateur passe souvent par Internet.

**Son** : les mots en langue apprise sont lus par la synthèse vocale du
navigateur (gratuite, hors ligne) : à l'affichage d'une carte EN → FR, au
retournement d'une carte FR → EN, après la correction d'une traduction tapée ou
d'un QCM. Bouton 🔊 sur chaque exercice (touche <kbd>R</kbd> sur une carte),
« Son auto » en haut de la session pour couper la lecture automatique (retenu
sur l'appareil). La voix suit le nom de la langue (`code_langue` dans le
fichier pour l'imposer, ex. `"en-US"`).

**Importer une liste de mots sans Claude** (page des QCM, admins) : coller une
liste (une ligne par mot : mot, puis traduction, séparés par une tabulation,
une virgule ou « = ») ou envoyer un export Quizlet, Anki ou tableur (`.csv`,
`.txt`, `.tsv` ; lignes « # » et HTML ignorés), choisir l'ordre des colonnes,
la langue et les types de cartes : un paquet à part est créé, prêt à réviser.

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

**Garder un passage** (admins) : sélectionner du texte dans le lecteur fait
apparaître « 🃏 Garder ce passage » : soit une **carte de révision** recto/verso
(verso : le passage et sa source « PDF, p. n ») dans le set « <PDF> —
annotations » (`QCM/Annotations/<PDF>.json`, lié à la page du cours s'il y en a
une), soit une **citation** ajoutée au bas d'une page du wiki (par défaut la
page du cours, créée au besoin), en encadré avec le numéro de page.

## QCM de révision

Le wiki intègre un module de QCM (repris de
[revision_qcm](https://github.com/wakadu13/revision_qcm)), accessible via **QCM**
dans la barre latérale ou sur `/qcm/`.

- Un set de questions est un fichier `.json` déposé **dans le coffre** (même
  format que l'application d'origine) ; le nom du dossier qui le contient devient
  sa catégorie. Voir la page d'aide `vault/Guide/QCM.md`. Les admins peuvent
  aussi **glisser-déposer** des fichiers `.json` sur la page `/qcm/` : chaque set
  est validé puis enregistré dans `vault/QCM/<catégorie>/`.
- **Mon espace** (`/qcm/mon-espace/`, bouton « 🔒 Mon espace » sur la page des
  QCM) : **chaque compte**, pas seulement les admins, importe ses propres sets
  (`.json`) et listes de mots (collées ou exportées de Quizlet, Anki, d'un
  tableur), **visibles de lui seul**. Ils apparaissent avec les autres, marqués
  « 🔒 perso », et se révisent pareil : FSRS, planning, hors ligne, export Anki,
  page « Aujourd'hui ». Un autre compte, même admin, ne les voit nulle part.
  Limite : 200 fichiers et 20 Mo par compte. Fichiers rangés hors du coffre,
  dans `perso/<compte>/` du dossier de données.
- **Cartes à image masquée** (`/qcm/image-masquee/`, bouton « 🖼 Image
  masquée » sur la page des QCM et dans « Mon espace ») : un schéma (image du
  coffre ou envoyée), des rectangles tracés à la souris ou au doigt, un nom pour
  chacun ; chaque zone devient une carte où elle est cachée (en couleur, les
  autres zones cachées en gris si « Cacher aussi les autres zones » est coché),
  qui se découvre en retournant la carte. Rangées dans « Mon espace » (tout
  compte) ou dans le coffre sous `QCM/<dossier>/` (admins) ; « 🖼 Modifier les
  zones » sur le set pour les reprendre. Format JSON : question de type
  `MASQUE` (voir `wiki/masque.py`). Révision FSRS et hors ligne comme les
  autres ; pas d'export Anki (l'image reste sur le wiki).
- 6 types de questions : **QCM**, **QCR** (plusieurs réponses), **TROU** (texte à
  trous), **QRC** (réponse courte tapée : traduction, synonyme…, avec sens inverse
  optionnel), **FLASHCARD** (recto/verso) et **MASQUE** (image masquée, voir plus
  bas). Markdown et formules LaTeX `$...$` gérés.
- Feedback immédiat, navigation clavier, et **révision espacée FSRS** (le même
  planificateur que le module Langues) : chaque question revient juste avant
  d'être oubliée, les plus menacées d'abord ; statistiques de maîtrise et de
  rétention par set, **révisions à venir** sur 14 jours dans les statistiques.
  La progression faite avant FSRS (boîtes de Leitner) est reprise telle quelle
  à la prochaine réponse.
- **Page « Aujourd'hui »** (`/aujourdhui/`, lien dans le menu) : la série de
  jours, les réponses et les minutes du jour face à un **objectif quotidien**
  (nombre de réponses, réglable), tout ce qui est dû (révision intelligente,
  session du jour de chaque langue, sets les plus chargés), les **examens à
  venir** avec le compte à rebours et l'état du planning, et les révisions
  prévues sur 7 jours. On y active aussi le **rappel par notification web**.
- **Temps de révision** : chaque réponse est chronométrée (de l'affichage de la
  question à la suivante, 2 minutes au plus), QCM et langues, en ligne comme hors
  ligne ; les statistiques montrent les minutes par matière (catégorie de QCM ou
  langue) sur les 8 dernières semaines.
- **Rappel par notification web** : sur la page « Aujourd'hui », « Activer » et
  une heure ; chaque jour à cette heure, une notification dit ce qu'il reste à
  réviser (rien si tout est fait). Marche sur ordinateur et sur Android dans le
  navigateur, et sur iPhone quand le wiki est ajouté à l'écran d'accueil. L'envoi
  se fait par une commande à lancer par cron sur le serveur (voir « Mettre le
  serveur à jour ») ; l'application Android garde son propre rappel.
- **Planning** par set (quotas de nouvelles et de révisions par jour, date
  d'examen, estimation de la durée) ; **date d'examen par catégorie** en un
  clic (« Examen le … » en tête de catégorie) ; case « Ajuster automatiquement
  pour être prêt à temps » : si l'estimation dit « en retard », les nouvelles
  par jour passent au nombre conseillé et les révisions ne sont plus limitées.
  Dans les 30 jours avant l'examen, les révisions visent 95 % de rappel au lieu
  de 90 % (intervalles plus serrés).
- **Révision intensive** (par set ou par catégorie) : les questions ratées
  reviennent dans la session jusqu'à être réussies 2 fois de suite.
- **Module Langues** (comme dans revision_qcm) : un fichier `.json` avec une clé
  `"langue"` décrit du vocabulaire, des tableaux de conjugaison et de la
  grammaire. Répétition espacée **FSRS**, mot découvert en reconnaissance puis
  revu en production (on le tape) et en contexte, conjugaison personne par
  personne, remise en ordre de mots, correction d'erreurs, exercices entrelacés,
  réessai des erreurs dans la session, quota de 20 nouveautés par jour,
  tolérance aux accents/fautes de frappe en vocabulaire. Pages `/qcm/langues/<langue>/`.
  **Révision intensive** (toute la langue, un dossier ou un paquet) : tous les
  exercices sans attendre leur échéance, et chaque exercice raté revient dans la
  session jusqu'à être réussi 2 fois de suite ; seule la première réponse compte
  pour la répétition espacée.
- **Examen blanc** (bouton « Examen » sur un set, « Examen blanc » sur une
  catégorie) : 20 questions tirées au sort (réglable, sans flashcards),
  chronométrées (1 min par question par défaut), aucune correction avant la
  fin ; puis note sur 20 et correction détaillée. Les réponses comptent pour
  la révision espacée.
- **Activité** : la page des statistiques montre la série de jours
  consécutifs avec au moins une réponse (QCM et langues), le record, les
  réponses du jour et des 30 derniers jours, et un calendrier d'activité sur
  26 semaines. La série s'affiche aussi en haut de la page des QCM.
- **Prompts IA** : `prompts_ia/` contient un prompt prêt à copier-coller par
  type de carte (QCM, QCR, TROU, FLASHCARD, set mixte, vocabulaire, conjugaison,
  grammaire). Vérifier ensuite le fichier produit :
  `uv run python manage.py verifier_qcm vault/QCM/<catégorie>/<fichier>.json`
  (sans argument : tout `vault/QCM`).
- **Réviser une page** : quand un QCM a été écrit d'après une page du wiki (par
  Claude, ou avec `"source_page"` dans le JSON), la page affiche dans « Réviser
  ce cours » sa maîtrise et les boutons Réviser, Tout, Examen ; le set indique
  « d'après la page… ».
- **Cartes de la page, sans Claude** (admins) : bouton « 🃏 Créer les cartes de
  la page » dans « Réviser ce cours » : chaque encadré à titre (`> [!definition]
  Titre`, théorème, méthode, formule…) devient une carte recto/verso et chaque
  surlignage `==texte==` un texte à trous, dans « Page — cartes » (`QCM/<dossier
  de la page>/Page (cartes).json`). Régénérer après modification de la page
  garde la progression des cartes inchangées.
- **Signaler une question** : pendant un QCM, « ⚑ Signaler un problème » envoie
  la question et un commentaire aux admins (`/qcm/signalements/`), qui peuvent
  demander une correction à Claude (d'après le cours), l'appliquer, retirer la
  question ou clore. La question corrigée garde son identifiant : la progression
  de chacun est conservée.
- **Export Anki** : bouton « ⬇ Anki » sur chaque set et paquet de langue :
  fichier `.apkg` (notes recto/verso, carte inversée pour les flashcards, le
  vocabulaire et les QRC, formules en MathJax) à importer dans Anki ; avec
  `&format=tsv`, texte tabulé pour Quizlet ou un tableur.
- **Hors ligne** : `/qcm/hors-ligne/` (installable depuis Chrome, HTTPS requis), ou
  l'**application Android** : sets de QCM et paquets de langue téléchargés sur le
  téléphone, révision sans réseau (les sessions de langue sont corrigées et
  planifiées sur l'appareil avec les règles FSRS du serveur), réponses
  synchronisées au retour de la connexion.
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
ensuite directement, partout. Les QCM et les paquets de langue restent
disponibles sans réseau. L'appli peut envoyer un **rappel quotidien**
(notification à l'heure choisie dans ses réglages, avec ce qu'il reste à réviser
et la série de jours ; rien si tout est déjà fait) et recevoir un PDF ou une
note depuis une autre application (« **Partager** » vers ProjetPluri : le fichier
est importé dans le dossier Importés et, pour un cours, transformé en page par
Claude ; admins). **Widget** d'écran d'accueil (à réviser, série de jours) et
**raccourcis** d'application (révision du jour, QCM, hors ligne). Marche aussi
avec l'adresse du réseau local (HTTP, ou HTTPS avec Caddy). Détails :
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

## Surveillance du serveur

- **Depuis l'extérieur** : un moniteur gratuit (UptimeRobot, Better Stack…) qui
  appelle `https://wiki.airhiterofprovence.fr/api/status/` toutes les 5 minutes
  prévient par mail ou notification quand le wiki ne répond plus, même si le
  serveur est éteint.
- **Sur le serveur** : `scripts/surveiller-serveur.sh`, lancé toutes les 5
  minutes par cron, vérifie `/api/status/` en local, note l'incident dans le
  journal système (`journalctl -t wiki-surveillance`), envoie une notification
  au téléphone par [ntfy](https://ntfy.sh) si un sujet est réglé, une seule par
  panne et une au retour, et peut relancer le conteneur. Réglages et ligne de
  crontab en tête du script :

  ```bash
  */5 * * * * WIKI_NTFY=projetpluri-alertes-a1b2c3 /home/pi/ProjetPluri/ProjetPluri/scripts/surveiller-serveur.sh
  ```

- **Sur le téléphone** : l'application Android avertit les admins quand le
  rappel quotidien ne joint pas le serveur alors que le réseau est là.
- **Erreurs du serveur** (`/erreurs/`, menu des admins, avec un badge quand il y
  en a de nouvelles) : chaque page en erreur 500 et chaque incident du fil des
  travaux de Claude, regroupés quand ils se répètent, avec l'adresse, le compte,
  l'endroit du code et la trace complète ; « Marquer comme réglée », « Effacer ».

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
| `WIKI_CLAUDE_CLE` | clé d'API Claude, si elle n'est pas saisie dans la page Réglages de Claude (`ANTHROPIC_API_KEY` marche aussi) | vide |
| `WIKI_CLAUDE_MODELE` | modèle, s'il n'est pas choisi dans la page Réglages de Claude | `claude-opus-5-5` |
| `WIKI_CLAUDE_EFFORT` | effort de réflexion du modèle (`low` à `max`) | `medium` |

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
servir le site en HTTPS derrière un proxy (`DJANGO_BEHIND_PROXY=1`) avec gunicorn
(`config/gunicorn.conf.py`, voir « Mettre le serveur à jour ») plutôt que
`runserver`, puis vérifier avec `uv run python manage.py check --deploy`.

Les tests d'attaque (accès sans compte, élévation de privilèges, XSS, traversée
de chemins, CSRF, force brute, redirections ouvertes, fixation de session,
en-têtes) sont dans [`core/tests.py`](core/tests.py) :
`uv run python manage.py test core`.

## Routes

- `/` : page d'accueil du wiki
- `/wiki/<chemin>` : une note
- `/modifier/<chemin>` : éditeur d'une note (admins) ; `/nouvelle/` : nouvelle page
- `/importer/` : import de fichiers `.md`, de PDF et de pièces jointes (admins)
- `/transformations/` : travaux de Claude (admins) ; `/transformations/<id>/relire/` : relecture d'un brouillon
- `/qcm/expliquer/` : explication d'une question par Claude (POST, connecté)
- `/claude/ameliorer/` : relecture d'un passage par Claude pour l'éditeur (admins, POST)
- `/claude/reglages/` : clé d'API et modèle de Claude (admins)
- `/qcm/generer/` : QCM et paquets de vocabulaire générés par Claude (admins, POST)
- `/qcm/importer-vocabulaire/` : paquet de vocabulaire d'après une liste ou un export (admins, POST)
- `/qcm/mon-espace/` : espace personnel (sets et listes de mots de chaque compte, visibles de lui seul)
- `/pdf/<chemin>` : lecteur de PDF (`?integre=1` : version intégrée dans les notes)
- `/sommaire/` : sommaire de toutes les notes
- `/tags/` et `/tags/<tag>` : les tags
- `/recherche/?q=...` : recherche plein texte (insensible aux accents), notes et texte des PDF
- `/demander/` : « Demander au wiki » (Claude, sources citées) ; `/graphe/` et `/graphe.json` : graphe des liens
- `/copie/` : « Corriger ma copie » (photos, Claude) ; `/copie/photo/<id>/<n>`, `/copie/<id>/supprimer/`
- `/qcm/image-masquee/` : éditeur de cartes à image masquée ; `/qcm/mon-espace/images/<nom>` : images de l'espace personnel
- `/historique/<page>` : versions précédentes d'une page (admins) ; `/pdf-annotation/` (POST, admins) : passage d'un PDF → carte ou citation
- `/sw.js`, `/manifest.webmanifest`, `/hors-connexion/`, `/hors-ligne/dossier.json` : lecture hors ligne du wiki (PWA)
- `/qcm/exporter/?set=…` : export d'un set ou d'un paquet en `.apkg` (Anki) ou `.tsv` (`&format=tsv`)
- `/qcm/cartes-de-la-page/` (POST, admins) : cartes tirées d'une page ; `/qcm/corriger-qrc/` (POST) : réponse rédigée jugée par Claude
- `/claude/tuteur/` (POST) : question au tuteur de la page
- `/qcm/signaler/` (POST) et `/qcm/signalements/` (admins) : questions signalées
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
- `/api/rappel/` : ce qu'il reste à réviser et la série de jours (JSON, notification de l'application)
- `/aujourdhui/` : page « Aujourd'hui » ; `/api/push/cle/`, `/api/push/abonner/`, `/api/push/desabonner/`, `/api/push/tester/` : notifications web
- `/erreurs/` : erreurs du serveur (admins)
- `/qcm/hors-ligne/` : QCM hors ligne (PWA)
- `/admin/` : administration Django (créer un compte avec `uv run python manage.py createsuperuser`)

## Tests

Ils tournent sur GitHub à chaque push et chaque pull request (workflow
« Tests » : tests Django, syntaxe des scripts, et un scénario de bout en bout
dans Chromium avec Playwright, sur gunicorn comme en production), en plus de
l'APK. **Dependabot** (`.github/dependabot.yml`) propose chaque lundi les mises à
jour des dépendances Python et Android (et chaque mois celles des actions
GitHub) en pull requests regroupées, testées par la même CI.

```bash
uv run python manage.py test
```

Les tests du wiki sont rangés par thème dans `wiki/tests/` (`test_pages`,
`test_fichiers`, `test_qcm`, `test_langues`, `test_claude`, `test_appli`), avec
les bases communes dans `wiki/tests/base.py` ; `uv run python manage.py test
wiki.tests.test_qcm` n'en lance qu'une partie.

**Organisation du code** (`wiki/`) : `views.py` (pages, édition, recherche,
historique), `claude_views.py` (tout ce qui passe par Claude), `pdf_views.py`
(lecteur de PDF, pièces jointes), `pwa_views.py` (lecture hors ligne),
`quiz_views.py` (sessions de QCM, statistiques, planning, « Aujourd'hui »),
`qcm_gestion_views.py` (import, rangement, export, signalements, « Mon
espace »), `langues_views.py`, `hors_ligne_views.py` (QCM hors ligne),
`explorer_views.py` (« Demander au wiki », graphe), `masque_views.py`,
`copie_views.py` ; `claude.py` (client, travaux en file, lots, plafond) et
`claude_demandes.py` (appels courts : explications, tuteur, corrections).

Le scénario navigateur (`e2e/scenario.js`) lance le wiki sur le coffre de test
`e2e/vault` : connexion, lecture d'une page et de son panneau « Réviser ce
cours », thème, palette, session de QCM avec signalement puis traitement par
l'admin, export Anki, paquet de langue téléchargé et révisé sans réseau puis
synchronisé. En local, après `npm install playwright` et
`npx playwright install chromium` :

```bash
cp -r e2e/vault /tmp/coffre && mkdir -p /tmp/donnees
export E2E_VAULT=/tmp/coffre DJANGO_DATA_DIR=/tmp/donnees DJANGO_SETTINGS_MODULE=settings_e2e PYTHONPATH=e2e
uv run python manage.py migrate
uv run python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_user('testeur', password='Test-pass-1234!', is_staff=True)"
uv run python manage.py runserver 127.0.0.1:8765
```

```bash
node e2e/scenario.js /tmp
```
