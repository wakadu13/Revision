"""QCM : bibliothèque, sessions, import, rangement, hors ligne, export Anki, signalements,
FSRS, activité et examen blanc, espace personnel, images masquées, listes de mots."""

import json
import tempfile
from pathlib import Path
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone

from wiki import claude_demandes, quiz

from .base import QuizBase, WikiTestCase


class QuizTests(QuizBase):
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
        from django.utils import timezone

        from wiki.models import QuizProgress
        # q-qcm en boîte 5, révisée à l'instant → pas due ; les autres jamais vues → dues.
        QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-qcm", box=5,
                                    last_review=timezone.now(), seen=1, correct=1)
        response = self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=review")
        ids = {q["id"] for q in response.context["questions"]}
        self.assertNotIn("q-qcm", ids)
        self.assertEqual(len(ids), 3)

    def test_intensive_mode(self):
        from django.utils import timezone

        from wiki.models import QuizProgress
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

        from wiki import fsrs, planning
        neuves = [(None, 0, 0)] * 4
        # Réponses toujours justes : découverte (stabilité 3 j), révision 3 jours plus tard
        # → stabilité > 7 j, sue : 4 jours, 8 réponses.
        self.assertEqual(planning.simuler(neuves, 4, 4, 1.0), (4, 8))
        # Un quota de nouvelles plus faible rallonge la durée ; un quota épuisé aujourd'hui décale d'un jour.
        self.assertGreater(planning.simuler(neuves, 1, 4, 1.0)[0], 4)
        self.assertEqual(planning.simuler(neuves, 4, 4, 1.0, deja=(4, 0))[0], 5)
        # Des révisions plafonnées ralentissent aussi ; une question déjà stable est sue d'emblée.
        self.assertGreater(planning.simuler(neuves, 4, 1, 1.0)[0], 4)
        self.assertEqual(planning.simuler([(fsrs.Etat(7.0, 5.0), 0, 0)], 1, 1, 1.0), (0, 0))
        # Examen proche : rétention visée plus haute, révisions plus serrées, donc plus nombreuses.
        self.assertGreater(planning.simuler(neuves, 4, 4, 1.0, retention=0.95)[1], 8)

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


class QuizImportTests(QuizBase):
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


class QuizRangementTests(QuizBase):
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


class QuizHorsLigneTests(QuizBase):
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
        self.assertContains(sw, 'importScripts("/static/wiki/qcm_attente.js?v=')
        self.assertIn("connect-src 'self' https://cdn.jsdelivr.net", sw["Content-Security-Policy"])
        manifest = self.client.get("/qcm/manifest.webmanifest").json()
        self.assertEqual((manifest["start_url"], manifest["scope"]), ("/qcm/hors-ligne/", "/qcm/"))


class ExportAnkiTests(TestCase):
    def setUp(self):
        QuizTests.setUp(self)

    def test_apkg(self):
        import io
        import sqlite3
        import tempfile
        import zipfile
        r = self.client.get("/qcm/exporter/", {"set": self.SET if hasattr(self, "SET") else "reseaux/test_set"})
        self.assertEqual(r.status_code, 200)
        self.assertIn('filename="set-de-test.apkg"', r["Content-Disposition"])
        archive = zipfile.ZipFile(io.BytesIO(r.content))
        self.assertEqual(sorted(archive.namelist()), ["collection.anki2", "media"])
        with tempfile.TemporaryDirectory() as d:
            chemin = Path(d) / "c.anki2"
            chemin.write_bytes(archive.read("collection.anki2"))
            base = sqlite3.connect(chemin)
            self.assertEqual(base.execute("SELECT count(*) FROM notes").fetchone()[0], 4)
            # Flashcard et QRC : carte inversée en plus.
            self.assertEqual(base.execute("SELECT count(*) FROM cards").fetchone()[0], 5)
            champs = [f.split("\x1f") for (f,) in base.execute("SELECT flds FROM notes ORDER BY id")]
            self.assertIn("2+2 ?", champs[0][0])
            self.assertIn("B. 4", champs[0][1])
            self.assertIn("Paris", champs[2][1])
            col = base.execute("SELECT ver, models, decks FROM col").fetchone()
            self.assertEqual(col[0], 11)
            import json
            self.assertEqual(len(json.loads(col[1])), 2)
            self.assertIn("ProjetPluri::Set de test", json.dumps(json.loads(col[2]), ensure_ascii=False))
            base.close()
        # Deux exports : mêmes identifiants (Anki met à jour au lieu de dupliquer).
        self.assertEqual(self.client.get("/qcm/exporter/", {"set": "reseaux/test_set"}).content[:4], b"PK\x03\x04")
        self.assertEqual(self.client.get("/qcm/exporter/", {"set": "inconnu"}).status_code, 404)

    def test_tsv_et_formatage(self):
        from wiki import anki
        r = self.client.get("/qcm/exporter/", {"set": "reseaux/test_set", "format": "tsv"})
        lignes = r.content.decode().splitlines()
        self.assertEqual(len(lignes), 4)
        self.assertTrue(lignes[0].startswith("2+2 ? A. 3 B. 4\t"), lignes[0])
        self.assertEqual(lignes[3], "chat\tcat")
        self.assertEqual(anki.formater("Soit $x^2$ et **gras** `code`"), "Soit \\(x^2\\) et <b>gras</b> <code>code</code>")
        self.assertEqual(anki.formater("a <b> c\nd"), "a &lt;b&gt; c<br>d")


