"""Vues qui passent par Claude (et l'import de listes de mots) : transformations de cours,
génération de QCM et de vocabulaire, relecture des brouillons, explications, réponses
rédigées, tuteur de page, « Améliorer » de l'éditeur, réglages (clé d'API, plafond)."""

import re

from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import claude, claude_demandes, paquets
from .models import (
    EchangeTuteur,
    Explication,
    QuizProgress,
    ReglagesClaude,
    Transformation,
    UsageClaude,
)
from .vault import get_vault
from .vues_communes import _deny, _render, can_edit


def _cartes_de_la_page(vault, note):
    """Cartes qu'on peut tirer de la page (encadrés, surlignages) et set déjà écrit, s'il existe."""
    from . import cartes, quiz

    try:
        texte = (vault.root / note.path).read_text(encoding="utf-8")
    except OSError:
        return None
    nombre = len(cartes.extraire(texte))
    if not nombre:
        return None
    return {"nombre": nombre, "existe": quiz.get_library().commune().get(cartes.chemin_du_set(note).removesuffix(".json")) is not None}


@require_POST
def cartes_page(request):
    """Écrit (ou met à jour) le set de cartes tirées d'une page : encadrés et surlignages, sans Claude."""
    from . import cartes

    if not can_edit(request):
        return _deny(request)
    vault = get_vault()
    note = vault.notes.get(request.POST.get("page", "").strip().removesuffix(".md").lower())
    if note is None:
        messages.error(request, "Page introuvable.")
        return redirect("wiki:home")
    questions = cartes.extraire((vault.root / note.path).read_text(encoding="utf-8"))
    if not questions:
        messages.info(request, "Rien à tirer de cette page : ajoutez des encadrés à titre (> [!definition] Titre) ou des ==surlignages==.")
        return redirect(note.url)
    chemin = cartes.chemin_du_set(note)
    existait = (vault.root / chemin).exists()
    try:
        paquets.enregistrer_json(chemin, cartes.set_de_la_page(note, questions))
    except paquets.PaquetInvalide as e:
        messages.error(request, str(e))
        return redirect(note.url)
    n = len(questions)
    messages.success(request, f"{'Cartes mises à jour' if existait else 'Cartes créées'} : {n} question{'s' if n > 1 else ''} "
                              f"dans « {note.title} — cartes » ({chemin}).")
    return redirect(note.url)


def _tuteur_de_la_page(request, vault, note):
    """Historique du tuteur sur cette page pour l'utilisateur, si Claude est disponible."""
    if not claude.disponible():
        return None
    from .quiz_views import _render_html, player_id

    echanges = EchangeTuteur.objects.filter(player=player_id(request), page=note.key)
    return {"echanges": [{"question": e.question, "html": _render_html(vault, e.reponse), "quand": e.cree_le}
                         for e in list(echanges)[-claude_demandes.HISTORIQUE_TUTEUR:]],
            "plafond": claude.plafond_atteint()}


@require_POST
def tuteur(request):
    """Question au tuteur sur une page : réponse de Claude ancrée sur la page, gardée dans l'historique."""
    import json

    from .quiz_views import _render_html, player_id

    try:
        data = json.loads(request.body)
        cle, question = str(data["page"]).strip().removesuffix(".md"), str(data["question"]).strip()
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)
    vault = get_vault()
    note = vault.notes.get(cle.lower())
    if note is None or not question:
        return JsonResponse({"error": "page inconnue ou question vide"}, status=404)
    if not claude.disponible():
        return JsonResponse({"error": "Pas de clé d'API Claude sur le serveur."}, status=503)
    if claude.plafond_atteint():
        return JsonResponse({"error": "Plafond mensuel de Claude atteint : le tuteur reviendra le mois prochain."}, status=429)
    player = player_id(request)
    historique = [(e.question, e.reponse) for e in list(EchangeTuteur.objects.filter(player=player, page=note.key))[-claude_demandes.HISTORIQUE_TUTEUR:]]
    try:
        texte, usage, modele_id = claude_demandes.tuteur(note, question, historique)
    except claude.Echec as e:
        return JsonResponse({"error": str(e)}, status=502)
    EchangeTuteur.objects.create(player=player, page=note.key, question=question[:claude_demandes.MAX_CHARS_QUESTION], reponse=texte,
                                 modele=modele_id, jetons_entree=usage[0], jetons_sortie=usage[1])
    claude.noter_usage(UsageClaude.TUTEUR, player, modele_id, usage)
    return JsonResponse({"html": _render_html(vault, texte), "modele": modele_id})


