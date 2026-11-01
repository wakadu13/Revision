// Plein écran : il ne reste que le texte. Le menu (bord gauche), le panneau de
// droite (bord droit) et, dans l'éditeur, la barre d'outils (bord haut)
// réapparaissent quand la souris touche le bord de l'écran (ou d'un appui du
// doigt sur le bord). Bouton ⛶ ou Ctrl+Maj+F ; Échap pour quitter.
//
// Recharger la page fait quitter le plein écran au navigateur : en plein écran,
// les pages qui n'ont besoin d'aucun script en plus (notes, sommaire, tags,
// recherche) sont donc chargées sans recharger le document.
(function () {
  "use strict";
  const body = document.body;
  const app = body.classList.contains("app"); // Android : déjà en plein écran
  const BORD = 12; // px depuis le bord de l'écran
  const MARGE = 48; // la souris s'éloigne d'autant du panneau avant qu'il se cache
  let actif = false;
  let astuceTimer = null;

  const $ = (sel) => document.querySelector(sel);
  const boutons = () => document.querySelectorAll("[data-plein-ecran]");

  function majBoutons() {
    boutons().forEach((b) => {
      b.setAttribute("aria-pressed", String(actif));
      b.title = actif ? "Quitter le plein écran (Échap)" : "Plein écran (Ctrl+Maj+F)";
    });
  }

  function cacher(...cotes) {
    cotes.forEach((c) => body.classList.remove("pe-" + c));
  }

  function annoncer() {
    window.dispatchEvent(new CustomEvent("wiki:plein-ecran", { detail: { actif } }));
  }

  function entrer() {
    if (actif) return;
    actif = true;
    body.classList.add("plein-ecran");
    majBoutons();
    if (!app && document.fullscreenEnabled && !document.fullscreenElement) {
      // Refusé (iPhone, réglage du navigateur) : la page reste quand même épurée.
      document.documentElement.requestFullscreen({ navigationUI: "hide" }).catch(() => {});
    }
    astuce();
    annoncer();
  }

  function sortir() {
    if (!actif) return;
    actif = false;
    body.classList.remove("plein-ecran");
    cacher("gauche", "droite", "haut");
    majBoutons();
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    $(".pe-astuce")?.remove();
    annoncer();
  }

  function basculer() {
    if (actif) sortir();
    else entrer();
  }

  // Échap (géré par le navigateur) ou F11 : on suit.
  document.addEventListener("fullscreenchange", () => {
    if (!document.fullscreenElement) sortir();
  });

  function astuce() {
    $(".pe-astuce")?.remove();
    const div = document.createElement("div");
    div.className = "pe-astuce";
    div.setAttribute("role", "status");
    const parties = ["Bord gauche : menu", "bord droit : plan"];
    if ($(".editing .toolbar")) parties.push("bord haut : barre d'outils");
    div.textContent = parties.join(" · ") + " · Échap pour quitter";
    body.appendChild(div);
    clearTimeout(astuceTimer);
    astuceTimer = setTimeout(() => div.classList.add("pe-astuce-fin"), 3500);
    div.addEventListener("transitionend", () => div.remove());
  }

  // -- Panneaux qui réapparaissent au bord de l'écran ---------------------------

  const aContenu = (el) => el && el.textContent.trim() !== "";
  const garde = (el) => el && (el.contains(document.activeElement) || el.querySelector("details[open]"));

  function suivre(x, y) {
    const largeur = document.documentElement.clientWidth;
    const sidebar = $(".sidebar");
    const aside = $(".aside");
    const toolbar = $(".editing .toolbar");

    if (x <= BORD) body.classList.add("pe-gauche");
    else if (body.classList.contains("pe-gauche") && x > sidebar.offsetWidth + MARGE && !garde(sidebar)) cacher("gauche");

    if (x >= largeur - BORD && aContenu(aside)) body.classList.add("pe-droite");
    else if (body.classList.contains("pe-droite") && x < largeur - aside.offsetWidth - MARGE && !garde(aside)) cacher("droite");

    if (toolbar) {
      if (y <= BORD) body.classList.add("pe-haut");
      else if (body.classList.contains("pe-haut") && y > toolbar.getBoundingClientRect().bottom + MARGE && !garde(toolbar)) cacher("haut");
    }
  }

  let attente = null;
  document.addEventListener("mousemove", (e) => {
    if (!actif || attente) return;
    attente = requestAnimationFrame(() => {
      attente = null;
      suivre(e.clientX, e.clientY);
    });
  }, { passive: true });

  // Écran tactile : un appui sur le bord ouvre le panneau, un appui ailleurs le referme.
  document.addEventListener("pointerdown", (e) => {
    if (!actif) return;
    const dansPanneau = e.target.closest(".sidebar, .aside, .toolbar, .pe-astuce");
    if (e.pointerType !== "mouse" && !dansPanneau) {
      const largeur = document.documentElement.clientWidth;
      if (e.clientX <= 24) return void body.classList.add("pe-gauche");
      if (e.clientX >= largeur - 24 && aContenu($(".aside"))) return void body.classList.add("pe-droite");
      if (e.clientY <= 24 && $(".editing .toolbar")) return void body.classList.add("pe-haut");
    }
    if (!dansPanneau) cacher("gauche", "droite", "haut");
  });

  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && !e.altKey && e.key.toLowerCase() === "f") {
      e.preventDefault();
      basculer();
      return;
    }
    // Sans plein écran du navigateur (refusé, application) : Échap quitte aussi,
    // sauf dans l'éditeur, une fenêtre ou un champ, qui s'en servent déjà.
    if (e.key === "Escape" && actif && !document.fullscreenElement && !e.defaultPrevented
        && !e.target.closest(".cm-editor, input, textarea, select, dialog")) {
      sortir();
    }
  });

  document.addEventListener("click", (e) => {
    const bouton = e.target.closest("[data-plein-ecran]");
    if (!bouton) return;
    e.preventDefault();
    basculer();
  });

  // -- Changer de page sans quitter le plein écran ------------------------------

  // Scripts propres à une page (éditeur, QCM, lecteur PDF, import) : ils sont
  // dans le corps de la page. Ceux du <head> (wiki.js, ce fichier) servent partout.
  const pageSimple = (doc) => !doc.querySelector("body script[src]");
  let enCours = null;

  function eligible(url) {
    return url.origin === location.origin && !/^\/(fichiers|static|api|admin)\//.test(url.pathname)
      && !url.pathname.endsWith("sw.js") && !url.pathname.endsWith(".webmanifest");
  }

  async function naviguer(url, { retour = false } = {}) {
    const controle = new AbortController();
    enCours?.abort();
    enCours = controle;
    let doc;
    let finale;
    try {
      const reponse = await fetch(url, { headers: { Accept: "text/html" }, signal: controle.signal });
      finale = new URL(reponse.url);
      if (!reponse.ok || !(reponse.headers.get("Content-Type") || "").includes("text/html")) throw new Error();
      doc = new DOMParser().parseFromString(await reponse.text(), "text/html");
    } catch (e) {
      if (e.name === "AbortError") return;
      location.href = url;
      return;
    }
    const charges = new Set([...document.scripts].map((s) => s.src));
    const tetes = [...doc.head.querySelectorAll("script[src]")].map((s) => new URL(s.getAttribute("src"), finale).href);
    const contenu = doc.querySelector("main.content");
    const aside = doc.querySelector("aside.aside");
    if (!pageSimple(doc) || !contenu || !aside || tetes.some((src) => !charges.has(src)) || !actif) {
      location.href = finale.href;
      return;
    }

    // Première page du plein écran : marquée pour que « Retour » y revienne sans recharger.
    if (!history.state || !history.state.pleinEcran) history.replaceState({ pleinEcran: true }, "");
    if (!retour) history.pushState({ pleinEcran: true }, "", finale.href);

    $("main.content").replaceWith(document.adoptNode(contenu));
    $("aside.aside").replaceWith(document.adoptNode(aside));
    document.title = doc.title;
    const classes = ["plein-ecran", "app"].filter((c) => body.classList.contains(c));
    body.className = doc.body.className;
    body.classList.add(...classes);

    // Menu : note active et recherche, sans perdre le défilement de l'arborescence.
    const active = doc.querySelector(".tree-note.active");
    document.querySelectorAll(".tree-note.active").forEach((a) => a.classList.remove("active"));
    if (active) {
      const href = active.getAttribute("href");
      document.querySelectorAll(".tree-note").forEach((a) => {
        if (a.getAttribute("href") === href) a.classList.add("active");
      });
    }
    const recherche = doc.querySelector(".sidebar .search input");
    const champ = $(".sidebar .search input");
    if (recherche && champ) champ.value = recherche.value;

    cacher("gauche", "droite", "haut");
    if (window.wikiInitPage) window.wikiInitPage($("main.content"));
    const ancre = finale.hash && document.getElementById(decodeURIComponent(finale.hash.slice(1)));
    if (ancre) ancre.scrollIntoView();
    else window.scrollTo(0, 0);
    $("main.content").focus({ preventScroll: true });
  }

  document.addEventListener("click", (e) => {
    if (!actif || e.defaultPrevented || e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    const lien = e.target.closest("a[href]");
    if (!lien || lien.target || lien.hasAttribute("download") || !pageSimple(document)) return;
    const url = new URL(lien.href, location.href);
    if (!eligible(url)) return;
    // Ancre de la même page : le navigateur s'en charge.
    if (url.pathname === location.pathname && url.search === location.search && url.hash) return;
    e.preventDefault();
    naviguer(url.href);
  });

  // Formulaires de recherche (GET) : même chose.
  document.addEventListener("submit", (e) => {
    const form = e.target;
    if (!actif || e.defaultPrevented || (form.method || "get").toLowerCase() !== "get" || !pageSimple(document)) return;
    const url = new URL(form.action || location.href, location.href);
    if (!eligible(url)) return;
    url.search = new URLSearchParams(new FormData(form)).toString();
    e.preventDefault();
    naviguer(url.href);
  });

  window.addEventListener("popstate", (e) => {
    if (!e.state || !e.state.pleinEcran) return;
    // Plein écran quitté entre-temps : la page affichée n'est pas celle de l'adresse.
    if (actif) naviguer(location.href, { retour: true });
    else location.reload();
  });

  window.wikiPleinEcran = { basculer, entrer, sortir, actif: () => actif };
})();
