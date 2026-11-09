import re
from pathlib import PurePosixPath

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_POST

from accounts.roles import is_admin

from . import claude
from . import historique
from . import latex as latex_converter
from . import paquets
from . import uploads
from .models import EchangeTuteur, Explication, QuizProgress, ReglagesClaude, Transformation, UsageClaude
from .render import IMAGE_EXTS, Renderer, render_note
from .vault import CODE_RE, Note, clean_key, get_vault, split_frontmatter


def can_edit(request):
    """Seuls les admins modifient le wiki."""
    return is_admin(request.user)


def _deny(request):
    """Anonyme → page de connexion ; utilisateur simple → 403."""
    if request.user.is_authenticated:
        raise PermissionDenied
    return redirect_to_login(request.get_full_path())


def _wants_json(request):
    """Requête envoyée par le JavaScript de l'éditeur ou de l'import (réponse JSON)."""
    return "application/json" in request.headers.get("Accept", "")


def _render(request, vault, template, context, status=200):
    context = {"vault": vault, "tree": vault.tree, "can_edit": can_edit(request), **context}
    return render(request, template, context, status=status)


def _qcm_de_la_page(request, note):
    """Sets de QCM écrits d'après cette page (source_page), avec la progression du joueur."""
    from . import quiz
    from .models import QuizDeck, QuizProgress
    from .quiz_views import _ancre, _set_summary, player_id

    cle = note.key.lower()
    sets = [s for s in quiz.get_library().sets.values() if s.source_page.lower() == cle]
    if not sets:
        return []
    player, now, decks = player_id(request), timezone.now(), QuizDeck.map_for(player_id(request))
    return [{"set": s, "ancre": _ancre(s.id),
             "summary": _set_summary(s, QuizProgress.map_for(player, s.id), now, decks.get(s.id))}
            for s in sorted(sets, key=lambda s: s.titre.lower())]


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
    return {"nombre": nombre, "existe": quiz.get_library().get(cartes.chemin_du_set(note).removesuffix(".json")) is not None}


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
                         for e in list(echanges)[-claude.HISTORIQUE_TUTEUR:]],
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
    historique = [(e.question, e.reponse) for e in list(EchangeTuteur.objects.filter(player=player, page=note.key))[-claude.HISTORIQUE_TUTEUR:]]
    try:
        texte, usage, modele_id = claude.tuteur(note, question, historique)
    except claude.Echec as e:
        return JsonResponse({"error": str(e)}, status=502)
    EchangeTuteur.objects.create(player=player, page=note.key, question=question[:claude.MAX_CHARS_QUESTION], reponse=texte,
                                 modele=modele_id, jetons_entree=usage[0], jetons_sortie=usage[1])
    claude.noter_usage(UsageClaude.TUTEUR, player, modele_id, usage)
    return JsonResponse({"html": _render_html(vault, texte), "modele": modele_id})


def _note_page(request, vault, note):
    content, toc = vault.render(note)
    backlinks = sorted(vault.backlinks.get(note.key.lower(), ()), key=lambda n: n.title.lower())
    fiche = vault.notes.get(note.path.with_name(f"{note.path.stem} (Fiche)").with_suffix("").as_posix().lower())
    return _render(request, vault, "wiki/page.html", {
        "note": note,
        "content": content,
        "toc": toc,
        "backlinks": backlinks,
        "claude_dispo": can_edit(request) and claude.disponible(),
        "fiche": fiche,
        "qcm_page": _qcm_de_la_page(request, note),
        "cartes": _cartes_de_la_page(vault, note) if can_edit(request) else None,
        "tuteur": _tuteur_de_la_page(request, vault, note),
        "fiche_en_cours": fiche is None and Transformation.objects.filter(
            genre=Transformation.FICHE, source=note.path.as_posix(),
            statut__in=[Transformation.ATTENTE, Transformation.EN_COURS]).exists(),
    })


def home(request):
    vault = get_vault()
    note = vault.home()
    if note is not None:
        return _note_page(request, vault, note)
    return _render(request, vault, "wiki/index.html", {"recent": vault.recent_notes()})


