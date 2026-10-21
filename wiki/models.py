"""Persistance de la progression aux QCM (Leitner) et au module Langues (FSRS).

Remplace le fichier progression.json de l'application d'origine par la base de
données Django. Une ligne = une question (ou une facette d'exercice de langue)
suivie, pour un « joueur » (le nom d'utilisateur connecté ; les QCM demandent
d'être connecté).
"""

from datetime import datetime, timezone as dt_timezone

from django.db import models
from django.utils import timezone

from . import fsrs, langues, quiz

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
    premiere_revue = models.DateTimeField(null=True, blank=True)  # 1re réponse : compte les nouvelles du jour
    last_correct = models.BooleanField(null=True, blank=True)
    # Module Langues uniquement (vides pour les QCM) : état FSRS de la facette.
    stabilite = models.FloatField(null=True, blank=True)     # jours avant 90 % de rappel
    difficulte = models.FloatField(null=True, blank=True)    # 1 à 10
    echeance = models.DateTimeField(null=True, blank=True)   # prochaine révision
    decouverte = models.DateTimeField(null=True, blank=True)  # 1re révision : quota de nouveautés
    oublis = models.PositiveIntegerField(default=0)           # échecs après avoir été appris

    class Meta:
        unique_together = ("player", "set_id", "question_id")
        indexes = [models.Index(fields=["player", "set_id"])]

    def record(self, reponse, quand=None) -> None:
        """Enregistre une réponse : note (quiz.NOTES) ou booléen juste/faux.

        `quand` : date de la réponse si elle n'est pas immédiate (réponses faites
        hors ligne puis synchronisées) ; maintenant par défaut."""
        correcte = quiz.note_de(reponse) != quiz.A_REVOIR
        self.seen += 1
        if correcte:
            self.correct += 1
        self.box = quiz.nouvelle_boite(self.box, reponse)
        self.last_correct = correcte
        self.last_review = quand or timezone.now()
        if self.premiere_revue is None:
            self.premiere_revue = self.last_review

    def record_langue(self, note: int) -> None:
        """Enregistre une révision du module Langues (note FSRS 1 à 4) : statistiques,
        boîte de Leitner et état FSRS."""
        now = timezone.now()
        deja_appris = not langues.est_nouveau(self)
        etat = langues.etat_suivant(self, note, now)  # avant record(), qui change last_review
        self.record(quiz.NOTES[note - 1])
        self.last_review = now
        self.stabilite = round(etat.stabilite, 3)
        self.difficulte = round(etat.difficulte, 3)
        self.echeance = now + langues.delai(etat, note)
        if self.decouverte is None and not deja_appris:
            self.decouverte = now
        if deja_appris and note == fsrs.A_REVOIR:
            self.oublis += 1

    def is_due(self, now=None) -> bool:
        return quiz.intervalle_ecoule(self.box, self.last_review, now or timezone.now())

    def priority(self, now=None):
        """Clé de tri : à réviser d'abord, puis boîtes basses, puis plus ancien."""
        return (0 if self.is_due(now) else 1, self.box, self.last_review or _JAMAIS)

    @classmethod
    def map_for(cls, player: str, set_id: str) -> dict:
        """{question_id: QuizProgress} pour un set et un joueur donnés."""
        return {p.question_id: p for p in cls.objects.filter(player=player, set_id=set_id)}

    @classmethod
    def map_langue(cls, player: str, sets) -> dict:
        """{(set_id, exercice_id): QuizProgress} pour des fichiers de langue."""
        rows = cls.objects.filter(player=player, set_id__in=[s.id for s in sets])
        return {(p.set_id, p.question_id): p for p in rows}


class QuizDeck(models.Model):
    """Réglages d'un set pour un joueur (quotas journaliers, date d'examen) et temps
    de réponse mesuré, qui sert à estimer la durée des révisions."""

    player = models.CharField(max_length=150, blank=True, default="")
    set_id = models.CharField(max_length=500)
    nouvelles_jour = models.PositiveIntegerField(null=True, blank=True)  # questions jamais vues, max par jour
    revisions_jour = models.PositiveIntegerField(null=True, blank=True)  # questions déjà vues, max par jour
    date_objectif = models.DateField(null=True, blank=True)            # date d'examen
    temps_ms = models.PositiveBigIntegerField(default=0)               # cumul des temps de réponse
    reponses_chronometrees = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("player", "set_id")

    @property
    def configure(self) -> bool:
        return bool(self.nouvelles_jour or self.revisions_jour or self.date_objectif)

    def secondes_par_carte(self, defaut, minimum):
        """(secondes moyennes par réponse, mesurée ?) ; `defaut` s'il y a moins de `minimum` mesures."""
        if self.reponses_chronometrees < minimum:
            return defaut, False
        return self.temps_ms / self.reponses_chronometrees / 1000, True

    @classmethod
    def map_for(cls, player: str) -> dict:
        """{set_id: QuizDeck} pour un joueur."""
        return {d.set_id: d for d in cls.objects.filter(player=player)}

    @classmethod
    def pour(cls, decks: dict, player: str, set_id: str):
        """Réglages du set, ou réglages vides (non enregistrés) s'il n'en a pas."""
        return decks.get(set_id) or cls(player=player, set_id=set_id)
