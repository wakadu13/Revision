import json
import tempfile
from pathlib import Path
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
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

    def test_save_without_leaving_editor(self):
        """Ctrl+S dans l'éditeur : réponse JSON avec la nouvelle version, sans redirection."""
        json_post = lambda data: self.client.post("/modifier/Dossier/Note", data, HTTP_ACCEPT="application/json")
        response = json_post({"content": "un\r\n", "version": ""})
        self.assertEqual(response.status_code, 200)
        file = self.root / "Dossier/Note.md"
        self.assertEqual(file.read_text(encoding="utf-8"), "un\n")
        self.assertEqual(response.json(), {"version": str(file.stat().st_mtime_ns), "url": "/wiki/Dossier/Note"})
        response = json_post({"content": "deux", "version": response.json()["version"]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(file.read_text(encoding="utf-8"), "deux")
        # Version périmée (page modifiée ailleurs) : 409, fichier intact.
        response = json_post({"content": "écrasé", "version": "0"})
        self.assertEqual(response.status_code, 409)
        self.assertIn("modifiée ailleurs", response.json()["error"])
        self.assertEqual(file.read_text(encoding="utf-8"), "deux")

    def test_editor_lists_attachments(self):
        self.write("Note.md", "")
        self.write("img/schéma.png", "")
        self.write("autre/schéma.png", "")
        self.write("doc.pdf", "")
        self.write("qcm/set.json", "{}")
        response = self.client.get("/modifier/Note")
        self.assertContains(response, 'src="/static/wiki/vendor/codemirror.min.js"')
        files = response.context["attachment_choices"]
        self.assertEqual([f["link"] for f in files], ["autre/schéma.png", "doc.pdf", "img/schéma.png"])
        self.assertEqual(files[1]["url"], "/pdf/doc.pdf")  # un PDF s'ouvre dans le lecteur

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


class AppareilTests(TestCase):
    """Application Android : jeton d'appareil à la place de la session."""

    SET = "reseaux/test_set"

    def setUp(self):
        QuizTests.setUp(self)  # même set de test, sans hériter de ses tests
        self.client.logout()

    def _connexion(self, password="x"):
        import json
        return self.client.post("/api/appareil/connexion/", data=json.dumps(
            {"username": "alice", "password": password, "appareil": "Pixel"}), content_type="application/json")

    def _auth(self, jeton):
        return {"HTTP_AUTHORIZATION": "Bearer " + jeton}

    def test_connexion_et_api_avec_jeton(self):
        import json
        from accounts.models import JetonAppareil
        from wiki.models import QuizProgress
        data = self._connexion().json()
        self.assertEqual(data["joueur"], "alice")
        jeton = data["jeton"]
        self.assertEqual(JetonAppareil.objects.get().nom, "Pixel")
        self.assertFalse(JetonAppareil.objects.filter(empreinte=jeton).exists())  # seule l'empreinte est gardée
        self.assertEqual(self.client.get("/qcm/hors-ligne/catalogue/", **self._auth(jeton)).json()["joueur"], "alice")
        sets = self.client.get("/qcm/hors-ligne/sets/", {"id": self.SET}, **self._auth(jeton)).json()
        self.assertEqual(len(sets["sets"][0]["questions"]), 4)
        # POST sans jeton CSRF : accepté avec un jeton d'appareil.
        client = self.client_class(enforce_csrf_checks=True)
        r = client.post("/qcm/hors-ligne/synchro/", data=json.dumps({"reponses": [
            {"uid": "a", "set_id": self.SET, "question_id": "q-qcm", "correct": True, "date": "2026-10-01T08:00:00Z"}]}),
            content_type="application/json", **self._auth(jeton))
        self.assertEqual(r.json()["enregistrees"], 1)
        self.assertEqual(QuizProgress.objects.get().player, "alice")
        self.assertIsNotNone(JetonAppareil.objects.get().utilise)

    def test_jeton_limite_a_l_api_hors_ligne(self):
        jeton = self._connexion().json()["jeton"]
        self.assertEqual(self.client.get("/qcm/", **self._auth(jeton)).status_code, 403)
        self.assertEqual(self.client.get("/compte/", **self._auth(jeton)).status_code, 403)
        self.assertEqual(self.client.get("/qcm/hors-ligne/catalogue/", **self._auth("faux")).status_code, 401)

    def test_mauvais_mot_de_passe_et_compte_desactive(self):
        self.assertEqual(self._connexion("faux").status_code, 401)
        self.assertEqual(self.client.post("/api/appareil/connexion/", data="{}", content_type="application/json").status_code, 400)
        jeton = self._connexion().json()["jeton"]
        self.user.is_active = False
        self.user.save()
        self.assertEqual(self.client.get("/qcm/hors-ligne/catalogue/", **self._auth(jeton)).status_code, 401)

    def test_deconnexion_et_revocation(self):
        from accounts.models import JetonAppareil
        jeton = self._connexion().json()["jeton"]
        self.assertEqual(self.client.post("/api/appareil/deconnexion/", **self._auth(jeton)).json(), {"ok": True})
        self.assertEqual(self.client.get("/qcm/hors-ligne/catalogue/", **self._auth(jeton)).status_code, 401)
        # Depuis « Mon compte » sur le wiki.
        self._connexion()
        self.client.force_login(self.user)
        self.assertContains(self.client.get("/compte/"), "Pixel")
        self.client.post(f"/compte/appareils/{JetonAppareil.objects.get().pk}/revoquer/")
        self.assertFalse(JetonAppareil.objects.exists())
        # Le jeton d'un autre compte ne se révoque pas.
        autre = get_user_model().objects.create_user("bob", password="y")
        a, _ = JetonAppareil.creer(autre)
        self.assertEqual(self.client.post(f"/compte/appareils/{a.pk}/revoquer/").status_code, 404)


class ImportTests(WikiTestCase):
    """Import de notes .md et de pièces jointes depuis le navigateur."""

    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(self.admin)

    def upload(self, files, json_reply=True, follow=False, **extra):
        data = {
            "fichiers": [SimpleUploadedFile(name.rsplit("/", 1)[-1], body) for name, body in files],
            "chemins": [name for name, _ in files],
            **extra,
        }
        headers = {"HTTP_ACCEPT": "application/json"} if json_reply else {}
        return self.client.post("/importer/", data, follow=follow, **headers)

    def test_page_reserved_to_admins(self):
        self.assertContains(self.client.get("/importer/"), "data-md-import")
        self.assertContains(self.client.get("/sommaire/"), "Importer (.md, PDF)")
        self.client.force_login(self.reader)
        self.assertEqual(self.client.get("/importer/").status_code, 403)
        self.assertEqual(self.upload([("a.md", b"x")]).status_code, 403)
        self.assertFalse((self.root / "a.md").exists())

    def test_import_folder_keeps_structure(self):
        response = self.upload([
            ("Coffre/Cours.md", "# Cours\r\nVoir [[Annexe]] et ![[schéma.png]]".encode("utf-8-sig")),
            ("Coffre/Sous/Annexe.markdown", b"Annexe"),
            ("Coffre/Sous/schéma.png", b"PNG"),
            ("Coffre/.obsidian/app.json", b"{}"),
        ], dossier="Importés")
        results = response.json()["results"]
        self.assertEqual([r["ok"] for r in results], [True, True, True, False])
        self.assertTrue(results[3]["ignored"])
        self.assertEqual(results[0]["path"], "Importés/Coffre/Cours.md")
        self.assertEqual(results[0]["url"], "/wiki/Import%C3%A9s/Coffre/Cours")
        self.assertEqual(results[1]["path"], "Importés/Coffre/Sous/Annexe.md")
        self.assertEqual(results[2]["link"], "schéma.png")
        # BOM retiré, fins de ligne normalisées.
        self.assertEqual((self.root / "Importés/Coffre/Cours.md").read_text(encoding="utf-8"),
                         "# Cours\nVoir [[Annexe]] et ![[schéma.png]]")
        self.assertFalse((self.root / "Importés/Coffre/.obsidian").exists())
        html = self.html("Importés/Coffre/Cours")
        self.assertIn('href="/wiki/Import%C3%A9s/Coffre/Sous/Annexe"', html)
        self.assertIn('src="/fichiers/Import%C3%A9s/Coffre/Sous/sch%C3%A9ma.png"', html)

    def test_refused_files(self):
        with mock.patch("wiki.uploads.MAX_NOTE_SIZE", 10):
            results = self.upload([
                ("page.html", b"<script></script>"),
                ("latin1.md", "é".encode("latin-1")),
                ("gros.md", b"x" * 11),
                ("a:b.md", b"x"),
                ("../dehors.md", b"x"),
            ]).json()["results"]
        self.assertEqual([r["ok"] for r in results], [False] * 5)
        self.assertIn("type de fichier", results[0]["message"])
        self.assertIn("UTF-8", results[1]["message"])
        self.assertIn("volumineux", results[2]["message"])
        self.assertIn("interdits", results[3]["message"])
        self.assertEqual(list(self.root.iterdir()), [])
        # Un fichier porte le nom d'un dossier du chemin : refus, pas d'erreur serveur.
        self.write("Fichier.md", "x")
        result = self.upload([("Fichier.md/dedans.md", b"x")]).json()["results"][0]
        self.assertFalse(result["ok"])
        self.assertEqual(self.upload([]).status_code, 400)

    def test_existing_file_kept_unless_replace(self):
        self.write("Dossier/Note.md", "ancien")
        result = self.upload([("note.md", b"nouveau")], dossier="dossier").json()["results"][0]
        self.assertFalse(result["ok"])
        self.assertIn("existe déjà", result["message"])
        self.assertEqual((self.root / "Dossier/Note.md").read_text(encoding="utf-8"), "ancien")
        # « Remplacer » : le fichier existant est écrasé, même à une casse près (pas de doublon).
        result = self.upload([("note.md", b"nouveau")], dossier="dossier", remplacer="1").json()["results"][0]
        self.assertTrue(result["ok"])
        self.assertEqual(result["path"], "Dossier/Note.md")
        self.assertEqual((self.root / "Dossier/Note.md").read_text(encoding="utf-8"), "nouveau")
        self.assertEqual([p.name for p in self.root.rglob("*.md")], ["Note.md"])

    def test_form_without_javascript(self):
        response = self.upload([("Seule.md", b"x")], json_reply=False)
        self.assertRedirects(response, "/wiki/Seule")
        response = self.upload([("Une.md", b"x"), ("Deux.md", b"x"), ("x.exe", b"x")], json_reply=False, follow=True)
        self.assertRedirects(response, "/importer/")
        self.assertContains(response, "2 fichiers importés")
        self.assertContains(response, "x.exe : type de fichier non accepté")

    def test_imported_pdf_opens_in_reader(self):
        result = self.upload([("Poly.pdf", b"%PDF-1.4")], dossier="Cours").json()["results"][0]
        self.assertEqual(result["url"], "/pdf/Cours/Poly.pdf")
        self.assertRedirects(self.upload([("Autre.pdf", b"%PDF")], json_reply=False), "/pdf/Autre.pdf")

    def test_pasted_image_goes_to_obsidian_attachment_folder(self):
        self.write("Cours/Note.md", "")
        self.write(".obsidian/app.json", json.dumps({"attachmentFolderPath": "./images"}))
        first = self.upload([("Pasted image 1.png", b"1")], pour_note="Cours/Note").json()["results"][0]
        second = self.upload([("Pasted image 1.png", b"2")], pour_note="Cours/Note").json()["results"][0]
        self.assertEqual(first["path"], "Cours/images/Pasted image 1.png")
        self.assertEqual(second["path"], "Cours/images/Pasted image 1 1.png")
        self.assertIn("sous le nom", second["message"])
        self.assertEqual(second["link"], "Pasted image 1 1.png")
        self.assertEqual(second["url"], "/fichiers/Cours/images/Pasted%20image%201%201.png")
        self.assertEqual((self.root / "Cours/images/Pasted image 1.png").read_bytes(), b"1")

    def test_attachment_folder_setting(self):
        vault = get_vault()
        self.assertEqual(vault.attachment_folder("Cours/Note"), "")  # pas de réglage : racine, comme Obsidian
        for setting, expected in [("/", ""), ("./", "Cours"), ("./img", "Cours/img"), ("Pièces jointes", "Pièces jointes"),
                                  ("../hors", ""), (".cache", "")]:
            with self.subTest(setting=setting):
                self.write(".obsidian/app.json", json.dumps({"attachmentFolderPath": setting}))
                self.assertEqual(vault.attachment_folder("Cours/Note"), expected)
        self.write(".obsidian/app.json", "pas du JSON")
        self.assertEqual(vault.attachment_folder("Note"), "")


class PdfReaderTests(WikiTestCase):
    """Lecteur de PDF intégré (PDF.js) : page complète, intégration dans les notes, arborescence."""

    def setUp(self):
        super().setUp()
        self.write("Cours/Réseau/Poly réseau.pdf", "%PDF-1.4")
        self.write("Cours/Réseau/Fiche.md", "Support : [[Poly réseau.pdf]]\n\n![[Poly réseau.pdf#page=3]]\n\n![[Poly réseau.pdf]]")

    def test_reader_page(self):
        response = self.client.get("/pdf/Cours/Réseau/Poly réseau.pdf")
        self.assertContains(response, 'data-src="/fichiers/Cours/R%C3%A9seau/Poly%20r%C3%A9seau.pdf"')
        self.assertContains(response, 'src="/static/wiki/lecteur_pdf.js"')
        self.assertContains(response, "vendor/pdfjs/pdf.worker.min.js")
        self.assertContains(response, "pdf_viewer.min.css")
        self.assertContains(response, "<h1 class=\"note-title\">Poly réseau</h1>", html=False)
        # Rétroliens : les notes qui citent le PDF ; arborescence : le PDF, marqué actif.
        self.assertEqual([n.name for n in response.context["backlinks"]], ["Fiche"])
        self.assertContains(response, 'class="tree-note tree-file active"')
        # Insensible à la casse, comme les liens du wiki.
        self.assertEqual(self.client.get("/pdf/cours/réseau/poly réseau.pdf").status_code, 200)

    def test_embedded_reader(self):
        response = self.client.get("/pdf/Cours/Réseau/Poly réseau.pdf?integre=1")
        self.assertTemplateUsed(response, "wiki/pdf_integre.html")
        self.assertContains(response, "is-embedded")
        self.assertContains(response, 'target="_top"')
        self.assertNotContains(response, 'class="sidebar"')
        self.assertEqual(response["X-Frame-Options"], "SAMEORIGIN")

    def test_not_a_pdf(self):
        self.write("image.png", "x")
        self.assertEqual(self.client.get("/pdf/image.png").status_code, 404)
        self.assertEqual(self.client.get("/pdf/absent.pdf").status_code, 404)
        self.assertEqual(self.client.get("/pdf/Cours/Réseau/Fiche.md").status_code, 404)

    def test_links_and_embeds_in_notes(self):
        html = self.html("Cours/Réseau/Fiche")
        self.assertIn('<a class="internal-link" href="/pdf/Cours/R%C3%A9seau/Poly%20r%C3%A9seau.pdf">Poly réseau.pdf</a>', html)
        self.assertIn('src="/pdf/Cours/R%C3%A9seau/Poly%20r%C3%A9seau.pdf?integre=1#page=3"', html)
        self.assertIn('src="/pdf/Cours/R%C3%A9seau/Poly%20r%C3%A9seau.pdf?integre=1"', html)
        self.assertIn("allowfullscreen", html)

    def test_pdfs_listed_in_tree_and_sommaire(self):
        tree = get_vault().tree
        cours = next(f for f in tree["folders"] if f["name"] == "Cours")
        reseau = cours["folders"][0]
        self.assertEqual([f.name for f in reseau["files"]], ["Poly réseau.pdf"])
        self.assertEqual(reseau["count"], 2)
        self.assertContains(self.client.get("/sommaire/"), 'href="/pdf/Cours/R%C3%A9seau/Poly%20r%C3%A9seau.pdf"')


LATEX_COURSE = r"""$$
% Préambule d'un cours
\documentclass{report}
\usepackage{amsmath}
\newtheorem{definition}{Définition}[chapter]
\newtheorem{proposition}[definition]{Proposition}
\newtheorem{exercice}{Exercice}[chapter]
\renewcommand{\proofname}{Démonstration}
\newtcolorbox{retenir}[1][À retenir]{colback=white}
\newcommand{\cpl}[1]{\overline{#1}}
\newcommand{\nQ}{\overline{Q}}
\begin{document}
\begin{titlepage}
{\Large Logique séquentielle\par}
\end{titlepage}
\tableofcontents
\chapter*{Notations}
On note $\cpl{A}$ le complément. % commentaire
\chapter{Les bascules}
\label{ch:bascules}
\section{Généralités}
\begin{definition}[Bascule]
Une \emph{bascule} stocke un \textbf{bit}.
\end{definition}
\begin{proposition}
\label{prop:rs}
On a
\begin{equation}
  Q_{t+1} = S + \cpl{R}\,Q_t \label{eq:rs}
\end{equation}
\end{proposition}
\begin{proof}
D'après \eqref{eq:rs} et la proposition~\ref{prop:rs}.
\end{proof}
\begin{enumerate}[(i)]
  \item premier ;
  \item second.
\end{enumerate}
\begin{enumerate}[\textbf{Phase \arabic*.}, leftmargin=*]
  \item mise à 1.
\end{enumerate}
\begin{center}
\begin{tabular}{|cc|c|}
\hline
\multicolumn{2}{|c|}{Entrées} & Sortie \\ \hline
\rowcolor{bleu!10} $S$ & $R$ & $|Q|$ \\
\multirow{2}{*}{0} & 1 & $\nQ_t$ \\ \hline
\end{tabular}
\end{center}
\begin{figure}[htbp]
\centering
\begin{circuitikz}
  \node[nand port] (G1) at (0,0) {};
\end{circuitikz}
\caption{La bascule RS.}
\label{fig:rs}
\end{figure}
Voir la figure~\ref{fig:rs}, le chapitre~\ref{ch:bascules}\footnote{Note de bas de page.}.
\begin{retenir}
\begin{itemize}
  \item Une bascule mémorise un bit.
\end{itemize}
\end{retenir}
\begin{verbatim}
$ ne_pas_toucher % ici
\end{verbatim}
\appendix
\titleformat{\chapter}[display]{\bfseries}{Annexe~\thechapter}{0.5em}{\Huge}
\chapter{Corrigés}
\begin{exercice}
Prix : 5 \$ et 10 \$.
\end{exercice}
\end{document}
$$"""


class LatexTests(WikiTestCase):
    """Conversion d'un cours LaTeX en page du wiki."""

    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)

    def test_course_structure(self):
        from .latex import convert

        md = convert(LATEX_COURSE)
        # $$ autour du document, préambule et commentaires retirés ; titres numérotés comme LaTeX.
        self.assertNotIn("documentclass", md)
        self.assertNotIn("commentaire", md)
        self.assertIn("> [!info] Page de titre\n> Logique séquentielle", md)
        self.assertIn("# Notations\n", md)
        self.assertIn("# Chapitre 1 — Les bascules", md)
        self.assertIn("## 1.1 Généralités", md)
        self.assertIn("# Annexe A — Corrigés", md)
        self.assertNotIn("display", md)  # \titleformat ignoré
        # Macros développées pour KaTeX.
        self.assertIn(r"On note $\overline{A}$ le complément.", md)
        # Théorèmes en encadrés, compteur partagé, démonstration repliée, équation numérotée.
        self.assertIn("> [!definition] Définition 1.1 (Bascule)\n> Une *bascule* stocke un **bit**.", md)
        self.assertIn("> [!theoreme] Proposition 1.2", md)
        self.assertIn(r"> Q_{t+1} = S + \overline{R}\,Q_t \tag{1.1}", md)
        self.assertIn("> [!demonstration]- Démonstration\n> D'après (1.1) et la proposition 1.2.", md)
        self.assertIn("> [!exercice] Exercice A.1", md)
        self.assertIn(r"Prix : 5 \$ et 10 \$.", md)
        # Listes à étiquettes.
        self.assertIn("- **(i)** premier ;\n- **(ii)** second.", md)
        self.assertIn("- **Phase 1.** mise à 1.", md)
        # Tableau : colonnes fusionnées, couleurs retirées, | dans une formule protégé.
        self.assertIn("| Entrées |  | Sortie |\n| --- | --- | --- |\n| $S$ | $R$ | $\\vert Q\\vert$ |", md)
        self.assertIn("| 0 | 1 | $\\overline{Q}_t$ |", md)
        # Figure TikZ : légende numérotée, code source replié, avertissement en tête.
        self.assertTrue(md.startswith("> [!info] Converti depuis LaTeX"))
        self.assertIn("> [!figure]- Figure 1.1 — La bascule RS.", md)
        self.assertIn("> \\begin{circuitikz}", md)
        # Renvois : numéros, liens vers les titres ; note de bas de page.
        self.assertIn("Voir la figure 1.1, le chapitre [[#Chapitre 1 — Les bascules|1]][^1].", md)
        self.assertIn("[^1]: Note de bas de page.", md)
        self.assertIn("> [!retenir] À retenir\n> - Une bascule mémorise un bit.", md)
        self.assertIn("```\n$ ne_pas_toucher % ici\n```", md)

    def test_converted_page_renders(self):
        from .latex import convert

        self.write("Cours.md", convert(LATEX_COURSE))
        html = self.html("Cours")
        self.assertIn('data-callout="definition"', html)
        self.assertIn('<details class="callout" data-callout="demonstration">', html)
        self.assertIn('<details class="callout" data-callout="figure">', html)
        self.assertIn('class="math math-block"', html)
        self.assertIn("<table>", html)
        self.assertIn('href="#chapitre-1-les-bascules"', html)

    def test_editor_conversion_endpoint(self):
        self.client.force_login(self.admin)
        response = self.client.post("/latex/", {"source": r"\section{Titre} Texte $\alpha$."})
        self.assertEqual(response.json(), {"markdown": "## 1 Titre\n\nTexte $\\alpha$.\n"})
        self.assertEqual(self.client.post("/latex/", {"source": " "}).status_code, 400)
        self.assertContains(self.client.get("/modifier/Note"), 'data-latex-url="/latex/"')
        self.client.force_login(self.reader)
        self.assertEqual(self.client.post("/latex/", {"source": "x"}).status_code, 403)

    def test_import_tex_file(self):
        self.client.force_login(self.admin)
        upload = SimpleUploadedFile("Logique.tex", LATEX_COURSE.encode("utf-8"))
        result = self.client.post("/importer/", {"fichiers": [upload], "chemins": ["Logique.tex"], "dossier": "Cours"},
                                  HTTP_ACCEPT="application/json").json()["results"][0]
        self.assertTrue(result["ok"])
        self.assertEqual(result["path"], "Cours/Logique.md")
        self.assertEqual(result["message"], "converti depuis LaTeX")
        self.assertIn("# Chapitre 1 — Les bascules", (self.root / "Cours/Logique.md").read_text(encoding="utf-8"))
        self.assertFalse((self.root / "Cours/Logique.tex").exists())

    def test_looks_like_latex(self):
        from .latex import looks_like_latex

        self.assertTrue(looks_like_latex(LATEX_COURSE))
        self.assertFalse(looks_like_latex(r"$$\frac{a}{b}$$"))


class ApplicationTests(TestCase):
    """Application Android : wiki complet dans la WebView, session ouverte avec le jeton."""

    setUp = AppareilTests.setUp
    _connexion = AppareilTests._connexion
    _auth = AppareilTests._auth
    APP = {"HTTP_USER_AGENT": "Mozilla/5.0 (Linux; Android 15) Chrome/140 Mobile ProjetPluriApp/2.0"}

    def test_jeton_ouvre_une_session(self):
        from accounts.models import JetonAppareil
        jeton = self._connexion().json()["jeton"]
        anonyme = self.client_class()
        self.assertEqual(anonyme.get("/").status_code, 302)  # site privé
        # L'appli (sans cookie, sans jeton CSRF) échange son jeton contre une session.
        appli = self.client_class(enforce_csrf_checks=True)
        r = appli.post("/api/appareil/session/", **self._auth(jeton))
        self.assertEqual(r.json(), {"ok": True, "joueur": "alice"})
        self.assertIn("sessionid", r.cookies)
        self.assertEqual(r.cookies["sessionid"]["max-age"], 60 * 60 * 24 * 14)
        session = self.client_class()
        session.cookies["sessionid"] = r.cookies["sessionid"].value
        self.assertEqual(session.get("/qcm/").status_code, 200)
        # Révoquer le jeton (page « Mon compte ») ferme aussi cette session.
        JetonAppareil.objects.all().delete()
        self.assertEqual(session.get("/qcm/").status_code, 302)
        self.assertEqual(appli.post("/api/appareil/session/", **self._auth(jeton)).status_code, 401)

    def test_session_demande_un_jeton(self):
        self.assertEqual(self.client.post("/api/appareil/session/").status_code, 302)  # anonyme : connexion
        self.client.force_login(get_user_model().objects.get(username="alice"))
        self.assertEqual(self.client.post("/api/appareil/session/").status_code, 400)

    def test_navigation_de_l_application(self):
        self.client.force_login(get_user_model().objects.get(username="alice"))
        page = self.client.get("/qcm/", **self.APP)
        self.assertContains(page, '<body class="app ')
        self.assertContains(page, 'class="app-nav"')
        self.assertContains(page, 'href="https://appassets.androidplatform.net/index.html"')
        # Déconnexion par les réglages de l'appli (le jeton reconnecterait aussitôt).
        self.assertContains(page, 'href="https://appassets.androidplatform.net/connexion.html">Se déconnecter')
        self.assertNotContains(page, 'action="/deconnexion/"')
        navigateur = self.client.get("/qcm/")
        self.assertNotContains(navigateur, 'class="app-nav"')
        self.assertNotContains(navigateur, "appassets")
        self.assertContains(navigateur, 'action="/deconnexion/"')
