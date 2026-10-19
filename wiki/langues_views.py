"""Vues du module Langues : menu d'une langue, sessions, correction, statistiques.

Comme pour les QCM, l'exercice se déroule dans le navigateur (quiz_langue.js) :
la vue « jouer » fournit la session pré-rendue en JSON. La correction des
réponses tapées (tolérance, différences surlignées) est faite ici, par
langues.corriger, et la révision est enregistrée quand on quitte l'exercice
(la touche F peut entre-temps la passer en « Facile »).
"""

import json
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import fsrs, langues, quiz
from .models import QuizProgress
from .quiz_views import _ctx, _render_html, player_id
from .vault import get_vault

TAILLE_MAX_SESSION = 200


def dossier_de(set_langue):
    """Dossier d'un fichier de langue : le nom du dossier qui le contient."""
    return (set_langue.path.parent.name if set_langue.path else "") or quiz.CATEGORIE_DEFAUT


def _sets(langue, dossier=""):
    """Fichiers d'une langue, restreints à un dossier si `dossier` est donné."""
    sets = quiz.get_library().sets_langue(langue)
    if dossier:
        sets = [s for s in sets if dossier_de(s) == dossier]
    if not sets:
        raise Http404("Langue introuvable")
    return sets


def _url_menu(langue, dossier=""):
    url = reverse("wiki:langue_menu", args=[langue])
    return f"{url}?{urlencode({'dossier': dossier})}" if dossier else url


def resume_langue(player, langue, sets, now):
    """Résumé d'une langue pour la page des QCM : à revoir, nouveaux disponibles."""
    return langues.resume(sets, QuizProgress.map_langue(player, sets), now)


@login_required
def menu(request, langue):
    dossier = request.GET.get("dossier", "")
    sets = _sets(langue, dossier)
    now = timezone.now()
    r = langues.resume(sets, QuizProgress.map_langue(player_id(request), sets), now)
    modes = [(cle, nom) for cle, nom in langues.MODES.items()
             if cle not in langues.GENRES or any(g["nom"] == nom for g in r["genres"])]
    return render(request, "wiki/langue_menu.html", _ctx(
        request, langue=langue, dossier=dossier, sets=sets, resume=r, modes=modes,
        taille=langues.TAILLE_SESSION,
    ))


def _payload(vault, item, st, now):
    """Exercice pré-rendu (HTML) pour le moteur côté navigateur. Les réponses des
    saisies restent sur le serveur, qui corrige."""
    exo, d = item.exo, item.exo.donnees

    def html(texte):
        # Rendu en ligne (Markdown + LaTeX), une ligne de texte à la fois.
        return "<br>".join(_render_html(vault, ligne, block=False) for ligne in texte.split("\n"))

    p = {
        "set_id": item.set.id,
        "exo_id": exo.id,
        "etiquette": exo.etiquette,
        "genre": exo.genre,
        "forme": exo.forme,
        "nouveau": item.nouveau,
        "details": [html(t) for t in exo.details],
    }
    if exo.forme == langues.CARTE:
        p.update(recto=html(d["recto"]), verso=html(d["verso"]),
                 previsions={str(n): t for n, t in langues.previsions(st, now).items()})
    elif exo.forme == langues.SAISIE:
        p.update(consigne=html(d["consigne"]), invite=d["invite"],
                 prerempli=d["prerempli"], tableau=d["tableau"],
                 caracteres=item.set.caracteres_speciaux)
    elif exo.forme == langues.CHOIX:
        p.update(enonce=html(d["enonce"]), choix=[html(c) for c in d["choix"]], multiple=d["multiple"])
    elif exo.forme == langues.ORDRE:
        p.update(consigne=html(d["consigne"]), mots=d["mots"], melange=item.melange)
    return p


@login_required
def play(request, langue):
    dossier = request.GET.get("dossier", "")
    sets = _sets(langue, dossier)
    mode = request.GET.get("mode", langues.QUOTIDIEN)
    if mode not in langues.MODES:
        raise Http404("Mode inconnu")
    n = request.GET.get("n", "")
    n = min(int(n), TAILLE_MAX_SESSION) if n.isdigit() and int(n) > 0 else langues.TAILLE_SESSION
    now = timezone.now()
    prog = QuizProgress.map_langue(player_id(request), sets)
    session = langues.construire_session(sets, prog, mode, n, now)
    vault = get_vault()
    payload = [_payload(vault, e, prog.get((e.set.id, e.exo.id)), now) for e in session]
    menu_url = _url_menu(langue, dossier)
    titre = f"{langues.MODES[mode]} · {langue}" + (f" · {dossier}" if dossier else "")
    return render(request, "wiki/langue_play.html", _ctx(
        request, langue=langue, titre=titre, mode=mode,
        exercices=payload, count=len(payload),
        corriger_url=reverse("wiki:langue_corriger"), record_url=reverse("wiki:langue_record"),
        back_url=menu_url,
    ))


def _exercice(data):
    """(set, exercice) désignés par la requête, ou une réponse d'erreur."""
    set_langue = quiz.get_library().langues.get(str(data.get("set_id", "")))
    exo = set_langue.exercice(str(data.get("exo_id", ""))) if set_langue else None
    if exo is None:
        return None, None, JsonResponse({"error": "exercice inconnu"}, status=404)
    return set_langue, exo, None


def _json(request):
    try:
        data = json.loads(request.body)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


@require_POST
@login_required
def corriger(request):
    """Corrige une réponse sans l'enregistrer : verdict, réponse attendue, différences."""
    data = _json(request)
    if data is None:
        return JsonResponse({"error": "requête invalide"}, status=400)
    set_langue, exo, erreur = _exercice(data)
    if erreur:
        return erreur
    reponse = data.get("reponse")
    if isinstance(reponse, list) and not all(isinstance(i, int) and not isinstance(i, bool) for i in reponse):
        return JsonResponse({"error": "requête invalide"}, status=400)
    resultat = langues.corriger(set_langue, exo, reponse)
    if resultat is None:
        return JsonResponse({"error": "réponse incomplète"}, status=400)
    if exo.forme == langues.CHOIX:
        resultat["reponses"] = exo.donnees["reponses"]
    if exo.forme == langues.SAISIE:
        resultat["autres"] = [_render_html(get_vault(), a, block=False) for a in resultat["autres"]]
    return JsonResponse(resultat)


@require_POST
@login_required
def record(request):
    """Enregistre une révision (note FSRS 1 à 4) : état FSRS et prochaine échéance."""
    data = _json(request)
    if data is None or data.get("note") not in fsrs.NOTES:
        return JsonResponse({"error": "requête invalide"}, status=400)
    set_langue, exo, erreur = _exercice(data)
    if erreur:
        return erreur
    obj, _ = QuizProgress.objects.get_or_create(
        player=player_id(request), set_id=set_langue.id, question_id=exo.id
    )
    obj.record_langue(data["note"])
    obj.save()
    return JsonResponse({"stabilite": obj.stabilite, "echeance": obj.echeance.isoformat()})


@require_POST
@login_required
def reset(request, langue):
    dossier = request.POST.get("dossier", "")
    sets = _sets(langue, dossier)
    QuizProgress.objects.filter(player=player_id(request), set_id__in=[s.id for s in sets]).delete()
    messages.success(request, f"Progression en {langue}{f' ({dossier})' if dossier else ''} réinitialisée.")
    return redirect(_url_menu(langue, dossier))
