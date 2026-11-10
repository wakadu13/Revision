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

from wiki import fsrs, langues, quiz, verifier
from wiki.models import QuizProgress
from wiki.vault import get_vault

from .base import WikiTestCase

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

    def test_types_de_cartes_choisis(self):
        mots = [{"id": "v1", "mot": "to achieve", "traductions": ["réussir"], "exemple": "She [achieved] it.",
                 "prononciation": "/əˈtʃiːv/"},
                {"id": "v2", "mot": "a kitchen", "traductions": ["une cuisine"]},
                {"id": "v3", "mot": "a job", "traductions": ["un emploi"]},
                {"id": "v4", "mot": "to cook", "traductions": ["cuisiner"]}]
        tous = ["decouverte", "production", "choix", "contexte", "reconnaissance", "traduction"]
        s = langues.set_depuis_json({"langue": "Anglais", "exercices": tous, "vocabulaire": mots}, PurePosixPath("t.json"))
        v1 = {e.id: e for e in s.exercices if e.entree == "v1"}
        self.assertEqual(list(v1), ["v1#dec", "v1#prod", "v1#qcm", "v1#ctx", "v1#rec", "v1#trad"])
        # La carte français → anglais fait découvrir le mot ; les autres attendent qu'elle soit réussie.
        self.assertIsNone(v1["v1#dec"].prerequis)
        self.assertTrue(all(e.prerequis == "v1#dec" for i, e in v1.items() if i != "v1#dec"))
        self.assertEqual(v1["v1#dec"].donnees, {"recto": "réussir", "verso": "to achieve   /əˈtʃiːv/"})
        self.assertEqual(v1["v1#dec"].etiquette, "Vocabulaire · carte (FR → EN)")
        self.assertEqual(v1["v1#prod"].donnees["reponses"], ["to achieve"])
        self.assertEqual(v1["v1#trad"].donnees["reponses"], ["réussir"])
        qcm = v1["v1#qcm"].donnees
        self.assertEqual(len(qcm["choix"]), 4)
        self.assertEqual(qcm["choix"][qcm["reponses"][0]], "to achieve")
        self.assertEqual(sorted(qcm["choix"]), ["a job", "a kitchen", "to achieve", "to cook"])
        # Même ordre des choix à chaque chargement.
        s2 = langues.set_depuis_json({"langue": "Anglais", "exercices": tous, "vocabulaire": mots}, PurePosixPath("t.json"))
        self.assertEqual(s2.exercice("v1#qcm").donnees, qcm)
        # Sans exemple, pas de phrase à compléter.
        self.assertNotIn("v2#ctx", [e.id for e in s.exercices])
        self.assertEqual(s.noms_types[0], "Carte FR → EN")

        # Une seule sorte de carte : elle fait découvrir le mot.
        s = langues.set_depuis_json({"langue": "Anglais", "exercices": ["production"], "vocabulaire": mots[:1]},
                                    PurePosixPath("t.json"))
        self.assertEqual([(e.id, e.prerequis) for e in s.exercices], [("v1#prod", None)])
        # QCM impossible avec un seul mot dans le paquet.
        s = langues.set_depuis_json({"langue": "Anglais", "exercices": ["choix", "production"], "vocabulaire": mots[:1]},
                                    PurePosixPath("t.json"))
        self.assertEqual([(e.id, e.prerequis) for e in s.exercices], [("v1#prod", None)])
        with self.assertRaisesMessage(ValueError, "'exercices' doit lister"):
            langues.set_depuis_json({"langue": "Anglais", "exercices": ["lecture"], "vocabulaire": mots}, PurePosixPath("t.json"))
        # Sans clé « exercices » : comme avant.
        self.assertEqual(set_test().types_vocabulaire, ["reconnaissance", "production", "contexte"])

    def test_dictee_et_son(self):
        mots = [{"id": "v1", "mot": "to achieve", "traductions": ["réussir"], "exemple": "She [achieved] it."}]
        s = langues.set_depuis_json({"langue": "Anglais", "exercices": ["dictee", "production", "contexte"], "vocabulaire": mots},
                                    PurePosixPath("t.json"))
        self.assertEqual(s.code_langue, "en-GB")
        dictee = s.exercice("v1#dict")
        self.assertEqual(dictee.forme, langues.SAISIE)
        self.assertEqual(dictee.audio, {"texte": "to achieve", "quand": "debut"})
        self.assertEqual(dictee.donnees["reponses"], ["to achieve"])
        self.assertEqual(dictee.donnees["indice"], "réussir")
        self.assertEqual(dictee.details[0], "Sens : « réussir »")
        # La dictée ne fait jamais découvrir un mot quand une autre carte existe.
        self.assertEqual(dictee.prerequis, "v1#prod")
        self.assertEqual(s.exercice("v1#prod").audio, {"texte": "to achieve", "quand": "fin"})
        self.assertEqual(s.exercice("v1#ctx").audio, {"texte": "She achieved it.", "quand": "fin"})
        self.assertEqual(set_test().exercice("v1#rec").audio, {"texte": "to achieve", "quand": "debut"})
        self.assertIsNone(set_test().exercice("c1#I").audio)
        es = langues.set_depuis_json({"langue": "Espagnol", "code_langue": "es-MX", "vocabulaire": mots}, PurePosixPath("t.json"))
        self.assertEqual(es.code_langue, "es-MX")
        self.assertEqual(langues.code_langue("Roumain"), "ro-RO")
        self.assertEqual(langues.code_langue("Klingon"), "kl")

    def test_erreurs_de_format(self):
        rel = PurePosixPath("t.json")
        with self.assertRaisesMessage(ValueError, "'traductions' (ou 'definition') manquante"):
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

    def test_session_intensive(self):
        # Tout, sans prérequis ni quota ni limite de facettes : 9 exercices.
        self.set.nouveaux_par_jour = 1
        ids = [e.exo.id for e in self.session(langues.INTENSIF, n=2)]
        self.assertEqual(sorted(ids), sorted(e.id for e in self.set.exercices))
        # La carte qui fait découvrir le mot passe avant ses autres facettes.
        self.assertLess(ids.index("v1#rec"), ids.index("v1#prod"))
        self.assertLess(ids.index("v1#rec"), ids.index("v1#ctx"))
        # Déjà su et pas encore dû : revu quand même.
        self.enregistrer("v1#rec", fsrs.FACILE)
        self.assertIn("v1#rec", [e.exo.id for e in self.session(langues.INTENSIF)])
        # Au-delà de la limite : les éléments fragiles (oubliés) d'abord.
        self.enregistrer("g2", fsrs.BIEN)
        self.enregistrer("g2", fsrs.A_REVOIR)
        petite = langues.session_intensive([self.set], self.prog, self.now, limite=1)
        self.assertEqual([e.exo.id for e in petite], ["g2"])
        # Remise en ordre : mots mélangés comme dans les autres modes.
        g1 = next(e for e in self.session(langues.INTENSIF) if e.exo.id == "g1")
        self.assertNotEqual(g1.melange, sorted(g1.melange))

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

    def test_revision_intensive(self):
        self.assertContains(self.client.get("/qcm/langues/Anglais/"), "Révision intensive")
        index = self.client.get("/qcm/").content.decode()
        self.assertIn("/qcm/langues/Anglais/jouer/?mode=intensif", index)
        self.assertIn("/qcm/langues/Anglais/jouer/?mode=intensif&dossier=langues", index)
        self.assertIn("mode=intensif&amp;fichier=langues/t", index)
        response = self.client.get("/qcm/langues/Anglais/jouer/?mode=intensif&n=3")
        self.assertEqual(len(response.context["exercices"]), 9)  # tout, malgré n=3
        self.assertContains(response, 'data-mode="intensif"')
        self.assertContains(response, "2 fois de suite")
        self.assertEqual(response.context["exercices"][0]["resume"].split(" ")[0] != "", True)
        paquet = self.client.get("/qcm/langues/Anglais/jouer/?mode=intensif&fichier=langues/t")
        self.assertEqual(len(paquet.context["exercices"]), 9)
        self.assertContains(self.client.get("/qcm/langues/Anglais/jouer/?mode=quotidien"), 'data-mode="normal"')

    def test_son_dans_la_session(self):
        exos = self.client.get("/qcm/langues/Anglais/jouer/?mode=intensif").context["exercices"]
        carte = next(e for e in exos if e["exo_id"] == "v1#rec")
        self.assertEqual(carte["audio"], {"texte": "to achieve", "quand": "debut", "lang": "en-GB"})
        self.assertNotIn("audio", next(e for e in exos if e["exo_id"] == "g1"))

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


