"""Module Langues : vocabulaire, conjugaison et grammaire.

Porté depuis l'application « revision_qcm » (src/langues.rs). Il applique les
techniques dont l'efficacité est la mieux établie par la recherche sur la
mémoire et l'acquisition des langues :

- **Répétition espacée optimisée (FSRS)** : chaque élément revient juste avant
  d'être oublié (voir fsrs.py).
- **Rappel actif en production** : on tape la réponse au lieu de la reconnaître.
- **Facettes multiples d'un même mot** : reconnaissance (langue → français),
  puis, une fois le mot découvert, production (français → langue) et rappel en
  contexte (phrase à compléter). Deux facettes d'un même mot ne sont jamais
  posées dans la même session.
- **Conjugaison personne par personne** : chaque forme est suivie séparément,
  le tableau complet est montré à la correction.
- **Grammaire par la pratique** : phrases à trous, remise en ordre de mots,
  correction d'erreurs, en plus des QCM.
- **Entrelacement** : vocabulaire, conjugaison et grammaire sont mélangés au sein
  d'une session.
- **Correction immédiate et réessai** : les différences sont surlignées, puis
  l'exercice revient quelques questions plus tard (géré par le navigateur).
- **Tolérance raisonnable** : en vocabulaire, un accent manquant ou une faute de
  frappe compte comme « presque » (note Difficile) plutôt qu'un échec.

Comme quiz.py, ce module ne dépend ni des modèles ni des vues : la progression
lui est passée sous la forme {(set_id, exercice_id): stats}, où `stats` a les
attributs de QuizProgress (stabilite, difficulte, echeance, decouverte, oublis,
last_review, last_correct).
"""

from __future__ import annotations

import random
import re
from collections import deque
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import PurePosixPath

from django.utils import timezone

from . import fsrs, quiz

VOCABULAIRE, CONJUGAISON, GRAMMAIRE = "vocabulaire", "conjugaison", "grammaire"
GENRES = (VOCABULAIRE, CONJUGAISON, GRAMMAIRE)
NOMS_GENRES = {VOCABULAIRE: "Vocabulaire", CONJUGAISON: "Conjugaison", GRAMMAIRE: "Grammaire"}

# Modes de session : session du jour (tout mélangé), un seul genre, points faibles.
QUOTIDIEN, FAIBLES = "quotidien", "faibles"
MODES = {QUOTIDIEN: "Session du jour", **NOMS_GENRES, FAIBLES: "Points faibles"}

# Quota par défaut de nouveaux éléments par jour : au-delà, la charge de
# révisions des jours suivants devient difficile à tenir.
NOUVEAUX_PAR_JOUR = 20
TAILLE_SESSION = 20
MAITRISE_JOURS = 21   # stabilité à partir de laquelle un élément est « maîtrisé »

# Formes d'exercice.
CARTE, SAISIE, CHOIX, ORDRE = "carte", "saisie", "choix", "ordre"


# ===========================================================================
# Modèle
# ===========================================================================
@dataclass
class Exercice:
    """Une facette d'un élément (mot, forme verbale, point de grammaire).

    `donnees` dépend de `forme` :
      carte  : recto, verso
      saisie : consigne, invite, reponses, tolerant, prerempli, tableau
               (tableau = {titre, lignes: [[personne, forme]], surligne} ou None)
      choix  : enonce, choix, reponses, multiple
      ordre  : consigne, mots, reponses
    """

    id: str                 # clé de suivi (ex. "voc-001#prod")
    entree: str             # élément d'origine : ses facettes sont limitées par session
    genre: str
    etiquette: str          # type d'exercice affiché (ex. « Vocabulaire · production »)
    resume: str             # résumé court (statistiques, points faibles)
    forme: str
    donnees: dict
    details: list[str] = field(default_factory=list)  # montrés après la réponse
    prerequis: str | None = None                      # facette à connaître avant celle-ci
    max_par_session: int = 1


@dataclass
class SetLangue:
    """Un fichier de langue (`"langue": "..."`)."""

    id: str
    langue: str
    titre: str
    description: str
    exercices: list[Exercice]
    particules: list[str] = field(default_factory=list)          # mots facultatifs en tête de réponse
    caracteres_speciaux: list[str] = field(default_factory=list)  # boutons sous le champ de saisie
    nouveaux_par_jour: int | None = None
    path: PurePosixPath | None = None

    def __len__(self):
        return len(self.exercices)

    def exercice(self, exo_id):
        return next((e for e in self.exercices if e.id == exo_id), None)


