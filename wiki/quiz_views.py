"""Vues des QCM de révision : choix des sets, sessions, statistiques.

L'interaction du quiz (afficher les questions, feedback immédiat, clavier) se
fait côté navigateur : la vue « jouer » fournit les questions pré-rendues en
JSON, et chaque réponse est enregistrée via une petite requête POST.
"""

import json
import random
import tempfile
from datetime import date
from pathlib import Path, PurePosixPath

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.db.models import F
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from . import planning, quiz
from .models import _JAMAIS, QuizDeck, QuizProgress
from .render import Renderer
from .vault import Note, clean_key, get_vault

# Import par glisser-déposer : dossier du coffre qui reçoit les sets.
DOSSIER_QCM = "QCM"
CATEGORIE_IMPORT = "Importés"
TAILLE_MAX_IMPORT = 2 * 1024 * 1024  # 2 Mo par fichier
LIMITE_JOUR_MAX = 9999
DUREE_MAX_MS = 120_000  # au-delà, le joueur s'est sans doute absenté


def player_id(request):
    """Identifie le « joueur » : chaque utilisateur connecté a sa progression."""
    return request.user.get_username()


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
        "consigne": question.consigne,
        "verso": _render_html(vault, question.verso),
        "explication": _render_html(vault, question.explication),
        "box": st.box if st else 0,
    }


def _file_du_jour(qset, progress, deck, now):
    """Questions à réviser aujourd'hui et nombre total de questions dues.

    Les questions déjà vues passent d'abord (boîtes basses, puis les plus
    anciennes), puis les nouvelles ; la limite journalière du set s'applique en
    tenant compte des questions déjà révisées aujourd'hui.
    """
    vues, nouvelles = [], []
    for q in qset.questions:
        st = progress.get(q.id)
        if st is None:
            nouvelles.append(q)
        elif st.is_due(now):
            vues.append((st, q))
    vues.sort(key=lambda t: (t[0].box, t[0].last_review or _JAMAIS))
    file = [q for _, q in vues] + nouvelles
    dues = len(file)
    if deck is not None and deck.limite_jour:
        file = file[:max(0, deck.limite_jour - planning.revues_aujourdhui(progress, now))]
    return file, dues


def _set_summary(qset, progress, now, deck=None):
    """Statistiques d'un set (maîtrise, à réviser, précision, répartition)."""
    seen = corrects = total_rep = 0
    repartition = {b: 0 for b in range(quiz.BOITE_MAX + 1)}
    for q in qset.questions:
        st = progress.get(q.id)
        if st:
            seen += 1
            corrects += st.correct
            total_rep += st.seen
            repartition[st.box] += 1
        else:
            repartition[0] += 1
    file, dues = _file_du_jour(qset, progress, deck, now)
    maitrise = sum(b * n for b, n in repartition.items())
    maitrise_max = quiz.BOITE_MAX * len(qset) or 1
    return {
        "total": len(qset),
        "rencontrees": seen,
        "a_reviser": len(file),
        "dues": dues,
        "quota_atteint": dues > 0 and not file,
        "precision": (corrects / total_rep * 100) if total_rep else 0.0,
        "repartition": repartition,
        "pct_maitrise": maitrise / maitrise_max * 100,
    }


@login_required
def index(request):
    library = quiz.get_library()
    player = player_id(request)
    now = timezone.now()
    q = request.GET.get("q", "").strip()
    categories = []
    total_due = matches = 0
    decks = QuizDeck.map_for(player)
    for cat, sets in library.categories().items():
        entries = []
        for qset in sets:
            progress = QuizProgress.map_for(player, qset.id)
            deck = QuizDeck.pour(decks, player, qset.id)
            summary = _set_summary(qset, progress, now, deck)
            total_due += summary["a_reviser"]
            # Les sets hors recherche restent dans la page (masqués) pour le filtre en direct.
            entries.append({
                "set": qset,
                "summary": summary,
                "deck": deck,
                "ancre": _ancre(qset.id),
                "estimation": planning.estimer(qset, progress, deck, now) if deck.configure else None,
                "match": not q or qset.correspond(q),
            })
        shown = sum(e["match"] for e in entries)
        matches += shown
        categories.append({
            "nom": cat,
            "sets": entries,
            "shown": shown,
            "a_reviser": sum(e["summary"]["a_reviser"] for e in entries),
        })
    context = _ctx(
        request,
        categories=categories,
        categories_import=_categories_import(),
        total_sets=len(library.sets),
        total_due=total_due,
        errors=library.errors,
        q=q,
        matches=matches,
    )
    return render(request, "wiki/quiz_index.html", context)


