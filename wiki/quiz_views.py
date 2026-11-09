"""Vues des QCM de révision : choix des sets, sessions, statistiques.

L'interaction du quiz (afficher les questions, feedback immédiat, clavier) se
fait côté navigateur : la vue « jouer » fournit les questions pré-rendues en
JSON, et chaque réponse est enregistrée via une petite requête POST.
"""

import json
import random
from datetime import date, timedelta
from pathlib import Path, PurePosixPath

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.db.models import F
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_POST

from . import claude, masque, planning, quiz
from .models import _JAMAIS, Activite, ObjectifRevision, QuizDeck, QuizProgress, Signalement, TempsRevision
from .render import Renderer
from .vault import Note, get_vault

# Import par glisser-déposer : dossier du coffre qui reçoit les sets.
DOSSIER_QCM = "QCM"
CATEGORIE_IMPORT = "Importés"
TAILLE_MAX_IMPORT = 2 * 1024 * 1024  # 2 Mo par fichier
QUOTA_MAX = 9999
EXAMEN_QUESTIONS = 20   # questions d'un examen blanc par défaut
EXAMEN_DUREE_MAX = 180  # minutes
DUREE_MAX_MS = 120_000  # au-delà, le joueur s'est sans doute absenté


def bibliotheque(request):
    """Bibliothèque vue par le compte connecté : sets communs et son espace personnel."""
    return quiz.get_library().pour(player_id(request))


def player_id(request):
    """Identifie le « joueur » : chaque utilisateur connecté a sa progression."""
    return request.user.get_username()


def _ctx(request, **extra):
    vault = get_vault()
    return {"vault": vault, "tree": vault.tree, "can_edit": _can_edit(request), **extra}


def _can_edit(request):
    from .vues_communes import can_edit
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
        "enonce": _render_html(vault, question.enonce) + (masque.html(vault, qset, question.masque) if question.masque else ""),
        "choix": [_render_html(vault, c, block=False) for c in question.choix],
        "reponses": question.reponses,
        "reponses_texte": question.reponses_texte,
        "consigne": question.consigne,
        "verso": _render_html(vault, question.verso),
        "explication": _render_html(vault, question.explication),
        "box": st.box if st else 0,
        "perso": bool(qset.proprietaire),
    }


def _file_du_jour(qset, progress, deck, now):
    """Questions à réviser aujourd'hui, et leur répartition.

    Ordre : questions ratées aujourd'hui (réapprentissage, hors quota), puis
    révisions (boîtes basses, puis les plus anciennes), puis nouvelles. Les
    quotas du set tiennent compte de ce qui a déjà été fait aujourd'hui.
    Renvoie (file, {"dues", "nouvelles", "revisions", "reapprendre"}).
    """
    aujourdhui = timezone.localdate(now)
    reapprendre, vues, nouvelles = [], [], []
    for q in qset.questions:
        st = progress.get(q.id)
        if st is None:
            nouvelles.append(q)
        elif st.is_due(now):
            if st.last_review and timezone.localdate(st.last_review) == aujourdhui:
                reapprendre.append(q)
            else:
                vues.append((st, q))
    vues.sort(key=lambda t: (t[0].urgence(now), t[0].last_review or _JAMAIS))
    vues = [q for _, q in vues]
    dues = len(reapprendre) + len(vues) + len(nouvelles)
    if deck is not None:
        deja_n, deja_r = planning.faites_aujourdhui(progress, now)
        quota_n, quota_r = planning.quotas_effectifs(qset, progress, deck, now)
        places_r = planning.restant(quota_r, deja_r)
        places_n = planning.restant(quota_n, deja_n)
        vues = vues[:places_r] if places_r is not None else vues
        nouvelles = nouvelles[:places_n] if places_n is not None else nouvelles
    detail = {"dues": dues, "nouvelles": len(nouvelles), "revisions": len(vues), "reapprendre": len(reapprendre)}
    return reapprendre + vues + nouvelles, detail


