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

    def record(self, reponse, quand=None, retention=None) -> None:
        """Enregistre une réponse : note (quiz.NOTES) ou booléen juste/faux. Met à jour
        les statistiques, la boîte de Leitner (indicateur hérité) et l'état FSRS, qui fixe
        la prochaine échéance.

        `quand` : date de la réponse si elle n'est pas immédiate (réponses faites hors
        ligne puis synchronisées) ; `retention` : probabilité de rappel visée (90 % par
        défaut, plus haute à l'approche d'un examen)."""
        now = quand or timezone.now()
        note = quiz.note_de(reponse)
        correcte = note != quiz.A_REVOIR
        note_fsrs = quiz.NOTES.index(note) + 1
        deja_appris = self.stabilite is not None or self.seen > 0
        etat = self._etat_suivant(note_fsrs, now)  # avant de changer last_review
        self.seen += 1
        if correcte:
            self.correct += 1
        self.box = quiz.nouvelle_boite(self.box, reponse)
        self.last_correct = correcte
        self.last_review = now
        if self.premiere_revue is None:
            self.premiere_revue = now
        self.stabilite = round(etat.stabilite, 3)
        self.difficulte = round(etat.difficulte, 3)
        self.echeance = now + langues.delai(etat, note_fsrs, retention)
        if self.decouverte is None and not deja_appris:
            self.decouverte = now
        if deja_appris and not correcte:
            self.oublis += 1

    def _etat_suivant(self, note: int, now):
        if self.stabilite is not None and self.difficulte is not None:
            return langues.etat_suivant(self, note, now)
        if self.seen > 0:
            # Progression antérieure à FSRS (boîtes de Leitner) : stabilité estimée d'après la boîte.
            depuis = langues._jours_depuis(self, now)
            return fsrs.suivante(fsrs.Etat(quiz.STABILITE_LEITNER.get(self.box, 30.0), 5.0), depuis, note)
        return fsrs.premiere(note)

    def record_langue(self, note: int, quand=None) -> None:
        """Enregistre une révision du module Langues (note FSRS 1 à 4) ; même suivi que
        les QCM. `quand` : date de la réponse si elle a été faite hors ligne."""
        self.record(quiz.NOTES[note - 1], quand)

    def is_due(self, now=None) -> bool:
        now = now or timezone.now()
        if self.echeance is not None:
            return self.echeance <= now
        return quiz.intervalle_ecoule(self.box, self.last_review, now)

    def urgence(self, now=None) -> float:
        """0 (oublié) à 1 (bien su) : rétention FSRS, ou boîte de Leitner pour une progression ancienne."""
        if self.stabilite is not None:
            return langues.retention(self, now or timezone.now())
        return self.box / quiz.BOITE_MAX

    def priority(self, now=None):
        """Clé de tri : à réviser d'abord, puis les plus menacées d'oubli, puis plus ancien."""
        return (0 if self.is_due(now) else 1, self.urgence(now), self.last_review or _JAMAIS)

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
    auto_quota = models.BooleanField(default=False)                    # nouvelles/jour ajustées pour être prêt à temps
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

    ATTENTE, EN_COURS, LOT, BROUILLON, FAIT, ERREUR = "attente", "en_cours", "lot", "brouillon", "fait", "erreur"
    STATUTS = [(ATTENTE, "En attente"), (EN_COURS, "En cours"), (LOT, "Dans un lot"), (BROUILLON, "À relire"),
               (FAIT, "Terminée"), (ERREUR, "Échec")]
    PAGE, QCM, VOCABULAIRE, FICHE = "page", "qcm", "vocabulaire", "fiche"
    GENRES = [(PAGE, "Page de cours"), (QCM, "QCM"), (VOCABULAIRE, "Vocabulaire"), (FICHE, "Fiche de révision")]

    genre = models.CharField(max_length=12, choices=GENRES, default=PAGE)
    # QCM : nombre de questions, catégorie, titre, publier (sans relecture) ;
    # vocabulaire : langue, types de cartes, dossier, titre, publier ;
    # tous : lot (traitement différé à moitié prix), fichier_api (PDF envoyé).
    options = models.JSONField(default=dict, blank=True)
    # Traitement différé : identifiant du lot (Message Batches) qui porte la requête.
    lot_id = models.CharField(max_length=64, blank=True)
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
    # Plafond mensuel (en dollars) des usages « à la demande » : corrections de
    # réponses rédigées, explications et tuteur. Les transformations demandées
    # par un admin ne sont pas plafonnées.
    plafond_mensuel = models.FloatField(default=5.0)
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


class Signalement(models.Model):
    """Question de QCM signalée par un joueur (erreur, ambiguïté, coquille). L'admin la
    corrige à la main, la retire, ou applique la correction proposée par Claude."""

    set_id = models.CharField(max_length=500)
    question_id = models.CharField(max_length=255)
    player = models.CharField(max_length=150, blank=True, default="")
    commentaire = models.TextField(blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)
    traite_le = models.DateTimeField(null=True, blank=True)
    proposition = models.JSONField(null=True, blank=True)  # question corrigée proposée par Claude
    proposition_note = models.TextField(blank=True)        # ce que Claude a changé, et pourquoi

    class Meta:
        ordering = ["traite", "-cree_le"]

    def __str__(self):
        return f"{self.set_id} » {self.question_id}"


class UsageClaude(models.Model):
    """Appels à Claude hors transformations (correction d'une réponse rédigée, tuteur) :
    jetons consommés, pour le coût du mois et le plafond."""

    QRC, TUTEUR, WIKI = "qrc", "tuteur", "wiki"
    genre = models.CharField(max_length=12)
    player = models.CharField(max_length=150, blank=True, default="")
    modele = models.CharField(max_length=64, blank=True)
    jetons_entree = models.PositiveIntegerField(default=0)
    jetons_sortie = models.PositiveIntegerField(default=0)
    cree_le = models.DateTimeField(auto_now_add=True)


