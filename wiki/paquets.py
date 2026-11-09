"""Écriture des fichiers de QCM et de langue dans le coffre (QCM/<dossier>/…).

Commun à la génération par Claude (claude.py) et à l'import de listes de
vocabulaire (CSV Quizlet, Anki) : nom de fichier libre d'après le titre,
validation par les chargeurs, écriture en JSON lisible.
"""

import json
from pathlib import PurePosixPath

from django.utils.text import slugify

from . import langues, quiz
from .vault import INVALID_NAME_RE, get_vault

DOSSIER_QCM = "QCM"


class PaquetInvalide(ValueError):
    """Le fichier ne passe pas le chargeur ; le message est montré tel quel."""


def dossier_valide(nom):
    """Nom de dossier sous QCM/ (un seul niveau), ou None s'il est invalide."""
    nom = " ".join(str(nom).split())
    if not nom or "/" in nom or "\\" in nom or nom.startswith(".") or INVALID_NAME_RE.search(nom):
        return None
    return nom


def chemin_libre(dossier, titre, defaut):
    """QCM/<dossier>/<titre en minuscules>.json, avec « -2 », « -3 »… si le nom est pris."""
    racine = get_vault().root
    base = (slugify(titre) or defaut)[:60]
    for i in range(1, 1000):
        rel = PurePosixPath(DOSSIER_QCM, dossier, f"{base}.json" if i == 1 else f"{base}-{i}.json")
        if not (racine / rel).exists():
            return rel
    raise PaquetInvalide("Aucun nom de fichier libre.")


def enregistrer_json(rel, donnees):
    racine = get_vault().root
    cible = racine / rel
    if not cible.resolve().is_relative_to(racine.resolve()):
        raise PaquetInvalide("Dossier invalide.")
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def ecrire_paquet_langue(dossier, paquet):
    """Valide un fichier de langue et l'écrit ; renvoie son chemin dans le coffre."""
    rel = chemin_libre(dossier, paquet.get("titre", ""), "vocabulaire")
    try:
        langues.set_depuis_json(paquet, rel)
    except ValueError as e:
        raise PaquetInvalide(f"Paquet invalide : {e}") from None
    enregistrer_json(rel, paquet)
    return rel.as_posix()


def ecrire_set_qcm(dossier, set_json):
    """Valide un set de questions et l'écrit ; renvoie son chemin dans le coffre."""
    rel = chemin_libre(dossier, set_json.get("titre", ""), "qcm")
    try:
        quiz.set_depuis_json(set_json, rel)
    except ValueError as e:
        raise PaquetInvalide(f"QCM invalide : {e}") from None
    enregistrer_json(rel, set_json)
    return rel.as_posix()


def paquet_vocabulaire(langue, titre, description, types, fiches, origine):
    """Fichier de langue d'après des fiches {mot, traductions, …} (ids ajoutés)."""
    prefixe = (slugify(titre) or "voc")[:30]
    vus, propres = set(), []
    for fiche in fiches:
        mot = str(fiche.get("mot", "")).strip()
        trads = [t for t in (fiche.get("traductions") or []) if str(t).strip()]
        if not mot or not trads or mot.lower() in vus:
            continue
        vus.add(mot.lower())
        propres.append({"id": f"{prefixe}-{len(propres) + 1:03d}", **{k: v for k, v in fiche.items() if v not in ("", [], None)}})
    paquet = {"langue": langue, "titre": titre, "description": description, "origine": origine,
              "exercices": list(types), "vocabulaire": propres}
    if langues.abreviation(langue) == "EN":
        paquet["particules_optionnelles"] = ["to", "a", "an", "the"]
    return paquet


# -- Listes de mots collées ou exportées (Quizlet, Anki, tableur) --------------------------------

import csv  # noqa: E402
import html as html_  # noqa: E402
import io  # noqa: E402
import re  # noqa: E402

LANGUE_PUIS_FR, FR_PUIS_LANGUE = "langue_fr", "fr_langue"
ORDRES = (LANGUE_PUIS_FR, FR_PUIS_LANGUE)
MAX_LIGNES = 500
_BALISES = re.compile(r"<[^>]+>")


def _propre(cellule):
    """Sans balises HTML (export Anki), entités décodées, espaces normalisés."""
    texte = html_.unescape(_BALISES.sub(" ", str(cellule))).replace("\xa0", " ")
    return " ".join(texte.split())


def _separateur(lignes):
    echantillon = "\n".join(lignes[:30])
    if "\t" in echantillon:
        return "\t"
    try:
        return csv.Sniffer().sniff(echantillon, delimiters=";,|").delimiter
    except csv.Error:
        pass
    if sum(" = " in l or "=" in l for l in lignes) >= max(1, len(lignes) // 2):
        return "="
    return "," if "," in echantillon else ";"


def analyser_liste(texte, ordre=LANGUE_PUIS_FR):
    """Lignes « mot ⇄ traduction » → (fiches {mot, traductions, exemple?, note?}, lignes ignorées).

    Accepte les exports Quizlet et Anki (tabulations, lignes « #… » d'en-tête,
    HTML), un CSV de tableur (virgules, points-virgules, guillemets) ou des
    lignes « mot = traduction ». Un 3e champ devient l'exemple, un 4e la note.
    Plusieurs traductions séparées par « , », « ; » ou « / » ; plusieurs formes
    du mot séparées par « / » (la première est le mot, les autres des variantes).
    """
    lignes = [l for l in texte.replace("\r\n", "\n").split("\n") if l.strip() and not l.lstrip().startswith("#")]
    if len(lignes) > MAX_LIGNES:
        raise PaquetInvalide(f"Trop de lignes ({len(lignes)}) : {MAX_LIGNES} au plus par paquet.")
    if not lignes:
        return [], 0
    sep = _separateur(lignes)
    if sep == "=":
        rangs = [[part.strip() for part in l.split("=", 1)] for l in lignes]
    else:
        rangs = list(csv.reader(io.StringIO("\n".join(lignes)), delimiter=sep, skipinitialspace=True))
    fiches, ignorees = [], 0
    for rang in rangs:
        cellules = [_propre(c) for c in rang]
        cellules = [c for c in cellules if c] + [""] * 2
        if not cellules[0] or not cellules[1]:
            ignorees += 1
            continue
        a, b = cellules[0], cellules[1]
        mot_brut, trad_brut = (a, b) if ordre == LANGUE_PUIS_FR else (b, a)
        formes = [f.strip() for f in mot_brut.split("/") if f.strip()]
        trads = [t.strip() for t in re.split(r"[;,/]", trad_brut) if t.strip()]
        if not formes or not trads:
            ignorees += 1
            continue
        fiche = {"mot": formes[0], "traductions": trads}
        if len(formes) > 1:
            fiche["variantes"] = formes[1:]
        extra = [c for c in cellules[2:] if c]
        if extra:
            fiche["exemple"] = extra[0]
        if len(extra) > 1:
            fiche["note"] = extra[1]
        fiches.append(fiche)
    return fiches, ignorees