def _transformer_cours(request, vault, results, lot=False):
    """Cours importés (PDF, LaTeX) confiés à Claude, qui les transforme en pages en
    arrière-plan (``lot`` : dans un lot, moitié prix, sous 24 h). Renvoie le nombre
    de transformations lancées."""
    suivi = reverse("wiki:transformations")
    qui = request.user.get_username()
    lances = 0
    for r in results:
        if not r.ok:
            continue
        if r.source_latex:
            claude.demander_latex(r.name, r.source_latex, r.path, qui, lot=lot)
        elif r.path.lower().endswith(".pdf") and (pdf := vault.attachments.get(r.path.lower())) is not None:
            claude.demander_pdf(pdf, qui, lot=lot)
        else:
            continue
        r.message += " · transformation par Claude " + ("dans un lot (sous 24 h)" if lot else "lancée")
        r.claude = suivi
        lances += 1
    return lances


def _resultat(vault, t):
    """(adresse, texte du lien) du résultat d'un travail de Claude, ou ("", "")."""
    from urllib.parse import quote

    if t.statut != Transformation.FAIT or not t.page_ecrite:
        return "", ""
    if t.genre == Transformation.QCM:
        set_id = t.page_ecrite.removesuffix(".json")
        return f"{reverse('wiki:quiz_play')}?set={quote(set_id)}&mode=all", "Jouer ce QCM"
    if t.genre == Transformation.VOCABULAIRE:
        set_id = t.page_ecrite.removesuffix(".json")
        langue = (t.options or {}).get("langue", "Anglais")
        return f"{reverse('wiki:langue_play', args=[langue])}?mode=quotidien&fichier={quote(set_id)}", "Réviser ce paquet"
    note = vault.notes.get(t.page_ecrite.removesuffix(".md").lower())
    lien = "Ouvrir la fiche" if t.genre == Transformation.FICHE else "Ouvrir la page"
    return (reverse("wiki:page", args=[note.key]), lien) if note else ("", "")


def transformations(request):
    """Suivi des cours transformés par Claude ; relancer un échec ; transformer un PDF du coffre."""
    if not can_edit(request):
        return _deny(request)
    vault = get_vault()
    if request.method == "POST":
        if not claude.disponible():
            messages.error(request, "Aucune clé d'API : ajoutez-la dans les réglages de Claude.")
        elif pk := request.POST.get("relancer"):
            claude.relancer(get_object_or_404(Transformation, pk=pk))
        elif request.POST.get("verifier_lots"):
            try:
                n = claude.verifier_lots()
            except claude.Echec as e:
                messages.error(request, str(e))
            else:
                messages.success(request, f"{n} travail{'aux' if n > 1 else ''} terminé{'s' if n > 1 else ''}." if n
                                 else "Les lots ne sont pas encore traités par Anthropic : revenez plus tard.")
        elif pk := request.POST.get("publier"):
            t = get_object_or_404(Transformation, pk=pk)
            try:
                claude.publier(t)
                messages.success(request, f"« {t.nom} » publié.")
            except claude.Echec as e:
                messages.error(request, str(e))
        elif pk := request.POST.get("supprimer"):
            claude.supprimer_brouillon(get_object_or_404(Transformation, pk=pk, statut=Transformation.BROUILLON))
            messages.success(request, "Brouillon supprimé.")
        elif cle := request.POST.get("fiche"):
            note = vault.notes.get(cle.lower())
            if note is None:
                raise Http404("Page introuvable")
            if Transformation.objects.filter(genre=Transformation.FICHE, source=note.path.as_posix(),
                                             statut__in=[Transformation.ATTENTE, Transformation.EN_COURS]).exists():
                messages.info(request, f"La fiche de « {note.title} » est déjà en préparation.")
            else:
                claude.demander_fiche(note, request.user.get_username())
                messages.success(request, f"Claude rédige la fiche de révision de « {note.title} ».")
        elif chemin := request.POST.get("pdf"):
            pdf = vault.attachments.get(chemin.lower())
            if pdf is None or pdf.suffix != ".pdf":
                raise Http404("PDF introuvable")
            source = pdf.path.as_posix()
            if Transformation.objects.filter(source=source, statut__in=[Transformation.ATTENTE, Transformation.EN_COURS]).exists():
                messages.info(request, f"{pdf.name} est déjà en cours de transformation.")
            else:
                lot = request.POST.get("lot") == "1"
                claude.demander_pdf(pdf, request.user.get_username(), lot=lot)
                messages.success(request, f"Transformation de {pdf.name} " + ("déposée dans un lot (résultat sous 24 h)." if lot else "lancée."))
        return redirect("wiki:transformations")

    liste = list(Transformation.objects.all()[:50])
    en_cours = any(t.statut in (Transformation.ATTENTE, Transformation.EN_COURS) for t in liste)
    lots = any(t.statut == Transformation.LOT for t in liste)
    if en_cours:
        claude.lancer()  # reprend après un redémarrage du serveur
    if lots:
        claude.surveiller_lots()
    for t in liste:
        t.cout = claude.cout(t)
        t.url_page, t.lien = _resultat(vault, t)
    return _render(request, vault, "wiki/transformations.html", {
        "transformations": liste,
        "en_cours": en_cours,
        "lots": lots,
        "claude_dispo": claude.disponible(),
        "modele": claude.modele(),
    })


