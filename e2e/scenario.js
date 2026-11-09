// Scénario de bout en bout dans un vrai navigateur (Playwright, Chromium) : le wiki
// tourne sur le coffre e2e/vault avec le compte admin « testeur » (voir
// .github/workflows/tests.yml). Chaque vérification ratée est listée à la fin et
// fait échouer le script ; une capture d'écran est prise à chaque échec.
//
// En local :
//   cp -r e2e/vault /tmp/vault && mkdir -p /tmp/data
//   E2E_VAULT=/tmp/vault DJANGO_DATA_DIR=/tmp/data DJANGO_SETTINGS_MODULE=settings_e2e PYTHONPATH=e2e \
//     uv run python manage.py migrate && (créer le compte testeur) && uv run python manage.py runserver 127.0.0.1:8765
//   node e2e/scenario.js /tmp
const { chromium } = require("playwright");

const DOSSIER = process.argv[2] || ".";
const BASE = process.env.E2E_BASE || "http://127.0.0.1:8765";
const COMPTE = { nom: "testeur", mot_de_passe: "Test-pass-1234!" };
const PAQUET = "QCM/Voc/anglais";
const SET = "QCM/Test/signal";

const echecs = [];
let page;
async function verifier(nom, condition, detail) {
  if (condition) { console.log("  ✓", nom); return; }
  echecs.push(nom + (detail ? " — " + detail : ""));
  console.log("  ✗", nom, detail || "");
  try { await page.screenshot({ path: `${DOSSIER}/echec-${echecs.length}.png` }); } catch (e) { /* page fermée */ }
}
const texte = async (sel) => ((await page.textContent(sel)) || "").replace(/\s+/g, " ").trim();

