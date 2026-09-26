import tempfile
from pathlib import Path

from django.test import TestCase, override_settings

from .vault import get_vault


class WikiTestCase(TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        override = override_settings(WIKI_DIR=self.root, WIKI_HOME="Accueil")
        override.enable()
        self.addCleanup(override.disable)

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

    @override_settings(WIKI_EDIT_LOGIN_REQUIRED=True)
    def test_login_required(self):
        response = self.client.post("/modifier/Planning", {"content": "x", "version": ""})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])
        self.assertFalse((self.root / "Planning.md").exists())
        self.assertEqual(self.client.post("/apercu/X", {"content": "x"}).status_code, 403)


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
        override = override_settings(WIKI_DIR=self.root, WIKI_HOME="Accueil", WIKI_EDIT_LOGIN_REQUIRED=False)
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
        # Une mauvaise réponse fait redescendre d'une boîte.
        self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "q-qcm", "correct": False},
                         content_type="application/json")
        p.refresh_from_db()
        self.assertEqual(p.box, 1)

    def test_review_mode_only_due(self):
        from wiki.models import QuizProgress
        from django.utils import timezone
        # q-qcm en boîte 5, révisée à l'instant → pas due ; les autres jamais vues → dues.
        QuizProgress.objects.create(set_id="reseaux/test_set", question_id="q-qcm", box=5,
                                    last_review=timezone.now(), seen=1, correct=1)
        response = self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=review")
        ids = {q["id"] for q in response.context["questions"]}
        self.assertNotIn("q-qcm", ids)
        self.assertEqual(len(ids), 3)

    def test_record_rejects_unknown_question(self):
        r = self.client.post("/qcm/reponse/", data={"set_id": "reseaux/test_set", "question_id": "nope", "correct": True},
                             content_type="application/json")
        self.assertEqual(r.status_code, 404)

    def test_reset(self):
        from wiki.models import QuizProgress
        QuizProgress.objects.create(set_id="reseaux/test_set", question_id="q-qcm", box=3)
        self.client.post("/qcm/reinitialiser/", {"set": "reseaux/test_set"})
        self.assertFalse(QuizProgress.objects.filter(set_id="reseaux/test_set").exists())
