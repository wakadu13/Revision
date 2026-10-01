"""Rôles des comptes.

Deux rôles, portés par le champ ``is_staff`` du modèle User de Django :

- **admin** (``is_staff``) : modifie le wiki, gère les comptes, accède à /admin/ ;
- **utilisateur** : lit le wiki et fait les QCM avec sa propre progression.

Les visiteurs non connectés peuvent seulement lire le wiki.
"""

from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

ADMIN = "admin"
USER = "utilisateur"


def is_admin(user):
    return user.is_authenticated and user.is_active and user.is_staff


def role_of(user):
    return ADMIN if user.is_staff else USER


def admin_required(view):
    """Réservé aux admins : connexion demandée si anonyme, 403 sinon."""
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not is_admin(request.user):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper
