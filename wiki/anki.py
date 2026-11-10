"""Export d'un set de QCM ou d'un paquet de langue vers Anki (.apkg) ou en texte
tabulé (Quizlet, tableur).

Un fichier .apkg est une archive zip : une base SQLite « collection.anki2 » au
format historique d'Anki (version 11, toujours importé par les versions
récentes) et un index « media » (vide ici : les images restent sur le wiki).
Les identifiants (paquet, type de note, notes) sont dérivés du contenu : un
second export du même set met les notes à jour dans Anki au lieu de les
dupliquer.

Comme quiz.py, ce module ne dépend ni des modèles ni des vues.
"""

import hashlib
import html
import io
import json
import re
import sqlite3
import tempfile
import time
import zipfile
from pathlib import Path

from . import langues, quiz

SEPARATEUR_CHAMPS = "\x1f"
_LATEX_PRE = ("\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n"
              "\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n")
_CSS = (".card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }\n"
        ".recto-liste { text-align: left; display: inline-block; margin-top: .6em; }\n"
        ".explication { font-size: 16px; color: #555; margin-top: 1em; }")

_SCHEMA = """
CREATE TABLE col (id integer primary key, crt integer not null, mod integer not null, scm integer not null,
  ver integer not null, dty integer not null, usn integer not null, ls integer not null, conf text not null,
  models text not null, decks text not null, dconf text not null, tags text not null);
CREATE TABLE notes (id integer primary key, guid text not null, mid integer not null, mod integer not null,
  usn integer not null, tags text not null, flds text not null, sfld integer not null, csum integer not null,
  flags integer not null, data text not null);
CREATE TABLE cards (id integer primary key, nid integer not null, did integer not null, ord integer not null,
  mod integer not null, usn integer not null, type integer not null, queue integer not null, due integer not null,
  ivl integer not null, factor integer not null, reps integer not null, lapses integer not null, left integer not null,
  odue integer not null, odid integer not null, flags integer not null, data text not null);
CREATE TABLE revlog (id integer primary key, cid integer not null, usn integer not null, ease integer not null,
  ivl integer not null, lastIvl integer not null, factor integer not null, time integer not null, type integer not null);
CREATE TABLE graves (usn integer not null, oid integer not null, type integer not null);
CREATE INDEX ix_notes_usn ON notes (usn);
CREATE INDEX ix_cards_usn ON cards (usn);
CREATE INDEX ix_revlog_usn ON revlog (usn);
CREATE INDEX ix_cards_nid ON cards (nid);
CREATE INDEX ix_cards_sched ON cards (did, queue, due);
CREATE INDEX ix_revlog_cid ON revlog (cid);
CREATE INDEX ix_notes_csum ON notes (csum);
"""


def _identifiant(*parties):
    """Entier positif stable (31 bits) dérivé d'une clé : identifiants Anki reproductibles."""
    h = hashlib.sha1("\x00".join(parties).encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big") & 0x7FFFFFFF or 1


def _guid(*parties):
    return hashlib.sha1("\x00".join(parties).encode("utf-8")).hexdigest()[:10]


def _csum(champ):
    return int(hashlib.sha1(_strip_html(champ).encode("utf-8")).hexdigest()[:8], 16)


def _strip_html(texte):
    return re.sub(r"<[^>]+>", "", texte)


def formater(texte):
    """Texte du wiki (Markdown léger, LaTeX $...$) vers le HTML d'une carte Anki :
    les formules passent en MathJax (\\(...\\)), que Anki affiche nativement."""
    texte = html.escape(str(texte), quote=False)
    texte = re.sub(r"\$\$(.+?)\$\$", lambda m: "\\[" + m.group(1) + "\\]", texte, flags=re.S)
    texte = re.sub(r"(?<!\\)\$([^$\n]+?)\$", lambda m: "\\(" + m.group(1) + "\\)", texte)
    texte = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texte)
    texte = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?!\w)", r"<i>\1</i>", texte)
    texte = re.sub(r"`([^`\n]+?)`", r"<code>\1</code>", texte)
    return texte.strip().replace("\n", "<br>")


# ---------------------------------------------------------------------------
# Notes à exporter : (recto, verso, inversable)
# ---------------------------------------------------------------------------
def notes_qcm(qset):
    """Notes recto/verso d'un set de QCM : la question (avec ses choix) devant,
    la réponse et l'explication derrière."""
    notes = []
    for q in qset.questions:
        if q.masque:
            continue  # image masquée : l'image reste sur le wiki (pas de médias dans l'export)
        recto = formater(q.enonce)
        if q.consigne:
            recto = f"<i>{formater(q.consigne)}</i><br>{recto}"
        if q.choix:
            lignes = "".join(f"{chr(65 + i)}. {formater(c)}<br>" for i, c in enumerate(q.choix))
            recto += f'<div class="recto-liste">{lignes}</div>'
            verso = ", ".join(f"{chr(65 + i)}. {formater(q.choix[i])}" for i in q.reponses)
        elif q.est_flashcard:
            verso = formater(q.verso)
        else:
            verso = " / ".join(formater(r) for r in q.reponses_texte)
        if q.explication:
            verso += f'<div class="explication">{formater(q.explication)}</div>'
        notes.append((q.id, recto, verso, q.est_flashcard or q.est_qrc))
    return notes


