from django.utils.functional import SimpleLazyObject

from .vault import get_vault


def wiki(request):
    """Coffre et arborescence pour la barre latérale des pages hors wiki (comptes...).

    Paresseux : le coffre n'est lu que si le gabarit s'en sert (pas dans /admin/).
    """
    return {
        "vault": SimpleLazyObject(get_vault),
        "tree": SimpleLazyObject(lambda: get_vault().tree),
        # Application Android (WebView) : navigation tactile en bas de l'écran.
        "in_app": "ProjetPluriApp/" in request.headers.get("User-Agent", ""),
    }
