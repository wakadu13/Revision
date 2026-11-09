"""Lit le texte des PDF du coffre (nouveaux ou modifiés) pour la recherche et
« Demander au wiki ». Le wiki le fait aussi tout seul, en arrière-plan, à la première
recherche ; la commande sert à tout préparer d'un coup (après un gros import)."""

from django.core.management.base import BaseCommand

from wiki import texte_pdf
from wiki.models import TextePdf
from wiki.vault import get_vault


class Command(BaseCommand):
    help = "Extrait le texte des PDF du coffre pour la recherche."

    def handle(self, *args, **options):
        n = texte_pdf.indexer(get_vault())
        erreurs = TextePdf.objects.exclude(erreur="")
        self.stdout.write(f"{n} PDF lu{'s' if n > 1 else ''} ; {TextePdf.objects.count()} dans l'index.")
        for t in erreurs:
            self.stdout.write(f"  illisible : {t.chemin} ({t.erreur})")
