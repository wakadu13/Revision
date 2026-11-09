"""Fonctions qui passent par Claude (faux client, sans réseau) : transformations, génération,
cartes d'une page, variantes, réponses rédigées, lots, tuteur, « Demander au wiki »,
recherche dans les PDF, graphe, copie photographiée."""

import base64
import json
import tempfile
from pathlib import Path
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from wiki import claude_demandes, quiz
from wiki.vault import get_vault

from .base import QuizBase, WikiTestCase, _FauxClaude, _FauxLots, _pdf_texte


@override_settings(WIKI_CLAUDE_FIL=False)
@mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": "sk-ant-test", "ANTHROPIC_API_KEY": "", "WIKI_CLAUDE_MODELE": "", "WIKI_CLAUDE_EFFORT": ""})
class ClaudeTests(WikiTestCase):
    """Cours (PDF, LaTeX) transformés en pages par Claude, avec un faux client."""

    PDF = b"%PDF-1.4\n%%EOF\n"

    def setUp(self):
        super().setUp()
        from wiki import claude

        self.claude = claude
        claude._repris = False
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(self.admin)

    def upload(self, files, **extra):
        data = {
            "fichiers": [SimpleUploadedFile(name.rsplit("/", 1)[-1], body) for name, body in files],
            "chemins": [name for name, _ in files],
            **extra,
        }
        return self.client.post("/importer/", data, HTTP_ACCEPT="application/json")

    def traiter(self, faux):
        with mock.patch.object(self.claude, "_client", return_value=faux):
            self.claude.traiter_en_attente()

    def test_pdf_import_becomes_course_page(self):
        from wiki.models import Transformation

        self.assertContains(self.client.get("/importer/"), 'name="claude"')
        results = self.upload([("Cours/Signal.pdf", self.PDF)], dossier="", claude="1").json()["results"]
        self.assertEqual(results[0]["claude"], "/transformations/")
        self.assertIn("Claude", results[0]["message"])
        t = Transformation.objects.get()
        self.assertEqual((t.source, t.page, t.statut), ("Cours/Signal.pdf", "Cours/Signal.md", "attente"))

        faux = _FauxClaude()
        self.traiter(faux)
        t.refresh_from_db()
        self.assertEqual(t.statut, "fait", t.message)
        self.assertEqual(t.page_ecrite, "Cours/Signal.md")
        page = (self.root / "Cours/Signal.md").read_text(encoding="utf-8")
        self.assertTrue(page.startswith("---\ntags: [cours]\n---\n# Cours"))
        self.assertIn("## Document d'origine\n\n![[Signal.pdf]]", page)
        self.assertEqual((t.jetons_entree, t.jetons_sortie), (1000, 500))
        demande = faux.demandes[0]
        self.assertEqual(demande["model"], "claude-opus-5-5")
        self.assertEqual(demande["fallbacks"], "default")
        self.assertEqual(demande["betas"], ["server-side-fallback-2026-07-01"])
        self.assertEqual(demande["output_config"], {"effort": "medium"})
        self.assertEqual(demande["max_tokens"], 128000)
        self.assertIn("Markdown d'Obsidian", demande["system"])
        document = demande["messages"][0]["content"][0]
        self.assertEqual(document["type"], "document")
        self.assertEqual(document["source"]["media_type"], "application/pdf")
        self.assertEqual(base64.b64decode(document["source"]["data"]), self.PDF)
        # Suivi : page écrite et coût estimé (1000 × 4 $ + 500 × 20 $ par million de jetons).
        suivi = self.client.get("/transformations/").content.decode()
        self.assertIn('href="/wiki/Cours/Signal"', suivi)
        self.assertRegex(suivi, r"environ 0[,.]01 \$")
        self.assertNotIn('http-equiv="refresh"', suivi)
        # Le PDF mène à sa page de cours.
        self.assertContains(self.client.get("/pdf/Cours/Signal.pdf"), "Page du cours")

    def test_latex_import_replaces_local_conversion(self):
        from wiki.models import Transformation

        tex = rb"\documentclass{article}\begin{document}\section{Intro}Bonjour $x$.\end{document}"
        self.upload([("Analyse.tex", tex)], claude="1")
        locale = (self.root / "Analyse.md").read_text(encoding="utf-8")
        self.assertIn("Intro", locale)  # conversion sur place, en attendant Claude
        faux = _FauxClaude(texte="# Analyse\n\nVersion de Claude.")
        self.traiter(faux)
        self.assertEqual(Transformation.objects.get().statut, "fait")
        self.assertEqual((self.root / "Analyse.md").read_text(encoding="utf-8"), "# Analyse\n\nVersion de Claude.\n")
        bloc = faux.demandes[0]["messages"][0]["content"][0]
        self.assertEqual(bloc["type"], "text")
        self.assertIn(r"\section{Intro}", bloc["text"])

    def test_page_edited_meanwhile_is_kept(self):
        tex = rb"\documentclass{article}\begin{document}Texte\end{document}"
        self.upload([("Cours.tex", tex)], claude="1")
        self.write("Cours.md", "Mes notes à moi")
        self.traiter(_FauxClaude(texte="# Version Claude"))
        self.assertEqual((self.root / "Cours.md").read_text(encoding="utf-8"), "Mes notes à moi")
        self.assertEqual((self.root / "Cours (Claude).md").read_text(encoding="utf-8"), "# Version Claude\n")

    def test_without_api_key_nothing_is_sent(self):
        from wiki.models import Transformation

        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": ""}):
            self.assertNotContains(self.client.get("/importer/"), 'name="claude"')
            self.upload([("Signal.pdf", self.PDF)], claude="1")
            self.assertFalse(Transformation.objects.exists())
            self.assertContains(self.client.get("/transformations/"), "réglages de Claude")
            self.assertNotContains(self.client.get("/pdf/Signal.pdf"), "Créer une page de cours avec Claude")

    def test_unchecked_box_or_editor_upload_do_nothing(self):
        from wiki.models import Transformation

        self.upload([("A.pdf", self.PDF)])
        self.write("Note.md", "x")
        self.upload([("B.pdf", self.PDF)], pour_note="Note", claude="1")
        self.assertFalse(Transformation.objects.exists())

    def test_errors_are_reported_and_can_be_retried(self):
        import anthropic
        import httpx2

        from wiki.models import Transformation

        requete = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
        self.upload([("Signal.pdf", self.PDF)], claude="1")
        refus = anthropic.AuthenticationError("invalid x-api-key", response=httpx2.Response(401, request=requete), body=None)
        self.traiter(_FauxClaude(erreur=refus))
        t = Transformation.objects.get()
        self.assertEqual(t.statut, "erreur")
        self.assertIn("Clé d'API refusée", t.message)
        self.assertFalse((self.root / "Signal.md").exists())
        self.assertContains(self.client.get("/transformations/"), "Relancer")
        self.client.post("/transformations/", {"relancer": t.pk})
        t.refresh_from_db()
        self.assertEqual(t.statut, "attente")
        self.traiter(_FauxClaude(erreur=anthropic.APIConnectionError(request=requete)))
        t.refresh_from_db()
        self.assertIn("injoignable", t.message)
        # Crédits du mois épuisés (abonnement Max : 100 $ par mois) : message clair.
        self.client.post("/transformations/", {"relancer": t.pk})
        epuise = anthropic.BadRequestError(
            "Your credit balance is too low to access the Anthropic API. Please go to Plans & Billing to upgrade or purchase credits.",
            response=httpx2.Response(400, request=requete), body=None)
        self.traiter(_FauxClaude(erreur=epuise))
        t.refresh_from_db()
        self.assertIn("Plus de crédits d'API", t.message)

    def test_refusal_and_truncated_page(self):
        from wiki.models import Transformation

        self.upload([("A.pdf", self.PDF)], claude="1")
        self.traiter(_FauxClaude(stop="refusal", texte=""))
        self.assertEqual(Transformation.objects.get().statut, "erreur")
        self.upload([("B.pdf", self.PDF)], claude="1")
        self.traiter(_FauxClaude(stop="max_tokens", texte="# B\n\nDébut"))
        t = Transformation.objects.get(source="B.pdf")
        self.assertEqual(t.statut, "fait")
        self.assertIn("fin de la page manque", t.message)
        self.assertIn("> [!warning]", (self.root / "B.md").read_text(encoding="utf-8"))

    def test_large_pdf_goes_through_files_api(self):
        self.upload([("Gros.pdf", self.PDF)], claude="1")
        faux = _FauxClaude()
        with mock.patch.object(self.claude, "PDF_EN_LIGNE_MAX", 4):
            self.traiter(faux)
        self.assertEqual(faux.envois[0][0], "Gros.pdf")
        self.assertEqual(faux.demandes[0]["messages"][0]["content"][0]["source"], {"type": "file", "file_id": "file_1"})
        self.assertEqual(faux.suppressions, ["file_1"])

    def test_existing_pdf_button_and_permissions(self):
        from wiki.models import Transformation

        self.write("Vieux.pdf", "%PDF-1.4\n%%EOF\n")
        self.assertContains(self.client.get("/pdf/Vieux.pdf"), "Créer une page de cours avec Claude")
        self.client.post("/transformations/", {"pdf": "Vieux.pdf"})
        self.client.post("/transformations/", {"pdf": "Vieux.pdf"})  # déjà en attente : pas de doublon
        self.assertEqual(Transformation.objects.filter(source="Vieux.pdf").count(), 1)
        self.assertContains(self.client.get("/transformations/"), 'http-equiv="refresh"')
        self.assertEqual(self.client.post("/transformations/", {"pdf": "../secret.pdf"}).status_code, 404)
        self.client.force_login(self.reader)
        self.assertEqual(self.client.get("/transformations/").status_code, 403)
        self.assertEqual(self.client.post("/transformations/", {"pdf": "Vieux.pdf"}).status_code, 403)
        self.assertNotContains(self.client.get("/pdf/Vieux.pdf"), "Créer une page de cours avec Claude")

    def test_interrupted_job_resumes_and_model_setting(self):
        from wiki.models import Transformation

        self.write("A.pdf", "%PDF-1.4\n%%EOF\n")
        Transformation.objects.create(source="A.pdf", page="A.md", statut="en_cours")
        faux = _FauxClaude()
        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_MODELE": "claude-haiku-5-5"}):
            self.traiter(faux)
        self.assertEqual(Transformation.objects.get().statut, "fait")
        # Modèle sans repli automatique : pas de paramètre « fallbacks ».
        self.assertEqual(faux.demandes[0]["model"], "claude-haiku-5-5")
        self.assertNotIn("fallbacks", faux.demandes[0])

    def test_key_variable_names(self):
        # Clé propre au wiki d'abord (Claude Code garde l'abonnement), ANTHROPIC_API_KEY sinon.
        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": "", "ANTHROPIC_API_KEY": "sk-ant-globale"}):
            self.assertEqual(self.claude.cle(), "sk-ant-globale")
        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": " sk-ant-wiki ", "ANTHROPIC_API_KEY": "sk-ant-globale"}):
            self.assertEqual(self.claude.cle(), "sk-ant-wiki")
            with mock.patch("anthropic.Anthropic") as client:
                self.claude._client()
            self.assertEqual(client.call_args.kwargs["api_key"], "sk-ant-wiki")

    CLE = "sk-ant-api03-" + "A1b2C3d4E5f6G7h8I9j0" * 3 + "wxyz"

    def test_settings_page_saves_checked_key_without_showing_it(self):
        from wiki.models import ReglagesClaude

        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": ""}):
            page = self.client.get("/claude/reglages/").content.decode()
            self.assertIn("Pas encore de clé", page)
            self.assertIn('href="/claude/reglages/"', self.client.get("/sommaire/").content.decode())  # menu des admins
            with mock.patch.object(self.claude, "verifier", return_value=(True, None)) as verifier:
                self.client.post("/claude/reglages/", {"cle": f"  {self.CLE} ", "modele": "claude-sonnet-5-5"})
            verifier.assert_called_once_with(self.CLE, "claude-sonnet-5-5")
            reglages = ReglagesClaude.charger()
            self.assertEqual((reglages.cle, reglages.modele, reglages.modifie_par), (self.CLE, "claude-sonnet-5-5", "admin"))
            self.assertEqual((self.claude.cle(), self.claude.modele()), (self.CLE, "claude-sonnet-5-5"))
            self.assertTrue(self.claude.disponible())
            page = self.client.get("/claude/reglages/").content.decode()
            self.assertIn("Clé enregistrée", page)
            self.assertIn("sk-ant-api…wxyz", page)
            self.assertNotIn(self.CLE, page)
            self.assertNotIn(self.CLE, self.client.get("/transformations/").content.decode())
            self.assertContains(self.client.get("/importer/"), 'name="claude"')
            # Changer seulement de modèle garde la clé, sans nouvelle vérification.
            with mock.patch.object(self.claude, "verifier") as verifier:
                self.client.post("/claude/reglages/", {"cle": "", "modele": "claude-opus-5-5"})
            verifier.assert_not_called()
            self.assertEqual((self.claude.cle(), self.claude.modele()), (self.CLE, "claude-opus-5-5"))
            # Supprimer.
            self.client.post("/claude/reglages/", {"action": "supprimer"})
            self.assertEqual(ReglagesClaude.charger().cle, "")
            self.assertFalse(self.claude.disponible())

    def test_settings_page_rejects_bad_keys(self):
        from wiki.models import ReglagesClaude

        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": ""}):
            reponse = self.client.post("/claude/reglages/", {"cle": "mot-de-passe", "modele": "claude-opus-5-5"}, follow=True)
            self.assertContains(reponse, "commence par sk-ant-")
            with mock.patch.object(self.claude, "verifier", return_value=(False, "Clé refusée par Anthropic")):
                reponse = self.client.post("/claude/reglages/", {"cle": self.CLE, "modele": "claude-opus-5-5"}, follow=True)
            self.assertContains(reponse, "Clé refusée par Anthropic")
            self.assertEqual(ReglagesClaude.charger().cle, "")
            reponse = self.client.post("/claude/reglages/", {"cle": "", "modele": "gpt-9"}, follow=True)
            self.assertContains(reponse, "Modèle inconnu")
            # Vérification impossible (réseau) : enregistrée, avec un avertissement.
            with mock.patch.object(self.claude, "verifier", return_value=(None, "Vérification impossible pour l'instant.")):
                reponse = self.client.post("/claude/reglages/", {"cle": self.CLE, "modele": "claude-opus-5-5"}, follow=True)
            self.assertContains(reponse, "enregistrée quand même")
            self.assertEqual(ReglagesClaude.charger().cle, self.CLE)

    def test_site_key_wins_over_environment_and_admins_only(self):
        from wiki.models import ReglagesClaude

        self.assertContains(self.client.get("/claude/reglages/"), "variables d'environnement")
        ReglagesClaude.objects.create(pk=1, cle=self.CLE)
        self.assertEqual(self.claude.cle(), self.CLE)
        self.client.force_login(self.reader)
        self.assertEqual(self.client.get("/claude/reglages/").status_code, 403)
        self.assertEqual(self.client.post("/claude/reglages/", {"action": "supprimer"}).status_code, 403)
        self.assertNotIn('href="/claude/reglages/"', self.client.get("/sommaire/").content.decode())
        self.assertEqual(ReglagesClaude.charger().cle, self.CLE)
        self.client.logout()
        self.assertEqual(self.client.get("/claude/reglages/").status_code, 302)

    def test_verifier_asks_anthropic(self):
        import anthropic
        import httpx2

        requete = httpx2.Request("GET", "https://api.anthropic.com/v1/models/claude-opus-5-5")
        cas = [
            (None, (True, None)),
            (anthropic.AuthenticationError("bad", response=httpx2.Response(401, request=requete), body=None), False),
            (anthropic.NotFoundError("no", response=httpx2.Response(404, request=requete), body=None), False),
            (anthropic.APIConnectionError(request=requete), None),
        ]
        for erreur, attendu in cas:
            with self.subTest(erreur=type(erreur).__name__), mock.patch("anthropic.Anthropic") as client:
                if erreur is not None:
                    client.return_value.models.retrieve.side_effect = erreur
                resultat = self.claude.verifier(self.CLE, "claude-opus-5-5")
                self.assertEqual(client.call_args.kwargs["api_key"], self.CLE)
                client.return_value.models.retrieve.assert_called_once_with("claude-opus-5-5")
                if isinstance(attendu, tuple):
                    self.assertEqual(resultat, attendu)
                else:
                    self.assertIs(resultat[0], attendu)
                    self.assertTrue(resultat[1])

    def _qcm_json(self):
        return json.dumps({
            "titre": "Signal — échantillonnage", "description": "Shannon et repliement.",
            "questions": [
                {"type": "QCM", "question": "Fréquence minimale d'échantillonnage ?", "choix": ["f", "2 f_max", "f/2", "4 f"],
                 "reponses": [1], "reponses_texte": [], "consigne": "", "verso": "", "explication": "Shannon."},
                {"type": "QCR", "question": "Effets d'un sous-échantillonnage ?", "choix": ["repliement", "bruit", "perte", "rien"],
                 "reponses": [0, 2], "reponses_texte": [], "consigne": "", "verso": "", "explication": ""},
                {"type": "TROU", "question": "Le _____ apparaît si f_e < 2 f_max.", "choix": [], "reponses": [],
                 "reponses_texte": ["repliement", "aliasing"], "consigne": "", "verso": "", "explication": ""},
                {"type": "QCM", "question": "Question mal formée", "choix": ["a", "b"], "reponses": [7],
                 "reponses_texte": [], "consigne": "", "verso": "", "explication": ""},
                {"type": "FLASHCARD", "question": "Théorème de Shannon", "choix": [], "reponses": [], "reponses_texte": [],
                 "consigne": "", "verso": "f_e > 2 f_max", "explication": ""},
            ]})

    def test_generate_qcm_from_course_page(self):
        from wiki.models import Transformation

        self.write("Cours/Signal.md", "# Signal\n\nThéorème de Shannon : f_e > 2 f_max.")
        page = self.client.get("/wiki/Cours/Signal").content.decode()
        self.assertIn("Générer un QCM (20 questions)", page)
        index = self.client.get("/qcm/").content.decode()
        self.assertIn('id="generer"', index)
        self.assertIn('<option value="Cours/Signal">Signal</option>', index)
        self.client.post("/qcm/generer/", {"genre": "qcm", "page": "Cours/Signal", "nombre": "10", "publier": "1"})
        t = Transformation.objects.get()
        self.assertEqual((t.genre, t.source, t.options["categorie"], t.options["nombre"]), ("qcm", "Cours/Signal.md", "Cours", 10))
        self.assertTrue(t.options["publier"])

        faux = _FauxClaude(texte=self._qcm_json())
        self.traiter(faux)
        t.refresh_from_db()
        self.assertEqual(t.statut, "fait", t.message)
        self.assertEqual(t.page_ecrite, "QCM/Cours/signal-echantillonnage.json")
        self.assertIn("1 question mal formée écartée", t.message)
        demande = faux.demandes[0]
        self.assertEqual(demande["output_config"]["format"]["type"], "json_schema")
        self.assertEqual(demande["max_tokens"], 64000)
        textes = [b["text"] for b in demande["messages"][0]["content"]]
        self.assertIn("Théorème de Shannon", textes[0])
        self.assertEqual(textes[1], "Écris 10 questions sur ce cours.")
        donnees = json.loads((self.root / t.page_ecrite).read_text(encoding="utf-8"))
        self.assertEqual(donnees["source_page"], "Cours/Signal")
        self.assertEqual([q["id"] for q in donnees["questions"]], ["ia001", "ia002", "ia003", "ia005"])
        self.assertNotIn("verso", donnees["questions"][0])  # champs vides retirés
        qset = quiz.get_library().get("QCM/Cours/signal-echantillonnage")
        self.assertEqual(len(qset), 4)
        suivi = self.client.get("/transformations/").content.decode()
        self.assertIn('href="/qcm/jouer/?set=QCM/Cours/signal-echantillonnage&amp;mode=all"', suivi)
        self.assertEqual(self.client.get("/qcm/jouer/?set=QCM/Cours/signal-echantillonnage&mode=all").status_code, 200)

    def test_generate_qcm_from_pasted_text_and_errors(self):
        from wiki.models import Transformation

        reponse = self.client.post("/qcm/generer/", {"genre": "qcm", "page": "", "texte": ""}, follow=True)
        self.assertContains(reponse, "Choisissez une page du wiki")
        reponse = self.client.post("/qcm/generer/", {"genre": "qcm", "page": "Inconnue"}, follow=True)
        self.assertContains(reponse, "Page introuvable")
        reponse = self.client.post("/qcm/generer/", {"genre": "qcm", "texte": "x", "categorie": "a/b"}, follow=True)
        self.assertContains(reponse, "Catégorie invalide")
        self.assertFalse(Transformation.objects.exists())
        self.client.post("/qcm/generer/", {"genre": "qcm", "texte": "Le cours collé", "nombre": "999", "titre": "Mon QCM", "publier": "1"})
        t = Transformation.objects.get()
        self.assertEqual((t.options["nombre"], t.options["categorie"], t.texte_source), (20, "Générés", "Le cours collé"))
        self.traiter(_FauxClaude(texte=self._qcm_json()))
        t.refresh_from_db()
        self.assertEqual(t.page_ecrite, "QCM/Générés/mon-qcm.json")
        self.assertEqual(json.loads((self.root / t.page_ecrite).read_text(encoding="utf-8"))["titre"], "Mon QCM")
        # Réponse coupée (trop de questions) : erreur claire.
        self.client.post("/qcm/generer/", {"genre": "qcm", "texte": "Autre cours", "publier": "1"})
        self.traiter(_FauxClaude(texte='{"titre": "x", "questions": [', stop="max_tokens"))
        self.assertIn("moins de questions", Transformation.objects.latest("pk").message)

    def test_generate_vocabulary_pack(self):
        from wiki.models import Transformation

        index = self.client.get("/qcm/").content.decode()
        self.assertIn('name="cartes" value="decouverte" checked', index)
        self.assertIn('name="cartes" value="production" checked', index)
        self.assertIn('name="cartes" value="reconnaissance">', index)
        self.client.post("/qcm/generer/", {"genre": "vocabulaire", "mots": "un emploi\n\nto achieve\nla cuisine",
                                           "langue": "anglais", "cartes": ["decouverte", "production", "choix"],
                                           "dossier": "Voc perso", "publier": "1"})
        t = Transformation.objects.get()
        self.assertEqual((t.genre, t.texte_source), ("vocabulaire", "un emploi\nto achieve\nla cuisine"))
        self.assertEqual(t.options, {"langue": "Anglais", "exercices": ["decouverte", "production", "choix"],
                                     "dossier": "Voc perso", "titre": "", "publier": True, "lot": False})
        fiches = [
            {"mot": "a job", "traductions": ["un emploi"], "variantes": [], "exemple": "I found a new [job].",
             "exemple_traduction": "J'ai trouvé un nouvel emploi.", "prononciation": "/dʒɒb/", "note": ""},
            {"mot": "to achieve", "traductions": ["réussir", "atteindre"], "variantes": [], "exemple": "",
             "exemple_traduction": "", "prononciation": "/əˈtʃiːv/", "note": "Faux ami : pas « achever »."},
            {"mot": "a kitchen", "traductions": ["une cuisine"], "variantes": [], "exemple": "", "exemple_traduction": "",
             "prononciation": "", "note": ""},
            {"mot": "a job", "traductions": ["un travail"], "variantes": [], "exemple": "", "exemple_traduction": "",
             "prononciation": "", "note": ""},
        ]
        faux = _FauxClaude(texte=json.dumps({"titre": "Travail et maison", "description": "Mots du quotidien.", "vocabulaire": fiches}))
        self.traiter(faux)
        t.refresh_from_db()
        self.assertEqual(t.statut, "fait", t.message)
        self.assertEqual(t.page_ecrite, "QCM/Voc perso/travail-et-maison.json")
        self.assertIn("Mots à préparer en anglais", faux.demandes[0]["messages"][0]["content"][0]["text"])
        self.assertIn("anglais", faux.demandes[0]["system"])
        paquet = json.loads((self.root / t.page_ecrite).read_text(encoding="utf-8"))
        self.assertEqual(paquet["langue"], "Anglais")
        self.assertEqual(paquet["exercices"], ["decouverte", "production", "choix"])
        self.assertEqual(paquet["particules_optionnelles"], ["to", "a", "an", "the"])
        self.assertEqual([f["id"] for f in paquet["vocabulaire"]], ["travail-et-maison-001", "travail-et-maison-002", "travail-et-maison-003"])
        set_langue = quiz.get_library().langues["QCM/Voc perso/travail-et-maison"]
        self.assertEqual(set_langue.exercices[0].id, "travail-et-maison-001#dec")
        # Paquet à part : révisable seul.
        suivi = self.client.get("/transformations/").content.decode()
        self.assertIn("/qcm/langues/Anglais/jouer/?mode=quotidien&amp;fichier=QCM/Voc%20perso/travail-et-maison", suivi)
        jeu = self.client.get("/qcm/langues/Anglais/jouer/", {"mode": "quotidien", "fichier": "QCM/Voc perso/travail-et-maison"})
        self.assertContains(jeu, "Travail et maison")
        self.assertContains(self.client.get("/qcm/langues/Anglais/", {"fichier": "QCM/Voc perso/travail-et-maison"}), "Ce paquet seulement")
        index = self.client.get("/qcm/").content.decode()
        self.assertIn("Réviser ce paquet", index)
        self.assertIn("Cartes : Carte FR → EN · Traduction à taper FR → EN · QCM FR → EN (choisir le bon mot)", index)
        self.assertEqual(self.client.get("/qcm/langues/Anglais/jouer/", {"fichier": "QCM/inconnu"}).status_code, 404)

    def test_vocabulary_form_errors_and_permissions(self):
        from wiki.models import Transformation

        erreurs = [
            ({"mots": "", "cartes": ["production"]}, "Collez au moins un mot"),
            ({"mots": "a", "cartes": []}, "Cochez au moins un type de carte"),
            ({"mots": "a", "cartes": ["production"], "langue": "<script>"}, "Langue invalide"),
            ({"mots": "\n".join(f"mot{i}" for i in range(200)), "cartes": ["production"]}, "Trop de mots"),
            ({"mots": "a", "cartes": ["production"], "dossier": "../x"}, "Dossier invalide"),
        ]
        for donnees, message in erreurs:
            with self.subTest(message=message):
                reponse = self.client.post("/qcm/generer/", {"genre": "vocabulaire", **donnees}, follow=True)
                self.assertContains(reponse, message)
        self.assertFalse(Transformation.objects.exists())
        self.client.force_login(self.reader)
        self.assertEqual(self.client.post("/qcm/generer/", {"genre": "vocabulaire", "mots": "a", "cartes": ["production"]}).status_code, 403)
        self.assertNotIn('id="generer"', self.client.get("/qcm/").content.decode())
        self.write("Cours.md", "x")
        self.assertNotContains(self.client.get("/wiki/Cours"), "Générer un QCM")
        self.client.force_login(self.admin)
        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": ""}):
            self.assertContains(self.client.get("/qcm/"), "ajoutez une clé d'API")
            self.assertRedirects(self.client.post("/qcm/generer/", {"genre": "vocabulaire", "mots": "a", "cartes": ["production"]}),
                                 "/claude/reglages/")

    def test_draft_review_and_publish(self):
        from wiki.models import Transformation

        self.write("Cours/Signal.md", "# Signal\n\nThéorème de Shannon.")
        self.client.post("/qcm/generer/", {"genre": "qcm", "page": "Cours/Signal", "nombre": "10"})
        self.traiter(_FauxClaude(texte=self._qcm_json()))
        t = Transformation.objects.get()
        self.assertEqual((t.statut, t.page_ecrite), ("brouillon", ""))
        self.assertTrue(t.termine)
        self.assertEqual(t.resultat["dossier"], "Cours")
        self.assertEqual(len(t.resultat["contenu"]["questions"]), 4)
        self.assertIn("À relire avant publication", t.message)
        self.assertFalse((self.root / "QCM").exists())
        suivi = self.client.get("/transformations/").content.decode()
        self.assertIn("Relire et publier", suivi)
        self.assertNotIn('http-equiv="refresh"', suivi)  # un brouillon n'est plus « en cours »
        page = self.client.get(f"/transformations/{t.pk}/relire/").content.decode()
        self.assertIn('name="q0-garder"', page)
        self.assertIn('name="q0-bonne" value="1" checked', page)
        self.assertIn('name="q1-bonne-0" value="1" checked', page)  # QCR : cases à cocher
        self.assertIn('value="repliement / aliasing"', page)
        # Relecture : on écarte la 2e question, on corrige la 1re et on vide un choix.
        donnees = {"titre": "Signal relu", "description": "Relu.",
                   "q0-garder": "1", "q0-question": "Fréquence minimale d'échantillonnage (corrigée) ?",
                   "q0-choix-0": "f", "q0-choix-1": "", "q0-choix-2": "f/2", "q0-choix-3": "2 f_max", "q0-bonne": "3",
                   "q0-explication": "Shannon-Nyquist.",
                   "q2-garder": "1", "q2-question": "Le _____ apparaît si f_e < 2 f_max.", "q2-reponses": "repliement / aliasing / recouvrement",
                   "q3-garder": "1", "q3-question": "Théorème de Shannon", "q3-verso": "f_e > 2 f_max (corrigé)"}
        reponse = self.client.post(f"/transformations/{t.pk}/relire/", donnees)
        self.assertRedirects(reponse, "/qcm/jouer/?set=QCM/Cours/signal-relu&mode=all", fetch_redirect_response=False)
        t.refresh_from_db()
        self.assertEqual((t.statut, t.page_ecrite, t.resultat), ("fait", "QCM/Cours/signal-relu.json", None))
        self.assertIn("3 sur 4 gardés", t.message)
        publie = json.loads((self.root / t.page_ecrite).read_text(encoding="utf-8"))
        self.assertEqual([q["id"] for q in publie["questions"]], ["ia001", "ia003", "ia005"])
        q0 = publie["questions"][0]
        self.assertEqual((q0["question"], q0["choix"], q0["reponses"], q0["explication"]),
                         ("Fréquence minimale d'échantillonnage (corrigée) ?", ["f", "f/2", "2 f_max"], [2], "Shannon-Nyquist."))
        self.assertEqual(publie["questions"][1]["reponses_texte"], ["repliement", "aliasing", "recouvrement"])
        self.assertEqual(publie["questions"][2]["verso"], "f_e > 2 f_max (corrigé)")
        self.assertEqual(len(quiz.get_library().get("QCM/Cours/signal-relu")), 3)
        # Déjà publié : la relecture renvoie au suivi.
        self.assertRedirects(self.client.get(f"/transformations/{t.pk}/relire/"), "/transformations/")

    def test_draft_publish_as_is_and_delete(self):
        from wiki.models import Transformation

        self.client.post("/qcm/generer/", {"genre": "vocabulaire", "mots": "a job", "cartes": ["production"]})
        fiches = [{"mot": "a job", "traductions": ["un emploi"], "variantes": [], "exemple": "", "exemple_traduction": "",
                   "prononciation": "", "note": ""}]
        self.traiter(_FauxClaude(texte=json.dumps({"titre": "Travail", "description": "", "vocabulaire": fiches})))
        t = Transformation.objects.get()
        self.assertEqual(t.statut, "brouillon")
        self.client.post("/transformations/", {"publier": t.pk})
        t.refresh_from_db()
        self.assertEqual((t.statut, t.page_ecrite), ("fait", "QCM/Vocabulaire/travail.json"))
        self.assertIn("QCM/Vocabulaire/travail", quiz.get_library().langues)
        # Un second brouillon, supprimé.
        self.client.post("/qcm/generer/", {"genre": "vocabulaire", "mots": "to cook", "cartes": ["production"]})
        self.traiter(_FauxClaude(texte=json.dumps({"titre": "Cuisine", "description": "", "vocabulaire": fiches})))
        t2 = Transformation.objects.latest("pk")
        self.client.post("/transformations/", {"supprimer": t2.pk})
        t2.refresh_from_db()
        self.assertEqual((t2.statut, t2.resultat), ("erreur", None))
        self.assertFalse((self.root / "QCM/Vocabulaire/cuisine.json").exists())
        # Relecture d'un paquet : mot corrigé, fiche écartée.
        self.client.post("/qcm/generer/", {"genre": "vocabulaire", "mots": "a job\nto cook", "cartes": ["production"]})
        deux = fiches + [{"mot": "to cook", "traductions": ["cuisiner"], "variantes": [], "exemple": "", "exemple_traduction": "",
                          "prononciation": "", "note": ""}]
        self.traiter(_FauxClaude(texte=json.dumps({"titre": "Mix", "description": "", "vocabulaire": deux})))
        t3 = Transformation.objects.latest("pk")
        self.client.post(f"/transformations/{t3.pk}/relire/", {"titre": "Mix", "v0-garder": "1", "v0-mot": "a job",
                                                                "v0-traductions": "un emploi ; un travail", "v0-note": "Courant."})
        paquet = json.loads((self.root / "QCM/Vocabulaire/mix.json").read_text(encoding="utf-8"))
        self.assertEqual(paquet["vocabulaire"], [{"id": "mix-001", "mot": "a job", "traductions": ["un emploi", "un travail"], "note": "Courant."}])

    def test_fiche_de_revision(self):
        from wiki.models import Transformation

        self.write("Cours/Signal.md", "# Signal\n\nShannon : $f_e > 2 f_{max}$.")
        page = self.client.get("/wiki/Cours/Signal").content.decode()
        self.assertIn('name="fiche" value="Cours/Signal"', page)
        self.client.post("/transformations/", {"fiche": "Cours/Signal"})
        self.assertContains(self.client.get("/wiki/Cours/Signal"), "Fiche de révision en préparation")
        faux = _FauxClaude(texte="## Définitions\n\n- **Échantillonnage**…\n\n> [!retenir] L'essentiel\n> Shannon.")
        self.traiter(faux)
        t = Transformation.objects.get()
        self.assertEqual((t.genre, t.statut, t.page_ecrite), ("fiche", "fait", "Cours/Signal (Fiche).md"))
        texte = (self.root / "Cours/Signal (Fiche).md").read_text(encoding="utf-8")
        self.assertTrue(texte.startswith("> [!abstract] Fiche de révision de [[Cours/Signal|Signal]]"))
        self.assertIn("fiche de révision", faux.demandes[0]["system"].lower())
        self.assertIn("Shannon", faux.demandes[0]["messages"][0]["content"][0]["text"])
        page = self.client.get("/wiki/Cours/Signal").content.decode()
        self.assertIn("📄 Fiche de révision", page)
        self.assertNotIn('name="fiche"', page)
        self.assertIn("Ouvrir la fiche", self.client.get("/transformations/").content.decode())

    def test_explique_moi(self):
        from wiki.models import Explication

        self.write("Cours/Signal.md", "# Signal\n\nLe théorème de Shannon impose f_e > 2 f_max.")
        self.write("QCM/Cours/signal.json", json.dumps({"titre": "Signal", "source_page": "Cours/Signal", "questions": [
            {"id": "q1", "type": "QCM", "question": "Fréquence minimale ?", "choix": ["f_max", "2 f_max"], "reponses": [1]}]}))
        self.assertContains(self.client.get("/qcm/jouer/?set=QCM/Cours/signal&mode=all"), "data-expliquer-url=\"/qcm/expliquer/\"")
        faux = _FauxClaude(texte="Parce que **Shannon** : il faut $f_e > 2 f_{max}$.")
        with mock.patch.object(self.claude, "_client", return_value=faux):
            r = self.client.post("/qcm/expliquer/", json.dumps({"set_id": "QCM/Cours/signal", "question_id": "q1"}),
                                 content_type="application/json").json()
        self.assertIn("<strong>Shannon</strong>", r["html"])
        self.assertEqual((r["modele"], r["gardee"]), ("claude-haiku-5-5", False))
        demande = faux.demandes[0]
        self.assertEqual((demande["model"], demande["max_tokens"], demande["output_config"]["effort"]), ("claude-haiku-5-5", 1500, "low"))
        self.assertNotIn("fallbacks", demande)
        textes = [b["text"] for b in demande["messages"][0]["content"]]
        self.assertIn("théorème de Shannon impose", textes[0])  # le cours
        self.assertIn("Bonne(s) réponse(s) : B", textes[1])
        self.assertEqual(Explication.objects.count(), 1)
        # Deuxième demande : servie depuis la base, sans appel.
        faux2 = _FauxClaude(texte="autre")
        with mock.patch.object(self.claude, "_client", return_value=faux2):
            r = self.client.post("/qcm/expliquer/", json.dumps({"set_id": "QCM/Cours/signal", "question_id": "q1"}),
                                 content_type="application/json").json()
        self.assertTrue(r["gardee"])
        self.assertEqual(faux2.demandes, [])
        # Lecteur simple : autorisé ; question inconnue : 404 ; examen : pas de bouton.
        self.client.force_login(self.reader)
        self.assertEqual(self.client.post("/qcm/expliquer/", json.dumps({"set_id": "QCM/Cours/signal", "question_id": "zz"}),
                                          content_type="application/json").status_code, 404)
        self.assertEqual(self.client.post("/qcm/expliquer/", json.dumps({"set_id": "QCM/Cours/signal", "question_id": "q1"}),
                                          content_type="application/json").status_code, 200)
        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": ""}):
            self.assertNotContains(self.client.get("/qcm/jouer/?set=QCM/Cours/signal&mode=all"), "data-expliquer-url")

    def test_ameliorer_la_redaction(self):
        self.write("Accueil.md", "x")
        self.assertContains(self.client.get("/modifier/Accueil"), 'data-action="ameliorer"')
        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": ""}):
            self.assertNotContains(self.client.get("/modifier/Accueil"), 'data-action="ameliorer"')
        faux = _FauxClaude(texte="```markdown\nUn texte **corrigé**.\n```")
        with mock.patch.object(self.claude, "_client", return_value=faux):
            r = self.client.post("/claude/ameliorer/", {"texte": "Un texte **corigé**."}).json()
        self.assertEqual(r["texte"], "Un texte **corrigé**.")
        self.assertEqual(faux.demandes[0]["output_config"]["effort"], "low")
        self.assertIn("balisage", faux.demandes[0]["system"])
        self.assertEqual(self.client.post("/claude/ameliorer/", {"texte": ""}).status_code, 400)
        self.assertEqual(self.client.post("/claude/ameliorer/", {"texte": "x" * 20000}).status_code, 400)
        self.client.force_login(self.reader)
        self.assertEqual(self.client.post("/claude/ameliorer/", {"texte": "x"}).status_code, 403)

    def test_unwraps_markdown_fence(self):
        self.assertEqual(self.claude._sans_cadre("```markdown\n# Titre\n\nTexte\n```"), "# Titre\n\nTexte")
        self.assertEqual(self.claude._sans_cadre("# Titre\n```py\nx\n```"), "# Titre\n```py\nx\n```")


