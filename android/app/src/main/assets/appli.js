// Application Android : relie la page au code natif (window.QcmNatif, Pont.java).
// QcmReseau.fetch() a la même interface que fetch() : les scripts du wiki
// (qcm_attente.js, qcm_hors_ligne.js) l'utilisent à sa place quand il existe.
(function () {
  const natif = window.QcmNatif;
  if (!natif) return;
  window.QUIZ_CDN = "lib/"; // KaTeX embarqué (formules hors ligne)

  const enAttente = new Map();
  let compteur = 0;

  function octets(base64) {
    const binaire = atob(base64);
    const t = new Uint8Array(binaire.length);
    for (let i = 0; i < binaire.length; i++) t[i] = binaire.charCodeAt(i);
    return t;
  }

  window.QcmReseau = {
    serveur: () => natif.serveur(),
    joueur: () => natif.joueur(),
    connecte: () => natif.connecte(),

    fetch(url, options) {
      options = options || {};
      return new Promise((resoudre, rejeter) => {
        const id = String(++compteur);
        enAttente.set(id, { resoudre, rejeter });
        natif.requete(id, options.method || "GET", String(url), options.body == null ? null : String(options.body));
      });
    },

    _fin(id, statut, type, location, base64) {
      const p = enAttente.get(id);
      if (!p) return;
      enAttente.delete(id);
      const vide = statut === 204 || statut === 205 || statut === 304;
      const entetes = { "Content-Type": type };
      if (location) entetes.Location = location;
      p.resoudre(new Response(vide ? null : octets(base64), { status: statut, headers: entetes }));
    },

    _echec(id, message) {
      const p = enAttente.get(id);
      if (!p) return;
      enAttente.delete(id);
      p.rejeter(new TypeError("Serveur injoignable (" + message + ")"));
    },
  };

  // Boutons « Wiki » : rouvrent le wiki (session ouverte avec le jeton).
  document.addEventListener("click", (e) => {
    const lien = e.target.closest && e.target.closest("[data-ouvrir-wiki]");
    if (!lien || !window.AppliNatif) return;
    e.preventDefault();
    window.AppliNatif.ouvrirWiki();
  });

  // Pas encore de compte : écran de connexion.
  if (!natif.connecte() && !/connexion\.html$/.test(location.pathname)) location.replace("connexion.html");
})();
