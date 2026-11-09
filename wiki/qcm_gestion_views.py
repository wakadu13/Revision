"""Gestion des sets de QCM et des paquets de langue : import de fichiers JSON (admins),
rangement (déplacer, supprimer), export Anki, signalements de questions, et « Mon espace »
(sets et listes de mots de chaque compte, visibles de lui seul)."""

import json
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from . import anki, claude, claude_demandes, paquets, quiz
from .models import QuizDeck, QuizProgress, Signalement

# Import par glisser-déposer : dossier du coffre qui reçoit les sets.
from .quiz_views import (
    CATEGORIE_IMPORT,
    DOSSIER_QCM,
    TAILLE_MAX_IMPORT,
    _ancre,
    _can_edit,
    _ctx,
    _question_payload,
    _render_html,
    bibliotheque,
    player_id,
)
from .vault import clean_key, get_vault, invalider


def _importer_fichier(fichier, categorie, remplacer, racine=None, prefixe=DOSSIER_QCM, lieu=None):
    """Valide puis enregistre un set déposé, dans le coffre (``racine`` None :
    QCM/<catégorie>/) ou dans un espace personnel. Renvoie (succès, message)."""
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

    rel = PurePosixPath(*([prefixe] if prefixe else []), categorie, f"{stem}.json")
    # Validation avec le chargeur des sets, dans un dossier temporaire.
    with tempfile.TemporaryDirectory() as tmp:
        essai = Path(tmp, rel)
        essai.parent.mkdir(parents=True)
        essai.write_text(texte, encoding="utf-8")
        try:
            qset = quiz.charger(essai, tmp)
        except ValueError as e:
            return False, str(e)

    destination = Path(racine or get_vault().root, rel)
    if destination.exists() and not remplacer:
        return False, (f"{rel} existe déjà : cochez « Remplacer les sets existants » pour l'écraser "
                       "(la progression est conservée pour les questions dont l'id ne change pas).")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(texte, encoding="utf-8", newline="\n")
    invalider()
    n = len(qset)
    unite = "question" if isinstance(qset, quiz.QuestionSet) else "exercice"
    return True, f"« {qset.titre} » importé dans {lieu or rel} ({n} {unite}{'s' if n > 1 else ''})."


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


# ---------------------------------------------------------------------------
# Rangement : déplacer un set dans un dossier, supprimer un set ou un dossier
# ---------------------------------------------------------------------------
def _element(library, set_id):
    """Set de QCM ou fichier de langue désigné par son identifiant."""
    return library.get(set_id) or library.langues.get(set_id)


def _dossier(element):
    return element.path.parent.name or quiz.CATEGORIE_DEFAUT


def _retirer_dossiers_vides(dossier, racine):
    """Supprime les dossiers devenus vides, en remontant jusqu'à vault/QCM (exclu)."""
    arret = {racine, racine / DOSSIER_QCM}
    while dossier not in arret and racine in dossier.parents and dossier.is_dir() and not any(dossier.iterdir()):
        dossier.rmdir()
        dossier = dossier.parent


def _oublier(set_ids):
    """Efface la progression et les réglages de sets (pour tous les joueurs)."""
    QuizProgress.objects.filter(set_id__in=set_ids).delete()
    QuizDeck.objects.filter(set_id__in=set_ids).delete()


