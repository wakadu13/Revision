"""Tests du module Langues (FSRS, facettes, correction, sessions, vues), de la
vérification des fichiers et des prompts IA."""

import json
import re
import tempfile
from datetime import timedelta
from io import StringIO
from pathlib import Path, PurePosixPath

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase, TestCase, override_settings
from django.utils import timezone

from . import fsrs, langues, quiz, verifier
from .models import QuizProgress

SET_TEST = {
    "langue": "Anglais", "particules_optionnelles": ["to"],
    "vocabulaire": [{"id": "v1", "mot": "to achieve", "traductions": ["réussir", "accomplir"],
                     "exemple": "She [achieved] her goal."}],
    "conjugaison": [{"id": "c1", "verbe": "to be", "temps": "present simple",
                     "formes": {"I": "am", "you": "are", "he / she / it": "is"}}],
    "grammaire": [{"id": "g1", "type": "ORDRE", "phrase": "She has never been to London."},
                  {"id": "g2", "type": "CORRECTION", "phrase": "He don't like it.",
                   "corrections": ["He doesn't like it.", "He does not like it."]},
                  {"id": "g3", "type": "TROU", "question": "I ___ (go)", "reponses_texte": ["went"]}],
}


def set_test():
    return langues.set_depuis_json(SET_TEST, PurePosixPath("langues/t.json"))


class FsrsTests(SimpleTestCase):
    def test_retention_a_l_echeance(self):
        # Par construction, R vaut 90 % au bout de S jours.
        self.assertAlmostEqual(fsrs.retrievabilite(10, 10), 0.9)
        self.assertAlmostEqual(fsrs.intervalle_jours(10), 10)

    def test_notes_ordonnees(self):
        e = fsrs.premiere(fsrs.BIEN)
        s = [fsrs.suivante(e, e.stabilite, n).stabilite for n in fsrs.NOTES]
        self.assertTrue(s[0] < s[1] < s[2] < s[3], s)
        self.assertLessEqual(s[0], e.stabilite)
        # Une révision réussie au bon moment augmente fortement la stabilité.
        self.assertGreater(s[2], 2 * e.stabilite)

    def test_reviser_tard_rapporte_plus(self):
        e = fsrs.Etat(10, 5)
        self.assertGreater(fsrs.suivante(e, 20, fsrs.BIEN).stabilite, fsrs.suivante(e, 5, fsrs.BIEN).stabilite)