def page(request, path):
    vault = get_vault()
    note = vault.notes.get(path.lower().removesuffix(".md"))
    if note is None:
        # Lien court (/wiki/Ma note) vers une note rangée dans un sous-dossier.
        target = vault.resolve(path)
        if target is not None:
            return redirect(target.url)
        backlinks = sorted(vault.unresolved.get(path.lower(), ()), key=lambda n: n.title.lower())
        return _render(request, vault, "wiki/missing.html", {
            "name": path,
            "filename": f"{path}.md",
            "backlinks": backlinks,
            "can_create": clean_key(path) is not None,
        }, status=404)
    return _note_page(request, vault, note)


def edit(request, path):
    """Création ou modification d'une note depuis le navigateur."""
    if not can_edit(request):
        return _deny(request)
    vault = get_vault()
    key = clean_key(path)
    if key is None:
        raise Http404("Nom de page invalide")
    note = vault.notes.get(key.lower())
    if note is None and "/" not in key:
        # /modifier/Ma note pour une note rangée dans un sous-dossier.
        target = vault.resolve(key)
        if isinstance(target, Note):
            return redirect("wiki:edit", target.key)
    if note is not None:
        key = note.key
    file = vault.root / f"{key}.md"
    version = str(file.stat().st_mtime_ns) if file.is_file() else ""
    error = ""

    if request.method == "POST":
        content = request.POST.get("content", "").replace("\r\n", "\n")
        if request.POST.get("version", "") != version:
            error = (
                "Cette page a été modifiée ailleurs depuis l'ouverture de l'éditeur. "
                "Copiez votre texte, rechargez la page, puis réappliquez vos changements."
            )
            if _wants_json(request):
                return JsonResponse({"error": error}, status=409)
        else:
            file.parent.mkdir(parents=True, exist_ok=True)
            if file.is_file():
                ancien = file.read_text(encoding="utf-8")
                if ancien != content:
                    historique.sauvegarder(f"{key}.md", ancien, request.user.get_username())
            file.write_text(content, encoding="utf-8", newline="\n")
            if _wants_json(request):
                # Ctrl+S dans l'éditeur : on reste sur la page, avec la nouvelle version.
                return JsonResponse({"version": str(file.stat().st_mtime_ns), "url": reverse("wiki:page", args=[key])})
            return redirect("wiki:page", key)
    else:
        content = file.read_text(encoding="utf-8").lstrip("\ufeff") if file.is_file() else ""

    return _render(request, vault, "wiki/edit.html", {
        "note": note,
        "key": key,
        "folders": key.split("/")[:-1],
        "name": key.rsplit("/", 1)[-1],
        "is_new": note is None,
        "content": content,
        "version": version,
        "error": error,
        "link_choices": vault.link_choices(),
        "attachment_choices": vault.attachment_choices(uploads.ATTACHMENT_EXTS),
        "tag_choices": [t for t, _ in vault.all_tags()],
        "preview_url": reverse("wiki:preview", args=[key]),
        "import_url": reverse("wiki:import"),
        "latex_url": reverse("wiki:latex"),
        "ameliorer_url": reverse("wiki:claude_ameliorer") if claude.disponible() else "",
    })


@require_POST
def preview(request, path):
    """Rendu HTML du texte en cours d'édition (bouton « Aperçu »)."""
    if not can_edit(request):
        return HttpResponse(status=403)
    key = clean_key(path) or "Aperçu"
    meta, body = split_frontmatter(request.POST.get("content", "").replace("\r\n", "\n"))
    note = Note(PurePosixPath(f"{key}.md"), 0, meta, body)
    return HttpResponse(Renderer(get_vault(), note).convert(body))


@require_POST
def latex(request):
    """Conversion d'un document LaTeX en Markdown pour l'éditeur (bouton, collage, fichier .tex)."""
    if not can_edit(request):
        return JsonResponse({"error": "Réservé aux admins."}, status=403)
    source = request.POST.get("source", "")
    if not source.strip():
        return JsonResponse({"error": "Aucun texte LaTeX à convertir."}, status=400)
    try:
        markdown = latex_converter.convert(source)
    except (RecursionError, ValueError, IndexError):
        return JsonResponse({"error": "Ce LaTeX n'a pas pu être converti."}, status=400)
    return JsonResponse({"markdown": markdown})


