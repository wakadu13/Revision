// Page affichée quand le serveur du wiki ne répond pas (MainActivity.onReceivedError).
(function () {
  const params = new URLSearchParams(location.search);
  const adresse = params.get("url") || "";
  const $ = (id) => document.getElementById(id);
  if (params.get("ssl")) {
    $("hr-titre").textContent = "Certificat du wiki non reconnu";
    $("hr-message").textContent = "La connexion sécurisée au wiki a été refusée : son certificat n'est pas reconnu par l'appareil. "
      + "Avec Caddy (HTTPS sur le réseau local), installez son fichier root.crt : Paramètres → Sécurité → "
      + "Chiffrement et identifiants → Installer un certificat → Certificat CA.";
  }
  if (adresse) $("hr-adresse").textContent = "Adresse : " + adresse;
  $("hr-reessayer").addEventListener("click", () => {
    if (/^https?:\/\//.test(adresse)) location.replace(adresse);
    else if (window.AppliNatif) window.AppliNatif.ouvrirWiki();
  });
  // Réessaie tout seul quand le réseau revient.
  window.addEventListener("online", () => $("hr-reessayer").click());
})();