class CartesPageTests(TestCase):
    """Cartes tirées des encadrés et surlignages d'une page, sans Claude."""

    def setUp(self):
        QuizBase.setUp(self)

    MD = ("---\ntags: [x]\n---\n# Signal\n\n> [!definition] Échantillonnage\n> Prélèvement ==régulier== d'un signal.\n\n"
          "La fréquence de ==Nyquist== vaut $f_e/2$ et le ==repliement== apparaît au-delà.\n\n"
          "> [!warning] Piège\n> Rien.\n\n```python\n==pas une carte==\n```\n\n> [!theoreme]\n> Sans titre : pas de carte.\n")

    def test_extraction(self):
        from wiki import cartes
        qs = cartes.extraire(self.MD)
        types = [(q["type"], q["question"]) for q in qs]
        self.assertEqual(types[0], ("FLASHCARD", "Définition : Échantillonnage"))
        self.assertEqual(qs[0]["verso"], "Prélèvement **régulier** d'un signal.")
        self.assertIn(("TROU", "Prélèvement _____ d'un signal."), types)
        self.assertIn(("TROU", "La fréquence de _____ vaut $f_e/2$ et le repliement apparaît au-delà."), types)
        self.assertIn(("TROU", "La fréquence de Nyquist vaut $f_e/2$ et le _____ apparaît au-delà."), types)
        self.assertEqual(len(qs), 4)
        self.assertEqual(qs[2]["reponses_texte"], ["Nyquist"])
        self.assertEqual(qs, cartes.extraire(self.MD))  # identifiants stables
        self.assertTrue(all(q["id"].startswith("c") and len(q["id"]) == 11 for q in qs))
        self.assertEqual(cartes.extraire("# Rien\n\nTexte sans rien.\n"), [])

    def test_vue(self):
        import json
        (self.root / "Cours").mkdir()
        (self.root / "Cours" / "Signal.md").write_text(self.MD, encoding="utf-8")
        self.assertEqual(self.client.post("/qcm/cartes-de-la-page/", {"page": "Cours/Signal"}).status_code, 403)
        self.user.is_staff = True
        self.user.save()
        self.assertContains(self.client.get("/wiki/Cours/Signal"), "Créer les cartes de la page (4)")
        r = self.client.post("/qcm/cartes-de-la-page/", {"page": "Cours/Signal"}, follow=True)
        self.assertContains(r, "Cartes créées : 4 questions")
        data = json.loads((self.root / "QCM" / "Cours" / "Signal (cartes).json").read_text(encoding="utf-8"))
        self.assertEqual((data["source_page"], len(data["questions"]), data["titre"]), ("Cours/Signal", 4, "Signal — cartes"))
        page = self.client.get("/wiki/Cours/Signal")
        self.assertContains(page, "Mettre à jour les cartes de la page (4)")
        self.assertContains(page, "Signal — cartes")  # listé dans « Réviser ce cours »
        self.assertContains(self.client.get("/qcm/jouer/?set=QCM/Cours/Signal (cartes)&mode=all"), "quiz-data")
        (self.root / "Vide.md").write_text("# Vide\n\nRien.\n", encoding="utf-8")
        self.assertContains(self.client.post("/qcm/cartes-de-la-page/", {"page": "Vide"}, follow=True), "Rien à tirer")
        self.assertNotContains(self.client.get("/wiki/Vide"), "cartes de la page")