@require_POST
def deplacer(request):
    """Range un set (QCM ou fichier de langue) dans un dossier, créé au besoin.

    Les sets d'une langue vont dans vault/QCM/<langue>/<dossier>, les autres dans
    vault/QCM/<dossier>. La progression suit le set (son identifiant change)."""
    if not _can_edit(request):
        raise PermissionDenied
    library = quiz.get_library().commune()
    element = _element(library, request.POST.get("set", ""))
    if element is None:
        raise Http404("Set inconnu")
    dossier = clean_key(request.POST.get("dossier", ""))
    if dossier is None or "/" in dossier:
        messages.error(request, 'Dossier invalide : un seul nom de dossier, sans / \\ : * ? " < > | # ^ [ ].')
        return redirect(reverse("wiki:quiz_index") + "#" + _ancre(element.id))

    langue = clean_key(element.langue) if element.langue else None
    parties = [DOSSIER_QCM] + ([langue] if langue and "/" not in langue and langue != dossier else []) + [dossier]
    rel = PurePosixPath(*parties, element.path.name)
    racine = Path(get_vault().root)
    if rel == element.path:
        messages.info(request, f"« {element.titre} » est déjà dans le dossier {dossier}.")
        return redirect(reverse("wiki:quiz_index") + "#" + _ancre(element.id))
    if (racine / rel).exists():
        messages.error(request, f"{rel} existe déjà : renommez ou supprimez d'abord ce fichier.")
        return redirect(reverse("wiki:quiz_index") + "#" + _ancre(element.id))

    source = racine / element.path
    (racine / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.move(source, racine / rel)
    _retirer_dossiers_vides(source.parent, racine)
    nouvel_id = rel.with_suffix("").as_posix()
    _oublier([nouvel_id])  # restes éventuels d'un ancien set du même nom
    QuizProgress.objects.filter(set_id=element.id).update(set_id=nouvel_id)
    QuizDeck.objects.filter(set_id=element.id).update(set_id=nouvel_id)
    messages.success(request, f"« {element.titre} » rangé dans le dossier {dossier} ({rel}).")
    return redirect(reverse("wiki:quiz_index") + "#" + _ancre(nouvel_id))


@require_POST
def supprimer(request):
    """Supprime un set, ou tout un dossier (catégorie) d'une langue ou des cours,
    avec la progression associée."""
    if not _can_edit(request):
        raise PermissionDenied
    library = quiz.get_library().commune()
    set_id = request.POST.get("set", "")
    if set_id:
        element = _element(library, set_id)
        cibles = [element] if element else []
        libelle = f"« {element.titre} »" if element else ""
    else:
        categorie = request.POST.get("categorie", "")
        langue = request.POST.get("langue", "")
        cibles = [e for e in (*library.sets.values(), *library.langues.values())
                  if e.langue == langue and _dossier(e) == categorie]
        libelle = f"Le dossier {categorie} ({len(cibles)} set{'s' if len(cibles) > 1 else ''})"
    if not cibles:
        raise Http404("Set inconnu")

    racine = Path(get_vault().root)
    for element in cibles:
        chemin = racine / element.path
        chemin.unlink(missing_ok=True)
        _retirer_dossiers_vides(chemin.parent, racine)
    _oublier([e.id for e in cibles])
    messages.success(request, f"{libelle} supprimé.")
    return redirect("wiki:quiz_index")


# ---------------------------------------------------------------------------
# Export Anki / texte tabulé
# ---------------------------------------------------------------------------
@login_required
def exporter(request):
    """Un set de QCM ou un paquet de langue en .apkg (Anki) ou en .tsv (Quizlet, tableur)."""
    library = bibliotheque(request)
    set_id = request.GET.get("set", "")
    element = library.get(set_id) or library.langues.get(set_id)
    if element is None:
        raise Http404
    donnees = None
    if not isinstance(element, quiz.QuestionSet):
        _, donnees = quiz.lire_json(element.fichier, element.fichier.parent)
    titre, notes = anki.exporter(element, donnees)
    nom = slugify(titre) or "export"
    if request.GET.get("format") == "tsv":
        return HttpResponse(anki.tsv(notes), content_type="text/tab-separated-values; charset=utf-8",
                            headers={"Content-Disposition": f'attachment; filename="{nom}.tsv"'})
    contenu = anki.apkg(set_id, titre, element.description, notes)
    return HttpResponse(contenu, content_type="application/apkg",
                        headers={"Content-Disposition": f'attachment; filename="{nom}.apkg"'})


# ---------------------------------------------------------------------------
# Questions signalées
# ---------------------------------------------------------------------------
@login_required
@require_POST
def signaler(request):
    """Un joueur signale une question (erreur, ambiguïté) ; un signalement ouvert par
    joueur et par question, le commentaire remplace le précédent."""
    try:
        data = json.loads(request.body)
        set_id, question_id = str(data["set_id"]), str(data["question_id"])
        commentaire = str(data.get("commentaire") or "").strip()[:2000]
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)
    qset = bibliotheque(request).get(set_id)
    if qset is None or not any(q.id == question_id for q in qset.questions):
        return JsonResponse({"error": "question inconnue"}, status=404)
    if qset.proprietaire:
        return JsonResponse({"error": "set personnel : corrigez-le dans « Mon espace »"}, status=400)
    s, cree = Signalement.objects.get_or_create(
        set_id=set_id, question_id=question_id, player=player_id(request), traite=False,
        defaults={"commentaire": commentaire})
    if not cree and commentaire:
        s.commentaire = commentaire
        s.save(update_fields=["commentaire"])
    return JsonResponse({"ok": True, "nouveau": cree})


