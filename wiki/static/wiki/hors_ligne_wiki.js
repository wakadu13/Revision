// Lecture hors ligne du wiki : « Garder ce dossier hors ligne » sur le sommaire
// (pages, images et PDF du dossier mis en cache d'un coup, dans le cache du
// service worker sw_wiki.js) et liste des pages disponibles sur la page « hors
// connexion ».
(function () {
  "use strict";
  const CACHE = "wiki-hors-ligne-v1";
  const CLE = "wiki-dossiers-hors-ligne";

  const lireGardes = () => { try { return JSON.parse(localStorage.getItem(CLE) || "{}"); } catch (e) { return {}; } };
  const ecrireGardes = (g) => { try { localStorage.setItem(CLE, JSON.stringify(g)); } catch (e) { /* stockage bloqué */ } };

  // -- Sommaire : un bouton par dossier --
  const sommaire = document.querySelector("[data-dossier-url]");
  if (sommaire && window.caches) {
    const gardes = lireGardes();
    sommaire.querySelectorAll("summary[data-dossier]").forEach((summary) => {
      const dossier = summary.dataset.dossier;
      const b = document.createElement("button");
      b.type = "button";
      b.className = "button small sommaire-hors-ligne";
      const etat = () => {
        const g = lireGardes()[dossier];
        b.textContent = g ? `✓ Hors ligne (${g.n})` : "⤓ Hors ligne";
        b.title = g ? `Gardé hors ligne le ${new Date(g.date).toLocaleDateString("fr-FR")} : clic pour retirer du cache`
          : "Garder les pages, images et PDF de ce dossier sur cet appareil, pour les lire sans connexion";
        b.classList.toggle("is-garde", !!g);
      };
      etat();
      b.addEventListener("click", async (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (b.disabled) return;
        const g = lireGardes();
        if (g[dossier]) {
          if (!confirm(`Retirer « ${dossier} » du cache hors ligne de cet appareil ?`)) return;
          const cache = await caches.open(CACHE);
          await Promise.all((g[dossier].urls || []).map((u) => cache.delete(u)));
          delete g[dossier];
          ecrireGardes(g);
          etat();
          return;
        }
        b.disabled = true;
        try {
          const r = await fetch(sommaire.dataset.dossierUrl + "?dossier=" + encodeURIComponent(dossier), { credentials: "same-origin" });
          if (!r.ok) throw new Error("liste indisponible (" + r.status + ")");
          const { urls } = await r.json();
          const cache = await caches.open(CACHE);
          let faits = 0, rates = 0;
          for (const u of urls) {
            b.textContent = `${faits} / ${urls.length}…`;
            try {
              const rep = await fetch(u, { credentials: "same-origin" });
              if (rep.ok && !rep.redirected) await cache.put(u, rep); else rates++;
            } catch (err) { rates++; }
            faits++;
          }
          if (navigator.storage && navigator.storage.persist) navigator.storage.persist().catch(() => {});
          g[dossier] = { n: urls.length - rates, urls, date: Date.now() };
          ecrireGardes(g);
          etat();
          if (rates) b.title += ` · ${rates} fichier(s) non gardé(s)`;
        } catch (err) {
          b.textContent = "⤓ Hors ligne (réessayer)";
          b.title = err.message;
        } finally {
          b.disabled = false;
        }
      });
      summary.appendChild(b);
    });
    if (!gardes || !Object.keys(gardes).length) { /* rien */ }
  }

  // -- Page « hors connexion » : ce qui est lisible sur l'appareil --
  const liste = document.querySelector("[data-pages-hors-ligne]");
  if (liste && window.caches) {
    caches.open(CACHE).then(async (cache) => {
      const cles = await cache.keys();
      const pages = [];
      for (const req of cles) {
        const url = new URL(req.url);
        if (url.origin !== location.origin) continue;
        if (url.pathname.startsWith("/wiki/") || url.pathname.startsWith("/pdf/") || url.pathname === "/") {
          const nom = decodeURIComponent(url.pathname.replace(/^\/(wiki|pdf)\//, "")) || "Accueil";
          pages.push({ nom: url.pathname.startsWith("/pdf/") ? nom + " (PDF)" : nom, href: url.pathname });
        }
      }
      pages.sort((a, b) => a.nom.localeCompare(b.nom, "fr"));
      liste.replaceChildren();
      if (!pages.length) {
        liste.append(Object.assign(document.createElement("p"), { className: "muted", textContent: "Aucune page en cache pour l'instant." }));
        return;
      }
      const ul = document.createElement("ul");
      for (const p of pages) {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = p.href;
        a.textContent = p.nom;
        li.append(a);
        ul.append(li);
      }
      liste.append(ul);
    }).catch(() => { liste.textContent = "Cache indisponible sur ce navigateur."; });
  }
})();
