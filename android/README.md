# Application Android « QCM »

APK qui embarque la page `/qcm/hors-ligne/` du wiki : on télécharge des sets
sur le téléphone, on révise **sans réseau**, et les réponses sont envoyées au
serveur (le Pi) à la prochaine synchronisation — à l'ouverture de l'appli, au
retour du réseau ou avec le bouton « Synchroniser ». Mêmes règles de Leitner
que le site : la progression est la même partout.

## Installer

1. Télécharger le fichier `.apk` de la dernière release :
   <https://github.com/wakadu13/Revision/releases> (tags `apk-v…`).
2. L'ouvrir sur le téléphone et autoriser l'installation depuis cette source.
3. Au premier lancement : adresse du serveur, identifiant et mot de passe du wiki.
   - Pi en HTTP sur le réseau local : `http://192.168.1.20:8000` (IP du Pi et port publié par Docker).
   - Pi en HTTPS : `https://wiki.exemple.fr`. Avec un certificat d'une autorité
     locale (Caddy…), installer son `root.crt` sur le téléphone
     (Paramètres → Sécurité → Chiffrement → Installer un certificat → Certificat CA).
4. « Télécharger des sets » : cocher les sets à garder sur le téléphone.

Le mot de passe n'est pas gardé : le serveur donne un **jeton d'appareil** à
l'application. On le révoque depuis la page **Mon compte** du wiki ; il est
aussi révoqué par « Se déconnecter » dans l'appli, par un changement de mot de
passe et quand le compte est désactivé. Il n'ouvre que l'API des QCM hors ligne
et les images des questions.

## Côté serveur (Pi)

L'application a besoin de la version du wiki qui contient `/api/appareil/` :

```bash
git pull
uv run python manage.py migrate     # table des jetons d'appareil
# puis redémarrer le conteneur / le serveur
```

L'adresse utilisée par le téléphone doit être dans `DJANGO_ALLOWED_HOSTS`
(ex. `DJANGO_ALLOWED_HOSTS=192.168.1.20,localhost`), sinon Django répond 400.
Si `DJANGO_HTTPS=1`, le serveur redirige HTTP vers HTTPS : utiliser l'adresse en `https://`.
Hors de la maison, le téléphone ne joint le Pi que par un VPN (Tailscale,
WireGuard…) ; sans lui, on révise quand même et tout part au retour.

## Construire l'APK

Automatique : pousser un tag `apk-vX.Y` crée la release
(workflow [`.github/workflows/apk.yml`](../.github/workflows/apk.yml)).

```bash
git tag apk-v1.1 && git push origin apk-v1.1
```

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

- `MainActivity.java` : WebView qui sert les fichiers de `assets/` sur
  `https://appassets.androidplatform.net/` (origine sécurisée : IndexedDB garde
  sets et réponses sur le téléphone).
- `Pont.java` (`window.QcmNatif`) : fait les requêtes HTTP vers le serveur en
  Java, avec l'en-tête `Authorization: Bearer <jeton>` — pas de CORS ni de
  contenu mixte, HTTP ou HTTPS indifféremment.
- `assets/appli.js` : `QcmReseau.fetch()`, même interface que `fetch()`, que
  les scripts du wiki utilisent quand ils tournent dans l'appli. Les images des
  questions sont copiées dans les sets téléchargés (affichées hors ligne).
- Les QCM du module Langues (FSRS) restent en ligne seulement, comme sur le site.