@override_settings(WIKI_CLAUDE_FIL=False)
@mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": "sk-ant-test", "ANTHROPIC_API_KEY": "", "WIKI_CLAUDE_MODELE": "", "WIKI_CLAUDE_EFFORT": ""})
class VariantesQrcTests(TestCase):
    """Réponses rédigées corrigées par Claude, variantes des questions ratées, plafond mensuel."""

    def setUp(self):
        import json
        QuizBase.setUp(self)
        from wiki import claude
        self.claude = claude
        claude._repris = False
        self.user.is_staff = True
        self.user.save()
        (self.root / "reseaux" / "qrc.json").write_text(json.dumps({"titre": "QRC", "questions": [
            {"id": "r1", "type": "QRC", "question": "Définir l'échantillonnage.",
             "reponses_texte": ["Prélèvement régulier d'un signal"], "explication": "Voir le cours."}]}), encoding="utf-8")

    def _post_json(self, url, data):
        import json
        return self.client.post(url, data=json.dumps(data), content_type="application/json")

    def test_qrc_corrigee_par_claude(self):
        import json

        from wiki.models import ReglagesClaude, UsageClaude
        faux = _FauxClaude(texte=json.dumps({"verdict": "partiel", "retour": "Il manque la régularité du prélèvement."}))
        with mock.patch.object(self.claude, "_client", return_value=faux):
            r = self._post_json("/qcm/corriger-qrc/", {"set_id": "reseaux/qrc", "question_id": "r1", "reponse": "On prélève le signal"})
        self.assertEqual(r.json(), {"verdict": "partiel", "retour": "Il manque la régularité du prélèvement.",
                                    "correct": False, "modele": "claude-haiku-5-5"})
        demande = faux.demandes[0]
        self.assertEqual(demande["model"], "claude-haiku-5-5")
        self.assertEqual(demande["output_config"]["format"]["schema"], claude_demandes.SCHEMA_QRC)
        self.assertIn("Réponse de l'étudiant : On prélève le signal", demande["messages"][0]["content"][0]["text"])
        self.assertEqual((UsageClaude.objects.get().genre, UsageClaude.objects.get().player), ("qrc", "alice"))
        self.assertGreater(self.claude.cout_a_la_demande_du_mois(), 0)
        self.assertEqual(self._post_json("/qcm/corriger-qrc/", {"set_id": "reseaux/test_set", "question_id": "q-trou", "reponse": "x"}).status_code, 404)
        self.assertContains(self.client.get("/qcm/jouer/?set=reseaux/qrc&mode=all"), "data-corriger-qrc-url")
        # Plafond mensuel atteint : correction stricte côté navigateur.
        reglages = ReglagesClaude.charger()
        reglages.plafond_mensuel = 0.0000001
        reglages.save()
        self.assertEqual(self._post_json("/qcm/corriger-qrc/", {"set_id": "reseaux/qrc", "question_id": "r1", "reponse": "x"}).status_code, 429)
        reglages.plafond_mensuel = 0
        reglages.save()
        self.assertFalse(self.claude.plafond_atteint())

    def test_variantes_des_questions_ratees(self):
        import json

        from wiki.models import Transformation
        r = self.client.post("/qcm/generer/", {"genre": "variantes", "set": "reseaux/test_set"}, follow=True)
        self.assertContains(r, "Aucune question ratée")
        for qid, correct in (("q-qcm", False), ("q-trou", False), ("q-qcr", True)):
            self._post_json("/qcm/reponse/", {"set_id": "reseaux/test_set", "question_id": qid, "correct": correct})
        self.assertContains(self.client.get("/qcm/stats/"), "✦ Variantes")
        r = self.client.post("/qcm/generer/", {"genre": "variantes", "set": "reseaux/test_set"}, follow=True)
        self.assertContains(r, "2 variantes")
        t = Transformation.objects.get()
        self.assertEqual((t.genre, t.nom, sorted(t.options["variantes"])), ("qcm", "Variantes · Set de test", ["q-qcm", "q-trou"]))
        faux = _FauxClaude(texte=json.dumps({"titre": "x", "description": "d", "questions": [
            {"type": "QCM", "question": "3+3 ?", "choix": ["5", "6"], "reponses": [1], "reponses_texte": [], "consigne": "", "verso": "", "explication": ""},
            {"type": "TROU", "question": "Capitale de l'Italie ?", "choix": [], "reponses": [], "reponses_texte": ["Rome"], "consigne": "", "verso": "", "explication": ""},
            {"type": "QCM", "question": "mal formée", "choix": [], "reponses": [], "reponses_texte": [], "consigne": "", "verso": "", "explication": ""}]}))
        with mock.patch.object(self.claude, "_client", return_value=faux):
            self.claude.traiter_en_attente()
        t.refresh_from_db()
        self.assertEqual(t.statut, "brouillon", t.message)
        self.assertIn("1 question mal formée écartée", t.message)
        self.assertEqual(t.resultat["dossier"], "reseaux")
        self.assertEqual(t.resultat["contenu"]["titre"], "Variantes · Set de test")
        self.assertEqual([q["question"] for q in t.resultat["contenu"]["questions"]], ["3+3 ?", "Capitale de l'Italie ?"])
        demande = faux.demandes[0]
        self.assertEqual(demande["system"], self.claude.CONSIGNE_VARIANTES)
        texte = demande["messages"][0]["content"][-1]["text"]
        self.assertIn("2+2 ?", texte)
        self.assertIn("Écris 2 variantes", texte)
        self.assertContains(self.client.get(f"/transformations/{t.pk}/relire/"), "3+3 ?")

    def test_reglage_du_plafond(self):
        from wiki.models import ReglagesClaude
        self.assertContains(self.client.get("/claude/reglages/"), 'name="plafond"')
        self.client.post("/claude/reglages/", {"plafond": "12,5", "modele": "claude-opus-5-5"})
        self.assertEqual(ReglagesClaude.charger().plafond_mensuel, 12.5)
        self.assertContains(self.client.post("/claude/reglages/", {"plafond": "abc"}, follow=True), "Plafond invalide")


