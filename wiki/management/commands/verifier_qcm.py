from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from wiki.verifier import verifier_fichier


class Command(BaseCommand):
    help = ("Vérifie des fichiers de questions ou de langue (par exemple générés par une IA) "
            "avant de les déposer dans le coffre. Sans argument : tout vault/QCM.")

    def add_arguments(self, parser):
        parser.add_argument("chemins", nargs="*", help="fichiers .json ou dossiers")

    def handle(self, *args, chemins, **options):
        chemins = [Path(c) for c in chemins] or [Path(settings.WIKI_DIR) / "QCM"]
        fichiers = []
        for p in chemins:
            if p.is_dir():
                fichiers += [(f, p) for f in sorted(p.rglob("*.json"))
                             if not any(part.startswith(".") for part in f.relative_to(p).parts)]
            elif p.is_file():
                fichiers.append((p, p.parent))
            else:
                raise CommandError(f"Introuvable : {p}")

        invalides = 0
        for f, racine in fichiers:
            ok, resume, avert = verifier_fichier(f, racine)
            if ok:
                self.stdout.write(self.style.SUCCESS("✓ ") + str(f))
                self.stdout.write(f"    {resume}")
                for a in avert:
                    self.stdout.write(self.style.WARNING(f"    ⚠ {a}"))
            else:
                invalides += 1
                self.stdout.write(self.style.ERROR("✗ ") + str(f))
                self.stdout.write(self.style.ERROR(f"    {resume}"))

        self.stdout.write("")
        if invalides:
            raise CommandError(f"{invalides} fichier(s) invalide(s) : ils seraient ignorés par le site. "
                               "Recolle l'erreur à l'IA pour qu'elle corrige.")
        self.stdout.write(self.style.SUCCESS(f"{len(fichiers)} fichier(s) valide(s)."))
