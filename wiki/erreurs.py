"""Erreurs du serveur (500 et fil de Claude) gardées pour les admins : page /erreurs/.

Les erreurs identiques (même type, même message, même endroit du code) sont
regroupées et comptées. Rien ici ne doit lui-même lever d'exception : une base de
données indisponible ne doit pas cacher l'erreur d'origine.
"""

import hashlib
import logging
import sys
import traceback

from django.utils import timezone

log = logging.getLogger(__name__)
MAX_ERREURS = 200
MAX_TRACE = 20_000


def noter(contexte="", request=None, exc_info=None):
    """Enregistre l'exception en cours (ou `exc_info`)."""
    try:
        from .models import ErreurServeur

        type_, valeur, tb = exc_info or sys.exc_info()
        if type_ is None:
            return
        lieu = _lieu(traceback.extract_tb(tb))
        message = str(valeur)[:2000]
        empreinte = hashlib.sha1(f"{type_.__name__}\x1f{message}\x1f{lieu}".encode()).hexdigest()
        trace = "".join(traceback.format_exception(type_, valeur, tb))[-MAX_TRACE:]
        chemin = (request.get_full_path()[:500] if request is not None else contexte[:500])
        methode = request.method if request is not None else ""
        user = getattr(request, "user", None) if request is not None else None
        qui = user.get_username() if user is not None and user.is_authenticated else ""
        maintenant = timezone.now()
        e = ErreurServeur.objects.filter(empreinte=empreinte).first()
        if e is None:
            ErreurServeur.objects.create(empreinte=empreinte, type=type_.__name__, message=message, lieu=lieu,
                                         chemin=chemin, methode=methode, utilisateur=qui, trace=trace,
                                         premiere=maintenant, derniere=maintenant)
            anciennes = ErreurServeur.objects.order_by("-derniere").values_list("pk", flat=True)[MAX_ERREURS:]
            ErreurServeur.objects.filter(pk__in=list(anciennes)).delete()
        else:
            ErreurServeur.objects.filter(pk=e.pk).update(
                nombre=e.nombre + 1, derniere=maintenant, chemin=chemin, methode=methode, utilisateur=qui,
                trace=trace, reglee=False)
    except Exception:  # noqa: BLE001
        log.exception("Erreur impossible à enregistrer")


def _lieu(pile):
    """Endroit du code du wiki où l'erreur est née : la dernière ligne qui est dans le
    projet (pas dans Python ni dans une bibliothèque), en chemin relatif."""
    from pathlib import Path

    from django.conf import settings

    base = Path(settings.BASE_DIR).resolve()
    for cadre in reversed(pile):
        chemin = Path(cadre.filename).resolve()
        if chemin.is_relative_to(base) and ".venv" not in chemin.parts and "site-packages" not in chemin.parts:
            return f"{chemin.relative_to(base).as_posix()}:{cadre.lineno}"
    return f"{pile[-1].filename}:{pile[-1].lineno}" if pile else ""


def au_signal(sender, request=None, **kwargs):
    """Récepteur de django.core.signals.got_request_exception."""
    noter(request=request)
