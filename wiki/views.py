import re
from pathlib import PurePosixPath

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_POST

from accounts.roles import is_admin

from . import uploads
from .render import Renderer, render_note
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


def _note_page(request, vault, note):
    content, toc = vault.render(note)
    backlinks = sorted(vault.backlinks.get(note.key.lower(), ()), key=lambda n: n.title.lower())
    return _render(request, vault, "wiki/page.html", {
        "note": note,
        "content": content,
        "toc": toc,
        "backlinks": backlinks,
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
        "preview_url": reverse("wiki:preview", args=[key]),
        "import_url": reverse("wiki:import"),
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
        uploads.import_file(vault, upload, paths[i] if i < len(paths) else "", folder, replace=replace, rename=rename)
        for i, upload in enumerate(files)
    ]
    results = uploads.finish(get_vault(), results)
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
    if len(done) == 1 and done[0].url and (done[0].is_note or done[0].path.lower().endswith(".pdf")):
        return redirect(done[0].url)
    return redirect("wiki:import")


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
    return _render(request, vault, "wiki/pdf.html", {**context, "backlinks": backlinks})


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
