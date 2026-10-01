// Page d'accueil des QCM : catégories repliables (état mémorisé) et recherche
// en direct dans les sets (titre, description, catégorie, énoncés).
(function () {
  const input = document.querySelector("[data-quiz-search]");
  const empty = document.querySelector("[data-quiz-empty]");
  const categories = Array.from(document.querySelectorAll(".quiz-category"));
  const STORAGE_KEY = "qcm-categories-ouvertes";

  // Même normalisation que quiz.normaliser_texte côté serveur.
  function normalize(text) {
    return text.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase().split(/\s+/).filter(Boolean);
  }

  function nameOf(details) {
    return details.querySelector(".quiz-category-name").textContent;
  }

  function loadOpen() {
    try { return new Set(JSON.parse(localStorage.getItem(STORAGE_KEY)) || []); } catch (e) { return new Set(); }
  }

  function saveOpen() {
    try {
      const open = categories.filter((d) => d.open).map(nameOf);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(open));
    } catch (e) { /* stockage indisponible : l'état n'est simplement pas mémorisé */ }
  }

  let searching = false;

  function filter() {
    const words = normalize(input ? input.value : "");
    searching = words.length > 0;
    const remembered = searching ? null : loadOpen();
    let total = 0;
    for (const details of categories) {
      let shown = 0;
      for (const set of details.querySelectorAll(".quiz-set")) {
        const haystack = set.dataset.search;
        const match = words.every((w) => haystack.includes(w));
        set.hidden = !match;
        if (match) shown++;
      }
      total += shown;
      details.hidden = shown === 0;
      details.open = searching ? shown > 0 : remembered.has(nameOf(details));
      const count = details.querySelector("[data-quiz-count]");
      if (count) count.textContent = shown + (shown > 1 ? " sets" : " set");
    }
    if (empty) empty.hidden = !searching || total > 0;
  }

  for (const details of categories) {
    // Pendant une recherche, ouvrir/fermer ne modifie pas l'état mémorisé.
    details.addEventListener("toggle", () => { if (!searching) saveOpen(); });
  }

  document.querySelectorAll("[data-fold]").forEach((button) => {
    button.addEventListener("click", () => {
      const open = button.dataset.fold === "open";
      categories.forEach((d) => { if (!d.hidden) d.open = open; });
    });
  });

  if (input) {
    input.addEventListener("input", () => {
      filter();
      // Garde la recherche dans l'URL (lien partageable, retour arrière).
      const url = new URL(location.href);
      if (input.value.trim()) url.searchParams.set("q", input.value.trim());
      else url.searchParams.delete("q");
      history.replaceState(null, "", url);
    });
    input.addEventListener("keydown", (e) => {
      if (e.key === "Escape") { input.value = ""; input.dispatchEvent(new Event("input")); }
    });
    input.form.addEventListener("submit", (e) => e.preventDefault());
  }

  filter();
})();
