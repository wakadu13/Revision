from django.urls import path

from . import api, views

app_name = "accounts"

urlpatterns = [
    path("connexion/", views.LoginView.as_view(), name="login"),
    path("deconnexion/", views.LogoutView.as_view(), name="logout"),
    path("inscription/", views.register, name="register"),
    path("compte/", views.profile, name="profile"),
    path("compte/appareils/<int:pk>/revoquer/", views.revoquer_appareil, name="revoquer_appareil"),
    path("compte/mot-de-passe/", views.PasswordChangeView.as_view(), name="password_change"),
    path("utilisateurs/", views.users, name="users"),
    path("utilisateurs/<int:pk>/", views.user_action, name="user_action"),
    path("api/appareil/connexion/", api.connexion, name="appareil_connexion"),
    path("api/appareil/deconnexion/", api.deconnexion, name="appareil_deconnexion"),
    path("api/appareil/session/", api.session, name="appareil_session"),
]
