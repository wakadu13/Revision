"""PDF et pièces jointes du coffre : lecteur de PDF, fichiers servis, passages gardés
depuis le lecteur (carte de révision ou citation dans une page)."""

from pathlib import PurePosixPath

from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_POST

from . import claude, historique, paquets
from .vault import clean_key, get_vault
from .vues_communes import _deny, _render, can_edit


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


# Pièces jointes affichées dans la page ; tout le reste (HTML, SVG, JS...) est
# téléchargé, pour qu'un fichier déposé dans le coffre ne puisse pas exécuter
# de script au nom du site.
INLINE_TYPES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".avif", ".pdf",
    ".mp3", ".wav", ".ogg", ".m4a", ".flac", ".webm", ".3gp", ".mp4", ".ogv", ".mov", ".mkv",
}


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
