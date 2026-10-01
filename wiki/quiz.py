"""QCM de révision : chargement des sets de questions et logique de Leitner.

Porté depuis l'application « revision_qcm » (https://github.com/wakadu13/revision_qcm).
Les sets sont des fichiers JSON déposés dans le coffre (même format que l'appli
d'origine). Un fichier JSON est considéré comme un set s'il contient une liste
« questions ». La catégorie est le nom du dossier qui contient le fichier.

Ce module reste « pur » (aucun import de Django ni du rendu) : la persistance de
la progression est gérée par le modèle QuizProgress, et le rendu LaTeX/Markdown
des énoncés est fait dans les vues.
"""

from __future__ import annotations

import json
import threading
import unicodedata
from dataclasses import dataclass, field
from datetime import timedelta
from functools import cached_property
from pathlib import Path, PurePosixPath

from django.conf import settings

# --- Révision espacée (système de Leitner) ---
# Intervalle (en jours) avant qu'une question d'une boîte donnée soit « à réviser ».
INTERVALLES_JOURS = {0: 0, 1: 1, 2: 3, 3: 7, 4: 14, 5: 30}
BOITE_MAX = 5
TYPES_VALIDES = {"QCM", "QCR", "TROU", "QRC", "FLASHCARD"}
TYPES_TEXTE = {"TROU", "QRC"}  # réponse tapée au clavier, comparée à reponses_texte
CATEGORIE_DEFAUT = "Général"


def normaliser_texte(s: str) -> str:
    """Normalise une réponse libre : casse, accents et espaces superflus ignorés."""
    s = unicodedata.normalize("NFKD", str(s).strip().casefold())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.split())


def normaliser_reponse(s: str) -> str:
    """Comme normaliser_texte, en ignorant aussi les apostrophes typographiques et
    la ponctuation finale (. ! ? ; :) — utile pour les réponses tapées (TROU, QRC)."""
    s = normaliser_texte(str(s).replace("\u2019", "'").replace("\u2018", "'"))
    return s.rstrip(".!?;: ")


def intervalle_ecoule(boite: int, last_review, now) -> bool:
    """Vrai si l'intervalle de Leitner est écoulé (ou si jamais révisée)."""
    if last_review is None:
        return True
    jours = INTERVALLES_JOURS.get(boite, INTERVALLES_JOURS[BOITE_MAX])
    return now >= last_review + timedelta(days=jours)


def nouvelle_boite(boite: int, correcte: bool) -> int:
    """Bonne réponse → monte d'une boîte ; mauvaise → redescend d'une boîte."""
    return min(BOITE_MAX, boite + 1) if correcte else max(0, boite - 1)


# ---------------------------------------------------------------------------
# Modèles de données
# ---------------------------------------------------------------------------
@dataclass
class Question:
    id: str
    type: str
    enonce: str
    choix: list[str] = field(default_factory=list)
    reponses: list[int] = field(default_factory=list)        # indices 0-based, QCM/QCR
    reponses_texte: list[str] = field(default_factory=list)  # réponses acceptées, TROU/QRC
    consigne: str = ""                                       # ex. « Traduire en anglais », QRC
    verso: str = ""                                          # dos de carte, FLASHCARD
    explication: str = ""

    @property
    def est_qcr(self) -> bool:
        return self.type == "QCR"

    @property
    def est_trou(self) -> bool:
        return self.type == "TROU"

    @property
    def est_qrc(self) -> bool:
        return self.type == "QRC"

    @property
    def est_flashcard(self) -> bool:
        return self.type == "FLASHCARD"

    def est_correcte(self, selection) -> bool:
        return set(selection) == set(self.reponses)

    def est_correcte_texte(self, reponse: str) -> bool:
        cible = normaliser_reponse(reponse)
        return any(cible == normaliser_reponse(r) for r in self.reponses_texte)


@dataclass
class QuestionSet:
    id: str            # identifiant stable = chemin relatif sans extension
    titre: str
    description: str
    questions: list[Question]
    categorie: str = CATEGORIE_DEFAUT
    path: PurePosixPath | None = None

    def __len__(self) -> int:
        return len(self.questions)

    @cached_property
    def texte_recherche(self) -> str:
        """Titre, description, catégorie et énoncés, normalisés pour la recherche."""
        parts = [self.titre, self.description, self.categorie]
        parts += [q.enonce for q in self.questions]
        return normaliser_texte(" ".join(parts))

    def correspond(self, requete: str) -> bool:
        """Vrai si tous les mots de la requête figurent dans le set (accents ignorés)."""
        return all(mot in self.texte_recherche for mot in normaliser_texte(requete).split())