@override_settings(WIKI_CLAUDE_FIL=False)
@mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": "sk-ant-test", "ANTHROPIC_API_KEY": "", "WIKI_CLAUDE_MODELE": "", "WIKI_CLAUDE_EFFORT": ""})
class LotsTuteurTests(WikiTestCase):
    """Transformations en lot (Message Batches) et tuteur de la page."""

    PDF = b"%PDF-1.4\n%%EOF\n"

    def setUp(self):
        super().setUp()
        from wiki import claude
        self.claude = claude
        claude._repris = False
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(self.admin)

    def _faux(self, texte="# Cours\n\nContenu.", **lots):
        faux = _FauxClaude(texte)
        faux.lots = _FauxLots(texte, **lots)
        faux.beta.messages.batches = faux.lots
        return faux

    def test_pdf_en_lot(self):
        from wiki.models import Transformation
        r = self.client.post("/importer/", {"fichiers": SimpleUploadedFile("Signal.pdf", self.PDF), "chemins": "Signal.pdf",
                                            "dossier": "Cours", "claude": "1", "lot": "1"}, HTTP_ACCEPT="application/json")
        self.assertIn("dans un lot", r.json()["results"][0]["message"])
        t = Transformation.objects.get()
        self.assertEqual((t.statut, t.options["lot"]), ("attente", True))
        faux = self._faux()
        with mock.patch.object(self.claude, "_client", return_value=faux):
            self.claude.traiter_en_attente()
        t.refresh_from_db()
        self.assertEqual((t.statut, t.lot_id), ("lot", "msgbatch_1"))
        self.assertEqual(faux.demandes, [])  # rien d'envoyé en direct
        creation = faux.lots.creations[0]
        self.assertEqual(creation["requests"][0]["custom_id"], f"t{t.pk}")
        self.assertNotIn("betas", creation["requests"][0]["params"])
        self.assertEqual(creation["betas"], ["server-side-fallback-2026-07-01"])
        self.assertEqual(creation["requests"][0]["params"]["fallbacks"], "default")
        page = self.client.get("/transformations/")
        self.assertContains(page, "Vérifier maintenant")
        self.assertContains(page, "⧗")
        # Lot pas encore traité : rien ne change.
        with mock.patch.object(self.claude, "_client", return_value=faux):
            self.assertEqual(self.claude.verifier_lots(), 0)
        t.refresh_from_db()
        self.assertEqual(t.statut, "lot")
        # Lot terminé : la page est écrite, coût à moitié prix.
        faux.lots.statut = "ended"
        with mock.patch.object(self.claude, "_client", return_value=faux):
            self.assertContains(self.client.post("/transformations/", {"verifier_lots": "1"}, follow=True), "1 travail terminé")
        t.refresh_from_db()
        self.assertEqual((t.statut, t.page_ecrite, t.jetons_entree, t.jetons_sortie), ("fait", "Cours/Signal.md", 2000, 800))
        self.assertTrue((self.root / "Cours" / "Signal.md").read_text(encoding="utf-8").startswith("# Cours"))
        self.assertAlmostEqual(self.claude.cout(t), (2000 * 4.0 + 800 * 20.0) / 1_000_000 * 0.5)
        self.assertContains(self.client.get("/transformations/"), "lot à moitié prix")

    def test_lot_en_echec_et_qcm_en_lot(self):
        from wiki.models import Transformation
        self.write("Cours/Signal.md", "# Signal\n\nShannon.\n")
        r = self.client.post("/qcm/generer/", {"genre": "qcm", "page": "Cours/Signal", "nombre": "10", "lot": "1"}, follow=True)
        self.assertEqual(r.status_code, 200)
        t = Transformation.objects.get()
        self.assertTrue(t.options["lot"])
        faux = self._faux(type_resultat="errored")
        with mock.patch.object(self.claude, "_client", return_value=faux):
            self.claude.traiter_en_attente()
            faux.lots.statut = "ended"
            self.assertEqual(self.claude.verifier_lots(), 1)
        t.refresh_from_db()
        self.assertEqual((t.statut, t.message), ("erreur", "Lot : Quota dépassé"))
        self.assertEqual(faux.lots.creations[0]["requests"][0]["params"]["output_config"]["format"]["schema"], self.claude.SCHEMA_QCM)

    def test_tuteur(self):
        import json

        from wiki.models import EchangeTuteur, UsageClaude
        self.write("Cours/Signal.md", "# Signal\n\nLe théorème de Shannon impose $f_e > 2 f_{max}$.\n")
        page = self.client.get("/wiki/Cours/Signal")
        self.assertContains(page, 'id="tuteur"')
        self.assertContains(page, "tuteur.js")
        faux = _FauxClaude("D'après la page, il faut **échantillonner** à plus de $2 f_{max}$.")
        with mock.patch.object(self.claude, "_client", return_value=faux):
            r = self.client.post("/claude/tuteur/", data=json.dumps({"page": "Cours/Signal", "question": "Pourquoi 2 fois ?"}),
                                 content_type="application/json")
        self.assertEqual(r.status_code, 200, r.content)
        self.assertIn("<strong>échantillonner</strong>", r.json()["html"])
        demande = faux.demandes[0]
        self.assertEqual(demande["model"], "claude-haiku-5-5")
        self.assertIn("Le théorème de Shannon", demande["system"])
        self.assertEqual(demande["messages"], [{"role": "user", "content": "Pourquoi 2 fois ?"}])
        e = EchangeTuteur.objects.get()
        self.assertEqual((e.player, e.page, e.jetons_entree), ("admin", "Cours/Signal", 1000))
        self.assertEqual(UsageClaude.objects.get().genre, "tuteur")
        # Deuxième question : l'échange précédent est rejoué ; l'historique s'affiche dans la page.
        with mock.patch.object(self.claude, "_client", return_value=faux):
            self.client.post("/claude/tuteur/", data=json.dumps({"page": "Cours/Signal", "question": "Et sinon ?"}),
                             content_type="application/json")
        self.assertEqual(len(faux.demandes[1]["messages"]), 3)
        self.assertEqual(faux.demandes[1]["messages"][1]["role"], "assistant")
        self.assertContains(self.client.get("/wiki/Cours/Signal"), "Pourquoi 2 fois ?")
        # Lecteur simple : le tuteur lui est ouvert aussi ; page inconnue : 404 ; plafond : 429.
        self.client.force_login(self.reader)
        with mock.patch.object(self.claude, "_client", return_value=faux):
            self.assertEqual(self.client.post("/claude/tuteur/", data=json.dumps({"page": "Cours/Signal", "question": "?"}),
                                              content_type="application/json").status_code, 200)
        self.assertEqual(self.client.post("/claude/tuteur/", data=json.dumps({"page": "Nope", "question": "?"}),
                                          content_type="application/json").status_code, 404)
        from wiki.models import ReglagesClaude
        reglages = ReglagesClaude.charger()
        reglages.plafond_mensuel = 0.0000001
        reglages.save()
        self.assertEqual(self.client.post("/claude/tuteur/", data=json.dumps({"page": "Cours/Signal", "question": "?"}),
                                          content_type="application/json").status_code, 429)
        self.assertContains(self.client.get("/wiki/Cours/Signal"), "Plafond mensuel de Claude atteint")


