"""Authentification des applications installées par jeton (en-tête Authorization).

Les requêtes de l'APK Android vers l'API portent « Authorization: Bearer
<jeton> ». Le jeton n'ouvre que l'API des QCM hors ligne, les pièces jointes
(images des questions) et /api/appareil/session/, qui l'échange contre une
session pour afficher le wiki dans l'application ; cette session est fermée dès
que le jeton est révoqué. Le jeton n'est pas envoyé automatiquement par un
navigateur : pas de CSRF possible, la vérification CSRF est donc levée pour ces
requêtes.
"""

from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils import timezone

from .models import JetonAppareil

CHEMINS_AUTORISES = ("/qcm/hors-ligne/catalogue/", "/qcm/hors-ligne/sets/", "/qcm/hors-ligne/synchro/",
                     "/fichiers/", "/api/appareil/deconnexion/", "/api/appareil/session/")
# Clé de session : le jeton dont vient la session ouverte par l'application.
SESSION_JETON = "jeton_appareil"
PREFIXE = "Bearer "


class JetonAppareilMiddleware:
    """À placer après AuthenticationMiddleware (remplace request.user)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        entete = request.headers.get("Authorization", "")
        if entete.startswith(PREFIXE):
            if not request.path.startswith(CHEMINS_AUTORISES):
                return JsonResponse({"error": "jeton refusé sur cette adresse"}, status=403)
            jeton = JetonAppareil.trouver(entete[len(PREFIXE):].strip())
            if jeton is None or not jeton.user.is_active:
                return JsonResponse({"error": "jeton invalide ou révoqué : reconnectez l'application"}, status=401)
            now = timezone.now()
            if jeton.utilise is None or (now - jeton.utilise).total_seconds() > 3600:
                JetonAppareil.objects.filter(pk=jeton.pk).update(utilise=now)
            request.user = jeton.user
            request.jeton_appareil = jeton
            request._dont_enforce_csrf_checks = True
        elif request.user.is_authenticated:
            # Session ouverte par l'application : fermée si son jeton a été révoqué.
            jeton_id = request.session.get(SESSION_JETON)
            if jeton_id is not None and not JetonAppareil.objects.filter(pk=jeton_id, user=request.user).exists():
                logout(request)
        return self.get_response(request)
