"""Pages du wiki : lecture d'une note, édition et aperçu, nouvelle page, import de fichiers,
sommaire, tags, recherche, palette de commandes, documentation, historique des versions
et erreurs du serveur. Voir aussi claude_views (Claude), pdf_views (PDF et pièces jointes),
pwa_views (lecture hors ligne) et vues_communes (droits, rendu)."""

import re
from pathlib import PurePosixPath

from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import claude, historique, uploads
from . import latex as latex_converter
from .claude_views import _cartes_de_la_page, _transformer_cours, _tuteur_de_la_page
from .models import QuizProgress, Transformation
from .render import Renderer, render_note
from .vault import CODE_RE, Note, clean_key, get_vault, split_frontmatter
from .vues_communes import _deny, _render, _wants_json, can_edit


def _qcm_de_la_page(request, note):
    """Sets de QCM écrits d'après cette page (source_page), avec la progression du joueur."""
    from . import quiz
    from .models import QuizDeck
    from .quiz_views import _ancre, _set_summary, player_id

    cle = note.key.lower()
    sets = [s for s in quiz.get_library().pour(player_id(request)).sets.values() if s.source_page.lower() == cle]
    if not sets:
        return []
    player, now, decks = player_id(request), timezone.now(), QuizDeck.map_for(player_id(request))
    return [{"set": s, "ancre": _ancre(s.id),
             "summary": _set_summary(s, QuizProgress.map_for(player, s.id), now, decks.get(s.id))}
            for s in sorted(sets, key=lambda s: s.titre.lower())]


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


def palette(request):
    """Données de la palette de commandes (Ctrl+K) : pages, PDF, QCM, langues et commandes."""
    from urllib.parse import quote

    from . import quiz

    vault = get_vault()
    from .quiz_views import player_id

    library = quiz.get_library().pour(player_id(request))
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
        {"t": "Aujourd'hui", "u": reverse("wiki:aujourdhui")},
        {"t": "Mon espace (QCM personnels)", "u": reverse("wiki:quiz_perso")},
        {"t": "Cartes à image masquée (schéma)", "u": reverse("wiki:quiz_masque")},
        {"t": "QCM", "u": reverse("wiki:quiz_index")},
        {"t": "Révision intelligente (QCM)", "u": f"{jouer}?revision=1"},
        {"t": "Statistiques des QCM", "u": reverse("wiki:quiz_stats")},
        {"t": "Planning des révisions", "u": reverse("wiki:quiz_plan")},
        {"t": "Rechercher dans le wiki", "u": reverse("wiki:search")},
        {"t": "Demander au wiki (Claude)", "u": reverse("wiki:demander")},
        {"t": "Corriger ma copie (photo, Claude)", "u": reverse("wiki:copie")},
        {"t": "Graphe des liens entre pages", "u": reverse("wiki:graphe")},
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
    """Recherche dans les notes et dans le texte des PDF (page par page)."""
    from . import texte_pdf

    vault = get_vault()
    query = request.GET.get("q", "").strip()
    results = vault.search(query) if query else []
    pdfs = texte_pdf.chercher(vault, query) if query else []
    if len(results) == 1 and not pdfs and results[0][0].title.lower() == query.lower():
        return redirect(results[0][0].url)
    restants = len(texte_pdf.a_indexer(vault))
    if restants:
        texte_pdf.lancer()
    return _render(request, vault, "wiki/search.html", {
        "query": query, "results": results, "pdfs": pdfs, "pdf_restants": restants, "demander_dispo": claude.disponible()})


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
