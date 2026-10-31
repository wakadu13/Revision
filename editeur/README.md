# Bibliothèques de l'éditeur

L'éditeur de pages (`wiki/static/wiki/editor.js`) utilise
[CodeMirror 6](https://codemirror.net) (licence MIT), le moteur d'édition
d'Obsidian. Ses paquets sont regroupés en un seul fichier,
`wiki/static/wiki/vendor/codemirror.min.js`, servi par le site lui-même : pas
de CDN, et rien à installer pour faire tourner le wiki.

Ce dossier ne sert qu'à **reconstruire** ce fichier (mise à jour de CodeMirror,
nouveau langage pour la coloration des blocs de code...). Il faut Node.js :

```bash
cd editeur
npm ci          # installe les versions figées de package-lock.json
npm run build   # écrit ../wiki/static/wiki/vendor/codemirror.min.js
```

- `codemirror.js` : ce qui est exposé à `editor.js` (variable globale `CM`) et
  les langages reconnus dans les blocs de code (` ```bash `, ` ```python `...).
- Mettre à jour : `npm update`, `npm run build`, vérifier l'éditeur dans le
  navigateur, puis committer `package-lock.json` et le fichier reconstruit.
