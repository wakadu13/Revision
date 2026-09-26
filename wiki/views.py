from pathlib import PurePosixPath

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .render import Renderer
from .vault import Note, clean_key, get_vault, split_frontmatter


def can_edit(request):
    return request.user.is_authenticated or not settings.WIKI_EDIT_LOGIN_REQUIRED


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
        return redirect_to_login(request.get_full_path())
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
        else:
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(content, encoding="utf-8", newline="\n")
            return redirect("wiki:page", key)
    else:
        content = file.read_text(encoding="utf-8").lstrip("﻿") if file.is_file() else ""

    return _render(request, vault, "wiki/edit.html", {
        "note": note,
        "key": key,
        "is_new": note is None,
        "content": content,
        "version": version,
        "error": error,
        "link_choices": vault.link_choices(),
        "preview_url": reverse("wiki:preview", args=[key]),
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
        return redirect_to_login(request.get_full_path())
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


def file(request, path):
    vault = get_vault()
    attachment = vault.attachments.get(path.lower())
    if attachment is None:
        raise Http404("Fichier introuvable")
    return FileResponse(open(vault.root / attachment.path, "rb"))


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
