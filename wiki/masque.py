"""Cartes à image masquée (schémas) : une image et des zones rectangulaires ; chaque zone
devient une carte où elle est cachée, et il faut dire ce qu'elle cache.

Dans un set, une question ``"type": "MASQUE"`` :

    {"id": "coeur", "type": "MASQUE", "question": "Que cache la zone colorée ?",
     "image": "Images/coeur.png", "masquer_tout": true,
     "zones": [{"id": "z1", "x": 12.5, "y": 30, "l": 20, "h": 6, "reponse": "Aorte"}]}

Positions et tailles en % de l'image. ``masquer_tout`` : les autres zones sont aussi
cachées (sinon visibles). ``image`` : un fichier du coffre (chemin ou nom, comme un
lien), ou ``perso:<nom>`` pour une image de l'espace personnel du propriétaire du set.
Chaque zone donne une carte (type FLASHCARD) d'identifiant ``<id>#<id de zone>``."""

from pathlib import Path

from django.urls import reverse

from .vault import Attachment, escape

PERSO_IMAGE = "perso:"
DOSSIER_IMAGES_PERSO = "_images"
ENONCE_DEFAUT = "Que cache la zone colorée ?"
FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
TAILLE_MAX_IMAGE = 10 * 1024 * 1024
MAX_ZONES = 60


def questions(q, i, contexte):
    """Les cartes d'une question MASQUE (une par zone). ValueError si malformée."""
    from .quiz import Question

    image = str(q.get("image", "")).strip()
    if not image:
        raise ValueError(f"{contexte} : clé 'image' manquante (image masquée).")
    zones = q.get("zones")
    if not isinstance(zones, list) or not zones:
        raise ValueError(f"{contexte} : 'zones' doit lister au moins une zone.")
    if len(zones) > MAX_ZONES:
        raise ValueError(f"{contexte} : {MAX_ZONES} zones au plus.")
    propres, vus = [], set()
    for k, z in enumerate(zones, 1):
        ctx = f"{contexte} » zone #{k}"
        if not isinstance(z, dict):
            raise ValueError(f"{ctx} : zone invalide.")
        try:
            x, y, l, h = (float(z[c]) for c in ("x", "y", "l", "h"))
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"{ctx} : x, y, l et h (en % de l'image) sont requis.") from None
        if not (0 <= x < 100 and 0 <= y < 100 and 0 < l <= 100 and 0 < h <= 100):
            raise ValueError(f"{ctx} : zone hors de l'image.")
        reponse = str(z.get("reponse", "")).strip()
        if not reponse:
            raise ValueError(f"{ctx} : 'reponse' manquante (ce que cache la zone).")
        zid = str(z.get("id") or f"z{k}").strip()
        if zid in vus or "#" in zid:
            raise ValueError(f"{ctx} : identifiant '{zid}' en double ou invalide.")
        vus.add(zid)
        propres.append({"id": zid, "x": round(x, 2), "y": round(y, 2), "l": round(min(l, 100 - x), 2),
                        "h": round(min(h, 100 - y), 2), "reponse": reponse})
    base = str(q.get("id", f"q{i}"))
    enonce = str(q.get("question") or ENONCE_DEFAUT)
    tout = bool(q.get("masquer_tout", True))
    return [Question(id=f"{base}#{z['id']}", type="FLASHCARD", enonce=enonce, verso=z["reponse"],
                     explication=str(q.get("explication", "")),
                     masque={"image": image, "zones": propres, "cible": z["id"], "tout": tout})
            for z in propres]


def url_image(vault, qset, image):
    """Adresse de l'image d'un set ('' si introuvable)."""
    if image.startswith(PERSO_IMAGE):
        nom = image[len(PERSO_IMAGE):]
        if not qset.proprietaire or not nom or "/" in nom or "\\" in nom:
            return ""
        return reverse("wiki:quiz_perso_image", args=[nom])
    trouve = vault.resolve(image)
    return trouve.url if isinstance(trouve, Attachment) and trouve.suffix in FORMATS else ""


def html(vault, qset, masque):
    """L'image et ses zones (SVG par-dessus, en %) : la zone à deviner en couleur ; un
    clic sur « Retourner » ajoute la classe « revele » (quiz.js) qui la découvre."""
    src = url_image(vault, qset, masque["image"])
    if not src:
        return f'<p class="masque-absente">Image introuvable : {escape(masque["image"])}</p>'
    formes = []
    for z in masque["zones"]:
        cible = z["id"] == masque["cible"]
        if not cible and not masque["tout"]:
            continue
        formes.append(f'<rect x="{z["x"]}%" y="{z["y"]}%" width="{z["l"]}%" height="{z["h"]}%" rx="3" '
                      f'class="{"masque-cible" if cible else "masque-autre"}"/>')
        if cible:
            formes.append(f'<text x="{round(z["x"] + z["l"] / 2, 2)}%" y="{round(z["y"] + z["h"] / 2, 2)}%" '
                          'class="masque-question" text-anchor="middle" dominant-baseline="central">?</text>')
    return (f'<div class="masque" data-masque><img src="{escape(src)}" alt="Schéma : une zone colorée est à deviner" '
            f'loading="lazy"><svg class="masque-zones" aria-hidden="true">{"".join(formes)}</svg></div>')


def nom_libre(dossier, nom):
    """Nom de fichier image sûr et libre dans ``dossier`` (« schema.png », « schema-2.png »…)."""
    chemin = Path(nom)
    suffixe = chemin.suffix.lower()
    from .paquets import slug

    base = (slug(chemin.stem) or "image")[:60]
    for i in range(1, 1000):
        candidat = f"{base}{suffixe}" if i == 1 else f"{base}-{i}{suffixe}"
        if not (Path(dossier) / candidat).exists():
            return candidat
    raise ValueError("Aucun nom de fichier libre.")


def enregistrer_image(fichier, dossier):
    """Vérifie une image envoyée (format, taille, lisible) et l'écrit dans ``dossier``,
    allégée si elle est très grande. Renvoie le nom du fichier ; ValueError sinon."""
    from PIL import Image, UnidentifiedImageError

    from .uploads import alleger_image

    suffixe = Path(fichier.name).suffix.lower()
    if suffixe not in FORMATS:
        raise ValueError("Image PNG, JPEG, WebP ou GIF seulement.")
    if fichier.size > TAILLE_MAX_IMAGE:
        raise ValueError("Image trop grosse (10 Mo au plus).")
    try:
        with Image.open(fichier) as image:
            image.verify()
    except (UnidentifiedImageError, OSError, SyntaxError):
        raise ValueError("Ce fichier n'est pas une image lisible.") from None
    fichier.seek(0)
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    nom = nom_libre(dossier, fichier.name)
    with open(dossier / nom, "wb") as sortie:
        for morceau in fichier.chunks():
            sortie.write(morceau)
    alleger_image(dossier / nom)
    return nom