CLE_RE = re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")


LANGUE_RE = re.compile(r"[^\W\d_][^\W\d_ '-]*(?:[ '-][^\W\d_]+)*")


def _options_vocabulaire(request):
    """Langue, types de cartes, dossier et titre d'un paquet de vocabulaire demandé
    par formulaire : ({langue, types, dossier, titre}, message d'erreur ou "")."""
    from . import langues

    langue = " ".join(request.POST.get("langue", "").split()) or "Anglais"
    types = [t for t in request.POST.getlist("cartes") if t in langues.TYPES_VOCABULAIRE]
    dossier = request.POST.get("dossier", "").strip()
    erreur = (
        "Langue invalide." if len(langue) > 40 or not LANGUE_RE.fullmatch(langue)
        else "Cochez au moins un type de carte." if not types
        else 'Dossier invalide : un seul nom de dossier, sans / \\ : * ? " < > | # ^ [ ].' if dossier and paquets.dossier_valide(dossier) is None
        else ""
    )
    options = {"langue": langue[0].upper() + langue[1:], "types": types, "dossier": paquets.dossier_valide(dossier) or "",
               "titre": request.POST.get("titre", "").strip()[:120]}
    return options, erreur


@require_POST
def lire_liste(request):
    """Paquet de vocabulaire d'après une liste collée ou un fichier exporté (Quizlet,
    Anki, tableur) du formulaire : (paquet, options, lignes ignorées, erreur)."""
    options, erreur = _options_vocabulaire(request)
    texte = request.POST.get("liste", "")
    fichier = request.FILES.get("fichier")
    if fichier is not None:
        if fichier.size > 1024 * 1024:
            erreur = erreur or "Fichier trop gros (1 Mo au plus)."
        else:
            brut = fichier.read()
            try:
                texte = brut.decode("utf-8-sig")
            except UnicodeDecodeError:
                texte = brut.decode("cp1252", errors="replace")
    ordre = request.POST.get("ordre", paquets.LANGUE_PUIS_FR)
    if ordre not in paquets.ORDRES:
        ordre = paquets.LANGUE_PUIS_FR
    fiches, ignorees = [], 0
    if not erreur:
        try:
            fiches, ignorees = paquets.analyser_liste(texte, ordre)
        except paquets.PaquetInvalide as e:
            erreur = str(e)
        else:
            if not fiches:
                erreur = "Aucune ligne « mot – traduction » reconnue : une ligne par mot, séparés par une tabulation, une virgule ou « = »."
    if erreur:
        return None, options, 0, erreur
    titre = options["titre"] or f"Vocabulaire {options['langue'].lower()} du {timezone.localdate():%d/%m/%Y}"
    paquet = paquets.paquet_vocabulaire(options["langue"], titre, "", options["types"], fiches, "Import de liste")
    return paquet, options, ignorees, None


