// « Corriger ma copie » : aperçu des photos choisies, envoi au serveur (qui interroge
// Claude), correction ajoutée en tête de l'historique ; suppression d'une correction.
(function () {
  "use strict";
  const page = document.getElementById("copie");
  if (!page) return;
  const form = page.querySelector("[data-copie-form]");
  const historique = page.querySelector("[data-copie-historique]");
  const csrf = page.dataset.csrf;
  const max = Number(page.dataset.max) || 4;

  historique.addEventListener("click", async (e) => {
    const bouton = e.target.closest("[data-copie-supprimer]");
    if (!bouton) return;
    const bloc = bouton.closest("[data-copie]");
    if (!window.confirm("Supprimer cette correction et ses photos ?")) return;
    const r = await fetch(`${page.dataset.url}${bloc.dataset.copie}/supprimer/`, { method: "POST", headers: { "X-CSRFToken": csrf } });
    if (r.ok) bloc.remove();
  });

  if (!form) return;
  const champ = form.querySelector("[data-copie-photos]");
  const apercu = form.querySelector("[data-copie-apercu]");
  const etat = form.querySelector("[data-copie-etat]");
  const bouton = form.querySelector("button[type=submit]");
  let photos = [];

  function dire(texte, classe) {
    etat.textContent = texte;
    etat.className = classe || "";
  }

  // Photo d'appareil (souvent 4000 px et plusieurs Mo) : réduite à 2000 px en JPEG avant
  // l'envoi, plus rapide sur un téléphone ; le serveur la réduit encore pour Claude.
  async function reduire(f) {
    if (!window.createImageBitmap || !f.type.startsWith("image/")) return f;
    try {
      const image = await createImageBitmap(f, { imageOrientation: "from-image" });
      const k = Math.min(1, 2000 / Math.max(image.width, image.height));
      if (k === 1 && f.size < 1500000) return f;
      const toile = document.createElement("canvas");
      toile.width = Math.round(image.width * k);
      toile.height = Math.round(image.height * k);
      toile.getContext("2d").drawImage(image, 0, 0, toile.width, toile.height);
      const blob = await new Promise((res) => toile.toBlob(res, "image/jpeg", 0.85));
      return blob ? new File([blob], f.name.replace(/\.\w+$/, "") + ".jpg", { type: "image/jpeg" }) : f;
    } catch (e) {
      return f; // format que le navigateur ne sait pas lire : envoyé tel quel
    }
  }

  function montrer() {
    apercu.replaceChildren(...photos.map((f, i) => {
      const fig = document.createElement("figure");
      const img = document.createElement("img");
      img.alt = "Page " + (i + 1);
      const lecteur = new FileReader(); // data: (les adresses blob: sont refusées par la politique de sécurité)
      lecteur.onload = () => { img.src = lecteur.result; };
      lecteur.readAsDataURL(f);
      const retirer = document.createElement("button");
      retirer.type = "button";
      retirer.className = "link-button";
      retirer.textContent = "✕";
      retirer.setAttribute("aria-label", "Retirer la page " + (i + 1));
      retirer.addEventListener("click", () => { photos.splice(i, 1); montrer(); });
      const legende = document.createElement("figcaption");
      legende.append("Page " + (i + 1) + " ", retirer);
      fig.append(img, legende);
      return fig;
    }));
  }

  champ.addEventListener("change", () => {
    const nouvelles = [...champ.files].filter((f) => f.type.startsWith("image/") || /\.(jpe?g|png|webp|heic)$/i.test(f.name));
    photos = photos.concat(nouvelles).slice(0, max);
    if (photos.length === max && nouvelles.length) dire(`${max} pages au plus.`);
    else dire("");
    champ.value = "";
    montrer();
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!photos.length) return dire("Ajoutez au moins une photo de la copie.", "erreur");
    const corps = new FormData();
    bouton.disabled = true;
    dire("Préparation des photos…");
    try {
      for (const f of photos) {
        const reduite = await reduire(f);
        corps.append("photos", reduite, reduite.name);
      }
      corps.append("enonce", form.elements.enonce.value);
      corps.append("page", form.elements.page.value);
      dire("Claude lit et corrige la copie… (jusqu'à une minute)");
      const r = await fetch(page.dataset.url, { method: "POST", body: corps, headers: { "X-CSRFToken": csrf }, credentials: "same-origin" });
      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || "Correction impossible pour l'instant (" + r.status + ").");
      historique.querySelectorAll("details[open]").forEach((d) => { d.open = false; });
      if (!historique.querySelector("h2")) {
        const titre = document.createElement("h2");
        titre.textContent = "Mes corrections";
        historique.prepend(titre);
      }
      const modele = document.createElement("template");
      modele.innerHTML = data.bloc;
      const bloc = modele.content.firstElementChild;
      historique.querySelector("h2").after(bloc);
      if (window.wikiEnhance) window.wikiEnhance(bloc); // formules, coloration
      photos = [];
      montrer();
      form.elements.enonce.value = "";
      dire("Correction prête ✓", "ok");
      bloc.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (err) {
      dire(err.message, "erreur");
    } finally {
      bouton.disabled = false;
    }
  });
})();