# ===========================================================================
# Chargement
# ===========================================================================
def est_fichier_langue(data) -> bool:
    """Vrai si le JSON décrit un fichier de langue plutôt qu'un set de questions."""
    return isinstance(data, dict) and "langue" in data and "questions" not in data


def _texte(v) -> str:
    return "" if v is None else str(v)


def _textes(v) -> list[str]:
    """Chaîne ou liste de chaînes → liste (vide si absent)."""
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    return [str(v)] if str(v).strip() else []


def _objet(v, contexte):
    if not isinstance(v, dict):
        raise ValueError(f"{contexte} : un objet JSON est attendu.")
    return v


def _requis(o, clef, contexte):
    if clef not in o:
        raise ValueError(f"{contexte} : clé '{clef}' manquante.")
    s = _texte(o[clef])
    if not s.strip():
        raise ValueError(f"{contexte} : '{clef}' ne doit pas être vide.")
    return s


def _section(data, clef, nom):
    v = data.get(clef)
    if v is None:
        return []
    if not isinstance(v, list):
        raise ValueError(f"{nom} : '{clef}' doit être une liste.")
    return v


def trouer(exemple: str):
    """« She [achieved] her goal. » → (« She _____ her goal. », « achieved »), ou None."""
    m = re.search(r"\[([^\]]*)\]", exemple)
    if not m or not m.group(1).strip():
        return None
    return exemple[:m.start()] + "_____" + exemple[m.end():], m.group(1)


def _sans_crochets(s):
    return s.replace("[", "").replace("]", "")


def abreviation(langue: str) -> str:
    """« Anglais » → « EN », « Français » → « FR » (sinon deux premières lettres)."""
    connues = {
        "anglais": "EN", "english": "EN", "français": "FR", "francais": "FR", "french": "FR",
        "espagnol": "ES", "español": "ES", "spanish": "ES", "allemand": "DE", "deutsch": "DE",
        "german": "DE", "italien": "IT", "italiano": "IT", "italian": "IT", "portugais": "PT",
        "português": "PT",
    }
    l = langue.lower()
    return connues.get(l) or "".join(c for c in l if c.isalpha())[:2].upper()


def mots_a_ordonner(phrase: str) -> list[str]:
    """Mots d'une phrase à remettre en ordre (ponctuation finale retirée, première
    lettre en minuscule pour ne pas donner d'indice, sauf « I »)."""
    mots = phrase.strip().rstrip(".!?…").strip().split()
    if mots and mots[0] != "I" and not mots[0].startswith("I'"):
        premier = mots[0]
        # Première lettre (après une éventuelle ponctuation ouvrante : « ¿Dónde »).
        for i, c in enumerate(premier):
            if c.isalpha():
                mots[0] = premier[:i] + c.lower() + premier[i + 1:]
                break
    return mots


