import tempfile

from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.test import TestCase, override_settings

User = get_user_model()


class AccountsTestCase(TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        override = override_settings(WIKI_DIR=tmp.name, SECURE_SSL_REDIRECT=False)
        override.enable()
        self.addCleanup(override.disable)


class SessionTests(AccountsTestCase):
    def setUp(self):
        super().setUp()
        User.objects.create_user("alice", password="motdepasse-solide")

    def test_login_remember_and_logout(self):
        response = self.client.post("/connexion/", {"username": "alice", "password": "motdepasse-solide", "remember": "on"})
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        self.assertFalse(self.client.session.get_expire_at_browser_close())
        self.assertContains(self.client.get("/compte/"), "alice")
        self.client.post("/deconnexion/")
        self.assertIn("/connexion/", self.client.get("/compte/")["Location"])

    def test_login_without_remember_expires_at_browser_close(self):
        self.client.post("/connexion/", {"username": "alice", "password": "motdepasse-solide"})
        self.assertTrue(self.client.session.get_expire_at_browser_close())

    def test_bad_password(self):
        response = self.client.post("/connexion/", {"username": "alice", "password": "faux"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_redirects_to_next(self):
        response = self.client.post("/connexion/", {"username": "alice", "password": "motdepasse-solide", "next": "/qcm/"})
        self.assertRedirects(response, "/qcm/", fetch_redirect_response=False)


class RegisterTests(AccountsTestCase):
    @override_settings(ACCOUNTS_REGISTRATION_OPEN=True)
    def test_register_creates_simple_user(self):
        response = self.client.post("/inscription/", {
            "username": "bob", "email": "bob@example.com",
            "password1": "un-mot-de-passe-long", "password2": "un-mot-de-passe-long",
        })
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        bob = User.objects.get(username="bob")
        self.assertFalse(bob.is_staff)
        self.assertEqual(self.client.session["_auth_user_id"], str(bob.pk))

    def test_register_closed_by_default(self):
        self.assertRedirects(self.client.get("/inscription/"), "/connexion/", fetch_redirect_response=False)
        self.client.post("/inscription/", {"username": "bob", "password1": "un-mot-de-passe-long",
                                           "password2": "un-mot-de-passe-long"})
        self.assertFalse(User.objects.filter(username="bob").exists())


class UserManagementTests(AccountsTestCase):
    def setUp(self):
        super().setUp()
        self.admin = User.objects.create_user("admin", password="x", is_staff=True)
        self.bob = User.objects.create_user("bob", password="x")

    def test_only_admins_see_user_list(self):
        self.assertIn("/connexion/", self.client.get("/utilisateurs/")["Location"])
        self.client.force_login(self.bob)
        self.assertEqual(self.client.get("/utilisateurs/").status_code, 403)
        self.assertEqual(self.client.post(f"/utilisateurs/{self.bob.pk}/", {"action": "promote"}).status_code, 403)
        self.bob.refresh_from_db()
        self.assertFalse(self.bob.is_staff)
        self.client.force_login(self.admin)
        self.assertContains(self.client.get("/utilisateurs/"), "bob")

    def test_promote_and_demote(self):
        self.client.force_login(self.admin)
        self.client.post(f"/utilisateurs/{self.bob.pk}/", {"action": "promote"})
        self.bob.refresh_from_db()
        self.assertTrue(self.bob.is_staff)
        self.client.post(f"/utilisateurs/{self.bob.pk}/", {"action": "demote"})
        self.bob.refresh_from_db()
        self.assertFalse(self.bob.is_staff)

    def test_deactivate_ends_sessions(self):
        bob_client = self.client_class()
        bob_client.force_login(self.bob)
        self.assertEqual(Session.objects.count(), 1)
        self.client.force_login(self.admin)
        self.client.post(f"/utilisateurs/{self.bob.pk}/", {"action": "deactivate"})
        self.bob.refresh_from_db()
        self.assertFalse(self.bob.is_active)
        self.assertEqual(Session.objects.count(), 1)  # seule la session de l'admin reste
        self.assertIn("/connexion/", bob_client.get("/compte/")["Location"])

    def test_cannot_change_own_account_or_superuser(self):
        root = User.objects.create_superuser("root", password="x")
        self.client.force_login(self.admin)
        self.client.post(f"/utilisateurs/{self.admin.pk}/", {"action": "demote"})
        self.client.post(f"/utilisateurs/{root.pk}/", {"action": "deactivate"})
        self.admin.refresh_from_db()
        root.refresh_from_db()
        self.assertTrue(self.admin.is_staff)
        self.assertTrue(root.is_active)

    def test_admin_creates_account(self):
        self.client.force_login(self.admin)
        self.client.post("/utilisateurs/", {
            "username": "carole", "email": "", "role": "admin",
            "password1": "un-mot-de-passe-long", "password2": "un-mot-de-passe-long",
        })
        self.assertTrue(User.objects.get(username="carole").is_staff)
        # Un utilisateur simple ne peut pas créer de compte.
        self.client.force_login(self.bob)
        self.client.post("/utilisateurs/", {
            "username": "eve", "role": "admin",
            "password1": "un-mot-de-passe-long", "password2": "un-mot-de-passe-long",
        })
        self.assertFalse(User.objects.filter(username="eve").exists())
