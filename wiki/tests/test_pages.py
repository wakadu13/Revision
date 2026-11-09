"""Pages du wiki : lecture, interface, éditeur, sommaire et recherche, documentation,
historique, lecture hors ligne, détection des changements du coffre, erreurs, production."""

import json
import tempfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import override_settings

from wiki.vault import get_vault

from .base import QuizBase, WikiTestCase


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


class PleinEcranTests(WikiTestCase):
    def test_fullscreen_button_and_script(self):
        self.write("Accueil.md", "Bonjour")
        html = self.client.get("/wiki/Accueil").content.decode()
        head, body = html.split("<body", 1)
        self.assertIn("wiki/plein_ecran.js", head)
        self.assertIn("data-plein-ecran", body)
        self.assertIn('<main class="content" tabindex="-1">', body)
        self.client.logout()
        self.assertNotContains(self.client.get("/connexion/"), "data-plein-ecran")

    def test_reading_pages_need_no_extra_script(self):
        # En plein écran, ces pages s'ouvrent sans recharger le document (qui ferait
        # quitter le plein écran au navigateur) : seulement si leur corps n'a aucun script.
        self.write("Accueil.md", "# Titre\n\n$$x^2$$\n\n```python\nprint(1)\n```\n\n#cours")
        for url in ["/wiki/Accueil", "/sommaire/", "/recherche/?q=Titre", "/tags/", "/tags/cours"]:
            with self.subTest(url=url):
                body = self.client.get(url).content.decode().split("<body", 1)[1]
                self.assertNotIn("<script src", body)

    def test_reading_pages_hide_the_menu_unless_pinned(self):
        self.write("Accueil.md", "Bonjour")
        self.write("cours.pdf", "%PDF-1.4\n%%EOF\n")
        for url in ["/wiki/Accueil", "/pdf/cours.pdf"]:
            with self.subTest(url=url):
                html = self.client.get(url).content.decode()
                self.assertIn('<body class="lecture menu-cache"', html)
                self.assertIn("data-ouvrir-menu", html)
                self.assertIn('data-epingler-menu aria-pressed="false"', html)
        # Menu épinglé (cookie posé par le bouton « Garder le menu affiché »).
        self.client.cookies["menu"] = "epingle"
        html = self.client.get("/wiki/Accueil").content.decode()
        self.assertIn('<body class="lecture" data-sw', html)
        self.assertIn('data-epingler-menu aria-pressed="true"', html)
        self.assertIn('title="Cacher le menu pendant la lecture"', html)
        # Les autres pages gardent le menu.
        del self.client.cookies["menu"]
        for url in ["/sommaire/", "/recherche/?q=x", "/tags/"]:
            with self.subTest(url=url):
                self.assertNotContains(self.client.get(url), "menu-cache")

    def test_editor_fullscreen_button(self):
        get_user_model().objects.filter(pk=self.reader.pk).update(is_staff=True)
        self.write("Accueil.md", "Bonjour")
        html = self.client.get("/modifier/Accueil").content.decode()
        toolbar = html.split('class="toolbar"', 1)[1].split("</div>\n    <div class=\"editor-notice\"", 1)[0]
        self.assertIn("data-plein-ecran", toolbar)
        self.assertNotIn('data-action="focus"', html)


class StaticVersionneTests(WikiTestCase):
    def test_static_urls_change_with_content(self):
        # Cloudflare et les navigateurs gardent CSS et JS des heures : l'adresse porte
        # une empreinte du contenu, la nouvelle version est chargée dès la mise à jour.
        from config import storage

        self.write("Accueil.md", "Bonjour")
        html = self.client.get("/wiki/Accueil").content.decode()
        self.assertRegex(html, r'href="/static/wiki/wiki\.css\?v=[0-9a-f]{10}"')
        self.assertRegex(html, r'src="/static/wiki/wiki\.js\?v=[0-9a-f]{10}" defer')
        version = storage.empreinte("wiki/wiki.css")
        response = self.client.get(f"/static/wiki/wiki.css?v={version}")
        self.assertEqual(response.status_code, 200)
        response.close()
        # Dossier (base d'adresses de PDF.js) : sans empreinte.
        self.assertEqual(storage.StaticVersionne().url("wiki/vendor/pdfjs/wasm/"), "/static/wiki/vendor/pdfjs/wasm/")
        # Contenu modifié : nouvelle empreinte.
        with tempfile.TemporaryDirectory() as tmp:
            fichier = Path(tmp) / "a.css"
            fichier.write_text("a{}", encoding="utf-8")
            avant = storage._empreinte(str(fichier), *self._etat(fichier))
            fichier.write_text("b{color:red}", encoding="utf-8")
            self.assertNotEqual(avant, storage._empreinte(str(fichier), *self._etat(fichier)))

    @staticmethod
    def _etat(fichier):
        etat = fichier.stat()
        return etat.st_mtime_ns, etat.st_size


