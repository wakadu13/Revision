// Palette de commandes (Ctrl+K, comme le sélecteur rapide d'Obsidian) : ouvrir
// une page, un PDF ou un QCM, lancer une session de langue, ou une commande
// (thème, plein écran, nouvelle page…), au clavier. Les données viennent de
// /palette.json, chargé à la première ouverture.
(function () {
  "use strict";
  let dialog = null;
  let input = null;
  let liste = null;
  let donnees = null;
  let chargement = null;
  let resultats = [];
  let selection = 0;

  const normaliser = (s) => s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();

  function construire() {
    dialog = document.createElement("dialog");
    dialog.className = "palette";
    dialog.setAttribute("aria-label", "Ouvrir une page ou une commande");
    input = document.createElement("input");
    input.type = "text";
    input.placeholder = "Page, PDF, QCM, langue ou commande…";
    input.setAttribute("autocomplete", "off");
    input.setAttribute("spellcheck", "false");
    liste = document.createElement("ul");
    liste.setAttribute("role", "listbox");
    const aide = document.createElement("p");
    aide.className = "palette-aide";
    aide.textContent = "↑ ↓ choisir · Entrée ouvrir · Échap fermer";
    dialog.append(input, liste, aide);
    document.body.appendChild(dialog);
    input.addEventListener("input", filtrer);
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (!resultats.length) return;
        selection = (selection + (e.key === "ArrowDown" ? 1 : resultats.length - 1)) % resultats.length;
        afficher();
      } else if (e.key === "Enter") {
        e.preventDefault();
        if (resultats[selection]) ouvrir(resultats[selection]);
      }
    });
    liste.addEventListener("click", (e) => {
      const li = e.target.closest("li[data-i]");
      if (li) ouvrir(resultats[Number(li.dataset.i)]);
    });
    dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });
  }

  function charger() {
    if (!chargement) {
      chargement = fetch("/palette.json", { headers: { Accept: "application/json" } })
        .then((r) => (r.ok ? r.json() : Promise.reject(new Error(r.status))))
        .then((d) => {
          const genre = (items, g) => items.map((x) => ({ ...x, g }));
          donnees = [
            ...genre(d.commandes, "Commande"),
            ...genre(d.langues, "Langue"),
            ...genre(d.pages, "Page"),
            ...genre(d.qcm, "QCM"),
          ].map((x) => ({ ...x, n: normaliser(x.t + " " + (x.s || "")) }));
        })
        .catch(() => { chargement = null; donnees = []; });
    }
    return chargement;
  }

  // Score : début du titre > début d'un mot > contenu > lettres dans l'ordre.
  function score(item, mots) {
    let total = 0;
    for (const mot of mots) {
      const i = item.n.indexOf(mot);
      if (i === 0) total += 100;
      else if (i > 0 && item.n[i - 1] === " ") total += 60;
      else if (i > 0) total += 30;
      else {
        let k = 0;
        for (const c of item.n) { if (c === mot[k]) k++; if (k === mot.length) break; }
        if (k < mot.length) return -1;
        total += 5;
      }
    }
    return total - item.n.length / 200;
  }

  function filtrer() {
    const q = normaliser(input.value.trim());
    if (!donnees) { resultats = []; afficher(); return; }
    if (!q) {
      resultats = donnees.filter((x) => x.g === "Commande" || x.g === "Langue").slice(0, 14);
    } else {
      const mots = q.split(/\s+/);
      resultats = donnees
        .map((x) => ({ x, s: score(x, mots) }))
        .filter((r) => r.s >= 0)
        .sort((a, b) => b.s - a.s)
        .slice(0, 14)
        .map((r) => r.x);
    }
    selection = 0;
    afficher();
  }

  function afficher() {
    liste.replaceChildren();
    if (!resultats.length) {
      const vide = document.createElement("li");
      vide.className = "palette-vide";
      vide.textContent = donnees ? "Rien ne correspond." : "Chargement…";
      liste.appendChild(vide);
      return;
    }
    resultats.forEach((x, i) => {
      const li = document.createElement("li");
      li.dataset.i = String(i);
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", String(i === selection));
      const genre = document.createElement("span");
      genre.className = "palette-genre";
      genre.textContent = x.g;
      const titre = document.createElement("span");
      titre.className = "palette-titre";
      titre.textContent = x.t;
      li.append(genre, titre);
      if (x.s) {
        const sous = document.createElement("span");
        sous.className = "palette-sous";
        sous.textContent = x.s;
        li.appendChild(sous);
      }
      liste.appendChild(li);
    });
    const actif = liste.querySelector('[aria-selected="true"]');
    if (actif) actif.scrollIntoView({ block: "nearest" });
  }

  function ouvrir(item) {
    dialog.close();
    if (item.a === "theme") { if (window.wikiTheme) window.wikiTheme.cycle(); return; }
    if (item.a === "fullscreen") { if (window.wikiPleinEcran) window.wikiPleinEcran.basculer(); return; }
    if (item.a === "edit") {
      const lien = document.querySelector("[data-edit-shortcut]");
      if (lien) window.location.href = lien.href;
      return;
    }
    if (item.u) window.location.href = item.u;
  }

  function basculer() {
    if (!dialog) construire();
    if (dialog.open) { dialog.close(); return; }
    input.value = "";
    resultats = [];
    dialog.showModal();
    afficher();
    charger().then(filtrer);
    input.focus();
  }

  document.addEventListener("keydown", (e) => {
    if (!(e.ctrlKey || e.metaKey) || e.altKey || e.shiftKey) return;
    const k = e.key.toLowerCase();
    if (k !== "k" && k !== "p") return;
    // Dans l'éditeur, Ctrl+K insère un lien.
    if (k === "k" && e.target.closest(".cm-editor")) return;
    if (document.querySelector("dialog[open]:not(.palette)")) return;
    e.preventDefault();
    basculer();
  });
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-palette]")) basculer();
  });
  window.wikiPalette = { basculer };
})();
