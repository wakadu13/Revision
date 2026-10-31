# Bibliothèques JavaScript du wiki

Deux bibliothèques sont regroupées dans `wiki/static/wiki/vendor/` et servies par
le site lui-même : pas de CDN, et rien à installer pour faire tourner le wiki.

| Fichiers | Bibliothèque | Utilisée par |
|---|---|---|
| `codemirror.min.js` | [CodeMirror 6](https://codemirror.net) (licence MIT), le moteur d'édition d'Obsidian | l'éditeur de pages (`wiki/static/wiki/editor.js`) |
| `pdfjs/` | [PDF.js](https://mozilla.github.io/pdf.js/) de Mozilla (licence Apache 2.0), version « legacy » pour les navigateurs de téléphone un peu anciens | le lecteur de PDF (`wiki/static/wiki/lecteur_pdf.js`) |

`pdfjs/wasm/` contient les décodeurs d'images des PDF scannés (JBIG2, JPEG 2000)
et de profils de couleur. Ils tournent dans le « worker » de PDF.js, qui n'est pas
soumis à la politique de sécurité (CSP) des pages : celle-ci reste stricte. Les
polices et tables de caractères asiatiques (`cmaps`) ne sont pas incluses.

Ce dossier ne sert qu'à **reconstruire** ces fichiers (mise à jour, nouveau
langage pour la coloration des blocs de code...). Il faut Node.js :

```bash
cd bibliotheques
npm ci          # installe les versions figées de package-lock.json
npm run build   # réécrit ../wiki/static/wiki/vendor/
```

- `codemirror.js` : ce qui est exposé à `editor.js` (variable globale `CM`) et
  les langages reconnus dans les blocs de code (` ```bash `, ` ```python `...).
- `pdf.js` : ce qui est exposé à `lecteur_pdf.js` (module ES).
- `construire.mjs` : le script de construction (esbuild).
- Mettre à jour : `npm update`, `npm run build`, vérifier l'éditeur et le
  lecteur dans le navigateur, puis committer `package-lock.json` et
  `wiki/static/wiki/vendor/`.