def _ligne_signalement(vault, library, s):
    qset = library.get(s.set_id)
    question = next((q for q in qset.questions if q.id == s.question_id), None) if qset else None
    ligne = {"s": s, "set": qset, "question": question, "html": None, "proposition": None}
    if question is not None:
        ligne["html"] = _question_payload(vault, qset, question, {})
    if s.proposition:
        p = s.proposition
        ligne["proposition"] = {
            "type": p.get("type", ""),
            "enonce": _render_html(vault, p.get("question", "")),
            "consigne": p.get("consigne", ""),
            "choix": [(_render_html(vault, c, block=False), i in p.get("reponses", [])) for i, c in enumerate(p.get("choix", []))],
            "reponses_texte": p.get("reponses_texte", []),
            "verso": _render_html(vault, p.get("verso", "")),
            "explication": _render_html(vault, p.get("explication", "")),
        }
    return ligne


def _remplacer_question(qset, question_id, nouvelle):
    """Remplace une question dans le fichier JSON du set (``nouvelle`` : champs JSON), ou
    la retire si ``nouvelle`` est None. Les identifiants implicites (q1, q2…) des
    questions suivantes sont figés pour que leur progression reste rattachée."""
    racine = get_vault().root
    rel, data = quiz.lire_json(racine / qset.path, racine)  # sets communs seulement (signalements)
    questions = data["questions"]
    for i, q in enumerate(questions, start=1):
        if str(q.get("id", f"q{i}")) == question_id:
            if nouvelle is None:
                for j in range(i, len(questions)):
                    questions[j].setdefault("id", f"q{j + 1}")
                del questions[i - 1]
            else:
                garde = {k: v for k, v in q.items() if k not in claude.CHAMPS_QUESTION}
                questions[i - 1] = {**garde, **nouvelle}
            break
    else:
        raise Http404
    if not questions:
        raise ValueError("C'était la dernière question du set : supprimez plutôt le set.")
    quiz.set_depuis_json(data, rel)  # validation avant d'écrire
    paquets.enregistrer_json(rel, data)


