// Plein écran : il ne reste que le texte. Le menu (bord gauche), le panneau de
// droite (bord droit) et, dans l'éditeur, la barre d'outils (bord haut)
// réapparaissent quand la souris touche le bord de l'écran (ou d'un appui du
// doigt sur le bord). Bouton ⛶ ou Ctrl+Maj+F ; Échap pour quitter.
//
// Pages de lecture (notes, PDF ; classe menu-cache) : le menu est caché même
// sans plein écran et revient de la même façon, ou par la languette du bord
// gauche. Le bouton « Garder le menu affiché » l'épingle (cookie menu=epingle).
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
  // Sur téléphone, le menu est déjà un tiroir (☰) : menu-cache ne joue qu'en écran large.
  const large = window.matchMedia("(min-width: 761px)");
  const menuCache = () => body.classList.contains("menu-cache") && large.matches;
  const escamotable = () => actif || menuCache();

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

  function astuce(texte, duree = 3500) {
    $(".pe-astuce")?.remove();
    const div = document.createElement("div");
    div.className = "pe-astuce";
    div.setAttribute("role", "status");
    if (!texte) {
      const parties = ["Bord gauche : menu", "bord droit : plan"];
      if ($(".editing .toolbar")) parties.push("bord haut : barre d'outils");
      texte = parties.join(" · ") + " · Échap pour quitter";
    }
    div.textContent = texte;
    body.appendChild(div);
    clearTimeout(astuceTimer);
    astuceTimer = setTimeout(() => div.classList.add("pe-astuce-fin"), duree);
    div.addEventListener("transitionend", () => div.remove());
  }

  function ouvrirMenu() {
    if (body.classList.contains("pe-gauche")) return;
    body.classList.add("pe-gauche");
    // Note affichée hors de vue dans l'arborescence : on la montre.
    const sidebar = $(".sidebar");
    const active = sidebar && sidebar.querySelector(".tree-note.active");
    if (active) {
      const r = active.getBoundingClientRect();
      if (r.top < 0 || r.bottom > window.innerHeight) active.scrollIntoView({ block: "center" });
    }
  }

  // Garder le menu affiché pendant la lecture, ou le cacher de nouveau.
  function epingler(garder) {
    const secure = location.protocol === "https:" ? "; Secure" : "";
    document.cookie = garder ? `menu=epingle; path=/; max-age=31536000; SameSite=Lax${secure}`
      : `menu=; path=/; max-age=0; SameSite=Lax${secure}`;
    body.classList.toggle("menu-cache", !garder);
    cacher("gauche");
    document.querySelectorAll("[data-epingler-menu]").forEach((b) => {
      b.setAttribute("aria-pressed", String(garder));
      b.title = garder ? "Cacher le menu pendant la lecture" : "Garder le menu affiché pendant la lecture";
      b.setAttribute("aria-label", b.title);
    });
  }

  // -- Panneaux qui réapparaissent au bord de l'écran ---------------------------

  const aContenu = (el) => el && el.textContent.trim() !== "";
  // Panneau à laisser ouvert : on y tape (recherche) ou un menu déroulant y est ouvert
  // (« Fichier » de l'éditeur ; pas les dossiers de l'arborescence).
  const garde = (el) => el && (el.contains(document.activeElement) && document.activeElement.matches("input, textarea, select")
    || el.querySelector(".toolbar-menu[open]"));

  function suivre(x, y) {
    const largeur = document.documentElement.clientWidth;
    const sidebar = $(".sidebar");
    const aside = $(".aside");
    const toolbar = $(".editing .toolbar");

    if (x <= BORD) ouvrirMenu();
    else if (body.classList.contains("pe-gauche") && x > sidebar.offsetWidth + MARGE && !garde(sidebar)) cacher("gauche");
    if (!actif) return; // pages de lecture : seulement le menu

    if (x >= largeur - BORD && aContenu(aside)) body.classList.add("pe-droite");
    else if (body.classList.contains("pe-droite") && x < largeur - aside.offsetWidth - MARGE && !garde(aside)) cacher("droite");

    if (toolbar) {
      if (y <= BORD) body.classList.add("pe-haut");
      else if (body.classList.contains("pe-haut") && y > toolbar.getBoundingClientRect().bottom + MARGE && !garde(toolbar)) cacher("haut");
    }
  }

  let attente = null;
  document.addEventListener("mousemove", (e) => {
    if (!escamotable() || attente) return;
    attente = requestAnimationFrame(() => {
      attente = null;
      suivre(e.clientX, e.clientY);
    });
  }, { passive: true });

  // Écran tactile : un appui sur le bord ouvre le panneau, un appui ailleurs le referme.
  document.addEventListener("pointerdown", (e) => {
    if (!escamotable()) return;
    const dansPanneau = e.target.closest(".sidebar, .aside, .toolbar, .pe-astuce, [data-ouvrir-menu]");
    if (e.pointerType !== "mouse" && !dansPanneau) {
      const largeur = document.documentElement.clientWidth;
      if (e.clientX <= 24) return void ouvrirMenu();
      if (actif && e.clientX >= largeur - 24 && aContenu($(".aside"))) return void body.classList.add("pe-droite");
      if (actif && e.clientY <= 24 && $(".editing .toolbar")) return void body.classList.add("pe-haut");
    }
    if (!dansPanneau) cacher("gauche", "droite", "haut");
  });

  // Glisser le doigt depuis le bord gauche ouvre le menu, vers la gauche le referme.
  let glisse = null;
  document.addEventListener("touchstart", (e) => {
    const t = e.touches[0];
    const ouvert = body.classList.contains("pe-gauche");
    glisse = escamotable() && e.touches.length === 1 && (ouvert || t.clientX <= 32)
      ? { x: t.clientX, y: t.clientY, ouvert } : null;
  }, { passive: true });
  document.addEventListener("touchend", (e) => {
    if (!glisse) return;
    const t = e.changedTouches[0];
    const dx = t.clientX - glisse.x;
    if (Math.abs(dx) > 50 && Math.abs(dx) > 1.5 * Math.abs(t.clientY - glisse.y)) {
      if (dx > 0 && !glisse.ouvert) ouvrirMenu();
      else if (dx < 0 && glisse.ouvert) cacher("gauche");
    }
    glisse = null;
  }, { passive: true });

  document.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && !e.altKey && e.key.toLowerCase() === "f") {
      e.preventDefault();
      basculer();
      return;
    }
    // Échap referme d'abord un panneau ouvert.
    if (e.key === "Escape" && escamotable() && /\bpe-(gauche|droite|haut)\b/.test(body.className)
        && !e.target.closest(".cm-editor, dialog")) {
      cacher("gauche", "droite", "haut");
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
    if (e.target.closest("[data-plein-ecran]")) {
      e.preventDefault();
      basculer();
    } else if (e.target.closest("[data-epingler-menu]")) {
      e.preventDefault();
      epingler(body.classList.contains("menu-cache"));
    } else if (e.target.closest("[data-ouvrir-menu]") && escamotable()) {
      // Languette, ou « Parcourir » de l'application sur tablette.
      e.preventDefault();
      if (body.classList.contains("pe-gauche")) cacher("gauche");
      else ouvrirMenu();
    }
  });

  // Première lecture avec le menu caché : dire où il est passé.
  if (menuCache()) {
    let vu = true;
    try { vu = localStorage.getItem("wiki-menu-cache-vu") === "1"; localStorage.setItem("wiki-menu-cache-vu", "1"); } catch (e) { /* stockage bloqué */ }
    if (!vu) astuce("Menu caché pendant la lecture : touchez le bord gauche (languette ›) pour l'afficher", 6000);
  }

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
