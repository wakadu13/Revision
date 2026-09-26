"""Persistance de la progression aux QCM (système de Leitner).

Remplace le fichier progression.json de l'application d'origine par la base de
données Django. Une ligne = une question suivie, pour un « joueur » (le nom
d'utilisateur connecté, ou une chaîne vide si les modifications sont ouvertes).
"""

from datetime import datetime, timezone as dt_timezone

from django.db import models
from django.utils import timezone

from . import quiz

# Date « aware » très ancienne, pour trier les questions jamais révisées en premier.
_JAMAIS = datetime.min.replace(tzinfo=dt_timezone.utc)


class QuizProgress(models.Model):
    player = models.CharField(max_length=150, blank=True, default="")
    set_id = models.CharField(max_length=500)
    question_id = models.CharField(max_length=255)
    box = models.PositiveSmallIntegerField(default=0)      # boîte de Leitner (0–5)
    seen = models.PositiveIntegerField(default=0)          # nombre de passages
    correct = models.PositiveIntegerField(default=0)       # réponses correctes
    last_review = models.DateTimeField(null=True, blank=True)
    last_correct = models.BooleanField(null=True, blank=True)

    class Meta:
        unique_together = ("player", "set_id", "question_id")
        indexes = [models.Index(fields=["player", "set_id"])]

    def record(self, correcte: bool) -> None:
        self.seen += 1
        if correcte:
            self.correct += 1
        self.box = quiz.nouvelle_boite(self.box, correcte)
        self.last_correct = correcte
        self.last_review = timezone.now()

    def is_due(self, now=None) -> bool:
        return quiz.intervalle_ecoule(self.box, self.last_review, now or timezone.now())

    def priority(self, now=None):
        """Clé de tri : à réviser d'abord, puis boîtes basses, puis plus ancien."""
        return (0 if self.is_due(now) else 1, self.box, self.last_review or _JAMAIS)

    @classmethod
    def map_for(cls, player: str, set_id: str) -> dict:
        """{question_id: QuizProgress} pour un set et un joueur donnés."""
        return {p.question_id: p for p in cls.objects.filter(player=player, set_id=set_id)}