def set_depuis_json(data, rel: PurePosixPath) -> SetLangue:
    """Construit un fichier de langue et ses facettes. Lève ValueError si malformé."""
    nom = rel.name
    langue = _texte(data.get("langue"))
    if not langue.strip():
        raise ValueError(f"{rel} : 'langue' ne doit pas être vide.")
    maternelle = _texte(data.get("langue_maternelle")) or "Français"
    abr_l, abr_m = abreviation(langue), abreviation(maternelle)
    exercices: list[Exercice] = []

    # --- Vocabulaire ---
    for i, v in enumerate(_section(data, "vocabulaire", rel), start=1):
        contexte = f"{rel} » vocabulaire #{i}"
        o = _objet(v, contexte)
        mot = _requis(o, "mot", contexte)
        trads = _textes(o.get("traductions", o.get("traduction")))
        if not trads:
            raise ValueError(f"{contexte} : clé 'traductions' manquante ou vide.")
        id_ = _texte(o["id"]) if "id" in o else f"voc{i}"
        trad = ", ".join(trads)
        exemple = _texte(o.get("exemple"))
        ex_trad = _texte(o.get("exemple_traduction"))
        prononciation = _texte(o.get("prononciation"))
        reponses = [mot] + _textes(o.get("variantes"))

        details = []
        if exemple:
            d = f"Ex. : « {_sans_crochets(exemple)} »"
            if ex_trad:
                d += f" = « {ex_trad} »"
            details.append(d)
        details += [_texte(o[c]) for c in ("note", "explication") if _texte(o.get(c))]

        id_rec = f"{id_}#rec"
        exercices.append(Exercice(
            id=id_rec, entree=id_, genre=VOCABULAIRE,
            etiquette=f"Vocabulaire · reconnaissance ({abr_l} → {abr_m})",
            resume=f"{mot} → {trad}",
            forme=CARTE,
            donnees={"recto": f"{mot}   {prononciation}" if prononciation else mot, "verso": trad},
            details=list(details),
        ))
        exercices.append(Exercice(
            id=f"{id_}#prod", entree=id_, genre=VOCABULAIRE,
            etiquette=f"Vocabulaire · production ({abr_m} → {abr_l})",
            resume=f"{trad} → {mot}",
            forme=SAISIE,
            donnees=_saisie(f"Comment dit-on « {trad} » en {langue.lower()} ?", reponses, tolerant=True),
            details=list(details),
            prerequis=id_rec,
        ))
        troue = trouer(exemple)
        if troue:
            phrase, attendu = troue
            exercices.append(Exercice(
                id=f"{id_}#ctx", entree=id_, genre=VOCABULAIRE,
                etiquette="Vocabulaire · en contexte",
                resume=f"{mot} (en contexte)",
                forme=SAISIE,
                donnees=_saisie(f"Complète : {phrase}\n(indice : {trad})",
                                [a.strip() for a in attendu.split("|")], tolerant=True),
                details=details,
                prerequis=id_rec,
            ))

    # --- Conjugaison ---
    for i, c in enumerate(_section(data, "conjugaison", rel), start=1):
        contexte = f"{rel} » conjugaison #{i}"
        o = _objet(c, contexte)
        verbe = _requis(o, "verbe", contexte)
        temps = _requis(o, "temps", contexte)
        formes = o.get("formes")
        if not isinstance(formes, dict) or not formes:
            raise ValueError(f"{contexte} : clé 'formes' (objet personne → forme) manquante.")
        id_ = _texte(o["id"]) if "id" in o else f"conj{i}"
        traduction = _texte(o.get("traduction"))
        explication = _texte(o.get("explication"))
        lignes = [(str(p), _textes(f)) for p, f in formes.items()]
        for p, f in lignes:
            if not f:
                raise ValueError(f"{contexte} : forme vide pour « {p} ».")
        titre_verbe = f"« {verbe} » ({traduction})" if traduction else f"« {verbe} »"
        tableau_lignes = [[p, f[0]] for p, f in lignes]
        for k, (personne, reponses) in enumerate(lignes):
            exercices.append(Exercice(
                id=f"{id_}#{personne}", entree=id_, genre=CONJUGAISON,
                etiquette=f"Conjugaison · {temps}",
                resume=f"{verbe} ({temps}) — {personne}",
                forme=SAISIE,
                donnees=_saisie(f"Conjugue {titre_verbe} — {temps}", reponses, invite=personne,
                                tableau={"titre": f"{verbe} — {temps}", "lignes": tableau_lignes, "surligne": k}),
                details=[explication] if explication else [],
                max_par_session=2,
            ))

    # --- Grammaire ---
    for i, g in enumerate(_section(data, "grammaire", rel), start=1):
        contexte = f"{rel} » grammaire #{i}"
        o = _objet(g, contexte)
        type_g = _texte(o.get("type", "QCM")).upper()
        id_ = _texte(o["id"]) if "id" in o else f"gram{i}"
        explication = _texte(o.get("explication"))
        traduction = _texte(o.get("traduction"))
        details = []
        if type_g == "ORDRE":
            phrase = _requis(o, "phrase", contexte)
            mots = mots_a_ordonner(phrase)
            if len(mots) < 2:
                raise ValueError(f"{contexte} : la phrase doit contenir au moins 2 mots.")
            consigne = (f"Remets les mots dans l'ordre : « {traduction} »" if traduction
                        else "Remets les mots dans l'ordre.")
            etiquette, resume, forme = "Grammaire · remise en ordre", phrase, ORDRE
            donnees = {"consigne": consigne, "mots": mots, "reponses": [phrase] + _textes(o.get("variantes"))}
        elif type_g == "CORRECTION":
            phrase = _requis(o, "phrase", contexte)
            corrections = _textes(o.get("corrections", o.get("correction")))
            if not corrections:
                raise ValueError(f"{contexte} : clé 'corrections' manquante ou vide.")
            consigne = f"Cette phrase contient une erreur. Corrige-la :\n« {phrase} »"
            if traduction:
                consigne += f"\n(sens : « {traduction} »)"
            etiquette, resume, forme = "Grammaire · correction d'erreur", phrase, SAISIE
            donnees = _saisie(consigne, corrections, prerempli=phrase)
        else:
            q = quiz.question_depuis_json(o, i, contexte)
            if traduction:
                details.append(f"Traduction : « {traduction} »")
            resume = q.enonce
            if q.type in quiz.TYPES_TEXTE:
                etiquette, forme = "Grammaire · phrase à trous", SAISIE
                consigne = f"{q.consigne}\n{q.enonce}" if q.consigne else q.enonce
                donnees = _saisie(consigne, q.reponses_texte)
            elif q.est_flashcard:
                etiquette, forme = "Grammaire · carte", CARTE
                donnees = {"recto": q.enonce, "verso": q.verso}
            else:
                etiquette = "Grammaire · QCR (plusieurs réponses)" if q.est_qcr else "Grammaire · QCM"
                forme = CHOIX
                donnees = {"enonce": q.enonce, "choix": q.choix, "reponses": q.reponses, "multiple": q.est_qcr}
        if explication:
            details.append(explication)
        exercices.append(Exercice(
            id=id_, entree=id_, genre=GRAMMAIRE, etiquette=etiquette,
            resume=resume[:70], forme=forme, donnees=donnees, details=details,
        ))

    if not exercices:
        raise ValueError(f"{rel} : aucun élément ('vocabulaire', 'conjugaison' ou 'grammaire').")
    vus = set()
    for e in exercices:
        if e.id in vus:
            raise ValueError(f"{rel} : identifiant en double « {e.id} ».")
        vus.add(e.id)

    quota = data.get("nouveaux_par_jour")
    return SetLangue(
        id=rel.with_suffix("").as_posix(),
        langue=langue,
        titre=_texte(data.get("titre")) or rel.stem,
        description=_texte(data.get("description")),
        exercices=exercices,
        particules=[p.lower() for p in _textes(data.get("particules_optionnelles"))],
        caracteres_speciaux=_textes(data.get("caracteres_speciaux")),
        nouveaux_par_jour=quota if isinstance(quota, int) and not isinstance(quota, bool) and quota >= 0 else None,
        path=rel,
    )


