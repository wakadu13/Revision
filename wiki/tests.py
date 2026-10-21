import tempfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from .vault import get_vault


class WikiTestCase(TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        override = override_settings(WIKI_DIR=self.root, WIKI_HOME="Accueil", SECURE_SSL_REDIRECT=False)
        override.enable()
        self.addCleanup(override.disable)
        # Site privé : les tests du wiki se font avec un compte utilisateur.
        self.reader = get_user_model().objects.create_user("lecteur", password="x")
        self.client.force_login(self.reader)

    def write(self, path, text):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")

    def html(self, key):
        vault = get_vault()
        return vault.render(vault.notes[key.lower()])[0]


class WikiTests(WikiTestCase):
    def test_new_md_file_creates_page(self):
        self.write("Accueil.md", "Bonjour")
        self.assertEqual(self.client.get("/wiki/Nouvelle").status_code, 404)
        self.write("Dossier/Nouvelle.md", "Contenu **neuf**")
        response = self.client.get("/wiki/Dossier/Nouvelle")
        self.assertContains(response, "<strong>neuf</strong>")
        self.assertRedirects(self.client.get("/wiki/Nouvelle"), "/wiki/Dossier/Nouvelle")
        self.assertContains(self.client.get("/"), "Bonjour")

    def test_wikilinks(self):
        self.write("A.md", "[[B]] [[B|texte]] [[B#Mon Titre]] [[Alias B]] [[Absente]] [[#Local]]")
        self.write("sous/B.md", "---\naliases: [Alias B]\n---\n## Mon Titre")
        html = self.html("A")
        self.assertIn('href="/wiki/sous/B">B</a>', html)
        self.assertIn('href="/wiki/sous/B">texte</a>', html)
        self.assertIn('href="/wiki/sous/B#mon-titre">B &gt; Mon Titre</a>', html)
        self.assertIn('href="/wiki/sous/B">Alias B</a>', html)
        self.assertIn('is-unresolved" href="/wiki/Absente"', html)
        self.assertIn('href="#local">Local</a>', html)
        vault = get_vault()
        self.assertEqual([n.name for n in vault.backlinks["sous/b"]], ["A"])
        self.assertEqual([n.name for n in vault.unresolved["absente"]], ["A"])

    def test_embeds(self):
        self.write("A.md", "![[img.png|200]]\n\n![[B#Section]]\n\n![[A]]")
        self.write("B.md", "# Intro\navant\n## Section\ndedans\n## Autre\napres")
        (self.root / "img.png").write_bytes(b"\x89PNG")
        html = self.html("A")
        self.assertIn('<img class="embed-image" src="/fichiers/img.png" alt="img" width="200"', html)
        self.assertIn("dedans", html)
        self.assertNotIn("avant", html)
        self.assertNotIn("apres", html)
        response = self.client.get("/fichiers/img.png")
        self.assertEqual(response.status_code, 200)
        response.close()

    def test_callouts_tags_comments_and_code(self):
        self.write("A.md", (
            "> [!warning]- Titre *replié*\n> contenu #tag/sous\n\n"
            "==surligné== %%secret%%\n\n"
            "```\n[[pas un lien]] #pas-un-tag\n```\n`#non`"
        ))
        html = self.html("A")
        self.assertIn('<details class="callout" data-callout="warning">', html)
        self.assertIn("<em>replié</em>", html)
        self.assertIn('<a class="tag" href="/tags/tag/sous">#tag/sous</a>', html)
        self.assertIn("<mark>surligné</mark>", html)
        self.assertNotIn("secret", html)
        self.assertIn("[[pas un lien]] #pas-un-tag", html)
        self.assertIn("<code>#non</code>", html)
        self.assertEqual([n.name for n in get_vault().notes_with_tag("tag")], ["A"])
        self.assertContains(self.client.get("/tags/tag/sous"), "A")

    def test_search(self):
        self.write("A.md", "Le mot girafe est ici.")
        self.write("B.md", "Rien.")
        results = self.client.get("/recherche/", {"q": "girafe"}).context["results"]
        self.assertEqual([note.name for note, _ in results], ["A"])


class EditorTests(WikiTestCase):
    def setUp(self):
        super().setUp()
        admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(admin)

    def test_create_page_from_browser(self):
        self.write("Accueil.md", "[[Planning]]")
        self.assertContains(self.client.get("/wiki/Planning"), "Créer cette page", status_code=404)
        self.assertContains(self.client.get("/modifier/Planning"), 'id="editor"')
        response = self.client.post("/modifier/Planning", {"content": "Voir [[Accueil]]\r\n", "version": ""})
        self.assertRedirects(response, "/wiki/Planning")
        self.assertEqual((self.root / "Planning.md").read_text(encoding="utf-8"), "Voir [[Accueil]]\n")
        self.assertContains(self.client.get("/wiki/Planning"), 'href="/wiki/Accueil"')
        self.assertEqual([n.name for n in get_vault().backlinks["accueil"]], ["Planning"])

    def test_edit_existing_page_and_conflict(self):
        self.write("Dossier/Note.md", "avant")
        response = self.client.get("/modifier/Note")
        self.assertRedirects(response, "/modifier/Dossier/Note")
        version = self.client.get("/modifier/Dossier/Note").context["version"]
        self.assertRedirects(
            self.client.post("/modifier/Dossier/Note", {"content": "après", "version": version}),
            "/wiki/Dossier/Note",
        )
        # Une version périmée ne doit pas écraser le fichier.
        response = self.client.post("/modifier/Dossier/Note", {"content": "écrasé", "version": "0"})
        self.assertContains(response, "modifiée ailleurs")
        self.assertEqual((self.root / "Dossier/Note.md").read_text(encoding="utf-8"), "après")

    def test_link_choices_and_preview(self):
        self.write("a/Même.md", "")
        self.write("b/Même.md", "")
        self.write("Unique.md", "")
        links = [c["link"] for c in self.client.get("/modifier/X").context["link_choices"]]
        self.assertEqual(links, ["a/Même", "b/Même", "Unique"])
        response = self.client.post("/apercu/X", {"content": "[[Unique]] **gras**"})
        self.assertContains(response, 'href="/wiki/Unique"')
        self.assertContains(response, "<strong>gras</strong>")

    def test_new_page_form(self):
        self.write("Dossier/Existante.md", "")
        self.assertRedirects(
            self.client.get("/nouvelle/", {"name": "Réunion", "folder": "Dossier"}),
            "/modifier/Dossier/R%C3%A9union", fetch_redirect_response=False,
        )
        self.assertContains(self.client.get("/nouvelle/", {"name": "Existante", "folder": "Dossier"}), "déjà")
        self.assertContains(self.client.get("/nouvelle/", {"name": "a/b"}), "caractères")

    def test_invalid_paths_rejected(self):
        for path in ["../hors", ".cache/x", "a:b"]:
            self.assertEqual(self.client.post(f"/modifier/{path}", {"content": "x", "version": ""}).status_code, 404)
        self.assertFalse((self.root.parent / "hors.md").exists())

    def test_anonymous_redirected_to_login(self):
        self.client.logout()
        response = self.client.post("/modifier/Planning", {"content": "x", "version": ""})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/connexion/", response["Location"])
        self.assertFalse((self.root / "Planning.md").exists())
        self.assertIn("/connexion/", self.client.post("/apercu/X", {"content": "x"})["Location"])

    def test_simple_user_cannot_edit(self):
        self.client.force_login(get_user_model().objects.create_user("bob", password="x"))
        self.assertEqual(self.client.post("/modifier/Planning", {"content": "x", "version": ""}).status_code, 403)
        self.assertEqual(self.client.get("/nouvelle/").status_code, 403)
        self.assertFalse((self.root / "Planning.md").exists())
        self.assertNotContains(self.client.get("/sommaire/"), "+ Nouvelle page")


class SommaireSearchTests(WikiTestCase):
    def test_search_ignores_accents_and_highlights(self):
        self.write("Reseaux/OSI.md", "Le modèle OSI découpe le réseau en couches.")
        self.write("Autre.md", "Rien à voir.")
        # « reseau » (sans accent) doit trouver « réseau ».
        results = self.client.get("/recherche/", {"q": "reseau"}).context["results"]
        self.assertEqual([n.name for n, _ in results], ["OSI"])
        snippet = results[0][1]
        self.assertIn("<mark>réseau</mark>", snippet)

    def test_search_matches_title_folder_and_multiple_words(self):
        self.write("Cours/Théorème de Shannon.md", "Contenu.")
        self.write("Cours/Filtrage.md", "On parle du théorème ici aussi.")
        results = self.client.get("/recherche/", {"q": "theoreme shannon"}).context["results"]
        # Les deux contiennent « théorème », mais le titre gagne.
        self.assertEqual([n.name for n, _ in results][0], "Théorème de Shannon")

    def test_search_html_is_escaped(self):
        self.write("XSS.md", "texte <script>alert(1)</script> reseau")
        snippet = self.client.get("/recherche/", {"q": "script"}).context["results"][0][1]
        self.assertNotIn("<script>", snippet)
        self.assertIn("&lt;", snippet)
        self.assertIn("<mark>script</mark>", snippet)

    def test_sommaire_lists_everything(self):
        self.write("A/1.md", "")
        self.write("A/B/2.md", "")
        self.write("Seule.md", "")
        response = self.client.get("/sommaire/")
        self.assertContains(response, "3 notes dans le wiki")
        self.assertContains(response, 'href="/wiki/A/B/2"')
        self.assertContains(response, 'href="/wiki/Seule"')
        root = response.context["root"]
        self.assertEqual(root["count"], 3)
        folder_a = next(f for f in root["folders"] if f["name"] == "A")
        self.assertEqual(folder_a["count"], 2)


class QuizTests(TestCase):
    def setUp(self):
        import json, tempfile
        from pathlib import Path
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        override = override_settings(WIKI_DIR=self.root, WIKI_HOME="Accueil", SECURE_SSL_REDIRECT=False)
        override.enable()
        self.addCleanup(override.disable)
        self.set = {
            "titre": "Set de test",
            "questions": [
                {"id": "q-qcm", "type": "QCM", "question": "2+2 ?", "choix": ["3", "4"], "reponses": [1]},
                {"id": "q-qcr", "type": "QCR", "question": "Pairs ?", "choix": ["2", "3", "4"], "reponses": [0, 2]},
                {"id": "q-trou", "type": "TROU", "question": "Capitale de la France ?", "reponses_texte": ["Paris"]},
                {"id": "q-flash", "type": "FLASHCARD", "question": "chat", "verso": "cat"},
            ],
        }
        (self.root / "reseaux").mkdir(parents=True)
        (self.root / "reseaux" / "test_set.json").write_text(json.dumps(self.set), encoding="utf-8")
        self.user = get_user_model().objects.create_user("alice", password="x")
        self.client.force_login(self.user)

    def test_library_loads_and_categorizes(self):
        from wiki.quiz import get_library
        lib = get_library()
        self.assertIn("reseaux/test_set", lib.sets)
        self.assertEqual(lib.get("reseaux/test_set").categorie, "reseaux")
        self.assertEqual(len(lib.get("reseaux/test_set")), 4)

    def test_non_quiz_json_ignored(self):
        import json
        (self.root / "canvas.json").write_text(json.dumps({"nodes": []}), encoding="utf-8")
        from wiki.quiz import get_library
        self.assertEqual(list(get_library().sets), ["reseaux/test_set"])

    def test_malformed_set_reported(self):
        (self.root / "bad.json").write_text('{"questions": [{"type": "QCM", "question": "x"}]}', encoding="utf-8")
        from wiki.quiz import get_library
        self.assertTrue(any("bad.json" in e for e in get_library().errors))

    def test_index_and_play_pages(self):
        self.assertContains(self.client.get("/qcm/"), "Set de test")
        response = self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=all")
        self.assertContains(response, "quiz-data")
        self.assertEqual(len(response.context["questions"]), 4)
        types = {q["type"] for q in response.context["questions"]}
        self.assertEqual(types, {"QCM", "QCR", "TROU", "FLASHCARD"})

    def _set_vocab(self):
        import json
        (self.root / "langues").mkdir()
        (self.root / "langues" / "vocab.json").write_text(json.dumps({"questions": [
            {"id": "q-qrc", "type": "QRC", "question": "chien", "consigne": "Traduire en anglais",
             "reponses_texte": ["dog", "hound"], "inverse": True, "consigne_inverse": "Traduire en français"},
        ]}), encoding="utf-8")

    def test_qrc_page(self):
        self._set_vocab()
        response = self.client.get("/qcm/jouer/?set=langues/vocab&mode=all")
        qs = {q["id"]: q for q in response.context["questions"]}
        self.assertEqual(set(qs), {"q-qrc", "q-qrc~inverse"})
        self.assertEqual(qs["q-qrc"]["type"], "QRC")
        self.assertEqual(qs["q-qrc"]["consigne"], "Traduire en anglais")

    def test_qrc_and_inverse(self):
        self._set_vocab()
        from wiki.quiz import get_library
        qs = {q.id: q for q in get_library().get("langues/vocab").questions}
        self.assertTrue(qs["q-qrc"].est_correcte_texte("  HOUND. "))
        self.assertFalse(qs["q-qrc"].est_correcte_texte("cat"))
        inverse = qs["q-qrc~inverse"]
        self.assertEqual((inverse.enonce, inverse.consigne), ("dog", "Traduire en français"))
        self.assertTrue(inverse.est_correcte_texte("Chien"))

    def test_normalisation_texte(self):
        from wiki.quiz import normaliser_reponse
        self.assertEqual(normaliser_reponse("  I don\u2019t   KNOW ! "), "i don't know")
        self.assertEqual(normaliser_reponse("-p-"), "-p-")
        self.assertEqual(normaliser_reponse("Été"), "ete")

    def test_qrc_sans_reponse_signale(self):
        import json
        (self.root / "bad.json").write_text(json.dumps({"questions": [{"type": "QRC", "question": "chat"}]}), encoding="utf-8")
        from wiki.quiz import get_library
        self.assertTrue(any("reponses_texte" in e for e in get_library().errors))

    def test_record_updates_leitner(self):
        from wiki.models import QuizProgress
        for correct in (True, True):
            r = self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "q-qcm", "correct": correct},
                                  content_type="application/json")
            self.assertEqual(r.status_code, 200)
        p = QuizProgress.objects.get(set_id="reseaux/test_set", question_id="q-qcm")
        self.assertEqual(p.box, 2)
        self.assertEqual(p.seen, 2)
        self.assertEqual(p.correct, 2)
        # Une mauvaise réponse renvoie en boîte 0 (question oubliée).
        self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "q-qcm", "correct": False},
                         content_type="application/json")
        p.refresh_from_db()
        self.assertEqual(p.box, 0)

    def test_flashcard_grades(self):
        from wiki import quiz
        from wiki.models import QuizProgress
        self.assertEqual([quiz.nouvelle_boite(3, n) for n in quiz.NOTES], [0, 3, 4, 5])
        self.assertEqual([quiz.nouvelle_boite(0, n) for n in quiz.NOTES], [0, 1, 1, 2])
        self.assertEqual(quiz.nouvelle_boite(5, quiz.FACILE), 5)

        def noter(note):
            self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "q-flash",
                                                    "correct": note != "a_revoir", "note": note},
                             content_type="application/json")
            return QuizProgress.objects.get(question_id="q-flash")

        self.assertEqual(noter("facile").box, 2)
        self.assertEqual(noter("difficile").box, 2)
        p = noter("a_revoir")
        self.assertEqual((p.box, p.seen, p.correct, p.last_correct), (0, 3, 2, False))
        # Note inconnue : on se rabat sur « correct ».
        self.assertEqual(noter("parfait").box, 1)

    def test_review_mode_only_due(self):
        from wiki.models import QuizProgress
        from django.utils import timezone
        # q-qcm en boîte 5, révisée à l'instant → pas due ; les autres jamais vues → dues.
        QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-qcm", box=5,
                                    last_review=timezone.now(), seen=1, correct=1)
        response = self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=review")
        ids = {q["id"] for q in response.context["questions"]}
        self.assertNotIn("q-qcm", ids)
        self.assertEqual(len(ids), 3)

    def test_intensive_mode(self):
        from wiki.models import QuizProgress
        from django.utils import timezone
        # Le mode intensif reprend toutes les questions, même celles déjà maîtrisées.
        QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-qcm", box=5,
                                    last_review=timezone.now(), seen=1, correct=1)
        response = self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=intensif")
        self.assertEqual(len(response.context["questions"]), 4)
        self.assertTrue(response.context["intensif"])
        self.assertContains(response, 'data-mode="intensif"')
        self.assertContains(response, "Révision intensive · Set de test")
        # Les autres modes restent « normaux ».
        self.assertContains(self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=all"), 'data-mode="normal"')
        self.assertContains(self.client.get("/qcm/"), "mode=intensif")

    def test_intensive_mode_by_category(self):
        import json
        other = {"titre": "Autre", "questions": [{"type": "FLASHCARD", "question": "Port HTTPS ?", "verso": "443"}]}
        (self.root / "reseaux" / "autre.json").write_text(json.dumps(other), encoding="utf-8")
        response = self.client.get("/qcm/jouer/", {"categorie": "reseaux", "mode": "intensif"})
        self.assertEqual(len(response.context["questions"]), 5)
        self.assertEqual({q["set_id"] for q in response.context["questions"]}, {"reseaux/test_set", "reseaux/autre"})
        self.assertEqual(self.client.get("/qcm/jouer/", {"categorie": "inconnue", "mode": "intensif"}).status_code, 404)

    def test_record_rejects_unknown_question(self):
        r = self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "nope", "correct": True},
                             content_type="application/json")
        self.assertEqual(r.status_code, 404)

    def test_reset(self):
        from wiki.models import QuizProgress
        QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-qcm", box=3)
        self.client.post("/qcm/reinitialiser/", {"set": "reseaux/test_set"})
        self.assertFalse(QuizProgress.objects.filter(set_id="reseaux/test_set").exists())

    def test_login_required_and_progress_per_user(self):
        from wiki.models import QuizProgress
        self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "q-qcm", "correct": True},
                         content_type="application/json")
        self.assertEqual(QuizProgress.objects.get().player, "alice")
        self.client.logout()
        self.assertIn("/connexion/", self.client.get("/qcm/")["Location"])
        r = self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "q-qcm", "correct": True},
                             content_type="application/json")
        self.assertIn("/connexion/", r["Location"])
        self.assertEqual(QuizProgress.objects.count(), 1)

    def test_index_search(self):
        import json
        other = {"titre": "Protocoles réseau", "questions": [{"type": "FLASHCARD", "question": "Port HTTPS ?", "verso": "443"}]}
        (self.root / "reseaux" / "protocoles.json").write_text(json.dumps(other), encoding="utf-8")
        from wiki.quiz import get_library
        qset = get_library().get("reseaux/protocoles")
        self.assertTrue(qset.correspond("RESEAU protocoles"))  # accents et casse ignorés
        self.assertTrue(qset.correspond("https"))              # texte des questions
        self.assertFalse(qset.correspond("capitale"))

        response = self.client.get("/qcm/", {"q": "capitale"})
        self.assertEqual(response.context["matches"], 1)
        shown = [e["set"].titre for c in response.context["categories"] for e in c["sets"] if e["match"]]
        self.assertEqual(shown, ["Set de test"])
        self.assertContains(response, 'class="quiz-set" data-search=', count=2)  # l'autre set reste, masqué
        self.assertContains(response, 'data-search="protocoles reseau reseaux port https ?" hidden>')  # masqué
        self.assertContains(response, "data-quiz-empty hidden>")
        self.assertContains(self.client.get("/qcm/", {"q": "introuvable"}), "Aucun QCM ne correspond")


    def test_daily_quotas(self):
        from datetime import timedelta
        from django.utils import timezone
        from wiki.models import QuizDeck, QuizProgress
        hier = timezone.now() - timedelta(days=2)
        # q-qcm et q-qcr déjà vues et dues ; q-trou et q-flash jamais vues.
        for qid in ("q-qcm", "q-qcr"):
            QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id=qid, box=1,
                                        last_review=hier, premiere_revue=hier, seen=1, correct=1)
        deck = QuizDeck.objects.create(player="alice", set_id="reseaux/test_set", nouvelles_jour=1)
        ids = [q["id"] for q in self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=review").context["questions"]]
        self.assertEqual(len(ids), 3)  # 2 révisions + 1 nouvelle
        self.assertTrue({"q-qcm", "q-qcr"} <= set(ids))
        deck.revisions_jour = 1
        deck.save()
        summary = self.client.get("/qcm/").context["categories"][0]["sets"][0]["summary"]
        self.assertEqual((summary["a_reviser"], summary["revisions"], summary["nouvelles"], summary["dues"]), (2, 1, 1, 4))
        # Le quota s'applique aussi à la révision intelligente, pas aux modes « Tout » et « Intensif ».
        self.assertEqual(len(self.client.get("/qcm/jouer/?revision=1").context["questions"]), 2)
        self.assertEqual(len(self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=all").context["questions"]), 4)

        # Une nouvelle découverte aujourd'hui consomme le quota de nouvelles.
        self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "q-trou", "correct": True},
                         content_type="application/json")
        summary = self.client.get("/qcm/").context["categories"][0]["sets"][0]["summary"]
        self.assertEqual((summary["revisions"], summary["nouvelles"]), (1, 0))
        # Une révision faite aujourd'hui consomme le quota de révisions.
        self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "q-qcm", "correct": True},
                         content_type="application/json")
        summary = self.client.get("/qcm/").context["categories"][0]["sets"][0]["summary"]
        self.assertEqual((summary["a_reviser"], summary["dues"]), (0, 2))
        self.assertTrue(summary["quota_atteint"])
        self.assertContains(self.client.get("/qcm/"), "quota du jour atteint")

    def test_relearning_outside_quota(self):
        from django.utils import timezone
        from wiki.models import QuizDeck, QuizProgress
        # Ratée aujourd'hui et de nouveau due : proposée même quand les quotas sont épuisés.
        QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-qcm", box=0,
                                    last_review=timezone.now(), premiere_revue=timezone.now(), seen=1)
        QuizDeck.objects.create(player="alice", set_id="reseaux/test_set", nouvelles_jour=1, revisions_jour=1)
        ids = [q["id"] for q in self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=review").context["questions"]]
        self.assertEqual(ids, ["q-qcm"])

    def test_plan_settings(self):
        from wiki.models import QuizDeck
        r = self.client.post("/qcm/planning/", {"set": "reseaux/test_set", "nouvelles_jour": "20",
                                                "revisions_jour": "", "date_objectif": "2030-06-01"})
        self.assertEqual(r.status_code, 302)
        self.assertIn("#set-reseaux-test_set", r["Location"])
        deck = QuizDeck.objects.get(player="alice", set_id="reseaux/test_set")
        self.assertEqual((deck.nouvelles_jour, deck.revisions_jour, str(deck.date_objectif)), (20, None, "2030-06-01"))
        # Champs vidés → réglages supprimés ; valeurs invalides refusées.
        self.client.post("/qcm/planning/", {"set": "reseaux/test_set", "nouvelles_jour": "", "date_objectif": ""})
        deck.refresh_from_db()
        self.assertEqual((deck.nouvelles_jour, deck.date_objectif), (None, None))
        self.client.post("/qcm/planning/", {"set": "reseaux/test_set", "revisions_jour": "0"})
        self.client.post("/qcm/planning/", {"set": "reseaux/test_set", "nouvelles_jour": "abc"})
        self.client.post("/qcm/planning/", {"set": "reseaux/test_set", "date_objectif": "demain"})
        deck.refresh_from_db()
        self.assertEqual((deck.nouvelles_jour, deck.revisions_jour, deck.date_objectif), (None, None, None))
        self.assertEqual(self.client.post("/qcm/planning/", {"set": "inconnu"}).status_code, 404)

    def test_record_measures_answer_time(self):
        from wiki.models import QuizDeck
        for duree in (4000, 10_000_000):  # la 2e est plafonnée (joueur absent)
            self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "q-qcm",
                                                    "correct": True, "duree_ms": duree}, content_type="application/json")
        deck = QuizDeck.objects.get(player="alice", set_id="reseaux/test_set")
        self.assertEqual((deck.reponses_chronometrees, deck.temps_ms), (2, 124_000))

    def test_estimation(self):
        from datetime import timedelta
        from django.utils import timezone
        from wiki import planning
        neuves = [(0, 0, True)] * 4
        # Réponses toujours justes : boîte 3 au bout de 0+1+3 jours → 5 jours, 12 réponses.
        self.assertEqual(planning.simuler(neuves, 4, 4, 1.0), (5, 12))
        # Un quota de nouvelles plus faible rallonge la durée ; un quota épuisé aujourd'hui décale d'un jour.
        self.assertGreater(planning.simuler(neuves, 1, 4, 1.0)[0], 5)
        self.assertEqual(planning.simuler(neuves, 4, 4, 1.0, deja=(4, 0))[0], 6)
        # Des révisions plafonnées ralentissent aussi.
        self.assertGreater(planning.simuler(neuves, 4, 1, 1.0)[0], 5)
        self.assertEqual(planning.simuler([(3, 0, False)], 1, 1, 1.0), (0, 0))

        aujourdhui = timezone.localdate()
        self.client.post("/qcm/planning/", {"set": "reseaux/test_set", "nouvelles_jour": "1",
                                            "date_objectif": str(aujourdhui + timedelta(days=60))})
        e = self.client.get("/qcm/").context["categories"][0]["sets"][0]["estimation"]
        self.assertEqual(e["statut"], "ok")
        self.assertEqual(e["debut"], aujourdhui + timedelta(days=60 - e["jours"]))
        # Examen trop proche : plus de nouvelles par jour conseillées.
        self.client.post("/qcm/planning/", {"set": "reseaux/test_set", "nouvelles_jour": "1",
                                            "date_objectif": str(aujourdhui + timedelta(days=e["jours"] - 2))})
        response = self.client.get("/qcm/")
        e = response.context["categories"][0]["sets"][0]["estimation"]
        self.assertIn(e["statut"], ("retard", "impossible"))
        if e["statut"] == "retard":
            self.assertGreater(e["nouvelles_conseillees"], 1)
        self.assertContains(response, "en retard")