class LangueHorsLigneTests(TestCase):
    """Paquets de langue sur l'appareil : téléchargement complet, réponses rejouées."""

    def setUp(self):
        LangueViewTests.setUp(self)

    def _synchro(self, *reponses):
        return self.client.post("/qcm/hors-ligne/synchro/", data=json.dumps({"reponses": list(reponses)}),
                                content_type="application/json")

    def test_catalogue_et_telechargement(self):
        cat = self.client.get("/qcm/hors-ligne/catalogue/").json()
        self.assertEqual(cat["sets"], [])
        self.assertEqual(cat["langues"], [{"id": "langues/t", "titre": "t", "description": "", "langue": "Anglais",
                                           "dossier": "langues", "total": 9, "type": "langue"}])
        self.client.post("/qcm/langue/reponse/", data=json.dumps({"set_id": "langues/t", "exo_id": "v1#rec", "note": 3}),
                         content_type="application/json")
        data = self.client.get("/qcm/hors-ligne/sets/", {"id": ["langues/t", "inconnu"]}).json()
        self.assertEqual(data["manquants"], ["inconnu"])
        (s,) = data["sets"]
        self.assertEqual((s["type"], s["langue"], s["code_langue"], s["particules"]), ("langue", "Anglais", "en-GB", ["to"]))
        self.assertEqual([e["exo_id"] for e in s["exercices"]][:3], ["v1#rec", "v1#prod", "v1#ctx"])
        prod = s["exercices"][1]
        # Tout ce qu'il faut pour corriger et planifier sans le serveur.
        self.assertEqual((prod["forme"], prod["reponses"], prod["tolerant"], prod["entree"], prod["prerequis"]),
                         ("saisie", ["to achieve"], True, "v1", "v1#rec"))
        self.assertEqual(prod["max_par_session"], 1)
        self.assertNotIn("previsions", s["exercices"][0])
        self.assertEqual(s["exercices"][6]["reponses"], ["She has never been to London."])
        self.assertEqual(s["exercices"][3]["reponses"], ["am"])
        p = s["progression"]["v1#rec"]
        self.assertGreater(p["stabilite"], 0)
        self.assertEqual(p["oublis"], 0)
        self.assertTrue(p["last_correct"])
        self.assertTrue(p["echeance"] and p["decouverte"] and p["last_review"])
        self.assertEqual(list(s["progression"]), ["v1#rec"])

    def test_synchro_rejoue_les_notes_fsrs(self):
        from wiki.models import Activite
        r = self._synchro(
            {"uid": "b", "set_id": "langues/t", "exo_id": "v1#rec", "note": 1, "date": "2026-10-02T08:00:00Z"},
            {"uid": "a", "set_id": "langues/t", "exo_id": "v1#rec", "note": 3, "date": "2026-10-01T08:00:00Z"},
            {"uid": "x", "set_id": "langues/t", "exo_id": "inconnu", "note": 3, "date": "2026-10-01T08:00:00Z"},
            {"uid": "y", "set_id": "langues/t", "exo_id": "v1#prod", "note": 7, "date": "2026-10-01T08:00:00Z"},
            {"uid": "z", "set_id": "langues/t", "exo_id": "v1#prod", "note": "bien", "date": "2026-10-01T08:00:00Z"},
        )
        self.assertEqual(r.json(), {"traitees": ["b", "a", "x", "y", "z"], "enregistrees": 2})
        p = QuizProgress.objects.get(player="alice", set_id="langues/t", question_id="v1#rec")
        self.assertEqual(p.last_review.isoformat(), "2026-10-02T08:00:00+00:00")
        self.assertEqual(p.decouverte.isoformat(), "2026-10-01T08:00:00+00:00")
        self.assertEqual((p.oublis, p.last_correct, p.seen), (1, False, 2))
        self.assertEqual(p.echeance, p.last_review + timedelta(minutes=10))
        self.assertFalse(QuizProgress.objects.filter(question_id="v1#prod").exists())
        self.assertEqual(Activite.objects.filter(player="alice").count(), 2)  # 1er et 2 octobre
        # Renvoi : déjà reçue, ignorée.
        r = self._synchro({"uid": "a", "set_id": "langues/t", "exo_id": "v1#rec", "note": 3, "date": "2026-10-01T08:00:00Z"})
        self.assertEqual(r.json()["enregistrees"], 0)
        self.assertEqual(QuizProgress.objects.get(question_id="v1#rec").seen, 2)

    def test_page_hors_ligne_embarque_le_module_langues(self):
        page = self.client.get("/qcm/hors-ligne/").content.decode()
        self.assertIn('id="quiz-langue"', page)
        self.assertIn("langues_hors_ligne.js", page)
        self.assertIn("quiz_langue.js", page)
        sw = self.client.get("/qcm/sw.js").content.decode()
        self.assertIn("langues_hors_ligne.js", sw)


