"""Import de fichiers dans le coffre depuis le navigateur.

- Notes ``.md`` (ou ``.markdown``) : chacune devient une page, en gardant les
  sous-dossiers quand on dépose un dossier entier (un coffre Obsidian, par ex.).
- Pièces jointes intégrables dans les notes : images, PDF, audio, vidéo.

Tout le reste est refusé (HTML, scripts, JSON de QCM...). On n'écrit jamais
hors du coffre, ni dans ses dossiers cachés (``.obsidian``, ``.trash``).
"""

from dataclasses import asdict, dataclass
from pathlib import PurePosixPath

from django.urls import reverse

from .render import AUDIO_EXTS, IMAGE_EXTS, VIDEO_EXTS
from .vault import IGNORED_DIRS, INVALID_NAME_RE

NOTE_EXTS = {".md", ".markdown"}
ATTACHMENT_EXTS = IMAGE_EXTS | AUDIO_EXTS | VIDEO_EXTS | {".pdf"}
MAX_NOTE_SIZE = 5 * 1024 * 1024
MAX_ATTACHMENT_SIZE = 100 * 1024 * 1024  # PDF scannés compris
FORBIDDEN_CHARS = '/ \\ : * ? " < > | # ^ [ ]'


@dataclass
class Result:
    name: str  # chemin du fichier tel qu'envoyé
    ok: bool
    message: str
    ignored: bool = False
    path: str = ""  # chemin final dans le coffre
    url: str = ""
    link: str = ""  # texte à mettre entre [[ ]]
    is_note: bool = False

    def as_dict(self):
        return asdict(self)


def _parts(raw):
    return [p.strip() for p in str(raw).replace("\\", "/").split("/") if p.strip()]


def _hidden(part):
    return part.startswith(".") or part in IGNORED_DIRS


def clean_folder(raw):
    """Dossier de destination saisi (``""`` = racine du coffre), ou None s'il est invalide."""
    parts = _parts(raw)
    if any(_hidden(p) or INVALID_NAME_RE.search(p) for p in parts):
        return None
    return "/".join(parts)


def _free_path(root, vault, path, is_note):
    """« image.png » déjà pris → « image 1.png », « image 2.png »..."""
    for i in range(1, 10_000):
        candidate = path.with_name(f"{path.stem} {i}{path.suffix}")
        key = str(candidate.with_suffix("")).lower() if is_note else str(candidate).lower()
        taken = vault.notes if is_note else vault.attachments
        if key not in taken and not (root / candidate).exists():
            return candidate
    raise ValueError("aucun nom libre")


def import_file(vault, upload, relative, folder="", replace=False, rename=False):
    """Écrit un fichier envoyé dans ``folder/relative``. Renvoie un :class:`Result`.

    Un fichier qui existe déjà est refusé, sauf avec ``replace`` (écrasé) ou
    ``rename`` (enregistré sous un nom libre, comme Obsidian pour les images collées).
    """
    root = vault.root
    parts = _parts(relative or upload.name)
    shown = "/".join(parts) or str(upload.name)
    if not parts:
        return Result(shown, False, "nom de fichier vide")
    if any(_hidden(p) for p in parts):
        return Result(shown, False, "ignoré : fichier ou dossier caché (.obsidian, .trash…)", ignored=True)
    if any(INVALID_NAME_RE.search(p) for p in parts):
        return Result(shown, False, f"nom invalide : caractères interdits {FORBIDDEN_CHARS}")

    suffix = PurePosixPath(parts[-1]).suffix.lower()
    if suffix in NOTE_EXTS:
        is_note, limit = True, MAX_NOTE_SIZE
        parts[-1] = PurePosixPath(parts[-1]).stem + ".md"
    elif suffix in ATTACHMENT_EXTS:
        is_note, limit = False, MAX_ATTACHMENT_SIZE
    else:
        return Result(shown, False, "type de fichier non accepté (notes .md, images, PDF, audio ou vidéo)")
    if upload.size > limit:
        return Result(shown, False, f"trop volumineux (maximum {limit // 1024 // 1024} Mo)")

    if is_note:
        try:
            text = upload.read().decode("utf-8-sig")
        except UnicodeDecodeError:
            return Result(shown, False, "ce n'est pas un fichier texte UTF-8")
        text = text.replace("\r\n", "\n")

    path = PurePosixPath(*_parts(folder), *parts)
    existing = (
        vault.notes.get(str(path.with_suffix("")).lower()) if is_note else vault.attachments.get(str(path).lower())
    )
    message = "importé"
    if existing is not None or (root / path).exists():
        if rename:
            path = _free_path(root, vault, path, is_note)
            message = f"importé sous le nom « {path.name} »"
        elif replace:
            # Même fichier à une casse près : on écrase celui-là plutôt que d'en créer un second.
            path = existing.path if existing is not None else path
            message = "remplacé"
        else:
            return Result(shown, False, "existe déjà (cochez « Remplacer » pour l'écraser)")

    target = root / path
    if not target.resolve().is_relative_to(root.resolve()):
        return Result(shown, False, "chemin invalide")
    if target.is_dir():
        return Result(shown, False, "un dossier porte déjà ce nom")
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        if is_note:
            target.write_text(text, encoding="utf-8", newline="\n")
        else:
            with open(target, "wb") as out:
                for chunk in upload.chunks():
                    out.write(chunk)
    except OSError:
        # Ex. : un fichier porte le nom d'un des dossiers du chemin.
        return Result(shown, False, "écriture impossible à cet emplacement")
    return Result(shown, True, message, path=path.as_posix(), is_note=is_note)


def finish(vault, results):
    """Complète les fichiers importés avec leur adresse et le texte du lien,
    une fois le coffre relu (``vault`` doit les contenir)."""
    for result in results:
        if not result.ok:
            continue
        if result.is_note:
            item = vault.notes.get(result.path.removesuffix(".md").lower())
            if item is not None:
                result.url = reverse("wiki:page", args=[item.key])
        else:
            item = vault.attachments.get(result.path.lower())
            if item is not None:
                result.url = item.view_url
        if item is not None:
            result.link = vault.link_for(item)
    return results
