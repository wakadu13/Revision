"""Éditeur de cartes à image masquée : choisir une image du coffre ou en envoyer une,
tracer les zones, les nommer. Le set est écrit dans l'espace personnel (tout compte)
ou dans le coffre, sous QCM/<dossier>/ (admins)."""

import json
from pathlib import PurePosixPath
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from . import masque, paquets, quiz
from .quiz_views import (DOSSIER_QCM, MAX_FICHIERS_PERSO, MAX_OCTETS_PERSO, _can_edit, _ctx, _fichiers_perso,
                         _taille_perso, bibliotheque, player_id)
from .vault import Attachment, clean_key, get_vault, invalider

DOSSIER_DEFAUT = "Images masquées"


def _peut_modifier(request, qset):
    if qset.proprietaire:
        return qset.proprietaire == quiz.nom_perso(player_id(request))
    return _can_edit(request)


def _question_masque(donnees):
    return next((q for q in donnees.get("questions", []) if isinstance(q, dict) and str(q.get("type", "")).upper() == "MASQUE"), None)


def _images_perso(player):
    dossier = quiz.dossier_perso(player) / masque.DOSSIER_IMAGES_PERSO
    if not dossier.is_dir():
        return []
    return [{"lien": masque.PERSO_IMAGE + f.name, "dossier": "Mon espace", "url": reverse("wiki:quiz_perso_image", args=[f.name])}
            for f in sorted(dossier.iterdir(), key=lambda f: f.name.lower()) if f.suffix.lower() in masque.FORMATS]


@login_required
def editeur(request):
    """Page de l'éditeur (GET, ``?set=`` pour modifier) ; enregistrement (POST, réponse JSON)."""
    player = player_id(request)
    vault = get_vault()
    existant = None
    set_id = request.GET.get("set") or request.POST.get("set") or ""
    if set_id:
        existant = bibliotheque(request).get(set_id)
        if existant is None or not existant.est_masque:
            raise Http404("Set inconnu")
        if not _peut_modifier(request, existant):
            raise PermissionDenied
    if request.method == "POST":
        return _enregistrer(request, vault, player, existant)
    donnees = None
    if existant is not None:
        _, contenu = quiz.lire_json(existant.fichier, existant.fichier.parent)
        q = _question_masque(contenu) or {}
        donnees = {"set": existant.id, "titre": existant.titre, "question": q.get("question", ""), "image": q.get("image", ""),
                   "image_url": masque.url_image(vault, existant, str(q.get("image", ""))),
                   "masquer_tout": bool(q.get("masquer_tout", True)), "zones": q.get("zones", []),
                   "jouer": reverse("wiki:quiz_play") + "?" + urlencode({"set": existant.id, "mode": "all"})}
    images = [{"lien": a["link"], "dossier": a["folder"], "url": a["url"]} for a in vault.attachment_choices(masque.FORMATS)]
    dossiers = sorted({s.categorie for s in bibliotheque(request).sets.values() if s.est_masque} | {DOSSIER_DEFAUT}, key=str.lower)
    return render(request, "wiki/quiz_masque.html", _ctx(
        request, donnees=donnees, images=_images_perso(player) + images, dossiers=dossiers,
        enonce_defaut=masque.ENONCE_DEFAUT, max_zones=masque.MAX_ZONES))