def _saisie(consigne, reponses, *, tolerant=False, invite="", prerempli="", tableau=None):
    return {"consigne": consigne, "invite": invite, "reponses": reponses, "tolerant": tolerant,
            "prerempli": prerempli, "tableau": tableau}


# ===========================================================================
# Correction des réponses
# ===========================================================================
JUSTE, ACCENTS, FAUTE, FAUX = "juste", "accents", "faute", "faux"
MESSAGES = {
    JUSTE: "✓ Correct !",
    ACCENTS: "≈ Presque : attention aux accents",
    FAUTE: "≈ Presque : faute de frappe",
    FAUX: "✗ Incorrect",
}
_RANG = {JUSTE: 0, ACCENTS: 1, FAUTE: 2, FAUX: 3}


def note_du_verdict(verdict: str) -> int:
    """Juste → Bien ; presque (accent, faute de frappe) → Difficile ; faux → À revoir."""
    return {JUSTE: fsrs.BIEN, ACCENTS: fsrs.DIFFICILE, FAUTE: fsrs.DIFFICILE}.get(verdict, fsrs.A_REVOIR)


def normaliser_strict(s: str) -> str:
    """Casse, espaces, apostrophes typographiques et ponctuation finale ignorés ;
    accents conservés."""
    s = str(s).strip().lower()
    for c in "’‘`ʼ":
        s = s.replace(c, "'")
    for c in "“”«»":
        s = s.replace(c, '"')
    s = s.rstrip(".!?…;: \t\n\r")
    res = ""
    for mot in s.split():
        # Espace typographique avant « ? ! : ; » (usage français) ignoré.
        if res and not (len(mot) == 1 and mot in "?!:;,"):
            res += " "
        res += mot
    return res