class SignalementTests(TestCase):
    SET = "reseaux/test_set"

    def setUp(self):
        QuizTests.setUp(self)

    def _signaler(self, question="q-qcm", commentaire="La réponse est fausse"):
        import json
        return self.client.post("/qcm/signaler/", data=json.dumps(
            {"set_id": self.SET, "question_id": question, "commentaire": commentaire}), content_type="application/json")

    def _admin(self):
        self.user.is_staff = True
        self.user.save()

    def test_signaler_et_lister(self):
        from wiki.models import Signalement
        self.assertContains(self.client.get("/qcm/jouer/?set=reseaux/test_set&mode=all"), "data-signaler-url")
        self.assertEqual(self._signaler().json(), {"ok": True, "nouveau": True})
        self.assertEqual(self._signaler(commentaire="Ambiguë").json()["nouveau"], False)
        self.assertEqual(Signalement.objects.get().commentaire, "Ambiguë")
        self.assertEqual(self._signaler(question="nope").status_code, 404)
        self.assertEqual(self.client.get("/qcm/signalements/").status_code, 403)
        self.assertNotContains(self.client.get("/qcm/"), "Signalements")
        self._admin()
        self.assertContains(self.client.get("/qcm/"), "Signalements <b>(1)</b>")
        page = self.client.get("/qcm/signalements/")
        self.assertContains(page, "Ambiguë")
        self.assertContains(page, "2+2 ?")
        self.assertContains(page, "Retirer la question")

    def test_retirer_et_clore(self):
        import json

        from wiki.models import Signalement
        from wiki.quiz import get_library
        # Set sans identifiants explicites : ceux des questions suivantes sont figés.
        (self.root / "reseaux" / "sans_id.json").write_text(json.dumps({"titre": "Sans id", "questions": [
            {"type": "FLASHCARD", "question": "a", "verso": "A"}, {"type": "FLASHCARD", "question": "b", "verso": "B"},
            {"type": "FLASHCARD", "question": "c", "verso": "C"}]}), encoding="utf-8")
        self.client.post("/qcm/signaler/", data=json.dumps({"set_id": "reseaux/sans_id", "question_id": "q2", "commentaire": ""}),
                         content_type="application/json")
        self._admin()
        pk = Signalement.objects.get().pk
        r = self.client.post("/qcm/signalements/", {"pk": pk, "action": "retirer"})
        self.assertRedirects(r, "/qcm/signalements/")
        data = json.loads((self.root / "reseaux" / "sans_id.json").read_text(encoding="utf-8"))
        self.assertEqual([q["question"] for q in data["questions"]], ["a", "c"])
        self.assertEqual(data["questions"][1]["id"], "q3")
        self.assertEqual([q.id for q in get_library().get("reseaux/sans_id").questions], ["q1", "q3"])
        self.assertTrue(Signalement.objects.get().traite)
        # Clore sans toucher au set.
        self._signaler()
        pk = Signalement.objects.get(traite=False).pk
        self.client.post("/qcm/signalements/", {"pk": pk, "action": "clore"})
        self.assertEqual(Signalement.objects.filter(traite=False).count(), 0)
        self.assertEqual(len(get_library().get(self.SET).questions), 4)

    def test_correction_par_claude(self):
        import json
        from unittest.mock import patch

        from wiki.models import Signalement
        from wiki.quiz import get_library
        self._signaler()
        self._admin()
        pk = Signalement.objects.get().pk
        self.assertContains(self.client.post("/qcm/signalements/", {"pk": pk, "action": "proposer"}, follow=True), "Pas de clé")
        nouvelle = {"type": "QCM", "question": "Combien font 2 + 2 ?", "choix": ["3", "4"], "reponses": [1], "explication": "Addition."}
        with patch("wiki.claude.disponible", return_value=True), \
             patch("wiki.claude_demandes.corriger_question", return_value=(nouvelle, "Énoncé reformulé.", (10, 5), "claude-opus-5-5")) as corr:
            page = self.client.post("/qcm/signalements/", {"pk": pk, "action": "proposer"}, follow=True)
        self.assertEqual(corr.call_args.args[1].id, "q-qcm")
        self.assertEqual(corr.call_args.args[2], ["La réponse est fausse"])
        self.assertContains(page, "Correction proposée par Claude")
        self.assertContains(page, "Énoncé reformulé.")
        self.assertContains(page, "Combien font 2 + 2 ?")
        self.client.post("/qcm/signalements/", {"pk": pk, "action": "appliquer"})
        data = json.loads((self.root / "reseaux" / "test_set.json").read_text(encoding="utf-8"))
        self.assertEqual(data["questions"][0], {"id": "q-qcm", **nouvelle})
        self.assertEqual(get_library().get(self.SET).questions[0].enonce, "Combien font 2 + 2 ?")
        self.assertTrue(Signalement.objects.get().traite)

    def test_schema_et_json_question(self):
        from wiki import claude
        self.assertIn("modification", claude_demandes.SCHEMA_CORRECTION["required"])
        from wiki.quiz import get_library
        q = get_library().get(self.SET).questions[0]
        self.assertEqual(claude.question_en_json(q)["question"], "2+2 ?")


class PageQcmTests(TestCase):
    def setUp(self):
        QuizTests.setUp(self)

    def test_panneau_reviser_la_page(self):
        import json
        (self.root / "Cours").mkdir()
        (self.root / "Cours" / "Signal.md").write_text("# Signal\n\nTexte.\n", encoding="utf-8")
        (self.root / "reseaux" / "signal.json").write_text(json.dumps({
            "titre": "Signal — QCM", "source_page": "Cours/Signal",
            "questions": [{"id": "s1", "type": "FLASHCARD", "question": "a", "verso": "A"}]}), encoding="utf-8")
        page = self.client.get("/wiki/Cours/Signal")
        self.assertContains(page, "Réviser ce cours")
        self.assertContains(page, "Signal — QCM")
        self.assertContains(page, "Réviser (1)")
        self.assertContains(self.client.get("/qcm/"), "D'après la page <a href=\"/wiki/Cours/Signal\">")
        self.assertContains(page, 'href="/qcm/#')