def question_ratee(st):
    """Question à retravailler : ratée la dernière fois, ou réussie une fois sur deux au plus."""
    return st.last_correct is False or (st.seen >= 2 and st.correct * 2 <= st.seen)


def _set_summary(qset, progress, now, deck=None):
    """Statistiques d'un set (maîtrise, à réviser, précision, répartition)."""
    from . import langues

    seen = corrects = total_rep = maitrisees = 0
    maitrise = retention = 0.0
    repartition = {b: 0 for b in range(quiz.BOITE_MAX + 1)}
    for q in qset.questions:
        st = progress.get(q.id)
        if st:
            seen += 1
            corrects += st.correct
            total_rep += st.seen
            repartition[st.box] += 1
            # Maîtrise : stabilité FSRS rapportée à MAITRISE_JOURS (boîte de Leitner pour une progression ancienne).
            maitrise += min(1.0, st.stabilite / langues.MAITRISE_JOURS) if st.stabilite is not None else st.box / quiz.BOITE_MAX
            retention += st.urgence(now)
            maitrisees += st.stabilite is not None and st.stabilite >= langues.MAITRISE_JOURS
        else:
            repartition[0] += 1
    file, detail = _file_du_jour(qset, progress, deck, now)
    ids = {q.id for q in qset.questions}
    return {
        "total": len(qset),
        "rencontrees": seen,
        "maitrisees": maitrisees,
        "retention": retention / seen * 100 if seen else None,
        "a_reviser": len(file),
        "ratees": sum(1 for qid, st in progress.items() if qid in ids and question_ratee(st)),
        **detail,
        "quota_atteint": detail["dues"] > 0 and not file,
        "precision": (corrects / total_rep * 100) if total_rep else 0.0,
        "repartition": repartition,
        "pct_maitrise": maitrise / (len(qset) or 1) * 100,
    }


