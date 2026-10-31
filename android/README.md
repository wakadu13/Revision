# Application Android « ProjetPluri »

APK pour téléphone et tablette : le **wiki complet** (pages, éditeur, lecteur
PDF, QCM en ligne) avec une navigation pensée pour le tactile, et les **QCM hors
ligne** (`/qcm/hors-ligne/` embarqué) qui se synchronisent avec le serveur.

- **Connexion une seule fois** : au premier lancement, identifiant et mot de
  passe (l'adresse publique `https://wiki.airhiterofprovence.fr` est déjà
  remplie). L'appli reçoit un jeton d'appareil et ouvre ensuite le wiki sans
  redemander le mot de passe (`/api/appareil/session/`).
- **Navigation au pouce** : sur téléphone, barre en bas de l'écran (Accueil,
  Parcourir, Rechercher, QCM, Hors ligne) et menu latéral en tiroir (bouton
  « Parcourir » ou glissement depuis le bord gauche). Sur tablette, menu latéral
  toujours visible. Le bouton « retour » d'Android referme d'abord le menu.
- **Fichiers** : import de `.md`, `.tex`, PDF et images par le sélecteur
  d'Android ; téléchargements (PDF, page en `.md`) par « Enregistrer sous ».
- **Lecture** : plein écran pour les PDF, zoom au pincement, taille du texte
  qui suit le réglage d'Android, thème clair ou sombre comme le téléphone.
- **Sans réseau** : la dernière version enregistrée des pages déjà vues si elle
  existe, sinon une page qui propose de réessayer ou de réviser hors ligne
  (les QCM téléchargés restent disponibles et se synchronisent au retour).

La version 2 s'installe par-dessus l'ancienne appli « QCM » (même identifiant,
même clé de signature) : sets téléchargés et réponses en attente sont gardés.

## Installer

1. Télécharger le fichier `.apk` de la dernière release :
   <https://github.com/wakadu13/Revision/releases> (tags `apk-v…`), ou sur
   le téléphone directement depuis cette page.
2. L'ouvrir sur le téléphone et autoriser l'installation depuis cette source.
3. Au premier lancement : identifiant et mot de passe du wiki (le wiki s'ouvre
   ensuite tout seul ; « Réglages » depuis le menu pour changer).
   - Adresse proposée : `https://wiki.airhiterofprovence.fr`, le wiki sur
     Internet (Cloudflare) : marche partout, en Wi‑Fi comme en 4G.
   - Adresse du réseau local, seulement à la maison : `http://192.168.1.20:8000`
     (HTTP), ou `https://192.168.1.20` avec Caddy (installer alors son
     `root.crt` sur le téléphone : Paramètres → Sécurité → Chiffrement →
     Installer un certificat → Certificat CA). Un nom de domaine tapé sans
     `https://` est complété tout seul.
   - Déjà connecté à une adresse locale ? « Passer à wiki.airhiterofprovence.fr »
     (Réglages, ou la page « Le wiki ne répond pas ») : même serveur, même jeton,
     pas de mot de passe à retaper.
4. Pour réviser sans réseau : onglet « Hors ligne », puis « Télécharger des sets ».

Le mot de passe n'est pas gardé : le serveur donne un **jeton d'appareil** à
l'application. On le révoque depuis la page **Mon compte** du wiki ; il est
aussi révoqué par « Se déconnecter » dans l'appli, par un changement de mot de
passe et quand le compte est désactivé. Il n'ouvre que l'API des QCM hors ligne,
les images des questions et `/api/appareil/session/`, qui l'échange contre une
session du wiki pour la WebView. Cette session est liée au jeton : le révoquer
la ferme aussi.

## Côté serveur (Pi)

L'application a besoin d'une version récente du wiki (`/api/appareil/session/`,
navigation tactile) ; avec un serveur plus ancien, le wiki s'affiche quand même,
mais demande le mot de passe et sans barre de navigation :

```bash
git pull
uv run python manage.py migrate     # table des jetons d'appareil
# puis redémarrer le conteneur / le serveur
```

