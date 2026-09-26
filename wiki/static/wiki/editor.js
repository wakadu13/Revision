// Éditeur de pages : insertion de liens sans écrire la syntaxe à la main.
(function () {
  const textarea = document.getElementById("editor");
  if (!textarea) return;
  const form = document.getElementById("editor-form");
  const choices = JSON.parse(document.getElementById("link-choices").textContent);
  const suggestions = document.querySelector(".suggestions");
  const preview = document.querySelector(".preview");
  let dirty = false;
  let submitting = false;

  // -- Outils ---------------------------------------------------------------

  function normalize(s) {
    return s.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
  }

  function findPages(query) {
    const q = normalize(query.trim());
    const scored = [];
    for (const c of choices) {
      const names = [c.link, c.title, ...c.aliases].map(normalize);
      if (q && !names.some((n) => n.includes(q))) continue;
      scored.push([q && names.some((n) => n.startsWith(q)) ? 0 : 1, c]);
    }
    scored.sort((a, b) => a[0] - b[0] || a[1].title.localeCompare(b[1].title));
    const found = scored.slice(0, 30).map((s) => s[1]);
    const name = query.trim();
    if (name && !/[\\:*?"<>|#^\[\]]/.test(name) && !choices.some((c) => normalize(c.link) === normalize(name))) {
      found.push({ link: name, title: name, folder: "", aliases: [], isNew: true });
    }
    return found;
  }

  function wikilink(link, label) {
    return label && label !== link ? `[[${link}|${label}]]` : `[[${link}]]`;
  }

  function changed() {
    dirty = true;
  }

  // Remplace la sélection (ou le texte entre start et end) en gardant l'annulation Ctrl+Z.
  function replaceRange(text, start = textarea.selectionStart, end = textarea.selectionEnd) {
    textarea.focus();
    textarea.setSelectionRange(start, end);
    if (!document.execCommand("insertText", false, text)) {
      textarea.setRangeText(text, start, end, "end");
    }
    changed();
  }

  function selectedText() {
    return textarea.value.slice(textarea.selectionStart, textarea.selectionEnd);
  }

  function wrap(before, after, placeholder) {
    const start = textarea.selectionStart;
    const text = selectedText() || placeholder;
    replaceRange(before + text + after);
    textarea.setSelectionRange(start + before.length, start + before.length + text.length);
  }

  function prefixLines(prefix) {
    const value = textarea.value;
    const start = value.lastIndexOf("\n", textarea.selectionStart - 1) + 1;
    let end = value.indexOf("\n", textarea.selectionEnd);
    if (end === -1) end = value.length;
    const lines = value.slice(start, end).split("\n").map((l) => (l.startsWith(prefix) ? l : prefix + l));
    replaceRange(lines.join("\n"), start, end);
  }

  function insertBlock(text) {
    const before = textarea.value.slice(0, textarea.selectionStart);
    const lead = before === "" || before.endsWith("\n\n") ? "" : before.endsWith("\n") ? "\n" : "\n\n";
    replaceRange(lead + text + "\n");
  }

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

  // -- Suggestions en tapant [[ ----------------------------------------------

  let suggestItems = [];
  let suggestActive = 0;

  function currentQuery() {
    const before = textarea.value.slice(0, textarea.selectionStart);
    const m = before.match(/\[\[([^\[\]|#\n]*)$/);
    return m ? m[1] : null;
  }

  function caretPosition() {
    const style = getComputedStyle(textarea);
    const mirror = document.createElement("div");
    for (const prop of ["boxSizing", "width", "fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing",
      "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "borderTopWidth", "borderLeftWidth", "tabSize"]) {
      mirror.style[prop] = style[prop];
    }
    Object.assign(mirror.style, { position: "absolute", visibility: "hidden", whiteSpace: "pre-wrap", overflowWrap: "break-word" });
    mirror.textContent = textarea.value.slice(0, textarea.selectionStart);
    const marker = document.createElement("span");
    marker.textContent = "​";
    mirror.appendChild(marker);
    document.body.appendChild(mirror);
    const pos = { top: marker.offsetTop + marker.offsetHeight - textarea.scrollTop, left: marker.offsetLeft };
    mirror.remove();
    return pos;
  }

  function hideSuggestions() {
    suggestions.hidden = true;
    suggestItems = [];
  }

  function updateSuggestions() {
    const query = currentQuery();
    if (query === null) return hideSuggestions();
    suggestItems = findPages(query).slice(0, 10);
    if (!suggestItems.length) return hideSuggestions();
    suggestActive = 0;
    renderChoices(suggestions, suggestItems, suggestActive, pickSuggestion);
    const pos = caretPosition();
    suggestions.style.top = `${textarea.offsetTop + pos.top + 4}px`;
    suggestions.style.left = `${Math.min(textarea.offsetLeft + pos.left, textarea.offsetLeft + textarea.clientWidth - 260)}px`;
    suggestions.hidden = false;
  }

  function pickSuggestion(i) {
    const item = suggestItems[i];
    const query = currentQuery();
    if (!item || query === null) return;
    const caret = textarea.selectionStart;
    const start = caret - query.length - 2;
    const end = textarea.value.startsWith("]]", caret) ? caret + 2 : caret;
    replaceRange(wikilink(item.link), start, end);
    hideSuggestions();
  }

  textarea.addEventListener("input", () => {
    changed();
    updateSuggestions();
  });
  textarea.addEventListener("click", updateSuggestions);
  textarea.addEventListener("blur", () => setTimeout(hideSuggestions, 100));

  textarea.addEventListener("keydown", (e) => {
    if (!suggestions.hidden) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        const n = suggestItems.length;
        suggestActive = (suggestActive + (e.key === "ArrowDown" ? 1 : n - 1)) % n;
        renderChoices(suggestions, suggestItems, suggestActive, pickSuggestion);
        return;
      }
      if (e.key === "Enter" || e.key === "Tab") {
        e.preventDefault();
        return pickSuggestion(suggestActive);
      }
      if (e.key === "Escape") {
        e.preventDefault();
        return hideSuggestions();
      }
    }
    if (e.ctrlKey || e.metaKey) {
      const key = e.key.toLowerCase();
      const shortcuts = { k: "page-link", b: "bold", i: "italic" };
      if (key === "s") {
        e.preventDefault();
        form.requestSubmit();
      } else if (shortcuts[key]) {
        e.preventDefault();
        actions[shortcuts[key]]();
      }
    }
  });

  // -- Fenêtre « Lien vers une page » -----------------------------------------

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
    replaceRange(wikilink(item.link, pageLabel.value.trim()));
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

  // -- Fenêtre « Lien web » ---------------------------------------------------

  const webDialog = document.getElementById("web-link-dialog");
  const webUrl = document.getElementById("web-url");
  const webLabel = document.getElementById("web-label");

  function insertWebLink() {
    let url = webUrl.value.trim();
    if (!url) return webUrl.focus();
    if (!/^[a-z][\w+.-]*:/i.test(url)) url = "https://" + url;
    webDialog.close();
    replaceRange(`[${webLabel.value.trim() || url}](${url.replace(/ /g, "%20").replace(/\)/g, "%29")})`);
  }

  document.getElementById("web-ok").addEventListener("click", insertWebLink);
  [webUrl, webLabel].forEach((input) => input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      insertWebLink();
    }
  }));

  document.querySelectorAll("[data-close]").forEach((button) => {
    button.addEventListener("click", () => button.closest("dialog").close());
  });
  document.querySelectorAll("dialog").forEach((dialog) => {
    dialog.addEventListener("close", () => textarea.focus());
  });

  // -- Aperçu ------------------------------------------------------------------

  const previewButton = document.querySelector('[data-action="preview"]');

  async function togglePreview() {
    const show = preview.hidden;
    previewButton.setAttribute("aria-pressed", String(show));
    if (!show) {
      preview.hidden = true;
      textarea.hidden = false;
      return textarea.focus();
    }
    const data = new FormData();
    data.append("content", textarea.value);
    data.append("csrfmiddlewaretoken", form.querySelector("[name=csrfmiddlewaretoken]").value);
    const response = await fetch(form.dataset.previewUrl, { method: "POST", body: data });
    preview.innerHTML = response.ok ? await response.text() : "<p>Aperçu indisponible.</p>";
    textarea.hidden = true;
    preview.hidden = false;
  }

  // -- Boutons -------------------------------------------------------------------

  const actions = {
    "page-link"() {
      pageSearch.value = "";
      pageLabel.value = selectedText().trim();
      pageActive = 0;
      refreshPageList();
      pageDialog.showModal();
      pageSearch.focus();
    },
    "web-link"() {
      const text = selectedText().trim();
      const isUrl = /^(https?:\/\/|www\.)/i.test(text);
      webUrl.value = isUrl ? text : "";
      webLabel.value = isUrl ? "" : text;
      webDialog.showModal();
      webUrl.focus();
    },
    bold: () => wrap("**", "**", "texte en gras"),
    italic: () => wrap("*", "*", "texte en italique"),
    highlight: () => wrap("==", "==", "texte surligné"),
    heading: () => prefixLines("## "),
    list: () => prefixLines("- "),
    task: () => prefixLines("- [ ] "),
    callout: () => insertBlock(`> [!note] ${selectedText().trim() || "Titre"}\n> Texte de l'encadré`),
    preview: togglePreview,
  };

  document.querySelectorAll(".toolbar [data-action]").forEach((button) => {
    button.addEventListener("click", () => {
      const action = button.dataset.action;
      if (action !== "preview" && !preview.hidden) togglePreview();
      actions[action]();
    });
  });

  // -- Enregistrement ------------------------------------------------------------

  form.addEventListener("submit", () => {
    submitting = true;
  });
  window.addEventListener("beforeunload", (e) => {
    if (dirty && !submitting) e.preventDefault();
  });
})();
