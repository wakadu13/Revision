"""Historique des pages : versions précédentes gardées hors du coffre, différences,
restauration.

À chaque enregistrement qui modifie une page existante (éditeur, import avec
remplacement, page écrite par Claude), le texte **précédent** est copié dans
``DATA_DIR/versions/<chemin de la page>/<horodatage>-<auteur>.md`` ; la page
elle-même reste la version courante. Au plus MAX_VERSIONS versions par page.

Comme quiz.py, ce module ne dépend ni des modèles ni des vues.
"""

import difflib
import re
from datetime import datetime, timezone as dt_timezone
from pathlib import Path, PurePosixPath

from django.conf import settings

MAX_VERSIONS = 50
_NOM_RE = re.compile(r"^(\d{8}T\d{12})-([\w.-]*)\.md$")


def dossier() -> Path:
    return Path(settings.DATA_DIR) / "versions"


def _dossier_page(rel) -> Path:
    rel = PurePosixPath(str(rel).replace("\\", "/"))
    if not rel.parts or any(p in ("..", "") for p in rel.parts):
        raise ValueError("chemin de page invalide")
    cible = (dossier() / rel.as_posix()).resolve()
    if not cible.is_relative_to(dossier().resolve()):
        raise ValueError("chemin de page invalide")
    return cible


def sauvegarder(rel, contenu: str, auteur: str = "") -> str:
    """Garde `contenu` (le texte de la page avant modification) comme version datée.
    Renvoie l'identifiant de la version (nom du fichier)."""
    d = _dossier_page(rel)
    d.mkdir(parents=True, exist_ok=True)
    horodatage = datetime.now(dt_timezone.utc).strftime("%Y%m%dT%H%M%S%f")
    qui = re.sub(r"[^\w.-]", "_", auteur or "")[:40] or "inconnu"
    nom = f"{horodatage}-{qui}.md"
    (d / nom).write_text(contenu, encoding="utf-8", newline="\n")
    for ancienne in sorted(d.glob("*.md"))[:-MAX_VERSIONS]:
        ancienne.unlink()
    return nom


def lister(rel):
    """Versions d'une page, la plus récente d'abord : [{id, date, auteur, taille}]."""
    d = _dossier_page(rel)
    if not d.is_dir():
        return []
    versions = []
    for f in d.glob("*.md"):
        m = _NOM_RE.match(f.name)
        if not m:
            continue
        date = datetime.strptime(m.group(1), "%Y%m%dT%H%M%S%f").replace(tzinfo=dt_timezone.utc)
        versions.append({"id": f.name, "date": date, "auteur": m.group(2).replace("_", " ") if m.group(2) != "inconnu" else "",
                         "taille": f.stat().st_size})
    return sorted(versions, key=lambda v: v["id"], reverse=True)


def lire(rel, id_):
    """Texte d'une version, ou None."""
    if not _NOM_RE.match(str(id_)):
        return None
    f = _dossier_page(rel) / id_
    return f.read_text(encoding="utf-8") if f.is_file() else None


def differences(ancien: str, nouveau: str):
    """Lignes du texte en différences : [{type: 'suppr'|'ajout'|'contexte'|'info', texte}],
    avec 3 lignes de contexte autour de chaque changement."""
    lignes = []
    for l in difflib.unified_diff(ancien.splitlines(), nouveau.splitlines(), "version", "page actuelle", lineterm="", n=3):
        if l.startswith(("---", "+++")):
            continue
        if l.startswith("@@"):
            lignes.append({"type": "info", "texte": l})
        elif l.startswith("+"):
            lignes.append({"type": "ajout", "texte": l[1:]})
        elif l.startswith("-"):
            lignes.append({"type": "suppr", "texte": l[1:]})
        else:
            lignes.append({"type": "contexte", "texte": l[1:]})
    return lignes