class FsrsQcmTests(TestCase):
    """QCM planifiés par FSRS : échéances, progression ancienne (Leitner), examen par
    catégorie, ajustement automatique, prévisions."""

    def setUp(self):
        QuizTests.setUp(self)

    def _reponse(self, qid, correct=True, **extra):
        import json
        return self.client.post("/qcm/reponse/", data=json.dumps({"set_id": "reseaux/test_set", "question_id": qid,
                                                                  "correct": correct, **extra}), content_type="application/json")

    def test_record_fixe_une_echeance_fsrs(self):
        from datetime import timedelta

        from django.utils import timezone

        from wiki.models import QuizProgress
        r = self._reponse("q-qcm").json()
        p = QuizProgress.objects.get(question_id="q-qcm")
        self.assertAlmostEqual(p.stabilite, 3.126, places=3)
        self.assertEqual((p.box, p.oublis, p.last_correct), (1, 0, True))
        self.assertIsNotNone(p.decouverte)
        self.assertGreaterEqual(p.echeance, p.last_review + timedelta(days=1))
        self.assertEqual(r["stabilite"], p.stabilite)
        self.assertFalse(p.is_due())
        # Ratée : revient dans 10 minutes, un oubli de plus.
        self._reponse("q-qcm", correct=False)
        p.refresh_from_db()
        self.assertEqual((p.box, p.oublis, p.last_correct), (0, 1, False))
        self.assertEqual(p.echeance, p.last_review + timedelta(minutes=10))
        self.assertFalse(p.is_due())
        self.assertTrue(p.is_due(timezone.now() + timedelta(minutes=11)))
        # Priorité : les plus menacées d'oubli d'abord.
        self.assertLess(p.urgence(timezone.now() + timedelta(days=30)), p.urgence())

    def test_progression_ancienne_leitner(self):
        from datetime import timedelta

        from django.utils import timezone

        from wiki.models import QuizProgress
        il_y_a = timezone.now() - timedelta(days=10)
        # Ligne d'avant FSRS : boîte 3 (intervalle 7 jours), sans échéance → due selon Leitner.
        p = QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-qcm", box=3,
                                        seen=3, correct=3, last_review=il_y_a, premiere_revue=il_y_a)
        self.assertTrue(p.is_due())
        self.assertAlmostEqual(p.urgence(), 0.6)
        self._reponse("q-qcm")
        p.refresh_from_db()
        # Stabilité estimée d'après la boîte (7 j) puis révision réussie : elle grandit.
        self.assertGreater(p.stabilite, 7)
        self.assertEqual(p.box, 4)
        self.assertGreater(p.echeance, timezone.now() + timedelta(days=7))
        self.assertIsNone(p.decouverte)  # déjà apprise avant FSRS
        summary = self.client.get("/qcm/").context["categories"][0]["sets"][0]["summary"]
        self.assertIsNotNone(summary["retention"])
        self.assertGreater(summary["pct_maitrise"], 0)

    def test_retention_visee_avant_examen(self):
        from datetime import timedelta

        from django.utils import timezone

        from wiki import fsrs, planning
        from wiki.models import QuizDeck, QuizProgress
        auj = timezone.localdate()
        self.assertEqual(planning.retention_cible(None, timezone.now()), fsrs.RETENTION)
        self.assertEqual(planning.retention_cible(auj + timedelta(days=60), timezone.now()), fsrs.RETENTION)
        self.assertEqual(planning.retention_cible(auj + timedelta(days=10), timezone.now()), planning.RETENTION_EXAMEN)
        self.assertEqual(planning.retention_cible(auj - timedelta(days=1), timezone.now()), fsrs.RETENTION)
        # Examen dans 10 jours : même réponse, échéance plus proche.
        self._reponse("q-qcr")
        loin = QuizProgress.objects.get(question_id="q-qcr").echeance
        QuizDeck.objects.create(player="alice", set_id="reseaux/test_set", date_objectif=auj + timedelta(days=10))
        self._reponse("q-trou")
        pres = QuizProgress.objects.get(question_id="q-trou").echeance
        self.assertLess(pres, loin)

    def test_examen_par_categorie_et_ajustement_auto(self):
        import json
        from datetime import timedelta

        from django.utils import timezone

        from wiki.models import QuizDeck
        (self.root / "reseaux" / "autre.json").write_text(json.dumps({"titre": "Autre", "questions": [
            {"id": "a1", "type": "FLASHCARD", "question": "a", "verso": "A"}]}), encoding="utf-8")
        (self.root / "reseaux" / "grand.json").write_text(json.dumps({"titre": "Grand", "questions": [
            {"id": f"g{i}", "type": "FLASHCARD", "question": f"q{i}", "verso": "r"} for i in range(12)]}), encoding="utf-8")
        auj = timezone.localdate()
        r = self.client.post("/qcm/planning/", {"categorie": "reseaux", "langue": "", "date_objectif": str(auj + timedelta(days=20))}, follow=True)
        self.assertContains(r, "pour les 3 sets de « reseaux »")
        self.assertEqual(sorted(str(d.date_objectif) for d in QuizDeck.objects.filter(player="alice")),
                         [str(auj + timedelta(days=20))] * 3)
        self.assertContains(r, f'value="{auj + timedelta(days=20):%Y-%m-%d}"')
        self.assertEqual(self.client.post("/qcm/planning/", {"categorie": "inconnue", "date_objectif": ""}).status_code, 404)
        # Ajustement automatique : 1 nouvelle par jour (22 jours estimés) ne suffit pas pour
        # 12 questions en 14 jours ; l'estimation conseille 3 par jour, appliquées à la file.
        self.client.post("/qcm/planning/", {"set": "reseaux/grand", "nouvelles_jour": "1",
                                            "date_objectif": str(auj + timedelta(days=14)), "auto": "1"})
        deck = QuizDeck.objects.get(player="alice", set_id="reseaux/grand")
        self.assertTrue(deck.auto_quota)
        ids = [q["id"] for q in self.client.get("/qcm/jouer/?set=reseaux/grand&mode=review").context["questions"]]
        self.assertEqual(len(ids), 3)
        page = self.client.get("/qcm/")
        self.assertContains(page, "Ajustement automatique : 3 nouvelles par jour")
        self.assertContains(page, "name=\"auto\" value=\"1\" checked")
        # Sans date, l'ajustement ne s'applique pas.
        self.client.post("/qcm/planning/", {"set": "reseaux/grand", "nouvelles_jour": "1", "auto": "1"})
        deck.refresh_from_db()
        self.assertFalse(deck.auto_quota)
        ids = [q["id"] for q in self.client.get("/qcm/jouer/?set=reseaux/grand&mode=review").context["questions"]]
        self.assertEqual(len(ids), 1)

    def test_previsions_et_telechargement(self):
        from datetime import timedelta

        from django.utils import timezone

        from wiki.models import QuizProgress
        now = timezone.now()
        QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-qcm", seen=1, correct=1,
                                    stabilite=3.0, difficulte=5.0, last_review=now - timedelta(days=1), echeance=now + timedelta(days=2))
        QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-qcr", seen=1, correct=1,
                                    stabilite=3.0, difficulte=5.0, last_review=now - timedelta(days=5), echeance=now - timedelta(days=2))
        QuizProgress.objects.create(player="alice", set_id="reseaux/test_set", question_id="q-trou", box=2, seen=1, correct=1,
                                    last_review=now - timedelta(days=1))  # Leitner : due dans 2 jours
        QuizProgress.objects.create(player="alice", set_id="disparu", question_id="x", seen=1, stabilite=1.0, echeance=now,
                                    last_review=now)
        response = self.client.get("/qcm/stats/")
        self.assertContains(response, "Révisions à venir")
        previsions = response.context["previsions"]
        self.assertEqual(len(previsions), 14)
        self.assertEqual((previsions[0]["n"], previsions[2]["n"], response.context["previsions_total"]), (1, 2, 3))
        self.assertContains(response, "<th>Rétention</th>")
        data = self.client.get("/qcm/hors-ligne/sets/", {"id": "reseaux/test_set"}).json()
        p = data["sets"][0]["progression"]["q-qcm"]
        self.assertEqual((p["stabilite"], p["oublis"]), (3.0, 0))
        self.assertTrue(p["echeance"])
        self.assertContains(self.client.get("/qcm/hors-ligne/"), "fsrs.js")
        self.assertContains(self.client.get("/qcm/sw.js"), "fsrs.js")