def new(request):
    """Formulaire « Nouvelle page » : choisit un nom et un dossier."""
    if not can_edit(request):
        return _deny(request)
    vault = get_vault()
    name = request.GET.get("name", "").strip()
    folder = request.GET.get("folder", "").strip()
    error = ""
    if name:
        key = clean_key(f"{folder}/{name}")
        if key is None or "/" in name:
            error = 'Le nom ne doit pas contenir les caractères / \\ : * ? " < > | # ^ [ ]'
        elif key.lower() in vault.notes:
            error = "Une page porte déjà ce nom : choisissez-en un autre."
        else:
            return redirect("wiki:edit", key)
    return _render(request, vault, "wiki/new.html", {
        "folders": vault.folders(),
        "name": name,
        "folder": folder,
        "error": error,
    })


def import_files(request):
    """Import de notes .md (et de leurs images) par glisser-déposer.

    Champs : ``fichiers`` (les fichiers), ``chemins`` (chemin relatif de chacun,
    pour garder les sous-dossiers d'un dossier déposé), ``dossier`` (destination),
    ``remplacer`` (écraser les fichiers existants), ``pour_note`` (image collée
    dans l'éditeur : rangée comme Obsidian, sous un nom libre).
    """
    if not can_edit(request):
        return _deny(request)
    vault = get_vault()
    if request.method != "POST":
        return _render(request, vault, "wiki/import.html", {
            "folders": vault.folders(),
            "folder": request.GET.get("dossier", ""),
            "max_note": uploads.MAX_NOTE_SIZE // 1024 // 1024,
            "max_attachment": uploads.MAX_ATTACHMENT_SIZE // 1024 // 1024,
            "claude_dispo": claude.disponible(),
        })

    files = request.FILES.getlist("fichiers")
    paths = request.POST.getlist("chemins")
    note_key = clean_key(request.POST.get("pour_note", ""))
    rename = note_key is not None
    folder = vault.attachment_folder(note_key) if rename else uploads.clean_folder(request.POST.get("dossier", ""))
    error = ""
    if folder is None:
        error = f"Dossier de destination invalide : caractères interdits {uploads.FORBIDDEN_CHARS}, ou dossier caché."
    elif not files:
        error = "Aucun fichier reçu."
    if error:
        if _wants_json(request):
            return JsonResponse({"error": error}, status=400)
        messages.error(request, error)
        return redirect("wiki:import")

    replace = request.POST.get("remplacer") == "1"
    results = [
        uploads.import_file(vault, upload, paths[i] if i < len(paths) else "", folder, replace=replace, rename=rename,
                            auteur=request.user.get_username())
        for i, upload in enumerate(files)
    ]
    results = uploads.finish(get_vault(), results)
    lances = 0
    if request.POST.get("claude") == "1" and not rename and claude.disponible():
        lances = _transformer_cours(request, get_vault(), results, lot=request.POST.get("lot") == "1")
    if _wants_json(request):
        return JsonResponse({"results": [r.as_dict() for r in results]})

    done = [r for r in results if r.ok]
    if done:
        notes = sum(r.is_note for r in done)
        messages.success(request, f"{len(done)} fichier{'s' if len(done) > 1 else ''} importé{'s' if len(done) > 1 else ''}"
                         f" dont {notes} page{'s' if notes > 1 else ''}.")
    for r in results:
        if not r.ok and not r.ignored:
            messages.error(request, f"{r.name} : {r.message}")
    if lances:
        messages.info(request, f"{lances} cours en cours de transformation par Claude.")
        return redirect("wiki:transformations")
    if len(done) == 1 and done[0].url and (done[0].is_note or done[0].path.lower().endswith(".pdf")):
        return redirect(done[0].url)
    return redirect("wiki:import")


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
def importer_vocabulaire(request):
    """Paquet de vocabulaire d'après une liste collée ou un fichier exporté (Quizlet,
    Anki, tableur), sans Claude : un paquet à part, prêt à réviser."""
    if not can_edit(request):
        return _deny(request)
    retour = redirect(reverse("wiki:quiz_index") + "#importer-vocabulaire")
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
    if not erreur:
        try:
            fiches, ignorees = paquets.analyser_liste(texte, ordre)
        except paquets.PaquetInvalide as e:
            erreur = str(e)
        else:
            if not fiches:
                erreur = "Aucune ligne « mot – traduction » reconnue : une ligne par mot, séparés par une tabulation, une virgule ou « = »."
    if erreur:
        messages.error(request, erreur)
        return retour
    titre = options["titre"] or f"Vocabulaire {options['langue'].lower()} du {timezone.localdate():%d/%m/%Y}"
    paquet = paquets.paquet_vocabulaire(options["langue"], titre, "", options["types"], fiches, "Import de liste")
    try:
        rel = paquets.ecrire_paquet_langue(options["dossier"] or claude.DOSSIER_VOCABULAIRE, paquet)
    except paquets.PaquetInvalide as e:
        messages.error(request, str(e))
        return retour
    n = len(paquet["vocabulaire"])
    messages.success(request, f"Paquet « {titre} » créé : {n} mot{'s' if n > 1 else ''}"
                     + (f", {ignorees} ligne{'s' if ignorees > 1 else ''} ignorée{'s' if ignorees > 1 else ''}" if ignorees else "") + ".")
    from urllib.parse import urlencode

    return redirect(reverse("wiki:langue_menu", args=[options["langue"]]) + "?" + urlencode({"fichier": rel.removesuffix(".json")}))


