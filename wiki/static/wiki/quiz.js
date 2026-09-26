// Moteur de quiz côté navigateur : QCM, QCR, texte à trous et flashcards.
// Feedback immédiat, navigation clavier, rendu LaTeX, enregistrement de la
// progression (Leitner) via une requête POST après chaque réponse.
(function () {
  const root = document.getElementById("quiz");
  const stage = document.getElementById("quiz-stage");
  const dataTag = document.getElementById("quiz-data");
  if (!root || !stage || !dataTag) return;

  const questions = JSON.parse(dataTag.textContent);
  const recordUrl = root.dataset.recordUrl;
  const backUrl = root.dataset.backUrl;
  const csrf = root.dataset.csrf;
  const progressText = document.getElementById("quiz-progress");
  const barFill = document.getElementById("quiz-bar-fill");

  const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let index = 0;
  let score = 0;
  const state = { selection: [], answered: false, known: null };

  // -- LaTeX : rendu des $...$ (déjà transformés en spans .math par le serveur) --
  const CDN = "https://cdn.jsdelivr.net/npm/";
  let katexReady = null;

  function loadScript(src) {
    return new Promise((res, rej) => {
      const s = document.createElement("script");
      s.src = src; s.onload = res; s.onerror = rej;
      document.head.appendChild(s);
    });
  }

  function renderMath(container) {
    const spans = container.querySelectorAll(".math");
    if (!spans.length) return;
    if (!katexReady) {
      const link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = CDN + "katex@0.16/dist/katex.min.css";
      document.head.appendChild(link);
      katexReady = loadScript(CDN + "katex@0.16/dist/katex.min.js");
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

  // -- Comparaison souple pour les TROU (casse, accents, espaces ignorés) --
  function normalize(s) {
    return s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase().trim().replace(/\s+/g, " ");
  }

  function updateHeader() {
    progressText.textContent = `Question ${index + 1} / ${questions.length} · score ${score}`;
    barFill.style.width = (index / questions.length * 100) + "%";
  }

  function el(tag, cls, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  async function record(q, correct) {
    try {
      await fetch(recordUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
        body: JSON.stringify({ set_id: q.set_id, question_id: q.id, correct: correct }),
      });
    } catch (e) { /* progression enregistrée au mieux ; l'échec n'interrompt pas la session */ }
  }

  // -- Rendu d'une question --
  function build() {
    stage.replaceChildren();
    const q = questions[index];
    state.selection = [];
    state.answered = false;
    state.known = null;
    updateHeader();

    stage.appendChild(el("p", "quiz-set-label muted", q.set_titre + " · " + q.type));
    const enonce = el("div", "quiz-enonce markdown", q.enonce);
    stage.appendChild(enonce);

    const feedback = el("div", "quiz-feedback");
    const actions = el("div", "quiz-actions-row");
    const nextBtn = el("button", "button primary", index + 1 < questions.length ? "Suivant →" : "Voir le score");
    nextBtn.style.display = "none";
    nextBtn.addEventListener("click", next);

    let choiceEls = [];
    let input = null;

    if (q.type === "QCM" || q.type === "QCR") {
      const list = el("div", "quiz-choices");
      q.choix.forEach((choix, i) => {
        const c = el("button", "quiz-choice");
        c.type = "button";
        c.appendChild(el("span", "quiz-letter", LETTERS[i] + "."));
        c.appendChild(el("span", "quiz-choice-text markdown", choix));
        c.addEventListener("click", () => toggle(i));
        list.appendChild(c);
        choiceEls.push(c);
      });
      stage.appendChild(list);
      const validate = el("button", "button primary", "Valider");
      validate.addEventListener("click", submitChoices);
      actions.appendChild(validate);
      state._validateBtn = validate;
    } else if (q.type === "TROU") {
      input = el("input", "quiz-input");
      input.type = "text";
      input.placeholder = "Votre réponse…";
      input.autofocus = true;
      stage.appendChild(input);
      const validate = el("button", "button primary", "Valider");
      validate.addEventListener("click", submitTrou);
      actions.appendChild(validate);
      state._validateBtn = validate;
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); submitTrou(); } });
      setTimeout(() => input.focus(), 0);
    } else if (q.type === "FLASHCARD") {
      const verso = el("div", "quiz-verso markdown", q.verso);
      verso.style.display = "none";
      stage.appendChild(verso);
      const flip = el("button", "button primary", "Retourner la carte (Espace)");
      flip.addEventListener("click", () => revealCard(verso, flip));
      actions.appendChild(flip);
      state._flip = () => revealCard(verso, flip);
    }

    stage.appendChild(actions);
    stage.appendChild(feedback);
    actions.appendChild(nextBtn);
    state._els = { q, feedback, nextBtn, choiceEls, input, actions };
    renderMath(stage);

    function toggle(i) {
      if (state.answered) return;
      if (q.type === "QCM") state.selection = [i];
      else {
        const at = state.selection.indexOf(i);
        if (at >= 0) state.selection.splice(at, 1); else state.selection.push(i);
      }
      choiceEls.forEach((c, j) => c.classList.toggle("selected", state.selection.includes(j)));
    }
    state._toggle = toggle;
  }

  function showFeedback(correct, explicationHtml) {
    const { feedback, nextBtn } = state._els;
    feedback.innerHTML =
      '<div class="quiz-verdict ' + (correct ? "ok" : "ko") + '">' +
      (correct ? "✓ Correct" : "✗ Incorrect") + "</div>" +
      (explicationHtml ? '<div class="quiz-explication markdown">' + explicationHtml + "</div>" : "");
    renderMath(feedback);
    nextBtn.style.display = "";
    nextBtn.focus();
    if (correct) score++;
    updateHeader();
  }

  function submitChoices() {
    const { q, choiceEls } = state._els;
    if (state.answered || !state.selection.length) return;
    state.answered = true;
    if (state._validateBtn) state._validateBtn.disabled = true;
    const correctSet = new Set(q.reponses);
    const chosen = new Set(state.selection);
    const correct = chosen.size === correctSet.size && [...chosen].every((i) => correctSet.has(i));
    choiceEls.forEach((c, i) => {
      c.disabled = true;
      if (correctSet.has(i)) c.classList.add("is-correct");
      else if (chosen.has(i)) c.classList.add("is-wrong");
    });
    showFeedback(correct, q.explication);
    record(q, correct);
  }

  function submitTrou() {
    const { q, input } = state._els;
    if (state.answered || !input.value.trim()) return;
    state.answered = true;
    if (state._validateBtn) state._validateBtn.disabled = true;
    input.disabled = true;
    const correct = q.reponses_texte.some((r) => normalize(r) === normalize(input.value));
    input.classList.add(correct ? "is-correct" : "is-wrong");
    let exp = q.explication;
    if (!correct) {
      exp = '<p>Réponse attendue : <b>' + q.reponses_texte.map(escapeHtml).join(" / ") + "</b></p>" + exp;
    }
    showFeedback(correct, exp);
    record(q, correct);
  }

  function revealCard(verso, flip) {
    const { q } = state._els;
    if (state.answered) return;
    state.answered = true;
    verso.style.display = "";
    flip.style.display = "none";
    renderMath(verso);
    // Auto-évaluation : boutons « je savais » / « à revoir ».
    const self = el("div", "quiz-selfeval");
    const knew = el("button", "button primary", "Je savais (C)");
    const missed = el("button", "button", "À revoir (I)");
    knew.addEventListener("click", () => gradeCard(true));
    missed.addEventListener("click", () => gradeCard(false));
    self.appendChild(knew);
    self.appendChild(missed);
    state._els.actions.insertBefore(self, state._els.nextBtn);
    state._selfeval = self;
    if (q.explication) {
      const exp = el("div", "quiz-explication markdown", q.explication);
      verso.after(exp);
      renderMath(exp);
    }
  }

  function gradeCard(known) {
    const { q, nextBtn } = state._els;
    if (state._selfeval) state._selfeval.remove();
    if (known) score++;
    updateHeader();
    nextBtn.style.display = "";
    nextBtn.focus();
    record(q, known);
  }

  function next() {
    index++;
    if (index < questions.length) build();
    else results();
  }

  function results() {
    stage.replaceChildren();
    barFill.style.width = "100%";
    progressText.textContent = "Terminé";
    const pct = questions.length ? Math.round(score / questions.length * 100) : 0;
    const box = el("div", "quiz-results");
    box.appendChild(el("div", "quiz-score", score + " / " + questions.length));
    box.appendChild(el("div", "mastery", '<div class="mastery-fill" style="width:' + pct + '%"></div>'));
    const msg = pct >= 80 ? "Excellent 🎉" : pct >= 50 ? "Bien, continuez !" : "À retravailler 💪";
    box.appendChild(el("p", "muted", msg + " La progression a été enregistrée."));
    const actions = el("div", "quiz-actions");
    const again = el("a", "button primary", "Retour aux sets");
    again.href = backUrl;
    actions.appendChild(again);
    box.appendChild(actions);
    stage.appendChild(box);
  }

  function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  // -- Clavier --
  document.addEventListener("keydown", (e) => {
    if (!questions.length || index >= questions.length) return;
    const q = questions[index];
    if (e.target.tagName === "INPUT") return; // laisser taper dans les TROU
    const key = e.key.toLowerCase();

    if (state.answered) {
      if (q.type === "FLASHCARD" && state._selfeval) {
        if (key === "c") { e.preventDefault(); gradeCard(true); return; }
        if (key === "i") { e.preventDefault(); gradeCard(false); return; }
      }
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); if (state._els.nextBtn.style.display !== "none") next(); }
      return;
    }

    if (q.type === "FLASHCARD") {
      if (e.key === " ") { e.preventDefault(); if (state._flip) state._flip(); }
      return;
    }
    if (q.type === "QCM" || q.type === "QCR") {
      const i = LETTERS.indexOf(e.key.toUpperCase());
      if (i >= 0 && i < q.choix.length) { e.preventDefault(); state._toggle(i); return; }
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); submitChoices(); }
    }
  });

  if (questions.length) build();
})();
