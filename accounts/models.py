import hashlib
import secrets

from django.conf import settings
from django.db import models


def _empreinte(cle):
    return hashlib.sha256(cle.encode()).hexdigest()


class JetonAppareil(models.Model):
    """Jeton d'une application installée (APK Android) : remplace la session.

    Seule l'empreinte SHA-256 est gardée en base ; le jeton en clair n'est
    connu que du téléphone. Il est révoqué à la déconnexion de l'application,
    depuis /compte/, ou quand le compte est désactivé.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jetons")
    nom = models.CharField(max_length=100, blank=True)
    empreinte = models.CharField(max_length=64, unique=True)
    cree = models.DateTimeField(auto_now_add=True)
    utilise = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "jeton d'appareil"
        verbose_name_plural = "jetons d'appareil"
        ordering = ["-cree"]

    def __str__(self):
        return f"{self.user} · {self.nom or 'appareil'}"

    @classmethod
    def creer(cls, user, nom=""):
        """Crée un jeton ; renvoie (objet, jeton en clair)."""
        cle = secrets.token_urlsafe(32)
        return cls.objects.create(user=user, nom=nom[:100], empreinte=_empreinte(cle)), cle

    @classmethod
    def trouver(cls, cle):
        return cls.objects.select_related("user").filter(empreinte=_empreinte(cle)).first()
