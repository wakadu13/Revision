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

  // Diagrammes Mermaid (```mermaid).
  const diagrams = document.querySelectorAll("pre > code.language-mermaid");
  if (diagrams.length) {
    diagrams.forEach((code) => {
      const div = document.createElement("div");
      div.className = "mermaid";
      div.textContent = code.textContent;
      code.parentElement.replaceWith(div);
    });
    loadScript(CDN + "mermaid@11.17.2/dist/mermaid.min.js", "sha384-EOXBFmc3gx5mb+vn0vPvvGqACToJD24hhacX5Yx+8NUUQrHIle/Qi5Bg9o3zKwW2").then(() => {
      const dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      window.mermaid.initialize({ startOnLoad: false, theme: dark ? "dark" : "default" });
      window.mermaid.run({ querySelector: ".mermaid" });
    });
  }

  // Coloration syntaxique.
  if (document.querySelector(".markdown pre code")) {
    loadScript(CDN + "@highlightjs/cdn-assets@11.12.0/highlight.min.js", "sha384-wjfDDhOPPdjtva8vWBhWeVprSpmxisEu5aYT3q1JyACqXpdKpo3PWZTMVq24MBix").then(() => {
      document.querySelectorAll(".markdown pre code").forEach((el) => window.hljs.highlightElement(el));
    });
  }

  // Formules LaTeX ($...$ et $$...$$).
  if (document.querySelector(".math")) {
    loadStyle(CDN + "katex@0.16.47/dist/katex.min.css", "sha384-nH0MfJ44wi1dd7w6jinlyBgljjS8EJAh2JBoRad8a3VDw2K69vfaaqm4WnR+gXtA");
    loadScript(CDN + "katex@0.16.47/dist/katex.min.js", "sha384-CwjPRVHTvLiMBFjEoij+QZViMV5rhTOIp7CJzl24JEqpRDA1sJFHVXXLURktbYYp").then(() => {
      document.querySelectorAll(".math").forEach((el) => {
        const block = el.classList.contains("math-block");
        const tex = el.textContent.trim().replace(/^\\[\[(]|\\[\])]$/g, "");
        window.katex.render(tex, el, { displayMode: block, throwOnError: false });
      });
    });
  }
})();
