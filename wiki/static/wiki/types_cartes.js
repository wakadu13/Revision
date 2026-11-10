// Types de cartes de vocabulaire : les libellés suivent la langue tapée dans le
// formulaire (« Carte définition → mot (IT → IT) » pour l'italien), comme sur les
// cartes créées. Même règle que langues.abreviation() côté serveur.
(function () {
  "use strict";
  const source = document.getElementById("abreviations-langues");
  if (!source) return;
  const connues = JSON.parse(source.textContent);

  function abreviation(langue) {
    const l = langue.trim().toLowerCase();
    return connues[l] || [...l].filter((c) => /\p{L}/u.test(c)).slice(0, 2).join("").toUpperCase();
  }

  for (const form of document.querySelectorAll("form")) {
    const champ = form.querySelector("input[name=langue]");
    const libelles = [...form.querySelectorAll("[data-modele]")];
    if (!champ || !libelles.length) continue;
    const majLibelles = () => {
      const langue = champ.value.trim() || "Anglais";
      const abr = abreviation(langue) || "?";
      for (const l of libelles) {
        l.textContent = l.dataset.modele.replaceAll("{L}", abr).replaceAll("{langue}", langue.toLowerCase());
      }
    };
    champ.addEventListener("input", majLibelles);
    champ.addEventListener("change", majLibelles);
    majLibelles();
  }
})();
