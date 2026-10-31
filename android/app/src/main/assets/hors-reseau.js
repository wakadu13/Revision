// Page affichée quand le serveur du wiki ne répond pas (MainActivity.onReceivedError).
(function () {
  const params = new URLSearchParams(location.search);
  const adresse = params.get("url") || "";
  const $ = (id) => document.getElementById(id);
  if (params.get("ssl")) {
    $("hr-titre").textContent = "Certificat du wiki non reconnu";
    $("hr-message").textContent = "La connexion sécurisée au wiki a été refusée : son certificat n'est pas reconnu par l'appareil. "
      + "Le plus simple : passer à l'adresse publique wiki.airhiterofprovence.fr (Réglages), dont le certificat est reconnu partout. "
      + "Pour garder l'adresse locale de Caddy, installez son fichier root.crt : Paramètres → Sécurité → "
      + "Chiffrement et identifiants → Installer un certificat → Certificat CA.";
  }
  if (adresse) $("hr-adresse").textContent = "Adresse : " + adresse;
  $("hr-reessayer").addEventListener("click", () => {
    if (/^https?:\/\//.test(adresse)) location.replace(adresse);
    else if (window.AppliNatif) window.AppliNatif.ouvrirWiki();
  });
  // Adresse du réseau local, hors de la maison : passer à l'adresse publique
  // du wiki en gardant le jeton (pas de mot de passe à retaper).
  const R = window.QcmReseau;
  if (R && R.connecte() && R.locale(R.serveur())) {
    const passer = $("hr-passer");
    passer.textContent = "Passer à " + R.PUBLIQUE.replace(/^https:\/\//, "");
    passer.hidden = false;
    $("hr-reessayer").classList.remove("primary");
    passer.addEventListener("click", async () => {
      passer.disabled = true;
      const statut = await R.changerServeur(R.PUBLIQUE);
      passer.disabled = false;
      if (statut === 200) {
        window.AppliNatif.ouvrirWiki();
        return;
      }
      $("hr-message").textContent = statut === 0
        ? "L'adresse publique ne répond pas non plus : pas de connexion Internet, ou serveur éteint."
        : "Le serveur n'a pas accepté cet appareil à l'adresse publique : Réglages → « Se déconnecter », puis se reconnecter.";
    });
  }

  // Réessaie tout seul quand le réseau revient.
  window.addEventListener("online", () => $("hr-reessayer").click());
})();