@override_settings(WIKI_CLAUDE_FIL=False)
@mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": "sk-ant-test", "ANTHROPIC_API_KEY": "", "WIKI_CLAUDE_MODELE": "", "WIKI_CLAUDE_EFFORT": ""})
class ExplorerTests(WikiTestCase):
    """Recherche dans le texte des PDF, « Demander au wiki », graphe des liens."""

    def setUp(self):
        super().setUp()
        (self.root / "Cours").mkdir()
        (self.root / "Cours/Poly signal.pdf").write_bytes(_pdf_texte(
            "Introduction au signal", "La transformée de Fourier\ndécompose un signal en fréquences.",
            "Annexe : trans-\nformée en Z"))
        self.write("Cours/Fourier.md", "# Fourier\n\nLa **transformée de Fourier** passe du temps aux fréquences.\n\n"
                                       "Voir [[Échantillonnage]] et [[Fourier]].\n")
        self.write("Cours/Échantillonnage.md", "# Échantillonnage\n\nShannon : $f_e > 2 f_{max}$. Lien vers [[Fourier]].\n")
        self.write("Divers/Isolée.md", "Rien à voir.\n")

    def test_recherche_dans_les_pdf(self):
        from wiki import texte_pdf
        from wiki.models import TextePdf
        # Avant lecture des PDF : la page le signale (le fil d'arrière-plan est coupé en test).
        self.assertContains(self.client.get("/recherche/", {"q": "fréquences"}), "Lecture du texte des PDF en cours (1 restant)")
        self.assertEqual(texte_pdf.indexer(get_vault()), 1)
        self.assertEqual(texte_pdf.indexer(get_vault()), 0)  # rien de neuf : rien n'est relu
        self.assertEqual(TextePdf.objects.get().pages[2], "Annexe : transformée en Z")
        page = self.client.get("/recherche/", {"q": "frequences"}).content.decode()
        self.assertIn("Dans les PDF", page)
        self.assertIn('href="/pdf/Cours/Poly%20signal.pdf#page=2"', page)
        self.assertIn("<mark>fréquences</mark>", page)
        self.assertNotIn("Lecture du texte des PDF en cours", page)
        # Un mot coupé en fin de ligne est retrouvé ; les mots doivent être sur la même page.
        self.assertIn("#page=3", self.client.get("/recherche/", {"q": "transformée en z"}).content.decode())
        self.assertNotIn("Dans les PDF", self.client.get("/recherche/", {"q": "introduction fourier"}).content.decode())
        # PDF supprimé : oublié à la lecture suivante ; PDF illisible : noté, sans erreur.
        (self.root / "Cours/Poly signal.pdf").unlink()
        (self.root / "abime.pdf").write_bytes(b"%PDF-1.4\npas un vrai pdf")
        from wiki.vault import invalider
        invalider()
        texte_pdf.indexer(get_vault())
        self.assertEqual(list(TextePdf.objects.values_list("chemin", flat=True)), ["abime.pdf"])
        self.assertNotIn("Dans les PDF", self.client.get("/recherche/", {"q": "fréquences"}).content.decode())

    def test_commande_indexer_pdf(self):
        from io import StringIO

        from django.core.management import call_command
        sortie = StringIO()
        call_command("indexer_pdf", stdout=sortie)
        self.assertIn("1 PDF lu ; 1 dans l'index.", sortie.getvalue())

    def test_mots_cles_passages_et_citations(self):
        from wiki import demander
        self.assertEqual(demander.mots_cles("Qu'est-ce que la transformée de Fourier ? Explique la FFT"),
                         ["transformee", "fourier", "fft"])
        texte = "Intro générale.\n\nLe temps.\n\nLa transformée de Fourier.\n\nConclusion."
        self.assertEqual(demander.passages(texte, ["fourier"], 30), "La transformée de Fourier.")
        self.assertEqual(demander.passages(texte, ["fourier"], 1000), texte)
        sources = [{"titre": "A", "url": "/wiki/A", "type": "page"}, {"titre": "B", "url": "/pdf/b.pdf#page=2", "type": "pdf"}]
        html, cites = demander.lier_citations(
            '<p>Vrai [1, 2], faux [7].</p><pre><code>t[1]</code></pre><span class="math math-inline">\\(x[2]\\)</span><p>[2]</p>', sources)
        self.assertEqual(cites, [1, 2])
        self.assertIn('<a class="citation" href="/wiki/A" title="A">[1]</a><a class="citation" href="/pdf/b.pdf#page=2" title="B">[2]</a>', html)
        self.assertIn("faux [7]", html)
        self.assertIn("<code>t[1]</code>", html)
        self.assertIn("\\(x[2]\\)", html)
        self.assertTrue(html.endswith('<p><a class="citation" href="/pdf/b.pdf#page=2" title="B">[2]</a></p>'))

    def test_demander_au_wiki(self):
        from wiki import claude, texte_pdf
        from wiki.models import EchangeTuteur, UsageClaude
        texte_pdf.indexer(get_vault())
        self.assertContains(self.client.get("/demander/", {"q": "Fourier ?"}), "Fourier ?</textarea>")
        self.assertContains(self.client.get("/"), "Demander au wiki")
        faux = _FauxClaude("La transformée de **Fourier** décompose un signal [1][3]. Voir aussi [9].")
        with mock.patch.object(claude, "_client", return_value=faux):
            r = self.client.post("/demander/", data=json.dumps({"question": "À quoi sert la transformée de Fourier ?"}),
                                 content_type="application/json")
        self.assertEqual(r.status_code, 200, r.content)
        donnees = r.json()
        demande = faux.demandes[0]
        self.assertEqual(demande["model"], "claude-haiku-5-5")
        self.assertIn("[1] Fourier\n", demande["system"])
        self.assertIn("(PDF, page 2)\nLa transformée de Fourier décompose un signal en fréquences.", demande["system"])
        # Pages d'abord (la plus pertinente en tête), puis les pages de PDF ; la page sans rapport est écartée.
        self.assertEqual([s["titre"] for s in donnees["sources"]], ["Fourier", "Échantillonnage", "Poly signal (PDF, page 2)"])
        self.assertIn('href="/wiki/Cours/Fourier"', donnees["html"])
        self.assertIn('href="/pdf/Cours/Poly%20signal.pdf#page=2"', donnees["html"])
        self.assertIn("[9]", donnees["html"])  # numéro inventé : laissé tel quel
        self.assertEqual([s["n"] for s in donnees["sources"] if s["cite"]], [1, 3])
        e = EchangeTuteur.objects.get()
        self.assertEqual((e.page, e.player), (EchangeTuteur.PAGE_WIKI, "lecteur"))
        self.assertEqual(e.sources[0], {"titre": "Fourier", "url": "/wiki/Cours/Fourier", "type": "page"})
        self.assertEqual(UsageClaude.objects.get().genre, "wiki")
        # Question de suite : l'échange précédent est rejoué, la question précédente aide la recherche.
        with mock.patch.object(claude, "_client", return_value=faux):
            self.client.post("/demander/", data=json.dumps({"question": "Et son inverse ?"}), content_type="application/json")
        self.assertEqual(len(faux.demandes[1]["messages"]), 3)
        self.assertIn("[1] Fourier\n", faux.demandes[1]["system"])
        page = self.client.get("/demander/").content.decode()
        self.assertLess(page.index("Et son inverse ?"), page.index("À quoi sert la transformée"))
        self.assertIn('class="citation"', page)
        # Les échanges du tuteur d'une page restent à part.
        self.assertNotContains(self.client.get("/wiki/Cours/Fourier"), "Et son inverse ?")
        # Rien de pertinent : Claude est prévenu qu'aucun extrait ne correspond.
        with mock.patch.object(claude, "_client", return_value=faux):
            self.client.post("/demander/", data=json.dumps({"question": "Recette du gâteau basque"}), content_type="application/json")
        self.assertIn("(aucun extrait ne correspond à la question)", faux.demandes[2]["system"])
        # Erreurs : question vide, sans clé d'API.
        self.assertEqual(self.client.post("/demander/", data=json.dumps({"question": " "}), content_type="application/json").status_code, 400)
        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": ""}):
            self.assertEqual(self.client.post("/demander/", data=json.dumps({"question": "x"}), content_type="application/json").status_code, 503)
            self.assertNotContains(self.client.get("/"), "Demander au wiki")

    def test_graphe(self):
        donnees = self.client.get("/graphe.json").json()
        titres = [n["t"] for n in donnees["noeuds"]]
        self.assertEqual(sorted(titres), ["Fourier", "Isolée", "Échantillonnage"])
        i, j = titres.index("Fourier"), titres.index("Échantillonnage")
        self.assertEqual(donnees["liens"], [[min(i, j), max(i, j)]])  # un seul lien, sans boucle sur soi
        self.assertEqual(donnees["noeuds"][i]["d"], "Cours")
        self.assertContains(self.client.get("/graphe/"), "graphe.js")
        page = self.client.get("/graphe/", {"page": "Cours/Fourier"})
        self.assertContains(page, 'data-centre="Cours/Fourier"')
        self.assertContains(page, "les voisines de la page")
        self.assertContains(self.client.get("/wiki/Cours/Fourier"), "/graphe/?page=Cours/Fourier")