class QuizImportTests(QuizTests):
    """Import de sets JSON par glisser-déposer (formulaire multipart)."""

    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)

    def _post(self, *fichiers, **champs):
        import json
        from django.core.files.uploadedfile import SimpleUploadedFile
        files = [SimpleUploadedFile(nom, contenu if isinstance(contenu, bytes) else json.dumps(contenu).encode())
                 for nom, contenu in fichiers]
        return self.client.post("/qcm/importer/", {"fichiers": files, **champs}, follow=True)

    def _vocab(self, titre="Vocabulaire"):
        return {"titre": titre, "questions": [{"id": "v1", "type": "QRC", "question": "chat", "reponses_texte": ["cat"]}]}

    def test_reserve_aux_admins(self):
        response = self._post(("vocab.json", self._vocab()), categorie="Anglais")
        self.assertEqual(response.status_code, 403)
        self.assertFalse((self.root / "QCM").exists())

    def test_import_valide(self):
        self.client.force_login(self.admin)
        response = self._post(("vocab.json", self._vocab()), categorie="Anglais")
        self.assertContains(response, "importé dans QCM/Anglais/vocab.json")
        self.assertTrue((self.root / "QCM" / "Anglais" / "vocab.json").is_file())
        from wiki.quiz import get_library
        self.assertEqual(get_library().get("QCM/Anglais/vocab").titre, "Vocabulaire")
        self.assertContains(self.client.get("/qcm/"), '<option value="Anglais">')

    def test_categorie_par_defaut_et_bom(self):
        import json
        self.client.force_login(self.admin)
        self._post(("vocab.json", "﻿".encode() + json.dumps(self._vocab()).encode()))
        self.assertTrue((self.root / "QCM" / "Importés" / "vocab.json").is_file())

    def test_json_invalide_refuse(self):
        self.client.force_login(self.admin)
        response = self._post(("casse.json", b"{pas du json"),
                              ("vide.json", {"questions": [{"type": "QRC", "question": "chat"}]}),
                              ("notes.txt", b"texte"), categorie="Anglais")
        self.assertContains(response, "JSON invalide")
        self.assertContains(response, "reponses_texte")
        self.assertContains(response, "seuls les fichiers .json")
        self.assertFalse((self.root / "QCM").exists())

    def test_remplacement_explicite(self):
        self.client.force_login(self.admin)
        self._post(("vocab.json", self._vocab("V1")), categorie="Anglais")
        response = self._post(("vocab.json", self._vocab("V2")), categorie="Anglais")
        self.assertContains(response, "existe déjà")
        self._post(("vocab.json", self._vocab("V2")), categorie="Anglais", remplacer="1")
        from wiki.quiz import get_library
        self.assertEqual(get_library().get("QCM/Anglais/vocab").titre, "V2")

    def test_categorie_invalide(self):
        self.client.force_login(self.admin)
        for categorie in ("../hors", "a/b", ".cache"):
            self.assertContains(self._post(("vocab.json", self._vocab()), categorie=categorie), "Catégorie invalide")
        self.assertFalse((self.root / "QCM").exists())
        self.assertFalse((self.root.parent / "hors").exists())


