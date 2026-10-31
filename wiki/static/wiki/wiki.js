// Améliorations côté navigateur : dossier courant ouvert, coloration du code,
// formules (KaTeX) et diagrammes (Mermaid), chargés seulement si nécessaire.
(function () {
  const CDN = "https://cdn.jsdelivr.net/npm/";

  // Versions figées + empreinte SRI : le navigateur refuse un fichier modifié sur le CDN.
  function loadScript(src, integrity) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src;
      s.integrity = integrity;
      s.crossOrigin = "anonymous";
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function loadStyle(href, integrity) {
    const l = document.createElement("link");
    l.rel = "stylesheet";
    l.href = href;
    l.integrity = integrity;
    l.crossOrigin = "anonymous";
    document.head.appendChild(l);
  }

  // Sommaire : boutons « Tout déplier » / « Tout replier ».
  const sommaire = document.querySelector(".sommaire");
  if (sommaire) {
    document.querySelectorAll("[data-fold]").forEach((button) => {
      button.addEventListener("click", () => {
        const open = button.dataset.fold === "open";
        sommaire.querySelectorAll("details").forEach((d) => { d.open = open; });
      });
    });
  }

  // Ouvre les dossiers de l'arborescence qui contiennent la note affichée.
  const active = document.querySelector(".tree-note.active");
  for (let el = active && active.parentElement; el; el = el.parentElement) {
    if (el.tagName === "DETAILS") el.open = true;
  }

  // Ctrl+E sur une page : ouvre l'éditeur (comme Obsidian passe de la lecture à l'édition).
  const editLink = document.querySelector("[data-edit-shortcut]");
  if (editLink) {
    document.addEventListener("keydown", (e) => {
      if (!(e.ctrlKey || e.metaKey) || e.altKey || e.shiftKey || e.key.toLowerCase() !== "e") return;
      if (e.target.closest("input, textarea, select, [contenteditable]")) return;
      e.preventDefault();
      window.location.href = editLink.href;
    });
  }

  // Diagrammes, coloration du code et formules d'un morceau de page : appelé au
  // chargement, et par l'éditeur pour son mode « Lecture ».
  function enhance(root) {
    // Diagrammes Mermaid (```mermaid).
    const diagrams = root.querySelectorAll("pre > code.language-mermaid");
    if (diagrams.length) {
      const nodes = [];
      diagrams.forEach((code) => {
        const div = document.createElement("div");
        div.className = "mermaid";
        div.textContent = code.textContent;
        code.parentElement.replaceWith(div);
        nodes.push(div);
      });
      loadScript(CDN + "mermaid@11.17.2/dist/mermaid.min.js", "sha384-EOXBFmc3gx5mb+vn0vPvvGqACToJD24hhacX5Yx+8NUUQrHIle/Qi5Bg9o3zKwW2").then(() => {
        const dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        window.mermaid.initialize({ startOnLoad: false, theme: dark ? "dark" : "default" });
        window.mermaid.run({ nodes });
      });
    }

    // Coloration syntaxique.
    const blocks = root.querySelectorAll(".markdown pre code");
    if (blocks.length) {
      loadScript(CDN + "@highlightjs/cdn-assets@11.12.0/highlight.min.js", "sha384-wjfDDhOPPdjtva8vWBhWeVprSpmxisEu5aYT3q1JyACqXpdKpo3PWZTMVq24MBix").then(() => {
        blocks.forEach((el) => window.hljs.highlightElement(el));
      });
    }

    // Formules LaTeX ($...$ et $$...$$).
    if (root.querySelector(".math")) {
      loadKatex().then((katex) => {
        root.querySelectorAll(".math").forEach((el) => {
          const block = el.classList.contains("math-block");
          const tex = el.textContent.trim().replace(/^\\[\[(]|\\[\])]$/g, "");
          katex.render(tex, el, { displayMode: block, throwOnError: false });
        });
      });
    }
  }

  // KaTeX, chargé une seule fois : pour les pages et pour l'aperçu en direct de l'éditeur.
  let katexReady = null;
  function loadKatex() {
    if (!katexReady) {
      loadStyle(CDN + "katex@0.16.47/dist/katex.min.css", "sha384-nH0MfJ44wi1dd7w6jinlyBgljjS8EJAh2JBoRad8a3VDw2K69vfaaqm4WnR+gXtA");
      katexReady = loadScript(CDN + "katex@0.16.47/dist/katex.min.js", "sha384-CwjPRVHTvLiMBFjEoij+QZViMV5rhTOIp7CJzl24JEqpRDA1sJFHVXXLURktbYYp")
        .then(() => window.katex);
    }
    return katexReady;
  }
  window.wikiKatex = loadKatex;

  enhance(document);
  window.wikiEnhance = enhance;
})();