class FacettesCorrectionTests(SimpleTestCase):
    def test_facettes(self):
        s = set_test()
        self.assertEqual([e.id for e in s.exercices],
                         ["v1#rec", "v1#prod", "v1#ctx", "c1#I", "c1#you", "c1#he / she / it", "g1", "g2", "g3"])
        self.assertEqual(s.exercices[6].donnees["mots"], ["she", "has", "never", "been", "to", "London"])
        self.assertEqual(s.exercices[2].donnees["consigne"], "Complète : She _____ her goal.\n(indice : réussir, accomplir)")
        self.assertEqual(s.exercices[1].prerequis, "v1#rec")
        self.assertEqual(s.id, "langues/t")

    def test_erreurs_de_format(self):
        rel = PurePosixPath("t.json")
        with self.assertRaisesMessage(ValueError, "'traductions' manquante"):
            langues.set_depuis_json({"langue": "Anglais", "vocabulaire": [{"mot": "x"}]}, rel)
        with self.assertRaisesMessage(ValueError, "identifiant en double"):
            langues.set_depuis_json({"langue": "Anglais", "grammaire": [
                {"id": "g", "type": "TROU", "question": "a ___", "reponses_texte": ["b"]},
                {"id": "g", "type": "TROU", "question": "c ___", "reponses_texte": ["d"]}]}, rel)
        with self.assertRaisesMessage(ValueError, "aucun élément"):
            langues.set_depuis_json({"langue": "Anglais"}, rel)

    def test_correction_tolerante(self):
        p, r = ["to"], ["to achieve"]
        self.assertEqual(langues.noter_saisie("achieve", r, True, p)[0], langues.JUSTE)
        self.assertEqual(langues.noter_saisie("To Achieve", r, True, p)[0], langues.JUSTE)
        self.assertEqual(langues.noter_saisie("acheive", r, True, p)[0], langues.FAUTE)
        self.assertEqual(langues.noter_saisie("receive", r, True, p)[0], langues.FAUX)
        self.assertEqual(langues.noter_saisie("cafe", ["café"], True)[0], langues.ACCENTS)
        # Conjugaison / grammaire : aucune tolérance (« goed » n'est pas « goes »).
        self.assertEqual(langues.noter_saisie("goed", ["goes"], False)[0], langues.FAUX)
        self.assertEqual(langues.noter_saisie("he doesn’t like it", ["He doesn't like it."], False)[0], langues.JUSTE)
        self.assertEqual(langues.normaliser_strict("Tu es là ? Oui !"), "tu es là? oui")

    def test_surlignage(self):
        d = langues.diff("recieve", "receive")
        self.assertEqual(len([c for c, ok in d if not ok]), 1)
        self.assertEqual("".join(c for c, _ in d), "receive")

    def test_corriger(self):
        s = set_test()
        ordre = s.exercice("g1")
        juste = langues.corriger(s, ordre, [0, 1, 2, 3, 4, 5])
        self.assertEqual((juste["verdict"], juste["note"]), (langues.JUSTE, fsrs.BIEN))
        self.assertIsNone(langues.corriger(s, ordre, [0, 1]))  # mots non tous placés
        faux = langues.corriger(s, s.exercice("v1#prod"), "recevoir")
        self.assertEqual((faux["verdict"], faux["note"], faux["attendu"]), (langues.FAUX, fsrs.A_REVOIR, "to achieve"))
        self.assertTrue(faux["diff"])

    def test_texte_delai(self):
        self.assertEqual(langues.texte_delai(timedelta(minutes=10)), "10 min")
        self.assertEqual(langues.texte_delai(timedelta(days=3)), "3 j")
        self.assertEqual(langues.texte_delai(timedelta(days=61)), "2 mois")
        self.assertEqual(langues.texte_delai(timedelta(days=548)), "1,5 an")


class SessionTests(TestCase):
    def setUp(self):
        self.set = set_test()
        self.prog = {}
        self.now = timezone.now()

    def session(self, mode=langues.QUOTIDIEN, n=50):
        return langues.construire_session([self.set], self.prog, mode, n, self.now)

    def enregistrer(self, exo_id, note):
        st = self.prog.setdefault((self.set.id, exo_id),
                                  QuizProgress(player="p", set_id=self.set.id, question_id=exo_id))
        st.record_langue(note)
        return st

    def test_session_et_deblocage(self):
        ids = [e.exo.id for e in self.session()]
        # Production verrouillée tant que la carte n'est pas apprise ; 2 formes max par verbe.
        self.assertIn("v1#rec", ids)
        self.assertNotIn("v1#prod", ids)
        self.assertEqual(len([i for i in ids if i.startswith("c1#")]), 2)
        # Entrelacement : pas deux genres identiques à la suite au début.
        s = self.session()
        self.assertNotEqual(s[0].exo.genre, s[1].exo.genre)
        # Remise en ordre : mots mélangés, différemment de l'ordre d'origine.
        g1 = next(e for e in s if e.exo.id == "g1")
        self.assertNotEqual(g1.melange, sorted(g1.melange))

        st = self.enregistrer("v1#rec", fsrs.BIEN)
        self.assertIsNotNone(st.stabilite)
        self.assertGreater(st.echeance, self.now)
        ids = [e.exo.id for e in self.session(langues.VOCABULAIRE)]
        self.assertEqual(len(ids), 1, f"une seule facette du mot par session : {ids}")
        self.assertIn(ids[0], ("v1#prod", "v1#ctx"))

        st = self.enregistrer("v1#rec", fsrs.A_REVOIR)
        self.assertEqual(st.oublis, 1)
        self.assertEqual(self.session(langues.FAIBLES, 10)[0].exo.id, "v1#rec")

    def test_quota_de_nouveautes(self):
        self.set.nouveaux_par_jour = 3
        self.assertEqual(len(self.session()), 3)
        for exo_id in ("v1#rec", "g1"):
            self.enregistrer(exo_id, fsrs.BIEN)
        self.assertEqual(langues.quota_nouveaux([self.set], self.prog, self.now), 1)

    def test_resume(self):
        self.enregistrer("v1#rec", fsrs.BIEN)
        for _ in range(2):
            self.enregistrer("g3", fsrs.BIEN)
            self.enregistrer("g3", fsrs.A_REVOIR)
        r = langues.resume([self.set], self.prog, self.now)
        voc = next(g for g in r["genres"] if g["nom"] == "Vocabulaire")
        self.assertEqual((voc["total"], voc["appris"], voc["a_revoir"]), (3, 1, 0))
        self.assertEqual(r["difficiles"][0][1], 2)
        # g3 oublié revient dans 10 minutes, la carte dans quelques jours.
        self.assertEqual((r["a_revoir"], r["sept_jours"]), (0, 2))