def notes_langue(set_langue, donnees):
    """Notes d'un paquet de langue : le vocabulaire d'après le JSON d'origine (mot,
    traductions, exemple, prononciation), la conjugaison et la grammaire d'après les
    exercices."""
    notes = []
    for i, v in enumerate(donnees.get("vocabulaire") or [], start=1):
        if not isinstance(v, dict) or not v.get("mot"):
            continue
        id_ = str(v.get("id", f"voc{i}"))
        trads = v.get("traductions", v.get("traduction"))
        trads = trads if isinstance(trads, list) else [trads]
        recto = formater(v["mot"])
        if v.get("prononciation"):
            recto += f' <span class="muted">{formater(v["prononciation"])}</span>'
        verso = ", ".join(formater(t) for t in trads if t)
        extra = []
        if v.get("definition"):
            # Liste sans traduction : la définition au dos ; sinon en complément.
            if verso:
                extra.append(f"<i>{formater(v['definition'])}</i>")
            else:
                verso = formater(v["definition"])
        if v.get("exemple"):
            exemple = formater(str(v["exemple"]).replace("[", "<b>").replace("]", "</b>"))
            extra.append(exemple + (f"<br><i>{formater(v['exemple_traduction'])}</i>" if v.get("exemple_traduction") else ""))
        if v.get("note"):
            extra.append(formater(v["note"]))
        if extra:
            verso += '<div class="explication">' + "<br>".join(extra) + "</div>"
        notes.append((id_, recto, verso, True))
    for e in set_langue.exercices:
        if e.genre == langues.VOCABULAIRE:
            continue
        d = e.donnees
        if e.forme == langues.CARTE:
            notes.append((e.id, formater(d["recto"]), formater(d["verso"]), False))
        elif e.forme == langues.SAISIE:
            recto = formater(d["consigne"])
            if d.get("invite"):
                recto += f"<br><b>{formater(d['invite'])}</b>"
            notes.append((e.id, recto, formater(d["reponses"][0]), False))
        elif e.forme == langues.CHOIX:
            lignes = "".join(f"{chr(65 + i)}. {formater(c)}<br>" for i, c in enumerate(d["choix"]))
            verso = ", ".join(f"{chr(65 + i)}. {formater(d['choix'][i])}" for i in d["reponses"])
            notes.append((e.id, formater(d["enonce"]) + f'<div class="recto-liste">{lignes}</div>', verso, False))
        elif e.forme == langues.ORDRE:
            notes.append((e.id, formater(d["consigne"]) + "<br>" + " · ".join(formater(m) for m in d["mots"]),
                          formater(d["reponses"][0]), False))
    return notes


# ---------------------------------------------------------------------------
# Fichiers
# ---------------------------------------------------------------------------
def _modele(mid, nom, did, inverse, maintenant):
    champs = [{"name": n, "ord": i, "sticky": False, "rtl": False, "font": "Arial", "size": 20, "media": []}
              for i, n in enumerate(("Recto", "Verso"))]
    gabarits = [{"name": "Carte 1", "ord": 0, "qfmt": "{{Recto}}", "afmt": "{{FrontSide}}<hr id=answer>{{Verso}}",
                 "bqfmt": "", "bafmt": "", "did": None, "bfont": "", "bsize": 0}]
    req = [[0, "all", [0]]]
    if inverse:
        gabarits.append({"name": "Carte 2", "ord": 1, "qfmt": "{{Verso}}", "afmt": "{{FrontSide}}<hr id=answer>{{Recto}}",
                         "bqfmt": "", "bafmt": "", "did": None, "bfont": "", "bsize": 0})
        req.append([1, "all", [1]])
    return {"id": mid, "name": nom, "type": 0, "mod": maintenant, "usn": -1, "sortf": 0, "did": did,
            "tmpls": gabarits, "flds": champs, "css": _CSS, "latexPre": _LATEX_PRE, "latexPost": "\\end{document}",
            "latexsvg": False, "req": req, "tags": [], "vers": []}