@require_POST
def generer(request):
    """QCM (d'après une page du wiki ou un texte collé) ou paquet de vocabulaire
    (d'après des mots collés), générés par Claude en arrière-plan."""
    from . import langues

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

        qset = quiz.get_library().get(request.POST.get("set", ""))
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


def palette(request):
    """Données de la palette de commandes (Ctrl+K) : pages, PDF, QCM, langues et commandes."""
    from urllib.parse import quote

    from . import quiz

    vault = get_vault()
    library = quiz.get_library()
    pages = [{"t": n.title, "s": str(n.path.parent) if n.path.parent.parts else "", "u": reverse("wiki:page", args=[n.key])}
             for n in vault.notes.values()]
    pages += [{"t": a.path.stem, "s": "PDF" + (f" · {a.path.parent}" if a.path.parent.parts else ""), "u": a.view_url}
              for a in vault.attachments.values() if a.suffix == ".pdf"]
    pages.sort(key=lambda x: x["t"].lower())
    jouer = reverse("wiki:quiz_play")
    qcm = [{"t": s.titre, "s": s.categorie, "u": f"{jouer}?set={quote(s.id)}&mode=all"} for s in library.sorted_sets()]
    langues = []
    for nom in library.noms_langues():
        base = reverse("wiki:langue_play", args=[nom])
        langues += [{"t": f"Session du jour · {nom}", "u": f"{base}?mode=quotidien"},
                    {"t": f"Révision intensive · {nom}", "u": f"{base}?mode=intensif"},
                    {"t": f"Modes et statistiques · {nom}", "u": reverse("wiki:langue_menu", args=[nom])}]
    commandes = [
        {"t": "Accueil", "u": reverse("wiki:home")},
        {"t": "Sommaire", "u": reverse("wiki:sommaire")},
        {"t": "Tags", "u": reverse("wiki:tags")},
        {"t": "QCM", "u": reverse("wiki:quiz_index")},
        {"t": "Révision intelligente (QCM)", "u": f"{jouer}?revision=1"},
        {"t": "Statistiques des QCM", "u": reverse("wiki:quiz_stats")},
        {"t": "Planning des révisions", "u": reverse("wiki:quiz_plan")},
        {"t": "Rechercher dans le wiki", "u": reverse("wiki:search")},
        {"t": "Documentation", "u": reverse("wiki:documentation")},
        {"t": "Mon compte", "u": reverse("accounts:profile")},
        {"t": "Thème : clair, sombre ou automatique", "a": "theme"},
        {"t": "Plein écran", "a": "fullscreen"},
    ]
    if can_edit(request):
        commandes += [
            {"t": "Modifier cette page", "a": "edit"},
            {"t": "Nouvelle page", "u": reverse("wiki:new")},
            {"t": "Importer des fichiers (.md, PDF)", "u": reverse("wiki:import")},
            {"t": "Travaux de Claude", "u": reverse("wiki:transformations")},
            {"t": "Réglages de Claude", "u": reverse("wiki:claude_reglages")},
            {"t": "Utilisateurs", "u": reverse("accounts:users")},
        ]
    response = JsonResponse({"pages": pages, "qcm": qcm, "langues": langues, "commandes": commandes})
    response["Cache-Control"] = "private, max-age=60"
    return response


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
    from .quiz_views import _render_html

    try:
        data = json.loads(request.body)
        set_id, question_id = str(data["set_id"]), str(data["question_id"])
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)
    qset = quiz.get_library().get(set_id)
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
        texte, usage, modele_id = claude.expliquer(qset, question)
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
    qset = quiz.get_library().get(set_id)
    question = next((q for q in qset.questions if q.id == question_id), None) if qset else None
    if question is None or not question.est_qrc or not reponse:
        return JsonResponse({"error": "question inconnue"}, status=404)
    if not claude.disponible():
        return JsonResponse({"error": "Pas de clé d'API Claude sur le serveur."}, status=503)
    if claude.plafond_atteint():
        return JsonResponse({"error": "Plafond mensuel de Claude atteint : correction stricte."}, status=429)
    try:
        verdict, retour, usage, modele_id = claude.corriger_qrc(qset, question, reponse)
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
        resultat, usage = claude.ameliorer(texte)
    except claude.Echec as e:
        return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"texte": resultat, "jetons": list(usage)})


