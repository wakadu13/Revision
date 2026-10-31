// Connexion de l'application au serveur du wiki : identifiants contre un jeton
// d'appareil (/api/appareil/connexion/), gardé par le code natif.
(function () {
  const R = window.QcmReseau;
  const $ = (id) => document.getElementById(id);
  if (!R) return;
  const ADRESSE_PUBLIQUE = R.PUBLIQUE;

  function afficher() {
    const connecte = R.connecte();
    $("cx-connecte").hidden = !connecte;
    $("cx-formulaire").hidden = connecte;
    $("cx-retour").hidden = !connecte;
    $("cx-serveur").textContent = R.serveur();
    $("cx-joueur").textContent = R.joueur();
    if (!connecte) $("cx-adresse").value = R.serveur() || ADRESSE_PUBLIQUE;
    $("cx-conseil").hidden = !connecte || !R.locale(R.serveur());
    suggerer();
  }

  // Ancienne adresse du réseau local gardée : proposer l'adresse publique.
  function suggerer() {
    let actuelle = "";
    try { actuelle = normaliser($("cx-adresse").value); } catch (e) { /* saisie en cours */ }
    $("cx-suggestion").hidden = actuelle === ADRESSE_PUBLIQUE;
    $("cx-adresse-publique").textContent = "Utiliser " + ADRESSE_PUBLIQUE.replace(/^https:\/\//, "");
  }

  function erreur(texte) {
    $("cx-erreur").hidden = !texte;
    $("cx-erreur-texte").textContent = texte || "";
  }

  // « 192.168.1.20:8000/ » → « http://192.168.1.20:8000 » ; un nom de domaine
  // sans port (« wiki.exemple.fr ») → « https://wiki.exemple.fr ».
  function normaliser(adresse) {
    adresse = adresse.trim().replace(/\/+$/, "");
    if (!/^https?:\/\//i.test(adresse)) {
      const hote = adresse.split("/")[0];
      const local = /^[\d.]+(:\d+)?$/.test(hote) || /^\[|:\d+$|^localhost\b/i.test(hote);
      adresse = (local ? "http://" : "https://") + adresse;
    }
    const u = new URL(adresse);
    return u.origin + u.pathname.replace(/\/+$/, "");
  }

  async function lireErreur(r) {
    try { return (await r.json()).error || ("erreur " + r.status); } catch (e) { return "erreur " + r.status; }
  }

  $("cx-formulaire").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    erreur("");
    let serveur;
    try { serveur = normaliser($("cx-adresse").value); } catch (e) { erreur("Adresse invalide."); return; }
    $("cx-valider").disabled = true;
    try {
      const r = await R.fetch(serveur + "/api/appareil/connexion/", {
        method: "POST",
        body: JSON.stringify({ username: $("cx-utilisateur").value.trim(), password: $("cx-mdp").value, appareil: window.QcmNatif.nomAppareil() }),
      });
      if (r.status >= 300 && r.status < 400) {
        const vers = r.headers.get("Location") || "";
        if (/^https:\/\//i.test(vers) && serveur.startsWith("http://")) {
          erreur("Le serveur demande HTTPS : utilisez l'adresse " + serveur.replace(/^http:/i, "https:"));
        } else erreur("Le serveur redirige vers " + (vers || "une autre adresse") + " : vérifiez l'adresse.");
        return;
      }
      const type = r.headers.get("Content-Type") || "";
      if (r.status === 404 || !type.includes("json")) {
        erreur("Pas de wiki à cette adresse (ou serveur pas à jour : il faut la version avec l'application Android).");
        return;
      }
      if (!r.ok) { erreur(await lireErreur(r)); return; }
      const data = await r.json();
      window.QcmNatif.enregistrerCompte(serveur, data.jeton, data.joueur);
      if (window.AppliNatif) window.AppliNatif.ouvrirWiki();
      else location.replace("index.html");
    } catch (e) {
      erreur(e.message + ". Vérifiez l'adresse et la connexion Internet (une adresse en 192.168.… ne marche"
        + " que sur le Wi‑Fi de la maison).");
    } finally {
      $("cx-valider").disabled = false;
      $("cx-mdp").value = "";
    }
  });

  $("cx-deconnecter").addEventListener("click", async () => {
    if (!confirm("Se déconnecter ? Les sets téléchargés et les réponses pas encore synchronisées restent sur le téléphone.")) return;
    // Révoque le jeton côté serveur si possible ; sinon il reste révocable depuis « Mon compte ».
    try { await R.fetch("/api/appareil/deconnexion/", { method: "POST", body: "{}" }); } catch (e) { /* hors ligne */ }
    window.QcmNatif.oublierCompte();
    afficher();
  });

  // Connecté à l'adresse locale : passer à l'adresse publique en gardant le jeton.
  $("cx-passer").textContent = "Passer à " + ADRESSE_PUBLIQUE.replace(/^https:\/\//, "");
  $("cx-passer").addEventListener("click", async () => {
    const etat = $("cx-passer-etat");
    $("cx-passer").disabled = true;
    etat.textContent = "Vérification…";
    const statut = await R.changerServeur(ADRESSE_PUBLIQUE);
    $("cx-passer").disabled = false;
    if (statut === 200) {
      etat.textContent = "";
      afficher();
      if (window.AppliNatif) window.AppliNatif.ouvrirWiki();
      return;
    }
    etat.textContent = statut === 0 ? "Adresse publique injoignable pour l'instant : vérifiez la connexion Internet."
      : statut === 401 ? "Ce serveur ne reconnaît pas cet appareil : « Se déconnecter », puis se reconnecter avec cette adresse."
      : (statut > 0 ? "Le serveur a répondu " + statut + " (pas à jour ?). " : "")
        + "« Se déconnecter », puis se reconnecter avec cette adresse.";
  });

  $("cx-adresse").addEventListener("input", suggerer);
  $("cx-adresse-publique").addEventListener("click", () => {
    $("cx-adresse").value = ADRESSE_PUBLIQUE;
    suggerer();
    $("cx-utilisateur").focus();
  });

  $("cx-revoque").hidden = !/[?&]revoque=1/.test(location.search) || R.connecte();
  afficher();
})();