class RappelTests(TestCase):
    """/api/rappel/ : ce qu'il reste à réviser, pour la notification quotidienne de l'application."""

    def setUp(self):
        LangueViewTests.setUp(self)
        (self.root / "reseaux").mkdir()
        (self.root / "reseaux" / "s.json").write_text(json.dumps({"titre": "S", "questions": [
            {"id": "q1", "type": "QCM", "question": "2+2 ?", "choix": ["3", "4"], "reponses": [1]}]}), encoding="utf-8")

    def test_compte_les_elements_dus(self):
        r = self.client.get("/api/rappel/").json()
        # Une question jamais vue est à réviser ; un mot jamais vu n'est pas « dû ».
        self.assertEqual(r, {"a_revoir": 1, "qcm": 1, "langues": 0, "serie": 0, "aujourdhui": 0, "admin": False})
        self.user.is_staff = True
        self.user.save()
        self.assertTrue(self.client.get("/api/rappel/").json()["admin"])
        now = timezone.now()
        QuizProgress.objects.create(player="alice", set_id="langues/t", question_id="v1#rec", stabilite=2.0, difficulte=5.0,
                                    echeance=now - timedelta(days=1), last_review=now - timedelta(days=3), decouverte=now - timedelta(days=3))
        QuizProgress.objects.create(player="alice", set_id="langues/t", question_id="v1#prod", stabilite=30.0, difficulte=5.0,
                                    echeance=now + timedelta(days=20), last_review=now - timedelta(days=3), decouverte=now - timedelta(days=3))
        self.client.post("/qcm/reponse/", data=json.dumps({"set_id": "reseaux/s", "question_id": "q1", "correct": True}),
                         content_type="application/json")
        r = self.client.get("/api/rappel/").json()
        self.assertEqual((r["qcm"], r["langues"], r["a_revoir"]), (0, 1, 1))
        self.assertEqual((r["serie"], r["aujourdhui"]), (1, 1))

    def test_connexion_requise(self):
        self.client.logout()
        self.assertEqual(self.client.get("/api/rappel/").status_code, 302)


