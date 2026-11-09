"""« Corriger ma copie » : photos d'une copie manuscrite (1 à 4 pages), énoncé et page du
cours facultatifs ; Claude (Sonnet) corrige étape par étape. Photos allégées gardées
hors du coffre (DATA_DIR/copies/<compte>/), visibles de leur seul auteur."""

import io
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from . import claude, quiz
from .models import CorrectionCopie, UsageClaude
from .quiz_views import _render_html, player_id
from .vault import get_vault
from .views import _render

MAX_PHOTOS = 4
TAILLE_MAX_PHOTO = 15 * 1024 * 1024
COTE_MAX = 1568  # au-delà, l'API réduit l'image de toute façon
GARDER = 30  # corrections gardées par compte


def _dossier(player):
    return Path(settings.DATA_DIR) / "copies" / quiz.nom_perso(player)


def preparer_photo(fichier):
    """JPEG allégé (côté ≤ COTE_MAX, orientation de l'appareil appliquée) ; ValueError si illisible."""
    from PIL import Image, ImageOps, UnidentifiedImageError

    if fichier.size > TAILLE_MAX_PHOTO:
        raise ValueError(f"{fichier.name} : photo trop grosse (15 Mo au plus).")
    try:
        with Image.open(fichier) as image:
            image = ImageOps.exif_transpose(image)
            image.thumbnail((COTE_MAX, COTE_MAX), Image.Resampling.LANCZOS)
            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")
            tampon = io.BytesIO()
            image.save(tampon, "JPEG", quality=85, optimize=True)
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError):
        raise ValueError(f"{fichier.name} : ce n'est pas une photo lisible (JPEG, PNG ou WebP).") from None
    return tampon.getvalue()


def _bloc(vault, c):
    return {"c": c, "html": _render_html(vault, c.correction), "page": vault.notes.get(c.page.lower()) if c.page else None,
            "photos": range(c.photos)}


def _oublier_anciennes(player):
    for ancienne in CorrectionCopie.objects.filter(player=player)[GARDER:]:
        _supprimer(ancienne)


def _supprimer(c):
    for n in range(c.photos):
        (_dossier(c.player) / f"{c.pk}-{n}.jpg").unlink(missing_ok=True)
    c.delete()


@login_required
def copie(request):
    """Page « Corriger ma copie » (GET) ; correction d'une copie envoyée (POST, réponse JSON)."""
    player = player_id(request)
    vault = get_vault()
    if request.method != "POST":
        cle = request.GET.get("page", "")
        return _render(request, vault, "wiki/copie.html", {
            "dispo": claude.disponible(), "plafond": claude.plafond_atteint(), "max_photos": MAX_PHOTOS,
            "page": vault.notes.get(cle.lower()) if cle else None,
            "pages": sorted((n.key for n in vault.notes.values()), key=str.lower),
            "corrections": [_bloc(vault, c) for c in CorrectionCopie.objects.filter(player=player)[:GARDER]],
        })
    if not claude.disponible():
        return JsonResponse({"error": "Pas de clé d'API Claude sur le serveur."}, status=503)
    if claude.plafond_atteint():
        return JsonResponse({"error": "Plafond mensuel de Claude atteint : réessayez le mois prochain."}, status=429)
    fichiers = request.FILES.getlist("photos")
    if not fichiers:
        return JsonResponse({"error": "Ajoutez au moins une photo de la copie."}, status=400)
    if len(fichiers) > MAX_PHOTOS:
        return JsonResponse({"error": f"{MAX_PHOTOS} photos au plus."}, status=400)
    try:
        photos = [preparer_photo(f) for f in fichiers]
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    enonce = request.POST.get("enonce", "").strip()[:4000]
    cle = request.POST.get("page", "").strip().removesuffix(".md")
    note = vault.notes.get(cle.lower()) if cle else None
    if cle and note is None:
        return JsonResponse({"error": f"Page inconnue : {cle}"}, status=400)
    cours = (vault.root / note.path).read_text(encoding="utf-8", errors="replace") if note else ""
    try:
        texte, usage, modele_id = claude.corriger_copie(photos, enonce, cours, note.title if note else "")
    except claude.Echec as e:
        return JsonResponse({"error": str(e)}, status=502)
    c = CorrectionCopie.objects.create(player=player, enonce=enonce, page=note.key if note else "", photos=len(photos),
                                       correction=texte, modele=modele_id, jetons_entree=usage[0], jetons_sortie=usage[1])
    dossier = _dossier(player)
    dossier.mkdir(parents=True, exist_ok=True)
    for n, photo in enumerate(photos):
        (dossier / f"{c.pk}-{n}.jpg").write_bytes(photo)
    claude.noter_usage(UsageClaude.COPIE, player, modele_id, usage)
    _oublier_anciennes(player)
    return JsonResponse({"bloc": render_to_string("wiki/_copie.html", {"b": _bloc(vault, c), "ouvert": True}, request)})


@login_required
def photo(request, pk, n):
    c = get_object_or_404(CorrectionCopie, pk=pk, player=player_id(request))
    chemin = _dossier(c.player) / f"{c.pk}-{n}.jpg"
    if n >= c.photos or not chemin.is_file():
        raise Http404
    reponse = FileResponse(open(chemin, "rb"), content_type="image/jpeg")
    reponse["Cache-Control"] = "private, max-age=86400"
    return reponse


@require_POST
@login_required
def supprimer(request, pk):
    c = get_object_or_404(CorrectionCopie, pk=pk, player=player_id(request))
    _supprimer(c)
    return JsonResponse({"ok": True})
