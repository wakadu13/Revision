// Lecteur de PDF : PDF.js de Mozilla (licence Apache 2.0, https://mozilla.github.io/pdf.js/),
// version « legacy » pour les navigateurs de téléphone un peu anciens. Utilisé par
// wiki/static/wiki/lecteur_pdf.js.
//
// La bibliothèque doit être évaluée avant les composants d'affichage : elle
// définit globalThis.pdfjsLib, qu'ils utilisent.
import * as pdfjsLib from "pdfjs-dist/legacy/build/pdf.mjs";

export { pdfjsLib };
export {
  EventBus, FindState, LinkTarget, PDFFindController, PDFLinkService, PDFViewer,
} from "pdfjs-dist/legacy/web/pdf_viewer.mjs";