def message_paquet(paquet, ignorees):
    n = len(paquet["vocabulaire"])
    return (f"Paquet « {paquet['titre']} » créé : {n} mot{'s' if n > 1 else ''}"
            + (f", {ignorees} ligne{'s' if ignorees > 1 else ''} ignorée{'s' if ignorees > 1 else ''}" if ignorees else "") + ".")


def importer_vocabulaire(request):
    """Paquet de vocabulaire d'après une liste collée ou un fichier exporté (Quizlet,
    Anki, tableur), sans Claude : un paquet à part, prêt à réviser."""
    if not can_edit(request):
        return _deny(request)
    retour = redirect(reverse("wiki:quiz_index") + "#importer-vocabulaire")
    paquet, options, ignorees, erreur = lire_liste(request)
    if erreur:
        messages.error(request, erreur)
        return retour
    try:
        rel = paquets.ecrire_paquet_langue(options["dossier"] or claude.DOSSIER_VOCABULAIRE, paquet)
    except paquets.PaquetInvalide as e:
        messages.error(request, str(e))
        return retour
    messages.success(request, message_paquet(paquet, ignorees))
    from urllib.parse import urlencode

    return redirect(reverse("wiki:langue_menu", args=[options["langue"]]) + "?" + urlencode({"fichier": rel.removesuffix(".json")}))


@require_POST
def generer(request):
    """QCM (d'après une page du wiki ou un texte collé) ou paquet de vocabulaire
    (d'après des mots collés), générés par Claude en arrière-plan."""

    if not can_edit(request):
        return _deny(request)
    if not claude.disponible():
        messages.error(request, "Ajoutez d'abord une clé d'API dans les réglages de Claude.")
        return redirect("wiki:claude_reglages")
    qui = request.user.get_username()
    genre = request.POST.get("genre")
    retour = redirect(reverse("wiki:quiz_index") + "#generer")

    if genre == "qcm":
        cle = request.POST.get("page", "").strip().removesuffix(".md")
        texte = request.POST.get("texte", "").strip()
        nombre = request.POST.get("nombre", "")
        nombre = int(nombre) if nombre.isdigit() and int(nombre) in claude.NOMBRES_QUESTIONS else 20
        categorie = request.POST.get("categorie", "").strip()
        if categorie and claude.dossier_valide(categorie) is None:
            messages.error(request, 'Catégorie invalide : un seul nom de dossier, sans / \\ : * ? " < > | # ^ [ ].')
            return retour
        note = None
        if cle:
            note = get_vault().notes.get(cle.lower())
            if note is None:
                messages.error(request, f"Page introuvable : « {cle} ».")
                return retour
        elif not texte:
            messages.error(request, "Choisissez une page du wiki ou collez le texte du cours.")
            return retour
        elif len(texte) > 300_000:
            messages.error(request, "Texte trop long (300 000 caractères au plus) : générez le QCM d'une partie à la fois.")
            return retour
        claude.demander_qcm(note=note, texte="" if note else texte, nombre=nombre,
                            categorie=claude.dossier_valide(categorie) or "", titre=request.POST.get("titre", "").strip()[:120],
                            utilisateur=qui, publier=request.POST.get("publier") == "1", lot=request.POST.get("lot") == "1")
        messages.success(request, f"Claude écrit {nombre} questions sur « {note.title if note else 'le texte collé'} ».")
    elif genre == "variantes":
        from . import quiz
        from .quiz_views import player_id, question_ratee

        qset = quiz.get_library().pour(player_id(request)).get(request.POST.get("set", ""))
        if qset is None:
            messages.error(request, "Set introuvable.")
            return redirect("wiki:quiz_stats")
        progress = QuizProgress.map_for(player_id(request), qset.id)
        ratees = sorted((st for st in progress.values() if question_ratee(st)),
                        key=lambda st: (st.correct / st.seen if st.seen else 0, -st.seen))
        ids = [st.question_id for st in ratees if any(q.id == st.question_id for q in qset.questions)][:claude.MAX_VARIANTES]
        if not ids:
            messages.info(request, f"Aucune question ratée dans « {qset.titre} » : rien à varier.")
            return redirect("wiki:quiz_stats")
        claude.demander_variantes(qset, ids, utilisateur=qui)
        messages.success(request, f"Claude écrit {len(ids)} variante{'s' if len(ids) > 1 else ''} des questions ratées de « {qset.titre} » (brouillon à relire).")
    elif genre == "vocabulaire":
        mots = request.POST.get("mots", "").strip()
        lignes = [l for l in mots.splitlines() if l.strip()]
        options, erreur = _options_vocabulaire(request)
        if not lignes:
            erreur = "Collez au moins un mot."
        elif len(lignes) > claude.MAX_MOTS:
            erreur = f"Trop de mots ({len(lignes)}) : {claude.MAX_MOTS} au plus par paquet."
        if erreur:
            messages.error(request, erreur)
            return retour
        claude.demander_vocabulaire(mots="\n".join(l.strip() for l in lignes)[:20_000], utilisateur=qui,
                                    publier=request.POST.get("publier") == "1", lot=request.POST.get("lot") == "1", **options)
        messages.success(request, f"Claude prépare un paquet de {len(lignes)} mot{'s' if len(lignes) > 1 else ''} en {options['langue'].lower()}.")
    else:
        messages.error(request, "Demande inconnue.")
        return retour
    return redirect("wiki:transformations")