@override_settings(WIKI_CLAUDE_FIL=False)
@mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": "sk-ant-test", "ANTHROPIC_API_KEY": "", "WIKI_CLAUDE_MODELE": "", "WIKI_CLAUDE_EFFORT": ""})
class CopieTests(WikiTestCase):
    """« Corriger ma copie » : photos d'une copie manuscrite corrigées par Claude."""

    def setUp(self):
        super().setUp()
        self.data = tempfile.TemporaryDirectory()
        self.addCleanup(self.data.cleanup)
        override = override_settings(DATA_DIR=Path(self.data.name))
        override.enable()
        self.addCleanup(override.disable)
        self.write("Cours/Fourier.md", "# Fourier\n\nLa transformée de $e^{-a|t|}$ vaut $\\frac{2a}{a^2+\\omega^2}$.\n")

    @staticmethod
    def _photo(nom="copie.png", taille=(3000, 2000)):
        import io

        from PIL import Image
        tampon = io.BytesIO()
        Image.new("RGB", taille, "white").save(tampon, "PNG")
        return SimpleUploadedFile(nom, tampon.getvalue(), content_type="image/png")

    def test_correction(self):
        import base64
        import io

        from PIL import Image

        from wiki import claude
        from wiki.models import CorrectionCopie, UsageClaude
        self.assertContains(self.client.get("/copie/", {"page": "Cours/Fourier"}), 'value="Cours/Fourier"')
        faux = _FauxClaude("### Ce que tu as écrit\n1. $X(\\omega) = \\frac{1}{a}$\n\n### Correction pas à pas\n1. ❌ Il manque le facteur $2a$.")
        with mock.patch.object(claude, "_client", return_value=faux):
            r = self.client.post("/copie/", {"photos": [self._photo("p1.png"), self._photo("p2.png", (800, 600))],
                                             "enonce": "Transformée de e^{-a|t|}", "page": "Cours/Fourier"})
        self.assertEqual(r.status_code, 200, r.content)
        self.assertIn("Il manque le facteur", r.json()["bloc"])
        demande = faux.demandes[0]
        self.assertEqual(demande["model"], "claude-sonnet-5-5")
        self.assertIn("Cours de référence « Fourier »", demande["system"])
        contenu = demande["messages"][0]["content"]
        self.assertEqual([b["type"] for b in contenu], ["image", "image", "text"])
        self.assertIn("Transformée de e^{-a|t|}", contenu[2]["text"])
        # Photos réduites (côté ≤ 1568 px) et converties en JPEG pour Claude.
        image = Image.open(io.BytesIO(base64.b64decode(contenu[0]["source"]["data"])))
        self.assertEqual((image.format, image.size), ("JPEG", (1568, 1045)))
        c = CorrectionCopie.objects.get()
        self.assertEqual((c.player, c.page, c.photos, c.modele), ("lecteur", "Cours/Fourier", 2, "claude-sonnet-5-5"))
        self.assertEqual(UsageClaude.objects.get().genre, "copie")
        # Historique et photos : visibles de leur seul auteur.
        self.assertContains(self.client.get("/copie/"), "Il manque le facteur")
        self.assertEqual(self.client.get(f"/copie/photo/{c.pk}/1").status_code, 200)
        self.assertEqual(self.client.get(f"/copie/photo/{c.pk}/2").status_code, 404)
        autre = get_user_model().objects.create_user("bob", password="x")
        self.client.force_login(autre)
        self.assertNotContains(self.client.get("/copie/"), "Il manque le facteur")
        self.assertEqual(self.client.get(f"/copie/photo/{c.pk}/0").status_code, 404)
        self.assertEqual(self.client.post(f"/copie/{c.pk}/supprimer/").status_code, 404)
        self.client.force_login(self.reader)
        self.assertEqual(self.client.post(f"/copie/{c.pk}/supprimer/").status_code, 200)
        self.assertFalse(CorrectionCopie.objects.exists())
        self.assertFalse(any((Path(self.data.name) / "copies").rglob("*.jpg")))
        self.assertContains(self.client.get("/wiki/Cours/Fourier"), "/copie/?page=Cours/Fourier")

    def test_erreurs(self):
        from wiki import claude
        for donnees, message in [
            ({}, "Ajoutez au moins une photo"),
            ({"photos": [self._photo(f"p{i}.png", (10, 10)) for i in range(5)]}, "4 photos au plus"),
            ({"photos": [SimpleUploadedFile("faux.jpg", b"pas une image")]}, "pas une photo lisible"),
            ({"photos": [self._photo(taille=(10, 10))], "page": "Inconnue"}, "Page inconnue"),
        ]:
            with self.subTest(message=message):
                r = self.client.post("/copie/", donnees)
                self.assertEqual(r.status_code, 400)
                self.assertIn(message, r.json()["error"])
        with mock.patch.object(claude, "plafond_atteint", return_value=True):
            self.assertEqual(self.client.post("/copie/", {"photos": [self._photo(taille=(10, 10))]}).status_code, 429)
        with mock.patch.dict("os.environ", {"WIKI_CLAUDE_CLE": ""}):
            self.assertEqual(self.client.post("/copie/", {"photos": [self._photo(taille=(10, 10))]}).status_code, 503)
            self.assertContains(self.client.get("/copie/"), "Pas de clé d'API Claude")