class ActiviteExamenTests(WikiTestCase):
    """Série de jours, calendrier d'activité et examen blanc."""

    SET = {"titre": "Signal", "questions": [
        {"id": "q1", "type": "QCM", "question": "2+2 ?", "choix": ["3", "4"], "reponses": [1], "explication": "Addition."},
        {"id": "q2", "type": "TROU", "question": "Le _____ apparaît", "reponses_texte": ["repliement"]},
        {"id": "q3", "type": "QCR", "question": "Pairs ?", "choix": ["1", "2", "4"], "reponses": [1, 2]},
        {"id": "q4", "type": "FLASHCARD", "question": "Shannon", "verso": "f_e > 2 f_max"},
    ]}

    def setUp(self):
        super().setUp()
        self.write("QCM/Cours/signal.json", json.dumps(self.SET))

    def post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type="application/json")

    def test_streak_and_calendar(self):
        from datetime import date, timedelta

        from wiki.models import Activite

        auj = date(2026, 11, 9)  # un lundi
        for d in (0, 1, 2, 5, 6, 7, 8, 40):
            Activite.objects.create(player="lecteur", jour=auj - timedelta(days=d), reponses=d + 1, justes=1)
        self.assertEqual(Activite.serie("lecteur", auj), (3, 4))
        # Rien aujourd'hui mais hier : la série tient encore.
        Activite.objects.filter(player="lecteur", jour=auj).delete()
        self.assertEqual(Activite.serie("lecteur", auj), (2, 4))
        self.assertEqual(Activite.serie("personne", auj), (0, 0))
        grille = Activite.calendrier("lecteur", auj, semaines=4)
        self.assertEqual(len(grille), 4)
        self.assertTrue(all(len(s) == 7 for s in grille))
        self.assertEqual(grille[0][0]["jour"].weekday(), 0)
        self.assertEqual(grille[-1][0]["jour"], auj)  # dernière semaine : celle d'aujourd'hui
        self.assertTrue(grille[-1][1]["futur"])
        hier = grille[-2][6]
        self.assertEqual((hier["reponses"], hier["niveau"]), (2, 1))
        self.assertEqual([sum(n >= p for p in Activite.PALIERS) for n in (0, 1, 10, 30, 60)], [0, 1, 2, 3, 4])
        resume = Activite.resume("lecteur", auj)
        self.assertEqual((resume["serie"], resume["record"], resume["aujourdhui"]), (2, 4, 0))
        self.assertEqual(resume["trente_jours"], sum(d + 1 for d in (1, 2, 5, 6, 7, 8)))
        self.assertEqual(resume["jours_actifs_trente"], 6)

    def test_answers_feed_the_activity_log(self):
        from datetime import timedelta

        from wiki.models import Activite

        self.post_json("/qcm/reponse/", {"set_id": "QCM/Cours/signal", "question_id": "q1", "correct": True})
        self.post_json("/qcm/reponse/", {"set_id": "QCM/Cours/signal", "question_id": "q1", "correct": False})
        a = Activite.objects.get(player="lecteur", jour=timezone.localdate())
        self.assertEqual((a.reponses, a.justes, a.nouveaux), (2, 1, 1))
        # Réponse hors ligne synchronisée : comptée à sa date.
        avant_hier = timezone.now() - timedelta(days=2)
        self.post_json("/qcm/hors-ligne/synchro/", {"reponses": [
            {"uid": "u1", "set_id": "QCM/Cours/signal", "question_id": "q2", "correct": True, "date": avant_hier.isoformat()}]})
        self.assertEqual(Activite.objects.get(player="lecteur", jour=timezone.localdate(avant_hier)).reponses, 1)
        # Module Langues.
        self.write("QCM/langues/en.json", json.dumps({"langue": "Anglais", "vocabulaire": [{"id": "v1", "mot": "a job", "traductions": ["un emploi"]}]}))
        self.post_json("/qcm/langue/reponse/", {"set_id": "QCM/langues/en", "exo_id": "v1#rec", "note": 3})
        a.refresh_from_db()
        self.assertEqual((a.reponses, a.nouveaux), (3, 2))
        self.assertContains(self.client.get("/qcm/"), "1 jour d'affilée")
        stats = self.client.get("/qcm/stats/").content.decode()
        self.assertIn("jour d'affilée", stats)
        self.assertEqual(stats.count('class="quiz-jour'), 26 * 7 + 5)  # grille + légende
        self.assertIn("3 réponses, 2 justes", stats)

    def test_exam_mode(self):
        response = self.client.get("/qcm/jouer/", {"set": "QCM/Cours/signal", "mode": "examen"})
        self.assertEqual(response.context["titre"], "Examen blanc · Signal")
        types = [q["type"] for q in response.context["questions"]]
        self.assertEqual(sorted(types), ["QCM", "QCR", "TROU"])  # pas de flashcard
        self.assertEqual((response.context["duree_min"], response.context["total_dispo"]), (3, 3))
        self.assertContains(response, 'data-mode="examen" data-duree="180"')
        self.assertContains(response, "sans correction avant la fin")
        response = self.client.get("/qcm/jouer/", {"set": "QCM/Cours/signal", "mode": "examen", "n": "2", "duree": "500"})
        self.assertEqual((len(response.context["questions"]), response.context["duree_min"]), (2, 180))
        response = self.client.get("/qcm/jouer/", {"categorie": "Cours", "mode": "examen", "n": "99"})
        self.assertEqual((response.context["titre"], len(response.context["questions"])), ("Examen blanc · Cours", 3))
        self.assertEqual(self.client.get("/qcm/jouer/", {"categorie": "Inconnue", "mode": "examen"}).status_code, 404)
        index = self.client.get("/qcm/").content.decode()
        self.assertIn("set=QCM/Cours/signal&mode=examen", index)
        self.assertIn("categorie=Cours&mode=examen", index)