@login_required
def signalements(request):
    """Questions signalées (admins) : corriger avec Claude, appliquer, retirer la question, clore."""
    if not _can_edit(request):
        raise PermissionDenied
    library = quiz.get_library()
    if request.method == "POST":
        s = get_object_or_404(Signalement, pk=request.POST.get("pk"))
        action = request.POST.get("action", "")
        qset = library.get(s.set_id)
        question = next((q for q in qset.questions if q.id == s.question_id), None) if qset else None
        try:
            if action == "proposer" and question is not None:
                if not claude.disponible():
                    raise claude.Echec("Pas de clé d'API Claude sur le serveur.")
                commentaires = list(Signalement.objects.filter(set_id=s.set_id, question_id=s.question_id, traite=False)
                                    .exclude(commentaire="").values_list("commentaire", flat=True))
                nouvelle, note, _, _ = claude_demandes.corriger_question(qset, question, commentaires)
                s.proposition, s.proposition_note = nouvelle, note
                s.save(update_fields=["proposition", "proposition_note"])
                messages.success(request, "Claude propose une correction : relisez-la, puis appliquez-la ou non.")
            elif action in ("appliquer", "retirer") and question is not None:
                if action == "appliquer" and not s.proposition:
                    raise ValueError("Aucune correction à appliquer.")
                _remplacer_question(qset, s.question_id, s.proposition if action == "appliquer" else None)
                Signalement.objects.filter(set_id=s.set_id, question_id=s.question_id, traite=False).update(
                    traite=True, traite_le=timezone.now())
                messages.success(request, "Question corrigée dans le set." if action == "appliquer" else "Question retirée du set.")
            elif action == "clore":
                Signalement.objects.filter(set_id=s.set_id, question_id=s.question_id, traite=False).update(
                    traite=True, traite_le=timezone.now())
                messages.success(request, "Signalement clos.")
            else:
                messages.error(request, "Question introuvable : le set a changé.")
        except (claude.Echec, ValueError) as e:
            messages.error(request, str(e))
        return redirect("wiki:quiz_signalements")
    vault = get_vault()
    ouverts = [_ligne_signalement(vault, library, s) for s in Signalement.objects.filter(traite=False)]
    traites = Signalement.objects.filter(traite=True).order_by("-traite_le")[:20]
    return render(request, "wiki/quiz_signalements.html", _ctx(
        request, ouverts=ouverts, traites=traites, claude_dispo=claude.disponible()))


# ---------------------------------------------------------------------------
# Espace personnel : sets et paquets importés par chaque compte, visibles de lui seul
# ---------------------------------------------------------------------------
MAX_FICHIERS_PERSO = 200


MAX_OCTETS_PERSO = 20 * 2**20


CATEGORIE_PERSO = "Mes sets"


def _fichiers_perso(player):
    dossier = quiz.dossier_perso(player)
    return list(dossier.rglob("*.json")) if dossier.is_dir() else []


def _taille_perso(player):
    """Octets occupés par l'espace personnel (sets, paquets et images)."""
    dossier = quiz.dossier_perso(player)
    return sum(f.stat().st_size for f in dossier.rglob("*") if f.is_file()) if dossier.is_dir() else 0