# ---------------------------------------------------------------------------
# Chargement et validation
# ---------------------------------------------------------------------------
def charger_set(chemin, racine) -> QuestionSet:
    """Charge et valide un set depuis un fichier JSON. Lève ValueError si malformé."""
    chemin = Path(chemin)
    rel = PurePosixPath(chemin.relative_to(racine).as_posix())
    categorie = rel.parent.name or CATEGORIE_DEFAUT

    try:
        data = json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON invalide dans {rel} : {e}")
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        raise ValueError(f"{rel} : clé 'questions' (liste) manquante.")

    questions: list[Question] = []
    for i, q in enumerate(data["questions"], start=1):
        contexte = f"{rel} » question #{i}"
        if not isinstance(q, dict) or "question" not in q:
            raise ValueError(f"{contexte} : clé 'question' manquante.")
        type_q = str(q.get("type", "QCM")).upper()
        if type_q not in TYPES_VALIDES:
            raise ValueError(f"{contexte} : type '{type_q}' inconnu (QCM, QCR, TROU, QRC, FLASHCARD).")

        choix, reponses, reponses_texte, verso, consigne = [], [], [], "", ""
        if type_q in ("QCM", "QCR"):
            for clef in ("choix", "reponses"):
                if clef not in q:
                    raise ValueError(f"{contexte} : clé '{clef}' manquante.")
            choix = [str(c) for c in q["choix"]]
            reponses = list(q["reponses"])
            if not choix:
                raise ValueError(f"{contexte} : la liste 'choix' est vide.")
            if not reponses:
                raise ValueError(f"{contexte} : aucune bonne réponse fournie.")
            for r in reponses:
                if not isinstance(r, int) or not (0 <= r < len(choix)):
                    raise ValueError(f"{contexte} : indice de réponse {r} hors limites.")
            if type_q == "QCM" and len(reponses) != 1:
                raise ValueError(f"{contexte} : un QCM doit avoir exactement 1 réponse.")
        elif type_q in TYPES_TEXTE:
            reponses_texte = [str(r) for r in q.get("reponses_texte", []) if str(r).strip()]
            if not reponses_texte:
                raise ValueError(f"{contexte} : 'reponses_texte' doit contenir une réponse.")
            consigne = str(q.get("consigne", "")) if type_q == "QRC" else ""
        elif type_q == "FLASHCARD":
            verso = str(q.get("verso", ""))
            if not verso.strip():
                raise ValueError(f"{contexte} : clé 'verso' manquante (dos de la carte).")

        question = Question(
            id=str(q.get("id", f"q{i}")),
            type=type_q,
            enonce=str(q["question"]),
            choix=choix,
            reponses=reponses,
            reponses_texte=reponses_texte,
            consigne=consigne,
            verso=verso,
            explication=str(q.get("explication", "")),
        )
        questions.append(question)
        # QRC « inverse » : on pose aussi la question dans l'autre sens
        # (ex. chien → dog, puis dog → chien), suivie séparément dans Leitner.
        if type_q == "QRC" and q.get("inverse"):
            questions.append(Question(
                id=f"{question.id}~inverse",
                type="QRC",
                enonce=reponses_texte[0],
                reponses_texte=[question.enonce],
                consigne=str(q.get("consigne_inverse", "")),
                explication=question.explication,
            ))
    if not questions:
        raise ValueError(f"{rel} : aucune question.")

    return QuestionSet(
        id=rel.with_suffix("").as_posix(),
        titre=str(data.get("titre") or rel.stem),
        description=str(data.get("description", "")),
        questions=questions,
        categorie=categorie,
        path=rel,
    )


class Library:
    """Ensemble des sets de questions trouvés dans le coffre."""

    def __init__(self, root, files):
        self.root = Path(root)
        self.sets: dict[str, QuestionSet] = {}
        self.errors: list[str] = []
        for rel, _mtime, _size in files:
            if not rel.lower().endswith(".json"):
                continue
            try:
                qset = charger_set(self.root / rel, self.root)
            except ValueError as e:
                # On distingue « pas un set » (JSON sans 'questions', ex. .canvas)
                # d'un vrai set malformé, qu'on signale.
                if "questions' (liste) manquante" not in str(e):
                    self.errors.append(str(e))
                continue
            self.sets[qset.id] = qset

    def get(self, set_id):
        return self.sets.get(set_id)

    def sorted_sets(self):
        return sorted(self.sets.values(), key=lambda s: (s.categorie.lower(), s.titre.lower()))

    def categories(self):
        """{catégorie: [sets]} trié, pour l'affichage groupé."""
        cats: dict[str, list[QuestionSet]] = {}
        for qset in self.sorted_sets():
            cats.setdefault(qset.categorie, []).append(qset)
        return cats

    def all_questions(self):
        """Toutes les paires (set, question) de la bibliothèque."""
        return [(qset, q) for qset in self.sorted_sets() for q in qset.questions]


_lock = threading.Lock()
_cache = {"root": None, "signature": None, "library": None}


def get_library():
    """Renvoie la bibliothèque de QCM, réindexée seulement si un fichier a changé."""
    from .vault import scan  # import tardif : évite un cycle à l'import du module

    root = Path(settings.WIKI_DIR)
    signature = tuple(f for f in (scan(root) if root.is_dir() else ())
                      if f[0].lower().endswith(".json"))
    with _lock:
        if _cache["library"] is None or _cache["root"] != root or _cache["signature"] != signature:
            _cache.update(root=root, signature=signature, library=Library(root, signature))
        return _cache["library"]