class PrononciationTests(WikiTestCase):
    """Langues : cartes de prononciation, vérifiées par la reconnaissance vocale de l'appareil."""

    def setUp(self):
        super().setUp()
        paquet = {"langue": "Anglais", "titre": "Verbes", "exercices": ["decouverte", "prononciation"],
                  "particules_optionnelles": ["to"],
                  "vocabulaire": [{"id": "v1", "mot": "to achieve", "traductions": ["réussir"], "prononciation": "/əˈtʃiːv/",
                                   "variantes": ["achieve"]}]}
        self.write("QCM/Anglais/verbes.json", json.dumps(paquet))

    def test_carte_de_prononciation(self):
        from wiki import langues
        s = quiz.get_library().langues["QCM/Anglais/verbes"]
        oral = next(e for e in s.exercices if e.id == "v1#oral")
        self.assertEqual((oral.forme, oral.prerequis, oral.audio["quand"]), (langues.CARTE, "v1#dec", langues.VERSO))
        self.assertEqual(oral.donnees["oral"], {"reponses": ["to achieve", "achieve"]})
        self.assertIn("Prononciation", langues.nom_type("prononciation", "Anglais"))
        # Dans la session (après la découverte) et hors ligne : de quoi vérifier sur l'appareil.
        from wiki.langues_views import payload_hors_ligne
        p = payload_hors_ligne(get_vault(), s, oral)
        self.assertEqual(p["oral"], {"reponses": ["to achieve", "achieve"], "particules": ["to"], "lang": "en-GB"})
        self.assertIn("<strong>to achieve</strong>", p["recto"])
        self.assertIn("/əˈtʃiːv/", p["verso"])
        # Choix proposé à l'import de listes et à la génération par Claude.
        self.assertContains(self.client.get("/qcm/mon-espace/"), 'value="prononciation"')