# Pièces jointes affichées dans la page ; tout le reste (HTML, SVG, JS...) est
# téléchargé, pour qu'un fichier déposé dans le coffre ne puisse pas exécuter
# de script au nom du site.
INLINE_TYPES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".avif", ".pdf",
    ".mp3", ".wav", ".ogg", ".m4a", ".flac", ".webm", ".3gp", ".mp4", ".ogv", ".mov", ".mkv",
}


@xframe_options_sameorigin  # lecteur intégré dans les notes (iframe du même site)
def pdf(request, path):
    """Lecteur de PDF (PDF.js) : page complète, ou version compacte avec
    ``?integre=1`` pour les ``![[cours.pdf]]`` des notes."""
    vault = get_vault()
    attachment = vault.attachments.get(path.lower())
    if attachment is None or attachment.suffix != ".pdf":
        raise Http404("PDF introuvable")
    full = vault.root / attachment.path
    context = {
        "attachment": attachment,
        "title": attachment.path.stem,
        "size": full.stat().st_size if full.is_file() else 0,
    }
    if request.GET.get("integre") == "1":
        return render(request, "wiki/pdf_integre.html", context)
    backlinks = sorted(vault.attachment_backlinks.get(str(attachment.path).lower(), ()), key=lambda n: n.title.lower())
    page_cours = vault.notes.get(str(attachment.path.with_suffix("")).lower())
    return _render(request, vault, "wiki/pdf.html", {
        **context, "backlinks": backlinks, "page_cours": page_cours, "claude_dispo": claude.disponible(),
        "pages_wiki": sorted((n.key for n in vault.notes.values()), key=str.lower) if can_edit(request) else [],
    })


@xframe_options_sameorigin  # PDF intégrés dans les notes (iframe du même site)
def file(request, path):
    vault = get_vault()
    attachment = vault.attachments.get(path.lower())
    if attachment is None:
        raise Http404("Fichier introuvable")
    full = (vault.root / attachment.path).resolve()
    # Lien symbolique pointant hors du coffre : refusé.
    if not full.is_relative_to(vault.root.resolve()):
        raise Http404("Fichier introuvable")
    inline = attachment.suffix in INLINE_TYPES
    response = FileResponse(open(full, "rb"), as_attachment=not inline, filename=attachment.name)
    if attachment.suffix == ".pdf":
        # Le lecteur PDF des navigateurs ne s'affiche pas sous « sandbox » ; il
        # tourne de toute façon isolé du site.
        response._csp_config = {}
    else:
        # Même ouvert directement, le fichier ne peut rien exécuter.
        response.headers["Content-Security-Policy"] = "default-src 'none'; img-src 'self'; media-src 'self'; sandbox"
    return response


def sommaire(request):
    vault = get_vault()
    return _render(request, vault, "wiki/sommaire.html", {
        "root": vault.tree,
        "total": len(vault.notes),
        "recent": vault.recent_notes(8),
    })


def tags(request):
    vault = get_vault()
    return _render(request, vault, "wiki/tags.html", {"tags": vault.all_tags()})


