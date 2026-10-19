// Module Langues côté navigateur : cartes de vocabulaire (4 notes FSRS),
// réponses à taper (correction par le serveur, différences surlignées),
// QCM/QCR de grammaire et remise en ordre de mots.
// Un exercice raté revient 4 positions plus loin (2 nouvelles tentatives au
// plus) ; seule la 1re tentative est enregistrée, en quittant l'exercice (la
// touche F peut entre-temps la passer en « Facile »).
(function () {
  const root = document.getElementById("quiz-langue");
  const stage = document.getElementById("quiz-stage");
  const dataTag = document.getElementById("quiz-data");
  if (!root || !stage || !dataTag) return;

  const exercices = JSON.parse(dataTag.textContent);
  const corrigerUrl = root.dataset.corrigerUrl;
  const recordUrl = root.dataset.recordUrl;
  const backUrl = root.dataset.backUrl;
  const csrf = root.dataset.csrf;
  const progressText = document.getElementById("quiz-progress");
  const barFill = document.getElementById("quiz-bar-fill");
  const aide = document.getElementById("quiz-aide");

  const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const A_REVOIR = 1, DIFFICILE = 2, BIEN = 3, FACILE = 4;
  const NOTES = [[A_REVOIR, "À revoir"], [DIFFICILE, "Difficile"], [BIEN, "Bien"], [FACILE, "Facile"]];

  // File de la session : une entrée par passage (les réessais sont des copies).
  const file = exercices.map((e, i) => ({ i, tentative: 0, nouveau: e.nouveau, melange: (e.melange || []).slice() }));
  let index = 0, score = 0, premiers = 0;
  let s = null; // état de l'exercice courant

  // -- LaTeX : rendu des $...$ (déjà transformés en spans .math par le serveur) --
  const CDN = "https://cdn.jsdelivr.net/npm/";
  let katexReady = null;

  function loadScript(src, integrity) {
    return new Promise((res, rej) => {
      const el = document.createElement("script");
      el.src = src; el.integrity = integrity; el.crossOrigin = "anonymous";
      el.onload = res; el.onerror = rej;
      document.head.appendChild(el);
    });
  }

  function renderMath(container) {
    const spans = container.querySelectorAll(".math");
    if (!spans.length) return;
    if (!katexReady) {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = CDN + "katex@0.16.47/dist/katex.min.css";
      link.integrity = "sha384-nH0MfJ44wi1dd7w6jinlyBgljjS8EJAh2JBoRad8a3VDw2K69vfaaqm4WnR+gXtA";
      link.crossOrigin = "anonymous";
      document.head.appendChild(link);
      katexReady = loadScript(CDN + "katex@0.16.47/dist/katex.min.js", "sha384-CwjPRVHTvLiMBFjEoij+QZViMV5rhTOIp7CJzl24JEqpRDA1sJFHVXXLURktbYYp");
    }
    katexReady.then(() => {
      spans.forEach((el) => {
        if (el.dataset.done) return;
        const block = el.classList.contains("math-block");
        const tex = el.textContent.trim().replace(/^\\[\[(]|\\[\])]$/g, "");
        try { window.katex.render(tex, el, { displayMode: block, throwOnError: false }); } catch (e) {}
        el.dataset.done = "1";
      });
    });
  }

  function el(tag, cls, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  function text(tag, cls, t) {
    const e = el(tag, cls);
    e.textContent = t;
    return e;
  }

  function shuffle(n) {
    const m = [...Array(n).keys()];
    for (let essai = 0; essai < 10; essai++) {
      for (let i = n - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [m[i], m[j]] = [m[j], m[i]];
      }
      if (m.some((x, i) => x !== i)) break;
    }
    return m;
  }

  async function post(url, body) {
    const r = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
      body: JSON.stringify(body),
    });
    if (!r.ok) throw new Error(r.status);
    return r.json();
  }

  function current() { return file[index]; }
  function exo() { return exercices[current().i]; }

  function updateHeader() {
    progressText.textContent = `Exercice ${index + 1} / ${file.length} · score ${score} / ${premiers}`;
    barFill.style.width = (index / file.length * 100) + "%";
  }

  function setAide() {
    const e = exo();
    let t;
    if (s.verdict) t = s.verdict.verdict === "juste" ? "Entrée Suivant · F C'était trop facile · Q Quitter" : "Entrée / Espace Suivant · Q Quitter";
    else if (e.forme === "carte") t = s.revele ? "1 À revoir · 2 Difficile · 3 Bien (Espace) · 4 Facile" : "Espace Retourner la carte · Q Quitter";
    else if (e.forme === "saisie") t = "Tape ta réponse · Entrée Valider · Échap Quitter";
    else if (e.forme === "choix") t = (e.multiple ? "Lettres : cocher plusieurs réponses" : "Lettre : choisir") + " · Entrée Valider · Q Quitter";
    else t = "Clique les mots (ou tape leur numéro) · ⌫ Retirer le dernier · Entrée Valider · Q Quitter";
    if (aide) aide.textContent = t;
  }

  // -- Construction d'un exercice --
  function build() {
    const e = exo(), c = current();
    s = { revele: false, verdict: null, note: null, enregistre: false, selection: [], places: [], envoi: false };
    stage.replaceChildren();
    updateHeader();

    const label = el("p", "quiz-set-label muted");
    label.appendChild(document.createTextNode(e.etiquette));
    if (c.nouveau) label.appendChild(text("span", "quiz-badge", "nouveau"));
    if (c.tentative) label.appendChild(text("span", "quiz-badge retry", "nouvelle tentative"));
    stage.appendChild(label);

    const zone = el("div");
    stage.appendChild(zone);
    s.feedback = el("div", "quiz-feedback");
    s.actions = el("div", "quiz-actions-row");
    s.nextBtn = el("button", "button primary", "Suivant →");
    s.nextBtn.type = "button";
    s.nextBtn.style.display = "none";
    s.nextBtn.addEventListener("click", suivante);

    if (e.forme === "carte") buildCarte(e, zone);
    else if (e.forme === "saisie") buildSaisie(e, zone);
    else if (e.forme === "choix") buildChoix(e, zone);
    else buildOrdre(e, c, zone);

    s.actions.appendChild(s.nextBtn);
    stage.appendChild(s.actions);
    stage.appendChild(s.feedback);
    renderMath(stage);
    setAide();
  }

  function buildCarte(e, zone) {
    zone.appendChild(el("div", "quiz-recto markdown", e.recto));
    const flip = el("button", "button primary", "Retourner la carte (Espace)");
    flip.type = "button";
    flip.addEventListener("click", reveler);
    s.actions.appendChild(flip);
    s.flip = flip;
  }

  function reveler() {
    const e = exo();
    if (s.revele) return;
    s.revele = true;
    s.flip.remove();
    const verso = el("div", "quiz-verso markdown", e.verso);
    stage.insertBefore(verso, s.actions);
    stage.insertBefore(details(e), s.actions);
    const notes = el("div", "quiz-notes");
    for (const [n, libelle] of NOTES) {
      const b = el("button", "button note-" + n);
      b.type = "button";
      b.appendChild(text("span", "", n + " · " + libelle));
      b.appendChild(text("small", "", (e.previsions || {})[n] || ""));
      b.addEventListener("click", () => noter(n));
      notes.appendChild(b);
    }
    stage.insertBefore(text("p", "muted", "Tu t'en souvenais ?"), s.actions);
    stage.insertBefore(notes, s.actions);
    renderMath(stage);
    setAide();
  }

  function noter(n) {
    if (!s.revele || s.note) return;
    s.note = n;
    compter(n);
    suivante();
  }

  function buildSaisie(e, zone) {
    zone.appendChild(el("div", "quiz-enonce markdown", e.consigne));
    const row = el("div", "quiz-saisie-row");
    if (e.invite) row.appendChild(text("span", "quiz-invite", e.invite + " →"));
    const input = el("input", "quiz-input");
    input.type = "text";
    input.autocomplete = "off";
    input.autocapitalize = "off";
    input.spellcheck = false;
    input.placeholder = e.prerempli ? "Phrase corrigée…" : "Ta réponse…";
    input.value = e.prerempli || "";
    input.addEventListener("keydown", (ev) => {
      if (ev.key === "Enter") { ev.preventDefault(); ev.stopPropagation(); valider(); }
      else if (ev.key === "Escape") { ev.preventDefault(); ev.stopPropagation(); quitter(); }
    });
    row.appendChild(input);
    zone.appendChild(row);
    s.input = input;
    if ((e.caracteres || []).length) {
      const spec = el("div", "quiz-speciaux");
      for (const ch of e.caracteres) {
        const b = text("button", "button small", ch);
        b.type = "button";
        b.addEventListener("click", () => {
          if (input.disabled) return;
          const a = input.selectionStart ?? input.value.length, z = input.selectionEnd ?? a;
          input.setRangeText(ch, a, z, "end");
          input.focus();
        });
        spec.appendChild(b);
      }
      zone.appendChild(spec);
      s.speciaux = spec;
    }
    const v = el("button", "button primary", "Valider");
    v.type = "button";
    v.addEventListener("click", valider);
    s.actions.appendChild(v);
    s.validateBtn = v;
    setTimeout(() => { input.focus(); input.setSelectionRange(input.value.length, input.value.length); }, 0);
  }

  function buildChoix(e, zone) {
    zone.appendChild(el("div", "quiz-enonce markdown", e.enonce));
    const list = el("div", "quiz-choices");
    s.choiceEls = e.choix.map((html, i) => {
      const b = el("button", "quiz-choice");
      b.type = "button";
      b.appendChild(el("span", "quiz-letter", LETTERS[i] + "."));
      b.appendChild(el("span", "quiz-choice-text markdown", html));
      b.addEventListener("click", () => basculer(i));
      list.appendChild(b);
      return b;
    });
    zone.appendChild(list);
    const v = el("button", "button primary", "Valider");
    v.type = "button";
    v.addEventListener("click", valider);
    s.actions.appendChild(v);
    s.validateBtn = v;
  }

  function basculer(i) {
    const e = exo();
    if (s.verdict || s.envoi) return;
    if (!e.multiple) s.selection = [i];
    else {
      const at = s.selection.indexOf(i);
      if (at >= 0) s.selection.splice(at, 1); else s.selection.push(i);
    }
    s.choiceEls.forEach((b, j) => b.classList.toggle("selected", s.selection.includes(j)));
  }

  function buildOrdre(e, c, zone) {
    zone.appendChild(el("div", "quiz-enonce markdown", e.consigne));
    s.zoneOrdre = el("div", "quiz-ordre-zone");
    s.zoneMots = el("div", "quiz-ordre-mots");
    zone.appendChild(s.zoneOrdre);
    zone.appendChild(s.zoneMots);
    s.tuiles = c.melange.map((m, pos) => {
      const b = el("button", "quiz-mot");
      b.type = "button";
      b.appendChild(text("small", "", String(pos + 1)));
      b.appendChild(document.createTextNode(e.mots[m]));
      b.addEventListener("click", () => placer(pos));
      s.zoneMots.appendChild(b);
      return b;
    });
    const v = el("button", "button primary", "Valider");
    v.type = "button";
    v.addEventListener("click", valider);
    s.actions.appendChild(v);
    s.validateBtn = v;
  }

  function placer(pos) {
    const m = current().melange[pos];
    if (s.verdict || s.envoi || s.places.includes(m)) return;
    s.places.push(m);
    majOrdre();
  }

  function retirer(k) {
    if (s.verdict || s.envoi || k < 0 || k >= s.places.length) return;
    s.places.splice(k, 1);
    majOrdre();
  }

  function majOrdre() {
    const e = exo();
    s.zoneOrdre.replaceChildren();
    s.places.forEach((m, k) => {
      const b = text("button", "quiz-mot", e.mots[m]);
      b.type = "button";
      b.title = "Retirer";
      b.addEventListener("click", () => retirer(k));
      s.zoneOrdre.appendChild(b);
    });
    current().melange.forEach((m, pos) => { s.tuiles[pos].disabled = s.places.includes(m); });
  }

  function details(e) {
    const d = el("div", "quiz-details");
    for (const html of e.details || []) d.appendChild(el("p", "", "ⓘ " + html));
    return d;
  }

  function compter(note) {
    if (current().tentative) return;
    premiers++;
    if (note !== A_REVOIR) score++;
    updateHeader();
  }

  // -- Correction (par le serveur) --
  async function valider() {
    const e = exo();
    if (s.verdict || s.envoi) return;
    let reponse;
    if (e.forme === "saisie") {
      reponse = s.input.value.trim();
      if (!reponse) return;
    } else if (e.forme === "choix") {
      if (!s.selection.length) return;
      reponse = s.selection.slice();
    } else if (e.forme === "ordre") {
      if (s.places.length !== e.mots.length) return;
      reponse = s.places.slice();
    } else return;
    s.envoi = true;
    if (s.validateBtn) s.validateBtn.disabled = true;
    let v;
    try {
      v = await post(corrigerUrl, { set_id: e.set_id, exo_id: e.exo_id, reponse });
    } catch (err) {
      s.envoi = false;
      if (s.validateBtn) s.validateBtn.disabled = false;
      s.feedback.replaceChildren(text("p", "quiz-verdict ko", "Correction impossible (connexion ?) — réessaie."));
      return;
    }
    s.envoi = false;
    s.verdict = v;
    s.note = v.note;
    compter(v.note);
    afficherCorrection(e, v);
  }

  function afficherCorrection(e, v) {
    const classe = v.verdict === "juste" ? "ok" : v.verdict === "faux" ? "ko" : "close";
    if (s.validateBtn) s.validateBtn.remove();
    const fb = s.feedback;
    fb.replaceChildren(text("div", "quiz-verdict " + classe, v.message));

    if (e.forme === "saisie") {
      s.input.disabled = true;
      s.input.classList.add(classe === "ok" ? "is-correct" : classe === "ko" ? "is-wrong" : "is-close");
      if (s.speciaux) s.speciaux.remove();
      if (v.verdict !== "juste") {
        const p = el("p", "quiz-attendu");
        p.appendChild(document.createTextNode("Réponse attendue : "));
        let span = null, etat = null;
        for (const [ch, ok] of v.diff) {
          if (ok !== etat) { span = el("span", ok ? "ok" : "ko"); p.appendChild(span); etat = ok; }
          span.textContent += ch;
        }
        if (!v.diff.length) p.appendChild(text("b", "", v.attendu));
        fb.appendChild(p);
        if (v.autres.length) fb.appendChild(el("p", "muted", "Aussi accepté : " + v.autres.join(" / ")));
      }
      if (e.tableau) fb.appendChild(tableau(e.tableau));
    } else if (e.forme === "choix") {
      const bonnes = new Set(v.reponses);
      s.choiceEls.forEach((b, i) => {
        b.disabled = true;
        if (bonnes.has(i)) b.classList.add("is-correct");
        else if (s.selection.includes(i)) b.classList.add("is-wrong");
      });
    } else if (e.forme === "ordre") {
      s.tuiles.forEach((b) => { b.disabled = true; });
      s.zoneOrdre.querySelectorAll("button").forEach((b) => { b.disabled = true; });
      if (v.verdict !== "juste") {
        fb.appendChild(text("p", "", "Ta phrase : " + v.saisie));
        const p = el("p", "quiz-attendu");
        p.appendChild(document.createTextNode("Réponse : "));
        p.appendChild(text("span", "ok", v.attendu));
        fb.appendChild(p);
      }
    }
    fb.appendChild(details(e));
    renderMath(fb);
    s.nextBtn.style.display = "";
    s.nextBtn.focus();
    setAide();
  }

  function tableau(t) {
    const table = el("table", "quiz-tableau");
    table.appendChild(text("caption", "", t.titre));
    const tbody = el("tbody");
    t.lignes.forEach(([personne, forme], k) => {
      const tr = el("tr", k === t.surligne ? "surligne" : "");
      tr.appendChild(text("td", "", personne));
      tr.appendChild(text("td", "", forme));
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    return table;
  }

  function facile() {
    if (!s.verdict || s.verdict.verdict !== "juste" || s.note === FACILE) return;
    s.note = FACILE;
    s.feedback.appendChild(text("p", "quiz-facile", "Noté « trop facile » : il reviendra plus tard."));
  }

  // -- Enregistrement en quittant l'exercice --
  function enregistrer() {
    if (!s.note || s.enregistre) return;
    s.enregistre = true;
    const c = current(), e = exo();
    if (!c.tentative) {
      post(recordUrl, { set_id: e.set_id, exo_id: e.exo_id, note: s.note })
        .catch(() => { /* enregistrement au mieux ; l'échec n'interrompt pas la session */ });
    }
  }

  // Après un échec, l'exercice revient 4 positions plus loin (2 fois au plus).
  function reprogrammer() {
    const c = current();
    if (c.tentative >= 2) return;
    const copie = { i: c.i, tentative: c.tentative + 1, nouveau: false, melange: c.melange.length ? shuffle(c.melange.length) : [] };
    file.splice(Math.min(index + 4, file.length), 0, copie);
  }

  function suivante() {
    if (!s.note) return;
    const echec = s.note === A_REVOIR && !s.enregistre;
    enregistrer();
    if (echec) reprogrammer();
    index++;
    if (index < file.length) build(); else resultats();
  }

  function quitter() {
    if (!confirm("Quitter la session ? Les réponses déjà données sont enregistrées.")) return;
    enregistrer();
    window.location.href = backUrl;
  }

  function resultats() {
    stage.replaceChildren();
    s = null;
    if (aide) aide.textContent = "";
    barFill.style.width = "100%";
    progressText.textContent = "Terminé";
    const pct = premiers ? Math.round(score / premiers * 100) : 0;
    const box = el("div", "quiz-results");
    box.appendChild(text("div", "quiz-score", score + " / " + premiers));
    box.appendChild(el("div", "mastery", '<div class="mastery-fill" style="width:' + pct + '%"></div>'));
    const msg = pct >= 80 ? "Excellent 🎉" : pct >= 50 ? "Bien, continue !" : "À retravailler 💪";
    box.appendChild(text("p", "muted", msg + " (premiers essais) — la progression a été enregistrée."));
    const actions = el("div", "quiz-actions");
    const back = text("a", "button primary", "Retour au menu");
    back.href = backUrl;
    actions.appendChild(back);
    box.appendChild(actions);
    stage.appendChild(box);
  }

  // -- Clavier --
  document.addEventListener("keydown", (ev) => {
    if (!s || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const e = exo();
    const key = ev.key;
    const k = key.toLowerCase();
    if (ev.target.tagName === "INPUT" && !ev.target.disabled) return; // saisie en cours
    if (ev.target.tagName === "BUTTON" && (key === "Enter" || key === " ") && !s.verdict && e.forme !== "carte") return;

    if (s.verdict) {
      if (key === "Enter" || key === " ") { ev.preventDefault(); suivante(); }
      else if (k === "f") { ev.preventDefault(); facile(); }
      else if (k === "q" || key === "Escape") { ev.preventDefault(); quitter(); }
      return;
    }
    if (k === "q" || key === "Escape") { ev.preventDefault(); quitter(); return; }
    if (e.forme === "carte") {
      if (!s.revele) { if (key === " " || key === "Enter") { ev.preventDefault(); reveler(); } return; }
      if ("1234".includes(key) && key.length === 1) { ev.preventDefault(); noter(Number(key)); }
      else if (key === " " || key === "Enter") { ev.preventDefault(); noter(BIEN); }
    } else if (e.forme === "choix") {
      const i = LETTERS.indexOf(key.toUpperCase());
      if (key.length === 1 && i >= 0 && i < e.choix.length) { ev.preventDefault(); basculer(i); }
      else if (key === "Enter" || key === " ") { ev.preventDefault(); valider(); }
    } else if (e.forme === "ordre") {
      if (key === "Enter") { ev.preventDefault(); valider(); }
      else if (key === "Backspace") { ev.preventDefault(); retirer(s.places.length - 1); }
      else if (/^[1-9]$/.test(key) && Number(key) <= e.mots.length) { ev.preventDefault(); placer(Number(key) - 1); }
    }
  });

  if (exercices.length) build();
})();
