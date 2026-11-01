"""Fichiers statiques : adresse suivie d'une empreinte du contenu (?v=…).

Cloudflare et les navigateurs gardent ces fichiers plusieurs heures : sans
empreinte, après une mise à jour du wiki, la nouvelle page s'afficherait avec
l'ancien CSS ou l'ancien JavaScript. L'adresse change avec le contenu, sans
avoir à lancer collectstatic (WhiteNoise sert les fichiers depuis les applis).
"""

import hashlib
from functools import lru_cache
from pathlib import Path

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import StaticFilesStorage


@lru_cache(maxsize=None)
def _chemin(name):
    return finders.find(name)


@lru_cache(maxsize=None)
def _empreinte(chemin, mtime, taille):
    return hashlib.sha256(Path(chemin).read_bytes()).hexdigest()[:10]


def empreinte(name):
    # Dossier (base d'adresses complétée par le JavaScript, ex. wasm/ de PDF.js) : rien.
    chemin = None if name.endswith("/") else _chemin(name)
    if not chemin or not Path(chemin).is_file():
        return ""
    etat = Path(chemin).stat()
    return _empreinte(chemin, etat.st_mtime_ns, etat.st_size)


class StaticVersionne(StaticFilesStorage):
    def url(self, name):
        url = super().url(name)
        version = empreinte(name)
        return f"{url}?v={version}" if version else url