class QuizRangementTests(QuizTests):
    """Dossiers dans les langues, déplacement et suppression de sets (admins)."""

    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)

    def _langue(self):
        """Fichier de langue (Roumain) rangé dans vault/QCM/Importés."""
        import json
        langue = {"langue": "Roumain", "titre": "Verbes roumains",
                  "vocabulaire": [{"id": "v1", "mot": "a fi", "traductions": ["être"]}]}
        (self.root / "QCM" / "Importés").mkdir(parents=True)
        (self.root / "QCM" / "Importés" / "ro.json").write_text(json.dumps(langue), encoding="utf-8")

    def test_dossiers_de_langue(self):
        self._langue()
        response = self.client.get("/qcm/")
        self.assertContains(response, "Session du jour du dossier")
        self.assertContains(response, "/qcm/langues/Roumain/?dossier=Import%C3%A9s")
        self.assertNotContains(response, "Supprimer ce set")  # réservé aux admins
        self.assertContains(self.client.get("/qcm/langues/Roumain/?dossier=Importés"), "Dossier « Importés »")
        self.assertEqual(self.client.get("/qcm/langues/Roumain/?dossier=Autre").status_code, 404)
        self.assertEqual(self.client.get("/qcm/langues/Roumain/jouer/?dossier=Importés").status_code, 200)

    def test_deplacer_cree_le_dossier_et_garde_la_progression(self):
        from wiki.models import QuizProgress
        from wiki.quiz import get_library
        self._langue()
        QuizProgress.objects.create(player="alice", set_id="QCM/Importés/ro", question_id="v1")
        self.assertEqual(self.client.post("/qcm/deplacer/", {"set": "QCM/Importés/ro", "dossier": "Verbes"}).status_code, 403)
        self.client.force_login(self.admin)
        self.client.post("/qcm/deplacer/", {"set": "QCM/Importés/ro", "dossier": "Verbes"})
        self.assertTrue((self.root / "QCM" / "Roumain" / "Verbes" / "ro.json").is_file())
        self.assertFalse((self.root / "QCM" / "Importés").exists())  # dossier vide retiré
        self.assertIn("QCM/Roumain/Verbes/ro", get_library().langues)
        self.assertEqual(QuizProgress.objects.get().set_id, "QCM/Roumain/Verbes/ro")
        self.assertContains(self.client.post("/qcm/deplacer/", {"set": "QCM/Roumain/Verbes/ro", "dossier": "a/b"}, follow=True),
                            "Dossier invalide")
        # Un set de cours va dans vault/QCM/<dossier>.
        self.client.post("/qcm/deplacer/", {"set": "reseaux/test_set", "dossier": "Réseaux"})
        self.assertIn("QCM/Réseaux/test_set", get_library().sets)

    def test_supprimer_set_et_dossier(self):
        from wiki.models import QuizProgress
        from wiki.quiz import get_library
        self._langue()
        QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-qcm")
        self.assertEqual(self.client.post("/qcm/supprimer/", {"set": "reseaux/test_set"}).status_code, 403)
        self.client.force_login(self.admin)
        self.assertContains(self.client.get("/qcm/"), "Supprimer le dossier")
        self.client.post("/qcm/supprimer/", {"set": "reseaux/test_set"})
        self.assertFalse((self.root / "reseaux" / "test_set.json").exists())
        self.assertFalse(QuizProgress.objects.exists())
        self.assertEqual(self.client.post("/qcm/supprimer/", {"set": "reseaux/test_set"}).status_code, 404)
        self.client.post("/qcm/supprimer/", {"categorie": "Importés", "langue": "Roumain"})
        self.assertEqual(get_library().langues, {})
        self.assertTrue((self.root / "QCM").is_dir())  # vault/QCM est conservé