def _enregistrer(request, vault, player, existant):
    def erreur(message):
        return JsonResponse({"error": message}, status=400)

    try:
        zones = json.loads(request.POST.get("zones", "[]"))
    except ValueError:
        return erreur("Zones illisibles.")
    titre = " ".join(request.POST.get("titre", "").split())[:120]
    if not titre:
        return erreur("Donnez un titre au set.")
    enonce = " ".join(request.POST.get("question", "").split())[:300] or masque.ENONCE_DEFAUT
    if existant is not None:
        destination = "perso" if existant.proprietaire else "coffre"
    else:
        destination = request.POST.get("destination", "perso")
        if destination not in ("perso", "coffre"):
            destination = "perso"
        if destination == "coffre" and not _can_edit(request):
            raise PermissionDenied
    dossier = clean_key(request.POST.get("dossier", "").strip() or DOSSIER_DEFAUT)
    if dossier is None or "/" in dossier:
        return erreur('Dossier invalide : un seul nom, sans / \\ : * ? " < > | # ^ [ ].')
    perso_racine = quiz.dossier_perso(player)
    if destination == "perso" and existant is None and (
            len(_fichiers_perso(player)) >= MAX_FICHIERS_PERSO or _taille_perso(player) >= MAX_OCTETS_PERSO):
        return erreur(f"Votre espace est plein ({MAX_FICHIERS_PERSO} fichiers, {MAX_OCTETS_PERSO // 2**20} Mo) : supprimez-en d'abord.")

    image = request.POST.get("image", "").strip()
    fichier = request.FILES.get("fichier")
    if fichier is not None:
        try:
            if destination == "perso":
                if _taille_perso(player) + fichier.size > MAX_OCTETS_PERSO:
                    return erreur(f"Votre espace est plein ({MAX_OCTETS_PERSO // 2**20} Mo).")
                image = masque.PERSO_IMAGE + masque.enregistrer_image(fichier, perso_racine / masque.DOSSIER_IMAGES_PERSO)
            else:
                dossier_images = vault.attachment_folder(f"{DOSSIER_QCM}/{dossier}/schema")
                nom = masque.enregistrer_image(fichier, vault.root / dossier_images if dossier_images else vault.root)
                image = f"{dossier_images}/{nom}" if dossier_images else nom
                invalider()
                vault = get_vault()
        except ValueError as e:
            return erreur(str(e))
    if not image:
        return erreur("Choisissez une image.")
    if image.startswith(masque.PERSO_IMAGE):
        if destination != "perso":
            return erreur("Une image de votre espace ne peut servir qu'à un set de votre espace.")
        if not (perso_racine / masque.DOSSIER_IMAGES_PERSO / image[len(masque.PERSO_IMAGE):]).is_file():
            return erreur("Image introuvable dans votre espace.")
    elif not isinstance(vault.resolve(image), Attachment):
        return erreur(f"Image introuvable dans le coffre : {image}")

    question = {"id": "masque", "type": "MASQUE", "question": enonce, "image": image,
                "masquer_tout": request.POST.get("masquer_tout") == "1", "zones": zones}
    if existant is not None:
        _, contenu = quiz.lire_json(existant.fichier, existant.fichier.parent)
        ancienne = _question_masque(contenu)
        contenu["titre"] = titre
        contenu["questions"] = [question if q is ancienne else q for q in contenu.get("questions", [])]
    else:
        contenu = {"titre": titre, "description": "Cartes à image masquée.", "questions": [question]}
    try:
        quiz.set_depuis_json(contenu, PurePosixPath("set.json"))
    except ValueError as e:
        return erreur(str(e).replace("set.json » ", "").replace("question #1 » ", ""))

    if existant is not None:
        cible = existant.fichier
    elif destination == "perso":
        cible = perso_racine / dossier / masque.nom_libre(perso_racine / dossier, (paquets.slug(titre) or "image-masquee") + ".json")
    else:
        cible = vault.root / paquets.chemin_libre(dossier, titre, "image-masquee")
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(json.dumps(contenu, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    invalider()
    qset = next((s for s in quiz.get_library().pour(player).sets.values() if s.fichier == cible), None)
    if qset is None:
        return erreur("Set enregistré mais introuvable : rechargez la page.")
    n = len(zones)
    return JsonResponse({
        "ok": True, "set": qset.id, "image": image,
        "image_url": masque.url_image(get_vault(), qset, image),
        "jouer": reverse("wiki:quiz_play") + "?" + urlencode({"set": qset.id, "mode": "all"}),
        "message": f"« {titre} » enregistré : {n} carte{'s' if n > 1 else ''}.",
    })


@login_required
def image_perso(request, nom):
    """Image de l'espace personnel du compte connecté (seul lui la voit)."""
    if "/" in nom or "\\" in nom or nom.startswith("."):
        raise Http404
    chemin = quiz.dossier_perso(player_id(request)) / masque.DOSSIER_IMAGES_PERSO / nom
    if chemin.suffix.lower() not in masque.FORMATS or not chemin.is_file():
        raise Http404
    reponse = FileResponse(open(chemin, "rb"))
    reponse["Cache-Control"] = "private, max-age=86400"
    return reponse
