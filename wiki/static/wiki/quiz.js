// Moteur de quiz côté navigateur : QCM, QCR, texte à trous, réponse courte
// (QRC, ex. traduction ou synonyme) et flashcards.
// Feedback immédiat, navigation clavier, rendu LaTeX, enregistrement de la
// progression (Leitner) via une requête POST après chaque réponse.
// Mode « intensif » : les questions ratées reviennent plus loin dans la session
// jusqu'à être réussies 2 fois de suite ; seule la 1re réponse est enregistrée.
(function () {
  const root = document.getElementById("quiz");
  const stage = document.getElementById("quiz-stage");
  const dataTag = document.getElementById("quiz-data");
  if (!root || !stage || !dataTag) return;

  const questions = JSON.parse(dataTag.textContent);
  const recordUrl = root.dataset.recordUrl;
  const backUrl = root.dataset.backUrl;
  const csrf = root.dataset.csrf;
  const intensif = root.dataset.mode === "intensif";
  const progressText = document.getElementById("quiz-progress");
  const barFill = document.getElementById("quiz-bar-fill");

  const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  // File des questions à poser (indices dans `questions`) ; en mode intensif,
  // une question ratée y est réinsérée un peu plus loin.
  const queue = questions.map((_, i) => i);
  const track = questions.map(() => ({ attempts: 0, misses: 0, streak: 0 }));
  const REUSSITES_REQUISES = 2; // réussites consécutives exigées après une erreur
  let pos = 0;
  let score = 0;
  let mastered = 0;
  const state = { selection: [], answered: false, known: null, shownAt: 0 };

  // -- LaTeX : rendu des $...$ (déjà transformés en spans .math par le serveur) --
  const CDN = "https://cdn.jsdelivr.net/npm/";
  let katexReady = null;

  function loadScript(src, integrity) {
    return new Promise((res, rej) => {
      const s = document.createElement("script");
      s.src = src; s.integrity = integrity; s.crossOrigin = "anonymous";
      s.onload = res; s.onerror = rej;
      document.head.appendChild(s);
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

  // -- Comparaison souple pour les TROU/QRC (casse, accents, espaces, apostrophes
  // typographiques et ponctuation finale ignorés) — même règle que normaliser_reponse --
  function normalize(s) {
    return s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase()
      .replace(/[\u2018\u2019]/g, "'").trim().replace(/[.!?;:\s]+$/, "").replace(/\s+/g, " ");
  }

  function current() {
    return questions[queue[pos]];
  }

  function updateHeader() {
    if (intensif) {
      const reste = queue.length - pos - (state.answered ? 1 : 0);
      progressText.textContent = `Maîtrisées ${mastered} / ${questions.length} · ${reste} passage${reste > 1 ? "s" : ""} restant${reste > 1 ? "s" : ""}`;
      barFill.style.width = (mastered / questions.length * 100) + "%";
      return;
    }
    progressText.textContent = `Question ${pos + 1} / ${questions.length} · score ${score}`;
    barFill.style.width = (pos / questions.length * 100) + "%";
  }

  function shuffle(list) {
    for (let i = list.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [list[i], list[j]] = [list[j], list[i]];
    }
    return list;
  }

  // Une réponse vient d'être donnée : score, enregistrement, et en mode
  // intensif, remise en file de la question tant qu'elle n'est pas sue.
  function answered(q, correct) {
    const t = track[queue[pos]];
    t.attempts++;
    // Seule la 1re réponse compte pour le score et la révision espacée : les
    // répétitions de la session ne doivent pas gonfler les boîtes de Leitner.
    if (t.attempts === 1) {
      if (correct) score++;
      record(q, correct, Math.round(performance.now() - state.shownAt));
    }
    if (intensif) {
      if (correct) t.streak++;
      else { t.streak = 0; t.misses++; }
      const done = correct && (t.misses === 0 || t.streak >= REUSSITES_REQUISES);
      if (done) mastered++;
      else {
        // Ratée : revient vite ; réussie une fois après erreur : revient plus tard.
        const gap = correct ? 6 : 3;
        const at = pos + 1 + Math.min(gap, queue.length - pos - 1);
        queue.splice(at, 0, queue[pos]);
      }
    }
    if (pos + 1 >= queue.length) state._els.nextBtn.textContent = "Voir le score";
    updateHeader();
  }

  function el(tag, cls, html) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html !== undefined) e.innerHTML = html;
    return e;
  }

  async function record(q, correct, dureeMs) {
    try {
      await fetch(recordUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
        body: JSON.stringify({ set_id: q.set_id, question_id: q.id, correct: correct, duree_ms: dureeMs }),
      });
    } catch (e) { /* progression enregistrée au mieux ; l'échec n'interrompt pas la session */ }
  }

  // -- Rendu d'une question --
  function build() {
    stage.replaceChildren();
    const q = current();
    const t = track[queue[pos]];
    state.selection = [];
    state.answered = false;
    state.known = null;
    state.shownAt = performance.now();
    updateHeader();

    const label = q.set_titre + " · " + q.type + (t.attempts ? " · à revoir (passage " + (t.attempts + 1) + ")" : "");
    stage.appendChild(el("p", "quiz-set-label muted", label));
    if (q.consigne) {
      const consigne = el("p", "quiz-consigne");
      consigne.textContent = q.consigne;
      stage.appendChild(consigne);
    }
    const enonce = el("div", "quiz-enonce markdown", q.enonce);
    stage.appendChild(enonce);

    const feedback = el("div", "quiz-feedback");
    const actions = el("div", "quiz-actions-row");
    const nextBtn = el("button", "button primary", "Suivant →");
    nextBtn.style.display = "none";
    nextBtn.addEventListener("click", next);

    let choiceEls = [];
    let input = null;

    if (q.type === "QCM" || q.type === "QCR") {
      const list = el("div", "quiz-choices");
      // Au 2e passage d'une question, on mélange les choix pour ne pas
      // retenir une position plutôt qu'une réponse.
      const order = q.choix.map((_, i) => i);
      if (intensif && t.attempts) shuffle(order);
      state._order = order;
      choiceEls = new Array(q.choix.length);
      order.forEach((i, k) => {
        const c = el("button", "quiz-choice");
        c.type = "button";
        c.appendChild(el("span", "quiz-letter", LETTERS[k] + "."));
        c.appendChild(el("span", "quiz-choice-text markdown", q.choix[i]));
        c.addEventListener("click", () => toggle(i));
        list.appendChild(c);
        choiceEls[i] = c;
      });
      stage.appendChild(list);
      const validate = el("button", "button primary", "Valider");
      validate.addEventListener("click", submitChoices);
      actions.appendChild(validate);
      state._validateBtn = validate;
    } else if (q.type === "TROU" || q.type === "QRC") {
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
    answered(q, correct);
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
    } else if (q.type === "QRC") {
      // Synonymes / traductions : montrer les autres réponses acceptées.
      const autres = q.reponses_texte.filter((r) => normalize(r) !== normalize(input.value));
      if (autres.length) exp = '<p>Autres réponses acceptées : ' + autres.map(escapeHtml).join(" / ") + "</p>" + exp;
    }
    showFeedback(correct, exp);
    answered(q, correct);
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
    state._selfeval = null;
    nextBtn.style.display = "";
    nextBtn.focus();
    answered(q, known);
  }

  function next() {
    pos++;
    if (pos < queue.length) build();
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
    if (intensif) {
      box.querySelector(".quiz-score").textContent = "Tout est su ✓";
      box.appendChild(el("p", "",
        "Du premier coup : <b>" + score + " / " + questions.length + "</b> · " +
        "<b>" + queue.length + "</b> réponses au total pour tout maîtriser."));
      const hardest = questions
        .map((q, i) => ({ q, misses: track[i].misses }))
        .filter((h) => h.misses)
        .sort((a, b) => b.misses - a.misses)
        .slice(0, 10);
      if (hardest.length) {
        const wrap = el("div", "quiz-hardest");
        wrap.appendChild(el("p", "", "<b>Les plus difficiles</b> — elles reviendront dans la Révision intelligente :"));
        const ul = el("ul");
        hardest.forEach((h) => {
          const text = el("div", "", h.q.enonce).textContent.trim();
          const li = el("li");
          li.textContent = (text.length > 90 ? text.slice(0, 90) + "…" : text) + " — " + h.misses + " erreur" + (h.misses > 1 ? "s" : "");
          ul.appendChild(li);
        });
        wrap.appendChild(ul);
        box.appendChild(wrap);
      }
      box.appendChild(el("p", "muted", "Refaites une Révision intelligente demain pour ancrer ce que vous avez appris."));
    }
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
    if (!questions.length || pos >= queue.length) return;
    const q = current();
    if (e.target.tagName === "INPUT") return; // laisser taper dans les TROU/QRC
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
      const k = LETTERS.indexOf(e.key.toUpperCase());
      if (k >= 0 && k < q.choix.length) { e.preventDefault(); state._toggle(state._order[k]); return; }
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); submitChoices(); }
    }
  });

  if (questions.length) build();
})();