def reglages_claude(request):
    """Clé d'API et modèle de Claude, saisis par un admin. La clé est vérifiée
    auprès d'Anthropic avant d'être enregistrée, et jamais réaffichée en entier."""
    if not can_edit(request):
        return _deny(request)
    reglages = ReglagesClaude.charger()
    if request.method == "POST":
        if request.POST.get("action") == "supprimer":
            reglages.cle = ""
            reglages.modifie_le, reglages.modifie_par = timezone.now(), request.user.get_username()
            reglages.save()
            messages.success(request, "Clé supprimée.")
            return redirect("wiki:claude_reglages")
        modele = request.POST.get("modele") or reglages.modele
        if modele and modele not in {m[0] for m in claude.MODELES}:
            messages.error(request, "Modèle inconnu.")
            return redirect("wiki:claude_reglages")
        plafond = request.POST.get("plafond", "").strip().replace(",", ".")
        if plafond:
            try:
                reglages.plafond_mensuel = max(0.0, min(1000.0, float(plafond)))
            except ValueError:
                messages.error(request, "Plafond invalide : un montant en dollars (0 pour aucun plafond).")
                return redirect("wiki:claude_reglages")
        nouvelle = "".join(request.POST.get("cle", "").split())
        if nouvelle:
            if not CLE_RE.fullmatch(nouvelle):
                messages.error(request, "Ce n'est pas une clé d'API Anthropic (elle commence par sk-ant-).")
                return redirect("wiki:claude_reglages")
            ok, raison = claude.verifier(nouvelle, modele or claude.MODELE_PAR_DEFAUT)
            if ok is False:
                messages.error(request, raison)
                return redirect("wiki:claude_reglages")
            reglages.cle = nouvelle
            if ok is None:
                messages.warning(request, f"{raison} La clé est enregistrée quand même.")
            else:
                messages.success(request, "Clé vérifiée et enregistrée.")
        else:
            messages.success(request, "Réglages enregistrés.")
        reglages.modele = modele
        reglages.modifie_le, reglages.modifie_par = timezone.now(), request.user.get_username()
        reglages.save()
        return redirect("wiki:claude_reglages")

    source = "site" if reglages.cle else "env" if claude.cle_env() else None
    return _render(request, get_vault(), "wiki/claude_reglages.html", {
        "reglages": reglages,
        "source": source,
        "modeles": claude.MODELES,
        "modele": claude.modele(),
        "cout_demande": claude.cout_a_la_demande_du_mois(),
        "cout_total": claude.cout_du_mois(),
    })