class ImportVocabulaireTests(WikiTestCase):
    """Paquets de vocabulaire d'après une liste collée ou un export (Quizlet, Anki, tableur)."""

    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.client.force_login(self.admin)

    def test_parser(self):
        from wiki import paquets

        quizlet = "a job\tun emploi, un travail\nto achieve\tréussir; atteindre\n\ncolour / color\tcouleur\n"
        fiches, ignorees = paquets.analyser_liste(quizlet)
        self.assertEqual(fiches, [
            {"mot": "a job", "traductions": ["un emploi", "un travail"]},
            {"mot": "to achieve", "traductions": ["réussir", "atteindre"]},
            {"mot": "colour", "traductions": ["couleur"], "variantes": ["color"]},
        ])
        self.assertEqual(ignorees, 0)
        anki = "#separator:tab\n#html:true\n<b>a kitchen</b>&nbsp;\tune cuisine\tThe <i>kitchen</i> is clean.\tPièce\nseul\n"
        fiches, ignorees = paquets.analyser_liste(anki)
        self.assertEqual(fiches, [{"mot": "a kitchen", "traductions": ["une cuisine"], "exemple": "The kitchen is clean.", "note": "Pièce"}])
        self.assertEqual(ignorees, 1)
        tableur = '"un emploi","a job"\n"cuisiner, faire la cuisine","to cook"\n'
        fiches, _ = paquets.analyser_liste(tableur, paquets.FR_PUIS_LANGUE)
        self.assertEqual(fiches, [{"mot": "a job", "traductions": ["un emploi"]},
                                  {"mot": "to cook", "traductions": ["cuisiner", "faire la cuisine"]}])
        fiches, _ = paquets.analyser_liste("to run = courir\nto eat = manger")
        self.assertEqual([f["mot"] for f in fiches], ["to run", "to eat"])
        fiches, _ = paquets.analyser_liste("mot;traduction\n")
        self.assertEqual(fiches, [{"mot": "mot", "traductions": ["traduction"]}])
        with self.assertRaisesMessage(paquets.PaquetInvalide, "Trop de lignes"):
            paquets.analyser_liste("\n".join(f"m{i}\tt{i}" for i in range(501)))

    def test_import_creates_a_separate_pack(self):
        index = self.client.get("/qcm/").content.decode()
        self.assertIn('id="importer-vocabulaire"', index)
        reponse = self.client.post("/qcm/importer-vocabulaire/", {
            "liste": "a job\tun emploi\nto achieve\tréussir, atteindre\n", "ordre": "langue_fr", "langue": "anglais",
            "cartes": ["decouverte", "dictee"], "titre": "Métiers", "dossier": "Quizlet",
        })
        self.assertRedirects(reponse, "/qcm/langues/Anglais/?fichier=QCM%2FQuizlet%2Fmetiers", fetch_redirect_response=False)
        paquet = json.loads((self.root / "QCM/Quizlet/metiers.json").read_text(encoding="utf-8"))
        self.assertEqual(paquet["langue"], "Anglais")
        self.assertEqual(paquet["exercices"], ["decouverte", "dictee"])
        self.assertEqual(paquet["origine"], "Import de liste")
        self.assertEqual(paquet["particules_optionnelles"], ["to", "a", "an", "the"])
        self.assertEqual([(f["id"], f["mot"]) for f in paquet["vocabulaire"]], [("metiers-001", "a job"), ("metiers-002", "to achieve")])
        s = quiz.get_library().langues["QCM/Quizlet/metiers"]
        self.assertEqual([e.id for e in s.exercices], ["metiers-001#dec", "metiers-001#dict", "metiers-002#dec", "metiers-002#dict"])
        self.assertContains(self.client.get("/qcm/langues/Anglais/", {"fichier": "QCM/Quizlet/metiers"}), "Métiers")
        # Fichier envoyé, ordre inverse, titre par défaut.
        fichier = SimpleUploadedFile("export.csv", "un emploi,a job\r\ncuisiner,to cook\r\n".encode("utf-8-sig"))
        reponse = self.client.post("/qcm/importer-vocabulaire/", {"fichier": fichier, "ordre": "fr_langue", "cartes": ["production"]},
                                   follow=True)
        self.assertContains(reponse, "2 mots")
        fichiers = sorted(p.name for p in (self.root / "QCM/Vocabulaire").glob("*.json"))
        self.assertEqual(len(fichiers), 1)
        paquet = json.loads((self.root / "QCM/Vocabulaire" / fichiers[0]).read_text(encoding="utf-8"))
        self.assertEqual([f["mot"] for f in paquet["vocabulaire"]], ["a job", "to cook"])
        self.assertTrue(paquet["titre"].startswith("Vocabulaire anglais du "))

    def test_import_errors_and_permissions(self):
        for donnees, message in [
            ({"liste": "", "cartes": ["production"]}, "Aucune ligne"),
            ({"liste": "a job\tun emploi", "cartes": []}, "Cochez au moins un type de carte"),
            ({"liste": "a job\tun emploi", "cartes": ["production"], "langue": "x/y"}, "Langue invalide"),
            ({"liste": "a job\tun emploi", "cartes": ["production"], "dossier": "a/b"}, "Dossier invalide"),
        ]:
            with self.subTest(message=message):
                self.assertContains(self.client.post("/qcm/importer-vocabulaire/", donnees, follow=True), message)
        self.assertFalse((self.root / "QCM").exists())
        self.client.force_login(self.reader)
        self.assertEqual(self.client.post("/qcm/importer-vocabulaire/", {"liste": "a\tb", "cartes": ["production"]}).status_code, 403)
        self.assertNotIn("importer-vocabulaire", self.client.get("/qcm/").content.decode())