def tag(request, tag):
    vault = get_vault()
    notes = vault.notes_with_tag(tag)
    if not notes:
        raise Http404("Tag inconnu")
    return _render(request, vault, "wiki/tag.html", {"tag": tag, "notes": notes})


def search(request):
    vault = get_vault()
    query = request.GET.get("q", "").strip()
    results = vault.search(query) if query else []
    if len(results) == 1 and results[0][0].title.lower() == query.lower():
        return redirect(results[0][0].url)
    return _render(request, vault, "wiki/search.html", {"query": query, "results": results})


# Documentation du projet : les README à la racine du dépôt (hors du coffre),
# affichés avec le moteur du wiki. Clé d'URL → (fichier, titre de l'onglet).
DOCS = {
    "": ("README.md", "Le wiki"),
    "ia": ("README-IA.md", "Guide IA (pages et QCM)"),
}
# Lien Markdown, ou bloc/segment de code (laissé tel quel) : un lien dont le
# libellé est du code (« [`vault/`](vault/) ») commence avant lui et l'emporte.
LIEN_MD_RE = re.compile(r"(?<!!)\[(?P<label>[^\]\n]*)\]\((?P<cible>[^)\s]+)\)|" + CODE_RE.pattern, CODE_RE.flags)


def _adapter_liens(text):
    """Les liens relatifs des README visent des fichiers du dépôt : on les
    redirige vers le wiki quand c'est possible, sinon on garde le texte seul."""
    docs = {fichier: cle for cle, (fichier, _) in DOCS.items()}

    def lien(m):
        if m.group("label") is None:
            return m.group(0)
        label, cible = m.group("label"), m.group("cible")
        if cible.startswith(("http://", "https://", "mailto:", "/", "#")):
            return m.group(0)
        if cible in docs:
            return f"[{label}](/documentation/{docs[cible] + '/' if docs[cible] else ''})"
        if cible.startswith("vault/"):
            reste = cible.removeprefix("vault/")
            if reste.endswith(".md"):
                return f"[{label}](/wiki/{reste.removesuffix('.md')})"
            if not reste:
                return f"[{label}](/sommaire/)"
        return label

    return LIEN_MD_RE.sub(lien, text)


def documentation(request, doc=""):
    if doc not in DOCS:
        raise Http404("Documentation inconnue")
    fichier, _ = DOCS[doc]
    chemin = settings.BASE_DIR / fichier
    if not chemin.is_file():
        raise Http404("Documentation introuvable")
    vault = get_vault()
    meta, body = split_frontmatter(chemin.read_text(encoding="utf-8").lstrip("\ufeff"))
    note = Note(PurePosixPath(fichier), chemin.stat().st_mtime, meta, _adapter_liens(body))
    content, toc = render_note(vault, note)
    return _render(request, vault, "wiki/documentation.html", {
        "note": note,
        "content": content,
        "toc": toc,
        "onglets": [(cle, titre, cle == doc) for cle, (_, titre) in DOCS.items()],
    })


# ---------------------------------------------------------------------------
# Historique des pages
# ---------------------------------------------------------------------------
def historique_page(request, path):
    """Versions précédentes d'une page (admins) : différences avec la page actuelle, restauration."""
    if not can_edit(request):
        return _deny(request)
    vault = get_vault()
    note = vault.notes.get(path.lower().removesuffix(".md"))
    if note is None:
        raise Http404("Page introuvable")
    rel = note.path.as_posix()
    fichier = vault.root / note.path
    versions = historique.lister(rel)
    if request.method == "POST" and request.POST.get("action") == "restaurer":
        contenu = historique.lire(rel, request.POST.get("v", ""))
        if contenu is None:
            raise Http404("Version introuvable")
        actuel = fichier.read_text(encoding="utf-8")
        if actuel != contenu:
            historique.sauvegarder(rel, actuel, request.user.get_username())
            fichier.write_text(contenu, encoding="utf-8", newline="\n")
        messages.success(request, "Version restaurée ; la version précédente reste dans l'historique.")
        return redirect(note.url)
    choisie = next((v for v in versions if v["id"] == request.GET.get("v")), versions[0] if versions else None)
    contenu_version = historique.lire(rel, choisie["id"]) if choisie else ""
    actuel = fichier.read_text(encoding="utf-8") if fichier.is_file() else ""
    return _render(request, vault, "wiki/historique.html", {
        "note": note, "versions": versions, "choisie": choisie, "contenu_version": contenu_version or "",
        "diff": historique.differences(contenu_version or "", actuel) if choisie else [],
        "max_versions": historique.MAX_VERSIONS,
    })