@login_required
def index(request):
    library = bibliotheque(request)
    player = player_id(request)
    now = timezone.now()
    q = request.GET.get("q", "").strip()
    total_due = matches = 0
    decks = QuizDeck.map_for(player)
    # (langue, catégorie) → sets : les sets rattachés à une langue sont affichés
    # dans la section Langues, les autres dans les catégories habituelles.
    groupes = {}
    for cat, sets in library.categories().items():
        for qset in sets:
            progress = QuizProgress.map_for(player, qset.id)
            deck = QuizDeck.pour(decks, player, qset.id)
            summary = _set_summary(qset, progress, now, deck)
            total_due += summary["a_reviser"]
            # Les sets hors recherche restent dans la page (masqués) pour le filtre en direct.
            groupes.setdefault((qset.langue, cat), []).append({
                "set": qset,
                "summary": summary,
                "deck": deck,
                "ancre": _ancre(qset.id),
                "estimation": planning.estimer(qset, progress, deck, now) if deck.configure else None,
                "match": not q or qset.correspond(q),
            })
    par_langue = {}
    for (langue, cat), entries in groupes.items():
        shown = sum(e["match"] for e in entries)
        matches += shown
        dates = [e["deck"].date_objectif for e in entries if e["deck"].date_objectif]
        par_langue.setdefault(langue, []).append({
            "nom": cat,
            "langue": langue,
            "sets": entries,
            "shown": shown,
            "a_reviser": sum(e["summary"]["a_reviser"] for e in entries),
            "date_objectif": min(dates) if dates else None,
        })
    categories = par_langue.pop("", [])
    from .langues_views import dossier_de, resume_langue

    langues = []
    for nom in library.noms_langues():
        fichiers = library.sets_langue(nom)
        # Fichiers de langue regroupés par dossier, chacun révisable séparément.
        par_dossier = {}
        for f in fichiers:
            par_dossier.setdefault(dossier_de(f), []).append(f)
        dossiers = []
        for dossier, fs in sorted(par_dossier.items(), key=lambda t: t[0].lower()):
            entries = []
            for f in fs:
                texte = quiz.normaliser_texte(" ".join((f.titre, f.description, dossier, nom)))
                match = not q or all(mot in texte for mot in quiz.normaliser_texte(q).split())
                entries.append({"set": f, "search": texte, "match": match, "ancre": _ancre(f.id)})
            shown = sum(e["match"] for e in entries)
            matches += shown
            dossiers.append({"nom": dossier, "langue": nom, "sets": entries, "shown": shown,
                             "resume": resume_langue(player, nom, fs, now)})
        langues.append({"nom": nom, "sets": fichiers,
                        "resume": resume_langue(player, nom, fichiers, now) if fichiers else None,
                        "dossiers": dossiers,
                        "liste": "dossiers-" + slugify(nom),
                        "noms_dossiers": sorted({d["nom"] for d in dossiers} | {c["nom"] for c in par_langue.get(nom, [])}, key=str.lower),
                        "categories": par_langue.get(nom, [])})
    generation = None
    if _can_edit(request):
        from . import claude
        from . import langues as module_langues

        vault = get_vault()
        dossiers_langue = sorted({d["nom"] for l in langues for d in l["dossiers"]} | {claude.DOSSIER_VOCABULAIRE}, key=str.lower)
        generation = {
            "dispo": claude.disponible(),
            "pages": sorted(((n.key, n.title) for n in vault.notes.values() if not n.key.startswith("QCM/")), key=lambda p: p[0].lower()),
            "nombres": claude.NOMBRES_QUESTIONS,
            "langues": sorted(set(library.noms_langues()) | {"Anglais"}, key=str.lower),
            "dossiers_langue": dossiers_langue,
            "cartes": [(t, module_langues.nom_type(t, "Anglais"), t in claude.CARTES_PAR_DEFAUT)
                       for t in module_langues.TYPES_VOCABULAIRE],
            "max_mots": claude.MAX_MOTS,
        }
    serie, _ = Activite.serie(player, timezone.localdate(now))
    context = _ctx(
        request,
        serie=serie,
        signalements_ouverts=Signalement.objects.filter(traite=False).count() if _can_edit(request) else 0,
        generation=generation,
        langues=langues,
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
    library = bibliotheque(request)
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
        langue = request.GET.get("langue", "")
        sets = [s for s in library.categories().get(categorie, []) if s.langue == langue]
        if not sets:
            raise Http404("Catégorie de QCM introuvable")
        titre = f"Révision intensive · {categorie}"
        selection = []
        for qset in sets:
            progress = QuizProgress.map_for(player, qset.id)
            selection += [(qset, q, progress) for q in qset.questions]
        selection = _shuffled(selection)
    elif mode == "examen":
        # Examen blanc : n questions tirées au sort (pas de flashcards : elles
        # s'auto-évaluent), chronométrées, corrigées à la fin.
        if request.GET.get("categorie"):
            categorie = request.GET["categorie"]
            langue = request.GET.get("langue", "")
            sets = [s for s in library.categories().get(categorie, []) if s.langue == langue]
            if not sets:
                raise Http404("Catégorie de QCM introuvable")
            titre = f"Examen blanc · {categorie}"
        else:
            qset = library.get(set_id)
            if qset is None:
                raise Http404("Set de QCM introuvable")
            sets, titre = [qset], f"Examen blanc · {qset.titre}"
        selection = []
        for qset in sets:
            progress = QuizProgress.map_for(player, qset.id)
            selection += [(qset, q, progress) for q in qset.questions if not q.est_flashcard]
        selection = _shuffled(selection)
        total_dispo = len(selection)
        n = int(limite) if limite and limite.isdigit() else EXAMEN_QUESTIONS
        n = max(1, min(n, total_dispo)) if total_dispo else 0
        selection, limite = selection[:n], None
        duree = request.GET.get("duree", "")
        duree_min = max(1, min(int(duree) if duree.isdigit() else n, EXAMEN_DUREE_MAX))
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
        examen=mode == "examen",
        record_url=reverse("wiki:quiz_record"),
        expliquer_url=reverse("wiki:quiz_expliquer") if claude.disponible() else "",
        corriger_qrc_url=reverse("wiki:quiz_corriger_qrc") if claude.disponible() else "",
        back_url=reverse("wiki:quiz_index"),
    )
    if mode == "examen":
        context.update(duree_min=duree_min, duree_s=duree_min * 60, total_dispo=total_dispo,
                       examen_params={k: request.GET[k] for k in ("set", "categorie", "langue") if request.GET.get(k)})
    return render(request, "wiki/quiz_play.html", context)