class InterfaceTests(WikiTestCase):
    def test_theme_toggle_and_palette_in_base(self):
        self.write("Accueil.md", "Bonjour")
        html = self.client.get("/wiki/Accueil").content.decode()
        self.assertIn('localStorage.getItem("wiki-theme")', html)  # appliqué avant le rendu (nonce CSP)
        self.assertRegex(html, r'<script nonce="[^"]+">try\{var t=localStorage')
        self.assertIn("data-theme-toggle", html)
        self.assertIn('data-theme-css="dark"', html)
        self.assertIn("wiki/palette.js", html)
        self.assertIn("data-palette", html)
        css = (Path(__file__).resolve().parents[1] / "static/wiki/wiki.css").read_text(encoding="utf-8")
        self.assertIn(':root[data-theme="dark"] {', css)
        self.assertIn(':root:not([data-theme="light"]) {', css)
        self.client.logout()
        self.assertNotIn("palette.js", self.client.get("/connexion/").content.decode())

    def test_palette_data(self):
        self.write("Cours/Signal.md", "# Signal")
        self.write("cours.pdf", "%PDF-1.4\n%%EOF\n")
        self.write("QCM/Linux/base.json", json.dumps({"titre": "Linux de base", "questions": [
            {"type": "QCM", "question": "?", "choix": ["a", "b"], "reponses": [0]}]}))
        self.write("QCM/langues/en.json", json.dumps({"langue": "Anglais", "vocabulaire": [{"mot": "a job", "traductions": ["un emploi"]}]}))
        data = self.client.get("/palette.json").json()
        self.assertIn({"t": "Signal", "s": "Cours", "u": "/wiki/Cours/Signal"}, data["pages"])
        self.assertIn({"t": "cours", "s": "PDF", "u": "/pdf/cours.pdf"}, data["pages"])
        self.assertEqual(data["qcm"], [{"t": "Linux de base", "s": "Linux", "u": "/qcm/jouer/?set=QCM/Linux/base&mode=all"}])
        self.assertEqual(data["langues"][0], {"t": "Session du jour · Anglais", "u": "/qcm/langues/Anglais/jouer/?mode=quotidien"})
        titres = [c["t"] for c in data["commandes"]]
        self.assertIn("Thème : clair, sombre ou automatique", titres)
        self.assertNotIn("Nouvelle page", titres)  # lecteur : pas de commandes d'admin
        get_user_model().objects.filter(pk=self.reader.pk).update(is_staff=True)
        titres = [c["t"] for c in self.client.get("/palette.json").json()["commandes"]]
        self.assertIn("Nouvelle page", titres)
        self.client.logout()
        self.assertEqual(self.client.get("/palette.json").status_code, 302)


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
        self.assertContains(response, 'src="/static/wiki/vendor/codemirror.min.js?v=')
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


class DocumentationTests(QuizBase):
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


class EditeurConvivialTests(WikiTestCase):
    """Éditeur : menus Encadré et Insérer, annuler/rétablir, aide, côte à côte, brouillon, tags."""

    def test_outils_de_l_editeur(self):
        get_user_model().objects.filter(pk=self.reader.pk).update(is_staff=True)
        self.write("Cours/Signal.md", "---\ntags: [signal, maths]\n---\n# Signal\n\nTexte #physique.\n")
        page = self.client.get("/modifier/Cours/Signal")
        html = page.content.decode()
        for attendu in ('data-action="undo"', 'data-action="redo"', 'data-menu="encadre"', 'data-menu="inserer"',
                        'data-mode="split"', 'data-action="aide"', 'id="aide-dialog"', 'data-brouillon-notice',
                        'id="tag-choices"'):
            self.assertIn(attendu, html)
        self.assertEqual(page.context["tag_choices"], ["maths", "physique", "signal"])
        # L'ancien bouton « Encadré » unique a laissé la place au menu.
        self.assertNotIn('data-action="callout"', html)


