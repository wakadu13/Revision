// Éditeur de pages façon Obsidian, construit sur CodeMirror 6 (le moteur
// d'Obsidian, regroupé dans vendor/codemirror.min.js, voir editeur/) :
// - « Aperçu en direct » : la syntaxe Markdown s'efface hors de la ligne en
//   cours (titres en grand, gras, liens, cases à cocher cliquables, images,
//   encadrés colorés) ; « Source » : Markdown brut ; « Lecture » : rendu final ;
// - [[ propose les pages, ![[ les images ; Ctrl+clic ouvre un lien ;
// - Ctrl+S enregistre sans quitter (enregistrement auto en option) ;
// - images collées ou glissées : ajoutées au coffre ; .md glissé ou ouvert :
//   son texte est inséré ; bouton « Télécharger » : la page en .md.
// Si CodeMirror ne se charge pas, la zone de texte simple reste utilisable.
(function () {
  "use strict";
  const textarea = document.getElementById("editor");
  const CM = window.CM;
  if (!textarea || !CM) return;

  const {
    EditorState, EditorSelection, Compartment, Prec, StateField, EditorView, ViewPlugin, Decoration, WidgetType, keymap,
    drawSelection, dropCursor, placeholder, history, historyKeymap, defaultKeymap, indentWithTab,
    syntaxTree, syntaxHighlighting, HighlightStyle, indentOnInput, markdown, markdownLanguage,
    autocompletion, completionKeymap, closeBrackets, closeBracketsKeymap,
    search, searchKeymap, highlightSelectionMatches, tags, Tag, codeLanguage,
  } = CM;

  const form = document.getElementById("editor-form");
  const host = form.querySelector(".editor-cm");
  const preview = form.querySelector(".preview");
  const toolbar = form.querySelector(".toolbar");
  const footer = form.querySelector(".editor-footer");
  const versionInput = form.querySelector("[name=version]");
  const csrf = form.querySelector("[name=csrfmiddlewaretoken]").value;
  const stateLabel = form.querySelector("[data-state]");
  const countLabel = form.querySelector("[data-count]");
  const autosaveBox = form.querySelector("[data-autosave]");
  const closeLink = form.querySelector(".editor-actions a");
  const { previewUrl, importUrl, latexUrl, noteKey, noteName } = form.dataset;
  const choices = JSON.parse(document.getElementById("link-choices").textContent);
  const attachments = JSON.parse(document.getElementById("attachment-choices").textContent);

  // -- Outils -----------------------------------------------------------------

  function normalize(s) {
    return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  function stored(key, fallback) {
    try {
      return localStorage.getItem(key) ?? fallback;
    } catch (e) {
      return fallback;
    }
  }

  function store(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (e) {
      // Stockage indisponible (navigation privée) : réglage non mémorisé.
    }
  }

  // Identifiant d'un titre, comme le sommaire des pages (slugify_unicode de Python-Markdown).
  function slug(text) {
    return text.replace(/[^\p{L}\p{M}\p{N}_\s-]/gu, "").trim().toLowerCase().replace(/[-\s]+/g, "-");
  }

  function wikiUrl(page) {
    return "/wiki/" + page.split("/").map(encodeURIComponent).join("/");
  }

  const IMAGE_RE = /\.(png|jpe?g|gif|svg|webp|bmp|avif)$/i;
  const CALLOUT_ALIASES = {
    summary: "abstract", tldr: "abstract", hint: "tip", important: "tip", check: "success", done: "success",
    help: "question", faq: "question", caution: "warning", attention: "warning", fail: "failure",
    missing: "failure", error: "danger", cite: "quote",
  };

  // Pages et fichiers existants : un lien vers une page absente s'affiche en pointillés.
  const pageNames = new Set();
  const pageKeys = [];
  for (const c of choices) {
    const name = c.link.split("/").pop();
    const key = (c.folder ? c.folder + "/" : "") + name;
    pageKeys.push(key.toLowerCase());
    [name, key, ...c.aliases].forEach((n) => pageNames.add(n.toLowerCase()));
  }
  const files = new Map();
  function rememberFile(a) {
    const path = ((a.folder ? a.folder + "/" : "") + a.link.split("/").pop()).toLowerCase();
    [a.link.toLowerCase(), path, path.split("/").pop()].forEach((k) => files.has(k) || files.set(k, a));
  }
  attachments.forEach(rememberFile);

  function findFile(target) {
    return files.get(target.trim().toLowerCase()) || null;
  }

  function pageExists(target) {
    const t = target.trim().toLowerCase().replace(/\.md$/, "");
    if (!t || pageNames.has(t) || findFile(t)) return true;
    return t.includes("/") && pageKeys.some((k) => k.endsWith("/" + t));
  }

  // -- Syntaxe Obsidian en plus du Markdown (GFM) ---------------------------------

  const highlightTag = Tag.define();
  const commentTag = Tag.define();
  const hashtagTag = Tag.define();
  const mathTag = Tag.define();
  const wikilinkTag = Tag.define();
  const PUNCTUATION = /[!-/:-@[-`{-~¡-¿‐-‧]/;

  // ==surlignage== : délimiteur comme ~~barré~~.
  const HighlightDelim = { resolve: "Highlight", mark: "HighlightMark" };
  const Highlight = {
    defineNodes: [{ name: "Highlight", style: highlightTag }, { name: "HighlightMark", style: tags.processingInstruction }],
    parseInline: [{
      name: "Highlight",
      parse(cx, next, pos) {
        if (next !== 61 || cx.char(pos + 1) !== 61 || cx.char(pos + 2) === 61) return -1;
        const before = cx.slice(pos - 1, pos), after = cx.slice(pos + 2, pos + 3);
        const sBefore = /\s|^$/.test(before), sAfter = /\s|^$/.test(after);
        const pBefore = PUNCTUATION.test(before), pAfter = PUNCTUATION.test(after);
        return cx.addDelimiter(HighlightDelim, pos, pos + 2,
          !sAfter && (!pAfter || sBefore || pBefore),
          !sBefore && (!pBefore || sAfter || pAfter));
      },
      after: "Emphasis",
    }],
  };

  // [[Page|texte]] et ![[intégration]].
  const WikiLink = {
    defineNodes: [
      { name: "WikiLink", style: wikilinkTag },
      { name: "Embed", style: wikilinkTag },
      { name: "WikiLinkMark", style: tags.processingInstruction },
    ],
    parseInline: [{
      name: "WikiLink",
      parse(cx, next, pos) {
        const embed = next === 33;
        const open = embed ? pos + 1 : pos;
        if ((!embed && next !== 91) || cx.char(open) !== 91 || cx.char(open + 1) !== 91) return -1;
        for (let end = open + 2; end < cx.end - 1; end++) {
          const c = cx.char(end);
          if (c === 10 || c === 91) return -1;
          if (c === 93) {
            if (cx.char(end + 1) !== 93 || end === open + 2) return -1;
            return cx.addElement(cx.elt(embed ? "Embed" : "WikiLink", pos, end + 2, [
              cx.elt("WikiLinkMark", pos, open + 2), cx.elt("WikiLinkMark", end, end + 2),
            ]));
          }
        }
        return -1;
      },
      before: "Link",
    }],
  };

  // %% commentaire %% (invisible sur le wiki).
  const Comment = {
    defineNodes: [{ name: "ObsidianComment", style: commentTag }],
    parseInline: [{
      name: "ObsidianComment",
      parse(cx, next, pos) {
        if (next !== 37 || cx.char(pos + 1) !== 37) return -1;
        const close = cx.slice(pos + 2, cx.end).indexOf("%%");
        return cx.addElement(cx.elt("ObsidianComment", pos, close < 0 ? cx.end : pos + close + 4));
      },
      before: "Emphasis",
    }],
  };

  // #tag et #parent/enfant (pas uniquement des chiffres).
  const TAG_RE = /^#[\p{L}\p{N}_/-]*[\p{L}_/-][\p{L}\p{N}_/-]*/u;
  const Hashtag = {
    defineNodes: [{ name: "Hashtag", style: hashtagTag }],
    parseInline: [{
      name: "Hashtag",
      parse(cx, next, pos) {
        if (next !== 35 || /\S/.test(cx.slice(pos - 1, pos))) return -1;
        const m = TAG_RE.exec(cx.slice(pos, Math.min(cx.end, pos + 200)));
        return m ? cx.addElement(cx.elt("Hashtag", pos, pos + m[0].length)) : -1;
      },
    }],
  };

  // Formules LaTeX, reconnues comme sur le wiki : $...$ dans le texte (pas
  // d'espace contre les $, pas de chiffre après le $ fermant : « 5 $ et 10 $ »
  // n'est pas une formule) et blocs $$...$$, même collés au texte qui précède.
  const closesMath = (text) => /\$\$\s*$/.test(text);
  const Math_ = {
    defineNodes: [
      { name: "InlineMath", style: mathTag },
      { name: "BlockMath", block: true, style: mathTag },
      { name: "MathMark", style: tags.processingInstruction },
    ],
    parseInline: [{
      name: "InlineMath",
      parse(cx, next, pos) {
        if (next !== 36 || /[\\$]/.test(cx.slice(pos - 1, pos))) return -1;
        const rest = cx.slice(pos + 1, cx.end);
        if (rest[0] === "$") {
          const close = rest.indexOf("$$", 1);
          return close > 1 ? cx.addElement(cx.elt("InlineMath", pos, pos + close + 3)) : -1;
        }
        const m = /^(?=[^\s$])[^$\n]+?(?<=[^\s\\])\$(?!\d)/.exec(rest);
        return m ? cx.addElement(cx.elt("InlineMath", pos, pos + 1 + m[0].length)) : -1;
      },
      before: "Emphasis",
    }],
    parseBlock: [{
      name: "BlockMath",
      parse(cx, line) {
        const text = line.text.slice(line.pos);
        if (!text.startsWith("$$")) return false;
        const from = cx.lineStart + line.pos;
        const marks = [cx.elt("MathMark", from, from + 2)];
        let end = cx.lineStart + line.text.length;
        if (closesMath(text.slice(2)) && text.slice(2).replace(/\$\$\s*$/, "").trim()) {
          const at = from + text.lastIndexOf("$$");
          marks.push(cx.elt("MathMark", at, at + 2));
          cx.nextLine();
        } else {
          // Jusqu'au $$ fermant ; un bloc pas encore fermé s'arrête à la ligne vide.
          while (cx.nextLine() && line.depth >= cx.depth) {
            const rest = line.text.slice(line.pos);
            if (!rest.trim()) break;
            for (const m of line.markers) marks.push(m);
            end = cx.lineStart + line.text.length;
            if (closesMath(rest)) {
              const at = cx.lineStart + line.pos + rest.lastIndexOf("$$");
              marks.push(cx.elt("MathMark", at, at + 2));
              cx.nextLine();
              break;
            }
          }
        }
        cx.addElement(cx.elt("BlockMath", from, end, marks));
        return true;
      },
      endLeaf: (cx, line) => line.text.slice(line.pos).startsWith("$$"),
      before: "HorizontalRule",
    }],
  };

  // Texte LaTeX d'un bloc $$ (sans les $$ ni les « > » d'un encadré).
  function mathSource(text) {
    return text.split("\n").map((l, i) => (i ? l.replace(/^\s*(>\s?)+/, "") : l)).join("\n")
      .replace(/^\s*\$\$/, "").replace(/\$\$\s*$/, "").trim();
  }

  // Propriétés YAML entre deux lignes --- en tout début de note.
  const Frontmatter = {
    defineNodes: [{ name: "Frontmatter", block: true, style: tags.meta }, { name: "FrontmatterMark", style: tags.processingInstruction }],
    parseBlock: [{
      name: "Frontmatter",
      parse(cx, line) {
        if (cx.lineStart !== 0 || !/^---[ \t]*$/.test(line.text)) return false;
        const marks = [cx.elt("FrontmatterMark", 0, line.text.length)];
        let end = line.text.length;
        while (cx.nextLine()) {
          end = cx.lineStart + line.text.length;
          if (/^---[ \t]*$/.test(line.text)) {
            marks.push(cx.elt("FrontmatterMark", cx.lineStart, end));
            cx.nextLine();
            break;
          }
        }
        cx.addElement(cx.elt("Frontmatter", 0, end, marks));
        return true;
      },
      before: "HorizontalRule",
    }],
  };

  const obsidianHighlight = HighlightStyle.define([
    { tag: tags.heading1, class: "cmt-heading" },
    { tag: [tags.heading2, tags.heading3, tags.heading4, tags.heading5, tags.heading6], class: "cmt-heading" },
    { tag: tags.strong, class: "cmt-strong" },
    { tag: tags.emphasis, class: "cmt-em" },
    { tag: tags.strikethrough, class: "cmt-strike" },
    { tag: highlightTag, class: "cmt-highlight" },
    { tag: [tags.link, tags.url, wikilinkTag], class: "cmt-link" },
    { tag: tags.monospace, class: "cmt-code" },
    { tag: tags.processingInstruction, class: "cmt-mark" },
    { tag: tags.quote, class: "cmt-quote" },
    { tag: commentTag, class: "cmt-comment" },
    { tag: hashtagTag, class: "cmt-tag" },
    { tag: mathTag, class: "cmt-math" },
    { tag: tags.meta, class: "cmt-meta" },
    { tag: tags.labelName, class: "cmt-label" },
    // Blocs de code
    { tag: [tags.keyword, tags.operatorKeyword, tags.modifier, tags.controlKeyword, tags.definitionKeyword], class: "cmt-keyword" },
    { tag: [tags.string, tags.special(tags.string), tags.regexp, tags.character], class: "cmt-string" },
    { tag: [tags.comment, tags.lineComment, tags.blockComment, tags.docComment], class: "cmt-code-comment" },
    { tag: [tags.number, tags.bool, tags.null, tags.atom], class: "cmt-number" },
    { tag: [tags.function(tags.variableName), tags.function(tags.propertyName), tags.macroName], class: "cmt-function" },
    { tag: [tags.typeName, tags.className, tags.namespace, tags.tagName], class: "cmt-type" },
    { tag: [tags.propertyName, tags.attributeName, tags.special(tags.variableName)], class: "cmt-property" },
  ]);

  // -- Aperçu en direct --------------------------------------------------------------

  class CheckboxWidget extends WidgetType {
    constructor(checked) {
      super();
      this.checked = checked;
    }
    eq(other) {
      return other.checked === this.checked;
    }
    toDOM(view) {
      const box = document.createElement("input");
      box.type = "checkbox";
      box.className = "cm-task";
      box.checked = this.checked;
      box.setAttribute("aria-label", this.checked ? "Tâche faite" : "Tâche à faire");
      box.addEventListener("mousedown", (e) => e.preventDefault());
      box.addEventListener("click", (e) => {
        e.preventDefault();
        const pos = view.posAtDOM(box);
        if (!/^\[.\]$/.test(view.state.sliceDoc(pos, pos + 3))) return;
        view.dispatch({ changes: { from: pos + 1, to: pos + 2, insert: this.checked ? " " : "x" }, userEvent: "input" });
      });
      return box;
    }
    ignoreEvent() {
      return true;
    }
  }

  class TextWidget extends WidgetType {
    constructor(text, className) {
      super();
      this.text = text;
      this.className = className;
    }
    eq(other) {
      return other.text === this.text && other.className === this.className;
    }
    toDOM() {
      const span = document.createElement("span");
      span.className = this.className;
      span.textContent = this.text;
      return span;
    }
  }

  class ImageWidget extends WidgetType {
    constructor(url, width, alt) {
      super();
      this.url = url;
      this.width = width;
      this.alt = alt;
    }
    eq(other) {
      return other.url === this.url && other.width === this.width;
    }
    toDOM() {
      const img = document.createElement("img");
      img.className = "cm-embed-image";
      img.src = this.url;
      img.alt = this.alt;
      if (this.width) img.width = this.width;
      return img;
    }
  }

  // Formule rendue par KaTeX (chargé par wiki.js, comme pour les pages) ; un
  // clic place le curseur dessus et réaffiche le LaTeX.
  class MathWidget extends WidgetType {
    constructor(tex, display) {
      super();
      this.tex = tex;
      this.display = display;
    }
    eq(other) {
      return other.tex === this.tex && other.display === this.display;
    }
    toDOM(view) {
      const el = document.createElement(this.display ? "div" : "span");
      el.className = this.display ? "cm-math-block" : "cm-math-inline";
      el.textContent = this.display ? `$$${this.tex}$$` : `$${this.tex}$`;
      if (window.wikiKatex) {
        window.wikiKatex().then((katex) => {
          try {
            katex.render(this.tex, el, { displayMode: this.display, throwOnError: false });
          } catch (e) {
            // Formule invalide : le LaTeX reste affiché tel quel.
          }
          view.requestMeasure();
        }).catch(() => {});
      }
      return el;
    }
    ignoreEvent() {
      return false;
    }
  }

  const hidden = Decoration.replace({});
  const bullet = Decoration.replace({ widget: new TextWidget("•", "cm-bullet") });
  const rule = Decoration.replace({ widget: new TextWidget("", "cm-hr") });
  const checked = Decoration.replace({ widget: new CheckboxWidget(true) });
  const unchecked = Decoration.replace({ widget: new CheckboxWidget(false) });
  const lineDecos = {};
  function line(cls, attrs) {
    const id = cls + JSON.stringify(attrs || {});
    return (lineDecos[id] ||= Decoration.line({ attributes: Object.assign({ class: cls }, attrs || {}) }));
  }
  function linkMark(cls, href) {
    return Decoration.mark({ class: cls, attributes: href ? { "data-href": href, title: "Ctrl+clic pour ouvrir" } : {} });
  }

  const CALLOUT_RE = /^((?:\s*>)+\s?)\[!([\w-]+)\]([+-]?)[ \t]*(.*)$/;

  // « [!type] » d'un encadré : remplacé par le nom du type, ou masqué s'il y a un titre.
  function calloutMarker(out, lineFrom, m, type) {
    const start = lineFrom + m[1].length;
    const end = start + m[2].length + 3 + m[3].length;
    const after = out.doc.sliceString(end, end + 1) === " " ? end + 1 : end;
    const label = m[4] ? "" : type.charAt(0).toUpperCase() + type.slice(1);
    out.push((label ? Decoration.replace({ widget: new TextWidget(label, "cm-callout-label") }) : hidden).range(start, after));
  }

  function decorate(view, live) {
    const { state } = view;
    const doc = state.doc;
    const ranges = view.hasFocus ? state.selection.ranges : [];
    const touches = (from, to) => ranges.some((r) => r.from <= to && r.to >= from);
    const onLines = (from, to) => touches(doc.lineAt(from).from, doc.lineAt(to).to);
    const out = [];
    out.doc = doc;

    // Une décoration par ligne d'un bloc, en se limitant à la partie visible.
    function eachLine(from, to, viewFrom, viewTo, fn) {
      const first = doc.lineAt(from).number, last = doc.lineAt(to).number;
      const start = Math.max(first, doc.lineAt(viewFrom).number), end = Math.min(last, doc.lineAt(viewTo).number);
      for (let n = start; n <= end; n++) fn(doc.line(n), n === first, n === last);
    }

    for (const { from: viewFrom, to: viewTo } of view.visibleRanges) {
      syntaxTree(state).iterate({
        from: viewFrom,
        to: viewTo,
        enter(ref) {
          const { name, from, to } = ref;
          const node = ref.node;
          const parent = node.parent;
          const heading = /^ATXHeading(\d)$/.exec(name) || /^SetextHeading(\d)$/.exec(name);
          if (heading) {
            out.push(line(`cm-heading cm-h${heading[1]}`).range(doc.lineAt(from).from));
            return;
          }
          switch (name) {
            case "HeaderMark": {
              if (!live || !parent || !parent.name.startsWith("ATX") || onLines(parent.from, parent.to)) return;
              const atStart = from === parent.from;
              const end = atStart && doc.sliceString(to, to + 1) === " " ? to + 1 : to;
              const start = !atStart && doc.sliceString(from - 1, from) === " " ? from - 1 : from;
              if (end > start) out.push(hidden.range(start, end));
              return;
            }
            case "EmphasisMark":
            case "StrikethroughMark":
            case "HighlightMark":
              if (live && parent && !touches(parent.from, parent.to)) out.push(hidden.range(from, to));
              return;
            case "CodeMark":
              if (live && parent && parent.name === "InlineCode" && !touches(parent.from, parent.to)) out.push(hidden.range(from, to));
              return;
            case "QuoteMark": {
              if (!live || onLines(from, to)) return;
              const end = doc.sliceString(to, to + 1) === " " ? to + 1 : to;
              out.push(hidden.range(from, end));
              return;
            }
            case "ListMark": {
              if (!live || !parent || !parent.parent || parent.parent.name !== "BulletList") return;
              const task = parent.getChild("Task");
              const marker = task && task.getChild("TaskMarker");
              if (marker) {
                if (!touches(from, marker.to)) out.push(hidden.range(from, Math.min(to + 1, marker.from)));
              } else if (!touches(from, to + 1)) {
                out.push(bullet.range(from, to));
              }
              return;
            }
            case "TaskMarker":
              if (live && !touches(from, to)) {
                out.push((/x/i.test(doc.sliceString(from + 1, from + 2)) ? checked : unchecked).range(from, to));
              }
              return;
            case "HorizontalRule":
              if (live && !onLines(from, to)) {
                out.push(line("cm-hr-line").range(doc.lineAt(from).from));
                out.push(rule.range(from, to));
              }
              return;
            case "FencedCode":
              eachLine(from, to, viewFrom, viewTo, (l, first, last) => {
                const cls = ["cm-codeblock"];
                if (first) cls.push("cm-codeblock-first", "cm-fence");
                if (last) cls.push("cm-codeblock-last");
                if (last && !first && /^\s*(`{3,}|~{3,})\s*$/.test(l.text)) cls.push("cm-fence");
                out.push(line(cls.join(" ")).range(l.from));
              });
              return;
            case "InlineMath": {
              const text = doc.sliceString(from, to);
              if (!live || touches(from, to) || text.includes("\n")) return false;
              const double = text.startsWith("$$");
              const tex = text.slice(double ? 2 : 1, double ? -2 : -1);
              out.push(Decoration.replace({ widget: new MathWidget(tex, double) }).range(from, to));
              return false;
            }
            case "BlockMath":
              // Rendu par le champ blockMath (un bloc couvre plusieurs lignes) ; ici, le LaTeX brut.
              eachLine(from, to, viewFrom, viewTo, (l) => out.push(line("cm-math-line").range(l.from)));
              return false;
            case "Frontmatter":
              eachLine(from, to, viewFrom, viewTo, (l, first, last) => {
                out.push(line(`cm-frontmatter${first ? " cm-frontmatter-first" : ""}${last ? " cm-frontmatter-last" : ""}`).range(l.from));
              });
              return false;
            case "Table":
              eachLine(from, to, viewFrom, viewTo, (l) => out.push(line("cm-table").range(l.from)));
              return;
            case "Blockquote": {
              const firstLine = doc.lineAt(from);
              const m = CALLOUT_RE.exec(firstLine.text);
              if (parent && parent.name === "Blockquote") {
                // Encadré dans un encadré : seulement le titre.
                if (!m) return;
                const type = CALLOUT_ALIASES[m[2].toLowerCase()] || m[2].toLowerCase();
                const titleFrom = firstLine.to - m[4].length;
                if (m[4]) out.push(Decoration.mark({ class: "cm-callout-nested-title", attributes: { "data-callout": type } }).range(titleFrom, firstLine.to));
                if (live && !touches(firstLine.from, firstLine.to)) calloutMarker(out, firstLine.from, m, type);
                return;
              }
              if (!m) {
                eachLine(from, to, viewFrom, viewTo, (l) => out.push(line("cm-quote").range(l.from)));
                return;
              }
              const type = CALLOUT_ALIASES[m[2].toLowerCase()] || m[2].toLowerCase();
              eachLine(from, to, viewFrom, viewTo, (l, first, last) => {
                const cls = ["cm-callout"];
                if (first) cls.push("cm-callout-title");
                if (last) cls.push("cm-callout-last");
                out.push(line(cls.join(" "), { "data-callout": type }).range(l.from));
              });
              if (live && !touches(firstLine.from, firstLine.to)) calloutMarker(out, firstLine.from, m, type);
              return;
            }
            case "WikiLink":
            case "Embed": {
              const open = name === "Embed" ? 3 : 2;
              const inner = doc.sliceString(from + open, to - 2);
              const bar = inner.indexOf("|");
              const target = bar < 0 ? inner : inner.slice(0, bar);
              const alias = bar < 0 ? "" : inner.slice(bar + 1);
              const page = target.split("#")[0].trim();
              const file = name === "Embed" ? findFile(page) : null;
              const near = touches(from, to);
              if (file && IMAGE_RE.test(page) && live && !near) {
                const width = /^\d+/.exec(alias);
                out.push(Decoration.replace({ widget: new ImageWidget(file.url, width ? +width[0] : 0, page) }).range(from, to));
                return false;
              }
              const heading = target.includes("#") ? target.slice(target.indexOf("#") + 1).replace(/^\^/, "") : "";
              const href = file ? file.url : page ? wikiUrl(page) + (heading ? "#" + encodeURIComponent(slug(heading)) : "") : "";
              const cls = "cm-wikilink" + (pageExists(page) ? "" : " is-unresolved");
              if (!live || near) {
                if (inner) out.push(linkMark(cls, href).range(from + open, to - 2));
                return false;
              }
              const shownFrom = bar < 0 ? from + open : from + open + bar + 1;
              out.push(hidden.range(from, shownFrom));
              if (to - 2 > shownFrom) out.push(linkMark(cls, href).range(shownFrom, to - 2));
              const hash = bar < 0 ? target.indexOf("#") : -1;
              if (hash >= 0) {
                const at = from + open + hash;
                const end = at + (target[hash + 1] === "^" ? 2 : 1);
                out.push((hash ? Decoration.replace({ widget: new TextWidget(" > ", "cm-wikilink-sep") }) : hidden).range(at, end));
              }
              out.push(hidden.range(to - 2, to));
              return false;
            }
            case "Link": {
              if (/^\[![\w-]+\]$/.test(doc.sliceString(from, to))) return false;
              const url = node.getChild("URL");
              let href = url ? doc.sliceString(url.from, url.to).replace(/^<|>$/g, "") : "";
              if (/^[^:/?#]+\.md(#.*)?$/i.test(href)) href = wikiUrl(decodeURIComponent(href.replace(/\.md(#.*)?$/i, "")));
              else if (!/^(https?:|mailto:|\/)/i.test(href)) href = "";
              const marks = node.getChildren("LinkMark");
              if (!live || touches(from, to) || marks.length < 2) {
                if (url && href) out.push(linkMark("cm-link", href).range(url.from, url.to));
                return;
              }
              const textFrom = marks[0].to, textTo = marks[1].from;
              out.push(hidden.range(from, textFrom));
              if (textTo > textFrom) out.push(linkMark("cm-link", href).range(textFrom, textTo));
              out.push(hidden.range(textTo, to));
              return;
            }
            case "URL":
              if (parent && (parent.name === "Link" || parent.name === "Image")) return;
              out.push(linkMark("cm-link", doc.sliceString(from, to).replace(/^www\./i, "https://www.")).range(from, to));
              return;
            case "Hashtag": {
              const tag = doc.sliceString(from + 1, to).toLowerCase();
              out.push(linkMark("cm-hashtag", "/tags/" + tag.split("/").map(encodeURIComponent).join("/")).range(from, to));
              return;
            }
          }
        },
      });
    }
    return Decoration.set(out, true);
  }

  function previewPlugin(live) {
    return ViewPlugin.fromClass(class {
      constructor(view) {
        this.decorations = decorate(view, live);
      }
      update(u) {
        if (u.docChanged || u.viewportChanged || u.selectionSet || u.focusChanged || syntaxTree(u.startState) !== syntaxTree(u.state)) {
          this.decorations = decorate(u.view, live);
        }
      }
    }, { decorations: (v) => v.decorations });
  }
  // Blocs $$ rendus par KaTeX quand le curseur n'y est pas. Un bloc couvre
  // plusieurs lignes : ce remplacement doit venir d'un champ d'état, pas du plugin.
  const CONTAINERS = new Set(["Document", "Blockquote", "BulletList", "OrderedList", "ListItem"]);

  function blockMathDecorations(state) {
    const ranges = state.selection.ranges;
    const out = [];
    syntaxTree(state).iterate({
      enter(node) {
        if (node.name !== "BlockMath") return CONTAINERS.has(node.name);
        if (!ranges.some((r) => r.from <= node.to && r.to >= node.from)) {
          const tex = mathSource(state.sliceDoc(node.from, node.to));
          if (tex && !looksLikeLatex(tex)) out.push(Decoration.replace({ widget: new MathWidget(tex, true) }).range(node.from, node.to));
        }
        return false;
      },
    });
    return Decoration.set(out);
  }

  const blockMath = StateField.define({
    create: blockMathDecorations,
    update(decorations, tr) {
      if (tr.docChanged || tr.selection || syntaxTree(tr.startState) !== syntaxTree(tr.state)) {
        return blockMathDecorations(tr.state);
      }
      return decorations;
    },
    provide: (field) => EditorView.decorations.from(field),
  });

  const livePreview = [previewPlugin(true), blockMath];
  const sourceView = previewPlugin(false);

  // -- Commandes de mise en forme ---------------------------------------------------------

  function wrap(before, after = before, placeholderText = "texte") {
    return (view) => {
      const { state } = view;
      view.dispatch(state.update(state.changeByRange((range) => {
        const text = state.sliceDoc(range.from, range.to);
        const outside = state.sliceDoc(range.from - before.length, range.to + after.length);
        if (range.from >= before.length && outside.startsWith(before) && outside.endsWith(after)
          && outside.length >= before.length + after.length + text.length) {
          return {
            changes: [{ from: range.from - before.length, to: range.from }, { from: range.to, to: range.to + after.length }],
            range: EditorSelection.range(range.from - before.length, range.to - before.length),
          };
        }
        if (text.length >= before.length + after.length && text.startsWith(before) && text.endsWith(after)) {
          const inner = text.slice(before.length, text.length - after.length);
          return { changes: { from: range.from, to: range.to, insert: inner }, range: EditorSelection.range(range.from, range.from + inner.length) };
        }
        const inner = text || placeholderText;
        return {
          changes: { from: range.from, to: range.to, insert: before + inner + after },
          range: EditorSelection.range(range.from + before.length, range.from + before.length + inner.length),
        };
      }), { scrollIntoView: true, userEvent: "input" }));
      return true;
    };
  }

  function selectedLines(state) {
    const lines = new Map();
    for (const r of state.selection.ranges) {
      for (let pos = r.from; pos <= r.to;) {
        const l = state.doc.lineAt(pos);
        lines.set(l.number, l);
        pos = l.to + 1;
      }
    }
    return [...lines.values()];
  }

  // Change le début des lignes sélectionnées : fn(texte de la ligne) → nouveau préfixe.
  function editLines(view, fn) {
    const changes = [];
    for (const l of selectedLines(view.state)) {
      const change = fn(l.text);
      if (change) changes.push({ from: l.from + change.from, to: l.from + change.to, insert: change.insert });
    }
    view.dispatch({ changes, scrollIntoView: true, userEvent: "input" });
    view.focus();
    return true;
  }

  const MARKER_RE = /^(\s*)([-*+] \[[ xX]\] |[-*+] |\d+[.)] )?/;

  function listCommand(prefix) {
    return (view) => {
      const all = selectedLines(view.state).every((l) => MARKER_RE.exec(l.text)[2] === prefix);
      return editLines(view, (text) => {
        const m = MARKER_RE.exec(text);
        const from = m[1].length, to = from + (m[2] || "").length;
        return { from, to, insert: all ? "" : prefix };
      });
    };
  }

  function headingCommand(view) {
    return editLines(view, (text) => {
      const m = /^(#{1,6}) /.exec(text);
      const level = m ? m[1].length : 1;
      const next = !m ? "## " : level >= 4 ? "" : "#".repeat(level + 1) + " ";
      return { from: 0, to: m ? m[0].length : 0, insert: next };
    });
  }

  // Ctrl+Entrée : texte → tâche → tâche cochée → tâche (comme Obsidian).
  function toggleTask(view) {
    return editLines(view, (text) => {
      const m = /^(\s*)([-*+] )(\[([ xX])\] )?/.exec(text);
      if (!m) {
        const indent = /^\s*/.exec(text)[0].length;
        return { from: indent, to: indent, insert: "- [ ] " };
      }
      const at = m[1].length + m[2].length;
      if (!m[3]) return { from: at, to: at, insert: "[ ] " };
      return { from: at + 1, to: at + 2, insert: m[4] === " " ? "x" : " " };
    });
  }

  function insertBlock(view, text, select) {
    const { state } = view;
    const pos = state.selection.main.from;
    const before = state.sliceDoc(0, pos);
    const lead = before === "" || before.endsWith("\n\n") ? "" : before.endsWith("\n") ? "\n" : "\n\n";
    const start = pos + lead.length;
    view.dispatch({
      changes: { from: pos, to: state.selection.main.to, insert: lead + text + "\n" },
      selection: select ? EditorSelection.range(start + select[0], start + select[1]) : { anchor: start + text.length + 1 },
      scrollIntoView: true,
      userEvent: "input",
    });
    view.focus();
    return true;
  }

  function selectedText(view) {
    const { from, to } = view.state.selection.main;
    return view.state.sliceDoc(from, to);
  }

  function replaceSelection(view, text) {
    view.dispatch(view.state.replaceSelection(text), { scrollIntoView: true, userEvent: "input" });
    view.focus();
  }

  // Formule : sur une ligne vide, un bloc $$ ; sinon $...$ autour de la sélection.
  function mathCommand(view) {
    const { state } = view;
    const range = state.selection.main;
    const current = state.doc.lineAt(range.from);
    if (range.empty && !current.text.trim()) {
      view.dispatch({
        changes: { from: current.from, to: current.to, insert: "$$\n\n$$" },
        selection: { anchor: current.from + 3 },
        scrollIntoView: true,
        userEvent: "input",
      });
      view.focus();
      return true;
    }
    return wrap("$", "$", "x")(view);
  }

  // Avec du texte sélectionné, taper * _ = ~ ` ou $ l'entoure (« Auto pair Markdown syntax »).
  const pairOnSelection = EditorView.inputHandler.of((view, from, to, text) => {
    if (from === to || text.length !== 1 || !"*_=~`$".includes(text)) return false;
    const mark = text === "=" || text === "~" ? text + text : text;
    return wrap(mark)(view);
  });

  // -- Autocomplétion des liens ---------------------------------------------------------------

  function findPages(query) {
    const q = normalize(query.trim());
    const scored = [];
    for (const c of choices) {
      const names = [c.link, c.title, ...c.aliases].map(normalize);
      if (q && !names.some((n) => n.includes(q))) continue;
      const alias = q ? c.aliases.find((a) => normalize(a).includes(q) && !normalize(c.title).includes(q)) : null;
      scored.push([q && names.some((n) => n.startsWith(q)) ? 0 : 1, c, alias]);
    }
    scored.sort((a, b) => a[0] - b[0] || a[1].title.localeCompare(b[1].title));
    const found = scored.slice(0, 40).map(([, c, alias]) => ({ ...c, alias }));
    const name = query.trim();
    if (name && !/[\\:*?"<>|#^[\]]/.test(name) && !choices.some((c) => normalize(c.link) === normalize(name))) {
      found.push({ link: name, title: name, folder: "", aliases: [], isNew: true });
    }
    return found;
  }

  function findFiles(query) {
    const q = normalize(query.trim());
    return attachments.filter((a) => !q || normalize(a.link).includes(q)).slice(0, 40);
  }

  function applyLink(text) {
    return (view, completion, from, to) => {
      const after = view.state.sliceDoc(to, to + 2);
      const end = after === "]]" ? to + 2 : after[0] === "]" ? to + 1 : to;
      view.dispatch({
        changes: { from, to: end, insert: text + "]]" },
        selection: { anchor: from + text.length + 2 },
        userEvent: "input.complete",
      });
    };
  }

  function linkCompletion(context) {
    const match = context.matchBefore(/!?\[\[[^[\]|#\n]*/);
    if (!match) return null;
    const embed = match.text.startsWith("!");
    const from = match.from + (embed ? 3 : 2);
    const query = match.text.slice(embed ? 3 : 2);
    const options = [];
    if (embed) {
      for (const a of findFiles(query)) {
        options.push({ label: a.link, detail: a.folder, type: IMAGE_RE.test(a.link) ? "image" : "file", apply: applyLink(a.link) });
      }
    }
    for (const c of findPages(query)) {
      if (c.isNew) {
        options.push({ label: c.link, detail: "nouvelle page", type: "new", apply: applyLink(c.link), boost: -99 });
      } else if (c.alias) {
        options.push({ label: c.alias, detail: `→ ${c.title}`, type: "page", apply: applyLink(`${c.link}|${c.alias}`) });
      } else {
        options.push({ label: c.title, detail: c.folder, type: "page", apply: applyLink(c.link) });
      }
    }
    return { from, options, filter: false };
  }

  // -- Fichiers : images collées ou glissées, .md ouverts ou glissés, téléchargement --------------

  function status(text, kind) {
    stateLabel.textContent = text;
    stateLabel.dataset.kind = kind || "";
  }

  function pastedName(file) {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    const stamp = `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
    const ext = (file.type.split("/")[1] || "png").replace("jpeg", "jpg").replace("svg+xml", "svg");
    return `Pasted image ${stamp}.${ext}`;
  }

  async function uploadFiles(view, list, pos) {
    if (!list.length) return;
    const data = new FormData();
    data.append("csrfmiddlewaretoken", csrf);
    data.append("pour_note", noteKey);
    for (const file of list) {
      data.append("fichiers", file, file.name);
      data.append("chemins", file.name);
    }
    status(`Envoi de ${list.length} fichier${list.length > 1 ? "s" : ""}…`);
    let json = {};
    let response;
    try {
      response = await fetch(importUrl, { method: "POST", body: data, headers: { Accept: "application/json" } });
      json = await response.json();
    } catch (e) {
      status("Envoi impossible : serveur injoignable ou session expirée.", "error");
      return;
    }
    if (!response.ok) return status(json.error || "Envoi impossible.", "error");
    const links = [];
    const errors = [];
    for (const r of json.results || []) {
      if (r.ok) {
        const a = { link: r.link, folder: r.path.includes("/") ? r.path.slice(0, r.path.lastIndexOf("/")) : "", url: r.url };
        attachments.push(a);
        rememberFile(a);
        links.push(`![[${r.link}]]`);
      } else {
        errors.push(`${r.name} : ${r.message}`);
      }
    }
    if (links.length) {
      const at = pos == null ? view.state.selection.main.head : Math.min(pos, view.state.doc.length);
      const text = links.join("\n");
      view.dispatch({ changes: { from: at, insert: text }, selection: { anchor: at + text.length }, userEvent: "input" });
    }
    status(errors.length ? errors.join(" · ") : `${links.length} fichier${links.length > 1 ? "s" : ""} ajouté${links.length > 1 ? "s" : ""} au coffre`,
      errors.length ? "error" : "ok");
  }

  // -- LaTeX : un cours .tex est converti en page (chapitres, formules, encadrés, tableaux) --------

  function looksLikeLatex(text) {
    return /\\documentclass|\\begin\s*\{document\}/.test(text)
      || (text.match(/\\(chapter|section|subsection)\*?\{|\\begin\{(itemize|enumerate|tabular|figure|theorem|definition)\}/g) || []).length >= 3;
  }

  async function convertLatex(source) {
    const data = new FormData();
    data.append("csrfmiddlewaretoken", csrf);
    data.append("source", source);
    status("Conversion du LaTeX…");
    const response = await fetch(latexUrl, { method: "POST", body: data, headers: { Accept: "application/json" } });
    const json = await response.json().catch(() => ({}));
    if (!response.ok || typeof json.markdown !== "string") {
      throw new Error(json.error || "Conversion impossible (session expirée ?).");
    }
    return json.markdown;
  }

  async function convertDocument() {
    const { from, to } = view.state.selection.main;
    const whole = from === to;
    const source = whole ? view.state.doc.toString() : view.state.sliceDoc(from, to);
    if (!source.trim()) return status("Rien à convertir : collez d'abord le LaTeX.", "error");
    try {
      const markdown = await convertLatex(source);
      view.dispatch({
        changes: whole ? { from: 0, to: view.state.doc.length, insert: markdown } : { from, to, insert: markdown },
        selection: { anchor: whole ? 0 : from },
        scrollIntoView: true,
        userEvent: "input",
      });
      status("LaTeX converti : vérifiez puis enregistrez (Ctrl+Z pour annuler).", "dirty");
      view.focus();
    } catch (e) {
      status(e.message, "error");
    }
  }

  const isLatexFile = (file) => /\.(tex|latex)$/i.test(file.name);
  const isMarkdown = (file) => /\.(md|markdown|txt|tex|latex)$/i.test(file.name);
  const readText = (file) => file.text().then((t) => t.replace(/^﻿/, "").replace(/\r\n?/g, "\n"));

  async function insertMarkdownFiles(view, list, pos) {
    let texts;
    try {
      texts = await Promise.all(list.map(async (file) => (isLatexFile(file) ? convertLatex(await readText(file)) : readText(file))));
    } catch (e) {
      return status(e.message, "error");
    }
    const at = Math.min(pos, view.state.doc.length);
    const text = texts.join("\n\n");
    view.dispatch({ changes: { from: at, insert: text }, selection: { anchor: at + text.length }, userEvent: "input" });
    view.focus();
  }

  function handleFiles(view, list, pos) {
    const md = list.filter(isMarkdown);
    const others = list.filter((f) => !isMarkdown(f));
    if (md.length) insertMarkdownFiles(view, md, pos);
    if (others.length) uploadFiles(view, others, pos);
  }

  const fileEvents = EditorView.domEventHandlers({
    paste(e, view) {
      const list = [...(e.clipboardData ? e.clipboardData.files : [])];
      if (!list.length) {
        const text = e.clipboardData ? e.clipboardData.getData("text/plain") : "";
        if (!text || !looksLikeLatex(text)) return false;
        e.preventDefault();
        pastedLatex = text;
        latexDialog.showModal();
        return true;
      }
      e.preventDefault();
      uploadFiles(view, list.map((f) => (f.type.startsWith("image/") ? new File([f], pastedName(f), { type: f.type }) : f)));
      return true;
    },
    drop(e, view) {
      const list = [...(e.dataTransfer ? e.dataTransfer.files : [])];
      if (!list.length) return false;
      e.preventDefault();
      const pos = view.posAtCoords({ x: e.clientX, y: e.clientY });
      handleFiles(view, list, pos == null ? view.state.selection.main.head : pos);
      return true;
    },
    mousedown(e) {
      // Ctrl+clic (Cmd+clic sur Mac) : ouvre le lien dans un nouvel onglet.
      if (!(e.ctrlKey || e.metaKey) || e.button !== 0) return false;
      const el = e.target.closest("[data-href]");
      if (!el) return false;
      e.preventDefault();
      window.open(el.dataset.href, "_blank", "noopener");
      return true;
    },
  });

  function download() {
    const blob = new Blob([view.state.doc.toString()], { type: "text/markdown;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `${noteName}.md`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  }

  // -- Enregistrement --------------------------------------------------------------------------

  let savedDoc = null;
  let saving = null;
  let saveAgain = false;
  let conflict = false;
  let submitting = false;
  let autosaveTimer = null;
  const isDirty = () => !view.state.doc.eq(savedDoc);

  function refreshState() {
    if (saving || stateLabel.dataset.kind === "error") return;
    if (isDirty()) status("Modifications non enregistrées", "dirty");
  }

  function save() {
    if (saving) {
      saveAgain = true;
      return saving;
    }
    const doc = view.state.doc;
    const data = new FormData();
    data.append("csrfmiddlewaretoken", csrf);
    data.append("version", versionInput.value);
    data.append("content", doc.toString());
    status("Enregistrement…");
    saving = fetch(form.action, { method: "POST", body: data, headers: { Accept: "application/json" } })
      .then(async (response) => {
        const json = await response.json().catch(() => ({}));
        if (response.ok && json.version) {
          versionInput.value = json.version;
          savedDoc = doc;
          conflict = false;
          if (json.url) closeLink.href = json.url;
          const now = new Date().toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
          status(`Enregistré à ${now}`, "ok");
        } else {
          conflict = response.status === 409;
          status(json.error || "Échec de l'enregistrement (session expirée ?).", "error");
        }
      })
      .catch(() => status("Serveur injoignable : modifications non enregistrées.", "error"))
      .finally(() => {
        saving = null;
        if (saveAgain) {
          saveAgain = false;
          if (isDirty() && !conflict) save();
        }
        refreshState();
      });
    return saving;
  }

  function scheduleAutosave() {
    clearTimeout(autosaveTimer);
    if (autosaveBox.checked && !conflict) autosaveTimer = setTimeout(() => isDirty() && save(), 2000);
  }

  // -- Compteur de mots et plan ----------------------------------------------------------------

  const outline = document.querySelector("[data-outline]");
  let infoTimer = null;

  function headings(text) {
    const found = [];
    let fence = null;
    let pos = 0;
    for (const l of text.split("\n")) {
      const f = /^\s*(`{3,}|~{3,})/.exec(l);
      if (f && (!fence || f[1][0] === fence[0] && f[1].length >= fence.length)) fence = fence ? null : f[1];
      else if (!fence) {
        const h = /^(#{1,6})\s+(.+?)\s*#*\s*$/.exec(l);
        if (h) found.push({ level: h[1].length, text: h[2].replace(/\[\[([^\]|]*\|)?([^\]]*)\]\]/g, "$2").replace(/[*_=~`]/g, ""), pos });
      }
      pos += l.length + 1;
    }
    return found;
  }

  function refreshInfo() {
    const text = view.state.doc.toString();
    const body = text.replace(/^---\n[\s\S]*?\n---(\n|$)/, "");
    const words = (body.match(/[\p{L}\p{N}][\p{L}\p{N}'’-]*/gu) || []).length;
    countLabel.textContent = `${words} mot${words > 1 ? "s" : ""} · ${text.length} caractère${text.length > 1 ? "s" : ""}`;
    if (!outline) return;
    const list = headings(text);
    if (!list.length) {
      outline.innerHTML = '<p class="muted">Les titres de la page apparaîtront ici.</p>';
      return;
    }
    const ul = document.createElement("ul");
    const min = Math.min(...list.map((h) => h.level));
    for (const h of list) {
      const li = document.createElement("li");
      li.style.paddingLeft = `${(h.level - min) * 0.8}rem`;
      const button = document.createElement("button");
      button.type = "button";
      button.className = "link-button";
      button.textContent = h.text;
      button.addEventListener("click", () => {
        if (mode === "reading") setMode(editMode);
        view.dispatch({ selection: { anchor: h.pos }, effects: EditorView.scrollIntoView(h.pos, { y: "start", yMargin: 120 }) });
        view.focus();
      });
      li.appendChild(button);
      ul.appendChild(li);
    }
    outline.replaceChildren(ul);
  }

  // -- Création de l'éditeur ---------------------------------------------------------------------

  const preview_ = new Compartment();
  const stickyTop = () => toolbar.getBoundingClientRect().height + (parseFloat(getComputedStyle(form).getPropertyValue("--sticky-top")) || 0);

  const appKeymap = [
    { key: "Mod-s", run: () => (save(), true), preventDefault: true },
    { key: "Mod-b", run: wrap("**", "**", "texte en gras") },
    { key: "Mod-i", run: wrap("*", "*", "texte en italique") },
    { key: "Mod-Shift-h", run: wrap("==", "==", "texte surligné") },
    { key: "Mod-Shift-c", run: wrap("`", "`", "code") },
    { key: "Mod-/", run: wrap("%%", "%%", "commentaire") },
    { key: "Mod-k", run: () => (actions["page-link"](), true) },
    { key: "Mod-e", run: () => (setMode("reading"), true), preventDefault: true },
    { key: "Mod-Enter", run: toggleTask },
    { key: "Mod-Shift-m", run: mathCommand },
  ];

  const view = new EditorView({
    parent: host,
    state: EditorState.create({
      doc: textarea.value,
      extensions: [
        history(),
        drawSelection(),
        dropCursor(),
        indentOnInput(),
        EditorView.lineWrapping,
        markdown({
          base: markdownLanguage,
          codeLanguages: (info) => codeLanguage(info),
          extensions: [Frontmatter, WikiLink, Highlight, Comment, Hashtag, Math_],
        }),
        markdownLanguage.data.of({ closeBrackets: { brackets: ["(", "[", "{"] } }),
        syntaxHighlighting(obsidianHighlight),
        closeBrackets(),
        autocompletion({ override: [linkCompletion], icons: false, activateOnTyping: true }),
        highlightSelectionMatches(),
        search({ top: true }),
        pairOnSelection,
        fileEvents,
        preview_.of(stored("wiki-editor-mode", "live") === "source" ? sourceView : livePreview),
        placeholder("Écrivez ici… Tapez [[ pour lier une page."),
        EditorView.contentAttributes.of({ spellcheck: "true", lang: "fr", autocapitalize: "sentences", "aria-label": "Contenu de la page" }),
        EditorView.scrollMargins.of(() => ({ top: stickyTop(), bottom: footer.getBoundingClientRect().height })),
        EditorView.darkTheme.of(window.matchMedia("(prefers-color-scheme: dark)").matches),
        EditorView.theme({
          "&": { color: "var(--text)", backgroundColor: "transparent", fontSize: "1rem" },
          "&.cm-focused": { outline: "none" },
          ".cm-scroller": { fontFamily: "var(--editor-font)", lineHeight: "1.65" },
          ".cm-content": { caretColor: "var(--accent)", padding: ".75rem 0 4rem" },
          ".cm-line": { padding: "0 .25rem" },
          ".cm-cursor, .cm-dropCursor": { borderLeftColor: "var(--accent)", borderLeftWidth: "2px" },
          ".cm-placeholder": { color: "var(--muted)" },
          ".cm-panels": { backgroundColor: "var(--bg-alt)", color: "var(--text)" },
          ".cm-panels-top": { top: "calc(var(--sticky-top, 0px) + var(--toolbar-h, 0px))", borderBottom: "1px solid var(--border)" },
          ".cm-panel input, .cm-panel button": { fontSize: ".85rem" },
          ".cm-searchMatch": { backgroundColor: "var(--mark)" },
          ".cm-tooltip": { backgroundColor: "var(--bg)", color: "var(--text)", border: "1px solid var(--border)", borderRadius: "8px" },
          ".cm-tooltip.cm-tooltip-autocomplete > ul": { fontFamily: "var(--font)", maxHeight: "16rem" },
          ".cm-tooltip.cm-tooltip-autocomplete > ul > li": { padding: ".25rem .6rem" },
          ".cm-tooltip.cm-tooltip-autocomplete > ul > li[aria-selected]": { backgroundColor: "var(--accent-soft)", color: "var(--text)" },
          ".cm-completionDetail": { color: "var(--muted)", fontStyle: "normal", marginLeft: ".75em", fontSize: ".85em" },
          ".cm-completionMatchedText": { textDecoration: "none", fontWeight: "700" },
        }),
        EditorState.phrases.of({
          Find: "Rechercher", Replace: "Remplacer", next: "suivant", previous: "précédent", all: "tout",
          "match case": "respecter la casse", "by word": "mot entier", regexp: "expression régulière",
          replace: "remplacer", "replace all": "tout remplacer", close: "fermer", "current match": "occurrence actuelle",
          "replaced match on line $": "occurrence remplacée ligne $", "replaced $ matches": "$ occurrences remplacées",
          "on line": "ligne", "Go to line": "Aller à la ligne", go: "OK", "Control character": "Caractère de contrôle",
        }),
        Prec.high(keymap.of(appKeymap)),
        keymap.of([...closeBracketsKeymap, ...completionKeymap, ...searchKeymap, ...historyKeymap, indentWithTab, ...defaultKeymap]),
        EditorView.updateListener.of((u) => {
          if (!u.docChanged) return;
          if (stateLabel.dataset.kind !== "error" || !conflict) status("", "");
          refreshState();
          scheduleAutosave();
          clearTimeout(infoTimer);
          infoTimer = setTimeout(() => {
            refreshInfo();
            refreshLatexNotice();
          }, 300);
        }),
      ],
    }),
  });
  savedDoc = view.state.doc;

  textarea.hidden = true;
  host.hidden = false;
  toolbar.hidden = false;
  form.querySelector("[data-action=save]").hidden = false;
  form.querySelector(".editor-status").hidden = false;
  autosaveBox.checked = stored("wiki-editor-autosave", "0") === "1";
  refreshInfo();

  // Barre d'outils et recherche collées en haut de l'écran (sous la barre du téléphone).
  function layout() {
    const topbar = document.querySelector(".topbar");
    const top = topbar && getComputedStyle(topbar).display !== "none" ? topbar.getBoundingClientRect().height : 0;
    form.style.setProperty("--sticky-top", `${top}px`);
    form.style.setProperty("--toolbar-h", `${toolbar.getBoundingClientRect().height}px`);
  }
  layout();
  window.addEventListener("resize", layout);
  if (window.ResizeObserver) new ResizeObserver(layout).observe(toolbar);

  // -- Modes : aperçu en direct, source, lecture ---------------------------------------------------

  let mode = stored("wiki-editor-mode", "live") === "source" ? "source" : "live";
  let editMode = mode;
  host.classList.toggle("is-source", mode === "source");

  async function showReading() {
    const data = new FormData();
    data.append("content", view.state.doc.toString());
    data.append("csrfmiddlewaretoken", csrf);
    preview.innerHTML = '<p class="muted">Chargement…</p>';
    host.hidden = true;
    preview.hidden = false;
    try {
      const response = await fetch(previewUrl, { method: "POST", body: data });
      preview.innerHTML = response.ok ? await response.text() : "<p>Aperçu indisponible.</p>";
    } catch (e) {
      preview.innerHTML = "<p>Aperçu indisponible : serveur injoignable.</p>";
    }
    if (window.wikiEnhance) window.wikiEnhance(preview);
  }

  function setMode(next, focus = true) {
    if (next === "reading" && mode === "reading") next = editMode;
    mode = next;
    form.querySelectorAll("[data-mode]").forEach((b) => b.setAttribute("aria-checked", String(b.dataset.mode === next)));
    if (next === "reading") return showReading();
    editMode = next;
    store("wiki-editor-mode", next);
    preview.hidden = true;
    host.hidden = false;
    host.classList.toggle("is-source", next === "source");
    view.dispatch({ effects: preview_.reconfigure(next === "source" ? sourceView : livePreview) });
    if (focus) view.focus();
  }
  setMode(mode, !textarea.value.trim());

  form.querySelectorAll("[data-mode]").forEach((b) => b.addEventListener("click", () => setMode(b.dataset.mode)));
  document.addEventListener("keydown", (e) => {
    if (e.defaultPrevented || !(e.ctrlKey || e.metaKey) || e.altKey || e.shiftKey || document.querySelector("dialog[open]")) return;
    const key = e.key.toLowerCase();
    if (key === "e") {
      e.preventDefault();
      setMode(mode === "reading" ? editMode : "reading");
    } else if (key === "s") {
      e.preventDefault();
      save();
    }
  });

  // Panneaux latéraux masqués pour écrire en plein écran.
  const focusButton = form.querySelector("[data-action=focus]");
  function setFocus(on) {
    document.body.classList.toggle("editor-focus", on);
    focusButton.setAttribute("aria-pressed", String(on));
    store("wiki-editor-focus", on ? "1" : "0");
    layout();
  }
  setFocus(stored("wiki-editor-focus", "0") === "1");

  // -- Fenêtre « Lien vers une page » ---------------------------------------------------------------

  function renderChoices(list, items, active, onPick) {
    list.replaceChildren();
    items.forEach((item, i) => {
      const li = document.createElement("li");
      li.setAttribute("role", "option");
      li.className = i === active ? "active" : "";
      const title = document.createElement("span");
      title.textContent = item.isNew ? `Nouvelle page « ${item.link} »` : item.title;
      li.appendChild(title);
      const detail = item.isNew ? "sera créée en cliquant sur le lien" : item.folder;
      if (detail) {
        const small = document.createElement("small");
        small.textContent = detail;
        li.appendChild(small);
      }
      li.addEventListener("mousedown", (e) => {
        e.preventDefault();
        onPick(i);
      });
      list.appendChild(li);
    });
  }

  function wikilink(link, label) {
    return label && label !== link ? `[[${link}|${label}]]` : `[[${link}]]`;
  }

  const pageDialog = document.getElementById("page-link-dialog");
  const pageSearch = document.getElementById("page-search");
  const pageList = document.getElementById("page-choices");
  const pageLabel = document.getElementById("page-label");
  let pageItems = [];
  let pageActive = 0;

  function refreshPageList() {
    pageItems = findPages(pageSearch.value);
    pageActive = Math.min(pageActive, Math.max(pageItems.length - 1, 0));
    renderChoices(pageList, pageItems, pageActive, (i) => {
      pageActive = i;
      insertPageLink();
    });
  }

  function insertPageLink() {
    const item = pageItems[pageActive];
    if (!item) return pageSearch.focus();
    pageDialog.close();
    replaceSelection(view, wikilink(item.link, pageLabel.value.trim()));
  }

  pageSearch.addEventListener("input", () => {
    pageActive = 0;
    refreshPageList();
  });
  pageSearch.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      const n = pageItems.length || 1;
      pageActive = (pageActive + (e.key === "ArrowDown" ? 1 : n - 1)) % n;
      refreshPageList();
    } else if (e.key === "Enter") {
      e.preventDefault();
      insertPageLink();
    }
  });
  pageLabel.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      insertPageLink();
    }
  });
  document.getElementById("page-ok").addEventListener("click", insertPageLink);

  // -- Fenêtre « Lien web » ------------------------------------------------------------------------

  const webDialog = document.getElementById("web-link-dialog");
  const webUrl = document.getElementById("web-url");
  const webLabel = document.getElementById("web-label");

  function insertWebLink() {
    let url = webUrl.value.trim();
    if (!url) return webUrl.focus();
    if (!/^[a-z][\w+.-]*:/i.test(url)) url = "https://" + url;
    webDialog.close();
    replaceSelection(view, `[${webLabel.value.trim() || url}](${url.replace(/ /g, "%20").replace(/\)/g, "%29")})`);
  }

  document.getElementById("web-ok").addEventListener("click", insertWebLink);
  [webUrl, webLabel].forEach((input) => input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      insertWebLink();
    }
  }));

  // -- Collage de LaTeX : convertir ou coller tel quel -----------------------------------------------

  const latexDialog = document.getElementById("latex-paste-dialog");
  let pastedLatex = "";
  latexDialog.querySelectorAll("[data-paste-choice]").forEach((button) => button.addEventListener("click", async () => {
    latexDialog.close();
    let text = pastedLatex;
    if (button.dataset.pasteChoice === "convert") {
      try {
        text = await convertLatex(pastedLatex);
        status("LaTeX converti : vérifiez puis enregistrez (Ctrl+Z pour annuler).", "dirty");
      } catch (e) {
        return status(e.message, "error");
      }
    }
    replaceSelection(view, text);
  }));

  // Page qui contient du LaTeX brut (collé avant cette fonction) : proposer la conversion.
  const latexNotice = form.querySelector("[data-latex-notice]");
  function refreshLatexNotice() {
    latexNotice.hidden = !looksLikeLatex(view.state.doc.toString());
  }
  latexNotice.querySelector("[data-action=latex]").addEventListener("click", () => convertDocument());
  refreshLatexNotice();

  // -- Fenêtre « Ouvrir un .md » ---------------------------------------------------------------------

  const mdInput = form.querySelector("[data-md-input]");
  const mdDialog = document.getElementById("open-md-dialog");
  let mdText = "";

  mdInput.addEventListener("change", async () => {
    const file = mdInput.files[0];
    mdInput.value = "";
    if (!file) return;
    try {
      mdText = isLatexFile(file) ? await convertLatex(await readText(file)) : await readText(file);
    } catch (e) {
      return status(e.message, "error");
    }
    if (!view.state.doc.toString().trim()) return useMarkdown("replace");
    mdDialog.querySelector("[data-md-name]").textContent = `« ${file.name} »`;
    mdDialog.showModal();
  });

  function useMarkdown(how) {
    if (mdDialog.open) mdDialog.close();
    if (how === "replace") {
      view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: mdText }, selection: { anchor: 0 }, userEvent: "input" });
      view.focus();
    } else {
      replaceSelection(view, mdText);
    }
    status("Contenu du fichier chargé : pensez à enregistrer.", "dirty");
  }
  mdDialog.querySelectorAll("[data-md-choice]").forEach((b) => b.addEventListener("click", () => useMarkdown(b.dataset.mdChoice)));

  const attachInput = form.querySelector("[data-attach-input]");
  attachInput.addEventListener("change", () => {
    const list = [...attachInput.files];
    attachInput.value = "";
    handleFiles(view, list, view.state.selection.main.head);
  });

  document.querySelectorAll("[data-close]").forEach((button) => {
    button.addEventListener("click", () => button.closest("dialog").close());
  });
  document.querySelectorAll("dialog").forEach((dialog) => {
    dialog.addEventListener("close", () => view.focus());
  });

  // -- Boutons ------------------------------------------------------------------------------------------

  const actions = {
    "page-link"() {
      pageSearch.value = "";
      pageLabel.value = selectedText(view).trim();
      pageActive = 0;
      refreshPageList();
      pageDialog.showModal();
      pageSearch.focus();
    },
    "web-link"() {
      const text = selectedText(view).trim();
      const isUrl = /^(https?:\/\/|www\.)/i.test(text);
      webUrl.value = isUrl ? text : "";
      webLabel.value = isUrl ? "" : text;
      webDialog.showModal();
      webUrl.focus();
    },
    attach: () => attachInput.click(),
    bold: () => wrap("**", "**", "texte en gras")(view),
    italic: () => wrap("*", "*", "texte en italique")(view),
    strike: () => wrap("~~", "~~", "texte barré")(view),
    highlight: () => wrap("==", "==", "texte surligné")(view),
    code: () => wrap("`", "`", "code")(view),
    heading: () => headingCommand(view),
    list: () => listCommand("- ")(view),
    task: () => listCommand("- [ ] ")(view),
    callout: () => {
      const title = selectedText(view).trim() || "Titre";
      return insertBlock(view, `> [!note] ${title}\n> Texte de l'encadré`, [`> [!note] ${title}\n> `.length, `> [!note] ${title}\n> Texte de l'encadré`.length]);
    },
    table: () => insertBlock(view, "| Colonne 1 | Colonne 2 |\n| --- | --- |\n| Texte | Texte |", [2, 11]),
    math: () => mathCommand(view),
    codeblock: () => {
      const code = selectedText(view) || "code";
      return insertBlock(view, "```bash\n" + code + "\n```", [3, 7]);
    },
    "open-md": () => mdInput.click(),
    latex: () => convertDocument(),
    "download-md": download,
    save: () => save(),
    focus: () => setFocus(!document.body.classList.contains("editor-focus")),
  };

  const fileMenu = toolbar.querySelector(".toolbar-menu");
  document.addEventListener("click", (e) => {
    if (fileMenu.open && !fileMenu.contains(e.target)) fileMenu.open = false;
  });

  toolbar.querySelectorAll("[data-action]").forEach((button) => {
    button.addEventListener("click", () => {
      fileMenu.open = false;
      const action = button.dataset.action;
      const keepsMode = ["focus", "download-md", "open-md"].includes(action);
      if (mode === "reading" && !keepsMode) setMode(editMode);
      actions[action]();
      if (!["page-link", "web-link", "attach", "open-md", "download-md", "focus", "latex"].includes(action)) view.focus();
    });
  });
  form.querySelector("[data-action=save]").addEventListener("click", () => save());

  autosaveBox.addEventListener("change", () => {
    store("wiki-editor-autosave", autosaveBox.checked ? "1" : "0");
    if (autosaveBox.checked && isDirty()) save();
  });

  // « Enregistrer et fermer » : le formulaire classique, avec le texte de l'éditeur.
  form.addEventListener("submit", () => {
    textarea.value = view.state.doc.toString();
    submitting = true;
  });
  window.addEventListener("beforeunload", (e) => {
    if (!submitting && isDirty()) e.preventDefault();
  });
})();
