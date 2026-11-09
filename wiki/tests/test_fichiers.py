"""Import de fichiers, PDF (lecteur, annotations), cours LaTeX, images allégées."""

import json
import tempfile
from pathlib import Path
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from wiki.vault import get_vault

from .base import WikiTestCase


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
        self.assertContains(response, 'src="/static/wiki/lecteur_pdf.js?v=')
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
        from wiki.latex import convert

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
        from wiki.latex import convert

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
        from wiki.latex import looks_like_latex

        self.assertTrue(looks_like_latex(LATEX_COURSE))
        self.assertFalse(looks_like_latex(r"$$\frac{a}{b}$$"))


class ImagesAllegeesTests(WikiTestCase):
    """Images réduites et recompressées à l'import, sous le même nom."""

    def _jpeg(self, largeur, hauteur):
        import io

        from PIL import Image
        image = Image.linear_gradient("L").resize((largeur, hauteur)).convert("RGB")
        tampon = io.BytesIO()
        image.save(tampon, "JPEG", quality=98)
        return tampon.getvalue()

    def test_grande_photo_reduite(self):
        from PIL import Image

        from wiki import uploads
        chemin = self.root / "photo.jpg"
        chemin.write_bytes(self._jpeg(3000, 1500))
        avant = chemin.stat().st_size
        gain = uploads.alleger_image(chemin)
        self.assertIsNotNone(gain)
        self.assertEqual(gain[0], avant)
        self.assertLess(gain[1], avant)
        with Image.open(chemin) as image:
            self.assertEqual(image.size, (2000, 1000))
        # Petite image déjà compressée, GIF, fichier corrompu : gardés tels quels.
        petite = self.root / "icone.png"
        Image.new("RGB", (40, 40), "red").save(petite, optimize=True)
        self.assertIsNone(uploads.alleger_image(petite))
        gif = self.root / "anim.gif"
        gif.write_bytes(b"GIF89a")
        self.assertIsNone(uploads.alleger_image(gif))
        casse = self.root / "casse.jpg"
        casse.write_bytes(b"pas une image")
        self.assertIsNone(uploads.alleger_image(casse))
        self.assertEqual(casse.read_bytes(), b"pas une image")
        self.assertEqual(uploads.taille_lisible(3 * 1024 * 1024), "3,0 Mo")

    def test_import_signale_le_gain(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(admin)
        r = self.client.post("/importer/", {"fichiers": SimpleUploadedFile("photo.jpg", self._jpeg(2600, 2600)),
                                            "chemins": "photo.jpg", "dossier": "images"}, HTTP_ACCEPT="application/json")
        resultat = r.json()["results"][0]
        self.assertTrue(resultat["ok"], resultat)
        self.assertIn("image allégée", resultat["message"])
        self.assertTrue((self.root / "images" / "photo.jpg").is_file())


class AnnotationPdfTests(WikiTestCase):
    """Passage d'un PDF → carte de révision ou citation dans une page (admins)."""

    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(self.admin)
        self.write("Cours/Signal.pdf", "%PDF-1.4")
        self.versions = tempfile.TemporaryDirectory()
        self.addCleanup(self.versions.cleanup)
        override = override_settings(DATA_DIR=Path(self.versions.name))
        override.enable()
        self.addCleanup(override.disable)

    def _poster(self, **data):
        import json
        return self.client.post("/pdf-annotation/", data=json.dumps({"pdf": "Cours/Signal.pdf", "page": 3,
                                                                      "texte": "Le théorème de Shannon impose f_e > 2 f_max.", **data}),
                                content_type="application/json")

    def test_carte(self):
        import json

        from wiki.quiz import get_library
        page = self.client.get("/pdf/Cours/Signal.pdf")
        self.assertContains(page, 'data-can-edit="1"')
        self.assertContains(page, 'id="pdf-annotation-dialog"')
        r = self._poster(cible="carte", recto="Que dit Shannon ?")
        self.assertEqual(r.status_code, 200, r.content)
        self.assertIn("Carte ajoutée", r.json()["message"])
        data = json.loads((self.root / "QCM" / "Annotations" / "Signal.json").read_text(encoding="utf-8"))
        self.assertEqual(data["titre"], "Signal — annotations")
        self.assertEqual(data["questions"][0]["question"], "Que dit Shannon ?")
        self.assertIn("— *Signal, p. 3*", data["questions"][0]["verso"])
        self.assertNotIn("source_page", data)
        self._poster(cible="carte", texte="Autre passage", recto="")
        data = json.loads((self.root / "QCM" / "Annotations" / "Signal.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["questions"]), 2)
        self.assertEqual(data["questions"][1]["question"], "Signal, p. 3 : que dit ce passage ?")
        self.assertEqual(len(get_library().get("QCM/Annotations/Signal").questions), 2)
        self.assertEqual(self._poster(cible="carte", texte="   ").status_code, 400)
        self.assertEqual(self._poster(cible="carte", pdf="Nope.pdf").status_code, 404)

    def test_citation_dans_une_page(self):
        from wiki import historique
        self.write("Cours/Signal.md", "# Signal\n\nIntro.\n")
        r = self._poster(cible="note")  # page du cours par défaut (même nom que le PDF)
        self.assertEqual(r.json()["url"], "/wiki/Cours/Signal")
        texte = (self.root / "Cours" / "Signal.md").read_text(encoding="utf-8")
        self.assertTrue(texte.endswith("Intro.\n\n> [!quote] Signal, p. 3\n> Le théorème de Shannon impose f_e > 2 f_max.\n> — [[Signal.pdf]]\n"))
        self.assertEqual(len(historique.lister("Cours/Signal.md")), 1)
        # Page nommée, créée au besoin.
        r = self._poster(cible="note", page_wiki="Notes/Citations")
        self.assertEqual(r.json()["url"], "/wiki/Notes/Citations")
        self.assertTrue((self.root / "Notes" / "Citations.md").read_text(encoding="utf-8").startswith("# Citations\n\n> [!quote]"))
        # La page du PDF reçoit la citation (source_page du set d'annotations).
        self._poster(cible="carte")
        import json
        self.assertEqual(json.loads((self.root / "QCM" / "Annotations" / "Signal.json").read_text(encoding="utf-8"))["source_page"], "Cours/Signal")

    def test_reserve_aux_admins(self):
        self.client.force_login(self.reader)
        self.assertEqual(self._poster(cible="carte").status_code, 403)
        page = self.client.get("/pdf/Cours/Signal.pdf")
        self.assertNotContains(page, "data-can-edit")
        self.assertNotContains(page, "pdf-annotation-dialog")