def relire(request, pk):
    """Relecture d'un brouillon (QCM ou paquet de vocabulaire généré) : garder, corriger, publier."""
    from . import quiz

    if not can_edit(request):
        return _deny(request)
    t = get_object_or_404(Transformation, pk=pk)
    if t.statut != Transformation.BROUILLON or not t.resultat:
        messages.info(request, "Ce travail n'est plus un brouillon.")
        return redirect("wiki:transformations")
    contenu = t.resultat["contenu"]
    if request.method == "POST":
        if request.POST.get("action") == "supprimer":
            claude.supprimer_brouillon(t)
            messages.success(request, "Brouillon supprimé.")
            return redirect("wiki:transformations")
        corrige = dict(contenu)
        corrige["titre"] = request.POST.get("titre", "").strip() or contenu.get("titre", "")
        corrige["description"] = request.POST.get("description", "").strip()
        gardes, refus = [], []
        if t.genre == Transformation.QCM:
            for i, q in enumerate(contenu["questions"]):
                if request.POST.get(f"q{i}-garder") != "1":
                    continue
                nouvelle = _question_relue(request, i, q)
                try:
                    quiz.question_depuis_json(nouvelle, i + 1, f"question {i + 1}")
                except ValueError as e:
                    refus.append(str(e))
                    continue
                gardes.append(nouvelle)
            corrige["questions"] = gardes
            total = len(contenu["questions"])
        else:
            for i, fiche in enumerate(contenu["vocabulaire"]):
                if request.POST.get(f"v{i}-garder") != "1":
                    continue
                nouvelle = dict(fiche)
                nouvelle["mot"] = request.POST.get(f"v{i}-mot", "").strip() or fiche["mot"]
                trads = [x.strip() for x in request.POST.get(f"v{i}-traductions", "").split(";") if x.strip()]
                nouvelle["traductions"] = trads or fiche["traductions"]
                for champ in ("exemple", "exemple_traduction", "note"):
                    valeur = request.POST.get(f"v{i}-{champ}", "").strip()
                    if valeur:
                        nouvelle[champ] = valeur
                    else:
                        nouvelle.pop(champ, None)
                gardes.append(nouvelle)
            corrige["vocabulaire"] = gardes
            total = len(contenu["vocabulaire"])
        if refus:
            messages.error(request, "Questions non publiées : " + " · ".join(refus))
        if not gardes:
            messages.error(request, "Rien à publier : gardez au moins un élément.")
            return redirect("wiki:relire", pk=t.pk)
        try:
            claude.publier(t, corrige)
        except claude.Echec as e:
            messages.error(request, str(e))
            return redirect("wiki:relire", pk=t.pk)
        t.message = f"Publié après relecture : {len(gardes)} sur {total} gardé{'s' if len(gardes) > 1 else ''}."
        t.save(update_fields=["message"])
        messages.success(request, f"« {corrige['titre']} » publié ({len(gardes)} sur {total}).")
        url, _ = _resultat(get_vault(), t)
        return redirect(url or reverse("wiki:transformations"))

    questions = []
    if t.genre == Transformation.QCM:
        for i, q in enumerate(contenu["questions"]):
            questions.append({"i": i, "q": q, "choix": list(enumerate(q.get("choix", []))),
                              "reponses_texte": " / ".join(q.get("reponses_texte", [])), "qcr": q.get("type") == "QCR"})
    return _render(request, get_vault(), "wiki/claude_relire.html", {
        "t": t, "contenu": contenu, "questions": questions,
        "fiches": list(enumerate(contenu.get("vocabulaire", []))) if t.genre == Transformation.VOCABULAIRE else [],
        "avertissement": t.message.replace("À relire avant publication.", "").strip(),
    })


def _question_relue(request, i, q):
    """Question du brouillon après correction dans le formulaire de relecture."""
    nouvelle = {k: v for k, v in q.items() if k not in ("choix", "reponses", "reponses_texte", "verso", "explication", "consigne")}
    nouvelle["question"] = request.POST.get(f"q{i}-question", "").strip() or q.get("question", "")
    type_q = str(q.get("type", "QCM")).upper()
    if type_q in ("QCM", "QCR"):
        choix = [request.POST.get(f"q{i}-choix-{j}", "").strip() for j in range(len(q.get("choix", [])))]
        bonnes = [j for j in range(len(choix)) if request.POST.get(f"q{i}-bonne-{j}") == "1"] if type_q == "QCR" \
            else [int(request.POST.get(f"q{i}-bonne", -1))] if request.POST.get(f"q{i}-bonne", "").isdigit() else []
        # Un choix vidé disparaît ; les indices des bonnes réponses suivent.
        garde = [j for j, c in enumerate(choix) if c]
        nouvelle["choix"] = [choix[j] for j in garde]
        nouvelle["reponses"] = sorted(garde.index(j) for j in bonnes if j in garde)
    elif type_q in ("TROU", "QRC"):
        nouvelle["reponses_texte"] = [x.strip() for x in request.POST.get(f"q{i}-reponses", "").split("/") if x.strip()]
        if request.POST.get(f"q{i}-consigne", "").strip():
            nouvelle["consigne"] = request.POST.get(f"q{i}-consigne", "").strip()
    elif type_q == "FLASHCARD":
        nouvelle["verso"] = request.POST.get(f"q{i}-verso", "").strip()
    explication = request.POST.get(f"q{i}-explication", "").strip()
    if explication:
        nouvelle["explication"] = explication
    return nouvelle


