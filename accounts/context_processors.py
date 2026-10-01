from django.conf import settings

from .roles import is_admin, role_of


def roles(request):
    user = getattr(request, "user", None)
    admin = user is not None and is_admin(user)
    return {
        "is_admin": admin,
        "can_edit": admin,
        "user_role": role_of(user) if user is not None and user.is_authenticated else None,
        "registration_open": settings.ACCOUNTS_REGISTRATION_OPEN,
    }
