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

from . import fsrs, quiz
from .models import Activite, QuizDeck, QuizProgress
from .langues_views import dossier_de, payload_hors_ligne
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
    library = quiz.get_library()
    sets = [{"id": s.id, "titre": s.titre, "description": s.description, "categorie": s.categorie,
             "langue": s.langue, "total": len(s)}
            for s in library.sorted_sets()]
    fichiers = [{"id": f.id, "titre": f.titre, "description": f.description, "langue": f.langue,
                 "dossier": dossier_de(f), "total": len(f), "type": "langue"}
                for _, f in sorted(library.langues.items())]
    return JsonResponse({"joueur": player_id(request), "csrf": get_token(request), "sets": sets, "langues": fichiers})


@never_cache
def telecharger(request):
    """Sets demandés (?id=…&id=…) avec questions pré-rendues, progression et quotas."""
    library = quiz.get_library()
    player = player_id(request)
    decks = QuizDeck.map_for(player)
    vault = get_vault()
    sets, manquants = [], []
    for set_id in request.GET.getlist("id")[:MAX_SETS]:
        fichier = library.langues.get(set_id)
        if fichier is not None:
            sets.append(_fichier_langue(vault, player, fichier))
            continue
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


def _fichier_langue(vault, player, fichier):
    """Fichier de langue pour l'appareil : exercices complets et état FSRS du joueur."""
    prog = QuizProgress.map_langue(player, [fichier])
    return {
        "id": fichier.id,
        "type": "langue",
        "langue": fichier.langue,
        "titre": fichier.titre,
        "description": fichier.description,
        "dossier": dossier_de(fichier),
        "code_langue": fichier.code_langue,
        "particules": fichier.particules,
        "caracteres": fichier.caracteres_speciaux,
        "nouveaux_par_jour": fichier.nouveaux_par_jour,
        "exercices": [payload_hors_ligne(vault, fichier, e) for e in fichier.exercices],
        "progression": {
            exo_id: {"stabilite": p.stabilite, "difficulte": p.difficulte, "echeance": _date_iso(p.echeance),
                     "decouverte": _date_iso(p.decouverte), "oublis": p.oublis, "last_review": _date_iso(p.last_review),
                     "last_correct": p.last_correct}
            for (_, exo_id), p in prog.items()
        },
    }


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
            if "exo_id" in r:
                # Module Langues : note FSRS 1 à 4.
                note = int(r["note"])
                if note not in fsrs.NOTES:
                    continue
                set_id, exo_id = str(r["set_id"]), str(r["exo_id"])
                fichier = library.langues.get(set_id)
                if fichier is not None and fichier.exercice(exo_id) is not None:
                    valides.append((quand, set_id, exo_id, note, None, True))
                continue
            reponse = r["note"] if r.get("note") in quiz.NOTES else bool(r["correct"])
            set_id, question_id = str(r["set_id"]), str(r["question_id"])
        except (KeyError, ValueError, TypeError):
            continue
        qset = library.get(set_id)
        if qset is not None and any(q.id == question_id for q in qset.questions):
            valides.append((quand, set_id, question_id, reponse, r.get("duree_ms"), False))

    enregistrees = 0
    for quand, set_id, question_id, reponse, duree, langue in sorted(valides, key=lambda v: v[0]):
        obj, _ = QuizProgress.objects.get_or_create(player=player, set_id=set_id, question_id=question_id)
        if obj.last_review and quand <= obj.last_review:
            continue
        if langue:
            nouveau = obj.decouverte is None
            obj.record_langue(reponse, quand)
            obj.save()
            Activite.noter(player, reponse != fsrs.A_REVOIR, nouveau=nouveau, quand=quand)
        else:
            obj.record(reponse, quand)
            obj.save()
            Activite.noter(player, obj.last_correct, nouveau=obj.seen == 1, quand=quand)
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
