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

    // Le wiki sur Internet (Cloudflare) : joignable de partout, certificat reconnu.
    PUBLIQUE: "https://wiki.airhiterofprovence.fr",
    // Adresse du réseau local (IP privée, nom en .local, localhost) : injoignable hors de la maison.
    locale(adresse) {
      try {
        const hote = new URL(adresse).hostname;
        return /^(10|127|192\.168|172\.(1[6-9]|2\d|3[01]))\./.test(hote) || /\.local$|^localhost$/i.test(hote);
      } catch (e) { return false; }
    },

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

    // Autre adresse du même wiki, en gardant le jeton (Pont.changerServeur) :
    // résout le statut HTTP (200 : fait ; 401 : appareil inconnu ; 0 : injoignable).
    changerServeur(adresse) {
      return new Promise((resoudre) => {
        const id = String(++compteur);
        enAttente.set(id, { resoudre, rejeter: resoudre });
        natif.changerServeur(id, adresse);
      });
    },

    _statut(id, statut) {
      const p = enAttente.get(id);
      if (!p) return;
      enAttente.delete(id);
      p.resoudre(statut);
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