class DefinitionsEtQcmTests(WikiTestCase):
    """Langues : cartes anglais → anglais d'après la définition, et les autres QCM
    (traduction, phrase à compléter, à l'écoute)."""

    PAQUET = {
        "langue": "Anglais", "titre": "Mots", "particules_optionnelles": ["to", "a", "an", "the"],
        "exercices": ["definition", "definition_saisie", "definition_choix", "choix_traduction", "contexte_choix",
                      "ecoute_choix"],
        "vocabulaire": [
            {"id": "v1", "mot": "to achieve", "traductions": ["réussir", "atteindre"],
             "definition": "to achieve something is to succeed in doing it", "exemple": "She [achieved] her goal."},
            {"id": "v2", "mot": "a kitchen", "traductions": ["une cuisine"], "definition": "the room where food is cooked",
             "exemple": "The [kitchen] is clean."},
            {"id": "v3", "mot": "reliable", "traductions": ["fiable"], "definition": "that can be trusted"},
            {"id": "v4", "mot": "to succeed", "traductions": ["réussir"], "definition": "to do what you tried to do"},
        ],
    }

    def setUp(self):
        super().setUp()
        self.data = tempfile.TemporaryDirectory()
        self.addCleanup(self.data.cleanup)
        override = override_settings(DATA_DIR=Path(self.data.name))
        override.enable()
        self.addCleanup(override.disable)

    def _set(self, paquet=None):
        return langues.set_depuis_json(paquet or self.PAQUET, PurePosixPath("QCM/Anglais/mots.json"))

    def test_cartes_de_definition(self):
        s = self._set()
        par_id = {e.id: e for e in s.exercices}
        self.assertEqual(sorted(i for i in par_id if i.startswith("v1#")),
                         ["v1#def", "v1#defm", "v1#defq", "v1#qctx", "v1#qson", "v1#qtrad"])
        carte = par_id["v1#def"]
        self.assertEqual((carte.forme, carte.prerequis), (langues.CARTE, None))  # la carte fait découvrir le mot
        # Le mot (et sa forme sans « to ») est caché dans la définition.
        self.assertEqual(carte.donnees["recto"], "« _____ something is to succeed in doing it »")
        saisie = par_id["v1#defm"]
        self.assertEqual((saisie.forme, saisie.prerequis), (langues.SAISIE, "v1#def"))
        self.assertIn("Indice : a······ (7 lettres)", saisie.donnees["consigne"])
        self.assertEqual(saisie.donnees["reponses"], ["to achieve"])
        qcm = par_id["v2#defq"]
        self.assertEqual(qcm.donnees["choix"][qcm.donnees["reponses"][0]], "a kitchen")
        self.assertEqual(len(qcm.donnees["choix"]), 4)
        self.assertEqual(langues.indice_lettres("give up"), "g··· u· (2 mots)")

    def test_autres_qcm(self):
        par_id = {e.id: e for e in self._set().exercices}
        trad = par_id["v1#qtrad"].donnees
        self.assertEqual(trad["choix"][trad["reponses"][0]], "réussir")
        # « réussir » est aussi la traduction de v4 : jamais proposé comme piège ailleurs pour v1.
        self.assertEqual(trad["choix"].count("réussir"), 1)
        ctx = par_id["v1#qctx"].donnees
        self.assertIn("She _____ her goal.", ctx["enonce"])
        self.assertEqual(ctx["choix"][ctx["reponses"][0]], "achieved")
        self.assertNotIn("to succeed", ctx["choix"])  # pièges sans « to » ni « a »
        self.assertIn("succeed", ctx["choix"])
        ecoute = par_id["v3#qson"]
        self.assertEqual((ecoute.donnees["ecoute"], ecoute.donnees["indice"], ecoute.audio["quand"]), (True, "reliable", "debut"))
        self.assertEqual(ecoute.donnees["choix"][ecoute.donnees["reponses"][0]], "fiable")
        self.assertNotIn("reliable", ecoute.donnees["enonce"])
        # Rien à corriger de neuf : la correction des QCM sert telle quelle.
        v = langues.corriger(self._set(), par_id["v1#qtrad"], trad["reponses"])
        self.assertEqual(v["verdict"], langues.JUSTE)

    def test_liste_sans_traduction(self):
        paquet = {"langue": "Anglais", "exercices": ["decouverte", "production", "reconnaissance", "definition_saisie", "ecoute_choix"],
                  "vocabulaire": [{"id": "a", "mot": "reliable", "definition": "that can be trusted"},
                                  {"id": "b", "mot": "thrifty", "definition": "careful with money"}]}
        par_id = {e.id: e for e in self._set(paquet).exercices}
        # Sans traduction : pas de carte FR ; « reconnaissance » montre la définition.
        self.assertEqual(sorted(par_id), ["a#defm", "a#qson", "a#rec", "b#defm", "b#qson", "b#rec"])
        self.assertEqual(par_id["a#rec"].donnees["verso"], "that can be trusted")
        self.assertEqual(par_id["a#rec"].etiquette, "Vocabulaire · mot → définition (EN → EN)")
        qson = par_id["a#qson"].donnees
        self.assertEqual(qson["choix"][qson["reponses"][0]], "that can be trusted")
        with self.assertRaisesMessage(ValueError, "aucune carte de vocabulaire possible"):
            self._set({**paquet, "exercices": ["decouverte", "production"]})

    def test_session_et_hors_ligne(self):
        self.write("QCM/Anglais/mots.json", json.dumps(self.PAQUET))
        page = self.client.get("/qcm/langues/Anglais/jouer/", {"mode": "quotidien"}).content.decode()
        self.assertIn("v1#def", page)
        s = quiz.get_library().langues["QCM/Anglais/mots"]
        from wiki.langues_views import payload_hors_ligne
        exo = next(e for e in s.exercices if e.id == "v2#qson")
        p = payload_hors_ligne(get_vault(), s, exo)
        self.assertEqual((p["forme"], p["ecoute"], p["indice"]), ("choix", True, "a kitchen"))
        self.assertEqual(p["choix"][p["reponses"][0]], "une cuisine")
        # Les nouveaux types sont proposés partout où l'on choisit les cartes.
        self.assertContains(self.client.get("/qcm/mon-espace/"), 'value="definition_saisie"')
        self.assertContains(self.client.get("/qcm/mon-espace/"), 'value="langue_def"')

    def test_import_mot_puis_definition(self):
        reponse = self.client.post("/qcm/mon-espace/", {
            "action": "liste", "ordre": "langue_def", "langue": "anglais", "titre": "Adjectifs",
            "cartes": ["decouverte", "production", "contexte"],
            "liste": "reliable\tthat can be trusted\tShe is very [reliable].\nthrifty / frugal\tcareful with money\n"})
        self.assertEqual(reponse.status_code, 302, reponse.content)
        fichier = next((Path(settings.DATA_DIR) / "perso/lecteur/Vocabulaire").glob("*.json"))
        paquet = json.loads(fichier.read_text(encoding="utf-8"))
        # Cartes de traduction impossibles sans traduction : seule la phrase à compléter reste.
        self.assertEqual(paquet["exercices"], ["contexte"])
        self.assertEqual(paquet["vocabulaire"][0]["definition"], "that can be trusted")
        self.assertEqual(paquet["vocabulaire"][1]["variantes"], ["frugal"])
        # Rien de compatible coché : les cartes de définition par défaut ; virgules dans la définition.
        from wiki import paquets
        fiches, ignorees = paquets.analyser_liste("reliable, that can be trusted, dependable\n", paquets.MOT_PUIS_DEFINITION)
        self.assertEqual((fiches, ignorees), ([{"mot": "reliable", "definition": "that can be trusted, dependable"}], 0))
        self.client.post("/qcm/mon-espace/", {"action": "liste", "ordre": "langue_def", "cartes": ["production"],
                                               "liste": "thrifty\tcareful with money", "titre": "Autre"})
        autre = json.loads((Path(settings.DATA_DIR) / "perso/lecteur/Vocabulaire/autre.json").read_text(encoding="utf-8"))
        self.assertEqual(autre["exercices"], ["definition", "definition_choix", "definition_saisie"])

    def test_claude_et_anki(self):
        from wiki import anki, claude
        self.assertIn("definition", claude.SCHEMA_VOCABULAIRE["properties"]["vocabulaire"]["items"]["required"])
        self.assertIn("definition", claude.CONSIGNE_VOCABULAIRE)
        paquet = {"langue": "Anglais", "vocabulaire": [{"id": "a", "mot": "reliable", "definition": "that can be trusted"},
                                                       {"id": "b", "mot": "a kitchen", "traductions": ["une cuisine"],
                                                        "definition": "the room where food is cooked"}]}
        notes = anki.notes_langue(self._set(paquet), paquet)
        self.assertEqual(notes[0][2], "that can be trusted")
        self.assertIn("<i>the room where food is cooked</i>", notes[1][2])
