// Améliorations côté navigateur : dossier courant ouvert, coloration du code,
// formules (KaTeX) et diagrammes (Mermaid), chargés seulement si nécessaire.
(function () {
  const CDN = "https://cdn.jsdelivr.net/npm/";

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function loadStyle(href) {
    const l = document.createElement("link");
    l.rel = "stylesheet";
    l.href = href;
    document.head.appendChild(l);
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
    loadScript(CDN + "mermaid@11/dist/mermaid.min.js").then(() => {
      const dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      window.mermaid.initialize({ startOnLoad: false, theme: dark ? "dark" : "default" });
      window.mermaid.run({ querySelector: ".mermaid" });
    });
  }

  // Coloration syntaxique.
  if (document.querySelector(".markdown pre code")) {
    loadScript(CDN + "@highlightjs/cdn-assets@11/highlight.min.js").then(() => {
      document.querySelectorAll(".markdown pre code").forEach((el) => window.hljs.highlightElement(el));
    });
  }

  // Formules LaTeX ($...$ et $$...$$).
  if (document.querySelector(".math")) {
    loadStyle(CDN + "katex@0.16/dist/katex.min.css");
    loadScript(CDN + "katex@0.16/dist/katex.min.js").then(() => {
      document.querySelectorAll(".math").forEach((el) => {
        const block = el.classList.contains("math-block");
        const tex = el.textContent.trim().replace(/^\\[\[(]|\\[\])]$/g, "");
        window.katex.render(tex, el, { displayMode: block, throwOnError: false });
      });
    });
  }
})();
