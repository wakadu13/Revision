"""QCM hors ligne : application installable (PWA) pour réviser sans connexion.

Le téléphone télécharge des sets (questions pré-rendues + progression) et les
garde dans le navigateur (IndexedDB). Les réponses données hors ligne sont mises
en file d'attente avec leur date, puis envoyées à la vue « synchro » dès que la
connexion revient : elles sont rejouées dans l'ordre chronologique.

Un service worker (servi sur /qcm/sw.js pour contrôler tout /qcm/) garde en
cache la page, les scripts et les feuilles de style.
"""

import json
from datetime import datetime, timezone as dt_timezone

from django.conf import settings
from django.contrib.auth.decorators import login_not_required
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.csp import CSP
from django.views.decorators.cache import never_cache
from django.views.decorators.csp import csp_override
from django.views.decorators.http import require_POST

from . import quiz
from .models import QuizDeck, QuizProgress
from .quiz_views import _question_payload, chronometrer, player_id
from .vault import get_vault

MAX_REPONSES = 5000  # par requête de synchronisation
MAX_SETS = 500       # par requête de téléchargement


def _date_iso(d):
    return d.isoformat() if d else None


@never_cache
def page(request):
    """Coquille de l'application : tout le reste se passe dans le navigateur."""
    return render(request, "wiki/quiz_hors_ligne.html")


@never_cache
def catalogue(request):
    """Sets disponibles (sans les questions), jeton CSRF et joueur connecté."""
    sets = [{"id": s.id, "titre": s.titre, "description": s.description, "categorie": s.categorie,
             "langue": s.langue, "total": len(s)}
            for s in quiz.get_library().sorted_sets()]
    return JsonResponse({"joueur": player_id(request), "csrf": get_token(request), "sets": sets})


@never_cache
def telecharger(request):
    """Sets demandés (?id=…&id=…) avec questions pré-rendues, progression et quotas."""
    library = quiz.get_library()
    player = player_id(request)
    decks = QuizDeck.map_for(player)
    vault = get_vault()
    sets, manquants = [], []
    for set_id in request.GET.getlist("id")[:MAX_SETS]:
        qset = library.get(set_id)
        if qset is None:
            manquants.append(set_id)
            continue
        progress = QuizProgress.map_for(player, qset.id)
        deck = decks.get(qset.id)
        sets.append({
            "id": qset.id,
            "titre": qset.titre,
            "description": qset.description,
            "categorie": qset.categorie,
            "langue": qset.langue,
            "questions": [_question_payload(vault, qset, q, progress) for q in qset.questions],
            "progression": {
                qid: {"box": p.box, "seen": p.seen, "correct": p.correct,
                      "last_review": _date_iso(p.last_review), "premiere_revue": _date_iso(p.premiere_revue)}
                for qid, p in progress.items()
            },
            "quotas": {"nouvelles_jour": deck.nouvelles_jour if deck else None,
                       "revisions_jour": deck.revisions_jour if deck else None},
        })
    return JsonResponse({"joueur": player, "sets": sets, "manquants": manquants})


def _date_reponse(valeur, now):
    """Date d'une réponse envoyée par le téléphone (ISO 8601), jamais dans le futur."""
    quand = datetime.fromisoformat(str(valeur))
    if timezone.is_naive(quand):
        quand = quand.replace(tzinfo=dt_timezone.utc)
    return min(quand, now)


@require_POST
def synchro(request):
    """Rejoue les réponses faites hors ligne, dans l'ordre chronologique.

    Corps : {"reponses": [{"uid", "set_id", "question_id", "correct", "note",
    "duree_ms", "date"}]}. Une réponse plus ancienne que la dernière révision
    connue de la question est ignorée : soit elle a déjà été reçue (renvoi après
    une coupure), soit la question a été revue depuis sur un autre appareil.
    Renvoie les uid traités (enregistrés ou ignorés), que le téléphone peut
    retirer de sa file d'attente.
    """
    try:
        reponses = json.loads(request.body)["reponses"]
        if not isinstance(reponses, list):
            raise TypeError
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)

    library = quiz.get_library()
    player = player_id(request)
    now = timezone.now()
    valides, traitees = [], []
    for r in reponses[:MAX_REPONSES]:
        if not isinstance(r, dict) or "uid" not in r:
            continue
        traitees.append(str(r["uid"]))
        try:
            quand = _date_reponse(r["date"], now)
            reponse = r["note"] if r.get("note") in quiz.NOTES else bool(r["correct"])
            set_id, question_id = str(r["set_id"]), str(r["question_id"])
        except (KeyError, ValueError, TypeError):
            continue
        qset = library.get(set_id)
        if qset is not None and any(q.id == question_id for q in qset.questions):
            valides.append((quand, set_id, question_id, reponse, r.get("duree_ms")))

    enregistrees = 0
    for quand, set_id, question_id, reponse, duree in sorted(valides, key=lambda v: v[0]):
        obj, _ = QuizProgress.objects.get_or_create(player=player, set_id=set_id, question_id=question_id)
        if obj.last_review and quand <= obj.last_review:
            continue
        obj.record(reponse, quand)
        obj.save()
        chronometrer(player, set_id, duree)
        enregistrees += 1
    return JsonResponse({"traitees": traitees, "enregistrees": enregistrees})


@login_not_required
# Le service worker récupère KaTeX sur le CDN pour le garder en cache.
@csp_override({**settings.SECURE_CSP, "connect-src": [CSP.SELF, settings.CDN]})
def service_worker(request):
    """Service worker (sans secret) : servi sous /qcm/ pour contrôler toutes les pages du QCM."""
    response = render(request, "wiki/sw.js", content_type="text/javascript; charset=utf-8")
    response["Cache-Control"] = "no-cache"
    return response


@login_not_required
def manifest(request):
    """Manifeste de l'application installable (écran d'accueil Android)."""
    data = {
        "name": "QCM ProjetPluri",
        "short_name": "QCM",
        "description": "Réviser les QCM du wiki, même sans connexion.",
        "start_url": reverse("wiki:quiz_offline"),
        "scope": reverse("wiki:quiz_index"),
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#7852ee",
        "lang": "fr",
        "icons": [
            {"src": static("wiki/icone-192.png"), "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": static("wiki/icone-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/manifest+json")