def _shuffled(pairs):
    pairs = list(pairs)
    random.shuffle(pairs)
    return pairs


@login_required
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
        decks = QuizDeck.map_for(player)
        for qset in library.sorted_sets():
            progress = QuizProgress.map_for(player, qset.id)
            file, _ = _file_du_jour(qset, progress, decks.get(qset.id), now)
            for q in file:
                st = progress.get(q.id)
                prio = st.priority(now) if st else (0, -1, _JAMAIS)
                pairs.append((prio, qset, q, progress))
        pairs.sort(key=lambda p: p[0])
        selection = [(qset, q, progress) for _, qset, q, progress in pairs]
    elif mode == "intensif" and request.GET.get("categorie"):
        # Révision intensive de toute une catégorie : toutes ses questions.
        categorie = request.GET["categorie"]
        sets = library.categories().get(categorie)
        if not sets:
            raise Http404("Catégorie de QCM introuvable")
        titre = f"Révision intensive · {categorie}"
        selection = []
        for qset in sets:
            progress = QuizProgress.map_for(player, qset.id)
            selection += [(qset, q, progress) for q in qset.questions]
        selection = _shuffled(selection)
    else:
        qset = library.get(set_id)
        if qset is None:
            raise Http404("Set de QCM introuvable")
        titre = qset.titre
        progress = QuizProgress.map_for(player, qset.id)
        questions = list(qset.questions)
        if mode == "review":
            deck = QuizDeck.objects.filter(player=player, set_id=qset.id).first()
            questions, _ = _file_du_jour(qset, progress, deck, now)
        elif mode == "intensif":
            titre = f"Révision intensive · {qset.titre}"
        selection = _shuffled((qset, q, progress) for q in questions)

    if limite and limite.isdigit():
        selection = selection[:int(limite)]

    vault = get_vault()
    payload = [_question_payload(vault, qset, q, progress) for qset, q, progress in selection]
    context = _ctx(
        request,
        titre=titre,
        questions=payload,
        count=len(payload),
        intensif=mode == "intensif" and not request.GET.get("revision"),
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

    # Temps de réponse : sert à estimer la durée quotidienne des révisions.
    duree = data.get("duree_ms")
    if isinstance(duree, (int, float)) and duree > 0:
        deck, _ = QuizDeck.objects.get_or_create(player=obj.player, set_id=set_id)
        QuizDeck.objects.filter(pk=deck.pk).update(
            temps_ms=F("temps_ms") + int(min(duree, DUREE_MAX_MS)),
            reponses_chronometrees=F("reponses_chronometrees") + 1,
        )
    return JsonResponse({"box": obj.box, "seen": obj.seen, "correct": obj.correct})


@login_required
def stats(request):
    library = quiz.get_library()
    player = player_id(request)
    now = timezone.now()
    decks = QuizDeck.map_for(player)
    categories = []
    for cat, sets in library.categories().items():
        entries = [{"set": qset, "summary": _set_summary(qset, QuizProgress.map_for(player, qset.id), now, decks.get(qset.id))}
                   for qset in sets]
        categories.append({"nom": cat, "sets": entries})
    return render(request, "wiki/quiz_stats.html", _ctx(request, categories=categories, boites=range(quiz.BOITE_MAX + 1)))


def _ancre(set_id):
    return "set-" + slugify(set_id.replace("/", "-"))


@require_POST
@login_required
def plan(request):
    """Enregistre la limite journalière et la date d'examen d'un set."""
    set_id = request.POST.get("set", "")
    if quiz.get_library().get(set_id) is None:
        raise Http404("Set inconnu")
    limite = request.POST.get("limite_jour", "").strip()
    objectif = request.POST.get("date_objectif", "").strip()
    try:
        limite = int(limite) if limite else None
        if limite is not None and not 1 <= limite <= LIMITE_JOUR_MAX:
            raise ValueError
    except ValueError:
        messages.error(request, f"Limite journalière invalide : un nombre entre 1 et {LIMITE_JOUR_MAX}, ou vide.")
        return redirect(reverse("wiki:quiz_index") + "#" + _ancre(set_id))
    try:
        objectif = date.fromisoformat(objectif) if objectif else None
    except ValueError:
        messages.error(request, "Date d'examen invalide.")
        return redirect(reverse("wiki:quiz_index") + "#" + _ancre(set_id))
    QuizDeck.objects.update_or_create(
        player=player_id(request), set_id=set_id,
        defaults={"limite_jour": limite, "date_objectif": objectif},
    )
    return redirect(reverse("wiki:quiz_index") + "#" + _ancre(set_id))


@require_POST
@login_required
def reset(request):
    set_id = request.POST.get("set", "")
    library = quiz.get_library()
    if library.get(set_id) is None:
        raise Http404("Set inconnu")
    QuizProgress.objects.filter(player=player_id(request), set_id=set_id).delete()
    return redirect("wiki:quiz_stats")


def _categories_import():
    """Sous-dossiers de vault/QCM, proposés comme catégories à l'import."""
    racine = Path(get_vault().root) / DOSSIER_QCM
    if not racine.is_dir():
        return []
    return sorted((d.name for d in racine.iterdir() if d.is_dir() and not d.name.startswith(".")), key=str.lower)


def _importer_fichier(fichier, categorie, remplacer):
    """Valide puis enregistre un set déposé. Renvoie (succès, message)."""
    nom = PurePosixPath(fichier.name.replace("\\", "/")).name
    if not nom.lower().endswith(".json"):
        return False, f"{nom} : seuls les fichiers .json sont acceptés."
    stem = clean_key(nom[:-5])
    if stem is None or "/" in stem:
        return False, f"{nom} : nom de fichier invalide."
    if fichier.size > TAILLE_MAX_IMPORT:
        return False, f"{nom} : fichier trop gros (2 Mo maximum)."
    try:
        texte = fichier.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        return False, f"{nom} : le fichier doit être encodé en UTF-8."

    rel = PurePosixPath(DOSSIER_QCM, categorie, f"{stem}.json")
    # Validation avec le chargeur des sets, dans un dossier temporaire.
    with tempfile.TemporaryDirectory() as tmp:
        essai = Path(tmp, rel)
        essai.parent.mkdir(parents=True)
        essai.write_text(texte, encoding="utf-8")
        try:
            qset = quiz.charger_set(essai, tmp)
        except ValueError as e:
            return False, str(e)

    destination = Path(get_vault().root, rel)
    if destination.exists() and not remplacer:
        return False, (f"{rel} existe déjà : cochez « Remplacer les sets existants » pour l'écraser "
                       "(la progression est conservée pour les questions dont l'id ne change pas).")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(texte, encoding="utf-8", newline="\n")
    n = len(qset)
    return True, f"« {qset.titre} » importé dans {rel} ({n} question{'s' if n > 1 else ''})."


@require_POST
def importer(request):
    """Import de sets JSON déposés sur la page des QCM (admins seulement)."""
    if not _can_edit(request):
        raise PermissionDenied
    categorie = request.POST.get("categorie", "").strip() or CATEGORIE_IMPORT
    cle = clean_key(categorie)
    fichiers = request.FILES.getlist("fichiers")
    if cle is None or "/" in cle:
        messages.error(request, 'Catégorie invalide : un seul nom de dossier, sans / \\ : * ? " < > | # ^ [ ].')
    elif not fichiers:
        messages.error(request, "Aucun fichier reçu.")
    else:
        remplacer = request.POST.get("remplacer") == "1"
        for fichier in fichiers:
            ok, message = _importer_fichier(fichier, cle, remplacer)
            (messages.success if ok else messages.error)(request, message)
    return redirect("wiki:quiz_index")
