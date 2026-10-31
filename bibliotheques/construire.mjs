// Reconstruit les bibliothèques servies par le site (wiki/static/wiki/vendor/) :
//   npm ci && npm run build
import { build } from "esbuild";
import { copyFileSync, mkdirSync, rmSync, writeFileSync } from "node:fs";

const OUT = "../wiki/static/wiki/vendor";
const PDFJS = "node_modules/pdfjs-dist";

// La feuille de style de PDF.js sert aussi à son application complète : elle
// contient des règles globales (.sidebar, .dialog...) qui abîmeraient la mise en
// page du wiki. On ne garde que celles des pages du document.
const VIEWER_RULES = /^(:root|@media|\.pdfViewer|\.spread|\.page:has|\.canvasWrapper|\.textLayer|\.annotationLayer|:is\(\.annotationLayer|\.annotationEditorLayer|\.xfa|:is\(\.xfa|\[data-(main|editor)-rotation)/;

function viewerRules(text) {
  const kept = [];
  let depth = 0;
  let start = 0;
  let quote = null;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quote) {
      if (c === "\\") i++;
      else if (c === quote) quote = null;
    } else if (c === '"' || c === "'") {
      quote = c;
    } else if (c === "{") {
      depth++;
    } else if (c === "}" && --depth === 0) {
      const rule = text.slice(start, i + 1);
      if (VIEWER_RULES.test(rule.trimStart()) && !/^@media[^{]*\{\s*\.(sidebar|dialog|toggle-button)/.test(rule)) kept.push(rule);
      start = i + 1;
    }
  }
  return kept.join("\n") + "\n";
}

// Éditeur de pages : CodeMirror 6, exposé dans la variable globale « CM ».
await build({
  entryPoints: ["codemirror.js"],
  bundle: true,
  minify: true,
  format: "iife",
  globalName: "CM",
  target: "es2020",
  legalComments: "eof",
  banner: { js: "/* CodeMirror 6 et Lezer (licence MIT, https://codemirror.net) : regroupés par bibliotheques/codemirror.js, ne pas modifier à la main. */" },
  outfile: `${OUT}/codemirror.min.js`,
});

// Lecteur de PDF : PDF.js (module ES), son « worker », ses décodeurs d'images
// (JBIG2 et JPEG 2000 des PDF scannés, profils de couleur) et sa feuille de style.
rmSync(`${OUT}/pdfjs`, { recursive: true, force: true });
mkdirSync(`${OUT}/pdfjs/wasm`, { recursive: true });
await build({
  entryPoints: ["pdf.js"],
  bundle: true,
  minify: true,
  format: "esm",
  legalComments: "eof",
  banner: { js: "/* PDF.js (Mozilla, licence Apache 2.0, https://mozilla.github.io/pdf.js/) : regroupé par bibliotheques/pdf.js, ne pas modifier à la main. */" },
  outfile: `${OUT}/pdfjs/pdf.min.js`,
});
const css = await build({
  entryPoints: [`${PDFJS}/legacy/web/pdf_viewer.css`],
  bundle: true,
  minify: true,
  write: false,
  loader: { ".svg": "dataurl", ".gif": "dataurl", ".png": "dataurl" },
  outfile: "pdf_viewer.min.css",
});
writeFileSync(`${OUT}/pdfjs/pdf_viewer.min.css`, viewerRules(css.outputFiles[0].text));
copyFileSync(`${PDFJS}/legacy/build/pdf.worker.min.mjs`, `${OUT}/pdfjs/pdf.worker.min.js`);
copyFileSync(`${PDFJS}/LICENSE`, `${OUT}/pdfjs/LICENSE`);
for (const file of ["jbig2.wasm", "openjpeg.wasm", "qcms_bg.wasm", "LICENSE_JBIG2", "LICENSE_OPENJPEG",
  "LICENSE_QCMS", "LICENSE_PDFJS_JBIG2", "LICENSE_PDFJS_OPENJPEG", "LICENSE_PDFJS_QCMS"]) {
  copyFileSync(`${PDFJS}/wasm/${file}`, `${OUT}/pdfjs/wasm/${file}`);
}
console.log(`Bibliothèques écrites dans ${OUT}/`);