class DocumentationTests(QuizTests):
    def test_readmes_affiches(self):
        response = self.client.get("/documentation/")
        self.assertContains(response, "ProjetPluri")
        self.assertContains(response, 'href="/sommaire/"')  # lien relatif vault/ réécrit
        self.assertNotContains(response, 'href="core/tests.py"')
        self.assertContains(response, "<code>[texte](Page.md)</code>")  # exemple en code intact
        self.assertContains(self.client.get("/documentation/ia/"), "QRC")
        self.assertEqual(self.client.get("/documentation/secret/").status_code, 404)
        self.assertContains(self.client.get("/"), 'href="/documentation/"')

    def test_connexion_requise(self):
        self.client.logout()
        self.assertEqual(self.client.get("/documentation/").status_code, 302)


class QuizHorsLigneTests(QuizTests):
    """Mode hors ligne : téléchargement des sets et synchronisation des réponses."""

    SET = "reseaux/test_set"

    def _synchro(self, *reponses):
        import json
        return self.client.post("/qcm/hors-ligne/synchro/", data=json.dumps({"reponses": list(reponses)}),
                                content_type="application/json")

    def _rep(self, uid, date, correct=True, question="q-qcm", **extra):
        return {"uid": uid, "set_id": self.SET, "question_id": question, "correct": correct, "date": date, **extra}

    def test_page_et_catalogue(self):
        self.assertContains(self.client.get("/qcm/hors-ligne/"), "qcm_hors_ligne.js")
        data = self.client.get("/qcm/hors-ligne/catalogue/").json()
        self.assertEqual(data["joueur"], "alice")
        self.assertTrue(data["csrf"])
        self.assertEqual([(s["id"], s["total"]) for s in data["sets"]], [(self.SET, 4)])

    def test_telechargement_avec_progression(self):
        self.client.post("/qcm/reponse/", data={"set_id": self.SET, "question_id": "q-qcm", "correct": True},
                         content_type="application/json")
        data = self.client.get("/qcm/hors-ligne/sets/", {"id": [self.SET, "inconnu"]}).json()
        self.assertEqual(data["manquants"], ["inconnu"])
        (s,) = data["sets"]
        self.assertEqual(len(s["questions"]), 4)
        self.assertEqual(s["progression"]["q-qcm"]["box"], 1)
        self.assertIsNotNone(s["progression"]["q-qcm"]["last_review"])
        self.assertEqual(s["quotas"], {"nouvelles_jour": None, "revisions_jour": None})

    def test_synchro_rejoue_dans_l_ordre(self):
        from wiki.models import QuizDeck, QuizProgress
        # Envoyées dans le désordre : la dernière réponse (fausse) doit gagner.
        r = self._synchro(
            self._rep("c", "2026-10-03T08:00:00Z", correct=False, duree_ms=3000),
            self._rep("a", "2026-10-01T08:00:00Z"),
            self._rep("b", "2026-10-02T08:00:00+02:00"),
        )
        self.assertEqual(r.json(), {"traitees": ["c", "a", "b"], "enregistrees": 3})
        p = QuizProgress.objects.get(player="alice", set_id=self.SET, question_id="q-qcm")
        self.assertEqual((p.box, p.seen, p.correct, p.last_correct), (0, 3, 2, False))
        self.assertEqual(p.premiere_revue.isoformat(), "2026-10-01T08:00:00+00:00")
        self.assertEqual(QuizDeck.objects.get(player="alice", set_id=self.SET).temps_ms, 3000)
        # Renvoi après une coupure : déjà reçues, ignorées mais retirées de la file.
        r = self._synchro(self._rep("a", "2026-10-01T08:00:00Z"), self._rep("c", "2026-10-03T08:00:00Z", correct=False))
        self.assertEqual(r.json()["enregistrees"], 0)
        self.assertEqual(QuizProgress.objects.get(question_id="q-qcm").seen, 3)

    def test_synchro_ignore_les_reponses_depassees_et_invalides(self):
        from django.utils import timezone
        from wiki.models import QuizProgress
        # Question revue en ligne après la réponse hors ligne : la réponse hors ligne est ignorée.
        self.client.post("/qcm/reponse/", data={"set_id": self.SET, "question_id": "q-qcm", "correct": True},
                         content_type="application/json")
        r = self._synchro(
            self._rep("vieille", "2020-01-01T00:00:00Z", correct=False),
            self._rep("inconnue", "2026-10-01T00:00:00Z", question="nope"),
            self._rep("sans-date", None),
            self._rep("flash", "2099-01-01T00:00:00Z", question="q-flash", note="facile"),
        )
        self.assertEqual(r.json(), {"traitees": ["vieille", "inconnue", "sans-date", "flash"], "enregistrees": 1})
        self.assertEqual(QuizProgress.objects.get(question_id="q-qcm").box, 1)
        flash = QuizProgress.objects.get(question_id="q-flash")
        self.assertEqual(flash.box, 2)
        self.assertLessEqual(flash.last_review, timezone.now())  # date du futur ramenée à maintenant
        self.assertEqual(self.client.post("/qcm/hors-ligne/synchro/", data="{}", content_type="application/json").status_code, 400)

    def test_synchro_par_joueur_et_connexion_requise(self):
        from wiki.models import QuizProgress
        self._synchro(self._rep("a", "2026-10-01T08:00:00Z"))
        self.client.logout()
        self.assertEqual(self.client.get("/qcm/hors-ligne/catalogue/").status_code, 302)
        self.assertEqual(self._synchro(self._rep("b", "2026-10-02T08:00:00Z")).status_code, 302)
        self.assertEqual(list(QuizProgress.objects.values_list("player", "seen")), [("alice", 1)])

    def test_service_worker_et_manifeste_publics(self):
        self.client.logout()
        sw = self.client.get("/qcm/sw.js")
        self.assertEqual(sw.status_code, 200)
        self.assertIn("javascript", sw["Content-Type"])
        self.assertContains(sw, 'importScripts("/static/wiki/qcm_attente.js")')
        self.assertIn("connect-src 'self' https://cdn.jsdelivr.net", sw["Content-Security-Policy"])
        manifest = self.client.get("/qcm/manifest.webmanifest").json()
        self.assertEqual((manifest["start_url"], manifest["scope"]), ("/qcm/hors-ligne/", "/qcm/"))