(async () => {
  const navigateur = await chromium.launch();
  const contexte = await navigateur.newContext({ viewport: { width: 1100, height: 900 }, locale: "fr-FR" });
  page = await contexte.newPage();
  const erreursPage = [];
  page.on("pageerror", (e) => erreursPage.push(e.message));

  console.log("Connexion");
  await page.goto(BASE + "/connexion/");
  await page.fill("input[name=username]", COMPTE.nom);
  await page.fill("input[name=password]", COMPTE.mot_de_passe);
  await Promise.all([page.waitForNavigation(), page.click("form button[type=submit]")]);
  await verifier("page d'accueil après connexion", (await texte("h1")).includes("Accueil"), await texte("h1"));

  console.log("Lecture, thème, palette");
  await page.goto(BASE + "/wiki/Cours/Signal");
  await verifier("page de cours rendue", (await page.content()).includes("Shannon"));
  await verifier("callout rendu", await page.$(".callout") !== null);
  await verifier("panneau « Réviser ce cours » avec le QCM de la page", (await page.content()).includes("Signal — QCM"));
  await page.goto(BASE + "/sommaire/");
  const avant = await page.getAttribute("html", "data-theme");
  await page.click("[data-theme-toggle]");
  const apres = await page.getAttribute("html", "data-theme");
  await verifier("bascule du thème", avant !== apres && ["light", "dark"].includes(apres), `${avant} → ${apres}`);
  await page.keyboard.press("Control+k");
  await page.waitForTimeout(300);
  const palette = await page.$(".palette-aide, [data-palette-ouverte], dialog[open]");
  await verifier("palette ouverte avec Ctrl+K", palette !== null && (await palette.isVisible()));
  await page.keyboard.press("Escape");

  console.log("QCM : session, signalement");
  await page.goto(BASE + `/qcm/jouer/?set=${encodeURIComponent(SET)}&mode=all`);
  await page.waitForSelector(".quiz-stage .quiz-choice, .quiz-stage .quiz-input, .quiz-stage button");
  // Trois questions dans un ordre aléatoire : on répond à chacune selon sa forme.
  let signale = false;
  for (let i = 0; i < 3; i++) {
    if (await page.$(".quiz-stage .quiz-choice")) {
      await page.click(".quiz-stage .quiz-choice >> nth=1");
      await page.click(".quiz-stage button:has-text('Valider')");
    } else if (await page.$(".quiz-stage .quiz-input")) {
      await page.fill(".quiz-stage .quiz-input", "Nyquist");
      await page.keyboard.press("Enter");
    } else {
      await page.keyboard.press(" ");
      await page.waitForTimeout(100);
      await page.keyboard.press("3");
    }
    await page.waitForTimeout(150);
    if (!signale && (await page.$(".quiz-signaler"))) {
      page.once("dialog", (d) => d.accept("Énoncé ambigu (test e2e)"));
      await page.click(".quiz-signaler");
      await page.waitForFunction(() => /Signalée/.test(document.querySelector(".quiz-signaler")?.textContent || ""));
      signale = true;
    }
    // Bouton « Suivant → » (« Voir le score » pour la dernière question).
    for (const b of await page.$$(".quiz-stage button")) {
      if ((await b.isVisible()) && /Suivant|score|Terminer/i.test(await b.innerText())) { await b.click(); break; }
    }
    await page.waitForTimeout(150);
  }
  await verifier("fin de session affichée", (await texte(".quiz-progress-text")) === "Terminé", await texte(".quiz-progress-text"));
  await verifier("question signalée depuis le quiz", signale);
  await page.goto(BASE + "/qcm/signalements/");
  await verifier("signalement listé pour l'admin", (await page.content()).includes("Énoncé ambigu (test e2e)"));
  page.once("dialog", (d) => d.accept());
  await Promise.all([page.waitForNavigation(), page.click(".signalement-actions button[value=retirer]")]);
  await verifier("question retirée du set", (await page.content()).includes("Question retirée du set"));
  const exportation = await page.request.get(BASE + `/qcm/exporter/?set=${encodeURIComponent(SET)}`);
  await verifier("export Anki (.apkg)", exportation.status() === 200 && /\.apkg/.test(exportation.headers()["content-disposition"] || ""));
  const tsv = await page.request.get(BASE + `/qcm/exporter/?set=${encodeURIComponent(SET)}&format=tsv`);
  await verifier("export texte tabulé", (await tsv.text()).split("\n").filter(Boolean).length === 2);

  console.log("Éditeur");
  page.on("dialog", (d) => d.accept()); // « quitter sans enregistrer ? » pendant le rechargement
  const doc = () => page.evaluate(() => window.CM.EditorView.findFromDOM(document.querySelector(".editor-cm .cm-editor")).state.doc.toString());
  await page.goto(BASE + "/modifier/Cours/Signal");
  await page.waitForSelector(".editor-cm .cm-content");
  await verifier("barre d'outils : annuler, menus, côte à côte, aide",
    !!(await page.$("[data-action=undo]")) && !!(await page.$("[data-menu=inserer]")) && !!(await page.$("[data-mode=split]")) && !!(await page.$("[data-action=aide]")));
  await page.click(".editor-cm .cm-content");
  await page.keyboard.press("Control+End");
  await page.keyboard.type("\n\nTexte ajouté e2e");
  await page.waitForTimeout(1200); // brouillon gardé sur l'appareil
  await page.reload();
  await page.waitForSelector(".editor-cm .cm-content");
  await verifier("brouillon non enregistré retrouvé", await page.isVisible("[data-brouillon-notice]"));
  await page.click("[data-brouillon=reprendre]");
  await verifier("brouillon repris", (await doc()).includes("Texte ajouté e2e"));
  await page.click("[data-mode=split]");
  await page.waitForFunction(() => /Texte ajouté e2e/.test(document.querySelector(".preview")?.textContent || ""));
  await verifier("côte à côte : rendu à jour", await page.isVisible(".preview"));
  await page.click("[data-menu=encadre] summary");
  await page.click("[data-callout=definition]");
  await verifier("encadré « définition » inséré", (await doc()).includes("> [!definition] Titre"));
  await page.click("[data-action=undo]");
  await verifier("annuler depuis la barre", !(await doc()).includes("[!definition] Titre"));
  await page.click("[data-action=aide]");
  await verifier("aide ouverte", await page.$eval("#aide-dialog", (d) => d.open));
  await page.keyboard.press("Escape");
  // Enregistrement (Ctrl+S) : la version précédente part dans l'historique.
  await page.click(".editor-cm .cm-content");
  await page.keyboard.press("Control+s");
  await page.waitForFunction(() => /Enregistré/.test(document.querySelector("[data-state]")?.textContent || ""));
  await page.goto(BASE + "/historique/Cours/Signal");
  await verifier("historique : une version et le texte ajouté en différence",
    (await page.$$(".historique-versions li")).length === 1 && (await page.content()).includes("diff-ajout"));
  await Promise.all([page.waitForNavigation(), page.click("button[value=restaurer]")]);
  await verifier("version restaurée", !(await page.content()).includes("Texte ajouté e2e") && (await page.content()).includes("Version restaurée"));
  await page.evaluate(() => localStorage.removeItem("wiki-brouillon:Cours/Signal"));

  console.log("Hors ligne : lecture du wiki");
  const sw = await page.evaluate(async () => { const r = await navigator.serviceWorker.ready; return r.active ? r.active.state : ""; });
  await verifier("service worker du wiki actif", sw === "activated", sw);
  await page.goto(BASE + "/wiki/Cours/Signal");
  await page.waitForTimeout(400);
  await contexte.setOffline(true);
  await page.goto(BASE + "/wiki/Cours/Signal");
  await verifier("page lue disponible sans réseau", (await page.content()).includes("Shannon"));
  await page.goto(BASE + "/wiki/Accueil");
  await verifier("page jamais lue : page « hors connexion »", (await texte("h1")).includes("Pas de connexion"), await texte("h1"));
  await contexte.setOffline(false);

  console.log("Hors ligne : paquet de langue");
  await page.goto(BASE + "/qcm/hors-ligne/");
  await page.waitForSelector("#hl-liste fieldset", { state: "attached" });
  await page.click("#hl-catalogue summary");
  await page.check(`#hl-liste input[value="${PAQUET}"]`);
  await page.click("#hl-telecharger");
  await page.waitForSelector(".quiz-langues");
  await verifier("paquet de langue téléchargé", (await texte(".quiz-langues summary")).includes("3 nouveaux"), await texte(".quiz-langues summary"));
  await contexte.setOffline(true);
  const requetes = [];
  page.on("request", (r) => { if (r.url().startsWith(BASE)) requetes.push(r.url()); });
  await page.click('.quiz-langues a[href^="#langue?mode=quotidien"]');
  await page.waitForSelector("#quiz-langue:not([hidden]) .quiz-stage .quiz-set-label");
  for (let i = 0; i < 3; i++) {
    await page.keyboard.press(" ");
    await page.waitForTimeout(100);
    await page.keyboard.press("3");
    await page.waitForTimeout(150);
  }
  await verifier("session de langue sans aucune requête réseau", requetes.length === 0, requetes.join(", "));
  await verifier("session de langue terminée", (await texte("#quiz-langue .quiz-progress-text")) === "Terminé", await texte("#quiz-langue .quiz-progress-text"));
  await contexte.setOffline(false);
  await page.click("#quiz-langue .quiz-topbar a");
  await page.waitForSelector("#hl-accueil:not([hidden])");
  // Au retour du réseau, la synchronisation part toute seule ; le bouton la relance au besoin.
  await page.click("#hl-synchroniser");
  await page.waitForFunction(() => /synchronisées|tout est synchronisé/.test(document.getElementById("hl-etat").textContent));
  const serveur = await (await page.request.get(BASE + `/qcm/hors-ligne/sets/?id=${encodeURIComponent(PAQUET)}`)).json();
  await verifier("révisions hors ligne reçues par le serveur", Object.keys(serveur.sets[0].progression).length === 3, JSON.stringify(Object.keys(serveur.sets[0].progression)));
  const rappel = await (await page.request.get(BASE + "/api/rappel/")).json();
  await verifier("série d'activité démarrée", rappel.serie === 1 && rappel.aujourdhui > 0, JSON.stringify(rappel));

  await verifier("aucune erreur JavaScript", erreursPage.length === 0, erreursPage.join(" | "));
  await navigateur.close();
  if (echecs.length) {
    console.log(`\n${echecs.length} vérification(s) en échec :\n- ` + echecs.join("\n- "));
    process.exit(1);
  }
  console.log("\nScénario complet : tout est passé.");
})().catch((e) => { console.error(e); process.exit(1); });