@require_POST
def record(request):
    """Enregistre le résultat d'une question (mise à jour de la boîte de Leitner)."""
    try:
        data = json.loads(request.body)
        set_id = str(data["set_id"])
        question_id = str(data["question_id"])
        # Flashcards : note d'auto-évaluation ; autres types : juste/faux.
        reponse = data["note"] if data.get("note") in quiz.NOTES else bool(data["correct"])
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)

    library = bibliotheque(request)
    qset = library.get(set_id)
    if qset is None or not any(q.id == question_id for q in qset.questions):
        return JsonResponse({"error": "question inconnue"}, status=404)

    obj, _ = QuizProgress.objects.get_or_create(
        player=player_id(request), set_id=set_id, question_id=question_id
    )
    deck = QuizDeck.objects.filter(player=obj.player, set_id=set_id).first()
    obj.record(reponse, retention=planning.retention_cible(deck.date_objectif if deck else None, timezone.now()))
    obj.save()
    Activite.noter(obj.player, obj.last_correct, nouveau=obj.seen == 1)

    chronometrer(obj.player, set_id, data.get("duree_ms"), matiere_de(qset))
    return JsonResponse({"box": obj.box, "seen": obj.seen, "correct": obj.correct,
                         "stabilite": obj.stabilite, "echeance": obj.echeance.isoformat()})


def matiere_de(qset):
    """Matière d'un set pour les temps de révision : sa langue, sinon sa catégorie."""
    return qset.langue or qset.categorie


def chronometrer(player, set_id, duree, matiere="", quand=None):
    """Cumule un temps de réponse : estimation de la durée quotidienne des révisions
    (par set), et temps de révision par matière et par jour (statistiques)."""
    TempsRevision.noter(player, matiere, duree, quand)
    if isinstance(duree, (int, float)) and not isinstance(duree, bool) and duree > 0:
        deck, _ = QuizDeck.objects.get_or_create(player=player, set_id=set_id)
        QuizDeck.objects.filter(pk=deck.pk).update(
            temps_ms=F("temps_ms") + int(min(duree, DUREE_MAX_MS)),
            reponses_chronometrees=F("reponses_chronometrees") + 1,
        )


@login_required
def stats(request):
    library = bibliotheque(request)
    player = player_id(request)
    now = timezone.now()
    decks = QuizDeck.map_for(player)
    categories = []
    for cat, sets in library.categories().items():
        entries = [{"set": qset, "summary": _set_summary(qset, QuizProgress.map_for(player, qset.id), now, decks.get(qset.id))}
                   for qset in sets]
        categories.append({"nom": cat, "sets": entries})
    aujourdhui = timezone.localdate(now)
    previsions = _previsions(player, library, now)
    semaines, temps, temps_totaux = TempsRevision.tableau(player, aujourdhui)
    return render(request, "wiki/quiz_stats.html", _ctx(
        request, categories=categories, boites=range(quiz.BOITE_MAX + 1), claude_dispo=claude.disponible(),
        previsions=previsions, previsions_max=max([p["n"] for p in previsions] + [1]),
        previsions_total=sum(p["n"] for p in previsions),
        semaines=semaines, temps=temps, temps_totaux=temps_totaux,
        activite=Activite.resume(player, aujourdhui), calendrier=Activite.calendrier(player, aujourdhui),
        mois=_mois_du_calendrier(Activite.calendrier(player, aujourdhui)),
    ))