class EspacePersoTests(QuizBase):
    """Espace personnel : chaque compte importe ses sets et listes de mots, visibles de lui seul."""

    def setUp(self):
        super().setUp()
        self.data = tempfile.TemporaryDirectory()
        self.addCleanup(self.data.cleanup)
        override = override_settings(DATA_DIR=Path(self.data.name))
        override.enable()
        self.addCleanup(override.disable)
        self.bob = get_user_model().objects.create_user("bob", password="x")
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)

    def _set(self, titre="Mes verbes"):
        return {"titre": titre, "questions": [
            {"id": "v1", "type": "QCM", "question": "be → ?", "choix": ["was", "is"], "reponses": [0]},
            {"id": "v2", "type": "FLASHCARD", "question": "go", "verso": "went"}]}

    def _importer(self, nom="verbes.json", contenu=None, **champs):
        fichier = SimpleUploadedFile(nom, json.dumps(contenu or self._set()).encode())
        return self.client.post("/qcm/mon-espace/", {"action": "json", "fichiers": [fichier], **champs}, follow=True)

    def _repondre(self, set_id, question_id="v1"):
        return self.client.post("/qcm/reponse/", {"set_id": set_id, "question_id": question_id, "correct": True},
                                content_type="application/json")

    def test_set_importe_visible_de_son_seul_proprietaire(self):
        reponse = self._importer()
        self.assertContains(reponse, "« Mes verbes » importé dans votre espace, dossier « Mes sets » (2 questions).")
        self.assertTrue((Path(self.data.name) / "perso/alice/Mes sets/verbes.json").is_file())
        self.assertFalse((self.root / "QCM").exists())
        set_id = "~alice/Mes sets/verbes"
        index = self.client.get("/qcm/").content.decode()
        self.assertIn("Mes verbes", index)
        self.assertIn("🔒 perso", index)
        self.assertEqual(self.client.get("/qcm/jouer/", {"set": set_id}).status_code, 200)
        self.assertEqual(self._repondre(set_id).status_code, 200)
        self.assertEqual(self.client.get("/qcm/exporter/", {"set": set_id}).status_code, 200)
        catalogue = self.client.get("/qcm/hors-ligne/catalogue/").json()
        self.assertIn(set_id, [s["id"] for s in catalogue["sets"]])
        self.assertContains(self.client.get("/qcm/mon-espace/"), "Mes verbes")
        # Un autre compte, même admin, ne le voit nulle part.
        for compte in (self.bob, self.admin):
            with self.subTest(compte=compte.username):
                self.client.force_login(compte)
                self.assertNotIn("Mes verbes", self.client.get("/qcm/").content.decode())
                self.assertNotIn("Mes verbes", self.client.get("/qcm/mon-espace/").content.decode())
                self.assertEqual(self.client.get("/qcm/jouer/", {"set": set_id}).status_code, 404)
                self.assertEqual(self._repondre(set_id).status_code, 404)
                self.assertEqual(self.client.get("/qcm/exporter/", {"set": set_id}).status_code, 404)
                catalogue = self.client.get("/qcm/hors-ligne/catalogue/").json()
                self.assertNotIn(set_id, [s["id"] for s in catalogue["sets"]])
                telecharge = self.client.get("/qcm/hors-ligne/sets/", {"id": set_id}).json()
                self.assertEqual(telecharge["sets"], [])
                reponse = self.client.post("/qcm/mon-espace/", {"action": "supprimer", "set": set_id})
                self.assertEqual(reponse.status_code, 404)
        # Les outils de rangement des admins ne touchent pas aux espaces personnels.
        self.client.force_login(self.admin)
        self.client.post("/qcm/supprimer/", {"set": set_id})
        self.client.post("/qcm/deplacer/", {"set": set_id, "dossier": "Ailleurs"})
        self.assertTrue((Path(self.data.name) / "perso/alice/Mes sets/verbes.json").is_file())

    def test_liste_de_mots_dans_son_espace(self):
        reponse = self.client.post("/qcm/mon-espace/", {
            "action": "liste", "liste": "a job\tun emploi\nto run\tcourir\n", "ordre": "langue_fr",
            "langue": "anglais", "cartes": ["decouverte", "production"], "titre": "Métiers"})
        set_id = "~alice/Vocabulaire/metiers"
        self.assertRedirects(reponse, "/qcm/langues/Anglais/?fichier=%7Ealice%2FVocabulaire%2Fmetiers", fetch_redirect_response=False)
        paquet = json.loads((Path(self.data.name) / "perso/alice/Vocabulaire/metiers.json").read_text(encoding="utf-8"))
        self.assertEqual([f["mot"] for f in paquet["vocabulaire"]], ["a job", "to run"])
        self.assertContains(self.client.get("/qcm/langues/Anglais/", {"fichier": set_id}), "Métiers")
        self.assertIn(set_id, [s["id"] for s in self.client.get("/qcm/hors-ligne/catalogue/").json()["langues"]])
        self.assertContains(self.client.get("/qcm/exporter/", {"set": set_id, "format": "tsv"}), "a job")
        self.client.force_login(self.bob)
        # Pour bob, l'anglais n'existe même pas (aucun paquet commun dans cette langue).
        self.assertEqual(self.client.get("/qcm/langues/Anglais/").status_code, 404)
        self.assertNotIn(set_id, [s["id"] for s in self.client.get("/qcm/hors-ligne/catalogue/").json()["langues"]])
        # Erreurs de saisie : messages comme pour l'import des admins.
        self.assertContains(self.client.post("/qcm/mon-espace/", {"action": "liste", "liste": "", "cartes": ["production"]},
                                             follow=True), "Aucune ligne")

    def test_suppression_et_progression(self):
        from wiki.models import QuizProgress
        self._importer()
        set_id = "~alice/Mes sets/verbes"
        self._repondre(set_id)
        self.assertTrue(QuizProgress.objects.filter(set_id=set_id).exists())
        reponse = self.client.post("/qcm/mon-espace/", {"action": "supprimer", "set": set_id}, follow=True)
        self.assertContains(reponse, "« Mes verbes » supprimé de votre espace.")
        self.assertFalse((Path(self.data.name) / "perso/alice/Mes sets").exists())
        self.assertFalse(QuizProgress.objects.filter(set_id=set_id).exists())
        self.assertEqual(self.client.get("/qcm/jouer/", {"set": set_id}).status_code, 404)

    def test_signalement_refuse_et_json_invalide(self):
        self._importer()
        reponse = self.client.post("/qcm/signaler/", {"set_id": "~alice/Mes sets/verbes", "question_id": "v1"},
                                   content_type="application/json")
        self.assertEqual(reponse.status_code, 400)
        reponse = self._importer("faux.json", {"titre": "x", "questions": [{"type": "QCM"}]})
        self.assertFalse((Path(self.data.name) / "perso/alice/Mes sets/faux.json").exists())
        self.assertNotContains(reponse, "importé dans votre espace")
        # Un fichier abîmé à la main est signalé à son seul propriétaire.
        (Path(self.data.name) / "perso/alice/Mes sets/abime.json").write_text("{", encoding="utf-8")
        from wiki.vault import invalider
        invalider()
        self.assertContains(self.client.get("/qcm/mon-espace/"), "abime.json")
        self.client.force_login(self.bob)
        self.assertNotContains(self.client.get("/qcm/"), "abime.json")

    def test_quota(self):
        from wiki import qcm_gestion_views
        with mock.patch.object(qcm_gestion_views, "MAX_FICHIERS_PERSO", 1):
            self._importer()
            reponse = self._importer("autre.json", self._set("Autre"))
        self.assertContains(reponse, "Votre espace est plein")
        self.assertFalse((Path(self.data.name) / "perso/alice/Mes sets/autre.json").exists())

    def test_nom_de_dossier_sur(self):
        self.assertEqual(quiz.nom_perso("jean/../x"), "jean_.._x")
        self.assertEqual(quiz.nom_perso("é.a@b+c-d"), "é.a@b+c-d")


