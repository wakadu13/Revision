"""Outils communs aux vues du wiki : droits d'édition, refus, réponse JSON ou page."""

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from accounts.roles import is_admin


def can_edit(request):
    """Seuls les admins modifient le wiki."""
    return is_admin(request.user)


def _deny(request):
    """Anonyme → page de connexion ; utilisateur simple → 403."""
    if request.user.is_authenticated:
        raise PermissionDenied
    return redirect_to_login(request.get_full_path())


def _wants_json(request):
    """Requête envoyée par le JavaScript de l'éditeur ou de l'import (réponse JSON)."""
    return "application/json" in request.headers.get("Accept", "")


def _render(request, vault, template, context, status=200):
    context = {"vault": vault, "tree": vault.tree, "can_edit": can_edit(request), **context}
    return render(request, template, context, status=status)