class HistoriqueTests(WikiTestCase):
    """Versions précédentes des pages : gardées à chaque modification, comparées, restaurées."""

    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(self.admin)
        self.versions = tempfile.TemporaryDirectory()
        self.addCleanup(self.versions.cleanup)
        override = override_settings(DATA_DIR=Path(self.versions.name))
        override.enable()
        self.addCleanup(override.disable)

    def _modifier(self, key, contenu):
        from wiki.vault import get_vault
        version = str((get_vault().root / f"{key}.md").stat().st_mtime_ns)
        return self.client.post(f"/modifier/{key}", {"content": contenu, "version": version}, HTTP_ACCEPT="application/json")

    def test_versions_differences_restauration(self):
        import time

        from wiki import historique
        self.write("Cours/Signal.md", "# Signal\n\nPremière version.\n")
        self.assertEqual(historique.lister("Cours/Signal.md"), [])
        self.assertEqual(self._modifier("Cours/Signal", "# Signal\n\nDeuxième version.\n").status_code, 200)
        time.sleep(0.01)
        self.assertEqual(self._modifier("Cours/Signal", "# Signal\n\nTroisième version.\n").status_code, 200)
        self._modifier("Cours/Signal", "# Signal\n\nTroisième version.\n")  # texte identique : pas de version
        versions = historique.lister("Cours/Signal.md")
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[0]["auteur"], "admin")
        self.assertEqual(historique.lire("Cours/Signal.md", versions[1]["id"]), "# Signal\n\nPremière version.\n")
        self.assertIsNone(historique.lire("Cours/Signal.md", "../../x.md"))
        self.assertTrue((Path(self.versions.name) / "versions" / "Cours" / "Signal.md").is_dir())
        page = self.client.get("/historique/Cours/Signal")
        self.assertContains(page, "Historique de « Signal »")
        self.assertContains(page, "Deuxième version.")   # version la plus récente, retirée depuis
        self.assertContains(page, "Troisième version.")  # page actuelle, ajoutée
        self.assertContains(page, 'class="diff-suppr">')
        self.assertContains(page, 'class="diff-ajout">')
        self.assertContains(self.client.get("/wiki/Cours/Signal"), 'href="/historique/Cours/Signal"')
        self.assertContains(self.client.get("/modifier/Cours/Signal"), "Historique des versions")
        # Restauration de la première version : la page actuelle part dans l'historique.
        r = self.client.post("/historique/Cours/Signal", {"action": "restaurer", "v": versions[1]["id"]})
        self.assertRedirects(r, "/wiki/Cours/Signal")
        self.assertEqual((self.root / "Cours" / "Signal.md").read_text(encoding="utf-8"), "# Signal\n\nPremière version.\n")
        self.assertEqual(len(historique.lister("Cours/Signal.md")), 3)
        self.assertEqual(self.client.post("/historique/Cours/Signal", {"action": "restaurer", "v": "nope"}).status_code, 404)
        self.assertEqual(self.client.get("/historique/Inconnue").status_code, 404)
        # Lecteur simple : pas d'accès.
        self.client.force_login(self.reader)
        self.assertEqual(self.client.get("/historique/Cours/Signal").status_code, 403)
        self.assertNotContains(self.client.get("/wiki/Cours/Signal"), "/historique/")

    def test_import_et_claude_gardent_la_version(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from wiki import historique
        self.write("Cours/Signal.md", "# Ancien\n")
        self.client.post("/importer/", {"fichiers": SimpleUploadedFile("Signal.md", b"# Nouveau\n"), "chemins": "Signal.md",
                                        "dossier": "Cours", "remplacer": "1"}, HTTP_ACCEPT="application/json")
        self.assertEqual((self.root / "Cours" / "Signal.md").read_text(encoding="utf-8"), "# Nouveau\n")
        versions = historique.lister("Cours/Signal.md")
        self.assertEqual([v["auteur"] for v in versions], ["admin"])
        self.assertEqual(historique.lire("Cours/Signal.md", versions[0]["id"]), "# Ancien\n")

    def test_limite_et_differences(self):
        from wiki import historique
        with override_settings(DATA_DIR=Path(self.versions.name)):
            for i in range(historique.MAX_VERSIONS + 5):
                historique.sauvegarder("Note.md", f"v{i}", "alice")
            self.assertEqual(len(historique.lister("Note.md")), historique.MAX_VERSIONS)
        diff = historique.differences("a\nb\nc\n", "a\nB\nc\nd\n")
        self.assertEqual([(l["type"], l["texte"]) for l in diff if l["type"] != "info"],
                         [("contexte", "a"), ("suppr", "b"), ("ajout", "B"), ("contexte", "c"), ("ajout", "d")])
        with self.assertRaises(ValueError):
            historique.sauvegarder("../hors.md", "x")


class HorsLigneWikiTests(WikiTestCase):
    """Service worker du wiki entier, manifeste, page hors connexion, dossiers à garder."""

    def test_service_worker_manifeste_et_page(self):
        self.client.logout()
        sw = self.client.get("/sw.js")
        self.assertEqual(sw.status_code, 200)
        self.assertIn("javascript", sw["Content-Type"])
        self.assertContains(sw, 'const CACHE = "wiki-hors-ligne-v1"')
        self.assertContains(sw, "/hors-connexion/")
        self.assertContains(sw, "/static/wiki/wiki.css?v=")
        self.assertContains(sw, "/^\\/qcm\\//")  # le QCM garde son propre service worker
        manifest = self.client.get("/manifest.webmanifest").json()
        self.assertEqual((manifest["name"], manifest["start_url"], manifest["scope"], manifest["display"]),
                         ("ProjetPluri", "/", "/", "standalone"))
        page = self.client.get("/hors-connexion/")
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "data-pages-hors-ligne")
        self.assertContains(page, "hors_ligne_wiki.js")

    def test_base_et_sommaire(self):
        self.write("Cours/Signal.md", "# Signal\n")
        self.write("Cours/schema.png", "")
        self.write("Cours/poly.pdf", "%PDF-1.4")
        self.write("Autre/Note.md", "# Note\n")
        page = self.client.get("/wiki/Cours/Signal")
        self.assertContains(page, 'rel="manifest" href="/manifest.webmanifest"')
        self.assertContains(page, 'data-sw="/sw.js"')
        sommaire = self.client.get("/sommaire/")
        self.assertContains(sommaire, 'data-dossier="Cours/"')
        self.assertContains(sommaire, 'data-dossier-url="/hors-ligne/dossier.json"')
        self.assertContains(sommaire, "hors_ligne_wiki.js")
        data = self.client.get("/hors-ligne/dossier.json", {"dossier": "Cours/"}).json()
        self.assertEqual(data["pages"], 1)
        self.assertEqual(data["pdf"], 1)
        self.assertEqual(data["urls"], ["/wiki/Cours/Signal", "/fichiers/Cours/poly.pdf", "/pdf/Cours/poly.pdf", "/fichiers/Cours/schema.png"])
        self.assertEqual(self.client.get("/hors-ligne/dossier.json", {"dossier": ""}).json()["pages"], 2)
        self.assertEqual(self.client.get("/hors-ligne/dossier.json", {"dossier": "Vide"}).status_code, 404)
        # Application Android : pas de service worker du site (elle gère son propre hors ligne).
        self.assertNotContains(self.client.get("/wiki/Cours/Signal", HTTP_USER_AGENT="Mozilla/5.0 ProjetPluriApp/2"), 'data-sw=')


class VerificationCoffreTests(WikiTestCase):
    """Le coffre n'est parcouru qu'au plus toutes les WIKI_VERIF_INTERVALLE secondes ;
    ce que le wiki écrit lui-même est visible tout de suite."""

    def test_parcours_espace_et_invalidation(self):
        from unittest import mock

        from wiki import vault as module
        self.write("Une.md", "# Une\n")
        with override_settings(WIKI_VERIF_INTERVALLE=60), mock.patch.object(module, "scan", wraps=module.scan) as scan:
            module.invalider()
            self.assertIn("une", module.get_vault().notes)
            self.write("Deux.md", "# Deux\n")
            from wiki.quiz import get_library
            get_library()
            self.assertNotIn("deux", module.get_vault().notes)  # pas encore revu
            self.assertEqual(scan.call_count, 1)                 # pages et QCM : un seul parcours
            module.invalider()
            self.assertIn("deux", module.get_vault().notes)
            self.assertEqual(scan.call_count, 2)
            self.write("Trois.md", "# Trois\n")
            with module.toujours_verifier():
                self.assertIn("trois", module.get_vault().notes)

    def test_ecriture_par_le_wiki_visible_tout_de_suite(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from wiki import vault as module
        admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(admin)
        with override_settings(WIKI_VERIF_INTERVALLE=60):
            module.invalider()
            self.client.get("/sommaire/")
            r = self.client.post("/importer/", {"fichiers": SimpleUploadedFile("Nouvelle.md", b"# Nouvelle\n"),
                                                "chemins": "Nouvelle.md"}, HTTP_ACCEPT="application/json")
            self.assertEqual(r.json()["results"][0]["url"], "/wiki/Nouvelle")  # relu pendant la requête
            self.assertContains(self.client.get("/sommaire/"), "Nouvelle")       # et juste après


class ErreursServeurTests(WikiTestCase):
    def test_erreur_500_notee_et_regroupee(self):
        from unittest import mock

        from wiki.models import ErreurServeur
        client = self.client_class(raise_request_exception=False)
        client.force_login(self.reader)
        with mock.patch("wiki.views.get_vault", side_effect=RuntimeError("disque illisible")):
            self.assertEqual(client.get("/sommaire/").status_code, 500)
            client.get("/sommaire/?x=1")
        e = ErreurServeur.objects.get()
        self.assertEqual((e.type, e.message, e.nombre, e.methode, e.utilisateur), ("RuntimeError", "disque illisible", 2, "GET", "lecteur"))
        self.assertEqual(e.chemin, "/sommaire/?x=1")
        self.assertIn("Traceback", e.trace)
        self.assertIn("wiki/views.py", e.lieu)
        # Page réservée aux admins, badge dans le menu.
        self.assertEqual(self.client.get("/erreurs/").status_code, 403)
        admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(admin)
        page = self.client.get("/erreurs/")
        self.assertContains(page, "disque illisible")
        self.assertContains(page, "2 fois")
        self.assertContains(self.client.get("/sommaire/"), 'class="badge-erreurs">1<')
        self.client.post("/erreurs/", {"action": "reglee", "pk": e.pk})
        self.assertTrue(ErreurServeur.objects.get().reglee)
        self.assertNotContains(self.client.get("/sommaire/"), "badge-erreurs")
        self.client.post("/erreurs/", {"action": "effacer"})
        self.assertFalse(ErreurServeur.objects.exists())

    def test_noter_hors_requete_et_limite(self):
        from wiki import erreurs
        from wiki.models import ErreurServeur
        for i in range(erreurs.MAX_ERREURS + 3):
            try:
                raise ValueError(f"erreur {i}")
            except ValueError:
                erreurs.noter("Fil des travaux de Claude")
        self.assertEqual(ErreurServeur.objects.count(), erreurs.MAX_ERREURS)
        self.assertEqual(ErreurServeur.objects.order_by("-derniere").first().chemin, "Fil des travaux de Claude")
        erreurs.noter("rien")  # aucune exception en cours : rien à noter
        self.assertEqual(ErreurServeur.objects.count(), erreurs.MAX_ERREURS)


class ProductionTests(WikiTestCase):
    def test_gunicorn_impression_dependabot(self):
        import runpy

        import yaml
        from django.conf import settings
        conf = runpy.run_path(str(settings.BASE_DIR / "config" / "gunicorn.conf.py"))
        self.assertEqual((conf["workers"], conf["worker_class"]), (1, "gthread"))
        self.assertGreaterEqual(conf["threads"], 2)
        self.write("Fiche.md", "# Fiche\n")
        page = self.client.get("/wiki/Fiche").content.decode()
        self.assertIn("data-imprimer", page)
        css = (settings.BASE_DIR / "wiki" / "static" / "wiki" / "wiki.css").read_text(encoding="utf-8")
        self.assertIn("@media print", css)
        deps = yaml.safe_load((settings.BASE_DIR / ".github" / "dependabot.yml").read_text(encoding="utf-8"))
        self.assertEqual({u["package-ecosystem"] for u in deps["updates"]}, {"uv", "gradle", "github-actions"})
