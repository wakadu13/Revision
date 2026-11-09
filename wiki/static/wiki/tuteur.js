// Tuteur d'une page : question envoyée à Claude, réponse ajoutée au panneau.
(function () {
  "use strict";
  const panneau = document.getElementById("tuteur");
  if (!panneau) return;
  const form = panneau.querySelector("[data-tuteur-form]");
  const zone = panneau.querySelector("[data-tuteur-echanges]");
  if (!form) return;
  const champ = form.querySelector("textarea");
  const bouton = form.querySelector("button");

  function el(tag, cls, texte) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (texte !== undefined) e.textContent = texte;
    return e;
  }

  async function demander() {
    const question = champ.value.trim();
    if (!question || bouton.disabled) return;
    bouton.disabled = true;
    bouton.textContent = "Claude réfléchit…";
    const bloc = el("div", "tuteur-echange");
    bloc.append(el("p", "tuteur-question", question));
    const reponse = el("div", "tuteur-reponse markdown muted", "…");
    bloc.append(reponse);
    zone.append(bloc);
    bloc.scrollIntoView({ block: "nearest" });
    try {
      const r = await fetch(panneau.dataset.tuteurUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": panneau.dataset.csrf },
        body: JSON.stringify({ page: panneau.dataset.page, question }),
      });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || "Réponse impossible pour l'instant (" + r.status + ").");
      reponse.classList.remove("muted");
      reponse.innerHTML = data.html;
      if (window.wikiEnhance) window.wikiEnhance(reponse); // formules, coloration
      champ.value = "";
    } catch (e) {
      reponse.classList.add("tuteur-erreur");
      reponse.textContent = e.message;
    } finally {
      bouton.disabled = false;
      bouton.textContent = "Demander";
    }
  }

  form.addEventListener("submit", (e) => { e.preventDefault(); demander(); });
  champ.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); demander(); }
  });
})();
