"""Lecture hors ligne du wiki (PWA) : service worker à la racine, manifeste, page
« hors connexion », pages et PDF d'un dossier à garder sur l'appareil."""

from django.conf import settings
from django.contrib.auth.decorators import login_not_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.csp import CSP
from django.views.decorators.csp import csp_override

from .render import IMAGE_EXTS
from .vault import get_vault


@login_not_required
@csp_override({**settings.SECURE_CSP, "connect-src": [CSP.SELF, settings.CDN]})
def sw_wiki(request):
    """Service worker du wiki entier (sans secret), servi à la racine pour contrôler tout le site."""
    response = render(request, "wiki/sw_wiki.js", content_type="text/javascript; charset=utf-8")
    response["Cache-Control"] = "no-cache"
    return response


@login_not_required
def manifest_wiki(request):
    """Manifeste de l'application installable : le wiki entier (écran d'accueil d'un téléphone, iPhone compris)."""
    import json

    from django.templatetags.static import static

    data = {
        "name": "ProjetPluri", "short_name": "ProjetPluri",
        "description": "Le wiki de révision : cours, PDF, QCM, lisible même sans connexion.",
        "start_url": "/", "scope": "/", "display": "standalone", "background_color": "#ffffff",
        "theme_color": "#7852ee", "lang": "fr",
        "icons": [
            {"src": static("wiki/icone-192.png"), "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": static("wiki/icone-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/manifest+json")


@login_not_required
def hors_connexion(request):
    """Page servie par le service worker quand une page n'est ni accessible ni en cache."""
    return render(request, "wiki/hors_connexion.html")


def dossier_hors_ligne(request):
    """Adresses à mettre en cache pour lire un dossier sans connexion : ses pages, images et PDF."""
    vault = get_vault()
    dossier = request.GET.get("dossier", "").replace("\\", "/").strip("/")
    prefixe = f"{dossier}/" if dossier else ""
    pages = [n.url for n in vault.sorted_notes() if n.path.as_posix().startswith(prefixe)]
    fichiers, pdf = [], 0
    for a in sorted(vault.attachments.values(), key=lambda a: str(a.path).lower()):
        if not a.path.as_posix().startswith(prefixe) or a.suffix not in IMAGE_EXTS | {".pdf"}:
            continue
        fichiers.append(a.url)
        if a.suffix == ".pdf":
            fichiers.append(a.view_url)
            pdf += 1
    if not pages and not fichiers:
        raise Http404("Dossier introuvable ou vide")
    return JsonResponse({"dossier": dossier, "urls": pages + fichiers, "pages": len(pages), "pdf": pdf})
