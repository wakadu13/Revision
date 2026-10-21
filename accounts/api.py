"""Connexion de l'application Android : identifiants contre un jeton d'appareil."""

import json

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_not_required
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import JetonAppareil


@login_not_required
@csrf_exempt  # pas de cookie : rien à usurper, l'appelant fournit le mot de passe
@never_cache
@require_POST
def connexion(request):
    """{"username", "password", "appareil"} → {"jeton", "joueur"}.

    Passe par authenticate() : django-axes compte les échecs comme sur le
    formulaire de connexion (blocage après 5 essais).
    """
    try:
        data = json.loads(request.body)
        username, password = str(data["username"]), str(data["password"])
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "requête invalide"}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is None or not user.is_active:
        # Compte bloqué par axes : authenticate() renvoie None et marque la requête.
        if getattr(request, "axes_locked_out", False):
            return JsonResponse({"error": "trop d'essais : compte bloqué 30 minutes"}, status=403)
        return JsonResponse({"error": "identifiant ou mot de passe incorrect"}, status=401)
    _, cle = JetonAppareil.creer(user, str(data.get("appareil", "")))
    return JsonResponse({"jeton": cle, "joueur": user.get_username()})


@never_cache
@require_POST
def deconnexion(request):
    """Révoque le jeton qui porte la requête."""
    jeton = getattr(request, "jeton_appareil", None)
    if jeton is None:
        return JsonResponse({"error": "jeton requis"}, status=400)
    jeton.delete()
    return JsonResponse({"ok": True})
