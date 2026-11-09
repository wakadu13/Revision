"""Middlewares du wiki."""

from .vault import toujours_verifier

METHODES_SURES = {"GET", "HEAD", "OPTIONS", "TRACE"}


class VerificationCoffreMiddleware:
    """Pendant une requête qui peut écrire (POST…), le coffre est relu à chaque accès,
    et le prochain accès après elle le relira aussi : les fichiers écrits par le wiki
    sont visibles tout de suite malgré la vérification espacée (vault.signature_coffre)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in METHODES_SURES:
            return self.get_response(request)
        with toujours_verifier():
            return self.get_response(request)