class EchangeTuteur(models.Model):
    """Question posée au tuteur sur une page du cours, et la réponse de Claude : l'historique
    de l'utilisateur sur la page nourrit la conversation suivante."""

    player = models.CharField(max_length=150, blank=True, default="")
    page = models.CharField(max_length=500)  # clé de la note (PAGE_WIKI : « Demander au wiki »)
    question = models.TextField()
    reponse = models.TextField()
    sources = models.JSONField(default=list, blank=True)  # « Demander au wiki » : extraits cités [{titre, url, type}]
    modele = models.CharField(max_length=64, blank=True)
    jetons_entree = models.PositiveIntegerField(default=0)
    jetons_sortie = models.PositiveIntegerField(default=0)
    cree_le = models.DateTimeField(auto_now_add=True)

    PAGE_WIKI = "*"  # questions posées à tout le wiki

    class Meta:
        ordering = ["cree_le", "pk"]


class ErreurServeur(models.Model):
    """Erreur du serveur (page en erreur 500, fil de Claude), regroupée par empreinte."""

    empreinte = models.CharField(max_length=40, unique=True)
    type = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    lieu = models.CharField(max_length=500, blank=True)      # fichier:ligne du code
    chemin = models.CharField(max_length=500, blank=True)    # adresse demandée (dernière occurrence)
    methode = models.CharField(max_length=10, blank=True)
    utilisateur = models.CharField(max_length=150, blank=True)
    trace = models.TextField(blank=True)
    nombre = models.PositiveIntegerField(default=1)
    premiere = models.DateTimeField()
    derniere = models.DateTimeField()
    reglee = models.BooleanField(default=False)

    class Meta:
        ordering = ["reglee", "-derniere"]

    def __str__(self):
        return f"{self.type}: {self.message[:60]}"


class TempsRevision(models.Model):
    """Temps passé à réviser, par joueur, jour et matière (catégorie de QCM, ou langue)."""

    player = models.CharField(max_length=150)
    jour = models.DateField()
    matiere = models.CharField(max_length=200)
    temps_ms = models.PositiveBigIntegerField(default=0)
    reponses = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("player", "jour", "matiere")

    DUREE_MAX_MS = 120_000  # au-delà, le joueur s'est sans doute absenté

    @classmethod
    def noter(cls, player, matiere, duree, quand=None):
        """Ajoute une durée de réponse (ms) ; ignore une durée absente ou invalide."""
        from django.db.models import F

        if not matiere or not isinstance(duree, (int, float)) or isinstance(duree, bool) or duree <= 0:
            return
        jour = timezone.localdate(quand or timezone.now())
        obj, _ = cls.objects.get_or_create(player=player, jour=jour, matiere=str(matiere)[:200])
        cls.objects.filter(pk=obj.pk).update(temps_ms=F("temps_ms") + int(min(duree, cls.DUREE_MAX_MS)),
                                             reponses=F("reponses") + 1)

    @classmethod
    def minutes_du_jour(cls, player, jour):
        from django.db.models import Sum

        total = cls.objects.filter(player=player, jour=jour).aggregate(t=Sum("temps_ms"))["t"] or 0
        return round(total / 60000)

    @classmethod
    def tableau(cls, player, aujourdhui=None, semaines=8):
        """Minutes par matière et par semaine (lundi), les `semaines` dernières :
        (semaines [lundis], lignes [{matiere, minutes: [..], total}], totaux [..])."""
        from datetime import timedelta

        aujourdhui = aujourdhui or timezone.localdate()
        lundi = aujourdhui - timedelta(days=aujourdhui.weekday())
        lundis = [lundi - timedelta(weeks=k) for k in range(semaines - 1, -1, -1)]
        par_matiere = {}
        for t in cls.objects.filter(player=player, jour__gte=lundis[0]):
            k = (t.jour - lundis[0]).days // 7
            par_matiere.setdefault(t.matiere, [0] * semaines)[k] += t.temps_ms
        lignes = [{"matiere": m, "minutes": [round(ms / 60000) for ms in v], "total": round(sum(v) / 60000)}
                  for m, v in par_matiere.items()]
        lignes.sort(key=lambda l: (-l["total"], l["matiere"].lower()))
        totaux = [sum(l["minutes"][k] for l in lignes) for k in range(semaines)]
        return lundis, lignes, totaux


class ObjectifRevision(models.Model):
    """Objectif quotidien d'un joueur : nombre de réponses par jour (page « Aujourd'hui »)."""

    player = models.CharField(max_length=150, unique=True)
    reponses_jour = models.PositiveIntegerField(null=True, blank=True)


class AbonnementPush(models.Model):
    """Notifications web (navigateur, application installée) : un abonnement par appareil."""

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="abonnements_push")
    endpoint = models.URLField(max_length=1000, unique=True)
    p256dh = models.CharField(max_length=200)
    auth = models.CharField(max_length=100)
    heure = models.PositiveSmallIntegerField(default=19)
    minute = models.PositiveSmallIntegerField(default=0)
    agent = models.CharField(max_length=300, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    dernier_envoi = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} · {self.heure:02d}:{self.minute:02d}"


class TextePdf(models.Model):
    """Texte d'un PDF du coffre, page par page, pour la recherche (wiki/texte_pdf.py)."""

    chemin = models.CharField(max_length=500, unique=True)
    signature = models.CharField(max_length=64)  # date de modification et taille du fichier lu
    pages = models.JSONField(default=list)
    erreur = models.CharField(max_length=300, blank=True)
    indexe_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.chemin
