"""Application Android et suivi : jeton d'appareil, application, temps de révision,
page « Aujourd'hui », notifications web."""

import tempfile
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from .base import QuizBase


class AppareilTests(TestCase):
    """Application Android : jeton d'appareil à la place de la session."""

    SET = "reseaux/test_set"

    def setUp(self):
        QuizBase.setUp(self)  # même set de test, sans hériter de ses tests
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

    def test_rappel_et_import_par_jeton(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        jeton = self._connexion().json()["jeton"]
        r = self.client.get("/api/rappel/", **self._auth(jeton)).json()
        self.assertEqual((r["a_revoir"], r["qcm"], r["serie"]), (4, 4, 0))
        # « Partager vers le wiki » depuis Android : import en JSON, réservé aux admins.
        envoi = lambda: self.client_class(enforce_csrf_checks=True).post(  # noqa: E731
            "/importer/", {"fichiers": SimpleUploadedFile("Cours.md", "# Cours\n".encode()), "chemins": "Cours.md",
                           "dossier": "Importés", "claude": "1"},
            HTTP_ACCEPT="application/json", **self._auth(jeton))
        self.assertEqual(envoi().status_code, 403)
        self.user.is_staff = True
        self.user.save()
        data = envoi().json()
        self.assertTrue(data["results"][0]["ok"], data)
        self.assertEqual(data["results"][0]["url"], "/wiki/Import%C3%A9s/Cours")
        self.assertTrue((self.root / "Importés" / "Cours.md").is_file())

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


class TempsAujourdhuiTests(TestCase):
    """Temps de révision par matière, page « Aujourd'hui », objectif du jour."""

    def setUp(self):
        QuizBase.setUp(self)

    def _reponse(self, qid, duree, correct=True):
        import json
        return self.client.post("/qcm/reponse/", data=json.dumps({"set_id": "reseaux/test_set", "question_id": qid,
                                                                  "correct": correct, "duree_ms": duree}), content_type="application/json")

    def test_temps_par_matiere(self):
        import json

        from django.utils import timezone

        from wiki.models import TempsRevision
        self._reponse("q-qcm", 30_000)
        self._reponse("q-qcr", 500_000)  # plafonné à 2 minutes
        t = TempsRevision.objects.get()
        self.assertEqual((t.matiere, t.temps_ms, t.reponses), ("reseaux", 150_000, 2))
        # Hors ligne : la durée est rejouée avec la date de la réponse.
        self.client.post("/qcm/hors-ligne/synchro/", data=json.dumps({"reponses": [
            {"uid": "a", "set_id": "reseaux/test_set", "question_id": "q-trou", "correct": True, "duree_ms": 60_000,
             "date": "2026-10-01T08:00:00Z"}]}), content_type="application/json")
        self.assertEqual(TempsRevision.objects.get(jour="2026-10-01").temps_ms, 60_000)
        semaines, lignes, totaux = TempsRevision.tableau("alice", timezone.localdate())
        self.assertEqual(len(semaines), 8)
        self.assertEqual(lignes[0]["matiere"], "reseaux")
        self.assertEqual(lignes[0]["minutes"][-1], 2)  # 2,5 min arrondies
        page = self.client.get("/qcm/stats/")
        self.assertContains(page, "Temps de révision")
        self.assertContains(page, "<td>reseaux</td>")
        self.assertEqual(TempsRevision.minutes_du_jour("alice", timezone.localdate()), 2)

    def test_page_aujourdhui(self):
        from datetime import timedelta

        from django.utils import timezone

        from wiki.models import ObjectifRevision, QuizDeck
        QuizDeck.objects.create(player="alice", set_id="reseaux/test_set", date_objectif=timezone.localdate() + timedelta(days=10))
        page = self.client.get("/aujourdhui/")
        self.assertContains(page, "Révision intelligente (4)")
        self.assertContains(page, "dans 10 jours")
        self.assertContains(page, "Set de test")
        self.assertContains(page, 'id="rappel-web"')
        self.assertContains(self.client.get("/qcm/"), 'href="/aujourdhui/"')
        # Objectif du jour.
        self.client.post("/aujourdhui/", {"objectif": "2"})
        self.assertEqual(ObjectifRevision.objects.get(player="alice").reponses_jour, 2)
        self._reponse("q-qcm", 5000)
        page = self.client.get("/aujourdhui/")
        self.assertContains(page, "<b>1 / 2</b>")
        self._reponse("q-qcr", 5000)
        self.assertContains(self.client.get("/aujourdhui/"), "Objectif du jour atteint")
        self.client.post("/aujourdhui/", {"objectif": ""})
        self.assertIsNone(ObjectifRevision.objects.get(player="alice").reponses_jour)
        # Application Android : pas de notification web (l'appli a son propre rappel).
        self.assertContains(self.client.get("/aujourdhui/", HTTP_USER_AGENT="ProjetPluriApp/2"), 'id="rappel-web" data-cle-url')
        self.assertIn(' hidden>', self.client.get("/aujourdhui/", HTTP_USER_AGENT="ProjetPluriApp/2").content.decode().split('id="rappel-web"')[1].split("\n")[1])

    def test_texte_rappel(self):
        from wiki.quiz_views import texte_rappel
        self.assertIsNone(texte_rappel({"a_revoir": 0, "serie": 3, "aujourdhui": 5}))
        self.assertEqual(texte_rappel({"a_revoir": 4, "serie": 3, "aujourdhui": 0}), "4 éléments à réviser · série de 3 jours à prolonger")
        self.assertEqual(texte_rappel({"a_revoir": 0, "serie": 0, "aujourdhui": 0}), "Rien d'urgent : quelques nouveaux mots ?")


class NotificationsWebTests(TestCase):
    """Abonnement d'un appareil aux notifications web et envoi du rappel quotidien."""

    SUB = {"endpoint": "https://push.exemple.org/abc", "keys": {"p256dh": "BOrdLfZ", "auth": "k3y"}}

    def setUp(self):
        QuizBase.setUp(self)
        self.donnees = tempfile.TemporaryDirectory()
        self.addCleanup(self.donnees.cleanup)
        override = override_settings(DATA_DIR=Path(self.donnees.name), ALLOWED_HOSTS=["testserver", "wiki.exemple.org", "192.168.1.20"])
        override.enable()
        self.addCleanup(override.disable)

    def _post(self, url, data):
        import json
        return self.client.post(url, data=json.dumps(data), content_type="application/json")

    def test_cle_abonnement_et_envoi(self):
        import base64
        from datetime import datetime
        from io import StringIO
        from unittest import mock

        from django.core.management import call_command
        from django.utils import timezone

        from wiki import push
        from wiki.models import AbonnementPush
        cle = self.client.get("/api/push/cle/").json()["cle"]
        self.assertEqual(len(base64.urlsafe_b64decode(cle + "==")), 65)  # point non compressé P-256
        self.assertTrue((Path(self.donnees.name) / "vapid_prive.pem").is_file())
        self.assertEqual(self.client.get("/api/push/cle/").json()["cle"], cle)  # clé gardée
        self.assertEqual(push.contact(), "https://wiki.exemple.org")
        self.assertEqual(self._post("/api/push/abonner/", {"subscription": {"endpoint": "http://x"}}).status_code, 400)
        with mock.patch("wiki.quiz_views.timezone.localtime", return_value=timezone.make_aware(datetime(2026, 11, 10, 8, 0))):
            r = self._post("/api/push/abonner/", {"subscription": self.SUB, "heure": 18, "minute": 30})
        self.assertEqual(r.json(), {"ok": True, "heure": 18, "minute": 30})
        a = AbonnementPush.objects.get()
        self.assertEqual((a.user.username, a.heure, a.minute, a.dernier_envoi), ("alice", 18, 30, None))
        self.assertEqual(self.client.get("/api/push/cle/").json()["abonnements"], {self.SUB["endpoint"]: {"heure": 18, "minute": 30}})
        envois = []
        with mock.patch("pywebpush.webpush", side_effect=lambda **kw: envois.append(kw)):
            # Avant l'heure : rien.
            with mock.patch("wiki.management.commands.envoyer_rappels.timezone.localtime",
                            return_value=timezone.make_aware(datetime(2026, 11, 10, 18, 0))):
                call_command("envoyer_rappels", stdout=StringIO())
            self.assertEqual(envois, [])
            # À l'heure : un rappel, une seule fois dans la journée.
            with mock.patch("wiki.management.commands.envoyer_rappels.timezone.localtime",
                            return_value=timezone.make_aware(datetime(2026, 11, 10, 18, 45))):
                call_command("envoyer_rappels", stdout=StringIO())
                call_command("envoyer_rappels", stdout=StringIO())
        self.assertEqual(len(envois), 1)
        import json
        corps = json.loads(envois[0]["data"])
        self.assertEqual(corps, {"titre": "ProjetPluri", "texte": "4 éléments à réviser", "url": "/aujourdhui/"})
        self.assertEqual(envois[0]["subscription_info"]["keys"], self.SUB["keys"])
        self.assertEqual(envois[0]["vapid_claims"], {"sub": "https://wiki.exemple.org"})
        self.assertEqual(str(AbonnementPush.objects.get().dernier_envoi), "2026-11-10")

    def test_abonnement_expire_et_test(self):
        from types import SimpleNamespace
        from unittest import mock

        from pywebpush import WebPushException

        from wiki.models import AbonnementPush
        self._post("/api/push/abonner/", {"subscription": self.SUB, "heure": 0, "minute": 0})
        with mock.patch("pywebpush.webpush") as envoi:
            self.assertEqual(self._post("/api/push/tester/", {"endpoint": self.SUB["endpoint"]}).json(), {"ok": True})
        self.assertIn("4 éléments à réviser", envoi.call_args.kwargs["data"])
        expire = WebPushException("gone", response=SimpleNamespace(status_code=410, text=""))
        with mock.patch("pywebpush.webpush", side_effect=expire):
            self.assertEqual(self._post("/api/push/tester/", {"endpoint": self.SUB["endpoint"]}).status_code, 410)
        self.assertFalse(AbonnementPush.objects.exists())
        self._post("/api/push/abonner/", {"subscription": self.SUB})
        self._post("/api/push/desabonner/", {"endpoint": self.SUB["endpoint"]})
        self.assertFalse(AbonnementPush.objects.exists())
        self.assertEqual(self._post("/api/push/tester/", {"endpoint": "x"}).status_code, 404)

    def test_service_worker_gere_les_notifications(self):
        sw = self.client.get("/sw.js").content.decode()
        self.assertIn('addEventListener("push"', sw)
        self.assertIn("notificationclick", sw)
        self.assertIn("rappel_web.js", sw)
