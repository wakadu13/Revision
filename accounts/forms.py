from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .roles import ADMIN, USER


class LoginForm(AuthenticationForm):
    remember = forms.BooleanField(label="Rester connecté", required=False)


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")


class AdminCreateUserForm(RegisterForm):
    """Création d'un compte par un admin (le site n'a pas d'inscription libre)."""
    role = forms.ChoiceField(label="Rôle", choices=[(USER, "Utilisateur"), (ADMIN, "Admin")], initial=USER)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data["role"] == ADMIN
        if commit:
            user.save()
        return user
