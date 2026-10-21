// QCM hors ligne : sets téléchargés sur l'appareil, révision sans connexion et
// synchronisation avec le serveur quand la connexion revient.
//
// La progression (boîtes de Leitner) est recalculée sur l'appareil avec les
// mêmes règles que quiz.py, pour savoir quelles questions sont à réviser sans
// le serveur. Le serveur reste la référence : à chaque synchronisation, les
// réponses en attente lui sont envoyées puis la progression est re-téléchargée.
(function () {
  const A = window.QcmAttente;
  const app = document.getElementById("hl");
  if (!app || !A) return;
  const $ = (id) => document.getElementById(id);

  // --- Révision espacée : mêmes règles que quiz.py ---
  const INTERVALLES_JOURS = [0, 1, 3, 7, 14, 30];
  const BOITE_MAX = 5;
  const NOTES = ["a_revoir", "difficile", "bien", "facile"];
  const JOUR_MS = 86400000;

  function nouvelleBoite(boite, note) {
    if (note === "a_revoir") return 0;
    if (note === "difficile") return Math.max(1, boite);
    return Math.min(BOITE_MAX, boite + (note === "facile" ? 2 : 1));
  }

  function estDue(st, now) {
    if (!st || !st.last_review) return true;
    return now >= Date.parse(st.last_review) + INTERVALLES_JOURS[Math.min(st.box, BOITE_MAX)] * JOUR_MS;
  }

  function jour(d) {
    const x = new Date(d);
    return x.getFullYear() + "-" + (x.getMonth() + 1) + "-" + x.getDate();
  }

  // Applique une réponse à la progression locale d'un set (comme QuizProgress.record).
  function appliquer(set, rep) {
    const st = set.progression[rep.question_id] || { box: 0, seen: 0, correct: 0, last_review: null, premiere_revue: null };
    if (st.last_review && Date.parse(rep.date) <= Date.parse(st.last_review)) return;
    const note = NOTES.includes(rep.note) ? rep.note : (rep.correct ? "bien" : "a_revoir");
    st.seen++;
    if (note !== "a_revoir") st.correct++;
    st.box = nouvelleBoite(st.box, note);
    st.last_review = rep.date;
    if (!st.premiere_revue) st.premiere_revue = rep.date;
    set.progression[rep.question_id] = st;
  }

  // Questions à réviser aujourd'hui (comme _file_du_jour) : réapprentissage,
  // révisions (boîtes basses, puis plus anciennes), nouvelles ; avec les quotas.
  function fileDuJour(set, now) {
    const aujourdhui = jour(now);
    const reapprendre = [], vues = [], nouvelles = [];
    for (const q of set.questions) {
      const st = set.progression[q.id];
      if (!st) nouvelles.push(q);
      else if (estDue(st, now)) {
        if (st.last_review && jour(st.last_review) === aujourdhui) reapprendre.push(q);
        else vues.push(q);
      }
    }
    const cle = (q) => set.progression[q.id];
    vues.sort((a, b) => (cle(a).box - cle(b).box) || (Date.parse(cle(a).last_review || 0) - Date.parse(cle(b).last_review || 0)));
    let dejaN = 0, dejaR = 0;
    for (const st of Object.values(set.progression)) {
      if (st.premiere_revue && jour(st.premiere_revue) === aujourdhui) dejaN++;
      else if (st.last_review && jour(st.last_review) === aujourdhui) dejaR++;
    }
    const { nouvelles_jour: qn, revisions_jour: qr } = set.quotas || {};
    const r = qr == null ? vues : vues.slice(0, Math.max(0, qr - dejaR));
    const n = qn == null ? nouvelles : nouvelles.slice(0, Math.max(0, qn - dejaN));
    return reapprendre.concat(r, n);
  }

  // --- État ---
  const etat = { sets: new Map(), meta: {}, catalogue: null, attente: 0 };

  async function charger() {
    etat.sets = new Map((await A.tous("sets")).map((s) => [s.id, s]));
    etat.meta = (await A.lire("meta", "meta")) || {};
    etat.attente = (await A.tous("attente")).length;
  }

  const sauverMeta = () => A.ecrire("meta", etat.meta, "meta");

  // --- Affichage ---
  function el(tag, cls, texte) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (texte !== undefined) e.textContent = texte;
    return e;
  }

  function lien(texte, href, cls) {
    const a = el("a", "button small" + (cls ? " " + cls : ""), texte);
    a.href = href;
    return a;
  }

  const pluriel = (n, mot) => n + " " + mot + (n > 1 ? "s" : "");

  function afficherReseau() {
    const enLigne = navigator.onLine;
    $("hl-reseau").textContent = enLigne ? "● En ligne" : "○ Hors ligne";
    $("hl-reseau").classList.toggle("hors-ligne", !enLigne);
    document.querySelectorAll("[data-en-ligne]").forEach((e) => { e.hidden = !enLigne; });
    $("hl-synchroniser").disabled = !enLigne;
  }

  function afficherEtat(message) {
    const parts = [pluriel(etat.sets.size, "set") + " sur l'appareil"];
    parts.push(etat.attente ? pluriel(etat.attente, "réponse") + " à synchroniser" : "tout est synchronisé");
    if (etat.meta.derniereSynchro) {
      parts.push("dernière synchro " + new Date(etat.meta.derniereSynchro).toLocaleString("fr-FR", { dateStyle: "short", timeStyle: "short" }));
    }
    $("hl-etat").textContent = message || parts.join(" · ");
  }

  function alerte(texte, lienConnexion) {
    const zone = $("hl-alerte");
    zone.hidden = !texte;
    const titre = $("hl-alerte-texte");
    titre.textContent = texte || "";
    if (lienConnexion) {
      titre.append(" ");
      const a = el("a", "", "Se reconnecter");
      a.href = app.dataset.loginUrl;
      titre.append(a);
    }
  }

  function parCategorie(sets) {
    const cats = new Map();
    for (const s of sets) {
      const nom = s.langue ? s.langue + " · " + s.categorie : s.categorie;
      if (!cats.has(nom)) cats.set(nom, []);
      cats.get(nom).push(s);
    }
    return [...cats.entries()].sort((a, b) => a[0].localeCompare(b[0], "fr"));
  }

  function afficherTelecharges() {
    const zone = $("hl-telecharges");
    zone.replaceChildren();
    const now = Date.now();
    if (!etat.sets.size) {
      zone.append(el("p", "muted", "Aucun set sur cet appareil : ouvrez « Télécharger des sets » ci-dessous (connexion nécessaire)."));
      return;
    }
    let total = 0;
    const sections = [];
    for (const [nom, sets] of parCategorie(etat.sets.values())) {
      const details = el("details", "quiz-category");
      details.open = true;
      const summary = el("summary");
      const ul = el("ul", "quiz-sets");
      let dues = 0;
      for (const s of sets.sort((a, b) => a.titre.localeCompare(b.titre, "fr"))) {
        const n = fileDuJour(s, now).length;
        dues += n;
        const li = el("li", "quiz-set");
        const head = el("div", "quiz-set-head");
        head.append(el("span", "quiz-set-title", s.titre), el("span", "muted", s.questions.length + " q."));
        li.append(head);
        if (s.description) li.append(el("p", "quiz-set-desc muted", s.description));
        const vues = s.questions.filter((q) => s.progression[q.id]).length;
        li.append(el("p", "quiz-set-desc muted", pluriel(n, "question") + " à réviser · " + vues + " / " + s.questions.length + " rencontrées"));
        const boutons = el("div", "quiz-set-buttons");
        const id = encodeURIComponent(s.id);
        boutons.append(
          lien("Réviser (" + n + ")", "#jouer?mode=review&set=" + id, "primary"),
          lien("Tout", "#jouer?mode=all&set=" + id),
          lien("Intensif", "#jouer?mode=intensif&set=" + id),
        );
        const retirer = el("button", "button small", "Retirer");
        retirer.type = "button";
        retirer.addEventListener("click", () => retirerSet(s));
        boutons.append(retirer);
        li.append(boutons);
        ul.append(li);
      }
      total += dues;
      summary.append(el("span", "quiz-category-name", nom), el("span", "muted quiz-category-meta", pluriel(dues, "question") + " à réviser"));
      details.append(summary, ul);
      sections.push(details);
    }
    const actions = el("div", "quiz-actions");
    actions.append(lien("Révision intelligente (" + total + ")", "#jouer?revision=1", "primary"));
    zone.append(actions, ...sections);
  }

  function afficherCatalogue() {
    const liste = $("hl-liste");
    liste.replaceChildren();
    if (!etat.catalogue) {
      $("hl-catalogue-meta").textContent = navigator.onLine ? "" : "connexion nécessaire";
      liste.append(el("p", "muted", navigator.onLine ? "Chargement de la liste…" : "La liste des sets s'affiche quand l'appareil est connecté."));
      return;
    }
    $("hl-catalogue-meta").textContent = pluriel(etat.catalogue.length, "set");
    for (const [nom, sets] of parCategorie(etat.catalogue)) {
      const bloc = el("fieldset", "hl-categorie");
      const legende = el("legend");
      const toutes = el("input");
      toutes.type = "checkbox";
      legende.append(el("label", "", ""));
      legende.firstChild.append(toutes, " " + nom);
      bloc.append(legende);
      const cases = [];
      for (const s of sets) {
        const label = el("label", "hl-choix");
        const c = el("input");
        c.type = "checkbox";
        c.value = s.id;
        c.checked = etat.sets.has(s.id);
        cases.push(c);
        label.append(c, " " + s.titre + " ", el("span", "muted", "(" + s.total + ")"));
        bloc.append(label);
      }
      toutes.checked = cases.every((c) => c.checked);
      toutes.addEventListener("change", () => cases.forEach((c) => { c.checked = toutes.checked; }));
      liste.append(bloc);
    }
  }

  function afficherAccueil(message) {
    if (window.QuizMoteur) window.QuizMoteur.arreter();
    $("quiz").hidden = true;
    $("hl-accueil").hidden = false;
    afficherReseau();
    afficherEtat(message);
    afficherTelecharges();
    afficherCatalogue();
  }

  // --- Sessions de révision ---
  function melanger(liste) {
    for (let i = liste.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [liste[i], liste[j]] = [liste[j], liste[i]];
    }
    return liste;
  }

  function construireSession(params) {
    const now = Date.now();
    if (params.get("revision")) {
      // Comme la révision intelligente du serveur : dues d'abord, boîtes basses, plus anciennes.
      const paires = [];
      for (const s of etat.sets.values()) {
        for (const q of fileDuJour(s, now)) {
          const st = s.progression[q.id];
          paires.push({ q, prio: st ? [estDue(st, now) ? 0 : 1, st.box, Date.parse(st.last_review || 0)] : [0, -1, 0] });
        }
      }
      paires.sort((a, b) => a.prio[0] - b.prio[0] || a.prio[1] - b.prio[1] || a.prio[2] - b.prio[2]);
      return { titre: "Révision intelligente", questions: paires.map((p) => p.q), intensif: false };
    }
    const set = etat.sets.get(params.get("set"));
    if (!set) return null;
    const mode = params.get("mode");
    const questions = mode === "review" ? fileDuJour(set, now) : set.questions.slice();
    return { titre: set.titre, questions: melanger(questions), intensif: mode === "intensif" };
  }

  async function enregistrer(q, correct, note, dureeMs) {
    const rep = await A.ajouter({ set_id: q.set_id, question_id: q.id, correct, note: note || null, duree_ms: dureeMs, joueur: etat.meta.joueur || "" });
    const set = etat.sets.get(q.set_id);
    if (set) {
      appliquer(set, rep);
      await A.ecrire("sets", set);
    }
    etat.attente++;
    if (navigator.onLine) envoyerDiscretement();
  }

  function lancer(params) {
    const session = construireSession(params);
    if (!session) { location.hash = ""; return; }
    $("hl-accueil").hidden = true;
    $("quiz").hidden = false;
    $("hl-intensif-info").hidden = !(session.intensif && session.questions.length);
    document.title = session.titre + " · QCM hors ligne";
    const stage = $("quiz-stage");
    if (!session.questions.length) {
      $("quiz-progress").textContent = "";
      stage.replaceChildren(el("p", "", "Rien à réviser ici 🎉 Toutes les questions sont à jour."));
      stage.append(lien("Retour aux sets", "#", "primary"));
      return;
    }
    window.QuizMoteur.demarrer({
      stage,
      questions: session.questions,
      intensif: session.intensif,
      backUrl: "#",
      messageFin: "Réponses gardées sur l'appareil, envoyées au serveur à la prochaine connexion.",
      enregistrer,
    });
  }

  function router() {
    const hash = location.hash;
    if (hash.startsWith("#jouer?")) lancer(new URLSearchParams(hash.slice(7)));
    else {
      document.title = "QCM hors ligne · ProjetPluri";
      afficherAccueil();
    }
  }

  // --- Synchronisation ---
  let envoiPrevu = null;
  function envoyerDiscretement() {
    clearTimeout(envoiPrevu);
    envoiPrevu = setTimeout(async () => {
      try {
        await A.envoyer();
        etat.attente = (await A.tous("attente")).length;
      } catch (e) { /* nouvel essai à la prochaine synchronisation */ }
    }, 1500);
  }

  async function lireJson(r) {
    if (r.redirected || !(r.headers.get("Content-Type") || "").includes("json")) throw new A.Deconnecte("Session expirée");
    if (!r.ok) throw new Error("Serveur indisponible (" + r.status + ")");
    return r.json();
  }

  // Télécharge des sets (questions, progression du serveur, quotas) ; les réponses
  // encore en attente sont ré-appliquées par-dessus la progression reçue.
  async function telecharger(ids) {
    const attente = await A.tous("attente");
    const retires = [];
    for (let i = 0; i < ids.length; i += 40) {
      const params = new URLSearchParams();
      ids.slice(i, i + 40).forEach((id) => params.append("id", id));
      const data = await lireJson(await fetch(app.dataset.setsUrl + "?" + params, { credentials: "same-origin", cache: "no-store" }));
      for (const set of data.sets) {
        attente.filter((r) => r.set_id === set.id && (!r.joueur || r.joueur === data.joueur))
          .sort((a, b) => Date.parse(a.date) - Date.parse(b.date))
          .forEach((r) => appliquer(set, r));
        set.telecharge = new Date().toISOString();
        await A.ecrire("sets", set);
        etat.sets.set(set.id, set);
        mettreImagesEnCache(set);
      }
      for (const id of data.manquants) {
        const set = etat.sets.get(id);
        if (set) retires.push(set.titre);
        await A.effacer("sets", id);
        etat.sets.delete(id);
      }
    }
    return retires;
  }

  // Images des questions (servies par le wiki) gardées dans le cache du service worker.
  async function mettreImagesEnCache(set) {
    if (!window.caches) return;
    const html = set.questions.map((q) => [q.enonce, q.verso, q.explication, ...q.choix].join("")).join("");
    const doc = new DOMParser().parseFromString(html, "text/html");
    const urls = new Set();
    doc.querySelectorAll("img[src]").forEach((img) => {
      const url = new URL(img.getAttribute("src"), location.href);
      if (url.origin === location.origin) urls.add(url.href);
    });
    if (!urls.size) return;
    const cache = await caches.open(A.CACHE);
    for (const url of urls) {
      try { if (!(await cache.match(url))) await cache.add(url); } catch (e) { /* image indisponible */ }
    }
  }

  let synchroEnCours = false;
  async function synchroniser() {
    if (synchroEnCours || !navigator.onLine) return;
    synchroEnCours = true;
    afficherEtat("Synchronisation…");
    let message;
    try {
      // Si un autre compte s'est connecté, le re-téléchargement des sets plus bas
      // remplace la progression de l'appareil par la sienne.
      const cat = await A.catalogue();
      etat.meta.joueur = cat.joueur;
      etat.catalogue = cat.sets;
      const envoi = await A.envoyer(cat);
      const retires = etat.sets.size ? await telecharger([...etat.sets.keys()]) : [];
      etat.meta.derniereSynchro = new Date().toISOString();
      await sauverMeta();
      etat.attente = (await A.tous("attente")).length;
      alerte(retires.length ? "Retirés de l'appareil (supprimés du serveur) : " + retires.join(", ") : "");
      if (envoi.autres) alerte(pluriel(envoi.autres, "réponse") + " d'un autre compte en attente : elles seront envoyées quand ce compte se reconnectera.");
      if (envoi.envoyees) message = pluriel(envoi.envoyees, "réponse") + " synchronisée" + (envoi.envoyees > 1 ? "s" : "") + ".";
    } catch (e) {
      if (e instanceof A.Deconnecte) alerte("Session expirée : vos réponses restent sur l'appareil.", true);
      else alerte("Synchronisation impossible : " + e.message + ". Vos réponses restent sur l'appareil.");
    } finally {
      synchroEnCours = false;
    }
    if ($("quiz").hidden) afficherAccueil(message);
    if (message) setTimeout(() => { if ($("quiz").hidden) afficherEtat(); }, 4000);
  }

  async function telechargerSelection() {
    const ids = [...$("hl-liste").querySelectorAll("input[value]:checked")].map((c) => c.value);
    if (!ids.length) { alerte("Cochez au moins un set."); return; }
    const bouton = $("hl-telecharger");
    bouton.disabled = true;
    afficherEtat("Téléchargement de " + pluriel(ids.length, "set") + "…");
    try {
      // Demande au navigateur de ne pas effacer les données en cas de manque de place.
      if (navigator.storage && navigator.storage.persist) navigator.storage.persist().catch(() => {});
      const cat = await A.catalogue();
      etat.meta.joueur = cat.joueur;
      await A.envoyer(cat);
      await telecharger(ids);
      etat.meta.derniereSynchro = new Date().toISOString();
      await sauverMeta();
      alerte("");
      $("hl-catalogue").open = false;
    } catch (e) {
      if (e instanceof A.Deconnecte) alerte("Session expirée.", true);
      else alerte("Téléchargement impossible : " + e.message);
    } finally {
      bouton.disabled = false;
    }
    afficherAccueil();
  }

  async function retirerSet(set) {
    if (!confirm("Retirer « " + set.titre + " » de cet appareil ? Les réponses non synchronisées sont gardées.")) return;
    await A.effacer("sets", set.id);
    etat.sets.delete(set.id);
    afficherAccueil();
  }

  // --- Démarrage ---
  $("hl-synchroniser").addEventListener("click", synchroniser);
  $("hl-telecharger").addEventListener("click", telechargerSelection);
  $("hl-tout-cocher").addEventListener("click", () => {
    $("hl-liste").querySelectorAll("input[type=checkbox]").forEach((c) => { c.checked = true; });
  });
  window.addEventListener("hashchange", router);
  window.addEventListener("online", () => { afficherReseau(); synchroniser(); });
  window.addEventListener("offline", afficherReseau);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible" && navigator.onLine && etat.attente) synchroniser();
  });

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register(app.dataset.swUrl, { scope: app.dataset.scope }).catch(() => {
      alerte("Mode hors ligne indisponible : ce navigateur refuse le service worker (HTTPS requis).");
    });
  }

  charger().then(() => {
    router();
    synchroniser();
  }).catch((e) => alerte("Stockage indisponible sur ce navigateur : " + e.message));
})();