class ImageMasqueeTests(QuizBase):
    """Cartes à image masquée : format MASQUE, rendu des cartes, éditeur de zones."""

    ZONES = [{"id": "z1", "x": 10, "y": 20, "l": 30, "h": 10, "reponse": "Aorte"},
             {"id": "z2", "x": 50, "y": 60, "l": 20, "h": 15, "reponse": "Ventricule gauche"}]

    def setUp(self):
        super().setUp()
        self.data = tempfile.TemporaryDirectory()
        self.addCleanup(self.data.cleanup)
        override = override_settings(DATA_DIR=Path(self.data.name))
        override.enable()
        self.addCleanup(override.disable)
        (self.root / "Images").mkdir()
        (self.root / "Images/coeur.png").write_bytes(self._png())
        self.admin = get_user_model().objects.create_user("admin", password="x", is_staff=True)
        self.bob = get_user_model().objects.create_user("bob", password="x")

    @staticmethod
    def _png(couleur="red"):
        import io

        from PIL import Image
        tampon = io.BytesIO()
        Image.new("RGB", (40, 30), couleur).save(tampon, "PNG")
        return tampon.getvalue()

    def _set(self, **question):
        q = {"id": "coeur", "type": "MASQUE", "image": "coeur.png", "zones": self.ZONES, **question}
        (self.root / "Bio").mkdir(exist_ok=True)
        (self.root / "Bio/coeur.json").write_text(json.dumps({"titre": "Le cœur", "questions": [q]}), encoding="utf-8")
        from wiki.vault import invalider
        invalider()

    def test_une_carte_par_zone(self):
        self._set(masquer_tout=False)
        qset = quiz.get_library().get("Bio/coeur")
        self.assertTrue(qset.est_masque)
        self.assertEqual([(q.id, q.type, q.verso) for q in qset.questions],
                         [("coeur#z1", "FLASHCARD", "Aorte"), ("coeur#z2", "FLASHCARD", "Ventricule gauche")])
        self.assertEqual(qset.questions[0].enonce, "Que cache la zone colorée ?")
        page = self.client.get("/qcm/jouer/", {"set": "Bio/coeur", "mode": "all"}).content.decode()
        self.assertIn('src=\\"/fichiers/Images/coeur.png\\"', page)
        self.assertIn('x=\\"10.0%\\" y=\\"20.0%\\" width=\\"30.0%\\" height=\\"10.0%\\" rx=\\"3\\" class=\\"masque-cible\\"', page)
        self.assertNotIn("masque-autre", page)  # autres zones visibles
        self._set(masquer_tout=True)
        self.assertIn("masque-autre", self.client.get("/qcm/jouer/", {"set": "Bio/coeur", "mode": "all"}).content.decode())
        # Les réponses comptent comme celles des flashcards ; l'export Anki les laisse de côté (images).
        r = self.client.post("/qcm/reponse/", {"set_id": "Bio/coeur", "question_id": "coeur#z2", "note": "bien"},
                             content_type="application/json")
        self.assertEqual(r.status_code, 200)
        from wiki import anki
        self.assertEqual(anki.notes_qcm(qset), [])
        self.assertContains(self.client.get("/qcm/"), "🖼 Image masquée")

    def test_validation(self):
        for question, message in [
            ({"image": ""}, "'image' manquante"),
            ({"zones": []}, "au moins une zone"),
            ({"zones": [{"x": 10, "y": 10, "l": 5, "h": 5}]}, "'reponse' manquante"),
            ({"zones": [{"x": 120, "y": 10, "l": 5, "h": 5, "reponse": "a"}]}, "hors de l'image"),
            ({"zones": [{"x": "a", "y": 10, "l": 5, "h": 5, "reponse": "a"}]}, "x, y, l et h"),
            ({"zones": [dict(self.ZONES[0]), dict(self.ZONES[0])]}, "en double"),
        ]:
            with self.subTest(message=message):
                self._set(**question)
                self.assertTrue(any(message in e for e in quiz.get_library().errors), quiz.get_library().errors)
        # Zone qui déborde : ramenée dans l'image ; image introuvable : signalée dans la carte.
        self._set(image="absente.png", zones=[{"x": 90, "y": 95, "l": 30, "h": 30, "reponse": "a"}])
        q = quiz.get_library().get("Bio/coeur").questions[0]
        self.assertEqual((q.masque["zones"][0]["l"], q.masque["zones"][0]["h"]), (10, 5))
        self.assertContains(self.client.get("/qcm/jouer/", {"set": "Bio/coeur", "mode": "all"}), "Image introuvable : absente.png")

    def _enregistrer(self, **champs):
        donnees = {"titre": "Le cœur", "question": "", "masquer_tout": "1", "zones": json.dumps(self.ZONES), **champs}
        return self.client.post("/qcm/image-masquee/", donnees)

    def test_editeur_dans_mon_espace(self):
        self.assertContains(self.client.get("/qcm/image-masquee/"), "masque.js")
        r = self._enregistrer(fichier=SimpleUploadedFile("Mon schéma.png", self._png()), destination="coffre")
        self.assertEqual(r.status_code, 403)  # le coffre est réservé aux admins
        r = self._enregistrer(fichier=SimpleUploadedFile("Mon schéma.png", self._png()), dossier="Bio")
        self.assertEqual(r.status_code, 200, r.content)
        donnees = r.json()
        self.assertEqual((donnees["set"], donnees["image"]), ("~alice/Bio/le-coeur", "perso:mon-schema.png"))
        self.assertEqual(donnees["message"], "« Le cœur » enregistré : 2 cartes.")
        perso = Path(self.data.name) / "perso/alice"
        self.assertTrue((perso / "_images/mon-schema.png").is_file())
        contenu = json.loads((perso / "Bio/le-coeur.json").read_text(encoding="utf-8"))
        self.assertEqual(contenu["questions"][0]["image"], "perso:mon-schema.png")
        # L'image n'est servie qu'à son propriétaire ; la carte la montre.
        self.assertEqual(self.client.get("/qcm/mon-espace/images/mon-schema.png").status_code, 200)
        page = self.client.get("/qcm/jouer/", {"set": "~alice/Bio/le-coeur", "mode": "all"}).content.decode()
        self.assertIn("/qcm/mon-espace/images/mon-schema.png", page)
        self.assertContains(self.client.get("/qcm/mon-espace/"), "🖼 Zones")
        # Modification : mêmes fichier et identifiants, zones changées.
        self.assertContains(self.client.get("/qcm/image-masquee/", {"set": "~alice/Bio/le-coeur"}), "Ventricule gauche")
        zones = [dict(self.ZONES[0], reponse="Aorte (crosse)")]
        r = self._enregistrer(set="~alice/Bio/le-coeur", image="perso:mon-schema.png", zones=json.dumps(zones), masquer_tout="0")
        self.assertEqual(r.json()["set"], "~alice/Bio/le-coeur")
        qset = quiz.get_library().pour("alice").get("~alice/Bio/le-coeur")
        self.assertEqual([q.verso for q in qset.questions], ["Aorte (crosse)"])
        self.assertFalse(qset.questions[0].masque["tout"])
        # Un autre compte : ni l'image, ni le set, ni l'éditeur.
        self.client.force_login(self.bob)
        self.assertEqual(self.client.get("/qcm/mon-espace/images/mon-schema.png").status_code, 404)
        self.assertEqual(self.client.get("/qcm/image-masquee/", {"set": "~alice/Bio/le-coeur"}).status_code, 404)
        self.assertEqual(self._enregistrer(set="~alice/Bio/le-coeur", image="perso:mon-schema.png").status_code, 404)

    def test_editeur_admin_et_erreurs(self):
        self.client.force_login(self.admin)
        r = self._enregistrer(image="coeur.png", destination="coffre", dossier="Bio")
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual(r.json()["set"], "QCM/Bio/le-coeur")
        self.assertTrue((self.root / "QCM/Bio/le-coeur.json").is_file())
        page = self.client.get("/qcm/").content.decode()
        self.assertIn("🖼 Modifier les zones", page)
        # Image envoyée dans le coffre : rangée comme les pièces jointes (racine par défaut).
        r = self._enregistrer(fichier=SimpleUploadedFile("schema.png", self._png("blue")), destination="coffre", titre="Autre")
        self.assertEqual(r.json()["image"], "schema.png")
        self.assertTrue((self.root / "schema.png").is_file())
        for champs, message in [
            ({"zones": json.dumps([dict(self.ZONES[0], reponse="")])}, "'reponse' manquante"),
            ({"image": ""}, "Choisissez une image"),
            ({"image": "absente.png"}, "Image introuvable dans le coffre"),
            ({"image": "perso:x.png", "destination": "coffre"}, "ne peut servir qu'à un set de votre espace"),
            ({"titre": " "}, "Donnez un titre"),
            ({"fichier": SimpleUploadedFile("faux.png", b"pas une image")}, "pas une image lisible"),
            ({"fichier": SimpleUploadedFile("page.svg", b"<svg/>")}, "PNG, JPEG, WebP ou GIF"),
        ]:
            with self.subTest(message=message):
                r = self._enregistrer(**{"image": "coeur.png", **champs})
                self.assertEqual(r.status_code, 400)
                self.assertIn(message, r.json()["error"])