class LangueViewTests(TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        override = override_settings(WIKI_DIR=self.root, WIKI_HOME="Accueil", SECURE_SSL_REDIRECT=False)
        override.enable()
        self.addCleanup(override.disable)
        (self.root / "langues").mkdir()
        (self.root / "langues" / "t.json").write_text(json.dumps(SET_TEST), encoding="utf-8")
        self.user = get_user_model().objects.create_user("alice", password="x")
        self.client.force_login(self.user)

    def post(self, url, data):
        return self.client.post(url, data=data, content_type="application/json")

    def test_bibliotheque_et_index(self):
        lib = quiz.get_library()
        self.assertEqual(list(lib.langues), ["langues/t"])
        self.assertEqual(lib.sets, {})  # pas un set de QCM classique
        response = self.client.get("/qcm/")
        self.assertContains(response, "Langues")
        self.assertContains(response, "/qcm/langues/Anglais/jouer/?mode=quotidien")

    def test_menu_et_session(self):
        self.assertContains(self.client.get("/qcm/langues/Anglais/"), "Points faibles")
        self.assertEqual(self.client.get("/qcm/langues/Klingon/").status_code, 404)
        response = self.client.get("/qcm/langues/Anglais/jouer/?mode=quotidien&n=4")
        exos = response.context["exercices"]
        self.assertEqual(len(exos), 4)
        self.assertEqual(len({e["genre"] for e in exos[:3]}), 3)
        carte = next(e for e in response.context["exercices"] if e["forme"] == "carte")
        self.assertEqual(set(carte["previsions"]), {"1", "2", "3", "4"})
        self.assertEqual(carte["previsions"]["1"], "10 min")
        # Les réponses des saisies ne sont pas envoyées au navigateur.
        self.assertNotIn("reponses", next(e for e in exos if e["forme"] == "saisie"))
        self.assertEqual(self.client.get("/qcm/langues/Anglais/jouer/?mode=xyz").status_code, 404)

    def test_corriger_et_enregistrer(self):
        r = self.post("/qcm/langue/corriger/", {"set_id": "langues/t", "exo_id": "c1#I", "reponse": "is"}).json()
        self.assertEqual((r["verdict"], r["note"]), ("faux", 1))
        self.assertEqual(r["attendu"], "am")
        self.assertFalse(QuizProgress.objects.exists())  # corriger n'enregistre rien
        r = self.post("/qcm/langue/corriger/", {"set_id": "langues/t", "exo_id": "g1", "reponse": [0, 1]})
        self.assertEqual(r.status_code, 400)
        r = self.post("/qcm/langue/corriger/", {"set_id": "langues/t", "exo_id": "nope", "reponse": "x"})
        self.assertEqual(r.status_code, 404)

        self.assertEqual(self.post("/qcm/langue/reponse/", {"set_id": "langues/t", "exo_id": "v1#rec", "note": 3}).status_code, 200)
        p = QuizProgress.objects.get(question_id="v1#rec")
        self.assertEqual((p.player, p.set_id, p.seen, p.box), ("alice", "langues/t", 1, 1))
        self.assertGreater(p.echeance, timezone.now() + timedelta(days=2))
        self.assertIsNotNone(p.decouverte)
        self.assertEqual(self.post("/qcm/langue/reponse/", {"set_id": "langues/t", "exo_id": "v1#rec", "note": 9}).status_code, 400)
        # La production est maintenant débloquée.
        ids = [e["exo_id"] for e in self.client.get("/qcm/langues/Anglais/jouer/?mode=vocabulaire").context["exercices"]]
        self.assertIn(ids[0], ("v1#prod", "v1#ctx"))

        self.client.post("/qcm/langues/Anglais/reinitialiser/")
        self.assertFalse(QuizProgress.objects.exists())

    def test_import_fichier_langue(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(admin)
        f = SimpleUploadedFile("esp.json", json.dumps({**SET_TEST, "langue": "Espagnol"}).encode())
        response = self.client.post("/qcm/importer/", {"fichiers": [f], "categorie": "langues"}, follow=True)
        self.assertContains(response, "9 exercices")
        self.assertEqual(quiz.get_library().noms_langues(), ["Anglais", "Espagnol"])


class VerifierTests(SimpleTestCase):
    def test_exemples_des_prompts_ia_valides(self):
        """Chaque prompt de prompts_ia/ contient un exemple JSON accepté tel quel, sans avertissement."""
        fichiers = sorted(p for p in (Path(settings.BASE_DIR) / "prompts_ia").glob("*.txt")
                          if p.name != "00_LISEZMOI.txt")
        self.assertEqual(len(fichiers), 10)
        for f in fichiers:
            m = re.search(r"```json\n(.*?)```", f.read_text(encoding="utf-8"), re.S)
            self.assertIsNotNone(m, f"{f.name} : pas d'exemple")
            _, avert = verifier.verifier_donnees(json.loads(m.group(1)), PurePosixPath("test/exemple.json"))
            self.assertEqual(avert, [], f.name)

    def test_avertissements(self):
        _, avert = verifier.verifier_donnees({"questions": [
            {"id": "a", "type": "TROU", "question": "Sans trou $x", "reponses_texte": ["b"]},
            {"id": "a", "type": "QCR", "question": "?", "choix": ["x", "y"], "reponses": [0, 1]},
        ]}, PurePosixPath("t/x.json"))
        texte = "\n".join(avert)
        for attendu in ("non fermée", "pas de « ___ »", "toutes les propositions", "« a » utilisé plusieurs fois"):
            self.assertIn(attendu, texte)

    def test_commande(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "ok.json").write_text(json.dumps(SET_TEST), encoding="utf-8")
            out = StringIO()
            call_command("verifier_qcm", tmp, stdout=out)
            self.assertIn("1 fichier(s) valide(s)", out.getvalue())
            Path(tmp, "ko.json").write_text('{"questions": [{"type": "QCM", "question": "x"}]}', encoding="utf-8")
            with self.assertRaises(CommandError):
                call_command("verifier_qcm", tmp, stdout=StringIO())

    def test_tout_le_coffre_se_charge(self):
        lib = quiz.Library(settings.WIKI_DIR, [(p.relative_to(settings.WIKI_DIR).as_posix(), 0, 0)
                                                for p in Path(settings.WIKI_DIR, "QCM").rglob("*.json")])
        self.assertEqual(lib.errors, [])
        self.assertIn("Anglais", lib.noms_langues())