def _ecrire_paquet_perso(player, dossier, paquet):
    """Écrit un paquet de langue dans l'espace personnel ; renvoie son identifiant."""
    from . import langues

    racine = quiz.dossier_perso(player)
    base = (paquets.slug(paquet.get("titre", "")) or "vocabulaire")[:60]
    for i in range(1, 1000):
        rel = PurePosixPath(dossier, f"{base}.json" if i == 1 else f"{base}-{i}.json")
        if not (racine / rel).exists():
            break
    try:
        langues.set_depuis_json(paquet, rel)
    except ValueError as e:
        raise paquets.PaquetInvalide(f"Paquet invalide : {e}") from None
    cible = racine / rel
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(json.dumps(paquet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    invalider()
    return quiz.PERSO + quiz.nom_perso(player) + "/" + rel.with_suffix("").as_posix()


@login_required
def perso(request):
    """« Mon espace » : importer ses propres sets (JSON) et listes de mots, les supprimer."""
    from . import langues
    from .claude_views import lire_liste, message_paquet

    player = player_id(request)
    if request.method == "POST":
        action = request.POST.get("action", "")
        if action == "supprimer":
            element = _element(bibliotheque(request), request.POST.get("set", ""))
            if element is None or element.proprietaire != quiz.nom_perso(player):
                raise Http404("Set inconnu")
            element.fichier.unlink(missing_ok=True)
            _retirer_dossiers_vides(element.fichier.parent, quiz.dossier_perso(player))
            _oublier([element.id])
            invalider()
            messages.success(request, f"« {element.titre} » supprimé de votre espace.")
            return redirect("wiki:quiz_perso")
        if len(_fichiers_perso(player)) >= MAX_FICHIERS_PERSO or _taille_perso(player) >= MAX_OCTETS_PERSO:
            messages.error(request, f"Votre espace est plein ({MAX_FICHIERS_PERSO} fichiers, {MAX_OCTETS_PERSO // 2**20} Mo) : supprimez-en d'abord.")
            return redirect("wiki:quiz_perso")
        if action == "json":
            categorie = clean_key(request.POST.get("categorie", "").strip() or CATEGORIE_PERSO)
            fichiers = request.FILES.getlist("fichiers")
            if categorie is None or "/" in categorie:
                messages.error(request, 'Dossier invalide : un seul nom, sans / \\ : * ? " < > | # ^ [ ].')
            elif not fichiers:
                messages.error(request, "Aucun fichier reçu.")
            else:
                place = MAX_FICHIERS_PERSO - len(_fichiers_perso(player))
                for fichier in fichiers[:place]:
                    if _taille_perso(player) + fichier.size > MAX_OCTETS_PERSO:
                        messages.error(request, f"{fichier.name} : votre espace est plein ({MAX_OCTETS_PERSO // 2**20} Mo).")
                        break
                    ok, message = _importer_fichier(fichier, categorie, request.POST.get("remplacer") == "1",
                                                    racine=quiz.dossier_perso(player), prefixe="",
                                                    lieu=f"votre espace, dossier « {categorie} »")
                    (messages.success if ok else messages.error)(request, message)
                if len(fichiers) > place:
                    messages.error(request, f"{len(fichiers) - place} fichier(s) non importé(s) : {MAX_FICHIERS_PERSO} fichiers au plus.")
            return redirect("wiki:quiz_perso")
        if action == "liste":
            paquet, options, ignorees, erreur = lire_liste(request)
            if erreur:
                messages.error(request, erreur)
                return redirect("wiki:quiz_perso")
            try:
                set_id = _ecrire_paquet_perso(player, options["dossier"] or "Vocabulaire", paquet)
            except paquets.PaquetInvalide as e:
                messages.error(request, str(e))
                return redirect("wiki:quiz_perso")
            messages.success(request, message_paquet(paquet, ignorees))
            return redirect(reverse("wiki:langue_menu", args=[options["langue"]]) + "?" + urlencode({"fichier": set_id}))
        return redirect("wiki:quiz_perso")

    library = bibliotheque(request)
    elements = []
    for e in library.personnels(player):
        est_langue = not isinstance(e, quiz.QuestionSet)
        elements.append({"set": e, "langue": est_langue, "dossier": e.path.parent.name, "taille": len(e),
                         "jouer": (reverse("wiki:langue_menu", args=[e.langue]) + "?" + urlencode({"fichier": e.id})) if est_langue
                         else reverse("wiki:quiz_play") + "?" + urlencode({"set": e.id, "mode": "all"})})
    from . import claude

    return render(request, "wiki/quiz_perso.html", _ctx(
        request, elements=elements, erreurs=library.erreurs_perso.get(quiz.nom_perso(player), []),
        max_fichiers=MAX_FICHIERS_PERSO, nombre=len(_fichiers_perso(player)),
        langues=sorted(set(library.noms_langues()) | {"Anglais"}, key=str.lower),
        cartes=[(t, langues.nom_type(t, "Anglais"), t in claude.CARTES_PAR_DEFAUT) for t in langues.TYPES_VOCABULAIRE],
        dossiers=sorted({x["dossier"] for x in elements}, key=str.lower),
    ))