# ---------------------------------------------------------------------------
# Lecture hors ligne du wiki (service worker à la racine, dossiers gardés)
# ---------------------------------------------------------------------------
from django.contrib.auth.decorators import login_not_required  # noqa: E402
from django.utils.csp import CSP  # noqa: E402
from django.views.decorators.csp import csp_override  # noqa: E402


@login_not_required
@csp_override({**settings.SECURE_CSP, "connect-src": [CSP.SELF, settings.CDN]})
def sw_wiki(request):
    """Service worker du wiki entier (sans secret), servi à la racine pour contrôler tout le site."""
    response = render(request, "wiki/sw_wiki.js", content_type="text/javascript; charset=utf-8")
    response["Cache-Control"] = "no-cache"
    return response


@login_not_required
def manifest_wiki(request):
    """Manifeste de l'application installable : le wiki entier (écran d'accueil d'un téléphone, iPhone compris)."""
    import json

    from django.templatetags.static import static

    data = {
        "name": "ProjetPluri", "short_name": "ProjetPluri",
        "description": "Le wiki de révision : cours, PDF, QCM, lisible même sans connexion.",
        "start_url": "/", "scope": "/", "display": "standalone", "background_color": "#ffffff",
        "theme_color": "#7852ee", "lang": "fr",
        "icons": [
            {"src": static("wiki/icone-192.png"), "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": static("wiki/icone-512.png"), "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/manifest+json")


@login_not_required
def hors_connexion(request):
    """Page servie par le service worker quand une page n'est ni accessible ni en cache."""
    return render(request, "wiki/hors_connexion.html")


def dossier_hors_ligne(request):
    """Adresses à mettre en cache pour lire un dossier sans connexion : ses pages, images et PDF."""
    vault = get_vault()
    dossier = request.GET.get("dossier", "").replace("\\", "/").strip("/")
    prefixe = f"{dossier}/" if dossier else ""
    pages = [n.url for n in vault.sorted_notes() if n.path.as_posix().startswith(prefixe)]
    fichiers, pdf = [], 0
    for a in sorted(vault.attachments.values(), key=lambda a: str(a.path).lower()):
        if not a.path.as_posix().startswith(prefixe) or a.suffix not in IMAGE_EXTS | {".pdf"}:
            continue
        fichiers.append(a.url)
        if a.suffix == ".pdf":
            fichiers.append(a.view_url)
            pdf += 1
    if not pages and not fichiers:
        raise Http404("Dossier introuvable ou vide")
    return JsonResponse({"dossier": dossier, "urls": pages + fichiers, "pages": len(pages), "pdf": pdf})


# ---------------------------------------------------------------------------
# Annotations depuis le lecteur PDF : carte de révision ou citation dans une page
# ---------------------------------------------------------------------------
DOSSIER_ANNOTATIONS = "Annotations"
MAX_CHARS_ANNOTATION = 2000


@require_POST
def pdf_annotation(request):
    """Passage sélectionné dans un PDF → carte recto/verso (set « <PDF> — annotations ») ou
    citation ajoutée à une page du wiki (créée au besoin). Admins."""
    import hashlib
    import json
    from urllib.parse import quote

    from . import quiz

    if not can_edit(request):
        return _deny(request)
    try:
        data = json.loads(request.body)
        chemin, cible = str(data["pdf"]), str(data.get("cible", "carte"))
        texte = " ".join(str(data.get("texte", "")).split())[:MAX_CHARS_ANNOTATION]
        page_pdf = int(data.get("page") or 0)
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)
    vault = get_vault()
    pdf = vault.attachments.get(chemin.lower())
    if pdf is None or pdf.suffix != ".pdf":
        return JsonResponse({"error": "PDF introuvable"}, status=404)
    if not texte:
        return JsonResponse({"error": "Sélectionnez d'abord un passage du PDF."}, status=400)
    stem = pdf.path.stem
    source = f"{stem}, p. {page_pdf}" if page_pdf else stem
    page_cours = vault.notes.get(str(pdf.path.with_suffix("")).lower())
    qui = request.user.get_username()

    if cible == "carte":
        rel = f"{paquets.DOSSIER_QCM}/{DOSSIER_ANNOTATIONS}/{stem}.json"
        fichier = vault.root / rel
        if fichier.is_file():
            try:
                set_json = json.loads(fichier.read_text(encoding="utf-8"))
            except ValueError:
                return JsonResponse({"error": f"Le fichier {rel} est illisible."}, status=500)
        else:
            set_json = {"titre": f"{stem} — annotations", "description": f"Passages gardés depuis le PDF {pdf.name}.",
                        "genere_par": "Annotations du lecteur PDF", "questions": []}
            if page_cours is not None:
                set_json["source_page"] = page_cours.key
        recto = str(data.get("recto") or "").strip()[:500] or f"{source} : que dit ce passage ?"
        empreinte = hashlib.sha1(f"{page_pdf}\x1f{texte}".encode("utf-8")).hexdigest()[:10]
        set_json.setdefault("questions", []).append({
            "id": f"a{empreinte}", "type": "FLASHCARD", "question": recto, "verso": f"{texte}\n\n— *{source}*"})
        try:
            quiz.set_depuis_json(set_json, PurePosixPath(rel))
            paquets.enregistrer_json(rel, set_json)
        except (ValueError, paquets.PaquetInvalide) as e:
            return JsonResponse({"error": str(e)}, status=400)
        n = len(set_json["questions"])
        return JsonResponse({"ok": True, "message": f"Carte ajoutée à « {set_json['titre']} » ({n} carte{'s' if n > 1 else ''}).",
                             "url": reverse("wiki:quiz_play") + "?set=" + quote(rel.removesuffix(".json")) + "&mode=all"})

    if cible == "note":
        voulue = str(data.get("page_wiki") or "").strip().removesuffix(".md")
        cle = clean_key(voulue) if voulue else (page_cours.key if page_cours else clean_key(str(pdf.path.with_suffix(""))))
        if cle is None:
            return JsonResponse({"error": "Nom de page invalide."}, status=400)
        note = vault.notes.get(cle.lower())
        fichier = vault.root / (note.path if note is not None else PurePosixPath(f"{cle}.md"))
        citation = f"> [!quote] {source}\n> {texte}\n> — [[{vault.link_for(pdf)}]]\n"
        if fichier.is_file():
            ancien = fichier.read_text(encoding="utf-8")
            historique.sauvegarder(fichier.relative_to(vault.root).as_posix(), ancien, qui)
            nouveau = ancien.rstrip("\n") + "\n\n" + citation
            titre = note.title if note is not None else cle.rsplit("/", 1)[-1]
        else:
            fichier.parent.mkdir(parents=True, exist_ok=True)
            titre = cle.rsplit("/", 1)[-1]
            nouveau = f"# {titre}\n\n{citation}"
        fichier.write_text(nouveau, encoding="utf-8", newline="\n")
        return JsonResponse({"ok": True, "message": f"Citation ajoutée à « {titre} ».", "url": reverse("wiki:page", args=[cle])})
    return JsonResponse({"error": "cible inconnue"}, status=400)


# ---------------------------------------------------------------------------
# Erreurs du serveur (admins)
# ---------------------------------------------------------------------------
def erreurs(request):
    """Dernières erreurs du serveur : regroupées, avec leur trace ; marquer comme réglée, effacer."""
    from .models import ErreurServeur

    if not can_edit(request):
        return _deny(request)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "reglee":
            ErreurServeur.objects.filter(pk=request.POST.get("pk")).update(reglee=True)
        elif action == "tout_regle":
            ErreurServeur.objects.filter(reglee=False).update(reglee=True)
        elif action == "effacer":
            ErreurServeur.objects.filter(reglee=True).delete()
        return redirect("wiki:erreurs")
    liste = list(ErreurServeur.objects.all()[:100])
    return _render(request, get_vault(), "wiki/erreurs.html", {
        "ouvertes": [e for e in liste if not e.reglee], "reglees": [e for e in liste if e.reglee],
    })