def _sans_particule(s: str, particules) -> str:
    tete, _, reste = s.partition(" ")
    return reste if reste and tete in particules else s


def distance(a: str, b: str) -> int:
    """Distance d'édition (Levenshtein avec transpositions adjacentes)."""
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cout = a[i - 1] != b[j - 1]
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cout)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[len(a)][len(b)]


def noter_saisie(saisie: str, reponses, tolerant: bool, particules=()):
    """Note une réponse tapée. Renvoie (verdict, réponse attendue la plus proche)."""
    s = _sans_particule(normaliser_strict(saisie), particules)
    s_plat = quiz.normaliser_texte(s)
    meilleur = (FAUX, float("inf"), reponses[0] if reponses else "")
    for r in reponses:
        a = _sans_particule(normaliser_strict(r), particules)
        if a == s:
            return JUSTE, r
        a_plat = quiz.normaliser_texte(a)
        dist = distance(s_plat, a_plat)
        if not tolerant:
            verdict = FAUX
        elif dist == 0:
            verdict = ACCENTS
        else:
            n = len(a_plat)
            seuil = 2 if n >= 10 else 1 if n >= 5 else 0
            verdict = FAUTE if dist <= seuil else FAUX
        if (_RANG[verdict], dist) < (_RANG[meilleur[0]], meilleur[1]):
            meilleur = (verdict, dist, r)
    return meilleur[0], meilleur[2]


