"""Authentification des applications installées par jeton (en-tête Authorization).

L'APK Android n'a pas de session : chaque requête porte
« Authorization: Bearer <jeton> ». Le jeton n'ouvre que l'API des QCM hors
ligne et les pièces jointes (images des questions). Il n'est pas envoyé
automatiquement par un navigateur : pas de CSRF possible, la vérification
CSRF est donc levée pour ces requêtes.
"""

from django.http import JsonResponse
from django.utils import timezone

from .models import JetonAppareil

CHEMINS_AUTORISES = ("/qcm/hors-ligne/catalogue/", "/qcm/hors-ligne/sets/", "/qcm/hors-ligne/synchro/",
                     "/fichiers/", "/api/appareil/deconnexion/")
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
        return self.get_response(request)
