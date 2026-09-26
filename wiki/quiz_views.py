"""Vues des QCM de révision : choix des sets, sessions, statistiques.

L'interaction du quiz (afficher les questions, feedback immédiat, clavier) se
fait côté navigateur : la vue « jouer » fournit les questions pré-rendues en
JSON, et chaque réponse est enregistrée via une petite requête POST.
"""

import json
import random
from pathlib import PurePosixPath

from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import quiz
from .models import _JAMAIS, QuizProgress
from .render import Renderer
from .vault import Note, get_vault


def player_id(request):
    """Identifie le « joueur » : l'utilisateur connecté, ou tout le monde sinon."""
    return request.user.get_username() if request.user.is_authenticated else ""


def _ctx(request, **extra):
    vault = get_vault()
    return {"vault": vault, "tree": vault.tree, "can_edit": _can_edit(request), **extra}


def _can_edit(request):
    from .views import can_edit
    return can_edit(request)


def _render_html(vault, text, block=True):
    """Rend un énoncé/choix (Markdown + LaTeX $...$) avec le moteur du wiki."""
    if not text:
        return ""
    renderer = Renderer(vault, Note(PurePosixPath("_qcm_.md"), 0, {}, text))
    return renderer.convert(text) if block else renderer.convert_inline(text)


def _question_payload(vault, qset, question, progress):
    """Question pré-rendue (HTML) + réponses, pour le moteur côté navigateur."""
    st = progress.get(question.id)
    return {
        "set_id": qset.id,
        "set_titre": qset.titre,
        "id": question.id,
        "type": question.type,
        "enonce": _render_html(vault, question.enonce),
        "choix": [_render_html(vault, c, block=False) for c in question.choix],
        "reponses": question.reponses,
        "reponses_texte": question.reponses_texte,
        "verso": _render_html(vault, question.verso),
        "explication": _render_html(vault, question.explication),
        "box": st.box if st else 0,
    }


def _set_summary(qset, progress, now):
    """Statistiques d'un set (maîtrise, à réviser, précision, répartition)."""
    seen = corrects = total_rep = a_reviser = 0
    repartition = {b: 0 for b in range(quiz.BOITE_MAX + 1)}
    for q in qset.questions:
        st = progress.get(q.id)
        if st:
            seen += 1
            corrects += st.correct
            total_rep += st.seen
            repartition[st.box] += 1
            if st.is_due(now):
                a_reviser += 1
        else:
            repartition[0] += 1
            a_reviser += 1
    maitrise = sum(b * n for b, n in repartition.items())
    maitrise_max = quiz.BOITE_MAX * len(qset) or 1
    return {
        "total": len(qset),
        "rencontrees": seen,
        "a_reviser": a_reviser,
        "precision": (corrects / total_rep * 100) if total_rep else 0.0,
        "repartition": repartition,
        "pct_maitrise": maitrise / maitrise_max * 100,
    }


def index(request):
    library = quiz.get_library()
    player = player_id(request)
    now = timezone.now()
    categories = []
    total_due = 0
    for cat, sets in library.categories().items():
        entries = []
        for qset in sets:
            progress = QuizProgress.map_for(player, qset.id)
            summary = _set_summary(qset, progress, now)
            total_due += summary["a_reviser"]
            entries.append({"set": qset, "summary": summary})
        categories.append({"nom": cat, "sets": entries})
    context = _ctx(
        request,
        categories=categories,
        total_sets=len(library.sets),
        total_due=total_due,
        errors=library.errors,
    )
    return render(request, "wiki/quiz_index.html", context)


def _shuffled(pairs):
    pairs = list(pairs)
    random.shuffle(pairs)
    return pairs


def play(request):
    """Construit une session selon le mode demandé et rend le moteur de quiz."""
    library = quiz.get_library()
    player = player_id(request)
    now = timezone.now()
    mode = request.GET.get("mode", "all")
    limite = request.GET.get("n")
    set_id = request.GET.get("set")

    if request.GET.get("revision"):
        # Révision intelligente : questions dues de tous les sets, priorisées.
        titre = "Révision intelligente"
        pairs = []
        for qset in library.sorted_sets():
            progress = QuizProgress.map_for(player, qset.id)
            for q in qset.questions:
                st = progress.get(q.id)
                if st is None or st.is_due(now):
                    prio = st.priority(now) if st else (0, -1, _JAMAIS)
                    pairs.append((prio, qset, q, progress))
        pairs.sort(key=lambda p: p[0])
        selection = [(qset, q, progress) for _, qset, q, progress in pairs]
    else:
        qset = library.get(set_id)
        if qset is None:
            raise Http404("Set de QCM introuvable")
        titre = qset.titre
        progress = QuizProgress.map_for(player, qset.id)
        questions = list(qset.questions)
        if mode == "review":
            questions = [q for q in questions if (progress.get(q.id) is None or progress[q.id].is_due(now))]
        selection = _shuffled((qset, q, progress) for q in questions)

    if limite and limite.isdigit():
        selection = selection[:int(limite)]

    payload = [_question_payload(get_vault(), qset, q, progress) for qset, q, progress in selection]
    context = _ctx(
        request,
        titre=titre,
        questions=payload,
        count=len(payload),
        record_url=reverse("wiki:quiz_record"),
        back_url=reverse("wiki:quiz_index"),
    )
    return render(request, "wiki/quiz_play.html", context)


@require_POST
def record(request):
    """Enregistre le résultat d'une question (mise à jour de la boîte de Leitner)."""
    try:
        data = json.loads(request.body)
        set_id = str(data["set_id"])
        question_id = str(data["question_id"])
        correcte = bool(data["correct"])
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)

    library = quiz.get_library()
    qset = library.get(set_id)
    if qset is None or not any(q.id == question_id for q in qset.questions):
        return JsonResponse({"error": "question inconnue"}, status=404)

    obj, _ = QuizProgress.objects.get_or_create(
        player=player_id(request), set_id=set_id, question_id=question_id
    )
    obj.record(correcte)
    obj.save()
    return JsonResponse({"box": obj.box, "seen": obj.seen, "correct": obj.correct})


def stats(request):
    library = quiz.get_library()
    player = player_id(request)
    now = timezone.now()
    categories = []
    for cat, sets in library.categories().items():
        entries = [{"set": qset, "summary": _set_summary(qset, QuizProgress.map_for(player, qset.id), now)}
                   for qset in sets]
        categories.append({"nom": cat, "sets": entries})
    return render(request, "wiki/quiz_stats.html", _ctx(request, categories=categories, boites=range(quiz.BOITE_MAX + 1)))


@require_POST
def reset(request):
    set_id = request.POST.get("set", "")
    library = quiz.get_library()
    if library.get(set_id) is None:
        raise Http404("Set inconnu")
    QuizProgress.objects.filter(player=player_id(request), set_id=set_id).delete()
    return redirect("wiki:quiz_stats")