def _deck(did, nom, maintenant, description=""):
    return {"id": did, "name": nom, "mod": maintenant, "usn": -1, "lrnToday": [0, 0], "revToday": [0, 0],
            "newToday": [0, 0], "timeToday": [0, 0], "collapsed": False, "browserCollapsed": False,
            "desc": description, "dyn": 0, "conf": 1, "extendNew": 0, "extendRev": 0}


_DCONF = {"1": {"id": 1, "name": "Default", "replayq": True, "mod": 0, "usn": 0, "autoplay": True, "timer": 0,
                "maxTaken": 60,
                "new": {"perDay": 20, "delays": [1, 10], "separate": True, "ints": [1, 4, 7], "initialFactor": 2500,
                        "bury": True, "order": 1},
                "rev": {"perDay": 200, "fuzz": 0.05, "ivlFct": 1, "maxIvl": 36500, "ease4": 1.3, "bury": True, "minSpace": 1},
                "lapse": {"leechFails": 8, "minInt": 1, "delays": [10], "leechAction": 0, "mult": 0}}}


def apkg(set_id, titre, description, notes):
    """Archive .apkg (octets) d'une liste de notes (id, recto, verso, inversable)."""
    maintenant = int(time.time())
    did = _identifiant("paquet", set_id)
    modeles = {}
    for inverse in (False, True):
        if any(n[3] == inverse for n in notes):
            mid = _identifiant("modele", set_id, "inverse" if inverse else "simple")
            modeles[inverse] = _modele(mid, "ProjetPluri" + (" (et carte inversée)" if inverse else ""), did, inverse, maintenant)
    conf = {"nextPos": len(notes) + 1, "estTimes": True, "activeDecks": [did], "sortType": "noteFld", "timeLim": 0,
            "sortBackwards": False, "addToCur": True, "curDeck": did, "newBury": True, "newSpread": 0,
            "dueCounts": True, "curModel": str(next(iter(modeles.values()))["id"]) if modeles else "", "collapseTime": 1200}
    decks = {"1": _deck(1, "Default", maintenant), str(did): _deck(did, f"ProjetPluri::{titre}", maintenant, description)}

    base = sqlite3.connect(":memory:")
    base.executescript(_SCHEMA)
    base.execute("INSERT INTO col VALUES (1, ?, ?, ?, 11, 0, 0, 0, ?, ?, ?, ?, '{}')",
                 (maintenant - maintenant % 86400, maintenant * 1000, maintenant * 1000, json.dumps(conf),
                  json.dumps({str(m["id"]): m for m in modeles.values()}), json.dumps(decks), json.dumps(_DCONF)))
    base_id = maintenant * 1000
    for position, (id_, recto, verso, inverse) in enumerate(notes):
        nid = base_id + position
        mid = modeles[inverse]["id"]
        base.execute("INSERT INTO notes VALUES (?, ?, ?, ?, -1, '', ?, ?, ?, 0, '')",
                     (nid, _guid(set_id, id_), mid, maintenant, SEPARATEUR_CHAMPS.join((recto, verso)),
                      _strip_html(recto), _csum(recto)))
        for ord_ in range(2 if inverse else 1):
            base.execute("INSERT INTO cards VALUES (?, ?, ?, ?, ?, -1, 0, 0, ?, 0, 0, 0, 0, 0, 0, 0, 0, '')",
                         (base_id + 1_000_000 + position * 2 + ord_, nid, did, ord_, maintenant, position + 1))
    base.commit()
    contenu = io.BytesIO()
    with zipfile.ZipFile(contenu, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("collection.anki2", _dump_sqlite(base))
        archive.writestr("media", "{}")
    base.close()
    return contenu.getvalue()


def _dump_sqlite(base):
    """Octets du fichier SQLite d'une base en mémoire (copie sur disque, puis lecture)."""
    with tempfile.TemporaryDirectory() as dossier:
        chemin = Path(dossier) / "collection.anki2"
        cible = sqlite3.connect(chemin)
        base.backup(cible)
        cible.close()
        return chemin.read_bytes()


def tsv(notes):
    """Texte tabulé (recto, tabulation, verso) : import direct dans Quizlet ou un tableur."""
    lignes = []
    for _, recto, verso, _ in notes:
        r = _strip_html(recto.replace("<br>", " ").replace("<div", " <div"))
        v = _strip_html(verso.replace("<br>", " ").replace('<div class="explication">', " — "))
        lignes.append(" ".join(html.unescape(r).split()) + "\t" + " ".join(html.unescape(v).split()))
    return "\n".join(lignes) + "\n"


def exporter(element, donnees=None):
    """(titre, notes) d'un set de QCM ou d'un paquet de langue (`donnees` : son JSON)."""
    if isinstance(element, quiz.QuestionSet):
        return element.titre, notes_qcm(element)
    return element.titre, notes_langue(element, donnees or {})