L'adresse utilisée par le téléphone doit être dans `DJANGO_ALLOWED_HOSTS`
(ex. `DJANGO_ALLOWED_HOSTS=wiki.airhiterofprovence.fr,192.168.1.20`), sinon
Django répond 400. Si `DJANGO_HTTPS=1`, le serveur redirige HTTP vers HTTPS :
utiliser l'adresse en `https://`. Hors de la maison, l'appli passe par
l'adresse publique (Cloudflare, voir « Accès depuis Internet » dans le
[README](../README.md)) ; sans réseau, on révise quand même et tout part au retour.

## Construire l'APK

Automatique (workflow [`.github/workflows/apk.yml`](../.github/workflows/apk.yml)) :

- chaque push sur `main` qui modifie `android/` ou le moteur des QCM
  (`wiki/static/wiki/quiz.js`, `qcm_*.js`, `wiki.css`) publie une release `apk-v2.<n°>` ;
- pousser un tag `apk-vX.Y` publie la release `apk-vX.Y` :
  `git tag apk-v2.0 && git push origin apk-v2.0` ;
- sur les autres branches, l'APK est disponible en artefact du run (onglet Actions).

En local (JDK 17+, SDK Android avec la plateforme 35) :

```bash
cd android
./gradlew assembleRelease      # → app/build/outputs/apk/release/app-release.apk
```

Le build copie `quiz.js`, `qcm_attente.js`, `qcm_hors_ligne.js` et `wiki.css`
depuis `wiki/static/wiki/` (une modification du moteur de QCM du site passe
donc dans l'APK au prochain build) et télécharge KaTeX pour les formules hors ligne.

### Signature

Android n'accepte une mise à jour que si elle est signée avec la même clé.
Par défaut, la CI signe avec `android/signature/qcm.jks` (mot de passe
`projetpluri`) : pratique, mais le dépôt étant public, n'importe qui peut
signer avec. Pour une clé privée :

```bash
keytool -genkeypair -keystore qcm-prive.jks -alias qcm -keyalg RSA -keysize 3072 -validity 18250
base64 -w0 qcm-prive.jks   # → secret QCM_KEYSTORE_BASE64
```

puis créer les secrets GitHub `QCM_KEYSTORE_BASE64`, `QCM_KEYSTORE_PASSWORD`,
`QCM_KEY_ALIAS` (`qcm`) et `QCM_KEY_PASSWORD`. Changer de clé oblige à
désinstaller l'appli une fois : **synchroniser avant**, sinon les réponses
pas encore envoyées sont perdues.

## Fonctionnement

- `MainActivity.java` : WebView plein écran. Les pages du serveur s'y affichent
  directement (le site reconnaît l'appli à son User-Agent « ProjetPluriApp/ »
  et ajoute la barre de navigation) ; les autres sites s'ouvrent dans le
  navigateur. Les pages locales (`assets/` : QCM hors ligne, réglages,
  « hors réseau ») sont servies sur `https://appassets.androidplatform.net/`
  (origine sécurisée : IndexedDB garde sets et réponses sur le téléphone).
  Session expirée : la page de connexion du wiki est interceptée et la session
  rouverte avec le jeton. Sélecteur de fichiers, « Enregistrer sous » et plein
  écran sont fournis par l'appli (`WebChromeClient`, `Fichiers.java`).
- `Pont.java` (`window.QcmNatif`, pages locales seulement) : requêtes HTTP vers
  le serveur en Java, avec l'en-tête `Authorization: Bearer <jeton>` — pas de
  CORS ni de contenu mixte, HTTP ou HTTPS indifféremment ; échange du jeton
  contre la session du wiki ; passage à une autre adresse du même wiki
  (`changerServeur`, HTTPS seulement, gardée si le serveur accepte le jeton).
- `window.AppliNatif` (toutes les pages, rien de sensible) : rouvrir le wiki,
  enregistrer un fichier produit par la page (« Télécharger » de l'éditeur).
- `assets/appli.js` : `QcmReseau.fetch()`, même interface que `fetch()`, que
  les scripts du wiki utilisent quand ils tournent dans l'appli. Les images des
  questions sont copiées dans les sets téléchargés (affichées hors ligne).
- Les QCM du module Langues (FSRS) restent en ligne seulement, comme sur le site.
