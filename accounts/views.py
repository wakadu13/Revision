from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_not_required, login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import AdminCreateUserForm, LoginForm, RegisterForm
from .models import JetonAppareil
from .roles import admin_required


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        # Sans « Rester connecté », la session expire à la fermeture du navigateur.
        if not form.cleaned_data.get("remember"):
            self.request.session.set_expiry(0)
        return response


class LogoutView(auth_views.LogoutView):
    pass


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        # Comme les autres sessions, les applications Android doivent se reconnecter.
        JetonAppareil.objects.filter(user=self.request.user).delete()
        messages.success(self.request, "Mot de passe modifié.")
        return super().form_valid(form)


@login_not_required
def register(request):
    if not settings.ACCOUNTS_REGISTRATION_OPEN:
        messages.error(request, "Les inscriptions sont fermées : demandez un compte à un admin.")
        return redirect("accounts:login")
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()  # rôle « utilisateur » par défaut (is_staff = False)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, f"Bienvenue {user.get_username()} !")
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html", {"appareils": request.user.jetons.all()})


@require_POST
@login_required
def revoquer_appareil(request, pk):
    """Déconnecte une application Android (son jeton ne marche plus)."""
    get_object_or_404(JetonAppareil, pk=pk, user=request.user).delete()
    messages.success(request, "Appareil déconnecté.")
    return redirect("accounts:profile")


@admin_required
def users(request):
    form = AdminCreateUserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, f"Compte « {user.get_username()} » créé.")
        return redirect("accounts:users")
    return render(request, "accounts/users.html", {
        "users": get_user_model().objects.order_by("-is_staff", "username"),
        "form": form,
    })


@require_POST
@admin_required
def user_action(request, pk):
    """Promouvoir / rétrograder / activer / désactiver un compte."""
    user = get_object_or_404(get_user_model(), pk=pk)
    action = request.POST.get("action")
    if user == request.user:
        messages.error(request, "Vous ne pouvez pas modifier votre propre compte ici.")
    elif user.is_superuser and not request.user.is_superuser:
        messages.error(request, "Seul un superutilisateur peut modifier un superutilisateur.")
    elif action in {"promote", "demote", "activate", "deactivate"}:
        if action in {"promote", "demote"}:
            user.is_staff = action == "promote"
        else:
            user.is_active = action == "activate"
        user.save(update_fields=["is_staff", "is_active"])
        if action == "deactivate":
            _end_sessions(user)
        messages.success(request, f"Compte « {user.get_username()} » mis à jour.")
    return redirect("accounts:users")


def _end_sessions(user):
    """Déconnecte immédiatement un compte désactivé (supprime ses sessions)."""
    from django.contrib.sessions.models import Session
    from django.utils import timezone
    for session in Session.objects.filter(expire_date__gt=timezone.now()):
        if session.get_decoded().get("_auth_user_id") == str(user.pk):
            session.delete()