def diff(saisie: str, attendu: str):
    """Caractères de `attendu`, chacun marqué True s'il correspond à la saisie (plus
    longue sous-séquence commune, casse ignorée) : sert à surligner les différences."""
    a, s = attendu, saisie
    eq = lambda x, y: x.lower() == y.lower()  # noqa: E731
    lcs = [[0] * (len(s) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(s) - 1, -1, -1):
            lcs[i][j] = lcs[i + 1][j + 1] + 1 if eq(a[i], s[j]) else max(lcs[i + 1][j], lcs[i][j + 1])
    i = j = 0
    res = []
    while i < len(a):
        if j < len(s) and eq(a[i], s[j]):
            res.append((a[i], True))
            i += 1
            j += 1
        elif j < len(s) and lcs[i][j + 1] >= lcs[i + 1][j]:
            j += 1
        else:
            res.append((a[i], a[i].isspace()))
            i += 1
    return res


def corriger(set_langue: SetLangue, exo: Exercice, reponse):
    """Corrige une réponse (texte tapé, indices choisis, ou mots dans l'ordre).

    Renvoie {verdict, message, note, attendu, diff, autres} ou None si la réponse
    est incomplète (champ vide, aucun choix, mots non tous placés).
    """
    d = exo.donnees
    if exo.forme == SAISIE:
        saisie = str(reponse or "").strip()
        if not saisie:
            return None
        verdict, attendu = noter_saisie(saisie, d["reponses"], d["tolerant"], set_langue.particules)
    elif exo.forme == CHOIX:
        if not isinstance(reponse, list) or not reponse:
            return None
        verdict, attendu, saisie = (JUSTE if sorted(set(reponse)) == d["reponses"] else FAUX), "", ""
    elif exo.forme == ORDRE:
        if (not isinstance(reponse, list) or sorted(reponse) != list(range(len(d["mots"])))):
            return None
        saisie = " ".join(d["mots"][k] for k in reponse)
        verdict, attendu = noter_saisie(saisie, d["reponses"], False)
    else:
        return None
    reponses = d.get("reponses", [])
    return {
        "verdict": verdict,
        "message": MESSAGES[verdict],
        "note": note_du_verdict(verdict),
        "saisie": saisie,
        "attendu": attendu,
        "diff": diff(saisie, attendu) if exo.forme == SAISIE and verdict != JUSTE else [],
        "autres": [r for r in reponses if r != attendu] if exo.forme == SAISIE else [],
    }


# ===========================================================================
# Suivi FSRS
# ===========================================================================
def _jours_depuis(st, now) -> float:
    return 0.0 if st.last_review is None else max(0.0, (now - st.last_review).total_seconds()) / 86400


def est_nouveau(st) -> bool:
    return st is None or st.stabilite is None


def est_du(st, now) -> bool:
    return st.echeance is None or st.echeance <= now


def retention(st, now) -> float:
    return 0.0 if st.stabilite is None else fsrs.retrievabilite(_jours_depuis(st, now), st.stabilite)


def etat_suivant(st, note: int, now) -> fsrs.Etat:
    if st is not None and st.stabilite is not None and st.difficulte is not None:
        return fsrs.suivante(fsrs.Etat(st.stabilite, st.difficulte), _jours_depuis(st, now), note)
    return fsrs.premiere(note)


def delai(etat: fsrs.Etat, note: int) -> timedelta:
    """Délai avant la prochaine révision : un élément oublié revient dès la
    prochaine session ; sinon l'intervalle FSRS arrondi (au moins un jour)."""
    if note == fsrs.A_REVOIR:
        return timedelta(minutes=10)
    jours = int(fsrs.intervalle_jours(etat.stabilite) + 0.5)
    return timedelta(days=min(36_500, max(1, jours)))


def texte_delai(d: timedelta) -> str:
    """Texte court d'un délai : « 10 min », « 3 j », « 2 mois », « 1,5 an »."""
    jours = d.days
    if jours < 1:
        return f"{int(d.total_seconds() // 60)} min"
    if jours < 31:
        return f"{jours} j"
    if jours < 365:
        return f"{int(jours / 30.4 + 0.5)} mois"
    return f"{jours / 365:.1f} an".replace(".", ",")


def previsions(st, now) -> dict:
    """Délai prévu pour chaque note donnée maintenant (affiché sur les boutons)."""
    return {n: texte_delai(delai(etat_suivant(st, n, now), n)) for n in fsrs.NOTES}


# ===========================================================================
# Sessions
# ===========================================================================
@dataclass
class ExoSession:
    set: SetLangue
    exo: Exercice
    nouveau: bool
    melange: list[int] = field(default_factory=list)  # ordre de présentation des mots (ORDRE)


def debloque(prog, set_langue, exo) -> bool:
    if exo.prerequis is None:
        return True
    st = prog.get((set_langue.id, exo.prerequis))
    return st is not None and st.stabilite is not None and st.last_correct is True


def quota_nouveaux(sets, prog, now) -> int:
    """Nouveaux éléments qu'il reste possible de découvrir aujourd'hui."""
    aujourdhui = timezone.localdate(now)
    quotas = [s.nouveaux_par_jour for s in sets if s.nouveaux_par_jour is not None]
    quota = max(quotas) if quotas else NOUVEAUX_PAR_JOUR
    decouverts = 0
    for s in sets:
        for e in s.exercices:
            st = prog.get((s.id, e.id))
            if st is not None and st.decouverte is not None and timezone.localdate(st.decouverte) == aujourdhui:
                decouverts += 1
    return max(0, quota - decouverts)


def melanger_mots(n: int, hasard=random) -> list[int]:
    """Permutation aléatoire, différente de l'ordre d'origine."""
    m = list(range(n))
    for _ in range(10):
        hasard.shuffle(m)
        if m != sorted(m):
            break
    return m


def _files_par_genre(items):
    files = {g: deque() for g in GENRES}
    for e in items:
        files[e.exo.genre].append(e)
    return files


def _repartir_equitablement(items):
    """Nouveautés prises à tour de rôle dans chaque genre (parts égales)."""
    files = _files_par_genre(items)
    res = []
    while any(files.values()):
        for f in files.values():
            if f:
                res.append(f.popleft())
    return res


def entrelacer(items):
    """Entrelace les genres : chaque genre est réparti uniformément sur la session
    (on puise dans la file la moins avancée proportionnellement), et jamais deux
    exercices du même genre à la suite tant qu'un autre genre est disponible."""
    files = _files_par_genre(items)
    tailles = {g: max(1, len(f)) for g, f in files.items()}
    res = []
    dernier = None
    while True:
        ordre = sorted((g for g in GENRES if files[g]), key=lambda g: -len(files[g]) / tailles[g])
        if not ordre:
            return res
        g = next((x for x in ordre if x != dernier), ordre[0])
        file = files[g]
        # Évite deux formes du même verbe à la suite.
        if res and len(file) > 1 and file[0].exo.entree == res[-1].exo.entree:
            file[0], file[1] = file[1], file[0]
        res.append(file.popleft())
        dernier = g


def construire_session(sets, prog, mode, n, now, hasard=random):
    """Construit une session d'au plus `n` exercices.

    1. révisions dues (échéance passée), les plus menacées d'oubli d'abord ;
    2. nouveautés débloquées, réparties à parts égales entre les genres, dans la
       limite du quota du jour ;
    3. au plus `max_par_session` facettes par élément ;
    4. entrelacement des genres.
    En mode « points faibles » : éléments souvent oubliés ou ratés la dernière fois.
    """
    revues, nouveaux, faibles = [], [], []
    for s in sets:
        for exo in s.exercices:
            if mode in GENRES and exo.genre != mode:
                continue
            st = prog.get((s.id, exo.id))
            item = ExoSession(s, exo, est_nouveau(st))
            if item.nouveau:
                if debloque(prog, s, exo):
                    nouveaux.append(item)
                continue
            r = retention(st, now)
            if mode == FAIBLES:
                if st.oublis > 0 or st.last_correct is False:
                    faibles.append(((-st.oublis, r), item))
            elif est_du(st, now):
                revues.append((r, item))

    if mode == FAIBLES:
        faibles.sort(key=lambda t: t[0])
        candidats = [e for _, e in faibles]
        quota = 0
    else:
        revues.sort(key=lambda t: t[0])
        # Les révisions passent avant la nouveauté, mais une session garde une part
        # de nouveaux éléments (un tiers) quand il y en a.
        quota = quota_nouveaux(sets, prog, now)
        reserve = min(len(nouveaux), max(n // 3, 3), quota)
        nb_revues = min(len(revues), max(0, n - reserve))
        candidats = [e for _, e in revues[:nb_revues]] + _repartir_equitablement(nouveaux)

    # Limite de facettes par entrée (pas « réussir » la production juste après
    # avoir vu la carte du même mot) et quota de nouveautés.
    nb_nouveaux = 0
    par_entree = {}
    choisis = []
    for e in candidats:
        if len(choisis) >= n:
            break
        if e.nouveau and nb_nouveaux >= quota:
            continue
        cle = (e.set.id, e.exo.entree)
        if par_entree.get(cle, 0) < e.exo.max_par_session:
            par_entree[cle] = par_entree.get(cle, 0) + 1
            nb_nouveaux += e.nouveau
            choisis.append(e)

    session = entrelacer(choisis)
    for e in session:
        if e.exo.forme == ORDRE:
            e.melange = melanger_mots(len(e.exo.donnees["mots"]), hasard)
    return session


# ===========================================================================
# Statistiques
# ===========================================================================
def resume(sets, prog, now) -> dict:
    """Par genre : total, nouveaux, à revoir, maîtrisés, rétention estimée ; et
    révisions des 7 prochains jours, éléments les plus souvent oubliés."""
    dans_7j = now + timedelta(days=7)
    genres = {g: {"nom": NOMS_GENRES[g], "total": 0, "nouveaux": 0, "a_revoir": 0, "maitrises": 0,
                  "retention": None, "_somme": 0.0, "_n": 0} for g in GENRES}
    r = {"a_revoir": 0, "nouveaux_disponibles": 0, "sept_jours": 0, "difficiles": []}
    for s in sets:
        for exo in s.exercices:
            rg = genres[exo.genre]
            rg["total"] += 1
            st = prog.get((s.id, exo.id))
            if est_nouveau(st):
                rg["nouveaux"] += 1
                if debloque(prog, s, exo):
                    r["nouveaux_disponibles"] += 1
                continue
            if est_du(st, now):
                rg["a_revoir"] += 1
                r["a_revoir"] += 1
            elif st.echeance <= dans_7j:
                r["sept_jours"] += 1
            if st.stabilite >= MAITRISE_JOURS:
                rg["maitrises"] += 1
            rg["_somme"] += retention(st, now)
            rg["_n"] += 1
            if st.oublis >= 2:
                r["difficiles"].append((exo.resume, st.oublis))
    for rg in genres.values():
        if rg["_n"]:
            rg["retention"] = rg["_somme"] / rg["_n"] * 100
        rg["appris"] = rg["total"] - rg["nouveaux"]
        del rg["_somme"], rg["_n"]
    r["genres"] = [rg for rg in genres.values() if rg["total"]]
    r["nouveaux_disponibles"] = min(r["nouveaux_disponibles"], quota_nouveaux(sets, prog, now))
    r["difficiles"] = sorted(r["difficiles"], key=lambda d: -d[1])[:8]
    return r
