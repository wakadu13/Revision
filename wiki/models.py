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


class Transformation(models.Model):
    """Travail confié à Claude, fait en arrière-plan (claude.py) : un cours (PDF ou
    LaTeX) transformé en page, un QCM ou un paquet de vocabulaire généré."""

    ATTENTE, EN_COURS, BROUILLON, FAIT, ERREUR = "attente", "en_cours", "brouillon", "fait", "erreur"
    STATUTS = [(ATTENTE, "En attente"), (EN_COURS, "En cours"), (BROUILLON, "À relire"), (FAIT, "Terminée"), (ERREUR, "Échec")]
    PAGE, QCM, VOCABULAIRE, FICHE = "page", "qcm", "vocabulaire", "fiche"
    GENRES = [(PAGE, "Page de cours"), (QCM, "QCM"), (VOCABULAIRE, "Vocabulaire"), (FICHE, "Fiche de révision")]

    genre = models.CharField(max_length=12, choices=GENRES, default=PAGE)
    # QCM : nombre de questions, catégorie, titre, publier (sans relecture) ;
    # vocabulaire : langue, types de cartes, dossier, titre, publier.
    options = models.JSONField(default=dict, blank=True)
    # QCM ou paquet généré, en attente de relecture (statut « brouillon ») : le
    # JSON du fichier à écrire, et le dossier.
    resultat = models.JSONField(null=True, blank=True)

    # PDF : son chemin dans le coffre. LaTeX : le nom du fichier envoyé, et son
    # texte (le coffre ne garde que la page convertie sur place).
    source = models.CharField(max_length=500)
    texte_source = models.TextField(blank=True)
    # Page à écrire (chemin .md dans le coffre). Si elle existe déjà (page
    # convertie à l'import), elle n'est remplacée que si personne ne l'a
    # modifiée entre-temps (même empreinte) ; sinon la page part à côté.
    page = models.CharField(max_length=500)
    empreinte_page = models.CharField(max_length=64, blank=True)
    page_ecrite = models.CharField(max_length=500, blank=True)
    statut = models.CharField(max_length=10, choices=STATUTS, default=ATTENTE)
    message = models.TextField(blank=True)
    modele = models.CharField(max_length=64, blank=True)
    jetons_entree = models.PositiveIntegerField(default=0)
    jetons_sortie = models.PositiveIntegerField(default=0)
    demande_par = models.CharField(max_length=150, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    debut = models.DateTimeField(null=True, blank=True)
    fin = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-cree_le", "-pk"]

    def __str__(self):
        return f"{self.source} → {self.page} ({self.statut})"

    @property
    def nom(self):
        if self.genre in (self.QCM, self.FICHE):
            return (self.options or {}).get("nom") or self.source.rsplit("/", 1)[-1].removesuffix(".md")
        return self.source.rsplit("/", 1)[-1]

    @property
    def termine(self):
        return self.statut in (self.BROUILLON, self.FAIT, self.ERREUR)


class ReglagesClaude(models.Model):
    """Clé d'API et modèle de Claude, saisis dans le site par un admin (une seule ligne).

    La clé reste dans la base de données (jamais dans le dépôt) et n'est jamais
    réaffichée en entier.
    """

    cle = models.CharField(max_length=300, blank=True)
    modele = models.CharField(max_length=64, blank=True)
    modifie_le = models.DateTimeField(null=True, blank=True)
    modifie_par = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return "Réglages de Claude"

    @classmethod
    def charger(cls):
        return cls.objects.filter(pk=1).first() or cls(pk=1)

    @property
    def cle_masquee(self):
        return f"{self.cle[:10]}…{self.cle[-4:]}" if len(self.cle) > 16 else "…"


class Activite(models.Model):
    """Réponses d'un joueur par jour (QCM et langues) : série de jours, calendrier."""

    player = models.CharField(max_length=150)
    jour = models.DateField()
    reponses = models.PositiveIntegerField(default=0)
    justes = models.PositiveIntegerField(default=0)
    nouveaux = models.PositiveIntegerField(default=0)  # questions ou mots vus pour la 1re fois

    class Meta:
        unique_together = ("player", "jour")
        ordering = ["jour"]

    # Paliers du calendrier : 0 réponse, puis 1-9, 10-29, 30-59, 60 et plus.
    PALIERS = (1, 10, 30, 60)

    @classmethod
    def noter(cls, player, correct, nouveau=False, quand=None):
        """Compte une réponse (à la date `quand`, maintenant par défaut)."""
        from django.db.models import F

        jour = timezone.localdate(quand or timezone.now())
        obj, _ = cls.objects.get_or_create(player=player, jour=jour)
        cls.objects.filter(pk=obj.pk).update(
            reponses=F("reponses") + 1, justes=F("justes") + (1 if correct else 0), nouveaux=F("nouveaux") + (1 if nouveau else 0))

    @classmethod
    def jours_actifs(cls, player):
        return set(cls.objects.filter(player=player, reponses__gt=0).values_list("jour", flat=True))

    @classmethod
    def serie(cls, player, aujourdhui=None, jours=None):
        """(série en cours, record) : jours consécutifs avec au moins une réponse.
        La série tient encore si la dernière réponse date d'hier."""
        from datetime import timedelta

        aujourdhui = aujourdhui or timezone.localdate()
        jours = cls.jours_actifs(player) if jours is None else jours
        courante = 0
        depart = aujourdhui if aujourdhui in jours else aujourdhui - timedelta(days=1)
        while depart in jours:
            courante += 1
            depart -= timedelta(days=1)
        record = 0
        for j in jours:
            if j - timedelta(days=1) not in jours:
                n, k = 0, j
                while k in jours:
                    n += 1
                    k += timedelta(days=1)
                record = max(record, n)
        return courante, record

    @classmethod
    def calendrier(cls, player, aujourdhui=None, semaines=26):
        """Semaines (lundi → dimanche) des `semaines` dernières semaines, pour le
        calendrier d'activité : [{jour, reponses, justes, niveau}] par semaine."""
        from datetime import timedelta

        aujourdhui = aujourdhui or timezone.localdate()
        fin = aujourdhui + timedelta(days=6 - aujourdhui.weekday())  # dimanche de la semaine
        debut = fin - timedelta(weeks=semaines) + timedelta(days=1)
        par_jour = {a.jour: a for a in cls.objects.filter(player=player, jour__gte=debut, jour__lte=fin)}
        grille = []
        jour = debut
        while jour <= fin:
            semaine = []
            for _ in range(7):
                a = par_jour.get(jour)
                n = a.reponses if a else 0
                semaine.append({"jour": jour, "reponses": n, "justes": a.justes if a else 0,
                                "niveau": sum(n >= p for p in cls.PALIERS), "futur": jour > aujourdhui})
                jour += timedelta(days=1)
            grille.append(semaine)
        return grille

    @classmethod
    def resume(cls, player, aujourdhui=None):
        """Série, record, réponses du jour et des 30 derniers jours, jours actifs sur 30."""
        from datetime import timedelta

        from django.db.models import Sum

        aujourdhui = aujourdhui or timezone.localdate()
        jours = cls.jours_actifs(player)
        courante, record = cls.serie(player, aujourdhui, jours)
        depuis = aujourdhui - timedelta(days=29)
        recents = cls.objects.filter(player=player, jour__gte=depuis)
        totaux = recents.aggregate(reponses=Sum("reponses"), justes=Sum("justes"))
        auj = recents.filter(jour=aujourdhui).first()
        return {
            "serie": courante, "record": record,
            "aujourdhui": auj.reponses if auj else 0,
            "trente_jours": totaux["reponses"] or 0,
            "justes_trente_jours": totaux["justes"] or 0,
            "jours_actifs_trente": sum(1 for j in jours if j >= depuis),
        }


class Explication(models.Model):
    """Explication d'une question de QCM écrite par Claude à la demande (« Explique-moi »),
    gardée pour ne pas payer deux fois."""

    set_id = models.CharField(max_length=500)
    question_id = models.CharField(max_length=255)
    texte = models.TextField()
    modele = models.CharField(max_length=64, blank=True)
    jetons_entree = models.PositiveIntegerField(default=0)
    jetons_sortie = models.PositiveIntegerField(default=0)
    cree_le = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("set_id", "question_id")
