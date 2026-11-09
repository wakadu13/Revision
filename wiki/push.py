"""Notifications web (Web Push) : rappel quotidien sur l'ordinateur, le téléphone et
l'iPhone (wiki installé sur l'écran d'accueil), sans l'application Android.

Les clés VAPID du serveur sont créées au premier usage dans DATA_DIR/vapid_prive.pem
(à garder : les changer oblige chaque appareil à se réabonner). L'envoi se fait par
la commande « envoyer_rappels », lancée régulièrement par cron.
"""

import base64
import json
import logging
import threading
from pathlib import Path

from django.conf import settings

log = logging.getLogger(__name__)
_verrou = threading.Lock()


def _chemin_cle():
    return Path(settings.DATA_DIR) / "vapid_prive.pem"


def _vapid():
    from py_vapid import Vapid02

    chemin = _chemin_cle()
    with _verrou:
        if not chemin.is_file():
            v = Vapid02()
            v.generate_keys()
            chemin.parent.mkdir(parents=True, exist_ok=True)
            v.save_key(str(chemin))
        return Vapid02.from_file(str(chemin))


def cle_publique():
    """Clé publique (base64url, point non compressé) pour PushManager.subscribe()."""
    from cryptography.hazmat.primitives import serialization

    brut = _vapid().public_key.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    return base64.urlsafe_b64encode(brut).rstrip(b"=").decode("ascii")


def contact():
    """« sub » des jetons VAPID : WIKI_PUSH_CONTACT, sinon l'adresse publique du wiki."""
    import os

    valeur = os.environ.get("WIKI_PUSH_CONTACT", "").strip()
    if valeur:
        return valeur
    for hote in settings.ALLOWED_HOSTS:
        if "." in hote and any(c.isalpha() for c in hote) and not hote.startswith("."):
            return f"https://{hote}"
    return "mailto:admin@example.org"


class AbonnementExpire(Exception):
    """Le service de notifications ne connaît plus cet appareil (abonnement à supprimer)."""


def envoyer(abonnement, titre, texte, url="/aujourdhui/"):
    """Envoie une notification à un appareil ; AbonnementExpire si l'abonnement est mort."""
    from pywebpush import WebPushException, webpush

    try:
        webpush(
            subscription_info={"endpoint": abonnement.endpoint, "keys": {"p256dh": abonnement.p256dh, "auth": abonnement.auth}},
            data=json.dumps({"titre": titre, "texte": texte, "url": url}, ensure_ascii=False),
            vapid_private_key=str(_chemin_cle()) if _chemin_cle().is_file() else _vapid(),
            vapid_claims={"sub": contact()},
            ttl=12 * 3600,
            timeout=15,
        )
    except WebPushException as e:
        statut = getattr(getattr(e, "response", None), "status_code", None)
        if statut in (404, 410):
            raise AbonnementExpire(str(e)) from None
        raise