MOIS_COURTS = ["Jan", "Fév", "Mars", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
JOURS_PREVISION = 14


def _previsions(player, library, now, jours=JOURS_PREVISION):
    """Révisions à venir (QCM et langues) : une case par jour, les retards comptés aujourd'hui."""
    aujourdhui = timezone.localdate(now)
    compteurs = [0] * jours
    connus = set(library.sets) | set(library.langues)
    for p in QuizProgress.objects.filter(player=player).exclude(last_review=None):
        if p.set_id not in connus:
            continue
        echeance = p.echeance or (p.last_review + timedelta(days=quiz.INTERVALLES_JOURS.get(p.box, 30)))
        d = (timezone.localdate(echeance) - aujourdhui).days
        if d < jours:
            compteurs[max(0, d)] += 1
    return [{"jour": aujourdhui + timedelta(days=d), "n": compteurs[d]} for d in range(jours)]


def _mois_du_calendrier(grille):
    """Étiquettes de mois au-dessus du calendrier : (colonne, nom) à chaque changement de mois."""
    etiquettes, precedent = [], None
    for i, semaine in enumerate(grille):
        mois = semaine[0]["jour"].month
        if mois != precedent:
            etiquettes.append((i + 1, MOIS_COURTS[mois - 1]))
            precedent = mois
    return etiquettes


def etat_rappel(player, library=None, now=None):
    """Ce qu'il reste à réviser (QCM, langues), série et réponses du jour : rappel de
    l'application Android, notifications web, page « Aujourd'hui »."""
    from .langues_views import resume_langue

    library = (library or quiz.get_library()).pour(player)
    now = now or timezone.now()
    decks = QuizDeck.map_for(player)
    qcm = sum(_set_summary(s, QuizProgress.map_for(player, s.id), now, decks.get(s.id))["a_reviser"] for s in library.sets.values())
    langues_dues = 0
    for nom in library.noms_langues():
        fichiers = library.sets_langue(nom)
        if fichiers:
            langues_dues += resume_langue(player, nom, fichiers, now)["a_revoir"]
    activite = Activite.resume(player, timezone.localdate(now))
    return {"a_revoir": qcm + langues_dues, "qcm": qcm, "langues": langues_dues,
            "serie": activite["serie"], "aujourdhui": activite["aujourdhui"]}


def texte_rappel(etat):
    """Texte de la notification de rappel, ou None s'il n'y a rien à rappeler (tout est
    révisé et on a déjà travaillé aujourd'hui)."""
    n, serie, auj = etat["a_revoir"], etat["serie"], etat["aujourdhui"]
    if n == 0 and auj > 0:
        return None
    texte = (f"{n} élément{'s' if n > 1 else ''} à réviser" if n else "Rien d'urgent : quelques nouveaux mots ?")
    if serie > 0:
        texte += f" · série de {serie} jour{'s' if serie > 1 else ''}" + (" à prolonger" if auj == 0 else "")
    return texte


def rappel(request):
    """Pour le rappel quotidien de l'application : à réviser (QCM, langues), série, réponses du jour."""
    return JsonResponse({**etat_rappel(player_id(request)), "admin": _can_edit(request)})


@login_required
def aujourdhui(request):
    """Page « Aujourd'hui » : tout ce qui est dû, les examens à venir, la série, l'objectif du jour."""
    from .langues_views import resume_langue

    player = player_id(request)
    if request.method == "POST":
        valeur = request.POST.get("objectif", "").strip()
        objectif = int(valeur) if valeur.isdigit() and 0 < int(valeur) <= 2000 else None
        ObjectifRevision.objects.update_or_create(player=player, defaults={"reponses_jour": objectif})
        return redirect("wiki:aujourdhui")
    library = bibliotheque(request)
    now = timezone.now()
    jour = timezone.localdate(now)
    decks = QuizDeck.map_for(player)
    sets_dus, total_qcm = [], 0
    for qset in library.sorted_sets():
        progress = QuizProgress.map_for(player, qset.id)
        summary = _set_summary(qset, progress, now, decks.get(qset.id))
        total_qcm += summary["a_reviser"]
        if summary["a_reviser"]:
            sets_dus.append({"set": qset, "summary": summary})
    sets_dus.sort(key=lambda e: (-e["summary"]["a_reviser"], e["set"].titre.lower()))
    langues = []
    for nom in library.noms_langues():
        fichiers = library.sets_langue(nom)
        if fichiers:
            r = resume_langue(player, nom, fichiers, now)
            langues.append({"nom": nom, "a_revoir": r["a_revoir"], "nouveaux": r["nouveaux_disponibles"]})
    examens = []
    for deck in decks.values():
        if deck.date_objectif is None or deck.date_objectif < jour:
            continue
        qset = library.get(deck.set_id)
        if qset is None:
            continue
        e = planning.estimer(qset, QuizProgress.map_for(player, qset.id), deck, now)
        examens.append({"set": qset, "date": deck.date_objectif, "jours": (deck.date_objectif - jour).days, "e": e})
    examens.sort(key=lambda x: (x["date"], x["set"].titre.lower()))
    activite = Activite.resume(player, jour)
    objectif = ObjectifRevision.objects.filter(player=player).values_list("reponses_jour", flat=True).first()
    previsions = _previsions(player, library, now, 7)
    return render(request, "wiki/aujourdhui.html", _ctx(
        request, jour=jour, total_qcm=total_qcm, sets_dus=sets_dus[:8], autres_sets=max(0, len(sets_dus) - 8),
        langues=langues, examens=examens, activite=activite, objectif=objectif,
        pct_objectif=min(100, round(activite["aujourdhui"] / objectif * 100)) if objectif else 0,
        minutes=TempsRevision.minutes_du_jour(player, jour), previsions=previsions,
        previsions_max=max([p["n"] for p in previsions] + [1]),
        push_cle_url=reverse("wiki:push_cle"),
    ))


def _ancre(set_id):
    return "set-" + slugify(set_id.replace("/", "-"))


@require_POST
@login_required
def _plan_categorie(request, library, player):
    """Date d'examen appliquée à tous les sets d'une catégorie."""
    categorie, langue = request.POST.get("categorie", ""), request.POST.get("langue", "")
    sets = [s for s in library.categories().get(categorie, []) if s.langue == langue]
    if not sets:
        raise Http404("Catégorie inconnue")
    objectif = request.POST.get("date_objectif", "").strip()
    try:
        objectif = date.fromisoformat(objectif) if objectif else None
    except ValueError:
        messages.error(request, "Date d'examen invalide.")
        return redirect("wiki:quiz_index")
    for s in sets:
        QuizDeck.objects.update_or_create(player=player, set_id=s.id, defaults={"date_objectif": objectif})
    combien = "le set" if len(sets) == 1 else f"les {len(sets)} sets"
    messages.success(request, f"Date d'examen {'fixée au ' + objectif.strftime('%d/%m/%Y') if objectif else 'retirée'} "
                              f"pour {combien} de « {categorie} ».")
    return redirect("wiki:quiz_index")


def plan(request):
    """Enregistre les quotas journaliers et la date d'examen d'un set."""
    library = bibliotheque(request)
    if request.POST.get("categorie"):
        return _plan_categorie(request, library, player_id(request))
    set_id = request.POST.get("set", "")
    if bibliotheque(request).get(set_id) is None:
        raise Http404("Set inconnu")
    quotas = {}
    for champ, nom in (("nouvelles_jour", "nouvelles questions"), ("revisions_jour", "révisions")):
        valeur = request.POST.get(champ, "").strip()
        try:
            quotas[champ] = int(valeur) if valeur else None
            if valeur and not 1 <= quotas[champ] <= QUOTA_MAX:
                raise ValueError
        except ValueError:
            messages.error(request, f"Nombre de {nom} par jour invalide : entre 1 et {QUOTA_MAX}, ou vide.")
            return redirect(reverse("wiki:quiz_index") + "#" + _ancre(set_id))
    objectif = request.POST.get("date_objectif", "").strip()
    try:
        objectif = date.fromisoformat(objectif) if objectif else None
    except ValueError:
        messages.error(request, "Date d'examen invalide.")
        return redirect(reverse("wiki:quiz_index") + "#" + _ancre(set_id))
    QuizDeck.objects.update_or_create(
        player=player_id(request), set_id=set_id,
        defaults={**quotas, "date_objectif": objectif, "auto_quota": request.POST.get("auto") == "1" and objectif is not None},
    )
    return redirect(reverse("wiki:quiz_index") + "#" + _ancre(set_id))


@require_POST
@login_required
def reset(request):
    set_id = request.POST.get("set", "")
    library = bibliotheque(request)
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


# ---------------------------------------------------------------------------
# Notifications web : abonnement de l'appareil, test
# ---------------------------------------------------------------------------
@login_required
def push_cle(request):
    from . import push

    abonnements = {a.endpoint: {"heure": a.heure, "minute": a.minute} for a in request.user.abonnements_push.all()}
    return JsonResponse({"cle": push.cle_publique(), "abonnements": abonnements})


def _json_post(request):
    try:
        data = json.loads(request.body)
        return data if isinstance(data, dict) else None
    except ValueError:
        return None


@login_required
@require_POST
def push_abonner(request):
    from .models import AbonnementPush

    data = _json_post(request)
    try:
        sub = data["subscription"]
        endpoint, p256dh, auth = str(sub["endpoint"]), str(sub["keys"]["p256dh"]), str(sub["keys"]["auth"])
        heure, minute = int(data.get("heure", 19)), int(data.get("minute", 0))
        if not endpoint.startswith("https://") or not (0 <= heure <= 23 and 0 <= minute <= 59):
            raise ValueError
    except (KeyError, TypeError, ValueError):
        return JsonResponse({"error": "abonnement invalide"}, status=400)
    maintenant = timezone.localtime()
    # Heure déjà passée aujourd'hui : premier rappel demain (pas tout de suite).
    deja = (heure, minute) <= (maintenant.hour, maintenant.minute)
    AbonnementPush.objects.update_or_create(endpoint=endpoint, defaults={
        "user": request.user, "p256dh": p256dh, "auth": auth, "heure": heure, "minute": minute,
        "agent": request.headers.get("User-Agent", "")[:300], "dernier_envoi": maintenant.date() if deja else None})
    return JsonResponse({"ok": True, "heure": heure, "minute": minute})


@login_required
@require_POST
def push_desabonner(request):
    data = _json_post(request) or {}
    request.user.abonnements_push.filter(endpoint=str(data.get("endpoint", ""))).delete()
    return JsonResponse({"ok": True})


@login_required
@require_POST
def push_tester(request):
    from . import push

    data = _json_post(request) or {}
    abonnement = request.user.abonnements_push.filter(endpoint=str(data.get("endpoint", ""))).first()
    if abonnement is None:
        return JsonResponse({"error": "appareil non abonné"}, status=404)
    texte = texte_rappel(etat_rappel(player_id(request))) or "Tout est à jour ✓"
    try:
        push.envoyer(abonnement, "ProjetPluri · test", texte)
    except push.AbonnementExpire:
        abonnement.delete()
        return JsonResponse({"error": "abonnement expiré : réactivez le rappel"}, status=410)
    except Exception as e:  # noqa: BLE001
        return JsonResponse({"error": f"envoi impossible : {e}"}, status=502)
    return JsonResponse({"ok": True})
