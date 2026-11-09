// « Demander au wiki » : question envoyée au serveur (qui choisit les extraits et
// interroge Claude) ; la réponse et ses sources s'affichent en haut de la liste.
(function () {
  "use strict";
  const page = document.getElementById("demander");
  if (!page) return;
  const form = page.querySelector("[data-demander-form]");
  const zone = page.querySelector("[data-demander-echanges]");
  if (!form) return;
  const champ = form.querySelector("textarea");
  const bouton = form.querySelector("button");

  function el(tag, cls, texte) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (texte !== undefined) e.textContent = texte;
    return e;
  }

  function sources(liste) {
    const details = el("details", "demander-sources");
    details.open = true;
    details.append(el("summary", "", `Sources (${liste.length})`));
    const ol = el("ol");
    for (const s of liste) {
      const li = el("li", s.cite ? "cite" : "");
      li.value = s.n;
      const a = el("a", "", s.titre);
      a.href = s.url;
      li.append(a);
      ol.append(li);
    }
    details.append(ol);
    return details;
  }

  async function demander() {
    const question = champ.value.trim();
    if (!question || bouton.disabled) return;
    bouton.disabled = true;
    bouton.textContent = "Claude cherche dans le wiki…";
    const bloc = el("div", "tuteur-echange demander-echange");
    bloc.append(el("p", "tuteur-question", question));
    const reponse = el("div", "tuteur-reponse markdown muted", "…");
    bloc.append(reponse);
    zone.prepend(bloc);
    for (const d of zone.querySelectorAll(".demander-sources[open]")) d.open = false;
    try {
      const r = await fetch(page.dataset.url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": page.dataset.csrf },
        body: JSON.stringify({ question }),
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || "Réponse impossible pour l'instant (" + r.status + ").");
      reponse.classList.remove("muted");
      reponse.innerHTML = data.html;
      if (window.wikiEnhance) window.wikiEnhance(reponse); // formules, coloration
      if (data.sources && data.sources.length) bloc.append(sources(data.sources));
      champ.value = "";
    } catch (e) {
      reponse.classList.add("tuteur-erreur");
      reponse.textContent = e.message;
    } finally {
      bouton.disabled = false;
      bouton.textContent = "Demander";
      champ.focus();
    }
  }

  form.addEventListener("submit", (e) => { e.preventDefault(); demander(); });
  champ.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); demander(); }
  });
  if (champ.value) champ.setSelectionRange(champ.value.length, champ.value.length);
  champ.focus();
})();