@require_POST
def expliquer(request):
    """« Explique-moi » sur une question de QCM : explication par Claude, gardée."""
    import json

    from . import quiz
    from .quiz_views import _render_html, player_id

    try:
        data = json.loads(request.body)
        set_id, question_id = str(data["set_id"]), str(data["question_id"])
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)
    qset = quiz.get_library().pour(player_id(request)).get(set_id)
    question = next((q for q in qset.questions if q.id == question_id), None) if qset else None
    if question is None:
        return JsonResponse({"error": "question inconnue"}, status=404)
    vault = get_vault()
    existante = Explication.objects.filter(set_id=set_id, question_id=question_id).first()
    if existante is not None:
        return JsonResponse({"html": _render_html(vault, existante.texte), "modele": existante.modele, "gardee": True})
    if not claude.disponible():
        return JsonResponse({"error": "Pas de clé d'API Claude sur le serveur."}, status=503)
    try:
        texte, usage, modele_id = claude_demandes.expliquer(qset, question)
    except claude.Echec as e:
        return JsonResponse({"error": str(e)}, status=502)
    Explication.objects.update_or_create(
        set_id=set_id, question_id=question_id,
        defaults={"texte": texte, "modele": modele_id, "jetons_entree": usage[0], "jetons_sortie": usage[1]})
    return JsonResponse({"html": _render_html(vault, texte), "modele": modele_id, "gardee": False})


@require_POST
def corriger_qrc(request):
    """Réponse rédigée (QRC) différente du corrigé : verdict de Claude (Haiku) sur le fond."""
    import json

    from . import quiz
    from .quiz_views import player_id

    try:
        data = json.loads(request.body)
        set_id, question_id, reponse = str(data["set_id"]), str(data["question_id"]), str(data["reponse"]).strip()
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)
    qset = quiz.get_library().pour(player_id(request)).get(set_id)
    question = next((q for q in qset.questions if q.id == question_id), None) if qset else None
    if question is None or not question.est_qrc or not reponse:
        return JsonResponse({"error": "question inconnue"}, status=404)
    if not claude.disponible():
        return JsonResponse({"error": "Pas de clé d'API Claude sur le serveur."}, status=503)
    if claude.plafond_atteint():
        return JsonResponse({"error": "Plafond mensuel de Claude atteint : correction stricte."}, status=429)
    try:
        verdict, retour, usage, modele_id = claude_demandes.corriger_qrc(qset, question, reponse)
    except claude.Echec as e:
        return JsonResponse({"error": str(e)}, status=502)
    claude.noter_usage(UsageClaude.QRC, player_id(request), modele_id, usage)
    return JsonResponse({"verdict": verdict, "retour": retour, "correct": verdict == "juste", "modele": modele_id})


@require_POST
def ameliorer(request):
    """« Améliorer la rédaction » dans l'éditeur : le passage sélectionné, relu par Claude."""
    if not can_edit(request):
        return JsonResponse({"error": "Réservé aux admins."}, status=403)
    if not claude.disponible():
        return JsonResponse({"error": "Pas de clé d'API Claude sur le serveur."}, status=503)
    texte = request.POST.get("texte", "")
    if not texte.strip():
        return JsonResponse({"error": "Sélectionnez d'abord le texte à améliorer."}, status=400)
    try:
        resultat, usage = claude_demandes.ameliorer(texte)
    except claude.Echec as e:
        return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"texte": resultat, "jetons": list(usage)})
